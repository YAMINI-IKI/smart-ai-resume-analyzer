"""
CareerPilot AI - Main Application
"""
import time
from PIL import Image
from jobs.job_search import render_job_search
from datetime import datetime
from ui_components import (
    apply_modern_styles, hero_section, feature_card, about_section,
    page_header, render_analytics_section, render_activity_section,
    render_suggestions_section
)
from feedback.feedback import FeedbackManager
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from docx import Document
import io
import base64
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
from dashboard.dashboard import DashboardManager
from config.courses import COURSES_BY_CATEGORY, RESUME_VIDEOS, INTERVIEW_VIDEOS, get_courses_for_role, get_category_for_role
from config.job_roles import JOB_ROLES
from config.database import (
    get_database_connection, save_resume_data, save_analysis_data,
    init_database, verify_admin, log_admin_action, save_ai_analysis_data,
    get_ai_analysis_stats, reset_ai_analysis_stats, get_detailed_ai_analysis_stats
)
from utils.ai_resume_analyzer import AIResumeAnalyzer
from utils.resume_builder import ResumeBuilder
from utils.resume_analyzer import ResumeAnalyzer
import traceback
import plotly.express as px
import pandas as pd
import json
import streamlit as st
import datetime
import os
"""
CareerPilot AI - Main Application
"""
import time
from PIL import Image
from jobs.job_search import render_job_search
from datetime import datetime
from ui_components import (
    apply_modern_styles, hero_section, feature_card, about_section,
    page_header, render_analytics_section, render_activity_section,
    render_suggestions_section
)
from feedback.feedback import FeedbackManager
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from docx import Document
import io
import base64
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
from dashboard.dashboard import DashboardManager
from config.courses import COURSES_BY_CATEGORY, RESUME_VIDEOS, INTERVIEW_VIDEOS, get_courses_for_role, get_category_for_role
from config.job_roles import JOB_ROLES
from config.database import (
    get_database_connection, save_resume_data, save_analysis_data,
    init_database, verify_admin, log_admin_action, save_ai_analysis_data,
    get_ai_analysis_stats, reset_ai_analysis_stats, get_detailed_ai_analysis_stats
)
from utils.ai_resume_analyzer import AIResumeAnalyzer
from utils.resume_builder import ResumeBuilder
from utils.resume_analyzer import ResumeAnalyzer
import traceback
import plotly.express as px
import pandas as pd
import json
import streamlit as st
import datetime
import os

# ============================================
# 👇 PASTE YOUR API KEY HERE 👇
# ============================================
# Manually set your API key here (replace with your actual key)

# ============================================
# Set page config at the very beginning
# ============================================
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)

# Set page config at the very beginning
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)

