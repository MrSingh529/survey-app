import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Automation Tools Survey",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'responses' not in st.session_state:
    st.session_state.responses = []

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

def save_response(responses):
    """Save survey response to session state"""
    try:
        st.session_state.responses.append({
            **responses,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return True
    except Exception as e:
        st.error(f"Error saving response: {str(e)}")
        return False

def show_responses():
    """Display all responses in a table"""
    if st.session_state.responses:
        df = pd.DataFrame(st.session_state.responses)
        st.dataframe(df)
        
        # Convert to CSV for download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Responses as CSV",
            csv,
            "survey_responses.csv",
            "text/csv",
            key='download-csv'
        )
    else:
        st.info("No responses collected yet.")

def main():
    # Title with emoji
    st.markdown("""
        <h1 style='text-align: center; color: #1f77b4;'>
            🤖 Automation Tools Survey
        </h1>
    """, unsafe_allow_html=True)
    
    # Admin view for responses
    if st.sidebar.checkbox("Show Admin View"):
        st.sidebar.subheader("Survey Responses")
        show_responses()
        return

    # Progress bar
    progress_text = f"Step {st.session_state.current_step} of 5"
    st.progress(st.session_state.current_step / 5)
    st.write(progress_text)
    
    # Main form container
    with st.container():
        if st.session_state.current_step == 1:
            st.subheader("👥 Department Selection")
            department = st.selectbox(
                "Please select your department:",
                options=list(DEPARTMENT_DATA.keys())
            )
            if st.button("Next →"):
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
                if st.button("← Back"):
                    st.session_state.current_step = 1
                    st.rerun()
            with col2:
                if st.button("Next →"):
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
                if st.button("← Back"):
                    st.session_state.current_step = 2
                    st.rerun()
            with col2:
                if st.button("Next →"):
                    st.session_state.user = user
                    st.session_state.current_step = 4
                    st.rerun()
                    
        elif st.session_state.current_step == 4:
            st.subheader("💻 System Information")
            st.info(f"Department: {st.session_state.department} | Tool: {st.session_state.tool} | User: {st.session_state.user}")
            system_number = st.text_input("Enter your system number:")
            
            # Add system number validation
            is_valid = len(system_number) >= 5 if system_number else False
            if system_number and not is_valid:
                st.warning("System number should be at least 5 characters long")
                
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back"):
                    st.session_state.current_step = 3
                    st.rerun()
            with col2:
                if st.button("Next →", disabled=not is_valid):
                    st.session_state.system_number = system_number
                    st.session_state.current_step = 5
                    st.rerun()
                    
        elif st.session_state.current_step == 5:
            st.subheader("📋 Survey Questions")
            st.info(f"Department: {st.session_state.department} | Tool: {st.session_state.tool} | User: {st.session_state.user}")
            
            with st.form("survey_form"):
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
                    back_button = st.form_submit_button("← Back")
                with col2:
                    submit_button = st.form_submit_button("Submit Survey")
                
                if back_button:
                    st.session_state.current_step = 4
                    st.rerun()
                
                if submit_button:
                    if not features:
                        st.error("Please select at least one valuable feature")
                        return
                        
                    responses = {
                        'department': st.session_state.department,
                        'tool': st.session_state.tool,
                        'user': st.session_state.user,
                        'system_number': st.session_state.system_number,
                        'time_saved': time_saved,
                        'satisfaction': satisfaction,
                        'valuable_features': ', '.join(features),
                        'new_skills': new_skills,
                        'suggestions': suggestions
                    }
                    
                    if save_response(responses):
                        st.success("🎉 Thank you! Your survey has been submitted successfully.")
                        st.balloons()
                        
                        if st.button("Submit Another Response"):
                            # Reset form-related session state
                            keys_to_keep = ['responses']
                            for key in list(st.session_state.keys()):
                                if key not in keys_to_keep:
                                    del st.session_state[key]
                            st.session_state.current_step = 1
                            st.rerun()

if __name__ == "__main__":
    main()