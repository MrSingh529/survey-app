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
    page_title="🤖 Automation Tools Survey",
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

    .question-text {
        font-size: 1.1rem;
        font-weight: 500;
        color: #2c3e50;
        margin: 1.5rem 0 1rem 0;
    }

    .stTextArea textarea {
        border: 1px solid #ccc !important;
        border-radius: 5px !important;
        padding: 10px !important;
        background-color: white !important;
    }

    .stTextArea textarea:focus {
        border-color: #1f77b4 !important;
        box-shadow: 0 0 0 1px #1f77b4 !important;
    }

    /* Updated Radio Button Styling for Vertical Layout */
    .stRadio > div {
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
        padding: 10px 0 !important;
    }
    
    .stRadio > div > label {
        padding: 8px 15px !important;
        cursor: pointer !important;
        border-radius: 4px !important;
        transition: background-color 0.2s !important;
        margin: 0 !important;
    }

    .stRadio > div > label:hover {
        background-color: #f0f7ff !important;
    }

    /* MultiSelect Styling */
    .stMultiSelect {
        margin-top: 10px;
    }

    .stMultiSelect > div {
        background-color: white !important;
        border: 1px solid #ddd !important;
        border-radius: 5px !important;
    }

    .section-title {
        color: #1f77b4;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #edf2f7;
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
                RV Solutions
            </h1>
            <h2 style='
                font-size: 1.8rem;
                font-weight: 600;
                color: #2ecc71;
                margin-bottom: 2rem;
            '>
                🤖 Automation Tools Survey
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
        
        # Tool Usage section
        st.markdown('<div class="section-title">🛠 Tool Usage and Satisfaction</div>', unsafe_allow_html=True)
        
        # Duration question
        st.markdown('<div class="question-text">How long have you been using this tool? *</div>', unsafe_allow_html=True)
        usage_duration = st.radio(
            " ",  # Single space
            ['Less than 1 month', '1-3 months', 'More than 3 months'],
            key="duration_radio",
            index=None
        )
        
        # Satisfaction question
        st.markdown('<div class="question-text">On a scale of 1-5, how satisfied are you with the tool? (1 = Very Dissatisfied, 5 = Very Satisfied) *</div>', unsafe_allow_html=True)
        satisfaction = st.radio(
            " ",  # Single space
            ['1', '2', '3', '4', '5'],
            key="satisfaction_radio",
            index=None
        )
        
        # Features question
        st.markdown('<div class="question-text">What aspects of the tool do you find most valuable? (Select all that apply) *</div>', unsafe_allow_html=True)
        features = st.multiselect(
            " ",  # Single space
            options=['Easy to use', 'Reduces manual work', 'Improves accuracy', 'Speeds up processes', 'Other'],
            key="features_select"
        )
        
        # Time and Productivity Impact
        st.markdown('<div class="section-title">⏱ Time and Productivity Impact</div>', unsafe_allow_html=True)
        
        # Time saved question
        st.markdown('<div class="question-text">On average, how much time do you save daily using this tool? *</div>', unsafe_allow_html=True)
        time_saved = st.radio(
            " ",  # Single space
            ['30-60 minutes', '1-2 hours', '2-4 hours', 'More than 4 hours'],
            key="time_saved_radio",
            index=None
        )
        
        # Automation percentage question
        st.markdown('<div class="question-text">What percentage of your previous manual tasks has been automated? *</div>', unsafe_allow_html=True)
        automation_percentage = st.radio(
            " ",  # Single space
            ['0-25%', '26-50%', '51-75%', '76-100%'],
            key="automation_radio",
            index=None
        )
        
        # Time utilization question
        st.markdown('<div class="question-text">How are you utilizing the time saved through automation? *</div>', unsafe_allow_html=True)
        time_utilization = st.text_area(
            " ",  # Single space
            height=100,
            placeholder="Please describe how you are using the time saved...",
            key="time_util"
        )
        
        # Process Improvement section
        st.markdown('<div class="section-title">📈 Process Improvement</div>', unsafe_allow_html=True)
        
        # Error reduction question
        st.markdown('<div class="question-text">Have you noticed any reduction in errors since using the automation tool? *</div>', unsafe_allow_html=True)
        error_reduction = st.radio(
            " ",  # Single space
            ['Yes', 'No', 'Errors have increased'],
            key="error_red",
            index=None
        )
        
        # Suggestions question
        st.markdown('<div class="question-text">Do you have any suggestions for improving the tool? *</div>', unsafe_allow_html=True)
        suggestions = st.text_area(
            " ",  # Single space
            height=100,
            placeholder="Please share your suggestions for improvement...",
            key="suggestions"
        )
        
        # Job satisfaction question
        st.markdown('<div class="question-text">How has the automation tool affected your job satisfaction? *</div>', unsafe_allow_html=True)
        job_satisfaction = st.radio(
            " ",  # Single space
            ['Positively', 'No Change', 'Negatively'],
            key="job_satisfaction",
            index=None
        )
        
        # Additional feedback question
        st.markdown('<div class="question-text">Additional comments or feedback (Optional):</div>', unsafe_allow_html=True)
        additional_feedback = st.text_area(
            " ",  # Single space
            height=100,
            placeholder="Please share any additional feedback...",
            key="feedback"
        )
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state.current_step = 4
                st.rerun()
        with col2:
            if st.button("Submit"):
                if not features:
                    st.error("Please select at least one valuable feature")
                elif not usage_duration or not satisfaction or not time_saved or not automation_percentage or not time_utilization or not error_reduction or not job_satisfaction:
                    st.error("Please answer all required questions marked with *")
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