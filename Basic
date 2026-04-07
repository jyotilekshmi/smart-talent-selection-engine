import streamlit as st
import PyPDF2
import docx
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------- PAGE CONFIG ----------
st.set_page_config(page_title="Smart Talent Engine", layout="wide")

# ----------- SESSION STATE ----------
if "results" not in st.session_state:
    st.session_state.results = None

if "history" not in st.session_state:
    st.session_state.history = []

if "jd" not in st.session_state:
    st.session_state.jd = ""

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "show_history" not in st.session_state:
    st.session_state.show_history = False

# ----------- CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #e3f2fd, #ffffff);
}

/* FORCE TEXT BLACK */
html, body, [class*="css"], label {
    color: black !important;
}

h1, h2, h3 {
    color: #111827 !important;
}

.result-box {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    border-left: 5px solid #2563eb;
}

.header-box {
    background-color: #2563eb;
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ----------- HEADER ----------
st.markdown('<div class="header-box"><h1>💼 Smart Talent Selection Engine</h1></div>', unsafe_allow_html=True)

# =========================================================
# 🔹 HISTORY PAGE
# =========================================================
if st.session_state.show_history:

    st.markdown("## 📜 Past Analysis")

    if not st.session_state.history:
        st.info("No history available")
    else:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)

    if st.button("⬅ Back"):
        st.session_state.show_history = False
        st.rerun()

# =========================================================
# 🔹 MAIN PAGE
# =========================================================
else:

    # ----------- HISTORY BUTTON ----------
    if st.button("📜 View History"):
        st.session_state.show_history = True
        st.rerun()

    # ----------- INPUT ----------
    uploaded_files = st.file_uploader(
        "📂 Upload Resumes",
        accept_multiple_files=True,
        key=st.session_state.uploader_key
    )

    jd = st.text_area("📝 Paste Job Description", value=st.session_state.jd)

    # ----------- READ FUNCTIONS ----------
    def read_pdf(file):
        text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                if page.extract_text():
                    text += page.extract_text()
        except:
            pass
        return text

    def read_docx(file):
        text = ""
        try:
            doc = docx.Document(file)
            for para in doc.paragraphs:
                text += para.text
        except:
            pass
        return text

    # ----------- ANALYZE ----------
    if st.button("🚀 Analyze Candidates"):

        if not uploaded_files:
            st.error("Upload resumes")
            st.stop()

        if not jd.strip():
            st.error("Enter Job Description")
            st.stop()

        resume_texts = []
        names = []

        with st.spinner("Analyzing..."):

            for file in uploaded_files:
                if file.type == "application/pdf":
                    text = read_pdf(file)
                else:
                    text = read_docx(file)

                resume_texts.append(text[:1000] if text else " ")
                names.append(file.name)

            documents = resume_texts + [jd]

            tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
            vectors = tfidf.fit_transform(documents)

            scores = cosine_similarity(vectors[-1], vectors[:-1])

            results = [(names[i], round(score * 100, 2)) for i, score in enumerate(scores[0])]
            results.sort(key=lambda x: x[1], reverse=True)

            st.session_state.results = results

            # ✅ SAVE ONLY TOP 1
            top_name, top_score = results[0]

            st.session_state.history.append({
                "Top Candidate": top_name,
                "Match %": top_score,
                "Job Description": jd[:100] + "..."
            })

            # SAVE JD
            st.session_state.jd = jd

    # ----------- DISPLAY RESULTS ----------
    if st.session_state.results:

        st.markdown("## 🏆 Ranked Candidates")

        for name, score in st.session_state.results:
            st.markdown(f"""
                <div class="result-box">
                    👉 <span style="color:#111827; font-weight:600;">{name}</span> —
                    <span style="color:#2563eb; font-weight:bold;">{score}%</span>
                </div>
            """, unsafe_allow_html=True)

        # ----------- NEXT ANALYSIS ----------
        if st.button("🔄 Next Analysis"):
            st.session_state.results = None
            st.session_state.jd = ""
            st.session_state.uploader_key += 1
            st.rerun()
