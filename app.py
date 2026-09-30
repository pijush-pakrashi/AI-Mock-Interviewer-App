import io
import json
import os
import re
import streamlit as st
from dotenv import load_dotenv
from streamlit.components.v1 import html as components_html
from interview_manager import InterviewManager

# Load environment configuration
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="Elevate AI - Principal Technical Interview Coach",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design System & CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Hero Header */
    .hero-container {
        text-align: center;
        padding: 1.5rem 1rem 1rem 1rem;
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 50%, #6B8CFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.15rem;
        max-width: 680px;
        margin: 0 auto 1rem auto;
        line-height: 1.6;
    }
    .badge-pill-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 0.5rem;
    }
    .badge-pill {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #E2E8F0;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 5px 14px;
        border-radius: 9999px;
        backdrop-filter: blur(8px);
    }

    /* Question Showcase Card */
    .question-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(99, 102, 241, 0.25);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), 0 0 25px rgba(99, 102, 241, 0.1);
        backdrop-filter: blur(16px);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .question-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00F2FE, #4FACFE, #818CF8);
    }
    .question-tag {
        color: #38BDF8;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .question-title {
        font-size: 1.55rem;
        font-weight: 600;
        line-height: 1.5;
        color: #F8FAFC;
    }

    /* Score Metrics Grid */
    .metric-box {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 14px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #38BDF8;
        margin-top: 4px;
    }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94A3B8;
    }

    /* Button Enhancements */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.65rem 1.4rem;
        transition: all 0.25s ease;
        box-shadow: 0 4px 18px rgba(79, 70, 229, 0.35);
    }
    .stButton>button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
<div class="hero-container">
    <div class="hero-title">⚡ Elevate AI Coach</div>
    <div class="hero-subtitle">
        Accelerate your career with simulated bar-raiser technical interviews, multi-metric scoring, and personalized mastery paths.
    </div>
    <div class="badge-pill-container">
        <span class="badge-pill">🧠 Gemini Multi-Modal</span>
        <span class="badge-pill">🎙️ Voice & Text Assessment</span>
        <span class="badge-pill">🎯 Bar-Raiser Feedback</span>
        <span class="badge-pill">📄 Resume Contextualization</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Role Presets for Instant 1-Click Setup
ROLE_PRESETS = {
    "Custom Configuration": {
        "role": "Full-Stack Engineer",
        "description": "Python, React, System Design, REST APIs, Microservices",
        "company": "Top Tier Tech",
        "difficulty": "Intermediate"
    },
    "Full-Stack Architect": {
        "role": "Senior Full-Stack Architect",
        "description": "Modern React, Next.js, Node.js/FastAPI, Distributed Caching (Redis), PostgreSQL, Event-Driven Architecture (Kafka), WebSockets",
        "company": "Stripe",
        "difficulty": "Advanced"
    },
    "AI / Machine Learning Engineer": {
        "role": "AI & LLM Application Engineer",
        "description": "Python, PyTorch, LangChain/LlamaIndex, RAG Pipelines, Vector Databases (Pinecone/Milvus), Fine-tuning, Inference Optimization",
        "company": "OpenAI",
        "difficulty": "Advanced"
    },
    "Backend & Distributed Systems": {
        "role": "Staff Backend Engineer",
        "description": "Go/Java, High-throughput Distributed Systems, Consensus Protocols (Raft/Paxos), Database Sharding, Kubernetes, Observability",
        "company": "Google",
        "difficulty": "Expert"
    },
    "Frontend & Web Performance": {
        "role": "Senior Frontend Engineer",
        "description": "TypeScript, React 19, Web Vitals Optimization, State Management, SSR/SSG, Browser Rendering Engine internals, Design Systems",
        "company": "Netflix",
        "difficulty": "Advanced"
    },
    "DevOps & Site Reliability (SRE)": {
        "role": "Cloud Infrastructure & SRE",
        "description": "Terraform, AWS/GCP Multi-region Architecture, Docker, Kubernetes, Prometheus, Chaos Engineering, Zero-Downtime Deployments",
        "company": "Amazon AWS",
        "difficulty": "Intermediate"
    }
}

# Sidebar - Configuration & Setup
with st.sidebar:
    st.markdown("### ⚙️ System Settings")
    api_key = os.getenv("GEMINI_API_KEY") or st.text_input(
        "Gemini API Key",
        type="password",
        help="Get a free key from https://aistudio.google.com/app/apikey"
    )

    if not api_key:
        st.warning("⚠️ Enter your Gemini API Key to enable AI coaching.")
        st.caption("You can also define `GEMINI_API_KEY` inside `.env`.")
        st.stop()

    model_option = st.selectbox(
        "Gemini Model Engine",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"],
        index=0,
        help="Flash is ultra-fast with multi-modal audio support. Pro offers deeper reasoning."
    )

