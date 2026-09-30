import io
import json
import os
import re
import streamlit as st
from dotenv import load_dotenv
from streamlit.components.v1 import html as components_html
from interview_manager import InterviewManager
from history_manager import HistoryManager

# Load environment configuration
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="Elevate AI - Branch-Adaptive Technical Interview Coach",
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
        padding: 1rem 1rem 0.5rem 1rem;
        margin-bottom: 0.8rem;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 50%, #6B8CFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.1rem;
        max-width: 720px;
        margin: 0 auto 0.6rem auto;
        line-height: 1.5;
    }
    .badge-pill-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 0.3rem;
    }
    .badge-pill {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #E2E8F0;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 9999px;
        backdrop-filter: blur(8px);
    }

    /* Candidate Profile Banner */
    .profile-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 16px;
        padding: 14px 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 15px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .profile-info {
        display: flex;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
    }
    .profile-avatar {
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        color: #0F172A;
        font-weight: bold;
    }
    .profile-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .profile-details {
        font-size: 0.85rem;
        color: #94A3B8;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    .profile-tag {
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }

    /* Question Showcase Card */
    .question-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-radius: 20px;
        padding: 28px;
        border: 1px solid rgba(99, 102, 241, 0.25);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), 0 0 25px rgba(99, 102, 241, 0.1);
        backdrop-filter: blur(16px);
        margin-bottom: 20px;
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
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .question-title {
        font-size: 1.5rem;
        font-weight: 600;
        line-height: 1.5;
        color: #F8FAFC;
    }

    /* Revision Showcase Box */
    .revision-box {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 14px;
    }
    .exemplary-callout {
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10B981;
        padding: 12px 16px;
        border-radius: 0 10px 10px 0;
        margin-top: 10px;
        color: #E2E8F0;
    }

    /* Button Styling */
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

