# ⚡ Elevate AI — Principal Technical Interview Coach

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Powered by Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Multi-Modal](https://img.shields.io/badge/Audio-Multimodal%20Native-brightgreen.svg)]()

> **Elevate AI** is an enterprise-grade technical interview simulation and performance acceleration platform. Powered by Google Gemini multi-modal models, it conducts realistic, high-pressure technical mock interviews, delivers granular bar-raiser evaluations, and provides tailored 30-day learning roadmaps.

---

## 📑 Table of Contents
- [Key Features](#-key-features)
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

- **🎯 Role Presets & 1-Click Launch**: Instant configurations for *Full-Stack Architect, AI/LLM Application Engineer, Backend & Distributed Systems, Frontend & Web Performance, and DevOps/SRE*.
- **📄 Resume Contextualization**: Automatically parses PDF resumes using `pypdf`, aligning technical questions with the candidate's actual projects, stack, and seniority.
- **🎙️ Multi-Modal Response Engine**: Candidates can submit responses through:
  - 📝 **Verbal/Narrative Explanation**
  - 💻 **Syntax-highlighted Code & Architectural Snippets**
  - 🎙️ **Direct Microphone Voice Recording (WAV multi-modal audio)**
- **📊 Bar-Raiser Multi-Metric Scoring**: Real-time evaluation across **Accuracy**, **System Depth**, **Clarity**, and **Industry Terminology**.
- **🔊 Interactive Audio Feedback**: Integrated text-to-speech synthesized through browser SpeechSynthesis and `gTTS`.
- **💬 Elevate Follow-Up Chat**: Candidates can challenge ratings, inquire why they lost points, or ask for senior-level rephrasing in a threaded conversational assistant.
- **📈 Executive Dossier & Learning Path**: Synthesizes a hiring recommendation (*Strong Hire, Hire, Borderline, Needs Polish*) and generates an exportable Markdown dossier.

---

## 🏛 System Architecture

```mermaid
flowchart TD
    User([Candidate]) -->|Voice / Code / Text| UI[Streamlit Frontend Interface]
    UI -->|PDF Resume Parsing| PDFEngine[pypdf Resume Extractor]
    UI -->|Contextual Prompting| Manager[InterviewManager Engine]
    
    subgraph AI Core [Google Gemini Multi-Modal Engine]
        Manager -->|Question Engineering| GeminiQ[Question Generator]
        Manager -->|Multi-Modal WAV / Text| GeminiEval[Bar-Raiser Evaluator]
        Manager -->|Follow-Up Clarification| GeminiChat[Coaching Assistant]
        Manager -->|Performance Synthesis| GeminiReport[Executive Dossier Engine]
    end

    GeminiEval --> UI
    GeminiEval -->|Audio Feedback Synthesis| TTS[gTTS Audio Buffer / Web Speech]
    GeminiReport -->|Export Dossier| Export[Markdown Report File]
    Export --> User
```

---

## 🔄 Live Workflow

1. **Profile Setup**: Choose a role preset (or customize your own), define target company and difficulty level, and optionally upload a PDF resume.
2. **Dynamic Generation**: Gemini creates targeted technical questions targeting core architectural trade-offs, algorithms, and practical edge cases.
3. **Candidate Response**: Listen to the question via native speech, write an explanation, paste code/schemas, or record voice via microphone.
4. **Real-time Critique**: Receive immediate multi-metric ratings, positive highlights, exact omissions, an exemplary 10/10 response, and recommended study terms.
5. **Dossier & Learning Path**: Once completed, generate the Executive Assessment and download your complete interview dossier.

---

## 📊 Multi-Dimensional Evaluation

Unlike typical generic AI feedback, Elevate AI evaluates candidate responses across 4 discrete technical dimensions:

| Dimension | Weight | Focus Areas |
| :--- | :---: | :--- |
| **Technical Accuracy** | 25% | Factual correctness, absence of hallucinations, algorithmic precision. |
| **Depth & Architecture** | 30% | Understanding scale, concurrency, bottlenecks, trade-offs, and failure modes. |
| **Communication & Clarity** | 25% | Structured explanation (e.g. STAR method), conciseness, and narrative pacing. |
| **Industry Terminology** | 20% | Seniority signals, appropriate design pattern vocabulary, and domain idioms. |

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python **3.10** or higher
- A Google Gemini API key ([Get a free key here](https://aistudio.google.com/app/apikey))
- Git installed on your machine

### 1. Clone or Open Project
```bash
cd elevate-ai-coach-main
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Windows
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
Create a `.env` file from `.env.example`:
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
├── requirements.txt         # Pinned production Python dependencies
└── README.md                # Comprehensive documentation
```

---

## 🐙 Git Setup & Repository Management

To initialize this project under your own GitHub repository:

```bash
# 1. Initialize local repository
git init

# 2. Stage all files
git add .

# 3. Create your initial commit
git commit -m "feat: initial commit of Elevate AI technical interview coach"

# 4. Rename default branch to main
git branch -M main

# 5. Link to your personal GitHub repository
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY_NAME>.git

# 6. Push code to your repository
git push -u origin main
```

---

## ☁️ Deployment Guide

### Deploying to Streamlit Community Cloud
1. Push your repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io).
3. Connect your repository and select `app.py` as the entry point.
4. Under **Advanced Settings > Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
5. Click **Deploy**.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