# Initialize Session State & Backend Engine
try:
    if (
        'manager' not in st.session_state 
        or st.session_state.get('current_api_key') != api_key 
        or st.session_state.get('current_model_choice') != model_option
    ):
        st.session_state.manager = InterviewManager(api_key=api_key, preferred_model=model_option)
        st.session_state.current_api_key = api_key
        st.session_state.current_model_choice = model_option
except Exception as e:
    st.sidebar.error(f"Failed to connect to Gemini AI: {e}")
    st.stop()

# Session State Variables
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_q_idx' not in st.session_state:
    st.session_state.current_q_idx = 0
if 'evaluations' not in st.session_state:
    st.session_state.evaluations = {}
if 'final_report' not in st.session_state:
    st.session_state.final_report = None
if 'study_materials' not in st.session_state:
    st.session_state.study_materials = None
if 'interview_meta' not in st.session_state:
    st.session_state.interview_meta = {}

# Sidebar - Interview Setup
with st.sidebar:
    st.divider()
    st.markdown("### 🎯 Interview Profile")

    preset_name = st.selectbox("Quick Role Presets", list(ROLE_PRESETS.keys()), index=0)
    selected_preset = ROLE_PRESETS[preset_name]

    with st.expander("Role Details", expanded=True):
        role = st.text_input("Target Job Role", value=selected_preset["role"])
        company = st.text_input("Target Company", value=selected_preset["company"])
        description = st.text_area("Core Skills / Job Description", value=selected_preset["description"], height=90)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            diff_options = ["Beginner", "Intermediate", "Advanced", "Expert"]
            default_diff_idx = diff_options.index(selected_preset["difficulty"]) if selected_preset["difficulty"] in diff_options else 1
            difficulty = st.selectbox("Difficulty", diff_options, index=default_diff_idx)
        with col_c2:
            tone = st.selectbox("Interviewer Tone", ["Professional", "Strict Bar-Raiser", "Conversational", "Friendly"], index=1)
            
        num_questions = st.slider("Number of Questions", min_value=1, max_value=8, value=3)

    with st.expander("📄 Candidate Resume (Optional)", expanded=False):
        uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        use_resume = False
        resume_text = None

        if uploaded_resume:
            resume_text = st.session_state.manager.extract_text_from_pdf(uploaded_resume)
            word_count = len(resume_text.split())
            st.success(f"✓ Parsed {word_count} words from resume.")
            use_resume = st.checkbox("Tailor questions to resume background", value=True)

    st.write("")
    if st.button("🚀 Generate Interview", type="primary", use_container_width=True):
        with st.spinner("Engineering customized interview questions..."):
            try:
                r_text = resume_text if use_resume else None
                questions = st.session_state.manager.generate_questions(
                    role=role,
                    description=description,
                    company=company,
                    num_questions=num_questions,
                    resume_text=r_text,
                    difficulty=difficulty,
                    tone=tone
                )
                
                if not questions:
                    st.error("Failed to generate questions. Please try again.")
                else:
                    st.session_state.questions = questions
                    st.session_state.current_q_idx = 0
                    st.session_state.evaluations = {}
                    st.session_state.final_report = None
                    st.session_state.study_materials = None
                    st.session_state.interview_meta = {
                        "role": role,
                        "company": company,
                        "difficulty": difficulty,
                        "tone": tone
                    }
                    st.toast("✅ Technical questions generated!")
                    st.rerun()
            except Exception as e:
                st.error(f"Generation error: {e}")

# If no questions active, show landing prompt
if not st.session_state.questions:
    st.info("👈 Select a role preset or customize your target job on the sidebar, then click **'🚀 Generate Interview'** to begin.")
    st.stop()

