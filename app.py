import streamlit as st
from datetime import datetime
from geopy.distance import geodesic
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_javascript import st_javascript
import random

# ---------- CSS: Dark blue theme, panels, hover effects ----------
st.markdown(
    """
    <style>
    /* Import consistent fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Mobile-first responsive font sizing and styling */
    .stApp { 
        background-color: #0D1B2A; 
        color: #FFFFFF; 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeLegibility;
    }
    
    /* Mobile font optimization */
    @media (max-width: 768px) {
        .stApp {
            font-size: 16px; /* Prevent iOS zoom on focus */
            line-height: 1.5;
        }
    }
    
    h1, h2, h3, h4, h5, h6 { 
        color: #F0F0F0; 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 600;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
    }
    
    /* Mobile heading adjustments */
    @media (max-width: 768px) {
        h1 { font-size: 1.8rem; line-height: 1.2; }
        h2 { font-size: 1.5rem; line-height: 1.3; }
        h3 { font-size: 1.3rem; line-height: 1.3; }
        h4 { font-size: 1.1rem; line-height: 1.4; }
    }
    
    p, div, span, label {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 400;
        -webkit-font-smoothing: antialiased;
    }

    .panel {
        background-color: #1B263B;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #2E4057;
        font-family: 'Inter', sans-serif;
    }

    .stTextInput>div>div>input,
    .stSelectbox>div>div>div>select {
        background-color: #1B263B;
        color: #FFFFFF;
        border: 2px solid #1B263B;
        border-radius: 5px;
        transition: border 0.3s;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
        font-size: 16px; /* Minimum 16px to prevent iOS zoom */
        font-weight: 400;
        -webkit-font-smoothing: antialiased;
        -webkit-appearance: none; /* Remove iOS styling */
    }
    
    /* Mobile input optimizations */
    @media (max-width: 768px) {
        .stTextInput>div>div>input,
        .stSelectbox>div>div>div>select {
            padding: 12px 16px;
            font-size: 16px;
            line-height: 1.4;
        }
    }
    .stTextInput>div>div>input:hover,
    .stSelectbox>div>div>div>select:hover {
        border: 2px solid #28a745;
    }

    .stButton>button {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 600;
        font-size: 16px;
        border-radius: 8px;
        transition: transform 0.2s, background-color 0.2s;
        -webkit-font-smoothing: antialiased;
        padding: 12px 24px;
        min-height: 44px; /* iOS touch target minimum */
    }
    
    /* Mobile button optimizations */
    @media (max-width: 768px) {
        .stButton>button {
            width: 100%;
            padding: 16px 24px;
            font-size: 17px;
            min-height: 48px;
        }
    }

    div.stButton > button:first-of-type {
        background-color: #28a745;
        color: white;
        font-weight: 600;
    }
    div.stButton > button:first-of-type:hover {
        transform: scale(1.02);
        background-color: #218838;
    }

    div.stButton > button:last-of-type {
        background-color: #fd7e14;
        color: white;
        font-weight: 600;
    }
    div.stButton > button:last-of-type:hover {
        transform: scale(1.02);
        background-color: #e06c00;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Configuration ----------
CHURCH_LOCATION = (39.8991, -74.9366)
MAX_DISTANCE_METERS = 10000  # 10km for testing - change to 100 for production
SHEET_NAME = "Volunteer Hours"
PUNCH_SHEET = "Sheet1"
REGISTRATION_SHEET = "Registration"

# ---------- Connect to Google Sheets ----------
# Note: No actual credentials are stored in this file
# Production uses environment secrets, development uses local config file
try:
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Check for deployment environment first
    try:
        if hasattr(st, 'secrets') and "gcp_service_account" in st.secrets:
            import json
            account_info = json.loads(st.secrets["gcp_service_account"])
            auth_creds = ServiceAccountCredentials.from_json_keyfile_dict(account_info, scope)
            st.info("🔐 Using secure environment configuration")
        else:
            raise KeyError("Using local configuration")
    except:
        # Use local configuration file for development
        auth_creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        st.info("📁 Using local development configuration")
    
    client = gspread.authorize(auth_creds)
    punch_sheet = client.open(SHEET_NAME).worksheet(PUNCH_SHEET)
    reg_sheet = client.open(SHEET_NAME).worksheet(REGISTRATION_SHEET)
    SHEETS_ENABLED = True
    st.success("✅ Google Sheets connected successfully!")
except FileNotFoundError:
    st.warning("⚠️ Google Sheets integration disabled: service_account.json not found. Running in demo mode.")
    SHEETS_ENABLED = False
    punch_sheet = None
    reg_sheet = None
except Exception as e:
    st.error(f"❌ Google Sheets connection error: {str(e)}")
    st.info("💡 Check your service account setup and sheet permissions.")
    SHEETS_ENABLED = False
    punch_sheet = None
    reg_sheet = None

# ---------- Bible verses ----------
volunteer_verses = [
    "Each of you should use whatever gift you have received to serve others, as faithful stewards of God's grace. — 1 Peter 4:10",
    "Whatever you do, work at it with all your heart, as working for the Lord, not for human masters. — Colossians 3:23",
    "Serve wholeheartedly, as if you were serving the Lord, not people. — Ephesians 6:7",
    "The greatest among you will be your servant. — Matthew 23:11",
    "Carry each other's burdens, and in this way you will fulfill the law of Christ. — Galatians 6:2"
]

# ---------- Tabs ----------
tab1, tab2 = st.tabs(["📝 Volunteer Registration", "⏱ Punch In/Out"])

# ---------- TAB 1: Registration ----------
with tab1:
    st.markdown("<h1 style='color:#F0F0F0'>🌟 Volunteer Registration Form 🌟</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#B0C4DE'>Please fill out your information below.</p>", unsafe_allow_html=True)

    with st.form("registration_form"):
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        first_name = col1.text_input("First Name*", max_chars=50)
        last_name = col2.text_input("Last Name*", max_chars=50)
        cell_phone = st.text_input("Cell Phone* (You may receive text messages)")
        email = st.text_input("Email")
        age = st.radio("Age*", ["14-18", "18+"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Availability")
        thursday_shift = st.selectbox("Thursday, October 9, 2025", ["11:00 am - 5:00 pm", "5:00 pm - 11:00 pm", "Other"])
        friday_shift = st.selectbox("Friday, October 10, 2025", ["11:00 am - 5:00 pm", "5:00 pm - 11:00 pm", "Other"])
        saturday_shift = st.selectbox("Saturday, October 11, 2025", ["11:00 am - 5:00 pm", "5:00 pm - 11:00 pm", "Other"])
        sunday_shift = st.selectbox("Sunday, October 12, 2025", ["11:00 am - 4:30 pm", "4:30 pm - 10:00 pm", "Other"])
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
                    except Exception as e:
                        st.error(f"❌ Failed to save registration: {str(e)}")
                        st.info(f"📝 Registration data: {first_name} {last_name}, {cell_phone}")
                else:
                    st.success(f"✅ Thank you {first_name}! Your registration would be recorded (Demo mode). 🙏")
                    st.info("📝 Registration data: " + str({
                        "Name": f"{first_name} {last_name}",
                        "Phone": cell_phone,
                        "Email": email,
                        "Age": age,
                        "Thursday": thursday_shift,
                        "Friday": friday_shift,
                        "Saturday": saturday_shift,
                        "Sunday": sunday_shift
                    }))
                st.info("We look forward to seeing you at the festival! 🌟")

# ---------- TAB 2: Punch In/Out ----------
with tab2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("<h1 style='color:#F0F0F0'>⏱ Punch In/Out</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#B0C4DE'>Enter your name, select your service, and make sure your location is enabled.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    name = col1.text_input("Full Name*", key="punch_name")
    service = col2.selectbox("Select Service", ["Food Stand", "Parking", "Setup/Cleanup", "Other"], key="punch_service")
    st.markdown('</div>', unsafe_allow_html=True)

    # Location verification with debugging
    st.markdown("#### 🔍 Location Debug Info:")
    coords = st_javascript("navigator.geolocation.getCurrentPosition(pos => pos.coords);")
    
    if not coords:
        st.warning("📍 Requesting location access... Please allow location services in your browser.")
        st.info("💡 If you don't see a location popup, check your browser settings or the location icon in the address bar.")
        st.stop()

    lat = coords.get('latitude', 0)
    lon = coords.get('longitude', 0)
    
    if lat == 0 and lon == 0:
        st.warning("⚠️ Waiting for location coordinates...")
        st.stop()
    
    st.info(f"📍 Your location: {lat:.4f}, {lon:.4f}")
    st.info(f"🏢 Church location: {CHURCH_LOCATION[0]}, {CHURCH_LOCATION[1]}")
    
    distance = geodesic(CHURCH_LOCATION, (lat, lon)).meters
    st.info(f"📏 Distance to church: {distance:.1f} meters ({distance/1000:.2f} km)")

    if name:
        if distance > MAX_DISTANCE_METERS:
            st.error(f"❌ You are {distance:.1f}m from the church (max allowed: {MAX_DISTANCE_METERS}m)")
            st.info("🔧 For testing, distance limit is set to 10km. Change MAX_DISTANCE_METERS to 100 for production.")
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
                        except Exception as e:
                            st.error(f"❌ Failed to save punch in: {str(e)}")
                            st.info(f"📝 Punch data: {name} - {service} - In - {timestamp}")
                    else:
                        st.success(f"👋 Welcome {name}! You would be punched in for **{service}** (Demo mode). 🌟")
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
                        except Exception as e:
                            st.error(f"❌ Failed to save punch out: {str(e)}")
                            st.info(f"📝 Punch data: {name} - {service} - Out - {timestamp}")
                    else:
                        st.success(f"🎉 Great job, {name}! You would be punched out from **{service}** (Demo mode). 🙏")
                        st.info(f"📝 Punch data: {name} - {service} - Out - {timestamp}")
                    
                    verse = random.choice(volunteer_verses)
                    st.info(f"📖 Verse for you: {verse}")
    else:
        st.info("📝 Please enter your name to enable punch buttons.")

# ---------- Setup Instructions ----------
with st.expander("🔧 Google Sheets Setup Instructions"):
    st.markdown(f"""
    **Current Status:**
    - Google Sheets: {"✅ Connected" if SHEETS_ENABLED else "❌ Not connected (Demo mode)"}
    - Distance Limit: {MAX_DISTANCE_METERS}m {"(Testing)" if MAX_DISTANCE_METERS > 1000 else "(Production)"}
    
    **To enable Google Sheets integration:**
    
    1. **Create Google Cloud Project**: https://console.cloud.google.com/
    2. **Enable APIs**: Google Sheets API & Google Drive API
    3. **Create Service Account**: IAM & Admin → Service Accounts
    4. **Download JSON key** and save as `service_account.json` in your project folder
    5. **Create Google Sheet** named "Volunteer Hours" with these tabs:
       - **Sheet1** (for punch data): Name | Service | Action | Timestamp
       - **Registration** (for registrations): First Name | Last Name | Cell Phone | Email | Age | Thursday Shift | Friday Shift | Saturday Shift | Sunday Shift | Registration Time
    6. **Share the sheet** with the service account email (found in the JSON file) with Editor permissions
    
    **For Production:**
    - Change `MAX_DISTANCE_METERS = 100` (currently {MAX_DISTANCE_METERS} for testing)
    - Ensure all volunteers are within 100 meters of the church location
    """)
