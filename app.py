import streamlit as st
import pandas as pd
from datetime import datetime

# Move page configuration to the very top
st.set_page_config(
    page_title="Automation Tools Survey",
    page_icon="🤖",
    layout="centered"
)

# Default password if secrets are not set up
ADMIN_PASSWORD = "@RVsolutions@1234"

# Try to get password from secrets if available
if hasattr(st, 'secrets') and 'general' in st.secrets:
    try:
        ADMIN_PASSWORD = st.secrets["general"]["admin_password"]
    except:
        pass

# Add system-tool mapping
SYSTEM_TOOL_MAPPING = {
    'TSG': {
        'RA Invoice Tracker': ['RVS0F5C', 'RVS0F42', 'RVS1034'],
        'RA PO Extraction Tool': ['Not Installed ', 'Not Installed', 'Not Installed']
        'Telecom RAN KPI': ['Developed but Not Installed ', 'Developed but Not Installed']
    },
    'Finance': {
        'SMS & Tally Fnf Reco': ['RVS120A', 'RVS1094'],
        'Samsung Collections Reco': ['Not Installed', 'Not Installed', 'Not Installed']
    },
    'CSD': {
        'STN MIS Update Tool': ['RVSBF0', 'RVS0E77'],
        'Realme Claim Update Tool': ['In Development', 'In Development']
        'RV SMS Claim Update Tool': ['In Development', 'In Development']
    }
}

# Your company data
DEPARTMENT_DATA = {
    'Finance': {
        'tools': {
            'SMS & Tally Fnf Reco': ['Anmol Dubey', 'Shruti Dixit'],
            'Samsung Collections Reco': ['NA', 'NA']
        }
    },
    'CSD': {
        'tools': {
            'STN MIS Update Tool': ['Inderjeet', 'Dushyant Kumar'],
            'Realme Claim Update Tool': ['Hari Kishan', 'Mohit Senger']
            'RV SMS Claim Update Tool': ['Hari Kishan', 'Mohit Senger']
        }
    },
    'TSG': {
        'tools': {
            'RA Invoice Tracker': ['Rekha Pujari', 'Kokil Goswami', 'Sonika'],
            'RA PO Extraction Tool': ['NA', 'NA']
            'Telecom RAN KPI': ['NA', 'NA']
        }
    }
}

def check_system_number(department, tool, system_number):
    """Check if the system number is valid for the selected department and tool"""
    if department in SYSTEM_TOOL_MAPPING and tool in SYSTEM_TOOL_MAPPING[department]:
        valid_systems = SYSTEM_TOOL_MAPPING[department][tool]
        return system_number in valid_systems
    return False

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
    if st.session_state.current_step < 6:
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
        
        # Show valid system numbers for reference (remove in production)
        if st.session_state.department in SYSTEM_TOOL_MAPPING and st.session_state.tool in SYSTEM_TOOL_MAPPING[st.session_state.department]:
            valid_systems = SYSTEM_TOOL_MAPPING[st.session_state.department][st.session_state.tool]
            st.caption(f"Valid system numbers for testing: {', '.join(valid_systems)}")
        
        system_number = st.text_input("Enter your system number:")
        
        is_valid_format = len(system_number) >= 5 if system_number else False
        is_valid_system = check_system_number(st.session_state.department, st.session_state.tool, system_number)
        
        if system_number:
            if not is_valid_format:
                st.warning("System number should be at least 5 characters long")
            elif not is_valid_system:
                st.error(f"❌ The tool '{st.session_state.tool}' is not installed on system {system_number}. Please contact IT support if you believe this is an error.")
            
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                st.session_state.current_step = 3
                st.rerun()
        with col2:
            if st.button("Next", disabled=not (is_valid_format and is_valid_system)):
                st.session_state.system_number = system_number
                st.session_state.current_step = 5
                st.rerun()
                
    elif st.session_state.current_step == 5:
        st.subheader("📋 Survey Questions")
        st.info(f"Department: {st.session_state.department} | Tool: {st.session_state.tool} | User: {st.session_state.user}")
        
        # 🛠 Tool Usage and Satisfaction
        st.subheader("🛠 Tool Usage and Satisfaction")
        
        usage_duration = st.radio(
            "How long have you been using this tool?",
            options=['Less than 1 month', '1-3 months', 'More than 3 months'],
            required=True
        )
        
        satisfaction = st.slider(
            "On a scale of 1-5, how satisfied are you with the tool? (1 = Very Dissatisfied, 5 = Very Satisfied)",
            1, 5, 3
        )
        
        features = st.multiselect(
            "What aspects of the tool do you find most valuable? (Select all that apply)",
            ['Easy to use', 'Reduces manual work', 'Improves accuracy', 'Speeds up processes', 'Other']
        )
        
        # ⏱ Time and Productivity Impact
        st.subheader("⏱ Time and Productivity Impact")
        
        time_saved = st.select_slider(
            "On average, how much time do you save daily by using this tool?",
            options=['30-60 minutes', '1-2 hours', '2-4 hours', 'More than 4 hours']
        )
        
        automation_percentage = st.select_slider(
            "What percentage of your previous manual tasks has been automated?",
            options=['0-25%', '26-50%', '51-75%', '76-100%']
        )
        
        time_utilization = st.text_area(
            "How are you utilizing the time saved through automation?",
            height=100
        )
        
        # 📈 Process Improvement
        st.subheader("📈 Process Improvement")
        
        error_reduction = st.radio(
            "Have you noticed any reduction in errors since using the automation tool?",
            options=['Yes', 'No', 'Errors have increased']
        )
        
        suggestions = st.text_area(
            "Do you have any suggestions for improving the tool?",
            height=100
        )
        
        job_satisfaction = st.radio(
            "How has the automation tool affected your job satisfaction?",
            options=['Positively', 'No Change', 'Negatively']
        )
        
        additional_feedback = st.text_area(
            "Please share any additional comments or feedback about your experience with the automation tool: (Optional)",
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
                        'usage_duration': usage_duration,
                        'satisfaction': satisfaction,
                        'valuable_features': ', '.join(features),
                        'time_saved': time_saved,
                        'automation_percentage': automation_percentage,
                        'time_utilization': time_utilization,
                        'error_reduction': error_reduction,
                        'suggestions': suggestions,
                        'job_satisfaction': job_satisfaction,
                        'additional_feedback': additional_feedback,
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