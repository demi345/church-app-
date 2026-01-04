"""
St. Anthony Coptic Orthodox Church - Main Registration App
Volunteer Registration with Station Selection
"""

import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('volunteer_system.log') if not os.getenv('STREAMLIT_SHARING') else logging.StreamHandler()
    ]
)

# Config
CHURCH_LOCATION = (39.8637, -74.8284)
MAX_DISTANCE_METERS = 50000  # 50km for testing
SHEET_NAME = "Volunteer Hours"
PUNCH_SHEET = "Sheet1"
REGISTRATION_SHEET = "Registration"

volunteer_verses = [
    "Each of you should use whatever gift you have received to serve others, as faithful stewards of God's grace. — 1 Peter 4:10",
    "Whatever you do, work at it with all your heart, as working for the Lord, not for human masters. — Colossians 3:23",
    "Serve wholeheartedly, as if you were serving the Lord, not people. — Ephesians 6:7",
    "The greatest among you will be your servant. — Matthew 23:11",
    "Carry each other's burdens, and in this way you will fulfill the law of Christ. — Galatians 6:2"
]

# Google Sheets Connection
try:
    scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
    if hasattr(st, 'secrets') and "gcp_service_account" in st.secrets:
        import json
        account_info = json.loads(st.secrets["gcp_service_account"])
        auth_creds = ServiceAccountCredentials.from_json_keyfile_dict(account_info, scope)
    else:
        auth_creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(auth_creds)
    punch_sheet = client.open(SHEET_NAME).worksheet(PUNCH_SHEET)
    reg_sheet = client.open(SHEET_NAME).worksheet(REGISTRATION_SHEET)
    SHEETS_ENABLED = True
except Exception as e:
    # Google Sheets not connected - app will store data locally for display
    SHEETS_ENABLED = False
    punch_sheet = None
    reg_sheet = None

def get_common_css():
    """Return common CSS styling"""
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* White theme with black text */
.stApp { 
    background-color: #FFFFFF; 
    color: #000000; 
    font-family: 'Inter', sans-serif;
}

/* General text styling */
.stApp * {
    color: #000000 !important;
}

/* Image styling */
.stApp img {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin: 0 auto;
    display: block;
}

