import streamlit as st
from datetime import datetime
from geopy.distance import geodesic
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_javascript import st_javascript
import random
# ---------- Page Configuration ----------
st.set_page_config(
    page_title="St. Anthony Volunteer System",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
        font-weight: 600;
    }
    
    /* Mobile heading adjustments */
    @media (max-width: 768px) {
        h1 { font-size: 1.8rem; line-height: 1.2; }
        h2 { font-size: 1.5rem; line-height: 1.3; }
        h3 { font-size: 1.3rem; line-height: 1.3; }
        h4 { font-size: 1.1rem; line-height: 1.4; }
    }
    
    .panel {
        background-color: #1B263B;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #2E4057;
    }
    
    .stTextInput>div>div>input,
    .stSelectbox>div>div>div>select {
        background-color: #1B263B;
        border: 2px solid #1B263B;
        border-radius: 5px;
        transition: border 0.3s;
        font-size: 16px;
        -webkit-appearance: none;
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
        font-weight: 600;
        font-size: 16px;
        border-radius: 8px;
        transition: transform 0.2s, background-color 0.2s;
        padding: 12px 24px;
        min-height: 44px;
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
    }
    div.stButton > button:first-of-type:hover {
        transform: scale(1.02);
        background-color: #218838;
    }

    div.stButton > button:last-of-type {
        background-color: #fd7e14;
    }
    div.stButton > button:last-of-type:hover {
        transform: scale(1.02);
        background-color: #e06c00;
    }
    
    /* Registration submit button styling */
    .stForm .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        font-size: 18px;
        padding: 16px 32px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        width: 100%;
        min-height: 56px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stForm .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stForm .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Universal white text override */
    .stApp * {
        color: #FFFFFF !important;
    }
    
    /* Reduce spacing between elements */
    .stMarkdown {
        margin-bottom: 0.5rem !important;
        margin-top: 0.5rem !important;
    }
    
    [data-testid="stMarkdownContainer"] {
        margin-bottom: 0.5rem !important;
        margin-top: 0.5rem !important;
        padding-bottom: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Reduce spacing in tabs and containers */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem !important;
    }
    
    /* Tighten form spacing */
    .stForm {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Reduce column spacing */
    .row-widget.stHorizontal {
        gap: 0.5rem !important;
    }
    
    /* Compact text inputs and selectors */
    .stTextInput, .stSelectbox, .stRadio {
        margin-bottom: 0.5rem !important;
    }
    
    /* Reduce header spacing */
    h1, h2, h3, h4, h5, h6 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    

    
    /* Mobile-specific font color fixes */
    @media (max-width: 768px) {
        .stApp, .stApp * {            color: #FFFFFF !important;
        }
        
        /* Force white text on mobile form elements */
        .stTextInput input,
        .stSelectbox select,
        .stRadio div,
        .stCheckbox div,
        .stTextArea textarea {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        
        /* Mobile Safari specific fixes */
        input, select, textarea {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        
        /* Mobile alert and info messages */
        .stAlert div,
        .stInfo div,
        .stSuccess div,
        .stWarning div,
        .stError div {
            color: #FFFFFF !important;
        }
        
        /* Mobile markdown and text elements */
        .stMarkdown,
        .stMarkdown *,
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] * {
            color: #FFFFFF !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Configuration ----------
# St. Anthony Coptic Orthodox Church, 267 Hartford Rd, Medford, NJ 08055
CHURCH_LOCATION = (39.8637, -74.8284)
MAX_DISTANCE_METERS = 100  # 100m for production - volunteers must be at church
SHEET_NAME = "Volunteer Hours"
PUNCH_SHEET = "Sheet1"
REGISTRATION_SHEET = "Registration"

# ---------- Connect to Google Sheets ----------
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
    st.markdown("<h1>🌟 Volunteer Registration Form 🌟</h1>", unsafe_allow_html=True)
    st.markdown("<p>Please fill out your information below.</p>", unsafe_allow_html=True)
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
    st.markdown("<h1>⏱ Punch In/Out</h1>", unsafe_allow_html=True)
    st.markdown("<p>Enter your name, select your service, and make sure your location is enabled.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    name = col1.text_input("Full Name*", key="punch_name")
    service = col2.selectbox("Select Service", ["Food Stand", "Parking", "Setup/Cleanup", "Other"], key="punch_service")
    st.markdown('</div>', unsafe_allow_html=True)

    # Location verification
    coords = st_javascript("""
        new Promise((resolve) => {
            if (!navigator.geolocation) {
                resolve({error: "Geolocation not supported"});
                return;
            }
            navigator.geolocation.getCurrentPosition(
                (position) => resolve({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                }),
                (error) => resolve({error: error.message}),
                {timeout: 10000, enableHighAccuracy: true}
            );
        });
    """)
    
    if not coords:
        st.warning("📍 Requesting location access... Please allow location services in your browser.")
        st.info("💡 If you don't see a location popup, check your browser settings or the location icon in the address bar.")
        st.info("🔄 The page will automatically update once location is granted.")
        st.stop()

    if 'error' in coords:
        st.error(f"❌ Location error: {coords['error']}")
        st.info("💡 Please enable location services and refresh the page.")
        st.stop()

    lat = coords.get('latitude', 0)
    lon = coords.get('longitude', 0)
    
    if lat == 0 and lon == 0:
        st.warning("⚠️ Waiting for location coordinates...")
        st.info("🔄 Please wait while we get your location...")
        st.stop()
    
    distance = geodesic(CHURCH_LOCATION, (lat, lon)).meters

    if name:
        if distance > MAX_DISTANCE_METERS:
            st.error("❌ You must be at St. Anthony Coptic Orthodox Church to punch in/out.")
            st.info("� Please ensure you are within the church grounds and try again.")
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
