import streamlit as st
import pandas as pd
from datetime import datetime
import time
import os

# Initialize session state variables
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'responses' not in st.session_state:
    if os.path.exists('survey_responses.csv'):
        st.session_state.responses = pd.read_csv('survey_responses.csv').to_dict('records')
    else:
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

# Function to save responses to CSV
def save_responses_to_csv():
    df = pd.DataFrame(st.session_state.responses)
    df.to_csv('survey_responses.csv', index=False)

# Add system-tool mapping
SYSTEM_TOOL_MAPPING = {
    'TSG': {
        'RA Invoice Tracker': ['RVS0F5C', 'RVS0F42', 'RVS1034'],
        'RA PO Extraction Tool': ['Not Installed', 'Not Installed', 'Not Installed'],
        'Telecom RAN KPI': ['Developed but Not Installed', 'Developed but Not Installed'],
        'RV PermitFlow (PTW App)': ['RVS104C', 'RV Employee', 'Partner']
    },
    'Finance': {
        'SMS & Tally Fnf Reco': ['RVS120A', 'RVS1094'],
        'Samsung Collections Reco': ['Not Installed', 'Not Installed', 'Not Installed']
    },
    'CSD': {
        'STN MIS Update Tool': ['RVSBF0', 'RVS0E77'],
        'Realme Claim Update Tool': ['In Development', 'In Development'],
        'RV SMS Claim Update Tool': ['In Development', 'In Development'],
        'GR Invoice Generator': ['RVS0E7F'],
        'Inventory & OOW Report Automation': ['RVS0E7F'],
        'IW Invoice Generator': ['RVS0E7F']
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
            'RV SMS Claim Update Tool': ['Hari Kishan', 'Mohit Senger'],
            'GR Invoice Generator': ['Zasim'],
            'Inventory & OOW Report Automation': ['Zasim'],
            'IW Invoice Generator': ['Zasim']
        }
    },
    'TSG': {
        'tools': {
            'RA Invoice Tracker': ['Rekha Pujari', 'Kokil Goswami', 'Sonika'],
            'RA PO Extraction Tool': ['NA', 'NA'],
            'Telecom RAN KPI': ['NA', 'NA'],
            'RV PermitFlow (PTW App)': ['Richa Babbar', 'RV Employee', 'Partner']
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
    # Add Logo with controlled size
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image('logo.png', width=300)  # Adjust width to 200 pixels
    
    # Title and Heading
    st.markdown("""
        <div style='padding: 1.5rem 0; text-align: center;'>
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

        # Initialize response dictionary
        response = {}

        if st.session_state.tool == "RV PermitFlow (PTW App)":
            # PTW-specific questions
            # Tool Usage and Satisfaction
            st.markdown('<div class="section-title">🛠 Tool Usage and Satisfaction</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-text">How frequently do you use the PTW automation tool? *</div>', unsafe_allow_html=True)
            ptw_frequency = st.radio(
                " ", 
                ['Daily', 'Weekly', 'Occasionally', 'Rarely', 'Never'],
                key="ptw_frequency_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">How satisfied are you with the PTW automation tool\'s user interface? (1 = Very Dissatisfied, 5 = Very Satisfied) *</div>', unsafe_allow_html=True)
            ptw_ui_satisfaction = st.radio(
                " ", 
                ['1', '2', '3', '4', '5'],
                key="ptw_ui_satisfaction_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">What improvements would you suggest for the PTW automation tool\'s usability? *</div>', unsafe_allow_html=True)
            ptw_usability_improvements = st.text_area(
                " ", 
                height=100,
                placeholder="Please share your suggestions for usability improvements...",
                key="ptw_usability_improvements"
            )
            
            st.markdown('<div class="question-text">How well does the PTW automation tool handle the most common PTW processes? *</div>', unsafe_allow_html=True)
            ptw_process_handling = st.radio(
                " ", 
                ['Very well', 'Adequately', 'Needs improvement', 'Not effective'],
                key="ptw_process_handling_radio",
                index=None
            )
            
            # Time and Productivity Impact
            st.markdown('<div class="section-title">⏱ Time and Productivity Impact</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-text">On average, how much time do you save per PTW task due to automation? *</div>', unsafe_allow_html=True)
            ptw_time_saved = st.radio(
                " ", 
                ['10-30 minutes', '30 minutes to 1 hour', '1-2 hours', 'More than 2 hours'],
                key="ptw_time_saved_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">Has the PTW automation tool helped in reducing manual errors or delays in PTW processing? *</div>', unsafe_allow_html=True)
            ptw_error_reduction = st.radio(
                " ", 
                ['Significantly', 'Moderately', 'Slightly', 'Not at all'],
                key="ptw_error_reduction_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">How has the PTW automation impacted your overall workflow? *</div>', unsafe_allow_html=True)
            ptw_workflow_impact = st.multiselect(
                " ", 
                options=['Improved efficiency', 'Streamlined communication', 'Reduced stress', 'No significant change'],
                key="ptw_workflow_impact_multi"
            )
            
            # System Performance & Support
            st.markdown('<div class="section-title">⚙ System Performance & Support</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-text">Have you encountered any technical issues or bugs while using the PTW automation tool? *</div>', unsafe_allow_html=True)
            ptw_technical_issues = st.radio(
                " ", 
                ['Yes, frequently', 'Yes, occasionally', 'No issues encountered'],
                key="ptw_technical_issues_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">How would you rate the support provided for the PTW automation tool? *</div>', unsafe_allow_html=True)
            ptw_support_rating = st.radio(
                " ", 
                ['Excellent', 'Good', 'Fair', 'Poor'],
                key="ptw_support_rating_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">How easy was it to adapt to the PTW automation tool compared to the manual process? *</div>', unsafe_allow_html=True)
            ptw_adaptation_ease = st.radio(
                " ", 
                ['Very easy', 'Easy', 'Neutral', 'Difficult', 'Very difficult'],
                key="ptw_adaptation_ease_radio",
                index=None
            )
            
            # Overall Feedback and Future Use
            st.markdown('<div class="section-title">📝 Overall Feedback and Future Use</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-text">Do you feel that the PTW automation tool has improved the overall PTW process efficiency in your department? *</div>', unsafe_allow_html=True)
            ptw_process_efficiency = st.radio(
                " ", 
                ['Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'],
                key="ptw_process_efficiency_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">Would you recommend the PTW automation tool to others in your department or organization? *</div>', unsafe_allow_html=True)
            ptw_recommendation = st.radio(
                " ", 
                ['Yes', 'No', 'Not sure'],
                key="ptw_recommendation_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">What additional features or improvements would you like to see in future versions of the PTW automation tool? *</div>', unsafe_allow_html=True)
            ptw_future_improvements = st.text_area(
                " ", 
                height=100,
                placeholder="Please share your suggestions for future improvements...",
                key="ptw_future_improvements"
            )
            
            # Navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back"):
                    st.session_state.current_step = 4
                    st.rerun()
            with col2:
                if st.button("Submit"):
                    required_fields = [
                        ptw_frequency, ptw_ui_satisfaction, ptw_usability_improvements, ptw_process_handling,
                        ptw_time_saved, ptw_error_reduction, ptw_workflow_impact, ptw_technical_issues,
                        ptw_support_rating, ptw_adaptation_ease, ptw_process_efficiency, ptw_recommendation,
                        ptw_future_improvements
                    ]
                    if not all(required_fields):
                        st.error("Please answer all required questions marked with *")
                    else:
                        response = {
                            'department': st.session_state.department,
                            'tool': st.session_state.tool,
                            'user': st.session_state.user,
                            'system_number': st.session_state.system_number,
                            'ptw_frequency': ptw_frequency,
                            'ptw_ui_satisfaction': ptw_ui_satisfaction,
                            'ptw_usability_improvements': ptw_usability_improvements,
                            'ptw_process_handling': ptw_process_handling,
                            'ptw_time_saved': ptw_time_saved,
                            'ptw_error_reduction': ptw_error_reduction,
                            'ptw_workflow_impact': ', '.join(ptw_workflow_impact),
                            'ptw_technical_issues': ptw_technical_issues,
                            'ptw_support_rating': ptw_support_rating,
                            'ptw_adaptation_ease': ptw_adaptation_ease,
                            'ptw_process_efficiency': ptw_process_efficiency,
                            'ptw_recommendation': ptw_recommendation,
                            'ptw_future_improvements': ptw_future_improvements,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.responses.append(response)
                        st.session_state.current_step = 6
                        st.rerun()

        elif st.session_state.tool == "Inventory & OOW Report Automation":
            # Inventory & OOW-specific questions
            # Tool Usage and Satisfaction
            st.markdown('<div class="section-title">🛠 Tool Usage and Satisfaction</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-text">How frequently do you use the Inventory & OOW Report Automation tool? *</div>', unsafe_allow_html=True)
            inv_frequency = st.radio(
                " ", 
                ['Daily', 'Weekly', 'Occasionally', 'Rarely', 'Never'],
                key="inv_frequency_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">How satisfied are you with the user interface of the Inventory & OOW Report Automation tool? (1 = Very Dissatisfied, 5 = Very Satisfied) *</div>', unsafe_allow_html=True)
            inv_ui_satisfaction = st.radio(
                " ", 
                ['1', '2', '3', '4', '5'],
                key="inv_ui_satisfaction_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">What improvements would you suggest for the usability of the Inventory & OOW Report Automation tool? *</div>', unsafe_allow_html=True)
            inv_usability_improvements = st.text_area(
                " ", 
                height=100,
                placeholder="Please share your suggestions for improving the tool’s usability...",
                key="inv_usability_improvements"
            )
            
            st.markdown('<div class="question-text">How effective is the dashboard in providing insights into inventory and OOW data? *</div>', unsafe_allow_html=True)
            inv_dashboard_effectiveness = st.radio(
                " ", 
                ['Very effective', 'Moderately effective', 'Slightly effective', 'Not effective'],
                key="inv_dashboard_effectiveness_radio",
                index=None
            )
            
            # Time and Productivity Impact
            st.markdown('<div class="section-title">⏱ Time and Productivity Impact</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-text">On average, how much time do you save per inventory or OOW report task due to automation? *</div>', unsafe_allow_html=True)
            inv_time_saved = st.radio(
                " ", 
                ['10-30 minutes', '30 minutes to 1 hour', '1-2 hours', 'More than 2 hours'],
                key="inv_time_saved_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">Has the Inventory & OOW Report Automation tool reduced manual errors in report generation or email distribution? *</div>', unsafe_allow_html=True)
            inv_error_reduction = st.radio(
                " ", 
                ['Significantly', 'Moderately', 'Slightly', 'Not at all'],
                key="inv_error_reduction_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">Which aspects of your inventory and OOW reporting workflow have been improved by the automation tool? (Select all that apply) *</div>', unsafe_allow_html=True)
            inv_workflow_impact = st.multiselect(
                " ", 
                options=['Faster report generation', 'Accurate data summaries', 'Simplified email distribution', 'Reduced manual data entry', 'No significant change'],
                key="inv_workflow_impact_multi"
            )
            
            # System Performance & Support
            st.markdown('<div class="section-title">⚙ System Performance & Support</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-text">Have you encountered any technical issues or bugs while using the Inventory & OOW Report Automation tool? *</div>', unsafe_allow_html=True)
            inv_technical_issues = st.radio(
                " ", 
                ['Yes, frequently', 'Yes, occasionally', 'No issues encountered'],
                key="inv_technical_issues_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">How would you rate the support provided for the Inventory & OOW Report Automation tool? *</div>', unsafe_allow_html=True)
            inv_support_rating = st.radio(
                " ", 
                ['Excellent', 'Good', 'Fair', 'Poor'],
                key="inv_support_rating_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">How easy was it to configure the tool (e.g., setting up Excel files, output folders, or email settings)? *</div>', unsafe_allow_html=True)
            inv_config_ease = st.radio(
                " ", 
                ['Very easy', 'Easy', 'Neutral', 'Difficult', 'Very difficult'],
                key="inv_config_ease_radio",
                index=None
            )
            
            # Overall Feedback and Future Use
            st.markdown('<div class="section-title">📝 Overall Feedback and Future Use</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-text">Do you agree that the Inventory & OOW Report Automation tool has improved the efficiency of inventory and OOW reporting in your department? *</div>', unsafe_allow_html=True)
            inv_process_efficiency = st.radio(
                " ", 
                ['Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'],
                key="inv_process_efficiency_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">What additional features or improvements would you like to see in future versions of the Inventory & OOW Report Automation tool? *</div>', unsafe_allow_html=True)
            inv_future_improvements = st.text_area(
                " ", 
                height=100,
                placeholder="Please share your suggestions for future features or improvements...",
                key="inv_future_improvements"
            )
            
            st.markdown('<div class="question-text">Do you have any additional comments or feedback about the Inventory & OOW Report Automation tool? (Optional)</div>', unsafe_allow_html=True)
            inv_additional_feedback = st.text_area(
                " ", 
                height=100,
                placeholder="Please share any additional feedback...",
                key="inv_additional_feedback"
            )
            
            # Navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back"):
                    st.session_state.current_step = 4
                    st.rerun()
            with col2:
                if st.button("Submit"):
                    required_fields = [
                        inv_frequency, inv_ui_satisfaction, inv_usability_improvements, inv_dashboard_effectiveness,
                        inv_time_saved, inv_error_reduction, inv_workflow_impact, inv_technical_issues,
                        inv_support_rating, inv_config_ease, inv_process_efficiency,
                        inv_future_improvements
                    ]
                    if not all(required_fields):
                        st.error("Please answer all required questions marked with *")
                    else:
                        response = {
                            'department': st.session_state.department,
                            'tool': st.session_state.tool,
                            'user': st.session_state.user,
                            'system_number': st.session_state.system_number,
                            'inv_frequency': inv_frequency,
                            'inv_ui_satisfaction': inv_ui_satisfaction,
                            'inv_usability_improvements': inv_usability_improvements,
                            'inv_dashboard_effectiveness': inv_dashboard_effectiveness,
                            'inv_time_saved': inv_time_saved,
                            'inv_error_reduction': inv_error_reduction,
                            'inv_workflow_impact': ', '.join(inv_workflow_impact),
                            'inv_technical_issues': inv_technical_issues,
                            'inv_support_rating': inv_support_rating,
                            'inv_config_ease': inv_config_ease,
                            'inv_process_efficiency': inv_process_efficiency,
                            'inv_future_improvements': inv_future_improvements,
                            'inv_additional_feedback': inv_additional_feedback,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.responses.append(response)
                        st.session_state.current_step = 6
                        st.rerun()

        else:
            # General questions for other tools
            st.markdown('<div class="section-title">🛠 Tool Usage and Satisfaction</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-text">How long have you been using this tool? *</div>', unsafe_allow_html=True)
            usage_duration = st.radio(
                " ", 
                ['Less than 1 month', '1-3 months', 'More than 3 months'],
                key="duration_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">On a scale of 1-5, how satisfied are you with the tool? (1 = Very Dissatisfied, 5 = Very Satisfied) *</div>', unsafe_allow_html=True)
            satisfaction = st.radio(
                " ", 
                ['1', '2', '3', '4', '5'],
                key="satisfaction_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">What aspects of the tool do you find most valuable? (Select all that apply) *</div>', unsafe_allow_html=True)
            features = st.multiselect(
                " ", 
                options=['Easy to use', 'Reduces manual work', 'Improves accuracy', 'Speeds up processes', 'Other'],
                key="features_select"
            )
            
            st.markdown('<div class="section-title">⏱ Time and Productivity Impact</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-text">On average, how much time do you save daily using this tool? *</div>', unsafe_allow_html=True)
            time_saved = st.radio(
                " ", 
                ['30-60 minutes', '1-2 hours', '2-4 hours', 'More than 4 hours'],
                key="time_saved_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">What percentage of your previous manual tasks has been automated? *</div>', unsafe_allow_html=True)
            automation_percentage = st.radio(
                " ", 
                ['0-25%', '26-50%', '51-75%', '76-100%'],
                key="automation_radio",
                index=None
            )
            
            st.markdown('<div class="question-text">How are you utilizing the time saved through automation? *</div>', unsafe_allow_html=True)
            time_utilization = st.text_area(
                " ", 
                height=100,
                placeholder="Please describe how you are using the time saved...",
                key="time_util"
            )
            
            st.markdown('<div class="section-title">📈 Process Improvement</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="question-text">Have you noticed any reduction in errors since using the automation tool? *</div>', unsafe_allow_html=True)
            error_reduction = st.radio(
                " ", 
                ['Yes', 'No', 'Errors have increased'],
                key="error_red",
                index=None
            )
            
            st.markdown('<div class="question-text">Do you have any suggestions for improving the tool? *</div>', unsafe_allow_html=True)
            suggestions = st.text_area(
                " ", 
                height=100,
                placeholder="Please share your suggestions for improvement...",
                key="suggestions"
            )
            
            st.markdown('<div class="question-text">How has the automation tool affected your job satisfaction? *</div>', unsafe_allow_html=True)
            job_satisfaction = st.radio(
                " ", 
                ['Positively', 'No Change', 'Negatively'],
                key="job_satisfaction",
                index=None
            )
            
            st.markdown('<div class="question-text">Additional comments or feedback (Optional):</div>', unsafe_allow_html=True)
            additional_feedback = st.text_area(
                " ", 
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

    if st.session_state.current_step == 6:
        st.markdown("""
            <div class='success-message'>
                <h2>🎉 Thank you!</h2>
                <p style='font-size: 1.2em; color: #2c3e50;'>
                    Your survey has been submitted successfully.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
        # Save response to CSV for persistence
        save_responses_to_csv()
        
        # Center the button
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("📜 Submit Another Response"):
                show_spinner_with_message("Preparing new survey...")
                reset_form()
                st.rerun()

    # Enhanced Admin view
    with st.expander("🔒 Admin View (Password Protected)"):
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
                        "📅 Download Responses (CSV)",
                        csv,
                        "survey_responses.csv",
                        "text/csv",
                        key='download-csv'
                    )
            else:
                st.info("📊 No responses collected yet.")

if __name__ == "__main__":
    main()
