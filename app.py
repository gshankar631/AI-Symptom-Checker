import streamlit as st
from symptom_checker import SymptomChecker

checker = SymptomChecker(r"F:\Project\Data\symptoms_dataset.csv")

st.title("🩺 AI Symptom Checker")
st.write("Enter your symptoms, and we'll suggest a possible condition and doctor.")

user_input = st.text_area("Enter symptoms (comma separated):", "")

if st.button("Check"):
    if user_input.strip():
        result = checker.check_symptoms(user_input)

        st.success(f"Possible Condition: {result['Condition']}")
        st.info(f"Suggested Doctor: {result['Doctor']}")

        if result["Emergency"]:
            st.error("🚨 Emergency-level symptoms detected! Please seek immediate medical care.")
    else:
        st.warning("Please enter your symptoms.")
