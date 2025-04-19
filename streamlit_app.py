import streamlit as st
from database import SessionLocal, UserSubmission, test_connection, init_db

# Initialize database
init_db()

# Test database connection
if not test_connection():
    st.error("❌ Failed to connect to the database. Please check your configuration.")
    st.stop()

def save_submission(name, qualification, code, output):
    session = SessionLocal()
    try:
        submission = UserSubmission(
            name=name,
            qualification=qualification,
            code=code,
            output=output
        )
        session.add(submission)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Streamlit UI
st.title("Interview Preparation Assistant")

# Sidebar for user information
with st.sidebar:
    st.header("User Information")
    name = st.text_input("Name")
    qualification = st.text_input("Qualification")

# Main content
st.header("Python Code Editor")
code = st.text_area("Enter your Python code here:", height=200)

if st.button("Run Code"):
    if name and qualification and code:
        try:
            # Here you would typically send the code to Piston API
            # For now, we'll just save it
            output = "Code execution placeholder"
            if save_submission(name, qualification, code, output):
                st.success("Code executed and saved successfully!")
                st.code(output)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please fill in all fields (Name, Qualification, and Code)")
