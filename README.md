# openAI-to-freeCAD-workflow
This project uses a Large Language Model (LLM) with Retrieval-Augmented Generation (RAG) to convert natural language descriptions into executable FreeCAD Python scripts for 3D modeling.

# OpenAI to FreeCAD: A Text-to-CAD Generation Pipeline

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/giuliano-t/openAI-to-freeCAD-workflow/blob/main/Full_Pipeline_v05_RAG_For_GitHub.ipynb)

An end-to-end pipeline that converts natural language descriptions into 3D CAD models. This project leverages advanced prompt engineering, Retrieval-Augmented Generation (RAG), and few-shot learning to generate executable FreeCAD Python scripts, which are then used to build and visualize the final 3D model.


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

1.  **Initial Prompt:** The user provides a natural language description of the desired 3D object.
2.  **Meta-Prompting:** The first LLM call acts as a "Prompt Engineer," taking the user's text and converting it into a structured, unambiguous design brief with precise parameters.
3.  **Hybrid Prompt Construction:** The structured brief is combined with two high-quality, complete examples (few-shot learning) and several highly relevant code snippets retrieved from a custom knowledge base (RAG). This "master prompt" contains all the context the AI needs.
4.  **Code Generation:** The master prompt is sent to `gpt-4o`, which generates a complete, executable FreeCAD Python script.
5.  **Execution:** The notebook saves the generated script to a `.py` file and executes it using a headless version of FreeCAD, which creates the final `.stl` model.
6.  **Visualization:** The notebook loads the `.stl` file and displays it using the `trimesh` library.

---

## ⚙️ Setup and Usage

This project is designed to run entirely within a Google Colab environment.

1.  **Open in Colab:** Click the "Open in Colab" badge at the top of this README.

2.  **Provide Your API Key:**
    * In the Colab notebook, click the **Key icon (Secrets)** in the left sidebar.
    * Create a new secret with the name `OPENAI_API_KEY`.
    * Paste your OpenAI API key as the value and make sure the "Notebook access" toggle is enabled.

3.  **Create Your `.env` File:**
    * The notebook needs a `.env` file to load your key. In the Colab file browser (folder icon on the left), right-click and select **New file**.
    * Name the file `.env`.
    * Add the following line to the file, replacing the placeholder with your key:
        ```
        OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        ```
