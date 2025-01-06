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
### Login and Registration System:  
*(Insert screenshot here)*  

### ISRO-Themed Interface:  
*(Insert screenshot here)*  

### Document Query Results:  
*(Insert screenshot here)*  

---

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