# --- Active Interview Arena ---
if not st.session_state.final_report:
    total_q = len(st.session_state.questions)
    current_idx = st.session_state.current_q_idx
    current_q = st.session_state.questions[current_idx]

    # Progress Indicator
    progress_val = (current_idx + 1) / total_q
    st.progress(progress_val)

    # Active Question Display Card
    st.markdown(f"""
    <div class="question-card">
        <div class="question-tag">
            <span>⚡ QUESTION {current_idx + 1} OF {total_q}</span>
            <span>•</span>
            <span>{st.session_state.interview_meta.get('difficulty', 'Intermediate').upper()}</span>
        </div>
        <div class="question-title">{current_q}</div>
    </div>
    """, unsafe_allow_html=True)

    # Question Navigation and Audio Synthesizer
    col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 2])
    with col_nav1:
        if current_idx > 0:
            if st.button("⬅️ Previous Question", use_container_width=True):
                st.session_state.current_q_idx -= 1
                st.rerun()
    with col_nav2:
        if current_idx < total_q - 1:
            if st.button("Next Question ➡️", use_container_width=True):
                st.session_state.current_q_idx += 1
                st.rerun()
    with col_nav3:
        question_text_js = json.dumps(current_q)
        components_html(f"""
            <div style="display:flex;align-items:center;justify-content:center;height:100%;width:100%;">
                <button id="read-question-btn" style="width:100%;max-width:340px;padding:0.75rem 1rem;border:none;background:linear-gradient(135deg,#38BDF8,#818CF8);color:#0F172A;border-radius:12px;font-size:0.95rem;font-weight:700;cursor:pointer;box-shadow:0 8px 24px rgba(56,189,248,0.25);transition:transform 0.15s ease;">
                    🔊 Listen to Question
                </button>
            </div>
            <script>
                const questionText = {question_text_js};
                const synth = window.speechSynthesis;
                const getVoice = () => {{
                    const voices = synth.getVoices();
                    return voices.find(v => /female|natural|samantha|zira|google/i.test(v.name))
                        || voices.find(v => v.lang.toLowerCase().startsWith('en'))
                        || voices[0];
                }};
                const speakQuestion = () => {{
                    if (!synth) return;
                    synth.cancel();
                    const utterance = new SpeechSynthesisUtterance(questionText);
                    utterance.lang = 'en-US';
                    utterance.rate = 0.95;
                    const voice = getVoice();
                    if (voice) utterance.voice = voice;
                    synth.speak(utterance);
                }};
                document.getElementById('read-question-btn').addEventListener('click', () => {{
                    if (!window.speechSynthesis) return;
                    if (!window.speechSynthesis.getVoices().length) {{
                        window.speechSynthesis.onvoiceschanged = speakQuestion;
                    }} else {{
                        speakQuestion();
                    }}
                }});
            </script>
        """, height=65)

    st.write("")

    # If already evaluated, display structured metrics and feedback
    if current_idx in st.session_state.evaluations:
        eval_text = st.session_state.evaluations[current_idx]
        metrics = st.session_state.manager.parse_evaluation_scores(eval_text)

        st.success("✅ Response Evaluated")

        # Multi-Metric Dashboard Cards
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            overall = metrics["overall"]
            badge_label = "🌟 Bar-Raiser" if overall >= 8 else ("👍 Solid Effort" if overall >= 6 else "💡 Needs Polish")
            st.metric(label="Overall Score", value=f"{overall}/10", delta=badge_label)
        with c2:
            st.metric(label="Accuracy", value=f"{metrics['accuracy'] or overall}/10")
        with c3:
            st.metric(label="Architecture", value=f"{metrics['depth'] or overall}/10")
        with c4:
            st.metric(label="Clarity", value=f"{metrics['clarity'] or overall}/10")
        with c5:
            st.metric(label="Terminology", value=f"{metrics['terminology'] or overall}/10")

        # Detailed Feedback Expander
        with st.expander("🔍 In-Depth Technical Assessment & Exemplary Response", expanded=True):
            st.markdown(eval_text)

            col_audio1, col_audio2 = st.columns([1, 2])
            with col_audio1:
                if st.button("🔊 Play Evaluation Summary Audio", key=f"audio_btn_{current_idx}", use_container_width=True):
                    try:
                        audio_buffer = st.session_state.manager.text_to_speech(eval_text)
                        st.session_state[f"feedback_audio_{current_idx}"] = audio_buffer.getvalue()
                    except Exception as e:
                        st.error(f"Audio playback error: {e}")

            with col_audio2:
                audio_data = st.session_state.get(f"feedback_audio_{current_idx}")
                if audio_data:
                    st.audio(io.BytesIO(audio_data), format='audio/mp3')

        # Elevate Coach Interactive Q&A
        st.write("")
        st.markdown("### 💬 Elevate Coach Follow-Up")
        st.caption("Ask questions about where you lost points or request technical clarifications.")

        chat_key = f"chat_{current_idx}"
        if chat_key not in st.session_state:
            st.session_state[chat_key] = [
                {"role": "assistant", "content": "I'm Elevate. What would you like to clarify about this evaluation?"}
            ]

        with st.container(border=True):
            chat_container = st.container(height=300)
            with chat_container:
                for msg in st.session_state[chat_key]:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

                if st.session_state[chat_key] and st.session_state[chat_key][-1]["role"] == "user":
                    with st.chat_message("assistant"):
                        with st.spinner("Consulting coach..."):
                            user_msg = st.session_state[chat_key][-1]["content"]
                            ai_resp = st.session_state.manager.chat_about_evaluation(
                                current_q, eval_text, user_msg, st.session_state[chat_key][:-1]
                            )
                            st.markdown(ai_resp)
                    st.session_state[chat_key].append({"role": "assistant", "content": ai_resp})
                    st.rerun()

            if user_prompt := st.chat_input("Ask why you received this score or how to phrase it better..."):
                st.session_state[chat_key].append({"role": "user", "content": user_prompt})
                st.rerun()

    else:
        # Candidate Response Input Hub
        with st.container(border=True):
            st.markdown("### 🗣️ Your Response")
            
            tabs = st.tabs(["📝 Text Answer", "💻 Code / Architecture Snippet", "🎙️ Spoken Audio"])
            
            text_ans = None
            code_ans = None
            audio_bytes = None
            
            with tabs[0]:
                text_ans = st.text_area(
                    "Articulate your technical response:",
                    height=160,
                    placeholder="In production systems, I would structure this solution by considering trade-offs between...",
                    key=f"text_in_{current_idx}"
                )
            
            with tabs[1]:
                code_ans = st.text_area(
                    "Optional Code or Pseudocode snippet:",
                    height=160,
                    placeholder="// Write your algorithm, schema, or system component here...",
                    key=f"code_in_{current_idx}"
                )

            with tabs[2]:
                st.caption("Ensure your browser microphone permissions are enabled.")
                mic_input = st.audio_input("Record audio response (WAV format)", key=f"mic_{current_idx}")
                if mic_input:
                    audio_bytes = mic_input.getvalue()

            st.write("")
            if st.button("Submit Answer for Evaluation ✨", type="primary", use_container_width=True):
                cleaned_text = text_ans.strip() if text_ans else None
                cleaned_code = code_ans.strip() if code_ans else None

                if not cleaned_text and not cleaned_code and not audio_bytes:
                    st.warning("⚠️ Please provide an answer via text, code snippet, or voice recording before submitting.")
                else:
                    with st.spinner("🤖 Evaluating answer with Principal Bar-Raiser criteria..."):
                        try:
                            evaluation_result = st.session_state.manager.evaluate_answer(
                                question=current_q,
                                text_answer=cleaned_text,
                                code_snippet=cleaned_code,
                                audio_bytes=audio_bytes
                            )
                            st.session_state.evaluations[current_idx] = evaluation_result
                            st.session_state[f"feedback_audio_{current_idx}"] = None
                            st.toast("✅ Evaluation complete!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Evaluation error: {e}")

    # Complete Interview Check
    st.divider()
    if len(st.session_state.evaluations) == total_q:
        st.balloons()
        st.success("🎉 You have completed all questions in this session!")
        if st.button("Generate Executive Assessment Report 📈", type="primary", use_container_width=True):
            with st.spinner("Synthesizing comprehensive assessment dossier..."):
                try:
                    qas = [
                        {"question": q, "evaluation": st.session_state.evaluations[i]}
                        for i, q in enumerate(st.session_state.questions)
                    ]
                    report = st.session_state.manager.generate_final_report(qas)
                    st.session_state.final_report = report
                    st.toast("🎉 Executive Report Ready!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Report generation error: {e}")

