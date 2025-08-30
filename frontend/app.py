# frontend/app.py
import streamlit as st
import requests
import time
import json

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:8000"

# --- Custom CSS for Modern Design ---
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Card Styling */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Alert Styling */
    .alert-success {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Progress Bar */
    .progress-bar {
        width: 100%;
        height: 4px;
        background: #e1e5e9;
        border-radius: 2px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
        animation: progress 2s ease-in-out;
    }
    
    @keyframes progress {
        0% { width: 0%; }
        100% { width: 100%; }
    }
    
    /* Drug Card Styling */
    .drug-card {
        background: #f8f9fa;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .drug-card:hover {
        border-color: #667eea;
        background: #f0f4ff;
    }
    
    /* Result Cards */
    .result-card {
        background: white;
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .severity-high {
        border-left-color: #e74c3c;
        background: #fdf2f2;
    }
    
    .severity-medium {
        border-left-color: #f39c12;
        background: #fef9e7;
    }
    
    .severity-low {
        border-left-color: #27ae60;
        background: #f0f9f4;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Enhanced Helper Functions ---
def verify_prescription_data(age, drugs):
    if not drugs:
        st.error("⚠️ Please enter at least one drug name.")
        return None
    
    request_data = {"age": age, "drugs": drugs}
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔍 Connecting to AI backend...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        status_text.text("🧠 AI analyzing drug interactions...")
        progress_bar.progress(50)
        
        response = requests.post(f"{BACKEND_URL}/verify-prescription/", json=request_data)
        progress_bar.progress(75)
        
        status_text.text("📊 Processing results...")
        time.sleep(0.5)
        progress_bar.progress(100)
        
        status_text.text("✅ Analysis complete!")
        time.sleep(0.5)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Backend Error: {response.json().get('detail', response.text)}")
            return None
    except requests.exceptions.RequestException as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"🔌 Connection Error: Could not connect to the backend. Please ensure it is running.\n\nError: {e}")
        return None

def display_interaction_results(interactions):
    if not interactions:
        st.success("✅ **No harmful drug interactions detected!** Your medications appear to be safe to take together.")
        return
    
    st.warning(f"⚠️ **{len(interactions)} potential interaction(s) found:**")
    
    for i, interaction in enumerate(interactions, 1):
        severity = interaction.get('severity', 'Unknown').lower()
        severity_class = f"severity-{severity}" if severity in ['high', 'medium', 'low'] else ""
        
        severity_emoji = {
            'high': '🚨',
            'medium': '⚠️', 
            'low': '💡'
        }.get(severity, '❓')
        
        st.markdown(f"""
        <div class="result-card {severity_class}">
            <h4>{severity_emoji} Interaction #{i}: {' & '.join(interaction['drugs_involved'])}</h4>
            <p><strong>Severity:</strong> {interaction['severity']}</p>
            <p><strong>Description:</strong> {interaction['description']}</p>
        </div>
        """, unsafe_allow_html=True)

def display_dosage_warnings(warnings):
    if not warnings:
        st.info("ℹ️ No specific dosage concerns identified.")
        return
    
    st.subheader("💊 Dosage Analysis")
    for warning in warnings:
        st.markdown(f"""
        <div class="result-card">
            <p>{warning}</p>
        </div>
        """, unsafe_allow_html=True)

def display_alternatives(alternatives):
    if not alternatives:
        st.info("ℹ️ No alternative medications suggested at this time.")
        return
    
    st.subheader("🔄 Alternative Suggestions")
    for alt in alternatives:
        st.markdown(f"""
        <div class="result-card">
            <p>💡 {alt}</p>
        </div>
        """, unsafe_allow_html=True)

# --- Main App Configuration ---
st.set_page_config(
    page_title="AI Medical Prescription Verification",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
load_custom_css()

# --- Header Section ---
st.markdown("""
<div class="main-header">
    <div class="main-title">💊 AI Medical Prescription Verification</div>
    <div class="main-subtitle">Advanced AI-powered drug interaction analysis and safety verification</div>
</div>
""", unsafe_allow_html=True)

# --- Disclaimer ---
st.markdown("""
<div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
    <strong>⚠️ Medical Disclaimer:</strong> This AI tool is for informational purposes only and is not a substitute for professional medical advice. Always consult a qualified healthcare provider before making any medical decisions.
</div>
""", unsafe_allow_html=True)

# --- Create Tabs for Each Feature ---
tab1, tab2, tab3 = st.tabs(["Interaction Checker", "Dosage Analyzer", "Extract from Note"])

# --- Tab 1: Interaction Checker ---
with tab1:
    st.markdown("""
    <div class="feature-card">
        <h2>🔍 Drug Interaction Checker</h2>
        <p>Analyze potential harmful interactions between multiple medications using advanced AI algorithms.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**👤 Patient Information**")
        age_interaction = st.number_input("Age", min_value=1, max_value=120, value=30, step=1, key="age_interaction")
        
        st.markdown("**📊 Quick Stats**")
        if 'interaction_drugs' in st.session_state:
            drug_count = len([d for d in st.session_state.interaction_drugs if d['name'].strip()])
            st.metric("Drugs Added", drug_count)
    
    with col2:
        st.markdown("**💊 Medication List**")
        
        if 'interaction_drugs' not in st.session_state:
            st.session_state.interaction_drugs = [{"name": "", "dosage": ""}, {"name": "", "dosage": ""}]

        for i, drug in enumerate(st.session_state.interaction_drugs):
            st.markdown(f"""
            <div class="drug-card">
                <h4>💊 Medication #{i+1}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            cols = st.columns([4, 2, 1])
            drug['name'] = cols[0].text_input(f"Drug Name", value=drug['name'], key=f"int_name_{i}", placeholder="e.g., Aspirin")
            drug['dosage'] = cols[1].text_input(f"Dosage", value=drug['dosage'], key=f"int_dosage_{i}", placeholder="e.g., 100mg")
            
            if len(st.session_state.interaction_drugs) > 2:
                if cols[2].button("🗑️", key=f"remove_{i}", help="Remove this drug"):
                    st.session_state.interaction_drugs.pop(i)
                    st.rerun()

        col_add, col_analyze = st.columns([1, 1])
        
        with col_add:
            if st.button("➕ Add Another Drug", key="add_interaction_drug", use_container_width=True):
                st.session_state.interaction_drugs.append({"name": "", "dosage": ""})
                st.rerun()
        
        with col_analyze:
            if st.button("🔍 Analyze Interactions", type="primary", key="analyze_interactions", use_container_width=True):
                valid_drugs = [d for d in st.session_state.interaction_drugs if d['name'].strip()]
                results = verify_prescription_data(age_interaction, valid_drugs)
                
                if results:
                    st.markdown("---")
                    display_interaction_results(results['interactions'])
                    display_dosage_warnings(results['dosage_warnings'])
                    display_alternatives(results['alternative_suggestions'])


# --- Tab 2: Dosage Analyzer ---
with tab2:
    st.markdown("""
    <div class="feature-card">
        <h2>💊 Age-Specific Dosage Analyzer</h2>
        <p>Verify if medication dosages are appropriate for specific age groups using AI-powered analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**👤 Patient Details**")
        age_dosage = st.number_input("Patient Age", min_value=1, max_value=120, value=30, step=1, key="age_dosage")
        
        # Age category display
        if age_dosage < 2:
            age_category = "👶 Infant"
        elif age_dosage < 12:
            age_category = "🧒 Child"
        elif age_dosage < 18:
            age_category = "👦 Adolescent"
        elif age_dosage < 65:
            age_category = "👨 Adult"
        else:
            age_category = "👴 Senior"
            
        st.info(f"**Age Category:** {age_category}")
    
    with col2:
        st.markdown("**💊 Medication Information**")
        
        st.markdown("""
        <div class="drug-card">
            <h4>🔬 Single Drug Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns([3, 2])
        dosage_drug_name = cols[0].text_input("Drug Name", key="dosage_drug_name", placeholder="e.g., Ibuprofen")
        dosage_drug_amount = cols[1].text_input("Dosage", placeholder="e.g., 400mg", key="dosage_drug_amount")

        if st.button("🔍 Analyze Dosage Safety", type="primary", use_container_width=True):
            if dosage_drug_name and dosage_drug_amount:
                drug_to_check = [{"name": dosage_drug_name, "dosage": dosage_drug_amount}]
                results = verify_prescription_data(age_dosage, drug_to_check)
                if results:
                    st.markdown("---")
                    display_dosage_warnings(results['dosage_warnings'])
                    display_alternatives(results['alternative_suggestions'])
            else:
                st.error("⚠️ Please enter both a drug name and dosage amount.")


# --- Tab 3: Extract from Prescription Note ---
with tab3:
    st.markdown("""
    <div class="feature-card">
        <h2>📝 Smart Prescription Text Extractor</h2>
        <p>Extract structured medication information from unstructured prescription notes using advanced NLP.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**📄 Prescription Note**")
        unstructured_text = st.text_area(
            "Paste prescription text here:", 
            height=200,
            placeholder="Example: Patient should take Aspirin 100mg twice daily and Metformin 500mg with meals..."
        )
        
        # Sample text button
        if st.button("📋 Use Sample Text", help="Load a sample prescription for testing"):
            sample_text = """Patient: John Doe, Age: 45
            
Prescription:
- Lisinopril 10mg once daily for blood pressure
- Metformin 500mg twice daily with meals for diabetes
- Aspirin 81mg once daily for cardiovascular protection
- Atorvastatin 20mg at bedtime for cholesterol

Instructions: Take all medications as prescribed. Follow up in 3 months."""
            st.session_state.sample_text = sample_text
            st.rerun()
        
        if 'sample_text' in st.session_state:
            unstructured_text = st.session_state.sample_text
    
    with col2:
        st.markdown("**🎯 Extraction Tips**")
        st.info("""
        **Best Results:**
        - Include drug names
        - Mention dosages (mg, ml, etc.)
        - Add frequency if available
        - Use clear formatting
        """)
        
        st.markdown("**📊 Text Stats**")
        if unstructured_text:
            word_count = len(unstructured_text.split())
            char_count = len(unstructured_text)
            st.metric("Words", word_count)
            st.metric("Characters", char_count)

    if st.button("🔍 Extract Medication Information", type="primary", use_container_width=True):
        if unstructured_text:
            # Progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🔍 Analyzing prescription text...")
                progress_bar.progress(33)
                time.sleep(0.5)
                
                status_text.text("🧠 AI extracting medication data...")
                progress_bar.progress(66)
                
                response = requests.post(f"{BACKEND_URL}/extract-from-text/", params={"text": unstructured_text})
                progress_bar.progress(100)
                
                status_text.text("✅ Extraction complete!")
                time.sleep(0.5)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                if response.status_code == 200:
                    extracted_drugs = response.json()
                    if extracted_drugs:
                        st.markdown("---")
                        st.subheader("✅ Extracted Medications")
                        
                        for i, drug in enumerate(extracted_drugs, 1):
                            drug_name = drug.get('name', 'N/A')
                            drug_dosage = drug.get('dosage', 'Not specified')
                            
                            st.markdown(f"""
                            <div class="result-card">
                                <h4>💊 Medication #{i}: {drug_name}</h4>
                                <p><strong>Dosage:</strong> {drug_dosage}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Option to analyze extracted drugs
                        st.markdown("**🔍 Next Steps**")
                        if st.button("🚀 Analyze These Medications for Interactions", type="secondary"):
                            # Store extracted drugs for interaction analysis
                            st.session_state.interaction_drugs = [
                                {"name": drug.get('name', ''), "dosage": drug.get('dosage', '')} 
                                for drug in extracted_drugs
                            ]
                            st.success("✅ Medications loaded into Interaction Checker! Switch to the first tab to analyze.")
                    else:
                        st.warning("🤔 Could not extract any structured drug information from the text. Try rephrasing or adding more details.")
                else:
                    st.error(f"❌ Extraction Error: {response.text}")
            except requests.exceptions.RequestException as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"🔌 Connection Error: Could not connect to the backend: {e}")
        else:
            st.error("⚠️ Please paste some prescription text to analyze.")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>🏥 <strong>AI Medical Prescription Verification System</strong></p>
    <p>Powered by advanced AI models for drug interaction analysis and safety verification</p>
    <p><em>Always consult with healthcare professionals for medical decisions</em></p>
</div>
""", unsafe_allow_html=True)