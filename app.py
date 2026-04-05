import streamlit as st

st.title("Smart Talent Selection Engine")

st.write("Upload resumes and job description")

uploaded_files = st.file_uploader("Upload Resumes", accept_multiple_files=True)

jd = st.text_area("Paste Job Description")

if st.button("Analyze"):
    st.write("Processing...")
