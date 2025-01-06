"""This file should be imported if and only if you want to run the UI locally."""

import itertools
import logging
import time
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import requests
import gradio as gr  # type: ignore
from fastapi import FastAPI
from gradio import themes
from gradio.themes.utils.colors import slate  # type: ignore
from injector import inject, singleton
from llama_index.core.llms import ChatMessage, ChatResponse, MessageRole
from pydantic import BaseModel

from private_gpt.constants import PROJECT_ROOT_PATH
from private_gpt.di import global_injector
from private_gpt.open_ai.extensions.context_filter import ContextFilter
from private_gpt.server.chat.chat_service import ChatService, CompletionGen
from private_gpt.server.chunks.chunks_service import Chunk, ChunksService
from private_gpt.server.ingest.ingest_service import IngestService
from private_gpt.settings.settings import settings
from private_gpt.ui.images import logo_svg


#theam
import os
import pathlib

from gradio.themes.utils import ThemeAsset

uname = "Guest"

def create_theme_dropdown():
    import gradio as gr

    asset_path = pathlib.Path(__file__).parent / "themes"
    themes = []
    for theme_asset in os.listdir(str(asset_path)):
        themes.append(
            (ThemeAsset(theme_asset), gr.Theme.load(str(asset_path / theme_asset)))
        )

    def make_else_if(theme_asset):
        return f"""
        else if (theme == '{str(theme_asset[0].version)}') {{
            var theme_css = `{theme_asset[1]._get_theme_css()}`
        }}"""
 
    head, tail = themes[0], themes[1:]
    if_statement = f"""
        if (theme == "{str(head[0].version)}") {{
            var theme_css = `{head[1]._get_theme_css()}`
        }} {" ".join(make_else_if(t) for t in tail)}
    """

    latest_to_oldest = sorted([t[0] for t in themes], key=lambda asset: asset.version)[
        ::-1
    ]
    latest_to_oldest = [str(t.version) for t in latest_to_oldest]

    component = gr.Dropdown(
        choices=latest_to_oldest,
        value=latest_to_oldest[0],
        render=False,
        label="Select Version",
    )

    return (
        component,
        f"""
        (theme) => {{
            if (!document.querySelector('.theme-css')) {{
                var theme_elem = document.createElement('style');
                theme_elem.classList.add('theme-css');
                document.head.appendChild(theme_elem);
            }} else {{
                var theme_elem = document.querySelector('.theme-css');
            }}
            {if_statement}
            theme_elem.innerHTML = theme_css;
        }}
    """,
    )


dropdown, js = create_theme_dropdown()

# def get_fact():
#     response = requests.get('http://127.0.0.1:5000/get_fact')
#     fact = response.json()['fact']
#     return fact


def echo(text, request: gr.Request):
    if request:
        # print("Request headers dictionary:", request.headers)
        # print("IP address:", request.client.host)
        # print("Query parameters:", dict(request.query_params))
        return request.query_params['username']
    else:   
        return ""

def get_logged_in_user_name():
    # try:
    #     response = requests.get("http://127.0.0.1:5000/get_logged_in_user_name")
    #     if response.status_code == 200:
    #         data = response.json()
    #         return data['username']
    #     else:
    #         return "Guest"
    # except Exception as e:
    #     return "Guest"
    # uname = echo()
    return uname




logger = logging.getLogger(__name__)


THIS_DIRECTORY_RELATIVE = Path(__file__).parent.relative_to(PROJECT_ROOT_PATH)
# Should be "private_gpt/ui/ISRO.ico"
AVATAR_BOT = THIS_DIRECTORY_RELATIVE / "ISRO.ico"

UI_TAB_TITLE = "Mission GPT"

SOURCES_SEPARATOR = "\n\n Sources: \n"

MODES = ["Query Files", "Search Files"]




class Source(BaseModel):
    file: str
    page: str
    text: str

    class Config:
        frozen = True

    @staticmethod
    def curate_sources(sources: list[Chunk]) -> list["Source"]:
        curated_sources = []

        for chunk in sources:
            doc_metadata = chunk.document.doc_metadata

            file_name = doc_metadata.get("file_name", "-") if doc_metadata else "-"
            page_label = doc_metadata.get("page_label", "-") if doc_metadata else "-"

            source = Source(file=file_name, page=page_label, text=chunk.text)
            curated_sources.append(source)
            curated_sources = list(
                dict.fromkeys(curated_sources).keys()
            )  # Unique sources only

        return curated_sources


