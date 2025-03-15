from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import fitz
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure OpenAI API key

def get_openai_response(input_text, pdf_content, prompt):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Resume Content:\n{pdf_content}\n\nJob Description:\n{input_text}"}
    ]
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)
    return response.choices[0].message.content

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, output the match percentage, then list keywords missing, and provide final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = extract_text_from_pdf(uploaded_file)
        response = get_openai_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = extract_text_from_pdf(uploaded_file)
        response = get_openai_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume.")