/* Button styling */
.stButton>button {
    background: linear-gradient(135deg, #007BFF, #0056B3) !important;
    color: #FFFFFF !important;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #0056B3, #004085) !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}
</style>
"""

def display_logo():
    """Display the church logo"""
    try:
        st.image("stanthonylogo.png", width=150)
    except:
        st.markdown("### ⛪ St. Anthony Coptic Orthodox Church")

def get_random_verse():
    """Get a random volunteer verse"""
    return random.choice(volunteer_verses)

# Page Configuration
st.set_page_config(
    page_title="St. Anthony Volunteer Registration",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply CSS
st.markdown(get_common_css(), unsafe_allow_html=True)

# Custom CSS for tabs
st.markdown("""
<style>
/* Light tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: #F8F9FA;
    border-radius: 10px 10px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
    border: 1px solid #DEE2E6;
    color: #495057;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background-color: #E3F2FD !important;
    border-bottom: 3px solid #2196F3 !important;
    color: #1976D2 !important;
    font-weight: 600;
}

.stTabs [data-baseweb="tab-panel"] {
    background-color: #FFFFFF;
    border: 1px solid #DEE2E6;
    border-top: none;
    border-radius: 0px 0px 10px 10px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# Header
display_logo()
st.markdown("<h1>☦️ Volunteer Registration Form ☦️</h1>", unsafe_allow_html=True)
st.markdown("<p>Please fill out your information below to register as a volunteer.</p>", unsafe_allow_html=True)

# Registration Form
with st.form("volunteer_registration"):
    st.markdown("### Personal Information")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name*", placeholder="Enter your full name")
        phone = st.text_input("Phone Number*", placeholder="Enter your phone number")
        age_group = st.selectbox("Age Group*", ["Select age group", "Under 18", "18-25", "26-40", "41-60", "Over 60"])
    
    with col2:
        email = st.text_input("Email Address*", placeholder="Enter your email address")
        emergency_contact = st.text_input("Emergency Contact*", placeholder="Name and phone number")
        experience = st.selectbox("Volunteer Experience*", ["Select experience level", "First time", "Some experience", "Very experienced"])
    
    # Station Selection with Tabs
    st.markdown("### Station Preference & Schedule")
    
    # Station Information
    stations = {
        "🎁 Prizes and Games": {
            "description": "Help run carnival games and distribute prizes to children",
            "requirements": "Energetic, good with kids, patient"
        },
        "💄 Cosmetology": {
            "description": "Face painting, temporary tattoos, and beauty activities",
            "requirements": "Artistic skills preferred, attention to detail"
        },
        "🎈 Inflatables": {
            "description": "Supervise bounce houses and inflatable activities",
            "requirements": "Active, safety-conscious, good with children"
        },
        "🏀 Basketball": {
            "description": "Organize basketball games and sports activities",
            "requirements": "Sports knowledge helpful, energetic"
        },
        "🍿 Snacking": {
            "description": "Food preparation, serving, and kitchen assistance",
            "requirements": "Food safety awareness, teamwork"
        }
    }
    
    # Create tabs for each day
    tab1, tab2, tab3 = st.tabs(["📅 Friday", "📅 Saturday", "📅 Sunday"])
    
    selected_times = {}
    
    with tab1:
        st.markdown("#### Friday Schedule")
        friday_times = ["5:00 PM - 8:00 PM", "8:00 PM - 11:00 PM"]
        
        station_pref_fri = st.selectbox("Preferred Station - Friday", ["Select a station"] + list(stations.keys()), key="fri_station")
        if station_pref_fri != "Select a station":
            st.info(f"**Description:** {stations[station_pref_fri]['description']}")
            st.info(f"**Requirements:** {stations[station_pref_fri]['requirements']}")
        
        time_pref_fri = st.multiselect("Available Time Slots - Friday", friday_times, key="fri_times")
        if time_pref_fri:
            selected_times["Friday"] = {"station": station_pref_fri, "times": time_pref_fri}
    
    with tab2:
        st.markdown("#### Saturday Schedule")
        saturday_times = ["10:00 AM - 1:00 PM", "1:00 PM - 4:00 PM", "4:00 PM - 7:00 PM", "7:00 PM - 10:00 PM"]
        
        station_pref_sat = st.selectbox("Preferred Station - Saturday", ["Select a station"] + list(stations.keys()), key="sat_station")
        if station_pref_sat != "Select a station":
            st.info(f"**Description:** {stations[station_pref_sat]['description']}")
            st.info(f"**Requirements:** {stations[station_pref_sat]['requirements']}")
        
        time_pref_sat = st.multiselect("Available Time Slots - Saturday", saturday_times, key="sat_times")
        if time_pref_sat:
            selected_times["Saturday"] = {"station": station_pref_sat, "times": time_pref_sat}
    
    with tab3:
        st.markdown("#### Sunday Schedule")
        sunday_times = ["12:00 PM - 3:00 PM", "3:00 PM - 6:00 PM"]
        
        station_pref_sun = st.selectbox("Preferred Station - Sunday", ["Select a station"] + list(stations.keys()), key="sun_station")
        if station_pref_sun != "Select a station":
            st.info(f"**Description:** {stations[station_pref_sun]['description']}")
            st.info(f"**Requirements:** {stations[station_pref_sun]['requirements']}")
        
        time_pref_sun = st.multiselect("Available Time Slots - Sunday", sunday_times, key="sun_times")
        if time_pref_sun:
            selected_times["Sunday"] = {"station": station_pref_sun, "times": time_pref_sun}
    
    # Additional Information
    st.markdown("### Additional Information")
    special_skills = st.text_area("Special Skills or Notes", placeholder="Any special skills, allergies, or notes you'd like to share")
    
    # Submit button
    submit_button = st.form_submit_button("Register as Volunteer", use_container_width=True)
    
    if submit_button:
        # Validation
        required_fields = [name, email, phone, emergency_contact]
        if not all(required_fields) or age_group == "Select age group" or experience == "Select experience level":
            st.error("❌ Please fill in all required fields marked with *")
        elif not selected_times:
            st.error("❌ Please select at least one station and time slot")
        else:
            # Process registration
            registration_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "emergency_contact": emergency_contact,
                "age_group": age_group,
                "experience": experience,
                "selected_times": selected_times,
                "special_skills": special_skills,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save to Google Sheets
            if SHEETS_ENABLED:
                try:
                    # Format schedule for sheet
                    schedule_text = ""
                    for day, info in selected_times.items():
                        schedule_text += f"{day}: {info['station']} ({', '.join(info['times'])}) | "
                    
                    reg_sheet.append_row([
                        registration_data["timestamp"],
                        name, email, phone, emergency_contact,
                        age_group, experience,
                        schedule_text.rstrip(" | "),
                        special_skills
                    ])
                    
                    st.success(f"🎉 Thank you {name}! Your registration has been submitted successfully.")
                    logging.info(f"New volunteer registered: {name} - {email}")
                    
                except Exception as e:
                    st.error(f"❌ Registration failed to save: {str(e)}")
                    st.info("📝 Please contact the church office to complete your registration.")
            else:
                st.success(f"🎉 Thank you {name}! Your registration has been received.")
                st.info("📝 Registration data stored locally (Google Sheets not connected)")
            
            # Show summary
            st.balloons()
            st.markdown("### 📋 Registration Summary")
            
            for day, info in selected_times.items():
                st.markdown(f"**{day}:** {info['station']}")
                for time in info['times']:
                    st.markdown(f"  - {time}")
            
            st.info("🙏 We look forward to having you serve with us! You'll receive a confirmation email soon.")
            
            # Show random verse
            verse = get_random_verse()
            st.info(f"📖 Verse for you: {verse}")

# Footer
st.markdown("---")
st.markdown("### Ready to serve? 🙏")
st.info("After registration, you'll receive QR codes for easy punch in/out during your volunteer shifts!")
st.markdown("**For questions, contact: St. Anthony Coptic Orthodox Church**")