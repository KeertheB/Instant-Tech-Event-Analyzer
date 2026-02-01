import streamlit as st
import os
import json
from PIL import Image
from google import genai
from dotenv import load_dotenv

# 1. Setup and Config
load_dotenv()
st.set_page_config(page_title="Tech Career Mentor", layout="centered", page_icon="🚀")

class GeminiService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        self.client = genai.Client(api_key=api_key) if api_key else None
        self.model_id = 'gemini-2.0-flash'

    @st.cache_data(show_spinner=False)
    def analyze_event(_self, img_data, text_message, organizer_type, mock_mode=False):
        if mock_mode:
            return {
                "event_name": "Global AI Summit 2026",
                "date": "October 15, 2026",
                "sector": "Artificial Intelligence",
                "skills": ["Neural Networks", "LLM Fine-tuning"],
                "score": 8,
                "certificate": "Yes (E-Certificate provided)",
                "verdict": "Highly Recommended",
                "explanation": f"Organized by {organizer_type}. High networking value.",
                "missing_info": ["Exact venue link?"]
            }

        if not _self.client:
            return {"error": "API Key not found."}

        # Updated prompt to include Certificate detection
        prompt = f"""
        Act as a tech career mentor. Analyze this event.
        ORGANIZER: {organizer_type}
        
        Return ONLY a JSON object with these keys:
        "event_name", "date", "sector", "skills" (list), "score" (1-10), 
        "certificate" (Specify if Yes/No/Likely and what kind), 
        "verdict", "explanation", "missing_info" (list).
        """
        
        contents = [prompt]
        if img_data: contents.append(img_data)
        if text_message: contents.append(text_message)

        try:
            response = _self.client.models.generate_content(model=_self.model_id, contents=contents)
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            return {"error": str(e)}

    def generate_linkedin_post(self, event_name, reflection):
        prompt = f"Write a professional LinkedIn post for '{event_name}'. Reflection: {reflection}."
        response = self.client.models.generate_content(model=self.model_id, contents=[prompt])
        return response.text

# 2. UI Layout
st.title("🚀 Tech Event Mentor")
service = GeminiService()

with st.sidebar:
    st.header("Enter Event Details")
    mock_mode = False 
    #st.toggle("Enable Mock Mode (Skip API)", value=True)
    org_type = st.text_input("Organizer Name", placeholder="e.g. Google, IEEE, GDG")
    uploaded_file = st.file_uploader("Upload Event Poster", type=['png', 'jpg', 'jpeg'])
    text_msg = st.text_area("Event Message")
    analyze_btn = st.button("Analyse Event", type="primary", use_container_width=True)

tab1, tab2 = st.tabs(["📊 Event Analysis", "✍️ LinkedIn Generator"])

with tab1:
    if analyze_btn:
        with st.spinner("Analyzing..."):
            img = Image.open(uploaded_file).convert("RGB") if uploaded_file else None
            result = service.analyze_event(img, text_msg, org_type, mock_mode=mock_mode)
            if "error" in result: st.error(result["error"])
            else: st.session_state['analysis_result'] = result

    if 'analysis_result' in st.session_state:
        res = st.session_state['analysis_result']
        
        # Visual Score
        score = res.get('score', 0)
        st.write(f"### Career Impact Score: {score}/10")
        st.progress(score / 10)
        
        # NEW: Certificate Highlight
        cert_status = res.get('certificate', 'Unknown')
        if "Yes" in cert_status or "Likely" in cert_status:
            st.info(f"🎓 **Certificate Status:** {cert_status}")
        else:
            st.caption(f"Note: {cert_status}")

        # Overview Table
        st.write("#### 📋 Event Overview")
        metadata = {
            "Field": ["Event Name", "Date", "Sector", "Certificate", "Verdict"],
            "Value": [res.get('event_name'), res.get('date'), res.get('sector'), res.get('certificate'), res.get('verdict')]
        }
        st.table(metadata)

        # Skills and Explanation
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.write("**🎯 Skills You'll Gain**")
                for skill in res.get('skills', []): st.markdown(f"- {skill}")
        with col2:
            with st.container(border=True):
                st.write("**💡 Mentor's Perspective**")
                st.write(res.get('explanation'))

        # Missing Info Section
        if res.get('missing_info'):
            with st.expander("❓ Missing Information"):
                for item in res.get('missing_info', []): st.info(item)

with tab2:
    st.header("LinkedIn Post Draft")
    if 'analysis_result' in st.session_state:
        res = st.session_state['analysis_result']
        reflection = st.text_area("Personal takeaway?")
        if st.button("Generate Post"):
            if mock_mode: st.code("Mock Post: I attended " + res.get('event_name'))
            else:
                post = service.generate_linkedin_post(res.get('event_name'), reflection)
                st.text_area("Your Draft", value=post, height=250)

st.divider()
st.caption("Tech Event Analyzer")