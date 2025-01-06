# Mission GPT  
A **Mission Document Retrieval Solution** powered by **Private GPT**, customized and enhanced for efficient and secure data analysis.

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/zylon-ai/private-gpt/blob/main/LICENSE)  
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)  
[![Framework](https://img.shields.io/badge/framework-Private%20GPT-brightgreen)](https://github.com/zylon-ai/private-gpt)

---

## Overview  
**Mission GPT** is an advanced, interactive document retrieval solution designed to streamline the process of extracting precise information from mission-critical documents. The project leverages cutting-edge **Large Language Models (LLMs)**, integrated with **Retrieval-Augmented Generation (RAG)**, and is optimized for a secure and user-friendly experience.

This project is built upon the [Private GPT](https://github.com/zylon-ai/private-gpt) framework with several customizations and enhancements tailored to the requirements of **ISRO's MSSG Department**.

---

## Features  

### Unique Enhancements by Me:
1. **User Authentication System**  
   - Developed a secure login and registration system using **Flask**.  
   - Implemented email-based authentication to ensure only authorized users can access the application.  

2. **Thematic UI Enhancements**  
   - Redesigned the **Gradio interface** to reflect the official **ISRO theme**, ensuring it aligns with the organization's branding.  

3. **Automatic File Management**  
   - Customized the backend to automatically delete ingested files after they are successfully added to their respective sections.  
   - Helps maintain a clean and secure environment for document processing.  

4. **Integration with Advanced LLMs**  
   - Incorporated **Mistral 7B** models and enhanced them further using **Ollama** for improved accuracy and efficiency in retrieving mission-critical data.  

5. **Improved Document Ingestion Process**  
   - Optimized the ingestion process for local documents to handle mission files with improved speed and scalability.  

6. **ISRO-Specific Use Case Customizations**  
   - Tailored the solution specifically for ISRO’s MSSG department to assist in retrieving insights from mission documents with precision.

---

## Installation  

To install and set up the project, you can either follow the basics of the [Private GPT Documentation](https://docs.privategpt.dev/) or directly use the customized **Mission GPT** repository. Below is a guide to both options:  

### Option 1: Clone the Original Private GPT Repository  
1. **Follow the Documentation:**  
   Visit the [Private GPT Documentation](https://docs.privategpt.dev/) for complete instructions on installation, configuration, and usage.  

---

### Option 2: Clone the Mission GPT Repository  
For a customized and pre-configured version tailored to ISRO-specific requirements:  

1. **Clone the Mission GPT Repository:**  
   ```bash  
   git clone https://github.com/pratyushpany/MISSION-GPT.git  
   cd MISSION-GPT  
Set Up the Environment:

bash
Copy code
python3 -m venv env  
source env/bin/activate  # For Linux/Mac  
env\Scripts\activate     # For Windows  
pip install -r requirements.txt  
Ingest Documents:
Add your mission-related documents to the designated folder and run:

bash
Copy code
python ingest.py  
Run the Application:

bash
Copy code
python app.py  
Access the application at http://127.0.0.1:5000 in your browser.

Documentation
For detailed installation, configuration, API details, and deployment instructions, refer to the Private GPT Documentation.

Screenshots
Login and Registration System:
Login Interface:
Registration Interface:
ISRO-Themed Interface (Light Mode):
Application in Light Mode:
Final Interface in Dark Mode with Query Results:
Dark Mode Interface with Query Results:
PrivateGPT Overview
PrivateGPT is a production-ready AI project that enables you to ask questions about your documents using the power of Large Language Models (LLMs), even in environments without an Internet connection. The key advantage is that it is 100% private — no data leaves your execution environment at any point.

The project provides an API that offers all the primitives required to build private, context-aware AI applications. It follows and extends the OpenAI API standard and supports both normal and streaming responses.

API Overview
PrivateGPT provides a high-level API and a low-level API to cater to both basic and advanced users:

High-Level API:

Document Ingestion: Handles document parsing, splitting, metadata extraction, embedding generation, and storage internally.
Chat & Completions: Enables context-based querying using ingested documents, abstracting retrieval, prompt engineering, and response generation.
Low-Level API:

Embeddings Generation: Generates embeddings based on text input.
Contextual Chunks Retrieval: Returns the most relevant chunks of text from ingested documents based on a given query.
Additionally, Gradio UI is provided to easily test the API, along with useful tools like:

Bulk model download script
Ingestion script
Documents folder watch, etc.
Motivation Behind PrivateGPT
Generative AI is transforming industries, but concerns around privacy, especially in data-sensitive domains like healthcare and legal, limit its adoption. PrivateGPT was created to address these privacy concerns by enabling local, offline usage of Large Language Models, ensuring that data remains fully under your control. This project empowers developers to create privacy-focused AI applications without the risk of exposing sensitive information.

The Primordial Version
The first version of PrivateGPT was released in May 2023 as a simpler implementation designed to be a foundation for privacy-sensitive generative AI projects. While it quickly became a popular solution, it has now evolved into a more comprehensive and feature-rich version.

For those interested in experimenting with the primordial version, it is available in the primordial branch.

Note: If you are coming from the primordial version, it's highly recommended to do a clean clone and installation of this new version.

Present and Future of PrivateGPT
PrivateGPT is continuing to evolve, with plans to expand its capabilities to include:

Gateway to generative AI models and primitives.
Enhanced completion capabilities.
More powerful RAG pipelines.
Additional low-level building blocks.
Stay tuned for new releases to discover all the exciting features and changes as the project progresses.

For further details, visit the PrivateGPT GitHub repository.

Tech Stack
Languages: Python
Frameworks: Flask, Gradio
Models Used: Mistral 7B, Ollama
Methodologies: Retrieval-Augmented Generation (RAG)
Acknowledgments
Special thanks to the developers of Private GPT, the backbone of this project. Their innovative framework laid the foundation for building Mission GPT, enabling its advanced functionalities and seamless performance.

Additionally, I extend my gratitude to the MSSG Department, ISRO, for providing me with the opportunity to customize and enhance this framework for mission-critical use cases.

License
This project is licensed under the MIT License. See the LICENSE file for details.

markdown
Copy code

### Summary of Changes:
1. **PrivateGPT Overview**: Added a section detailing the purpose, features, and evolution of **PrivateGPT**.
2. **Motivation and Future**: Included explanations for the motivation behind **PrivateGPT** and its current and future capabilities.
3. **Screenshots**: Included the screenshots you shared for the login system, registration, and the ISRO-themed interface in both light and dark modes.
4. **Link to GitHub**: Added the link to the **PrivateGPT** GitHub repository for further exploration.

Let me know if you'd like any more adjustments!












