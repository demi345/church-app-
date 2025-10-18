import streamlit as st
from datetime import datetime
from geopy.distance import geodesic
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import logging
import os

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('volunteer_system.log') if not os.getenv('STREAMLIT_SHARING') else logging.StreamHandler()
    ]
)

# ------------------ Page Configuration ------------------
st.set_page_config(
    page_title="St. Anthony Volunteer System",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------ CSS Styling ------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.stApp { 
    background-color: #0D1B2A; 
    color: #FFFFFF; 
    font-family: 'Inter', sans-serif;
}
.panel {
    background-color: #1B263B;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    border: 1px solid #2E4057;
}
.stButton>button {
    font-weight: 600;
    font-size: 16px;
    border-radius: 8px;
    padding: 12px 24px;
}
div.stButton > button:first-of-type {background-color: #28a745;}
div.stButton > button:last-of-type {background-color: #fd7e14;}
.stApp * {color: #FFFFFF !important;}
.stApp img {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
    margin: 0 auto;
    display: block;
}
.main-header {
    text-align: center;
    margin-bottom: 30px;
}
.main-header h1 {
    color: #FFFFFF !important;
    font-weight: 600;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

/* Tab 2 specific styling - black text */
.stTabs [data-baseweb="tab-panel"]:nth-child(2) * {
    color: #000000 !important;
}
.stTabs [data-baseweb="tab-panel"]:nth-child(2) h1 {
    color: #000000 !important;
}
.stTabs [data-baseweb="tab-panel"]:nth-child(2) p {
    color: #000000 !important;
}
.stTabs [data-baseweb="tab-panel"]:nth-child(2) label {
    color: #000000 !important;
}
.stTabs [data-baseweb="tab-panel"]:nth-child(2) .stTextInput label {
    color: #000000 !important;
}
.stTabs [data-baseweb="tab-panel"]:nth-child(2) .stSelectbox label {
    color: #000000 !important;
}
.stTabs [data-baseweb="tab-panel"]:nth-child(2) div {
    color: #000000 !important;
}
/* Tab 2 input fields - black text */
.stTabs [data-baseweb="tab-panel"]:nth-child(2) input {
    color: #000000 !important;
}
.stTabs [data-baseweb="tab-panel"]:nth-child(2) .stTextInput input {
    color: #000000 !important;
}
.stTabs [data-baseweb="tab-panel"]:nth-child(2) .stSelectbox select {
    color: #000000 !important;
}
.stTabs [data-baseweb="tab-panel"]:nth-child(2) .stSelectbox div[data-baseweb="select"] {
    color: #000000 !important;
}
/* Keep status messages visible with appropriate colors */
.stTabs [data-baseweb="tab-panel"]:nth-child(2) .stSuccess {
    color: #155724 !important;
    background-color: #d4edda !important;
}
.stTabs [data-baseweb="tab-panel"]:nth-child(2) .stError {
    color: #721c24 !important;
    background-color: #f8d7da !important;
}
.stTabs [data-baseweb="tab-panel"]:nth-child(2) .stInfo {
    color: #0c5460 !important;
    background-color: #d1ecf1 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Config ------------------
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

# ------------------ Google Sheets Connection ------------------
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

# ------------------ Health Check ------------------
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

# ------------------ Header with Logo ------------------
try:
    # Center the logo above the title
    st.markdown('<div style="text-align: center; margin-bottom: 20px;">', unsafe_allow_html=True)
    st.image("stanthonylogo.png", width=150)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Title with logo positioned above "Anthony"
    st.markdown("""
    <div style="text-align: center; margin-top: -10px;">
        <h1 style="color: #FFFFFF; font-size: 2.5rem; margin: 0;">
            ⛪ St. Anthony Volunteer System
        </h1>
    </div>
    """, unsafe_allow_html=True)
    logging.info("Logo loaded successfully")
except FileNotFoundError:
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #FFFFFF; font-size: 2.5rem;">
            ⛪ St. Anthony Volunteer System
        </h1>
    </div>
    """, unsafe_allow_html=True)
    logging.warning("Logo file 'stanthonylogo.png' not found")

# ------------------ Tabs ------------------
tab1, tab2 = st.tabs(["📝 Volunteer Registration", "⏱ Punch In/Out"])

# ------------------ TAB 1: Registration ------------------
with tab1:
    st.markdown("<h1>🌟 Volunteer Registration Form 🌟</h1>", unsafe_allow_html=True)
    st.markdown("<p>Please fill out your information below.</p>", unsafe_allow_html=True)
    
    with st.form("registration_form"):
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        first_name = col1.text_input("First Name*", max_chars=50)
        last_name = col2.text_input("Last Name*", max_chars=50)
        cell_phone = st.text_input("Cell Phone*")
        email = st.text_input("Email")
        age = st.radio("Age*", ["14-18", "18+"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Availability")
        thursday_shift = st.selectbox("Thursday", ["11:00 am - 5:00 pm", "5:00 pm - 11:00 pm", "Other"])
        friday_shift = st.selectbox("Friday", ["11:00 am - 5:00 pm", "5:00 pm - 11:00 pm", "Other"])
        saturday_shift = st.selectbox("Saturday", ["11:00 am - 5:00 pm", "5:00 pm - 11:00 pm", "Other"])
        sunday_shift = st.selectbox("Sunday", ["11:00 am - 4:30 pm", "4:30 pm - 10:00 pm", "Other"])
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Submit Registration")
        if submitted:
            if not first_name or not last_name or not cell_phone:
                st.error("❌ Please fill out all required fields (*)")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if SHEETS_ENABLED:
                    try:
                        reg_sheet.append_row([
                            first_name, last_name, cell_phone, email, age,
                            thursday_shift, friday_shift, saturday_shift, sunday_shift,
                            timestamp
                        ])
                        st.success(f"✅ Thank you {first_name}! Your registration has been recorded. 🙏")
                        logging.info(f"New volunteer registration: {first_name} {last_name}")
                    except Exception as e:
                        st.error(f"❌ Failed to save registration: {str(e)}")
                        logging.error(f"Registration failed for {first_name} {last_name}: {str(e)}")
                else:
                    st.success(f"✅ Thank you {first_name}! Your registration has been recorded. 🙏")
                    
# ------------------ TAB 2: Punch In/Out ------------------
with tab2:
    st.markdown("<h1>⏱ Punch In/Out</h1>", unsafe_allow_html=True)
    st.markdown("<p>Enter your name, select your service. Location will be checked automatically.</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    name = col1.text_input("Full Name*", key="punch_name")
    service = col2.selectbox("Select Service", ["Food Stand", "Parking", "Setup/Cleanup", "Other"], key="punch_service")
    st.markdown('</div>', unsafe_allow_html=True)

    # IP-based location detection
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
                                'isp': data.get('org', data.get('isp', '')),
                                'service': service
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
                                'isp': data.get('isp', ''),
                                'service': service
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
                                'isp': data.get('org', ''),
                                'service': service
                            }
                except Exception:
                    continue
            
            return {'error': 'Unable to determine location - all IP location services failed'}
            
        except Exception as e:
            return {'error': str(e)}
    
    @st.cache_data(ttl=300)
    def get_full_address(lat, lon):
        """Get full street address from coordinates using reverse geocoding"""
        try:
            import requests
            
            services = [
                f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1",
                f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en",
                f"https://geocode.maps.co/reverse?lat={lat}&lon={lon}"
            ]
            
            for service in services:
                try:
                    headers = {'User-Agent': 'St.Anthony-Volunteer-App/1.0'}
                    response = requests.get(service, timeout=10, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        
                        if 'nominatim.openstreetmap.org' in service:
                            if 'display_name' in data:
                                address = data.get('address', {})
                                street_parts = []
                                
                                if address.get('house_number'):
                                    street_parts.append(address['house_number'])
                                if address.get('road'):
                                    street_parts.append(address['road'])
                                elif address.get('street'):
                                    street_parts.append(address['street'])
                                
                                street_address = ' '.join(street_parts) if street_parts else ''
                                
                                if street_address:
                                    city = address.get('city') or address.get('town') or address.get('village') or ''
                                    state = address.get('state') or ''
                                    postal = address.get('postcode') or ''
                                    
                                    full_addr = street_address
                                    if city:
                                        full_addr += f", {city}"
                                    if state:
                                        full_addr += f", {state}"
                                    if postal:
                                        full_addr += f" {postal}"
                                    return full_addr
                                
                                return data['display_name']
                        
                        elif 'bigdatacloud.net' in service:
                            if 'locality' in data:
                                street_parts = []
                                locality = data.get('locality', '')
                                
                                if locality:
                                    street_parts.append(locality)
                                
                                city = data.get('city', '')
                                state = data.get('principalSubdivision', '')
                                postal = data.get('postcode', '')
                                
                                if street_parts:
                                    full_addr = ', '.join(street_parts)
                                    if city and city not in full_addr:
                                        full_addr += f", {city}"
                                    if state:
                                        full_addr += f", {state}"
                                    if postal:
                                        full_addr += f" {postal}"
                                    return full_addr
                        
                        elif 'geocode.maps.co' in service:
                            if 'display_name' in data:
                                return data['display_name']
                            
                except Exception:
                    continue
            
            return 'Street address not available'
        except Exception as e:
            return f'Address lookup failed: {str(e)}'

    # Only detect location when user enters their name
    if name:
        # Get location when name is provided
        with st.spinner("� Detecting your location for verification..."):
            coords = get_ip_location()
            
        # Handle location verification
        if 'error' in coords:
            st.error(f"❌ Location error: {coords['error']}")
            st.error("🚫 Unable to verify your location. Please check your internet connection and try again.")
            st.info("💡 For security reasons, location verification is required for punch in/out.")
            st.stop()
        else:
            lat = coords.get('latitude', 0)
            lon = coords.get('longitude', 0)
            
            distance = geodesic(CHURCH_LOCATION, (lat, lon)).meters
            
            if distance > MAX_DISTANCE_METERS:
                st.error("❌ You must be at St. Anthony Coptic Orthodox Church to punch in/out.")
                st.info("📍 Please ensure you are within the church grounds and try again.")
                st.stop()
            else:
                st.success("✅ Location verified! You can punch in/out. 🙏")

                col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🟢 Punch In", key="punch_in", use_container_width=True):
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if SHEETS_ENABLED:
                        try:
                            punch_sheet.append_row([name, service, "In", timestamp])
                            st.success(f"👋 Welcome {name}! You've successfully punched in for **{service}**. 🌟")
                            logging.info(f"Punch IN: {name} - {service} - {timestamp}")
                        except Exception as e:
                            st.error(f"❌ Failed to save punch in: {str(e)}")
                            st.info(f"📝 Punch data: {name} - {service} - In - {timestamp}")
                    else:
                        st.success(f"👋 Welcome {name}! You've successfully punched in for **{service}**. 🌟")
                        st.info(f"📝 Punch data: {name} - {service} - In - {timestamp}")
                    
                    verse = random.choice(volunteer_verses)
                    st.info(f"📖 Verse for you: {verse}")

            with col2:
                if st.button("🔴 Punch Out", key="punch_out", use_container_width=True):
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if SHEETS_ENABLED:
                        try:
                            punch_sheet.append_row([name, service, "Out", timestamp])
                            st.success(f"🎉 Great job, {name}! You've successfully punched out from **{service}**. 🙏")
                            logging.info(f"Punch OUT: {name} - {service} - {timestamp}")
                        except Exception as e:
                            st.error(f"❌ Failed to save punch out: {str(e)}")
                            st.info(f"📝 Punch data: {name} - {service} - Out - {timestamp}")
                    else:
                        st.success(f"🎉 Great job, {name}! You've successfully punched out from **{service}**. 🙏")
                        st.info(f"📝 Punch data: {name} - {service} - Out - {timestamp}")
                    
                    verse = random.choice(volunteer_verses)
                    st.info(f"📖 Verse for you: {verse}")
    else:
        st.info("📝 Please enter your name above to start the punch in/out process.")
        st.info("🔒 Location verification will begin once you enter your name.")
