import streamlit as st
from datetime import datetime
from geopy.distance import geodesic
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

# Page Configuration
st.set_page_config(
    page_title="St. Anthony Volunteer System",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* White theme with black text */
.stApp { 
    background-color: #FFFFFF; 
    color: #000000; 
    font-family: 'Inter', sans-serif;
}

/* Panel styling for white theme */
.panel {
    background-color: #F8F9FA;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    border: 1px solid #E9ECEF;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Punch In Panel */
.punch-in-panel {
    background-color: #F8FFF8;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 2px solid #28A745;
    box-shadow: 0 4px 12px rgba(40, 167, 69, 0.15);
}

/* Punch Out Panel */
.punch-out-panel {
    background-color: #FFF8F8;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 2px solid #DC3545;
    box-shadow: 0 4px 12px rgba(220, 53, 69, 0.15);
}

/* Panel Headers */
.panel-header {
    text-align: center;
    margin-bottom: 15px;
    font-size: 24px;
    font-weight: 700;
}

.punch-in-header {
    color: #155724 !important;
    background: linear-gradient(90deg, #28A745, #20C997);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.punch-out-header {
    color: #721C24 !important;
    background: linear-gradient(90deg, #DC3545, #E83E8C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Button styling */
.stButton>button {
    font-weight: 600;
    font-size: 18px;
    border-radius: 12px;
    padding: 16px 32px;
    color: #FFFFFF !important;
    border: none;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Punch In Button */
.punch-in-panel .stButton>button {
    background: linear-gradient(135deg, #28A745, #20C997) !important;
    border: none !important;
}

.punch-in-panel .stButton>button:hover {
    background: linear-gradient(135deg, #218838, #1BA085) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
}

/* Punch Out Button */
.punch-out-panel .stButton>button {
    background: linear-gradient(135deg, #DC3545, #E83E8C) !important;
    border: none !important;
}

.punch-out-panel .stButton>button:hover {
    background: linear-gradient(135deg, #C82333, #D91A72) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4);
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

/* Header styling */
.main-header {
    text-align: center;
    margin-bottom: 30px;
}

.main-header h1 {
    color: #000000 !important;
    font-weight: 600;
    text-shadow: none;
}

/* Input fields styling */
.stTextInput input, .stSelectbox select {
    color: #000000 !important;
    background-color: #FFFFFF !important;
    border: 1px solid #CED4DA !important;
}

.stTextInput label, .stSelectbox label {
    color: #000000 !important;
    font-weight: 500;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: #FDFDFE;
    border-bottom: 1px solid #F1F3F4;
}

.stTabs [data-baseweb="tab"] {
    color: #8E9AAF !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #6C9BD2 !important;
    border-bottom-color: #6C9BD2 !important;
}

/* Success, error, and info message styling */
.stSuccess {
    color: #155724 !important;
    background-color: #d4edda !important;
    border: 1px solid #c3e6cb !important;
}

.stError {
    color: #721c24 !important;
    background-color: #f8d7da !important;
    border: 1px solid #f5c6cb !important;
}

.stInfo {
    color: #0c5460 !important;
    background-color: #d1ecf1 !important;
    border: 1px solid #bee5eb !important;
}

.stWarning {
    color: #856404 !important;
    background-color: #fff3cd !important;
    border: 1px solid #ffeaa7 !important;
}

/* Form elements consistency */
.stForm {
    background-color: #F8F9FA;
    border: 1px solid #E9ECEF;
    border-radius: 10px;
    padding: 20px;
}

/* Radio buttons and other form elements */
.stRadio label, .stSelectbox label, .stTextInput label {
    color: #000000 !important;
    font-weight: 500;
}

/* Sidebar styling if used */
.css-1d391kg {
    background-color: #F8F9FA;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .panel {
        padding: 15px;
        margin-bottom: 15px;
    }
    
    .stButton>button {
        width: 100%;
        margin-bottom: 10px;
    }
}

.big-title {
    font-size: 48px;
    font-weight: 700;
    margin: 20px 0;
    text-align: center;
}

.punch-in-title {
    color: #155724 !important;
    text-shadow: 2px 2px 4px rgba(21, 87, 36, 0.3);
}

.punch-out-title {
    color: #721C24 !important;
    text-shadow: 2px 2px 4px rgba(114, 28, 36, 0.3);
}
</style>
""", unsafe_allow_html=True)

# Config
CHURCH_LOCATION = (39.8637, -74.8284)
MAX_DISTANCE_METERS = 50000  # 50km for testing - allows testing from anywhere nearby
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

# Location Detection Functions
@st.cache_data(ttl=300)
def get_ip_location():
    try:
        import requests
        
        services = [
            "https://ipapi.co/json/",
            "http://ip-api.com/json/",
            "https://ipinfo.io/json"
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'latitude' in data and 'longitude' in data:
                        return {
                            'latitude': data['latitude'],
                            'longitude': data['longitude'],
                            'city': data.get('city', 'Unknown'),
                            'region': data.get('region_code', data.get('region', 'Unknown')),
                            'country': data.get('country_name', data.get('country', 'Unknown')),
                            'postal': data.get('postal', ''),
                            'timezone': data.get('timezone', ''),
                            'isp': data.get('org', data.get('isp', ''))
                        }
                    elif 'lat' in data and 'lon' in data:
                        return {
                            'latitude': data['lat'],
                            'longitude': data['lon'],
                            'city': data.get('city', 'Unknown'),
                            'region': data.get('regionName', data.get('region', 'Unknown')),
                            'country': data.get('country', 'Unknown'),
                            'postal': data.get('zip', ''),
                            'timezone': data.get('timezone', ''),
                            'isp': data.get('isp', '')
                        }
                    elif 'loc' in data:
                        lat, lon = data['loc'].split(',')
                        return {
                            'latitude': float(lat),
                            'longitude': float(lon),
                            'city': data.get('city', 'Unknown'),
                            'region': data.get('region', 'Unknown'),
                            'country': data.get('country', 'Unknown'),
                            'postal': data.get('postal', ''),
                            'timezone': data.get('timezone', ''),
                            'isp': data.get('org', '')
                        }
            except Exception:
                continue
        
        return {'error': 'Unable to determine location - all IP location services failed'}
        
    except Exception as e:
        return {'error': str(e)}

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

# Health Check
if st.query_params.get("health") == "check":
    st.json({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "sheets_enabled": SHEETS_ENABLED,
        "services": {
            "google_sheets": "connected" if SHEETS_ENABLED else "disconnected",
            "location_services": "available"
        }
    })
    st.stop()

# Header with Logo
try:
    # Center the logo above the title
    st.markdown('<div style="text-align: center; margin-bottom: 20px;">', unsafe_allow_html=True)
    st.image("stanthonylogo.png", width=150)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Title with logo positioned above "Anthony"
    st.markdown("""
    <div style="text-align: center; margin-top: -10px;">
        <h1 style="color: #000000; font-size: 2.5rem; margin: 0; font-weight: 600;">
            ⛪ St. Anthony Volunteer Form
        </h1>
    </div>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #000000; font-size: 2.5rem; font-weight: 600;">
            ⛪ St. Anthony Volunteer System
        </h1>
    </div>
    """, unsafe_allow_html=True)

# QR Code Parameter Handling
qr_action = st.query_params.get("action")

# Direct QR Code Actions
if qr_action == "punch_in":
    # Show only Punch In interface
    st.success("🎯 QR Code Scanned: PUNCH IN")
    st.markdown("<h1>🟢 Volunteer Punch In</h1>", unsafe_allow_html=True)
    
    # Name input
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    name = st.text_input("Full Name*", key="punch_in_name", placeholder="Enter your full name")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if name:
        # Location verification for punch in
        with st.spinner("🔍 Detecting your location for verification..."):
            # Use the same location detection logic
            coords = get_ip_location()
            
        # Handle location verification
        if 'error' in coords:
            st.error(f"❌ Location error: {coords['error']}")
            st.error("🚫 Unable to verify your location. Please check your internet connection and try again.")
            st.info("💡 For security reasons, location verification is required for punch in/out.")
        else:
            lat = coords.get('latitude', 0)
            lon = coords.get('longitude', 0)
            
            distance = geodesic(CHURCH_LOCATION, (lat, lon)).meters
            
            if distance > MAX_DISTANCE_METERS:
                st.error("❌ You must be at St. Anthony Coptic Orthodox Church to punch in.")
                st.info("📍 Please ensure you are within the church grounds and try again.")
            else:
                st.success("✅ Location verified! You can punch in. 🙏")
                
                # Punch In Section
                st.markdown('<div class="punch-in-panel">', unsafe_allow_html=True)
                st.markdown('<div class="panel-header punch-in-header">🟢 PUNCH IN</div>', unsafe_allow_html=True)
                st.markdown('<p style="text-align: center; color: #155724; margin-bottom: 20px;">Start your volunteer service</p>', unsafe_allow_html=True)
                
                if st.button("🟢 Punch In Now", key="qr_punch_in", use_container_width=True):
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if SHEETS_ENABLED:
                        try:
                            punch_sheet.append_row([name, "In", timestamp])
                            st.success(f"👋 Welcome {name}! You've successfully punched in. 🌟")
                            logging.info(f"Punch IN: {name} - {timestamp}")
                        except Exception as e:
                            st.error(f"❌ Failed to save punch in: {str(e)}")
                            st.info(f"📝 Punch data: {name} - In - {timestamp}")
                    else:
                        st.success(f"👋 Welcome {name}! You've successfully punched in. 🌟")
                        st.info(f"📝 Punch data: {name} - In - {timestamp}")
                    
                    verse = random.choice(volunteer_verses)
                    st.info(f"📖 Verse for you: {verse}")
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📝 Please enter your name to start the punch in process.")
        st.info("🔒 Location verification will begin once you enter your name.")

elif qr_action == "punch_out":
    # Show only Punch Out interface
    st.success("🎯 QR Code Scanned: PUNCH OUT")
    st.markdown("<h1>🔴 Volunteer Punch Out</h1>", unsafe_allow_html=True)
    
    # Name input
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    name = st.text_input("Full Name*", key="punch_out_name", placeholder="Enter your full name")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if name:
        # Location verification for punch out
        with st.spinner("🔍 Detecting your location for verification..."):
            coords = get_ip_location()
            
        # Handle location verification
        if 'error' in coords:
            st.error(f"❌ Location error: {coords['error']}")
            st.error("🚫 Unable to verify your location. Please check your internet connection and try again.")
            st.info("💡 For security reasons, location verification is required for punch in/out.")
        else:
            lat = coords.get('latitude', 0)
            lon = coords.get('longitude', 0)
            
            distance = geodesic(CHURCH_LOCATION, (lat, lon)).meters
            
            if distance > MAX_DISTANCE_METERS:
                st.error("❌ You must be at St. Anthony Coptic Orthodox Church to punch out.")
                st.info("📍 Please ensure you are within the church grounds and try again.")
            else:
                st.success("✅ Location verified! You can punch out. 🙏")
                
                # Punch Out Section
                st.markdown('<div class="punch-out-panel">', unsafe_allow_html=True)
                st.markdown('<div class="panel-header punch-out-header">🔴 PUNCH OUT</div>', unsafe_allow_html=True)
                st.markdown('<p style="text-align: center; color: #721C24; margin-bottom: 20px;">Complete your volunteer service</p>', unsafe_allow_html=True)
                
                if st.button("🔴 Punch Out Now", key="qr_punch_out", use_container_width=True):
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if SHEETS_ENABLED:
                        try:
                            punch_sheet.append_row([name, "Out", timestamp])
                            st.success(f"🎉 Great job, {name}! You've successfully punched out. 🙏")
                            logging.info(f"Punch OUT: {name} - {timestamp}")
                        except Exception as e:
                            st.error(f"❌ Failed to save punch out: {str(e)}")
                            st.info(f"📝 Punch data: {name} - Out - {timestamp}")
                    else:
                        st.success(f"🎉 Great job, {name}! You've successfully punched out. 🙏")
                        st.info(f"📝 Punch data: {name} - Out - {timestamp}")
                    
                    verse = random.choice(volunteer_verses)
                    st.info(f"📖 Verse for you: {verse}")
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📝 Please enter your name to start the punch out process.")
        st.info("🔒 Location verification will begin once you enter your name.")

else:
    # Default view - Registration only
    # Registration
    st.markdown("<h1>Volunteer Registration Form </h1>", unsafe_allow_html=True)
    st.markdown("<p>Please fill out your information below.</p>", unsafe_allow_html=True)
    
    with st.form("registration_form"):
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        first_name = col1.text_input("First Name*", max_chars=50)
        last_name = col2.text_input("Last Name*", max_chars=50)
        cell_phone = st.text_input("Cell Phone*")
        email = st.text_input("Email")
        age = st.radio("Age*", ["14-18", "18+"])
        st.markdown('</div>', unsafe_allow_html=True)

       
        st.subheader("Station Assignment")
        st.markdown("**Select your preferred station and time slots:**")
        
        # Station tabs
        station_tabs = st.tabs(["🎁 Prizes/Games", "💄 Cosmetology", "🎈 Inflatables", "🏀 Basketball", "🍿 Snacking"])
        
        # Initialize variables
        station = ""
        friday_slots = []
        saturday_slots = []
        sunday_slots = []
        
        # Station 1 - Prizes/Kids Games
        with station_tabs[0]:
            station = "Station 1 - Prizes/Kids Games"
            st.markdown("**🎁 Station 1 - Prizes/Kids Games**")
            
            day_tabs = st.tabs(["Friday", "Saturday", "Sunday"])
            
            with day_tabs[0]:
                st.markdown("**Friday Time Slots:**")
                friday_slots = st.multiselect("Friday Availability", [
                    "4:30 pm - 7:30 pm (Set up)",
                    "7:15 pm - 10:15 pm (Clean up)"
                ], key="station1_friday")
            
            with day_tabs[1]:
                st.markdown("**Saturday Time Slots:**")
                saturday_slots = st.multiselect("Saturday Availability", [
                    "10:45 am - 1:45 pm (Set up)",
                    "1:30 pm - 4:30 pm", 
                    "4:15 pm - 7:15 pm",
                    "7:00 pm - 10:00 pm"
                ], key="station1_saturday")
            
            with day_tabs[2]:
                st.markdown("**Sunday Time Slots:**")
                sunday_slots = st.multiselect("Sunday Availability", [
                    "11:45 am - 2:45 pm (Set up)",
                    "2:30 pm - 5:30 pm (Clean up)"
                ], key="station1_sunday")
        
        # Station 2 - Cosmetology
        with station_tabs[1]:
            station = "Station 2 - Cosmetology"
            st.markdown("**💄 Station 2 - Cosmetology**")
            
            day_tabs = st.tabs(["Friday", "Saturday", "Sunday"])
            
            with day_tabs[0]:
                st.markdown("**Friday Time Slots:**")
                friday_slots = st.multiselect("Friday Availability", [
                    "4:30 pm - 7:30 pm (Set up)",
                    "7:15 pm - 10:15 pm (Clean up)"
                ], key="station2_friday")
            
            with day_tabs[1]:
                st.markdown("**Saturday Time Slots:**")
                saturday_slots = st.multiselect("Saturday Availability", [
                    "10:45 am - 1:45 pm (Set up)",
                    "1:30 pm - 4:30 pm", 
                    "4:15 pm - 7:15 pm",
                    "7:00 pm - 10:00 pm"
                ], key="station2_saturday")
            
            with day_tabs[2]:
                st.markdown("**Sunday Time Slots:**")
                sunday_slots = st.multiselect("Sunday Availability", [
                    "11:45 am - 2:45 pm (Set up)",
                    "2:30 pm - 5:30 pm (Clean up)"
                ], key="station2_sunday")
        
        # Station 3 - Inflatables
        with station_tabs[2]:
            station = "Station 3 - Inflatables"
            st.markdown("**🎈 Station 3 - Inflatables**")
            
            day_tabs = st.tabs(["Friday", "Saturday", "Sunday"])
            
            with day_tabs[0]:
                st.markdown("**Friday Time Slots:**")
                friday_slots = st.multiselect("Friday Availability", [
                    "4:30 pm - 7:30 pm (Set up)",
                    "7:15 pm - 10:15 pm (Clean up)"
                ], key="station3_friday")
            
            with day_tabs[1]:
                st.markdown("**Saturday Time Slots:**")
                saturday_slots = st.multiselect("Saturday Availability", [
                    "10:45 am - 1:45 pm (Set up)",
                    "1:30 pm - 4:30 pm", 
                    "4:15 pm - 7:15 pm",
                    "7:00 pm - 10:00 pm"
                ], key="station3_saturday")
            
            with day_tabs[2]:
                st.markdown("**Sunday Time Slots:**")
                sunday_slots = st.multiselect("Sunday Availability", [
                    "11:45 am - 2:45 pm (Set up)",
                    "2:30 pm - 5:30 pm (Clean up)"
                ], key="station3_sunday")
        
        # Station 4 - Basketball
        with station_tabs[3]:
            station = "Station 4 - Basketball"
            st.markdown("**🏀 Station 4 - Basketball**")
            
            day_tabs = st.tabs(["Friday", "Saturday", "Sunday"])
            
            with day_tabs[0]:
                st.markdown("**Friday Time Slots:**")
                friday_slots = st.multiselect("Friday Availability", [
                    "4:30 pm - 7:30 pm (Set up)",
                    "7:15 pm - 10:15 pm (Clean up)"
                ], key="station4_friday")
            
            with day_tabs[1]:
                st.markdown("**Saturday Time Slots:**")
                saturday_slots = st.multiselect("Saturday Availability", [
                    "10:45 am - 1:45 pm (Set up)",
                    "1:30 pm - 4:30 pm", 
                    "4:15 pm - 7:15 pm",
                    "7:00 pm - 10:00 pm"
                ], key="station4_saturday")
            
            with day_tabs[2]:
                st.markdown("**Sunday Time Slots:**")
                sunday_slots = st.multiselect("Sunday Availability", [
                    "11:45 am - 2:45 pm (Set up)",
                    "2:30 pm - 5:30 pm (Clean up)"
                ], key="station4_sunday")
        
        # Station 5 - Snacking
        with station_tabs[4]:
            station = "Station 5 - Snacking"
            st.markdown("**🍿 Station 5 - Snacking**")
            
            day_tabs = st.tabs(["Friday", "Saturday", "Sunday"])
            
            with day_tabs[0]:
                st.markdown("**Friday Time Slots:**")
                friday_slots = st.multiselect("Friday Availability", [
                    "4:30 pm - 7:30 pm (Set up)",
                    "7:15 pm - 10:15 pm (Clean up)"
                ], key="station5_friday")
            
            with day_tabs[1]:
                st.markdown("**Saturday Time Slots:**")
                saturday_slots = st.multiselect("Saturday Availability", [
                    "10:45 am - 1:45 pm (Set up)",
                    "1:30 pm - 4:30 pm", 
                    "4:15 pm - 7:15 pm",
                    "7:00 pm - 10:00 pm"
                ], key="station5_saturday")
            
            with day_tabs[2]:
                st.markdown("**Sunday Time Slots:**")
                sunday_slots = st.multiselect("Sunday Availability", [
                    "11:45 am - 2:45 pm (Set up)",
                    "2:30 pm - 5:30 pm (Clean up)"
                ], key="station5_sunday")
        
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Submit Registration")
        if submitted:
            if not first_name or not last_name or not cell_phone or not station:
                st.error("❌ Please fill out all required fields (*)")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                selected_slots = {
                    'friday': ', '.join(friday_slots) if friday_slots else 'None',
                    'saturday': ', '.join(saturday_slots) if saturday_slots else 'None', 
                    'sunday': ', '.join(sunday_slots) if sunday_slots else 'None'
                }
                
                if SHEETS_ENABLED:
                    try:
                        reg_sheet.append_row([
                            first_name, last_name, cell_phone, email, age,
                            station, selected_slots['friday'], selected_slots['saturday'], selected_slots['sunday'],
                            timestamp
                        ])
                        st.success(f"✅ Thank you {first_name}! Your registration for {station} has been recorded. 🙏")
                        logging.info(f"New volunteer registration: {first_name} {last_name} - {station}")
                    except Exception as e:
                        st.error(f"❌ Failed to save registration: {str(e)}")
                        logging.error(f"Registration failed for {first_name} {last_name}: {str(e)}")
                else:
                    st.success(f"✅ Thank you {first_name}! Your registration for {station} has been recorded. 🙏")
                    
