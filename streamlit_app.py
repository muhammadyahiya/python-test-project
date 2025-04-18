import streamlit as st
import requests

# Title
st.title("Online Python Code Executor")

# Input Area
code = st.text_area("Enter your Python code here:", height=300, value="""print("Hello, world!")""")

# Button to run the code
if st.button("Run Code"):
    if not code.strip():
        st.warning("Please enter some Python code.")
    else:
        with st.spinner("Running your code..."):
            try:
                # Prepare the payload for Piston API
                payload = {
                    "language": "python3",
                    "version": "3.10.0",
                    "files": [{"name": "main.py", "content": code}]
                }

                response = requests.post("https://emkc.org/api/v2/piston/execute", json=payload)

                if response.status_code == 200:
                    result = response.json()
                    output = result.get("run", {}).get("output", "")
                    st.subheader("Output:")
                    st.code(output, language="text")
                else:
                    st.error("Error while executing code. Please try again.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