# ============================================
# PREMIUM CUSTOM CSS
# ============================================
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #f8fafc;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff, #f0f4f8);
        padding: 20px 15px;
        border-radius: 16px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(76, 175, 80, 0.1);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0px 8px 25px rgba(76, 175, 80, 0.15);
        border-color: #4CAF50;
    }
    
    div[data-testid="stMetric"] label {
        font-weight: 600 !important;
        color: #1a1a2e !important;
        font-size: 14px !important;
    }
    
    div[data-testid="stMetric"] div {
        font-weight: 700 !important;
        font-size: 28px !important;
        color: #4CAF50 !important;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 12px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border: none !important;
        background: linear-gradient(135deg, #4CAF50, #45a049) !important;
        color: white !important;
        box-shadow: 0px 4px 15px rgba(76, 175, 80, 0.3) !important;
        width: 100% !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 8px 25px rgba(76, 175, 80, 0.4) !important;
    }
    
    /* Hero Section */
    .hero-premium {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        padding: 60px 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    
    .hero-premium::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(76, 175, 80, 0.1), transparent);
        border-radius: 50%;
    }
    
    .hero-premium h1 {
        color: white;
        font-size: 3.2rem;
        font-weight: 700;
        margin-bottom: 10px;
        position: relative;
        z-index: 1;
    }
    
    .hero-premium .subtitle {
        color: #a8a8a8;
        font-size: 1.3rem;
        margin-bottom: 15px;
        position: relative;
        z-index: 1;
    }
    
    .hero-premium .description {
        color: #888;
        font-size: 1.1rem;
        max-width: 600px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }
    
    .hero-premium .badge {
        display: inline-block;
        background: rgba(76, 175, 80, 0.2);
        color: #4CAF50;
        padding: 5px 20px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-top: 15px;
        border: 1px solid rgba(76, 175, 80, 0.3);
        position: relative;
        z-index: 1;
    }
    
    /* Feature Cards */
    .feature-card-premium {
        background: white;
        padding: 30px 25px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card-premium:hover {
        transform: translateY(-6px);
        box-shadow: 0px 8px 30px rgba(76, 175, 80, 0.1);
        border-color: #4CAF50;
    }
    
    .feature-card-premium .icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .feature-card-premium h4 {
        color: #1a1a2e;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .feature-card-premium p {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .feature-card-premium .tag {
        display: inline-block;
        background: rgba(76, 175, 80, 0.1);
        color: #4CAF50;
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)


class ResumeApp:
    def __init__(self):
        """Initialize the application"""
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {
                'personal_info': {
                    'full_name': '',
                    'email': '',
                    'phone': '',
                    'location': '',
                    'linkedin': '',
                    'portfolio': ''
                },
                'summary': '',
                'experiences': [],
                'education': [],
                'projects': [],
                'skills_categories': {
                    'technical': [],
                    'soft': [],
                    'languages': [],
                    'tools': []
                }
            }

        if 'page' not in st.session_state:
            st.session_state.page = 'home'

        if 'is_admin' not in st.session_state:
            st.session_state.is_admin = False

        self.pages = {
            "🏠 HOME": self.render_home,
            "🔍 RESUME ANALYZER": self.render_analyzer,
            "📝 RESUME BUILDER": self.render_builder,
            "📊 DASHBOARD": self.render_dashboard,
            "🎯 JOB SEARCH": self.render_job_search,
            "🎯 SKILL GAP": self.render_skill_gap,
            "💬 FEEDBACK": self.render_feedback_page,
            "ℹ️ ABOUT": self.render_about
        }

        self.dashboard_manager = DashboardManager()
        self.analyzer = ResumeAnalyzer()
        self.ai_analyzer = AIResumeAnalyzer()
        self.builder = ResumeBuilder()
        self.job_roles = JOB_ROLES

        if 'user_id' not in st.session_state:
            st.session_state.user_id = 'default_user'
        if 'selected_role' not in st.session_state:
            st.session_state.selected_role = None

        init_database()

        with open('style/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        """, unsafe_allow_html=True)

        if 'resume_data' not in st.session_state:
            st.session_state.resume_data = []
        if 'ai_analysis_stats' not in st.session_state:
            st.session_state.ai_analysis_stats = {
                'score_distribution': {},
                'total_analyses': 0,
                'average_score': 0
            }

    def load_lottie_url(self, url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    def apply_global_styles(self):
        st.markdown("""
        <style>
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #1a1a1a;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb {
            background: #4CAF50;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #45a049;
        }
        .main-header {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .main-header h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 600;
            margin: 0;
            position: relative;
            z-index: 2;
        }
        .feature-card {
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .animate-slide-in {
            animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }
        </style>
        """, unsafe_allow_html=True)

    def add_footer(self):
        st.markdown("<hr style='margin-top: 50px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; margin-bottom: 10px;'>
                <a href='https://github.com/YAMINI-IKI/CareerPilot-AI' target='_blank' style='text-decoration: none;'>
                    <div style='display: flex; align-items: center; background-color: #24292e; padding: 5px 10px; border-radius: 5px; transition: all 0.3s ease;'>
                        <svg height="16" width="16" viewBox="0 0 16 16" version="1.1" style='margin-right: 5px;'>
                            <path fill-rule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z" fill="gold"></path>
                        </svg>
                        <span style='color: white; font-size: 14px;'>Star this repo</span>
                    </div>
                </a>
            </div>
            <p style='text-align: center;'>
                Powered by <b>Streamlit</b> and <b>Google Gemini AI</b> | Developed by Iki Yamini
            </p>
            <p style='text-align: center; font-size: 12px; color: #888888;'>
                "Every star counts! If you find this project helpful, please consider starring the repo."
            </p>
            """, unsafe_allow_html=True)

    def load_image(self, image_name):
        try:
            image_path = os.path.join("static", image_name)
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            encoded = base64.b64encode(image_bytes).decode()
            return f"data:image/png;base64,{encoded}"
        except Exception as e:
            print(f"Error loading image {image_name}: {e}")
            return None

    def export_to_excel(self):
        conn = get_database_connection()
        query = """
            SELECT
                rd.name, rd.email, rd.phone, rd.linkedin, rd.github, rd.portfolio,
                rd.summary, rd.target_role, rd.target_category,
                rd.education, rd.experience, rd.projects, rd.skills,
                ra.ats_score, ra.keyword_match_score, ra.format_score, ra.section_score,
                ra.missing_skills, ra.recommendations,
                rd.created_at
            FROM resume_data rd
            LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
        """
        try:
            df = pd.read_sql_query(query, conn)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Resume Data')
            return output.getvalue()
        except Exception as e:
            print(f"Error exporting to Excel: {str(e)}")
            return None
        finally:
            conn.close()

    def render_dashboard(self):
        self.dashboard_manager.render_dashboard()
        st.toast("Check out these repositories: [AI/ML Projects](https://github.com/YAMINI-IKI)", icon="ℹ️")

    def render_empty_state(self, icon, message):
        return f"""
            <div style='text-align: center; padding: 2rem; color: #666;'>
                <i class='{icon}' style='font-size: 2rem; margin-bottom: 1rem; color: #00bfa5;'></i>
                <p style='margin: 0;'>{message}</p>
            </div>
        """

    def analyze_resume(self, resume_text):
        analytics = self.analyzer.analyze_resume(resume_text)
        st.session_state.analytics_data = analytics
        return analytics

    def handle_resume_upload(self):
        uploaded_file = st.file_uploader("Upload your resume", type=['pdf', 'docx'])
        if uploaded_file is not None:
            try:
                if uploaded_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(uploaded_file)
                else:
                    resume_text = extract_text_from_docx(uploaded_file)
                st.session_state.resume_data = {
                    'filename': uploaded_file.name,
                    'content': resume_text,
                    'upload_time': datetime.now().isoformat()
                }
                analytics = self.analyze_resume(resume_text)
                return True
            except Exception as e:
                st.error(f"Error processing resume: {str(e)}")
                return False
        return False

    def render_home(self):
        st.markdown("""
        <div class="hero-premium">
            <h1>🚀 CareerPilot AI</h1>
            <p class="subtitle">Your AI-Powered Career Assistant</p>
            <p class="description">
                Analyze Resumes • Find Skill Gaps • Build ATS-Friendly Resumes
            </p>
            <span class="badge">✨ Powered by Google Gemini AI</span>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric(label="👥 Active Users", value="100+", delta="+12%")
        with c2:
            st.metric(label="📄 Resumes Analyzed", value="500+", delta="+8%")
        with c3:
            st.metric(label="🎯 Skills Analyzed", value="1,000+", delta="+15%")
        with c4:
            st.metric(label="🎯 Match Accuracy", value="95%", delta="+3%")

        st.markdown("---")
        st.markdown("### 🚀 Features")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="feature-card-premium">
                <div class="icon">🔍</div>
                <h4>Resume Analyzer</h4>
                <p>Get instant AI-powered feedback on your resume with detailed ATS score analysis.</p>
                <span class="tag">ATS Score • Insights • Suggestions</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="feature-card-premium">
                <div class="icon">🎯</div>
                <h4>Skill Gap Analyzer</h4>
                <p>Identify missing skills for your target role and get personalized learning recommendations.</p>
                <span class="tag">Missing Skills • Roadmap • Matching</span>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="feature-card-premium">
                <div class="icon">📝</div>
                <h4>Resume Builder</h4>
                <p>Create professional, ATS-friendly resumes with intelligent content suggestions.</p>
                <span class="tag">Professional • ATS Friendly • DOCX</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🎯 Quick Start")

        quick_col1, quick_col2, quick_col3 = st.columns(3)
        with quick_col1:
            if st.button("🔍 Analyze Resume", key="home_analyze", use_container_width=True):
                st.session_state.page = "resume_analyzer"
                st.rerun()
        with quick_col2:
            if st.button("🎯 Check Skill Gap", key="home_skill_gap", use_container_width=True):
                st.session_state.page = "skill_gap"
                st.rerun()
        with quick_col3:
            if st.button("📝 Build Resume", key="home_builder", use_container_width=True):
                st.session_state.page = "resume_builder"
                st.rerun()

        st.toast("🚀 Welcome to CareerPilot AI! Start by analyzing your resume.", icon="👋")

    def render_builder(self):
        st.title("Resume Builder 📝")
        st.write("Create your professional resume")

        template_options = ["Modern", "Professional", "Minimal", "Creative"]
        selected_template = st.selectbox("Select Resume Template", template_options)
        st.success(f"🎨 Currently using: {selected_template} Template")

        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            existing_name = st.session_state.form_data['personal_info']['full_name']
            existing_email = st.session_state.form_data['personal_info']['email']
            existing_phone = st.session_state.form_data['personal_info']['phone']
            full_name = st.text_input("Full Name", value=existing_name)
            email = st.text_input("Email", value=existing_email, key="email_input")
            phone = st.text_input("Phone", value=existing_phone)
            if 'email_input' in st.session_state:
                st.session_state.form_data['personal_info']['email'] = st.session_state.email_input
        with col2:
            existing_location = st.session_state.form_data['personal_info']['location']
            existing_linkedin = st.session_state.form_data['personal_info']['linkedin']
            existing_portfolio = st.session_state.form_data['personal_info']['portfolio']
            location = st.text_input("Location", value=existing_location)
            linkedin = st.text_input("LinkedIn URL", value=existing_linkedin)
            portfolio = st.text_input("Portfolio Website", value=existing_portfolio)

        st.session_state.form_data['personal_info'] = {
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'location': location,
            'linkedin': linkedin,
            'portfolio': portfolio
        }

        st.subheader("Professional Summary")
        summary = st.text_area("Professional Summary", value=st.session_state.form_data.get('summary', ''), height=150)

        st.subheader("Work Experience")
        if 'experiences' not in st.session_state.form_data:
            st.session_state.form_data['experiences'] = []

        if st.button("Add Experience"):
            st.session_state.form_data['experiences'].append({
                'company': '', 'position': '', 'start_date': '', 'end_date': '',
                'description': '', 'responsibilities': [], 'achievements': []
            })

        for idx, exp in enumerate(st.session_state.form_data['experiences']):
            with st.expander(f"Experience {idx + 1}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    exp['company'] = st.text_input("Company Name", key=f"company_{idx}", value=exp.get('company', ''))
                    exp['position'] = st.text_input("Position", key=f"position_{idx}", value=exp.get('position', ''))
                with col2:
                    exp['start_date'] = st.text_input("Start Date", key=f"start_date_{idx}", value=exp.get('start_date', ''))
                    exp['end_date'] = st.text_input("End Date", key=f"end_date_{idx}", value=exp.get('end_date', ''))
                exp['description'] = st.text_area("Role Overview", key=f"desc_{idx}", value=exp.get('description', ''))
                
                st.markdown("##### Key Responsibilities")
                resp_text = st.text_area("Enter responsibilities (one per line)", key=f"resp_{idx}",
                                        value='\n'.join(exp.get('responsibilities', [])), height=100)
                exp['responsibilities'] = [r.strip() for r in resp_text.split('\n') if r.strip()]
                
                st.markdown("##### Key Achievements")
                achv_text = st.text_area("Enter achievements (one per line)", key=f"achv_{idx}",
                                        value='\n'.join(exp.get('achievements', [])), height=100)
                exp['achievements'] = [a.strip() for a in achv_text.split('\n') if a.strip()]
                
                if st.button("Remove Experience", key=f"remove_exp_{idx}"):
                    st.session_state.form_data['experiences'].pop(idx)
                    st.rerun()

        st.subheader("Projects")
        if 'projects' not in st.session_state.form_data:
            st.session_state.form_data['projects'] = []

        if st.button("Add Project"):
            st.session_state.form_data['projects'].append({
                'name': '', 'technologies': '', 'description': '',
                'responsibilities': [], 'achievements': [], 'link': ''
            })

        for idx, proj in enumerate(st.session_state.form_data['projects']):
            with st.expander(f"Project {idx + 1}", expanded=True):
                proj['name'] = st.text_input("Project Name", key=f"proj_name_{idx}", value=proj.get('name', ''))
                proj['technologies'] = st.text_input("Technologies Used", key=f"proj_tech_{idx}", value=proj.get('technologies', ''))
                proj['description'] = st.text_area("Project Overview", key=f"proj_desc_{idx}", value=proj.get('description', ''))
                
                st.markdown("##### Key Responsibilities")
                proj_resp_text = st.text_area("Enter responsibilities (one per line)", key=f"proj_resp_{idx}",
                                              value='\n'.join(proj.get('responsibilities', [])), height=100)
                proj['responsibilities'] = [r.strip() for r in proj_resp_text.split('\n') if r.strip()]
                
                st.markdown("##### Key Achievements")
                proj_achv_text = st.text_area("Enter achievements (one per line)", key=f"proj_achv_{idx}",
                                              value='\n'.join(proj.get('achievements', [])), height=100)
                proj['achievements'] = [a.strip() for a in proj_achv_text.split('\n') if a.strip()]
                
                proj['link'] = st.text_input("Project Link (optional)", key=f"proj_link_{idx}", value=proj.get('link', ''))
                
                if st.button("Remove Project", key=f"remove_proj_{idx}"):
                    st.session_state.form_data['projects'].pop(idx)
                    st.rerun()

        st.subheader("Education")
        if 'education' not in st.session_state.form_data:
            st.session_state.form_data['education'] = []

        if st.button("Add Education"):
            st.session_state.form_data['education'].append({
                'school': '', 'degree': '', 'field': '', 'graduation_date': '', 'gpa': '', 'achievements': []
            })

        for idx, edu in enumerate(st.session_state.form_data['education']):
            with st.expander(f"Education {idx + 1}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    edu['school'] = st.text_input("School/University", key=f"school_{idx}", value=edu.get('school', ''))
                    edu['degree'] = st.text_input("Degree", key=f"degree_{idx}", value=edu.get('degree', ''))
                with col2:
                    edu['field'] = st.text_input("Field of Study", key=f"field_{idx}", value=edu.get('field', ''))
                    edu['graduation_date'] = st.text_input("Graduation Date", key=f"grad_date_{idx}", value=edu.get('graduation_date', ''))
                edu['gpa'] = st.text_input("GPA (optional)", key=f"gpa_{idx}", value=edu.get('gpa', ''))
                
                st.markdown("##### Achievements & Activities")
                edu_achv_text = st.text_area("Enter achievements (one per line)", key=f"edu_achv_{idx}",
                                             value='\n'.join(edu.get('achievements', [])), height=100)
                edu['achievements'] = [a.strip() for a in edu_achv_text.split('\n') if a.strip()]
                
                if st.button("Remove Education", key=f"remove_edu_{idx}"):
                    st.session_state.form_data['education'].pop(idx)
                    st.rerun()

        st.subheader("Skills")
        if 'skills_categories' not in st.session_state.form_data:
            st.session_state.form_data['skills_categories'] = {
                'technical': [], 'soft': [], 'languages': [], 'tools': []
            }

        col1, col2 = st.columns(2)
        with col1:
            tech_skills = st.text_area("Technical Skills (one per line)",
                                       value='\n'.join(st.session_state.form_data['skills_categories']['technical']),
                                       height=150)
            st.session_state.form_data['skills_categories']['technical'] = [s.strip() for s in tech_skills.split('\n') if s.strip()]
            
            soft_skills = st.text_area("Soft Skills (one per line)",
                                       value='\n'.join(st.session_state.form_data['skills_categories']['soft']),
                                       height=150)
            st.session_state.form_data['skills_categories']['soft'] = [s.strip() for s in soft_skills.split('\n') if s.strip()]
        
        with col2:
            languages = st.text_area("Languages (one per line)",
                                     value='\n'.join(st.session_state.form_data['skills_categories']['languages']),
                                     height=150)
            st.session_state.form_data['skills_categories']['languages'] = [l.strip() for l in languages.split('\n') if l.strip()]
            
            tools = st.text_area("Tools & Technologies (one per line)",
                                 value='\n'.join(st.session_state.form_data['skills_categories']['tools']),
                                 height=150)
            st.session_state.form_data['skills_categories']['tools'] = [t.strip() for t in tools.split('\n') if t.strip()]

        st.session_state.form_data.update({'summary': summary})

        if st.button("Generate Resume 📄", type="primary"):
            current_name = st.session_state.form_data['personal_info']['full_name'].strip()
            current_email = st.session_state.email_input if 'email_input' in st.session_state else ''
            
            if not current_name:
                st.error("⚠️ Please enter your full name.")
                return
            if not current_email:
                st.error("⚠️ Please enter your email address.")
                return

            st.session_state.form_data['personal_info']['email'] = current_email

            try:
                resume_data = {
                    "personal_info": st.session_state.form_data['personal_info'],
                    "summary": st.session_state.form_data.get('summary', '').strip(),
                    "experience": st.session_state.form_data.get('experiences', []),
                    "education": st.session_state.form_data.get('education', []),
                    "projects": st.session_state.form_data.get('projects', []),
                    "skills": st.session_state.form_data.get('skills_categories', {
                        'technical': [], 'soft': [], 'languages': [], 'tools': []
                    }),
                    "template": selected_template
                }

                resume_buffer = self.builder.generate_resume(resume_data)
                if resume_buffer:
                    try:
                        save_resume_data(resume_data)
                        st.success("✅ Resume generated successfully!")
                        st.snow()
                        st.download_button(
                            label="Download Resume 📥",
                            data=resume_buffer,
                            file_name=f"{current_name.replace(' ', '_')}_resume.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    except Exception as db_error:
                        st.warning("⚠️ Resume generated but couldn't be saved to database")
                        st.balloons()
                        st.download_button(
                            label="Download Resume 📥",
                            data=resume_buffer,
                            file_name=f"{current_name.replace(' ', '_')}_resume.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                else:
                    st.error("❌ Failed to generate resume. Please try again.")
            except Exception as e:
                st.error(f"❌ Error preparing resume data: {str(e)}")

        st.toast("Check out these repositories: [30-Days-Of-Rust](https://github.com/YAMINI-IKI)", icon="ℹ️")

    def render_about(self):
        from ui_components import apply_modern_styles
        import base64
        import os

        def get_image_as_base64(file_path):
            try:
                with open(file_path, "rb") as image_file:
                    encoded = base64.b64encode(image_file.read()).decode()
                    return f"data:image/jpeg;base64,{encoded}"
            except:
                return None

        image_path = os.path.join(os.path.dirname(__file__), "assets", "profile.jpeg")
        image_base64 = get_image_as_base64(image_path)
        apply_modern_styles()

        st.markdown("""
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                .profile-section, .vision-section, .feature-card {
                    text-align: center;
                    padding: 2rem;
                    background: rgba(45, 45, 45, 0.9);
                    border-radius: 20px;
                    margin: 2rem auto;
                    max-width: 800px;
                }
                .profile-image {
                    width: 200px;
                    height: 200px;
                    border-radius: 50%;
                    margin: 0 auto 1.5rem;
                    display: block;
                    object-fit: cover;
                    border: 4px solid #4CAF50;
                }
                .profile-name {
                    font-size: 2.5rem;
                    color: white;
                    margin-bottom: 0.5rem;
                }
                .profile-title {
                    font-size: 1.2rem;
                    color: #4CAF50;
                    margin-bottom: 1.5rem;
                }
                .social-links {
                    display: flex;
                    justify-content: center;
                    gap: 1.5rem;
                    margin: 2rem 0;
                }
                .social-link {
                    font-size: 2rem;
                    color: #4CAF50;
                    transition: all 0.3s ease;
                    padding: 0.5rem;
                    border-radius: 50%;
                    background: rgba(76, 175, 80, 0.1);
                    width: 60px;
                    height: 60px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    text-decoration: none;
                }
                .social-link:hover {
                    transform: translateY(-5px);
                    background: #4CAF50;
                    color: white;
                    box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
                }
                .bio-text {
                    color: #ddd;
                    line-height: 1.8;
                    font-size: 1.1rem;
                    margin-top: 2rem;
                    text-align: left;
                }
                .vision-text {
                    color: #ddd;
                    line-height: 1.8;
                    font-size: 1.1rem;
                    font-style: italic;
                    margin: 1.5rem 0;
                    text-align: left;
                }
                .vision-icon {
                    font-size: 2.5rem;
                    color: #4CAF50;
                    margin-bottom: 1rem;
                }
                .vision-title {
                    font-size: 2rem;
                    color: white;
                    margin-bottom: 1rem;
                }
                .features-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 2rem;
                    margin: 2rem auto;
                    max-width: 1200px;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="hero-section">
                <h1 class="hero-title">About CareerPilot AI</h1>
                <p class="hero-subtitle">A powerful AI-driven platform for optimizing your resume</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="profile-section">
                <img src="{image_base64 if image_base64 else 'https://avatars.githubusercontent.com/YAMINI-IKI'}"
                     alt="Iki Yamini"
                     class="profile-image"
                     onerror="this.onerror=null; this.src='https://avatars.githubusercontent.com/YAMINI-IKI';">
                <h2 class="profile-name">Iki Yamini</h2>
                <p class="profile-title">Computer Science Student | AI & Python Developer</p>
                <div class="social-links">
                    <a href="https://github.com/YAMINI-IKI" class="social-link" target="_blank">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="https://www.linkedin.com/in/iki-yamini" class="social-link" target="_blank">
                        <i class="fab fa-linkedin"></i>
                    </a>
                    <a href="mailto:iki.yamini@email.com" class="social-link" target="_blank">
                        <i class="fas fa-envelope"></i>
                    </a>
                </div>
                <p class="bio-text">
                    I am Iki Yamini, a Computer Science student passionate about Artificial Intelligence,
                    Python development, and Full Stack technologies. CareerPilot AI helps students
                    improve their resumes, identify skill gaps, and prepare for technology careers
                    through AI-powered analysis and career guidance.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="vision-section">
                <i class="fas fa-lightbulb vision-icon"></i>
                <h2 class="vision-title">Our Vision</h2>
                <p class="vision-text">
                    "CareerPilot AI represents my vision of democratizing career advancement through technology.
                    By combining cutting-edge AI with intuitive design, this platform empowers job seekers at
                    every career stage to showcase their true potential and stand out in today's competitive job market."
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="features-grid">
                <div class="feature-card">
                    <i class="fas fa-robot feature-icon"></i>
                    <h3 class="feature-title">AI-Powered Analysis</h3>
                    <p class="feature-description">
                        Advanced AI algorithms provide detailed insights and suggestions to optimize your resume.
                    </p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-chart-line feature-icon"></i>
                    <h3 class="feature-title">Data-Driven Insights</h3>
                    <p class="feature-description">
                        Make informed decisions with our analytics-based recommendations and industry insights.
                    </p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-shield-alt feature-icon"></i>
                    <h3 class="feature-title">Privacy First</h3>
                    <p class="feature-description">
                        Your data security is our priority. We ensure your information is always protected and private.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.toast("Check out these repositories: [Iriswise](https://github.com/YAMINI-IKI/Iriswise)", icon="ℹ️")

    def render_analyzer(self):
        apply_modern_styles()
        
        page_header("Resume Analyzer", "Get instant AI-powered feedback to optimize your resume")
        
        analyzer_tabs = st.tabs(["Standard Analyzer", "AI Analyzer"])
        
        with analyzer_tabs[0]:
            categories = list(self.job_roles.keys())
            selected_category = st.selectbox("Job Category", categories, key="standard_category")
            roles = list(self.job_roles[selected_category].keys())
            selected_role = st.selectbox("Specific Role", roles, key="standard_role")
            role_info = self.job_roles[selected_category][selected_role]
            
            st.markdown(f"""
            <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                <h3>{selected_role}</h3>
                <p>{role_info['description']}</p>
                <h4>Required Skills:</h4>
                <p>{', '.join(role_info['required_skills'])}</p>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("Upload your resume", type=['pdf', 'docx'], key="standard_file")
            
            if not uploaded_file:
                st.markdown(self.render_empty_state("fas fa-cloud-upload-alt", "Upload your resume to get started"), unsafe_allow_html=True)
            
            if uploaded_file:
                if st.button("🔍 Analyze My Resume", type="primary", use_container_width=True, key="analyze_standard_button"):
                    with st.spinner("Analyzing your document..."):
                        try:
                            if uploaded_file.type == "application/pdf":
                                text = self.analyzer.extract_text_from_pdf(uploaded_file)
                            else:
                                text = self.analyzer.extract_text_from_docx(uploaded_file)
                            
                            if not text or text.strip() == "":
                                st.error("Could not extract text from the file.")
                                return
                                
                            analysis = self.analyzer.analyze_resume({'raw_text': text}, role_info)
                            
                            if 'error' in analysis:
                                st.error(analysis['error'])
                                return
                            
                            st.snow()
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("ATS Score", f"{analysis['ats_score']}%")
                                st.metric("Keyword Match", f"{int(analysis.get('keyword_match', {}).get('score', 0))}%")
                            with col2:
                                st.metric("Format Score", f"{int(analysis.get('format_score', 0))}%")
                                st.metric("Section Score", f"{int(analysis.get('section_score', 0))}%")
                            
                            if analysis.get('suggestions'):
                                with st.expander("📋 Improvement Suggestions", expanded=True):
                                    for suggestion in analysis['suggestions'][:5]:
                                        st.markdown(f"- {suggestion}")
                        
                        except Exception as e:
                            st.error(f"Error during analysis: {str(e)}")
        
        with analyzer_tabs[1]:
            st.markdown("""
            <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                <h3>AI-Powered Resume Analysis</h3>
                <p>Upload your resume for advanced AI-powered insights.</p>
            </div>
            """, unsafe_allow_html=True)
            
            categories = list(self.job_roles.keys())
            selected_category = st.selectbox("Job Category", categories, key="ai_category")
            roles = list(self.job_roles[selected_category].keys())
            selected_role = st.selectbox("Specific Role", roles, key="ai_role")
            
            uploaded_file = st.file_uploader("Upload your resume", type=['pdf', 'docx'], key="ai_file")
            
            if uploaded_file:
                if st.button("🤖 Analyze with AI", type="primary", use_container_width=True, key="analyze_ai_button"):
                    with st.spinner("AI is analyzing your resume..."):
                        try:
                            analyzer = AIResumeAnalyzer()
                            if uploaded_file.type == "application/pdf":
                                resume_text = analyzer.extract_text_from_pdf(uploaded_file)
                            else:
                                resume_text = analyzer.extract_text_from_docx(uploaded_file)
                            
                            job_role = selected_role if selected_role else "Not specified"
                            analysis_result = analyzer.analyze_resume_with_gemini(resume_text, job_role=job_role)
                            
                            if analysis_result and "error" not in analysis_result:
                                st.success("✅ Analysis complete!")
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("📊 Resume Score", f"{analysis_result.get('resume_score', 0)}/100")
                                with col2:
                                    st.metric("🎯 ATS Score", f"{analysis_result.get('ats_score', 0)}/100")
                                
                                with st.expander("📄 View Full Analysis", expanded=True):
                                    st.markdown(analysis_result.get("analysis", "No analysis available"))
                            else:
                                st.error(f"Analysis failed: {analysis_result.get('error', 'Unknown error')}")
                        
                        except Exception as e:
                            st.error(f"Error during AI analysis: {str(e)}")

    def render_job_search(self):
        render_job_search()
        st.toast("Check out these repositories: [GeeksforGeeks-POTD](https://github.com/YAMINI-IKI)", icon="ℹ️")

    def render_skill_gap(self):
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;'>
            <h1 style='color: white; text-align: center; font-size: 2.5rem;'>🎯 Skill Gap Analyzer</h1>
            <p style='color: #a8a8a8; text-align: center; font-size: 1.1rem;'>
                Identify missing skills for your target role and get personalized learning recommendations
            </p>
        </div>
        """, unsafe_allow_html=True)

        categories = {
            "💻 Software Development": ["Python Developer", "Java Developer", "Full Stack Developer", "Frontend Developer", "Backend Developer"],
            "🤖 Data Science & AI": ["Data Scientist", "Machine Learning Engineer", "AI Engineer", "Data Analyst", "NLP Engineer"],
            "☁️ Cloud & DevOps": ["Cloud Engineer", "DevOps Engineer", "Site Reliability Engineer", "Platform Engineer"],
            "🛡️ Cyber Security": ["Security Engineer", "Penetration Tester", "Security Analyst", "SOC Analyst"],
            "📱 Mobile Development": ["Android Developer", "iOS Developer", "Flutter Developer", "React Native Developer"],
            "🏗️ Engineering": ["Software Engineer", "Systems Engineer", "Embedded Engineer", "QA Engineer"]
        }

        selected_category = st.selectbox("Select Job Category", list(categories.keys()))
        selected_role = st.selectbox("Select Target Role", categories[selected_category])

        role_skills = {
            "Python Developer": ["Python", "Git", "SQL", "Django/Flask", "REST APIs", "Docker", "Unit Testing", "Linux"],
            "Full Stack Developer": ["JavaScript", "React", "Node.js", "SQL", "MongoDB", "Git", "Docker", "HTML/CSS"],
            "Data Scientist": ["Python", "Pandas", "NumPy", "Scikit-learn", "SQL", "Statistics", "Machine Learning", "Deep Learning"],
            "AI Engineer": ["Python", "PyTorch", "Transformers", "Deep Learning", "NLP", "SQL", "Docker", "LLMs"],
            "DevOps Engineer": ["Docker", "Kubernetes", "Jenkins", "AWS", "Terraform", "Linux", "Python", "CI/CD"],
            "Software Engineer": ["Python/Java", "Data Structures", "Algorithms", "SQL", "Git", "System Design", "Testing"],
        }

        required_skills = role_skills.get(selected_role, [])

        st.markdown("### 📝 Your Current Skills")
        current_skills_input = st.text_area(
            "Your Skills",
            height=150,
            placeholder="e.g., Python\nSQL\nData Analysis",
            help="List all the skills you currently have"
        )

        current_skills = [skill.strip() for skill in current_skills_input.split('\n') if skill.strip()]

        if st.button("🔍 Analyze Skill Gap", type="primary", use_container_width=True):
            if not current_skills:
                st.warning("⚠️ Please enter your current skills first.")
                st.stop()

            matching_skills = [skill for skill in current_skills if any(req.lower() in skill.lower() or skill.lower() in req.lower() for req in required_skills)]
            missing_skills = [skill for skill in required_skills if not any(skill.lower() in cs.lower() or cs.lower() in skill.lower() for cs in current_skills)]
            
            match_percentage = (len(matching_skills) / len(required_skills) * 100) if required_skills else 0
            
            st.markdown("### 📊 Match Progress")
            
            if match_percentage >= 80:
                progress_color = "green"
                status_text = "Excellent Match! 🎉"
            elif match_percentage >= 60:
                progress_color = "orange"
                status_text = "Good Match! 💪"
            else:
                progress_color = "red"
                status_text = "Needs Improvement 📈"
            
            st.progress(int(match_percentage) / 100)
            st.markdown(f"<p style='text-align: center; font-size: 1.2rem; color: {progress_color};'>{status_text} ({match_percentage:.1f}%)</p>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Match Score", f"{match_percentage:.1f}%")
            with col2:
                st.metric("✅ Matched", len(matching_skills))
            with col3:
                st.metric("❌ Missing", len(missing_skills))
            
            st.markdown("---")
            
            if matching_skills:
                st.markdown("### ✅ Skills You Have")
                cols = st.columns(4)
                for i, skill in enumerate(matching_skills[:8]):
                    with cols[i % 4]:
                        st.success(f"✅ {skill}")
            
            if missing_skills:
                st.markdown("### ❌ Missing Skills")
                st.markdown("""
                <div style='background: rgba(255, 68, 68, 0.1); border: 1px solid #ff4444; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
                    <p style='color: #ff4444; font-weight: bold;'>🚨 Skills you need to learn:</p>
                </div>
                """, unsafe_allow_html=True)
                
                for skill in missing_skills:
                    with st.expander(f"📚 {skill}"):
                        st.markdown(f"**Recommended Learning Resources for {skill}:**")
                        st.markdown(f"- 📚 Online courses for {skill}")
                        st.markdown(f"- 🎓 Practice projects using {skill}")
                        st.markdown(f"- 📖 Documentation for {skill}")
            else:
                st.success("🎉 You have all the required skills for this role!")

    def render_feedback_page(self):
        apply_modern_styles()
        page_header("Feedback & Suggestions", "Help us improve by sharing your thoughts")
        
        feedback_manager = FeedbackManager()
        form_tab, stats_tab = st.tabs(["Submit Feedback", "Feedback Stats"])
        
        with form_tab:
            feedback_manager.render_feedback_form()
        with stats_tab:
            feedback_manager.render_feedback_stats()

    def show_repo_notification(self):
        message = """
<div style="background-color: #1e1e1e; border-radius: 10px; border: 1px solid #4b6cb7; padding: 10px; margin: 10px 0; color: white;">
    <div style="margin-bottom: 10px;">Check out these other repositories:</div>
    <ul style="margin-top: 0; padding-left: 20px;">
        <li><a href="https://github.com/YAMINI-IKI/Awesome-Hacking" target="_blank" style="color: #4CAF50;">Awesome Hacking</a></li>
        <li><a href="https://github.com/YAMINI-IKI/Awesome-Java" target="_blank" style="color: #4CAF50;">Awesome Java</a></li>
        <li><a href="https://github.com/YAMINI-IKI/AI-Nexus" target="_blank" style="color: #4CAF50;">AI Nexus</a></li>
    </ul>
    <div style="margin-top: 10px;">If you find this project helpful, please consider ⭐ starring the repo!</div>
</div>
"""
        st.sidebar.markdown(message, unsafe_allow_html=True)

    def main(self):
        self.apply_global_styles()
        
        with st.sidebar:
            st_lottie(self.load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_xyadoh9h.json"), height=200, key="sidebar_animation")
            st.title("CareerPilot AI")
            st.markdown("---")
            
            for page_name in self.pages.keys():
                if st.button(page_name, use_container_width=True):
                    cleaned_name = page_name.lower().replace(" ", "_").replace("🏠", "").replace("🔍", "").replace("📝", "").replace("📊", "").replace("🎯", "").replace("💬", "").replace("ℹ️", "").strip()
                    st.session_state.page = cleaned_name
                    st.rerun()
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("---")
            
            if st.session_state.get('is_admin', False):
                st.success(f"Logged in as: {st.session_state.get('current_admin_email')}")
                if st.button("Logout", key="logout_button", use_container_width=True):
                    st.session_state.is_admin = False
                    st.session_state.current_admin_email = None
                    st.rerun()
            else:
                with st.expander("👤 Admin Login"):
                    admin_email_input = st.text_input("Email", key="admin_email_input")
                    admin_password = st.text_input("Password", type="password", key="admin_password_input")
                    if st.button("Login", key="login_button", use_container_width=True):
                        if verify_admin(admin_email_input, admin_password):
                            st.session_state.is_admin = True
                            st.session_state.current_admin_email = admin_email_input
                            st.success("Logged in successfully!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
            
            self.show_repo_notification()
        
        if 'initial_load' not in st.session_state:
            st.session_state.initial_load = True
            st.session_state.page = 'home'
            st.rerun()
        
        current_page = st.session_state.get('page', 'home')
        page_mapping = {name.lower().replace(" ", "_").replace("🏠", "").replace("🔍", "").replace("📝", "").replace("📊", "").replace("🎯", "").replace("💬", "").replace("ℹ️", "").strip(): name for name in self.pages.keys()}
        
        if current_page in page_mapping:
            self.pages[page_mapping[current_page]]()
        else:
            self.render_home()
        
        self.add_footer()


if __name__ == "__main__":
    app = ResumeApp()
    app.main()