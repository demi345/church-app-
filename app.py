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
    .stApp { background-color: #0D1B2A; color: #FFFFFF; }
    h1, h2, h3 { color: #F0F0F0; }

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
        color: #FFFFFF;
        border: 2px solid #1B263B;
        border-radius: 5px;
        transition: border 0.3s;
    }
    .stTextInput>div>div>input:hover,
    .stSelectbox>div>div>div>select:hover {
        border: 2px solid #28a745;
    }

    .stButton>button {
        font-weight: bold;
        border-radius: 5px;
        transition: transform 0.2s;
    }

    div.stButton > button:first-of-type {
        background-color: #28a745;
        color: white;
        font-weight: bold;
    }
    div.stButton > button:first-of-type:hover {
        transform: scale(1.05);
        background-color: #218838;
    }

    div.stButton > button:last-of-type {
        background-color: #fd7e14;
        color: white;
        font-weight: bold;
    }
    div.stButton > button:last-of-type:hover {
        transform: scale(1.05);
        background-color: #e06c00;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Configuration ----------
CHURCH_LOCATION = (39.8991, -74.9366)
MAX_DISTANCE_METERS = 100
SHEET_NAME = "Volunteer Hours"
PUNCH_SHEET = "Sheet1"
REGISTRATION_SHEET = "Registration"

# ---------- Connect to Google Sheets ----------
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    punch_sheet = client.open(SHEET_NAME).worksheet(PUNCH_SHEET)
    reg_sheet = client.open(SHEET_NAME).worksheet(REGISTRATION_SHEET)
    SHEETS_ENABLED = True
    st.success("✅ Google Sheets connected successfully!")
except FileNotFoundError:
    st.warning("⚠️ Google Sheets integration disabled: service_account.json not found. Data will be displayed locally only.")
    SHEETS_ENABLED = False
    punch_sheet = None
    reg_sheet = None
except Exception as e:
    error_msg = str(e)
    if "Invalid JWT Signature" in error_msg:
        st.error("❌ Invalid service account credentials. Please regenerate your service_account.json file from Google Cloud Console.")
        st.info("💡 Go to Google Cloud Console → APIs & Services → Credentials → Your Service Account → Keys → Add Key → Create new key")
    elif "API has not been used" in error_msg:
        st.error("❌ Google Sheets API not enabled. Please enable it in Google Cloud Console.")
    elif "Worksheet not found" in error_msg or "Sheet1" in error_msg:
        st.error("❌ Worksheet not found. Please make sure your Google Sheet has worksheets named 'Sheet1' and 'Registration'.")
    else:
        st.error(f"❌ Google Sheets connection failed: {error_msg}")
    st.warning("⚠️ Running in local mode. Data will not be saved to Google Sheets.")
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
                if SHEETS_ENABLED:
                    try:
                        reg_sheet.append_row([
                            first_name, last_name, cell_phone, email, age,
                            thursday_shift, friday_shift, saturday_shift, sunday_shift,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ])
                        st.success(f"✅ Thank you {first_name}! Your registration has been recorded. 🙏")
                    except Exception as e:
                        st.error(f"❌ Failed to save to Google Sheets: {str(e)}")
                        st.info(f"📝 Registration details: {first_name} {last_name}, {cell_phone}")
                else:
                    st.success(f"✅ Thank you {first_name}! Your registration has been recorded locally. 🙏")
                    st.info(f"📝 Registration details: {first_name} {last_name}, {cell_phone}, {email}")
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

    coords = st_javascript("navigator.geolocation.getCurrentPosition(pos => pos.coords);")

    if not coords:
        st.warning("📍 Please enable location services in your browser. Thank you!")
        st.stop()

    lat = coords['latitude']
    lon = coords['longitude']

    if name:
        distance = geodesic(CHURCH_LOCATION, (lat, lon)).meters
        if distance > MAX_DISTANCE_METERS:
            st.error("❌ You are not at the church. Please come closer to register.")
            st.stop()
        else:
            st.success("✅ Location verified! You can punch in/out. 🙏")

            if st.button("Punch In", key="punch_in"):
                if SHEETS_ENABLED:
                    try:
                        punch_sheet.append_row([name, service, "In", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                        verse = random.choice(volunteer_verses)
                        st.success(f"👋 Welcome {name}! You've successfully punched in for **{service}**. 🌟")
                        st.info(f"📖 Verse for you: {verse}")
                    except Exception as e:
                        st.error(f"❌ Failed to save punch-in: {str(e)}")
                        st.info(f"📝 Punch-in recorded locally: {name} - {service} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    verse = random.choice(volunteer_verses)
                    st.success(f"👋 Welcome {name}! You've successfully punched in for **{service}**. 🌟")
                    st.info(f"📝 Punch-in recorded locally: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    st.info(f"📖 Verse for you: {verse}")
                st.stop()

            if st.button("Punch Out", key="punch_out"):
                if SHEETS_ENABLED:
                    try:
                        punch_sheet.append_row([name, service, "Out", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                        verse = random.choice(volunteer_verses)
                        st.success(f"🎉 Great job, {name}! You've successfully punched out from **{service}**. 🙏")
                        st.info(f"📖 Verse for you: {verse}")
                    except Exception as e:
                        st.error(f"❌ Failed to save punch-out: {str(e)}")
                        st.info(f"📝 Punch-out recorded locally: {name} - {service} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    verse = random.choice(volunteer_verses)
                    st.success(f"🎉 Great job, {name}! You've successfully punched out from **{service}**. 🙏")
                    st.info(f"📝 Punch-out recorded locally: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    st.info(f"📖 Verse for you: {verse}")
                st.stop()
    else:
        st.info("📝 Please enter your name to get started.")
