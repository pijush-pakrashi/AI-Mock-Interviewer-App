# ⚡ Elevate AI — Principal Technical Interview Coach

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Powered by Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://aistudio.google.com/)
[![SQLite Persistent Storage](https://img.shields.io/badge/Storage-SQLite%20Auto--Save-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Multi-Modal](https://img.shields.io/badge/Audio-Multimodal%20Native-brightgreen.svg)]()

> **Elevate AI** is an enterprise-grade technical interview simulation, bar-raiser assessment, and persistent revision platform. Powered by Google Gemini multi-modal models and an embedded SQLite history engine, it conducts branch-adaptive technical mock interviews, provides multi-metric evaluations, and permanently saves all sessions so candidates can revise past questions, feedback, and 10/10 exemplary answers anytime.

---

## 📑 Table of Contents
- [Key Features](#-key-features)
- [Mock Test History & Revision Center](#-mock-test-history--revision-center)
- [Academic Branch & Degree Personalization](#-academic-branch--degree-personalization)
- [System Architecture](#-system-architecture)
- [Live Workflow](#-live-workflow)
- [Multi-Dimensional Evaluation](#-multi-dimensional-evaluation)
- [Quickstart & Installation](#-quickstart--installation)
- [Configuration (.env)](#-configuration-env)
- [Project Structure](#-project-structure)
- [Git Setup & Repository Management](#-git-setup--repository-management)
- [Deployment Guide](#-deployment-guide)
- [License](#-license)

---

## 🌟 Key Features

- **👤 Candidate Registration & Profile Onboarding**: Save candidate profile with Full Name, Email, College/University, Degree (`B.Tech`, `BCA`, `MCA`, `M.Tech`, `B.Sc`), and Academic Branch (`CSE`, `IT`, `ECE`, `AI/DS`, `EEE`, `Mechanical`, etc.).
- **📚 Persistent Mock Test History & Revision**: Built-in SQLite database automatically stores completed mock tests with all questions, candidate answers, code, scores, and exemplary responses for exam revision.
- **🎓 Academic Branch-Adaptive Questions**: Automatically connects academic disciplines with target software engineering roles (OS/DBMS/DSA for CSE; low-level architectures & network protocols for ECE; mathematical intuition & inference pipelines for AI/DS).
- **🎯 1-Click Role Presets**: Immediate configurations for *Campus Placement SDE, Product-Based SDE-1, Full-Stack Architect, AI/LLM Engineer, and DevOps/SRE*.
- **📄 Resume Contextualization**: Automatically parses PDF resumes using `pypdf`, aligning technical questions with the candidate's actual projects, stack, and seniority.
- **🎙️ Multi-Modal Response Engine**: Candidates can submit responses through:
  - 📝 **Verbal/Narrative Explanation**
  - 💻 **Syntax-highlighted Code & Architectural Snippets**
  - 🎙️ **Direct Microphone Voice Recording (WAV multi-modal audio)**
- **📊 Bar-Raiser Multi-Metric Scoring**: Real-time evaluation across **Accuracy**, **System Depth**, **Clarity**, and **Industry Terminology**.
- **🔊 Interactive Audio Feedback**: Integrated text-to-speech synthesized through browser SpeechSynthesis and `gTTS`.
- **💬 Elevate Follow-Up Chat**: Candidates can challenge ratings, inquire why they lost points, or ask for senior-level rephrasing in a threaded conversational assistant.
- **📈 Executive Dossier & Learning Path**: Synthesizes a hiring recommendation (*Strong Hire, Hire, Borderline, Needs Polish*) and generates an exportable Markdown dossier with candidate credentials.

---

## 📚 Mock Test History & Revision Center

Every completed mock test session is automatically preserved in a zero-configuration SQLite database (`data/elevate_history.db`). Candidates can switch to the **"Mock Test History & Revision"** tab to:

- 📊 **Track Improvement Over Time**: View composite average score trends and total completed mock interviews.
- 📖 **Question-by-Question Deep Dive**: Re-read the exact questions asked and compare candidate submitted answers against the Bar-Raiser critique.
- 🌟 **10/10 Exemplary Response Revision**: Quickly revise model answers before real campus placement or company interviews.
- 📥 **Re-Export Dossiers**: Re-download past interview assessment dossiers at any time.

---

## 🎓 Academic Branch & Degree Personalization

Elevate AI customizes interview questions based on the candidate's degree and discipline:

| Academic Branch | Example Tailored Focus for Software Roles |
| :--- | :--- |
| **Computer Science (CSE / IT)** | Operating Systems (kernel vs user space), DBMS concurrency & indexes, System Design, DSA complexity. |
| **Electronics & Comm (ECE / EEE)** | Low-level architecture, C/C++ memory models, Embedded Systems / IoT bridging with backend cloud systems. |
| **Data Science & AI (AI/DS)** | Model pipelines, RAG latency bottlenecks, Vector search indices, Data structures for ML algorithms. |
| **Core Engineering (Mech/Civil to Tech)** | Fundamental logical reasoning, Clean Code practices, OOP abstractions, and transition motivation. |

---

## 🏛 System Architecture

```mermaid
flowchart TD
    User([Candidate]) -->|Profile Registration| Onboarding[Profile & Branch Engine]
    Onboarding --> UI[Streamlit Frontend Interface]
    UI -->|PDF Resume Parsing| PDFEngine[pypdf Resume Extractor]
    UI -->|Contextual Prompting| Manager[InterviewManager Engine]
    
    subgraph AI Core [Google Gemini Multi-Modal Engine]
        Manager -->|Branch + Role Calibration| GeminiQ[Question Generator]
        Manager -->|Multi-Modal WAV / Text| GeminiEval[Bar-Raiser Evaluator]
        Manager -->|Follow-Up Clarification| GeminiChat[Coaching Assistant]
        Manager -->|Performance Synthesis| GeminiReport[Executive Dossier Engine]
    end

    GeminiEval --> UI
    GeminiReport -->|Auto-Persist Session| History[(SQLite History DB)]
    History <-->|Revision & Historical Analysis| UI
    GeminiReport -->|Export Dossier with Profile| Export[Personalized Markdown Dossier]
    Export --> User
```

---

## 🔑 How to Get a Free Gemini API Key (API Key)

Elevate AI requires a free Google Gemini API Key to power the technical mock questions and bar-raiser evaluations. Follow these simple steps:

1. **Visit Google AI Studio**: Go to [https://aistudio.ggit oogle.com/app/apikey](https://aistudio.google.com/app/apikey) in your browser.
2. **Sign In**: Log in with your standard Google (Gmail) account.
3. **Create Key**: Click the blue button labeled **"Create API key"** (or **"Get API key"**).
4. **Select Project**: Choose **"Create API key in new project"**.
5. **Copy the Key**: Click **"Copy"** next to the newly generated key (it starts with `AIzaSy...`).
6. **Apply to Project**:
   - **Method A (Easiest)**: Open the `.env` file in the project folder and paste your key inside the quotes:
     ```env
     GEMINI_API_KEY="AIzaSyYourGeneratedGeminiKey..."
     ```
   - **Method B**: Or simply paste it directly into the **"Gemini API Key"** input box in the left sidebar of the running app!

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python **3.10** or higher
- A Google Gemini API key ([Get a free key here](https://aistudio.google.com/app/apikey))
- Git installed on your machine

### 2. Set Up Virtual Environment (Recommended)
```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file from `.env.example` (or edit the existing `.env` file):
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```
Open `.env` and set your key:
```env
GEMINI_API_KEY="AIzaSyYourGeneratedGeminiKey..."
```

### 5. Launch the Application
```bash
streamlit run app.py
```
The application will open in your default browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
elevate-ai-coach-main/
├── .devcontainer/           # DevContainer definition for GitHub Codespaces/VSCode
├── .streamlit/              # Streamlit server and theme configurations
│   └── config.toml
├── .env.example             # Safe template for environment variables
├── .gitignore               # Excludes secrets, venv, and binary artifacts
├── app.py                   # Streamlit Frontend application & design system
├── interview_manager.py     # Backend AI service layer, scoring & Gemini logic
├── history_manager.py       # SQLite database persistence & revision engine
├── requirements.txt         # Pinned production Python dependencies
└── README.md                # Comprehensive documentation
```

---

## 🐙 Git Setup & Repository Management

To push this project to your own GitHub repository:

```bash
# 1. Initialize local repository
git init

# 2. Stage all files
git add .

# 3. Create your initial commit
git commit -m "feat: complete Elevate AI interview coach with persistent revision history"

# 4. Rename default branch to main
git branch -M main

# 5. Link to your personal GitHub repository
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY_NAME>.git

# 6. Push code to your repository
git push -u origin main
```

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