@singleton
class PrivateGptUi:
    
    @inject
    def __init__(
        self,
        ingest_service: IngestService,
        chat_service: ChatService,
        chunks_service: ChunksService,
    ) -> None:
        self._ingest_service = ingest_service
        self._chat_service = chat_service
        self._chunks_service = chunks_service

        # Cache the UI blocks
        self._ui_block = None

        self._selected_filename = None

        # Initialize system prompt based on default mode
        self.mode = MODES[0]
        self._system_prompt = self._get_default_system_prompt(self.mode)

    def _chat(self, message: str, history: list[list[str]], mode: str, *_: Any) -> Any:
        def yield_deltas(completion_gen: CompletionGen) -> Iterable[str]:
            full_response: str = ""
            stream = completion_gen.response
            for delta in stream:
                if isinstance(delta, str):
                    full_response += str(delta)
                elif isinstance(delta, ChatResponse):
                    full_response += delta.delta or ""
                yield full_response
                time.sleep(0.02)

            if completion_gen.sources:
                full_response += SOURCES_SEPARATOR
                cur_sources = Source.curate_sources(completion_gen.sources)
                sources_text = "\n\n\n"
                used_files = set()
                for index, source in enumerate(cur_sources, start=1):
                    if f"{source.file}-{source.page}" not in used_files:
                        sources_text = (
                            sources_text
                            + f"{index}. {source.file} (page {source.page}) \n\n"
                        )
                        used_files.add(f"{source.file}-{source.page}")
                full_response += sources_text
            yield full_response

        def build_history() -> list[ChatMessage]:
            history_messages: list[ChatMessage] = list(
                itertools.chain(
                    *[
                        [
                            ChatMessage(content=interaction[0], role=MessageRole.USER),
                            ChatMessage(
                                # Remove from history content the Sources information
                                content=interaction[1].split(SOURCES_SEPARATOR)[0],
                                role=MessageRole.ASSISTANT,
                            ),
                        ]
                        for interaction in history
                    ]
                )
            )

            # max 20 messages to try to avoid context overflow
            return history_messages[:20]

        new_message = ChatMessage(content=message, role=MessageRole.USER)
        all_messages = [*build_history(), new_message]
        # If a system prompt is set, add it as a system message
        if self._system_prompt:
            all_messages.insert(
                0,
                ChatMessage(
                    content=self._system_prompt,
                    role=MessageRole.SYSTEM,
                ),
            )
        match mode:
            case "Query Files":

                # Use only the selected file for the query
                context_filter = None
                if self._selected_filename is not None:
                    docs_ids = []
                    for ingested_document in self._ingest_service.list_ingested():
                        if (
                            ingested_document.doc_metadata["file_name"]
                            == self._selected_filename
                        ):
                            docs_ids.append(ingested_document.doc_id)
                    context_filter = ContextFilter(docs_ids=docs_ids)

                query_stream = self._chat_service.stream_chat(
                    messages=all_messages,
                    use_context=True,
                    context_filter=context_filter,
                )
                yield from yield_deltas(query_stream)
            
            case "Search Files":
                response = self._chunks_service.retrieve_relevant(
                    text=message, limit=4, prev_next_chunks=0
                )

                sources = Source.curate_sources(response)

                yield "\n\n\n".join(
                    f"{index}. **{source.file} "
                    f"(page {source.page})**\n "
                    f"{source.text}"
                    for index, source in enumerate(sources, start=1)
                )

    # On initialization and on mode change, this function set the system prompt
    # to the default prompt based on the mode (and user settings).
    @staticmethod
    def _get_default_system_prompt(mode: str) -> str:
        p = ""
        match mode:
            # For query chat mode, obtain default system prompt from settings
            case "Query Files":
                p = settings().ui.default_query_system_prompt
            # For chat mode, obtain default system prompt from settings
            
            # For any other mode, clear the system prompt
            case _:
                p = ""
        return p

    def _set_system_prompt(self, system_prompt_input: str) -> None:
        logger.info(f"Setting system prompt to: {system_prompt_input}")
        self._system_prompt = system_prompt_input

    def _set_current_mode(self, mode: str) -> Any:
        self.mode = mode
        self._set_system_prompt(self._get_default_system_prompt(mode))
        # Update placeholder and allow interaction if default system prompt is set
        if self._system_prompt:
            return gr.update(placeholder=self._system_prompt, interactive=True)
        # Update placeholder and disable interaction if no default system prompt is set
        else:
            return gr.update(placeholder=self._system_prompt, interactive=False)

    def _list_ingested_files(self) -> list[list[str]]:
        files = set()
        for ingested_document in self._ingest_service.list_ingested():
            if ingested_document.doc_metadata is None:
                # Skipping documents without metadata
                continue
            file_name = ingested_document.doc_metadata.get(
                "file_name", "[FILE NAME MISSING]"
            )
            files.add(file_name)
        return [[row] for row in files]

    def _upload_file(self, files: list[str]) -> None:
        logger.debug("Loading count=%s files", len(files))
        paths = [Path(file) for file in files]

        # remove all existing Documents with name identical to a new file upload:
        file_names = [path.name for path in paths]
        doc_ids_to_delete = []
        for ingested_document in self._ingest_service.list_ingested():
            if (
                ingested_document.doc_metadata
                and ingested_document.doc_metadata["file_name"] in file_names
            ):
                doc_ids_to_delete.append(ingested_document.doc_id)
        if len(doc_ids_to_delete) > 0:
            logger.info(
                "Uploading file(s) which were already ingested: %s document(s) will be replaced.",
                len(doc_ids_to_delete),
            )
            for doc_id in doc_ids_to_delete:
                self._ingest_service.delete(doc_id)

        self._ingest_service.bulk_ingest([(str(path.name), path) for path in paths])

    def _delete_all_files(self) -> Any:
        ingested_files = self._ingest_service.list_ingested()
        logger.debug("Deleting count=%s files", len(ingested_files))
        for ingested_document in ingested_files:
            self._ingest_service.delete(ingested_document.doc_id)
        return [
            gr.List(self._list_ingested_files()),
            gr.components.Button(interactive=False),
            gr.components.Button(interactive=False),
            gr.components.Textbox("All files"),
        ]
    
    def _delete_user_files(self) -> Any:
        master_files = ['ps1als.txt']
        ingested_files = self._ingest_service.list_ingested()
        logger.debug("Deleting count=%s files", len(ingested_files))
        for ingested_document in ingested_files:
            if ingested_document.doc_metadata["file_name"] not in master_files:
                self._ingest_service.delete(ingested_document.doc_id)

    def _delete_selected_file(self) -> Any:
        logger.debug("Deleting selected %s", self._selected_filename)
        # Note: keep looping for pdf's (each page became a Document)
        for ingested_document in self._ingest_service.list_ingested():
            if (
                ingested_document.doc_metadata
                and ingested_document.doc_metadata["file_name"]
                == self._selected_filename
            ):
                self._ingest_service.delete(ingested_document.doc_id)
        return [
            gr.List(self._list_ingested_files()),
            gr.components.Button(interactive=False),
            gr.components.Button(interactive=False),
            gr.components.Textbox("All files"),
        ]

    def _deselect_selected_file(self) -> Any:
        self._selected_filename = None
        return [
            gr.components.Button(interactive=False),
            gr.components.Button(interactive=False),
            gr.components.Textbox("All files"),
        ]

    def _selected_a_file(self, select_data: gr.SelectData) -> Any:
        self._selected_filename = select_data.value
        return [
            gr.components.Button(interactive=True),
            gr.components.Button(interactive=True),
            gr.components.Textbox(self._selected_filename),
        ]

    def _build_ui_blocks(self) -> gr.Blocks:
        logger.debug("Creating the UI blocks")
        with gr.Blocks(
            title=UI_TAB_TITLE,
          theme='snehilsanyal/scikit-learn',
                      css=".logo-container { "
            "display: flex;"
            "justify-content: center;"
            "align-items: center;"
            "padding: 17px;"
            "background: linear-gradient(135deg, #24578E, #FF7F11);"    
            "border-radius: 8px;"
            "box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);"
            "transition: background-color 0.3s;"
            "box-sizing: border-box;"
            "}"

            ".contain { display: flex !important; flex-direction: column !important; }"
        "#component-0, #component-3, #component-10, #component-8  { height: 100% !important; }"
        "#chatbot { flex-grow: 1 !important; overflow: auto !important;}"
        "#col { height: calc(100vh - 112px - 16px) !important; }"

        ".logo { "
            "display:flex;"
            "align-items: center;"
            "}"
        ".logo img {"
            "height: 85px;"
            "width: auto;"
            "margin-right: 75px;"
            "border-radius: 50%;"
            "box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);"
            "transition: transform 0.3s ease-in-out;"
            "align-items: left;"
            "}"

              ".logo:hover img {"
            "transform: scale(1.1);"
            "}"
        ".logo h1 {"
            "font-size: 45px;"
            "color: white;"
            "text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);"
            "margin-left: 10px;" 
            "font-family: 'Montserrat', sans-serif;"
            "font-weight: 600;"
            "line-height: 1.2;"
            "letter-spacing: 1px;"  
            "position: relative;"
            "transition: color 0.5s ease, transform 0.5s ease;"
            "}"

            ".logo h1:hover {"
              "transform: scale(1.1); "
              "}"

   
    ) as blocks:
            with gr.Row():
                logo_html = gr.HTML(f"""
                    <div class='logo-container'>
                        <div class='logo'>
                            <img src={logo_svg} alt=PrivateGPT>
                            <h1>Mission GPT</h1>
                        </div>
                        
                """)
           
            with gr.Row(equal_height=False):
                with gr.Column(scale=3):
                    mode = gr.Radio(
                        MODES,
                        label="Mode",
                        value="Query Files",
                    )
                    
                    upload_button = gr.components.UploadButton(
                        "Upload File(s)",
                        type="filepath",
                        file_count="multiple",
                        size="sm",
                    )
                    
                    ingested_dataset = gr.List(
                        self._list_ingested_files,
                        headers=["File name"],
                        label="Ingested Files",
                        height=235,
                        interactive=False,
                        render=False,  # Rendered under the button
                    )
                    upload_button.upload(
                        self._upload_file,
                        inputs=upload_button,
                        outputs=ingested_dataset,
                    )
                    ingested_dataset.change(
                        self._list_ingested_files,
                        outputs=ingested_dataset,
                    )
                    ingested_dataset.render()
                    deselect_file_button = gr.components.Button(
                        "De-select selected file", size="sm", interactive=False
                    )
                    selected_text = gr.components.Textbox(
                        "All files", label="Selected for Query or Deletion", max_lines=1
                    )
                    delete_file_button = gr.components.Button(
                        "🗑️ Delete selected file",
                        size="sm",
                        visible=settings().ui.delete_file_button_enabled,
                        interactive=False,
                    )
                    delete_files_button = gr.components.Button(
                        "⚠️ Delete ALL files",
                        size="sm",
                        visible=settings().ui.delete_all_files_button_enabled,
                    )
                    deselect_file_button.click(
                        self._deselect_selected_file,
                        outputs=[
                            delete_file_button,
                            deselect_file_button,
                            selected_text,
                        ],
                    )
                    ingested_dataset.select(
                        fn=self._selected_a_file,
                        outputs=[
                            delete_file_button,
                            deselect_file_button,
                            selected_text,
                        ],
                    )
                    delete_file_button.click(
                        self._delete_selected_file,
                        outputs=[
                            ingested_dataset,
                            delete_file_button,
                            deselect_file_button,
                            selected_text,
                        ],
                    )
                    delete_files_button.click(
                        self._delete_all_files,
                        outputs=[
                            ingested_dataset,
                            delete_file_button,
                            deselect_file_button,
                            selected_text,
                        ],
                    )
                    system_prompt_input = gr.Textbox(
                        placeholder=self._system_prompt,
                        label="System Prompt",
                        lines=2,
                        interactive=True,
                        render=False,
                    )
                    # When mode changes, set default system prompt
                    mode.change(
                        self._set_current_mode, inputs=mode, outputs=system_prompt_input
                    )
                    # On blur, set system prompt to use in queries
                    system_prompt_input.blur(
                        self._set_system_prompt,
                        inputs=system_prompt_input,
                    )
               
                   
                  
                    spcae=gr.Row([]) 
                    
                    with gr.Tab("               🌏 🚀 🛰️             "):
                        with gr.Row():
                         import random

                        # welcome_sentences = [
                        #     "Welcome, cosmic explorer! Let's embark on a stellar journey of conversation!",
                        #     "Greetings, space cadet! Ready to launch into an intergalactic exchange?",
                        #     "Hello, stargazer! Let's orbit around some fascinating topics together!",
                        #     "Welcome aboard, space voyager! Let's navigate the universe of ideas!",
                        #     "Ahoy, fellow astronaut! Prepare for liftoff into the realm of discussion!",
                        #     "Welcome, star seeker! Let's dive into the cosmic sea of knowledge!",
                        #     "Greetings, celestial traveler! Let's explore the galaxy of conversation!",
                        #     "Hello, space enthusiast! Buckle up for a warp-speed exchange of ideas!",
                        #     "Welcome, cosmic wanderer! Let's traverse the galaxies of thought together!",
                        #     "Greetings, space aficionado! Let's rocket into a universe of dialogue!"
                        # ]

                      
                        # random_welcome_sentence = random.choice(welcome_sentences)
                    
                        # {get_logged_in_user_name()}   
                        #                                               

                        welcome_sentences="Welcome to Mission GPT! Let's explore space!"
                        # username_output = gr.HTML(f"<b style='font-family: Orbitron, sans-serif; font-size: 14px; color: #777777'> {welcome_sentences}</b>")

                                                
                        txt = gr.components.Textbox(visible=False)
                        txt_3 = gr.components.Textbox(label="Welcome to Mission GPT! Let's explore space!")
                        btn = gr.Button(value="Submit",elem_id="button",visible=False)
                        btn.click(echo, inputs=[txt], outputs=[txt_3])
                        
                        # io = gr.Interface(echo, inputs=gr.components.Textbox(visible=False),outputs= gr.components.Textbox(label="hello"),allow_flagging="never",clear_btn="never")
                        
                        logout_button = gr.Button(
                            "Logout",
                            size="lg",
                            visible=True,
                        )
                        logout_button.click(
                            self._delete_user_files,
                            None,
                            None,   
                                            js="""
                            () => {
                                window.location.assign('http://127.0.0.1:5000/logout');
                                }
                                """,)
                        toggle_dark = gr.Button(value="Toggle Light Mode",min_width=30)
                        dropdown.change(None, dropdown, None, js=js)
                        toggle_dark.click(
                            None,
                            js="""
                            () => {
                                document.body.classList.toggle('dark');
                                document.querySelector('gradio-app').style.backgroundColor = 'var(--color-    background-primary)'
                                }
                                """,
                                )
                        

                    def get_model_label() -> str | None:
                        """Get model label from llm mode setting YAML.

                        Raises:
                            ValueError: If an invalid 'llm_mode' is encountered.

                        Returns:
                            str: The corresponding model label.
                        """
                        # Get model label from llm mode setting YAML
                        # Labels: local, openai, openailike, sagemaker, mock, ollama
                        config_settings = settings()
                        if config_settings is None:
                            raise ValueError("Settings are not configured.")

                        # Get llm_mode from settings
                        llm_mode = config_settings.llm.mode

                        # Mapping of 'llm_mode' to corresponding model labels
                        model_mapping = {
                            "llamacpp": config_settings.llamacpp.llm_hf_model_file,
                            "openai": config_settings.openai.model,
                            "openailike": config_settings.openai.model,
                            "sagemaker": config_settings.sagemaker.llm_endpoint_name,
                            "mock": llm_mode,
                            "ollama": config_settings.ollama.llm_model,
                        }

                        if llm_mode not in model_mapping:
                            print(f"Invalid 'llm mode': {llm_mode}")
                            return None

                        return model_mapping[llm_mode]

                with gr.Column(scale=7, elem_id="col"):
                  

                    # Determine the model label based on the value of PGPT_PROFILES
                    model_label = get_model_label()
                    if model_label is not None:
                        label_text = (
                            f"LLM: {settings().llm.mode} | Model: {model_label}"
                        )
                    else:
                        label_text = f"LLM: {settings().llm.mode}"
                    _ = gr.ChatInterface(
                        self._chat,
                        chatbot=gr.Chatbot(
                            label=label_text,
                            show_copy_button=True,
                            elem_id="chatbot",
                            render=False,
                            avatar_images=(
                                None,
                                AVATAR_BOT,
                            ),
                        ),
                        additional_inputs=[mode, upload_button, system_prompt_input],
                    )
            blocks.load(None,None,None,js = """
                            function my_func(){
                            document.body.classList.toggle('dark');
                            document.querySelector('gradio-app').style.backgroundColor = 'var(--color-    background-primary)';
                            document.getElementById("button").click();
                            }
                            """)           
        return blocks

    def get_ui_blocks(self) -> gr.Blocks:
        if self._ui_block is None:
            self._ui_block = self._build_ui_blocks()
        return self._ui_block

    def mount_in_app(self, app: FastAPI, path: str) -> None:
        blocks = self.get_ui_blocks()
        blocks.queue()
        logger.info("Mounting the gradio UI, at path=%s", path)
        gr.mount_gradio_app(app, blocks, path=path)


        

if __name__ == "__main__":
    ui = global_injector.get(PrivateGptUi)
    _blocks = ui.get_ui_blocks()
    _blocks.queue()
    _blocks.launch(debug=False, show_api=False)
    