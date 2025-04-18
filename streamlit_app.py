import streamlit as st
import requests
from db import engine
import pandas as pd
from sqlalchemy import text

st.set_page_config(page_title="Python Code Executor", page_icon="🐍")

st.title("🧪 Online Python Code Executor with User Info")

# Inputs
name = st.text_input("👤 Name")
qualification = st.text_input("🎓 Education Qualification")
code = st.text_area("💻 Enter your Python code:", height=300, value='print("Hello, world!")')

# On Run
if st.button("Run Code"):
    if not name or not qualification or not code.strip():
        st.warning("Please complete all fields.")
    else:
        with st.spinner("Running and saving your code..."):
            try:
                # Execute the code with Piston API
                payload = {
                    "language": "python3",
                    "version": "3.10.0",
                    "files": [{"name": "main.py", "content": code}]
                }
                response = requests.post("https://emkc.org/api/v2/piston/execute", json=payload)

                if response.status_code == 200:
                    result = response.json()
                    output = result.get("run", {}).get("output", "")

                    # Display user details and output
                    st.success("✅ Code executed successfully!")
                    st.subheader("👤 User Info")
                    st.markdown(f"**Name:** {name}")
                    st.markdown(f"**Qualification:** {qualification}")
                    st.subheader("📤 Output:")
                    st.code(output)

                    # Save to DB
                    with engine.connect() as conn:
                        insert_query = text("""
                            INSERT INTO user_code_logs (name, qualification, code, output)
                            VALUES (:name, :qualification, :code, :output)
                        """)
                        conn.execute(insert_query, {
                            "name": name,
                            "qualification": qualification,
                            "code": code,
                            "output": output
                        })

                        st.info("🗂 User data and code execution saved to database.")

                else:
                    st.error("❌ Failed to execute code.")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
