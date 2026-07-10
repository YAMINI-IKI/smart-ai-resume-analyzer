import os
import streamlit as st
from dotenv import load_dotenv
import builtins

if not hasattr(builtins, "xrange"):
    builtins.xrange = range

import requests
import pdfplumber
import tempfile
import re


class AIResumeAnalyzer:
    def __init__(self):
        load_dotenv()

        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

        self.openrouter_model = "openrouter/free"

    def extract_text_from_pdf(self, pdf_file):
        text = ""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            if hasattr(pdf_file, 'getbuffer'):
                temp_file.write(pdf_file.getbuffer())
            elif hasattr(pdf_file, 'read'):
                temp_file.write(pdf_file.read())
                pdf_file.seek(0)
            else:
                temp_file.write(pdf_file)
            temp_path = temp_file.name
        try:
            with pdfplumber.open(temp_path) as pdf:
                for page in pdf.pages:
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception:
                        pass
        except Exception:
            pass
        try:
            os.unlink(temp_path)
        except:
            pass
        return text.strip()

    def extract_text_from_docx(self, docx_file):
        try:
            from docx import Document
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
                temp_file.write(docx_file.getbuffer())
                temp_path = temp_file.name
            text = ""
            doc = Document(temp_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
            os.unlink(temp_path)
            return text.strip()
        except Exception:
            return ""

    def analyze_resume_with_gemini(self, resume_text, job_description=None, job_role=None):
        if not resume_text:
            return {"error": "Resume text is required for analysis."}
        if not self.openrouter_api_key:
            return {"error": "OpenRouter API key is not configured. Add OPENROUTER_API_KEY to your .env file."}
        try:
            st.info(f"Using model: {self.openrouter_model} (via OpenRouter)")
            base_prompt = f"""
            Analyze this resume concisely. Return the following format only:

            Resume Score: [score]/100
            ATS Score: [score]/100

            Key Strengths:
            - [strength 1]
            - [strength 2]
            - [strength 3]

            Areas for Improvement:
            - [area 1]
            - [area 2]
            - [area 3]

            Missing Skills:
            - [skill 1]
            - [skill 2]
            - [skill 3]

            Recommended Courses:
            - [course 1]
            - [course 2]
            - [course 3]

            Resume: {resume_text[:3000]}
            """
            if job_role:
                base_prompt += f"\n\nTarget Role: {job_role}"

            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.openrouter_model,
                    "messages": [{"role": "user", "content": base_prompt}]
                },
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            analysis = data["choices"][0]["message"]["content"].strip()

            resume_score = self._extract_score_from_text(analysis)
            ats_score = self._extract_ats_score_from_text(analysis)

            return {
                "analysis": analysis,
                "resume_score": resume_score if resume_score else 75,
                "ats_score": ats_score if ats_score else 70,
                "model_used": self.openrouter_model
            }
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def _extract_score_from_text(self, analysis_text):
        try:
            score_match = re.search(r'Resume Score:\s*(\d{1,3})/100', analysis_text)
            if score_match:
                return max(0, min(int(score_match.group(1)), 100))
            return 0
        except Exception:
            return 0

    def _extract_ats_score_from_text(self, analysis_text):
        try:
            score_match = re.search(r'ATS Score:\s*(\d{1,3})/100', analysis_text)
            if score_match:
                return max(0, min(int(score_match.group(1)), 100))
            return 0
        except Exception:
            return 0

    def analyze_resume(self, resume_text, job_role=None, role_info=None, model="Google Gemini"):
        try:
            result = self.analyze_resume_with_gemini(resume_text, None, job_role)
            analysis_text = result.get("analysis", "")

            strengths = []
            if "Key Strengths:" in analysis_text:
                section = analysis_text.split("Key Strengths:")[1].split("Areas for Improvement:")[0].strip()
                for line in section.split("\n"):
                    if line.strip().startswith("-"):
                        strengths.append(line.strip().replace("- ", ""))

            weaknesses = []
            if "Areas for Improvement:" in analysis_text:
                section = analysis_text.split("Areas for Improvement:")[1].split("Missing Skills:")[0].strip()
                for line in section.split("\n"):
                    if line.strip().startswith("-"):
                        weaknesses.append(line.strip().replace("- ", ""))

            suggestions = []
            if "Recommended Courses:" in analysis_text:
                section = analysis_text.split("Recommended Courses:")[1].strip()
                for line in section.split("\n"):
                    if line.strip().startswith("-"):
                        suggestions.append(line.strip().replace("- ", ""))

            return {
                "score": result.get("resume_score", 0),
                "ats_score": result.get("ats_score", 0),
                "strengths": strengths[:5] if strengths else ["No strengths identified"],
                "weaknesses": weaknesses[:5] if weaknesses else ["No weaknesses identified"],
                "suggestions": suggestions[:5] if suggestions else ["No suggestions available"],
                "full_response": analysis_text,
                "model_used": result.get("model_used", "OpenRouter")
            }
        except Exception as e:
            return {
                "error": f"Analysis failed: {str(e)}",
                "score": 0,
                "ats_score": 0,
                "strengths": ["Unable to analyze resume"],
                "weaknesses": ["Unable to analyze resume"],
                "suggestions": ["Try again"],
                "full_response": f"Error: {str(e)}",
                "model_used": "Error"
            }