# --- Comprehensive Final Report & Export Center ---
else:
    st.balloons()
    st.markdown('<h2 style="text-align:center; color:#38BDF8;">📋 Executive Assessment Dossier</h2>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(st.session_state.final_report)

    st.write("")

    if not st.session_state.study_materials:
        if st.button("Generate Personalized 30-Day Mastery Path 📚", type="primary", use_container_width=True):
            with st.spinner("Curating specialized study resources and search keywords..."):
                try:
                    study_guide = st.session_state.manager.generate_study_materials(st.session_state.final_report)
                    st.session_state.study_materials = study_guide
                    st.toast("📚 Mastery Guide Ready!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Study materials error: {e}")
    else:
        st.markdown('<h3 style="color:#818CF8; margin-top:20px;">📚 Personalized Technical Learning Path</h3>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(st.session_state.study_materials)

    st.divider()
    
    # Download Dossier & Reset Controls
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        # Generate Markdown export
        qas = [
            {"question": q, "evaluation": st.session_state.evaluations.get(i, "")}
            for i, q in enumerate(st.session_state.questions)
        ]
        export_md = st.session_state.manager.export_full_interview_markdown(
            role=st.session_state.interview_meta.get("role", "Software Engineer"),
            company=st.session_state.interview_meta.get("company", "Tech Company"),
            difficulty=st.session_state.interview_meta.get("difficulty", "Intermediate"),
            qas=qas,
            final_report=st.session_state.final_report,
            study_materials=st.session_state.study_materials
        )
        st.download_button(
            label="📥 Download Complete Interview Dossier (.md)",
            data=export_md,
            file_name=f"Elevate_AI_Interview_{st.session_state.interview_meta.get('role', 'Candidate').replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col_d2:
        if st.button("🔄 Start New Interview Session", use_container_width=True):
            st.session_state.questions = []
            st.session_state.current_q_idx = 0
            st.session_state.evaluations = {}
            st.session_state.final_report = None
            st.session_state.study_materials = None
            st.session_state.interview_meta = {}
            st.rerun()
