import streamlit as st
import pandas as pd

from utils.resume_reader import extract_resume_text
from agents.resume_optimizer_agent import ResumeOptimizerAgent
from agents.behavioral_interview_agent import BehavioralInterviewAgent
from agents.role_fit_analyzer_agent import RoleFitAnalyzerAgent
from memory.coach_db import save_resume_session, save_interview_response, get_all_records

st.set_page_config(page_title="Resume & Interview Coach", layout="wide")

resume_agent = ResumeOptimizerAgent()
interview_agent = BehavioralInterviewAgent()
role_fit_agent = RoleFitAnalyzerAgent()

st.title("Resume & Interview Coach")
st.subheader("AI-Powered Career Preparation Workspace")

menu = st.sidebar.selectbox(
    "Choose Option",
    ["Resume Review", "Mock Interview", "Progress History", "About"]
)

if menu == "Resume Review":
    st.header("Upload Resume or Enter Career Goal")

    uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    career_goal = st.text_input("Career Goal", "Prepare for an AI/ML Engineer role")
    target_role = st.text_input("Target Role", "Generative AI Engineer")
    job_description = st.text_area(
        "Job Description / Target Requirements",
        "Experience with Python, LLMs, RAG pipelines, FastAPI, cloud deployment, and backend APIs."
    )

    resume_text = ""
    if uploaded_file:
        resume_text = extract_resume_text(uploaded_file)
        if resume_text.startswith("ERROR:"):
            st.error(resume_text)
        else:
            st.subheader("Resume Preview")
            st.write(resume_text[:2000])

    if st.button("Analyze Resume"):
        if not resume_text and not career_goal:
            st.warning("Please upload a resume or enter a career goal.")
        else:
            source_text = resume_text if resume_text else career_goal

            with st.spinner("Optimizing resume..."):
                resume_feedback = resume_agent.run(source_text, career_goal, target_role)

            if resume_feedback.startswith("ERROR:"):
                st.error(f"Resume Optimizer failed: {resume_feedback}")
            else:
                with st.spinner("Analyzing role fit..."):
                    role_fit_feedback = role_fit_agent.run(source_text, career_goal, target_role, job_description)

                if role_fit_feedback.startswith("ERROR:"):
                    st.warning("Resume feedback generated, but Role-Fit analysis timed out.")
                    st.subheader("Resume Optimization Feedback")
                    st.write(resume_feedback)
                else:
                    save_resume_session(career_goal, target_role, source_text, resume_feedback, role_fit_feedback)

                    st.success("Resume analysis completed and saved.")

                    st.subheader("Resume Optimization Feedback")
                    st.write(resume_feedback)

                    st.subheader("Role-Fit Analysis")
                    st.write(role_fit_feedback)

elif menu == "Mock Interview":
    st.header("Behavioral Interview Practice")

    target_role = st.text_input("Target Role", "Backend Engineer", key="mock_role")
    career_goal = st.text_input("Career Goal", "Improve behavioral interview performance", key="mock_goal")

    if st.button("Generate Interview Questions"):
        questions = interview_agent.generate_questions(target_role, career_goal)

        if questions.startswith("ERROR:"):
            st.error(f"Behavioral Interview Agent failed: {questions}")
        else:
            st.session_state["generated_questions"] = questions
            st.subheader("Mock Interview Questions")
            st.write(questions)

    question = st.text_area("Paste one interview question here")
    answer = st.text_area("Write your answer here")

    if st.button("Review My Answer"):
        if not question or not answer:
            st.warning("Please provide both a question and an answer.")
        else:
            feedback = interview_agent.review_answer(question, answer, target_role)

            if feedback.startswith("ERROR:"):
                st.error(f"Interview answer review failed: {feedback}")
            else:
                save_interview_response(target_role, question, answer, feedback)

                st.success("Interview feedback generated and saved.")
                st.subheader("Interview Feedback")
                st.write(feedback)

elif menu == "Progress History":
    st.header("Saved Preparation History")

    records = get_all_records()

    if records:
        df = pd.DataFrame(records)
        display_cols = [c for c in ["timestamp", "type", "career_goal", "target_role", "question"] if c in df.columns]
        st.dataframe(df[display_cols], use_container_width=True)

        selected_index = st.number_input(
            "Select record index",
            min_value=0,
            max_value=len(records) - 1,
            step=1
        )

        record = records[selected_index]

        st.subheader(f"Record Type: {record['type']}")
        st.write(f"Saved on: {record['timestamp']}")

        if record["type"] == "resume_session":
            st.write(f"Career Goal: {record['career_goal']}")
            st.write(f"Target Role: {record['target_role']}")
            st.markdown("### Resume Feedback")
            st.write(record["resume_feedback"])
            st.markdown("### Role-Fit Feedback")
            st.write(record["role_fit_feedback"])

        elif record["type"] == "interview_response":
            st.write(f"Target Role: {record['target_role']}")
            st.markdown("### Interview Question")
            st.write(record["question"])
            st.markdown("### Your Answer")
            st.write(record["answer"])
            st.markdown("### Coach Feedback")
            st.write(record["feedback"])
    else:
        st.info("No preparation history found yet.")

else:
    st.header("About")
    st.markdown("""
This application helps job seekers prepare using three specialized AI agents:
- Resume Optimizer Agent
- Behavioral Interview Agent
- Role-Fit Analyzer Agent

It stores resume analyses, interview answers, and improvement history over time.
""")