# App Header
st.markdown("""
<div class="hero-container">
    <div class="hero-title">⚡ Elevate AI Coach</div>
    <div class="hero-subtitle">
        Branch-Adaptive Mock Interviews with Persistent History & Exam Revision.
    </div>
    <div class="badge-pill-container">
        <span class="badge-pill">🎓 Academic Branch Aligned</span>
        <span class="badge-pill">📚 Persistent Revision History</span>
        <span class="badge-pill">🎙️ Voice & Text Multimodal</span>
        <span class="badge-pill">📊 Bar-Raiser Feedback</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Degree & Branch Definitions
DEGREE_OPTIONS = [
    "B.Tech / B.E. (Bachelor of Technology / Engineering)",
    "BCA (Bachelor of Computer Applications)",
    "MCA (Master of Computer Applications)",
    "M.Tech / M.E. (Master of Technology / Engineering)",
    "B.Sc (Computer Science / IT)",
    "M.Sc (Computer Science / Data / IT)",
    "Diploma / Polytechnic Engineering",
    "Other Professional Degree"
]

BRANCH_OPTIONS = [
    "Computer Science & Engineering (CSE)",
    "Information Technology (IT)",
    "Electronics & Communication Engineering (ECE)",
    "Data Science & Artificial Intelligence (AI/DS)",
    "Electrical & Electronics Engineering (EEE)",
    "Mechanical Engineering (with CS / Tech interest)",
    "Civil Engineering / Other Core (Transitioning to Tech)",
    "Management / Business & Technology"
]

CAREER_STAGES = [
    "College Student (1st / 2nd Year)",
    "Pre-Final Year (3rd Year Internship Preparation)",
    "Final Year (Campus Placement Drive)",
    "Recent Graduate / Fresher (0 - 1 Years Experience)",
    "Junior Software Engineer (1 - 3 Years Experience)",
    "Mid-Level to Senior Professional (3+ Years Experience)"
]

# Role Presets
ROLE_PRESETS = {
    "Custom Configuration": {
        "role": "Full-Stack Engineer",
        "description": "Python, React, System Design, REST APIs, Microservices",
        "company": "Top Tier Tech",
        "difficulty": "Intermediate"
    },
    "Campus Placement / Fresher SDE": {
        "role": "Graduate Software Engineer (Fresher / Campus Hire)",
        "description": "Data Structures & Algorithms, Object-Oriented Programming (OOP), OS Fundamentals, DBMS & SQL, Computer Networks",
        "company": "TCS / Infosys / Wipro / Cognizant",
        "difficulty": "Intermediate"
    },
    "Product-Based SDE-1 (FAANG / Startups)": {
        "role": "Software Development Engineer I (SDE-1)",
        "description": "DSA, Clean Code, REST APIs, Database Design, System Architecture Basics, Unit Testing",
        "company": "Google / Amazon / Microsoft",
        "difficulty": "Advanced"
    },
    "Full-Stack Architect": {
        "role": "Senior Full-Stack Architect",
        "description": "Modern React, Next.js, FastAPI/Node, Distributed Caching (Redis), PostgreSQL, Event-Driven Architecture, WebSockets",
        "company": "Stripe",
        "difficulty": "Advanced"
    },
    "AI / Machine Learning Engineer": {
        "role": "AI & LLM Application Engineer",
        "description": "Python, PyTorch, LangChain, RAG Pipelines, Vector Databases, Fine-tuning, Inference Optimization",
        "company": "OpenAI",
        "difficulty": "Advanced"
    },
    "DevOps & Cloud SRE": {
        "role": "Cloud Infrastructure & SRE",
        "description": "Terraform, AWS/GCP, Docker, Kubernetes, Prometheus, CI/CD Pipelines, Zero-Downtime Deployments",
        "company": "Amazon AWS",
        "difficulty": "Intermediate"
    }
}

# Initialize History Manager
if 'history_manager' not in st.session_state:
    st.session_state.history_manager = HistoryManager()

# Sidebar - Configuration
with st.sidebar:
    st.markdown("### ⚙️ System Settings")
    api_key_from_env = os.getenv("GEMINI_API_KEY", "")
    api_key_from_state = st.session_state.get("user_gemini_key", "")
    current_key_val = api_key_from_env or api_key_from_state

    entered_key = st.text_input(
        "Gemini API Key",
        value=current_key_val,
        type="password",
        help="Get a free key from https://aistudio.google.com/app/apikey"
    )

    if entered_key:
        api_key = entered_key
        st.session_state.user_gemini_key = entered_key
    else:
        api_key = ""

    if not api_key:
        st.info("💡 Enter your free Gemini API key to activate AI mock interviews.")
        st.caption("Get key: [Google AI Studio](https://aistudio.google.com/app/apikey)")

    model_option = st.selectbox(
        "Gemini Model Engine",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"],
        index=0,
        help="Flash is ultra-fast with multi-modal audio support."
    )

# Initialize Backend AI Manager if Key is Present
if api_key:
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


# Initialize Session State
if 'candidate_profile' not in st.session_state or st.session_state.candidate_profile is None:
    # Auto-login to the last active profile from SQLite database
    st.session_state.candidate_profile = st.session_state.history_manager.get_last_active_profile()

if 'edit_profile_mode' not in st.session_state:
    st.session_state.edit_profile_mode = False
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_q_idx' not in st.session_state:
    st.session_state.current_q_idx = 0
if 'evaluations' not in st.session_state:
    st.session_state.evaluations = {}
if 'candidate_answers' not in st.session_state:
    st.session_state.candidate_answers = {}
if 'final_report' not in st.session_state:
    st.session_state.final_report = None
if 'study_materials' not in st.session_state:
    st.session_state.study_materials = None
if 'interview_meta' not in st.session_state:
    st.session_state.interview_meta = {}
if 'session_saved_id' not in st.session_state:
    st.session_state.session_saved_id = None

# --- CANDIDATE REGISTRATION / LOGIN MODAL ---
if not st.session_state.candidate_profile or st.session_state.edit_profile_mode:
    # Check if there are previously saved candidate profiles
    existing_profiles = st.session_state.history_manager.get_all_profiles()

    if existing_profiles and not st.session_state.edit_profile_mode:
        st.markdown("### 🔑 Candidate Login")
        st.info("Found existing registered profile(s). You can log in with 1-click or register a new candidate.")
        
        profile_labels = [f"{p['name']} ({p.get('degree', '').split('(')[0].strip()} • {p.get('branch', '').split('(')[0].strip()})" for p in existing_profiles]
        selected_prof_idx = st.selectbox("Select Your Profile:", range(len(existing_profiles)), format_func=lambda i: profile_labels[i])
        
        col_log1, col_log2 = st.columns([1, 1])
        with col_log1:
            if st.button("🚀 Log In to Selected Profile", type="primary", use_container_width=True):
                st.session_state.candidate_profile = existing_profiles[selected_prof_idx]
                st.session_state.history_manager.save_candidate_profile(st.session_state.candidate_profile)
                st.toast(f"Welcome back, {st.session_state.candidate_profile['name']}!")
                st.rerun()
        with col_log2:
            st.caption("Or create a brand new profile below:")
        st.divider()

    st.markdown("### 👤 Candidate Academic & Professional Profile")
    st.caption("Provide your details so Elevate AI personalizes questions to your exact branch and saves your revision history.")

    with st.form("candidate_registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            name_val = st.session_state.candidate_profile.get("name", "") if st.session_state.candidate_profile else ""
            candidate_name = st.text_input("Full Name", value=name_val, placeholder="e.g. Rahul Sharma / Sneha Roy")
            
            degree_default = DEGREE_OPTIONS.index(st.session_state.candidate_profile["degree"]) if st.session_state.candidate_profile and st.session_state.candidate_profile.get("degree") in DEGREE_OPTIONS else 0
            candidate_degree = st.selectbox("Professional Education / Degree", DEGREE_OPTIONS, index=degree_default)
            
            college_val = st.session_state.candidate_profile.get("college", "") if st.session_state.candidate_profile else ""
            candidate_college = st.text_input("College / University Name", value=college_val, placeholder="e.g. MAKAUT / Heritage Institute / IIT")

        with col2:
            email_val = st.session_state.candidate_profile.get("email", "") if st.session_state.candidate_profile else ""
            candidate_email = st.text_input("Email Address", value=email_val, placeholder="e.g. candidate@example.com")
            
            branch_default = BRANCH_OPTIONS.index(st.session_state.candidate_profile["branch"]) if st.session_state.candidate_profile and st.session_state.candidate_profile.get("branch") in BRANCH_OPTIONS else 0
            candidate_branch = st.selectbox("Academic Discipline / Branch", BRANCH_OPTIONS, index=branch_default)
            
            stage_default = CAREER_STAGES.index(st.session_state.candidate_profile["stage"]) if st.session_state.candidate_profile and st.session_state.candidate_profile.get("stage") in CAREER_STAGES else 2
            candidate_stage = st.selectbox("Current Academic / Career Stage", CAREER_STAGES, index=stage_default)

        submitted = st.form_submit_button("Save Profile & Proceed 🚀", type="primary", use_container_width=True)
        if submitted:
            if not candidate_name.strip():
                st.error("Please enter your name to register.")
            else:
                new_profile = {
                    "name": candidate_name.strip(),
                    "email": candidate_email.strip(),
                    "degree": candidate_degree,
                    "branch": candidate_branch,
                    "college": candidate_college.strip() or "University",
                    "stage": candidate_stage
                }
                st.session_state.candidate_profile = new_profile
                st.session_state.history_manager.save_candidate_profile(new_profile)
                st.session_state.edit_profile_mode = False
                st.toast(f"✅ Profile saved for {candidate_name}!")
                st.rerun()

    st.stop()

# --- PROFILE BANNER ---
profile = st.session_state.candidate_profile
col_p1, col_p2, col_p3 = st.columns([4, 1, 1])
with col_p1:
    initials = "".join([part[0].upper() for part in profile['name'].split()[:2]]) or "U"
    st.markdown(f"""
    <div class="profile-banner">
        <div class="profile-info">
            <div class="profile-avatar">{initials}</div>
            <div>
                <div class="profile-name">{profile['name']}</div>
                <div class="profile-details">
                    <span class="profile-tag">🎓 {profile['degree'].split('(')[0].strip()}</span>
                    <span class="profile-tag">📚 {profile['branch'].split('(')[0].strip()}</span>
                    <span>🏛️ {profile['college']}</span>
                    <span>• {profile['stage']}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_p2:
    st.write("")
    if st.button("✏️ Edit Profile", use_container_width=True):
        st.session_state.edit_profile_mode = True
        st.rerun()
with col_p3:
    st.write("")
    if st.button("🔄 Switch Profile", use_container_width=True):
        st.session_state.candidate_profile = None
        st.session_state.edit_profile_mode = False
        st.rerun()

# --- TOP NAVIGATION: ARENA vs REVISION ---
past_sessions = st.session_state.history_manager.get_candidate_sessions(profile.get("email") or profile.get("name"))
history_count = len(past_sessions)

nav_mode = st.radio(
    "Choose View:",
    ["🎯 Active Mock Arena", f"📚 Mock Test History & Revision ({history_count})"],
    horizontal=True,
    label_visibility="collapsed"
)

# ==============================================================================
# VIEW 1: ACTIVE MOCK ARENA
# ==============================================================================
if "Active Mock Arena" in nav_mode:
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
                try:
                    from pypdf import PdfReader
                    reader = PdfReader(uploaded_resume)
                    pages_txt = [p.extract_text() for p in reader.pages if p.extract_text()]
                    resume_text = "\n\n".join(pages_txt)
                    word_count = len(resume_text.split())
                    st.success(f"✓ Parsed {word_count} words from resume.")
                    use_resume = st.checkbox("Tailor questions to resume background", value=True)
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")

        st.write("")
        if st.button("🚀 Generate Branch-Aligned Interview", type="primary", use_container_width=True):
            if not api_key:
                st.error("⚠️ Please enter your Gemini API Key in the left sidebar to generate questions.")
            elif 'manager' not in st.session_state:
                st.error("⚠️ AI Coach is initializing. Please verify your API key.")
            else:
                with st.spinner(f"Crafting technical questions aligned with {profile['branch']} & {role}..."):
                    try:
                        r_text = resume_text if use_resume else None
                        questions = st.session_state.manager.generate_questions(
                            role=role,
                            description=description,
                            company=company,
                            num_questions=num_questions,
                            resume_text=r_text,
                            difficulty=difficulty,
                            tone=tone,
                            candidate_profile=st.session_state.candidate_profile
                        )
                        
                        if not questions:
                            st.error("Failed to generate questions. Please try again.")
                        else:
                            st.session_state.questions = questions
                            st.session_state.current_q_idx = 0
                            st.session_state.evaluations = {}
                            st.session_state.candidate_answers = {}
                            st.session_state.final_report = None
                            st.session_state.study_materials = None
                            st.session_state.session_saved_id = None
                            st.session_state.interview_meta = {
                                "role": role,
                                "company": company,
                                "difficulty": difficulty,
                                "tone": tone
                            }
                            st.toast("✅ Customized questions generated!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Generation error: {e}")

    # If no questions active, show landing prompt
    if not st.session_state.questions:
        if not api_key:
            st.warning("""
            ### 🔑 Gemini API Key Required
            To generate AI mock interview questions and bar-raiser evaluations, please enter your **Gemini API Key** in the left sidebar under **System Settings**.
            
            - 🆓 **Need a free key?** You can generate one in 30 seconds at [Google AI Studio](https://aistudio.google.com/app/apikey).
            - 🔒 Your key is kept secure in your local browser session and never stored publicly.
            """)
        else:
            st.info("👈 Select your role or customize the settings on the sidebar, then click **'🚀 Generate Branch-Aligned Interview'** to begin.")
            
        if history_count > 0:
            st.markdown(f"💡 *You have **{history_count} previous mock test(s)** saved. Switch to the **'Mock Test History & Revision'** tab above to revise them anytime!*")
        st.stop()

    # Active Interview Stage
    if not st.session_state.final_report:
        total_q = len(st.session_state.questions)
        current_idx = st.session_state.current_q_idx
        current_q = st.session_state.questions[current_idx]

        progress_val = (current_idx + 1) / total_q
        st.progress(progress_val)

        # Question Display Card
        st.markdown(f"""
        <div class="question-card">
            <div class="question-tag">
                <span>⚡ QUESTION {current_idx + 1} OF {total_q}</span>
                <span>•</span>
                <span>{profile['branch'].split('(')[-1].replace(')', '')} CONTEXT</span>
                <span>•</span>
                <span>{st.session_state.interview_meta.get('difficulty', 'Intermediate').upper()}</span>
            </div>
            <div class="question-title">{current_q}</div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation & Audio
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

        # Display Evaluations if already answered
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

            # Detailed Feedback
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

            # Follow-Up Chat
            st.write("")
            st.markdown("### 💬 Elevate Coach Follow-Up")
            chat_key = f"chat_{current_idx}"
            if chat_key not in st.session_state:
                st.session_state[chat_key] = [
                    {"role": "assistant", "content": f"Hi {profile['name'].split()[0]}! What would you like to clarify about this question or your rating?"}
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

                if user_prompt := st.chat_input("Ask why you received this score or how to improve..."):
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
                                    audio_bytes=audio_bytes,
                                    candidate_profile=st.session_state.candidate_profile
                                )
                                st.session_state.evaluations[current_idx] = evaluation_result
                                st.session_state.candidate_answers[current_idx] = {
                                    "text": cleaned_text,
                                    "code": cleaned_code,
                                    "had_audio": audio_bytes is not None
                                }
                                st.session_state[f"feedback_audio_{current_idx}"] = None
                                st.toast("✅ Evaluation complete!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Evaluation error: {e}")

        # Complete Interview Check
        st.divider()
        if len(st.session_state.evaluations) == total_q:
            st.balloons()
            st.success(f"🎉 Congratulations {profile['name']}! You have completed all questions.")
            if st.button("Generate Executive Assessment Report 📈", type="primary", use_container_width=True):
                with st.spinner("Synthesizing comprehensive assessment dossier..."):
                    try:
                        qas = [
                            {"question": q, "evaluation": st.session_state.evaluations[i]}
                            for i, q in enumerate(st.session_state.questions)
                        ]
                        report = st.session_state.manager.generate_final_report(
                            qas, candidate_profile=st.session_state.candidate_profile
                        )
                        st.session_state.final_report = report
                        
                        # Calculate Overall Average Score
                        all_scores = [
                            st.session_state.manager.parse_evaluation_scores(st.session_state.evaluations[i])["overall"]
                            for i in range(total_q)
                        ]
                        avg_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0.0

                        # Auto-Save to SQLite Revision History
                        saved_qas = []
                        for i, q in enumerate(st.session_state.questions):
                            ans_info = st.session_state.candidate_answers.get(i, {})
                            saved_qas.append({
                                "question": q,
                                "answer": ans_info.get("text", ""),
                                "code": ans_info.get("code", ""),
                                "evaluation": st.session_state.evaluations[i],
                                "metrics": st.session_state.manager.parse_evaluation_scores(st.session_state.evaluations[i])
                            })

                        saved_id = st.session_state.history_manager.save_session(
                            candidate_profile=st.session_state.candidate_profile,
                            role=st.session_state.interview_meta.get("role", "Software Engineer"),
                            company=st.session_state.interview_meta.get("company", "Tech Company"),
                            difficulty=st.session_state.interview_meta.get("difficulty", "Intermediate"),
                            qas=saved_qas,
                            final_report=report,
                            study_materials="",
                            overall_score=avg_score
                        )
                        st.session_state.session_saved_id = saved_id

                        st.toast("🎉 Executive Report Ready & Saved to Revision History!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Report generation error: {e}")

    # Comprehensive Final Report & Export Center
    else:
        st.balloons()
        st.markdown('<h2 style="text-align:center; color:#38BDF8;">📋 Executive Assessment Dossier</h2>', unsafe_allow_html=True)
        st.caption("💾 *This mock test has been permanently saved to your Revision History database.*")

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
                study_materials=st.session_state.study_materials,
                candidate_profile=st.session_state.candidate_profile
            )
            safe_name = profile['name'].replace(' ', '_')
            st.download_button(
                label="📥 Download Complete Interview Dossier (.md)",
                data=export_md,
                file_name=f"Elevate_AI_{safe_name}_Interview_Dossier.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col_d2:
            if st.button("🔄 Start New Interview Session", use_container_width=True):
                st.session_state.questions = []
                st.session_state.current_q_idx = 0
                st.session_state.evaluations = {}
                st.session_state.candidate_answers = {}
                st.session_state.final_report = None
                st.session_state.study_materials = None
                st.session_state.interview_meta = {}
                st.session_state.session_saved_id = None
                st.rerun()

# ==============================================================================
# VIEW 2: MOCK TEST HISTORY & REVISION CENTER
# ==============================================================================
else:
    st.markdown("### 📚 Mock Test History & Revision Center")
    st.caption("Review your past technical interview attempts, inspect candidate answers, learn from Bar-Raiser critiques, and revise exemplary 10/10 responses.")

    sessions = st.session_state.history_manager.get_candidate_sessions(profile.get("email") or profile.get("name"))

    if not sessions:
        st.info("ℹ️ No saved mock interviews found yet. Complete a mock test in the **'Active Mock Arena'** to build your revision bank!")
    else:
        # History Analytics Overview
        scores = [s.get("overall_score", 0.0) for s in sessions if s.get("overall_score")]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Mock Interviews Completed", len(sessions))
        with col_m2:
            st.metric("Average Composite Score", f"{avg_score}/10")
        with col_m3:
            st.metric("Latest Attempt Date", sessions[0]["created_at"].split()[0])

        st.divider()
        st.markdown("#### 📖 Select a Past Session to Revise:")

        for idx, sess in enumerate(sessions):
            role_title = sess.get("role", "Software Engineer")
            company_title = sess.get("company", "Tech Company")
            score_val = sess.get("overall_score", 0.0)
            date_str = sess.get("created_at", "")
            q_count = sess.get("total_questions", len(sess.get("qas", [])))
            sess_id = sess["session_id"]

            badge_text = "🌟 Bar-Raiser" if score_val >= 8 else ("👍 Solid Effort" if score_val >= 6 else "💡 Needs Polish")

            with st.expander(f"🗓️ {date_str} — {role_title} @ {company_title} (Score: {score_val}/10 • {badge_text})", expanded=(idx == 0)):
                st.markdown(f"""
                <div class="revision-box">
                    <strong>Target Role:</strong> {role_title} &nbsp;|&nbsp; 
                    <strong>Company:</strong> {company_title} &nbsp;|&nbsp; 
                    <strong>Difficulty:</strong> {sess.get('difficulty', 'Intermediate')} &nbsp;|&nbsp; 
                    <strong>Questions:</strong> {q_count}
                </div>
                """, unsafe_allow_html=True)

                # Drill down question by question
                qas_list = sess.get("qas", [])
                for q_i, item in enumerate(qas_list):
                    st.markdown(f"#### ❓ Question {q_i + 1}: {item.get('question', '')}")
                    
                    # Show what candidate answered
                    c_ans = item.get("answer", "")
                    c_code = item.get("code", "")
                    if c_ans or c_code:
                        with st.container(border=True):
                            st.markdown("**🗣️ Your Submitted Response:**")
                            if c_ans:
                                st.markdown(f"> *{c_ans}*")
                            if c_code:
                                st.code(c_code)
                    
                    # Evaluation & Exemplary Answer
                    eval_content = item.get("evaluation", "")
                    if eval_content:
                        st.markdown("**📊 Bar-Raiser Feedback & Metrics:**")
                        st.markdown(eval_content)

                    st.write("")

                # Final Report if present
                if sess.get("final_report"):
                    st.markdown("#### 📋 Executive Assessment Report")
                    with st.container(border=True):
                        st.markdown(sess["final_report"])

                # Action Controls (Download & Delete)
                col_btn1, col_btn2 = st.columns([3, 1])
                with col_btn1:
                    # Export Markdown
                    export_past_md = st.session_state.manager.export_full_interview_markdown(
                        role=role_title,
                        company=company_title,
                        difficulty=sess.get("difficulty", "Intermediate"),
                        qas=[{"question": it.get("question", ""), "evaluation": it.get("evaluation", "")} for it in qas_list],
                        final_report=sess.get("final_report", ""),
                        study_materials=sess.get("study_materials", ""),
                        candidate_profile=st.session_state.candidate_profile
                    )
                    st.download_button(
                        label=f"📥 Download Dossier for {role_title} (.md)",
                        data=export_past_md,
                        file_name=f"Elevate_AI_{profile['name'].replace(' ', '_')}_{sess_id[:8]}.md",
                        mime="text/markdown",
                        key=f"dl_sess_{sess_id}",
                        use_container_width=True
                    )
                with col_btn2:
                    if st.button("🗑️ Delete Record", key=f"del_sess_{sess_id}", use_container_width=True):
                        st.session_state.history_manager.delete_session(sess_id)
                        st.toast("🗑️ Session deleted from history.")
                        st.rerun()
