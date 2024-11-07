import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Automation Tools Survey",
    page_icon="🤖",
    layout="centered"
)

# Use secrets if available, otherwise fall back to default password
try:
    ADMIN_PASSWORD = st.secrets["general"]["admin_password"]
except:
    ADMIN_PASSWORD = "@RVsolutions@1234"  # Fallback password

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

# Your company data
DEPARTMENT_DATA = {
    'Finance': {
        'tools': {
            'Invoice Automation': ['John Doe', 'Jane Smith'],
            'Expense Reporter': ['Alice Brown', 'Charlie Davis']
        }
    },
    'HR': {
        'tools': {
            'Recruitment Tracker': ['Eva Green', 'Frank White'],
            'Onboarding System': ['Grace Lee', 'Henry Ford']
        }
    },
    'IT': {
        'tools': {
            'Service Desk': ['Ivan Black', 'Julia Red'],
            'Monitoring Tool': ['Karl Blue', 'Lisa Green']
        }
    }
}

def check_admin_password():
    """Check if admin password is correct"""
    if not st.session_state.admin_authenticated:
        password = st.text_input("Enter admin password:", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
        return False
    return True

def reset_form():
    """Reset the form to initial state"""
    st.session_state.current_step = 1
    for key in list(st.session_state.keys()):
        if key not in ['responses', 'current_step', 'admin_authenticated']:
            del st.session_state[key]

def main():
    st.title("🤖 Automation Tools Survey")
    
    # Progress bar
    if st.session_state.current_step < 6:  # Only show progress bar before completion
        st.progress(st.session_state.current_step / 5)
        st.write(f"Step {st.session_state.current_step} of 5")
    
    # Main form container
    if st.session_state.current_step == 1:
        st.subheader("👥 Department Selection")
        department = st.selectbox(
            "Please select your department:",
            options=list(DEPARTMENT_DATA.keys())
        )
        if st.button("Next"):
            st.session_state.department = department
            st.session_state.current_step = 2
            st.rerun()
            
    elif st.session_state.current_step == 2:
        st.subheader("🛠️ Tool Selection")
        st.info(f"Department: {st.session_state.department}")
        tool = st.selectbox(
            "Select the automation tool you're using:",
            options=list(DEPARTMENT_DATA[st.session_state.department]['tools'].keys())
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                st.session_state.current_step = 1
                st.rerun()
        with col2:
            if st.button("Next"):
                st.session_state.tool = tool
                st.session_state.current_step = 3
                st.rerun()
                
    elif st.session_state.current_step == 3:
        st.subheader("👤 User Selection")
        st.info(f"Department: {st.session_state.department} | Tool: {st.session_state.tool}")
        user = st.selectbox(
            "Select your name:",
            options=DEPARTMENT_DATA[st.session_state.department]['tools'][st.session_state.tool]
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                st.session_state.current_step = 2
                st.rerun()
        with col2:
            if st.button("Next"):
                st.session_state.user = user
                st.session_state.current_step = 4
                st.rerun()
                
    elif st.session_state.current_step == 4:
        st.subheader("💻 System Information")
        st.info(f"Department: {st.session_state.department} | Tool: {st.session_state.tool} | User: {st.session_state.user}")
        system_number = st.text_input("Enter your system number:")
        
        is_valid = len(system_number) >= 5 if system_number else False
        if system_number and not is_valid:
            st.warning("System number should be at least 5 characters long")
            
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                st.session_state.current_step = 3
                st.rerun()
        with col2:
            if st.button("Next", disabled=not is_valid):
                st.session_state.system_number = system_number
                st.session_state.current_step = 5
                st.rerun()
                
    elif st.session_state.current_step == 5:
        st.subheader("📋 Survey Questions")
        st.info(f"Department: {st.session_state.department} | Tool: {st.session_state.tool} | User: {st.session_state.user}")
        
        time_saved = st.select_slider(
            "How much time do you save daily using this tool?",
            options=['Less than 30 mins', '30-60 mins', '1-2 hours', '2-4 hours', 'More than 4 hours']
        )
        
        satisfaction = st.slider(
            "How satisfied are you with the tool?",
            1, 5, 3,
            help="1: Very Dissatisfied, 5: Very Satisfied"
        )
        
        features = st.multiselect(
            "What features do you find most valuable?",
            ['Easy to use', 'Reduces manual work', 'Improves accuracy', 'Speeds up processes', 
             'Better organization', 'Cost savings']
        )
        
        new_skills = st.text_area(
            "What new skills have you developed since using this tool?",
            height=100
        )
        
        suggestions = st.text_area(
            "Do you have any suggestions for improvement?",
            height=100
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                st.session_state.current_step = 4
                st.rerun()
        with col2:
            if st.button("Submit"):
                if not features:
                    st.error("Please select at least one valuable feature")
                else:
                    response = {
                        'department': st.session_state.department,
                        'tool': st.session_state.tool,
                        'user': st.session_state.user,
                        'system_number': st.session_state.system_number,
                        'time_saved': time_saved,
                        'satisfaction': satisfaction,
                        'valuable_features': ', '.join(features),
                        'new_skills': new_skills,
                        'suggestions': suggestions,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    st.session_state.responses.append(response)
                    st.session_state.current_step = 6
                    st.rerun()

    elif st.session_state.current_step == 6:
        st.success("🎉 Thank you! Your survey has been submitted successfully.")
        st.balloons()
        
        if st.button("Submit Another Response"):
            reset_form()
            st.rerun()

    # Admin view in expander
    with st.expander("Admin View (Password Protected)"):
        if check_admin_password():
            if st.button("Logout", key="logout"):
                st.session_state.admin_authenticated = False
                st.rerun()
                
            if st.session_state.responses:
                df = pd.DataFrame(st.session_state.responses)
                st.dataframe(df)
                
                # Download button for admin
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download Responses (CSV)",
                    csv,
                    "survey_responses.csv",
                    "text/csv",
                    key='download-csv'
                )
            else:
                st.info("No responses collected yet.")

if __name__ == "__main__":
    main()