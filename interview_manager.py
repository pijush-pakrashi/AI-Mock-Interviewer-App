"""Elevate AI - Interview Manager Module.

Provides comprehensive interview orchestration, resume parsing,
multi-dimensional evaluation, text-to-speech feedback, and exportable analytics
powered by Google Gemini.
"""

import io
import os
import re
from typing import Dict, List, Optional, Any

try:
    import google.generativeai as genai
except ImportError:
    try:
        from google.ai import generative as genai
    except ImportError as exc:
        raise ImportError(
            "Missing Gemini client library. Please install `google-generativeai` in your Python environment: "
            "pip install google-generativeai"
        ) from exc

from pypdf import PdfReader
from gtts import gTTS


class InterviewManager:
    """Manages the lifecycle of an AI-driven technical mock interview."""

    SUPPORTED_MODELS = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.0-flash-exp",
    ]

    def __init__(self, api_key: str, preferred_model: Optional[str] = None):
        """Initializes Gemini AI client with model discovery and fallback."""
        genai.configure(api_key=api_key)
        self.api_key = api_key
        self.model_name = self._select_model(preferred_model)
        self.model = genai.GenerativeModel(self.model_name)

    def _select_model(self, preferred_model: Optional[str]) -> str:
        """Selects the best available generative model for the configured API key."""
        if preferred_model:
            return preferred_model

        try:
            available_models = [
                m.name for m in genai.list_models()
                if "generateContent" in m.supported_generation_methods
            ]
            
            # Prefer flash variants for speed and audio multimodality
            for target in ["1.5-flash", "flash", "1.5-pro", "gemini"]:
                match = next((m for m in available_models if target in m.lower()), None)
                if match:
                    return match.replace("models/", "")

            if available_models:
                return available_models[0].replace("models/", "")
        except Exception:
            pass

        return "gemini-1.5-flash"

    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extracts and sanitizes text from an uploaded resume PDF."""
        text_content: List[str] = []
        try:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content.append(extracted.strip())
            return "\n\n".join(text_content)
        except Exception as e:
            return f"[Error parsing resume: {e}]"

    def generate_questions(
        self,
        role: str,
        description: str,
        company: str = "",
        num_questions: int = 3,
        resume_text: Optional[str] = None,
        difficulty: str = "Intermediate",
        tone: str = "Professional"
    ) -> List[str]:
        """Generates realistic, targeted technical interview questions."""
        prompt = (
            f"You are a Principal Engineering Interviewer conducting a mock interview for the role of '{role}'.\n"
            f"Target Company / Industry: {company or 'Top-Tier Tech Company'}\n"
            f"Difficulty Level: {difficulty}\n"
            f"Interviewer Tone: {tone}\n"
            f"Required Job Skills / Description: {description}\n"
        )

        if resume_text:
            prompt += (
                f"\nCandidate Resume Insights:\n"
                f"'''\n{resume_text[:2500]}\n'''\n"
                "Align questions with the candidate's stated background, validating both core strengths and technical depth.\n"
            )

        prompt += (
            f"\nGenerate exactly {num_questions} high-caliber interview questions covering technical depth, "
            "practical problem-solving, architectural design, and edge-case handling.\n"
            "CRITICAL FORMAT RULE: Return ONLY the questions separated by '|||'. Do not include numbering, bullets, "
            "intros, or concluding remarks."
        )

        response = self.model.generate_content(prompt)
        raw_output = response.text.strip()

        questions = [q.strip() for q in raw_output.split("|||") if q.strip()]

        # Fallback parsing in case separator wasn't used
        if len(questions) < num_questions:
            questions = [
                re.sub(r"^\d+[\.\)]\s*", "", line).strip()
                for line in raw_output.split("\n")
                if line.strip() and len(line.strip()) > 15
            ]

        return questions[:num_questions]

    def evaluate_answer(
        self,
        question: str,
        text_answer: Optional[str] = None,
        code_snippet: Optional[str] = None,
        audio_bytes: Optional[bytes] = None
    ) -> str:
        """Evaluates a candidate's answer across multiple dimensions."""
        prompt = (
            f"You are a rigorous, highly experienced Technical Bar-Raiser Interviewer.\n"
            f"Interview Question Asked: '{question}'\n\n"
            "Critique the candidate's answer thoroughly. Be realistic, insightful, and strict.\n"
            "Score each of the following dimensions on a 10-point scale (use decimals if appropriate):\n"
            "- Overall Score: X/10 (composite overall assessment)\n"
            "- Technical Accuracy: X/10 (factual correctness, lack of hallucinations)\n"
            "- Depth & Architecture: X/10 (understands trade-offs, internal mechanisms, scale)\n"
            "- Communication & Clarity: X/10 (structure, conciseness, articulation)\n"
            "- Industry Terminology: X/10 (seniority signals, proper domain vocabulary)\n\n"
            "Format the entire response cleanly using EXACTLY this markdown layout:\n"
            "### 📊 Evaluation Metrics\n"
            "- **Overall Score**: X/10\n"
            "- **Technical Accuracy**: X/10\n"
            "- **Depth & Architecture**: X/10\n"
            "- **Communication & Clarity**: X/10\n"
            "- **Industry Terminology**: X/10\n\n"
            "### 🌟 Strengths\n"
            "- (Provide 2-4 specific bullet points of what the candidate nailed)\n\n"
            "### 💡 Areas for Improvement\n"
            "- (Provide 4-6 specific, actionable technical flaws, omissions, edge cases missed, or ways to sound more senior)\n\n"
            "### 🎯 Exemplary 10/10 Response\n"
            "(Provide a concise, conversational 3-4 sentence response that sounds natural yet authoritative for a live interview)\n\n"
            "### 📚 Recommended Masterclass Topics\n"
            "- (3-4 specific concepts, architectural patterns, or exact YouTube search terms to master this)\n"
        )

        contents: List[Any] = [prompt]

        if audio_bytes:
            contents.append({"mime_type": "audio/wav", "data": audio_bytes})
        
        candidate_input_text = ""
        if text_answer:
            candidate_input_text += f"Candidate Verbal/Text Answer:\n{text_answer}\n\n"
        if code_snippet:
            candidate_input_text += f"Candidate Code / Technical Diagram Snippet:\n```\n{code_snippet}\n```\n"

        if candidate_input_text:
            contents.append(candidate_input_text)

        response = self.model.generate_content(contents)
        return response.text

    def parse_evaluation_scores(self, eval_text: str) -> Dict[str, float]:
        """Parses individual metric scores from evaluation markdown."""
        metrics = {
            "overall": 0.0,
            "accuracy": 0.0,
            "depth": 0.0,
            "clarity": 0.0,
            "terminology": 0.0,
        }

        patterns = {
            "overall": r"Overall Score[:\s\*]*(\d+(?:\.\d+)?)\s*(?:/|out of)\s*10",
            "accuracy": r"Technical Accuracy[:\s\*]*(\d+(?:\.\d+)?)\s*(?:/|out of)\s*10",
            "depth": r"Depth & Architecture[:\s\*]*(\d+(?:\.\d+)?)\s*(?:/|out of)\s*10",
            "clarity": r"Communication & Clarity[:\s\*]*(\d+(?:\.\d+)?)\s*(?:/|out of)\s*10",
            "terminology": r"Industry Terminology[:\s\*]*(\d+(?:\.\d+)?)\s*(?:/|out of)\s*10",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, eval_text, re.IGNORECASE)
            if match:
                try:
                    metrics[key] = float(match.group(1))
                except ValueError:
                    metrics[key] = 0.0

        # Fallback if only single Score pattern is matched
        if metrics["overall"] == 0.0:
            general_match = re.search(r"Score[:\s\*]*(\d+(?:\.\d+)?)\s*(?:/|out of)\s*10", eval_text, re.IGNORECASE)
            if general_match:
                metrics["overall"] = float(general_match.group(1))

        return metrics

    def text_to_speech(self, text: str, is_question: bool = False) -> io.BytesIO:
        """Converts text or crisp evaluation summary to an audio buffer using gTTS."""
        clean_text = text.replace("*", "").replace("#", "").replace("-", "")
        clean_text = re.sub(r"\s*\n+\s*", ". ", clean_text).strip()
        clean_text = re.sub(r"\.{2,}", ".", clean_text)
        clean_text = re.sub(r"\s{2,}", " ", clean_text)

        if not is_question:
            score_match = re.search(r"Overall Score[:\s\*]*\d+(?:\.\d+)?\s*(?:/|out of)\s*10", clean_text, re.IGNORECASE)
            if not score_match:
                score_match = re.search(r"Score[:\s\*]*\d+(?:\.\d+)?\s*(?:/|out of)\s*10", clean_text, re.IGNORECASE)
            
            exemplary_match = re.search(r"Exemplary (?:10/10 )?Response[:\s]*(.+?)(?:\.|$)", clean_text, re.IGNORECASE)
            
            summary_parts = []
            if score_match:
                summary_parts.append(score_match.group(0))
            if exemplary_match:
                summary_parts.append(f"Ideal response snippet: {exemplary_match.group(1).strip()}")

            if summary_parts:
                clean_text = ". ".join(summary_parts)

            if len(clean_text) > 320:
                clean_text = clean_text[:320].rsplit(".", 1)[0] + "."

        tts = gTTS(text=clean_text or "Evaluation complete.", lang="en", slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp

    def generate_final_report(self, qas: List[Dict[str, str]]) -> str:
        """Synthesizes a comprehensive executive Final Interview Report."""
        prompt = (
            "You are an executive Technical Hiring Director compiling an official Candidate Assessment Report.\n"
            "Here is the candidate's interview transcript and evaluations:\n\n"
        )
        for i, qa in enumerate(qas):
            prompt += f"### Question {i+1}:\n{qa['question']}\n\nEvaluation Feedback:\n{qa['evaluation']}\n\n"

        prompt += (
            "Generate a professional, structured Final Assessment Report in clean markdown:\n"
            "1. **Executive Summary & Readiness Index**: (Provide a hiring recommendation: "
            "'Strong Hire (L5/L6 Senior)', 'Hire (L4 Mid-Level)', 'Borderline / Needs Practice', or 'Not Ready Yet')\n"
            "2. **Core Technical Strengths & Highlights**: (Key areas where candidate excelled)\n"
            "3. **Critical Knowledge Gaps & Antipatterns**: (Specific technical blind spots observed)\n"
            "4. **Strategic 30-Day Action Plan**: (High-impact study priorities to reach peak interview readiness)\n\n"
            "Keep it crisp, objective, and deeply constructive."
        )

        response = self.model.generate_content(prompt)
        return response.text

    def generate_study_materials(self, final_report: str) -> str:
        """Generates targeted study materials, documentation links, and search queries."""
        prompt = (
            f"Based on the following Final Interview Report, synthesize an actionable Technical Mastery Guide:\n\n"
            f"{final_report}\n\n"
            "Include:\n"
            "- **Key Architecture Patterns & Algorithms to Master**\n"
            "- **Copy-Paste YouTube Search Queries** (format as exact search strings inside code quotes)\n"
            "- **Official Documentations & RFCs to Read** (e.g. Postgres Internals, System Design Primer, OAuth2 RFC, etc.)\n"
            "- **Hands-On Mini Coding / Design Challenges**\n"
        )

        response = self.model.generate_content(prompt)
        return response.text

    def chat_about_evaluation(
        self,
        question: str,
        evaluation: str,
        user_message: str,
        chat_history: List[Dict[str, str]]
    ) -> str:
        """Interactive coaching assistant for clarifying feedback and mistakes."""
        prompt = (
            f"You are Elevate, a friendly yet world-class Technical Interview Coach.\n"
            f"The candidate is asking questions about Question: '{question}'\n"
            f"Their initial evaluation was:\n{evaluation}\n\n"
        )

        if chat_history:
            prompt += "Conversation history:\n"
            for msg in chat_history:
                role = "Candidate" if msg["role"] == "user" else "Elevate Coach"
                prompt += f"{role}: {msg['content']}\n"

        prompt += (
            f"\nCandidate's new message: '{user_message}'\n"
            "Provide an encouraging, concise, and technically precise explanation (3-4 sentences max). "
            "Use clear analogies or code keywords to clarify where they lost points and how to phrase it like a Senior Engineer."
        )

        response = self.model.generate_content(prompt)
        return response.text

    def export_full_interview_markdown(
        self,
        role: str,
        company: str,
        difficulty: str,
        qas: List[Dict[str, str]],
        final_report: Optional[str],
        study_materials: Optional[str]
    ) -> str:
        """Packages the entire interview into an exportable Markdown dossier."""
        doc = [
            f"# 📋 Elevate AI - Technical Interview Dossier",
            f"**Target Role:** {role} | **Company:** {company or 'General Tech'} | **Difficulty:** {difficulty}",
            f"---\n",
            "## 📝 Question Breakdown & Evaluations\n",
        ]

        for i, qa in enumerate(qas):
            doc.append(f"### Question {i + 1}: {qa['question']}\n")
            doc.append(f"{qa['evaluation']}\n")
            doc.append("---\n")

        if final_report:
            doc.append("## 📈 Final Assessment Report\n")
            doc.append(f"{final_report}\n")
            doc.append("---\n")

        if study_materials:
            doc.append("## 📚 Personalized Learning Path\n")
            doc.append(f"{study_materials}\n")

        return "\n".join(doc)
