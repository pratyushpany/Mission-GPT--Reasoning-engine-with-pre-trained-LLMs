# Mission GPT  
A **Mission Document Retrieval Solution**  customized and enhanced for efficient and secure data analysis.

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
# About PrivateGPT

**PrivateGPT** is a production-ready AI project that enables you to ask questions about your documents using the power of Large Language Models (LLMs), even without an internet connection. It ensures 100% privacy, with no data leaving your execution environment at any point.

The project provides an API offering all the required primitives to build private, context-aware AI applications. It follows and extends the OpenAI API standard, supporting both normal and streaming responses.

### API Overview

The API is divided into two logical blocks:

1. **High-level API**:  
   - **Ingestion of Documents**: Handles document parsing, splitting, metadata extraction, embedding generation, and storage.  
   - **Chat & Completions using Context from Ingested Documents**: Abstracts the retrieval of context, prompt engineering, and response generation.

2. **Low-level API**:  
   - **Embeddings Generation**: Generates embeddings from text.  
   - **Contextual Chunks Retrieval**: Given a query, returns the most relevant chunks of text from the ingested documents.

In addition, a working **Gradio UI client** is provided to test the API. It includes useful tools such as a bulk model download script, ingestion script, and documents folder watch, etc.

---

### Motivation Behind PrivateGPT

Generative AI is transformative, but industries like healthcare and legal are cautious about adopting AI tools due to privacy concerns. The risk of using third-party AI services that might not guarantee full data control is unacceptable for these sectors.

PrivateGPT addresses these concerns by allowing the use of LLMs in an offline environment, ensuring privacy and control over the data. It is a solution designed for privacy-sensitive environments.

---

### Primordial Version

The first version of PrivateGPT was launched in May 2023 as an educational tool to build fully local and private chatGPT-like solutions. This version quickly became a go-to solution for privacy-sensitive setups and laid the foundation for what PrivateGPT has become today.

If you wish to continue experimenting with the original version, it is available in the **primordial branch** of the project.

**Recommendation**: It is strongly advised to perform a clean clone and install of the latest version of PrivateGPT if you are transitioning from the primordial version.

---

### Present and Future of PrivateGPT

PrivateGPT is continuously evolving to become a gateway for generative AI models and primitives. These include completions, document ingestion, RAG pipelines, and other low-level building blocks. Our goal is to make it easier for developers to build AI applications while providing a robust architecture for the community to contribute to.

Stay tuned for updates and new features in upcoming releases.

---

For further details, visit the official [PrivateGPT GitHub Repository](https://github.com/zylon-ai/private-gpt).

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
   ```  

2. **Set Up the Environment:**  
   ```bash  
   python3 -m venv env  
   source env/bin/activate  # For Linux/Mac  
   env\Scripts\activate     # For Windows  
   pip install -r requirements.txt  
   ```  

3. **Ingest Documents:**  
   Add your mission-related documents to the designated folder and run:  
   ```bash  
   python ingest.py  
   ```  

4. **Run the Application:**  
   ```bash  
   python app.py  
   ```  
   Access the application at `http://127.0.0.1:5000` in your browser.

---

## Documentation  
For detailed installation, configuration, API details, and deployment instructions, refer to the [Private GPT Documentation](https://docs.privategpt.dev/).  

---

## Screenshots  
## Images of the Application

### Login Page (Built using Flask)
![Login Page](https://drive.google.com/uc?export=view&id=1i5A74kysw8VK6LGhRaxCn0w_Bcx_50vF)

### Registration Page (Built using Flask)
![Registration Page](https://drive.google.com/uc?export=view&id=1mQ6T2EuQcGmCz1wC77_Vb8hYLH1Igas-)

### Main Interface (Light Mode)
![Main Interface Light Mode](https://drive.google.com/file/d/1dyks-R8Yp-lb6JLSpcXOIdIaUgKUSFkQ/view?usp=sharing)

### Main Interface (Dark Mode with Query and Result)
![Main Interface Dark Mode](https://drive.google.com/file/d/1TSxSGn9UUK1xQ44qqwe0d_YSqS5rZFdG/view?usp=sharing)


## Tech Stack  

- **Languages:** Python  
- **Frameworks:** Flask, Gradio  
- **Models Used:** Mistral 7B, Ollama  
- **Methodologies:** Retrieval-Augmented Generation (RAG)  

---

## Acknowledgments  

Special thanks to the developers of [Private GPT](https://github.com/zylon-ai/private-gpt), the backbone of this project. Their innovative framework laid the foundation for building Mission GPT, enabling its advanced functionalities and seamless performance.  

Additionally, I extend my gratitude to the **MSSG Department, ISRO**, for providing me with the opportunity to customize and enhance this framework for mission-critical use cases.  

---

## License  

This project is licensed under the MIT License. See the [LICENSE](https://github.com/zylon-ai/private-gpt/blob/main/LICENSE) file for details.
