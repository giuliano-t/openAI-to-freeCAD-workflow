# OpenAI to FreeCAD: A Text-to-CAD Generation Pipeline

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/giuliano-t/openAI-to-freeCAD-workflow/blob/main/Full_Pipeline_v05_RAG_For_GitHub.ipynb)

An end-to-end pipeline that converts natural language descriptions into 3D CAD models. This project leverages advanced prompt engineering, Retrieval-Augmented Generation (RAG), and few-shot learning to generate executable FreeCAD Python scripts, which are then used to build and visualize the final 3D model.

This project demonstrates how LLMs can bridge natural language and CAD software, making 3D design accessible to non-experts and accelerating prototyping. 

## ✨ Features

* **Natural Language to 3D Model:** Describe a 3D object in plain English and get a `.stl` file.
* **Advanced Prompt Engineering:** A two-step process refines the user's casual request into a structured, machine-friendly brief.
* **Hybrid RAG + Few-Shot Learning:** The pipeline uses a custom knowledge base of expert-written code snippets (RAG) to correct common AI mistakes, alongside complete examples (few-shot) to guide the overall script structure.
* **Headless FreeCAD Execution:** The notebook installs and runs a command-line version of FreeCAD to execute the generated script.
* **Automatic Visualization:** The final `.stl` model is automatically displayed in both an interactive 3D viewer and a 6-view orthographic projection plot.

---

## 🔧 How It Works

The project follows a multi-step pipeline to ensure high-quality and reliable output.

**`User Prompt -> [LLM] Prompt Refiner -> Structured Brief -> [LLM] Code Generator (RAG + Few-Shot) -> FreeCAD Script -> [FreeCAD] 3D Model -> Visualization`**

In simple terms: you describe an object → the AI writes a FreeCAD script → the script runs in FreeCAD → you get a 3D model you can view or export.

1.  **Initial Prompt:** The user provides a natural language description of the desired 3D object.
2.  **Meta-Prompting:** The first LLM call acts as a "Prompt Engineer," taking the user's text and converting it into a structured, unambiguous design brief with precise parameters.
3.  **Hybrid Prompt Construction:** The structured brief is combined with two high-quality, complete examples (few-shot learning) and several highly relevant code snippets retrieved from a custom knowledge base (RAG). This "master prompt" contains all the context the AI needs.
4.  **Code Generation:** The master prompt is sent to `gpt-4o`, which generates a complete, executable FreeCAD Python script.
5.  **Execution:** The notebook saves the generated script to a `.py` file and executes it using a headless version of FreeCAD, which creates the final `.stl` model.
6.  **Visualization:** The notebook loads the `.stl` file and displays it using the `trimesh` library.

---

## ⚙️ Setup and Usage

This project is designed to run easily in **Google Colab**, but you can also run it locally if you prefer.

1. **Open in Colab**  
   Click the "Open in Colab" badge at the top of this README.

2. **Add Your OpenAI API Key**  
You can provide your key in **one** of the following ways:

   - **Colab (recommended):**
     - Click the **Key icon (Secrets)** in the left sidebar.
     - Create a new secret with the name `OPENAI_API_KEY`.
     - Paste your key as the value and enable "Notebook access".
     - 👉 Alternative: instead of using Secrets, you can create a `.env` file in Colab (folder icon → right-click → **New file**) with the line:
       ```bash
       OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
       ```
       or simply run in a cell:
       ```python
       %env OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
       ```

   - **Local (optional):**
     - Install FreeCAD manually:
       - Ubuntu: `sudo apt-get install freecad`
       - macOS: `brew install --cask freecad`
       - Conda (cross-platform): `conda install -c conda-forge freecad`
     - Copy `.env.example` to `.env`.
     - Open `.env` in a text editor and replace the placeholder with your real API key.

3. **Run the Notebook**  
   - In Colab, just run all cells top to bottom.  
   - Locally, open the notebook in Jupyter or VS Code and do the same.

## 🛠️ Technologies Used

* **AI & Prompting:** OpenAI API (GPT-4o), LangChain, Few-Shot Learning
* **Retrieval-Augmented Generation (RAG):** FAISS Vector Store
* **CAD Engine:** FreeCAD
* **3D Visualization:** Trimesh, Matplotlib
* **Environment:** Google Colab, Python

## 📋 Requirements
- OpenAI API key (create one at [platform.openai.com](https://platform.openai.com/))  
- Python 3.9+  
- FreeCAD 0.21+ (installed automatically in Colab, or manually for local use)  

## ⚠️ Disclaimer
This is a research prototype. It executes AI-generated FreeCAD code in a headless subprocess (`freecadcmd`).  
While it is safer than running inline code, please review generated scripts before using them in sensitive or production environments.

## 📜 License
MIT License. See [LICENSE](LICENSE) for details.
