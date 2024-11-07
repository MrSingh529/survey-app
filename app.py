import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Initialize session state variables
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

# Custom CSS for better styling
st.set_page_config(
    page_title="Automation Tools Survey",
    page_icon="🤖",
    layout="centered"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
    }
    
    .stButton>button {
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    h1, h2 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    text-align: center;
    animation: fadeIn 1.5s ease-in;
    }

    .title-wrapper {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }

    .gradient-text {
        background: linear-gradient(45deg, #1f77b4, #2ecc71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .step-container {
        padding: 20px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 20px 0;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    
    @keyframes slideIn {
        0% { transform: translateY(20px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    .stProgress > div > div {
        background-color: #2ecc71;
        transition: all 0.3s ease;
    }
    
    .success-message {
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%);
        border-radius: 15px;
        animation: popIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    @keyframes popIn {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .info-box {
        background-color: #e8f4f8;
        border-left: 5px solid #1f77b4;
        padding: 10px 15px;
        margin: 10px 0;
        border-radius: 0 5px 5px 0;
    }
    
    .stSelectbox, .stTextInput {
        transition: all 0.3s ease;
    }
    
    .stSelectbox:hover, .stTextInput:hover {
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

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
        'RA PO Extraction Tool': ['Not Installed', 'Not Installed', 'Not Installed'],
        'Telecom RAN KPI': ['Developed but Not Installed', 'Developed but Not Installed']
    },
    'Finance': {
        'SMS & Tally Fnf Reco': ['RVS120A', 'RVS1094'],
        'Samsung Collections Reco': ['Not Installed', 'Not Installed', 'Not Installed']
    },
    'CSD': {
        'STN MIS Update Tool': ['RVSBF0', 'RVS0E77'],
        'Realme Claim Update Tool': ['In Development', 'In Development'],
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
            'Realme Claim Update Tool': ['Hari Kishan', 'Mohit Senger'],
            'RV SMS Claim Update Tool': ['Hari Kishan', 'Mohit Senger']
        }
    },
    'TSG': {
        'tools': {
            'RA Invoice Tracker': ['Rekha Pujari', 'Kokil Goswami', 'Sonika'],
            'RA PO Extraction Tool': ['NA', 'NA'],
            'Telecom RAN KPI': ['NA', 'NA']
        }
    }
}

def show_spinner_with_message(message, duration=0.5):
    with st.spinner(message):
        time.sleep(duration)

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
    # Title and Heading with company name
    st.markdown("""
        <div style='padding: 1.5rem 0; text-align: center;'>
            <h1 style='
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 1rem;
                color: #1f77b4;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            '>
                🤖 RV Solutions
            </h1>
            <h2 style='
                font-size: 1.8rem;
                font-weight: 600;
                color: #2ecc71;
                margin-bottom: 2rem;
            '>
                Automation Tools Survey
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress indicator
    if st.session_state.current_step < 6:
        col1, col2 = st.columns([7, 3])
        with col1:
            st.progress(st.session_state.current_step / 5)
        with col2:
            st.write(f"Step {st.session_state.current_step} of 5")
    
    # Main form container with animation
    st.markdown(f'<div class="step-container">', unsafe_allow_html=True)
    
    if st.session_state.current_step == 1:
        st.markdown("### 👥 Department Selection")
        st.markdown('<div class="info-box">Please select your department to begin the survey.</div>', 
                   unsafe_allow_html=True)
        department = st.selectbox(
            "Choose your department:",
            options=list(DEPARTMENT_DATA.keys())
        )
        if st.button("Next →"):
            show_spinner_with_message("Saving department selection...")
            st.session_state.department = department
            st.session_state.current_step = 2
            st.rerun()
            
    elif st.session_state.current_step == 2:
        st.markdown("### 🛠️ Tool Selection")
        st.markdown(f'<div class="info-box">Department: {st.session_state.department}</div>', 
                   unsafe_allow_html=True)
        tool = st.selectbox(
            "Which automation tool are you using?",
            options=list(DEPARTMENT_DATA[st.session_state.department]['tools'].keys())
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state.current_step = 1
                st.rerun()
        with col2:
            if st.button("Next →"):
                show_spinner_with_message("Loading tool information...")
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
        
        is_valid_format = len(system_number) >= 5 if system_number else False
        is_valid_system = check_system_number(st.session_state.department, st.session_state.tool, system_number)
        
        if system_number:
            if not is_valid_format:
                st.warning("System number should be at least 5 characters long")
            elif not is_valid_system:
                st.error(f"❌ The tool '{st.session_state.tool}' is not installed on system {system_number}. Please contact harpinder.singh@rvsolutions.in if you believe this is an error.")
            
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
        st.markdown("### 📋 Survey Questions")
        st.markdown(
            f'<div class="info-box">'
            f'Department: {st.session_state.department} | '
            f'Tool: {st.session_state.tool} | '
            f'User: {st.session_state.user}'
            f'</div>', 
            unsafe_allow_html=True
        )
        
        # Tool Usage section with animations and better spacing
        st.markdown("""
            <div style='padding: 20px 0;'>
                <h3 style='color: #1f77b4; animation: fadeIn 1s ease-in;'>
                    🛠 Tool Usage and Satisfaction
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        usage_duration = st.radio(
            "How long have you been using this tool? *",  # Added asterisk to indicate required
            options=['Less than 1 month', '1-3 months', 'More than 3 months']
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
                elif not usage_duration:  # Add validation for required fields
                    st.error("Please select how long you've been using the tool")
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
        st.markdown("""
            <div class='success-message'>
                <h2>🎉 Thank you!</h2>
                <p style='font-size: 1.2em; color: #2c3e50;'>
                    Your survey has been submitted successfully.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
        # Center the button
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("📝 Submit Another Response"):
                show_spinner_with_message("Preparing new survey...")
                reset_form()
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced Admin view
    with st.expander("🔐 Admin View (Password Protected)"):
        if check_admin_password():
            st.markdown("""
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px;'>
                    <h4 style='color: #2c3e50;'>Survey Responses Dashboard</h4>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", key="logout"):
                show_spinner_with_message("Logging out...")
                st.session_state.admin_authenticated = False
                st.rerun()
                
            if st.session_state.responses:
                df = pd.DataFrame(st.session_state.responses)
                st.dataframe(df)
                
                # Enhanced download button
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 Download Responses (CSV)",
                        csv,
                        "survey_responses.csv",
                        "text/csv",
                        key='download-csv'
                    )
            else:
                st.info("📊 No responses collected yet.")

if __name__ == "__main__":
    main()