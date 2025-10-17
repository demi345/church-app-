import streamlit as st
from datetime import datetime
from geopy.distance import geodesic
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

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
</style>
""", unsafe_allow_html=True)

# ------------------ Config ------------------
CHURCH_LOCATION = (39.8637, -74.8284)
MAX_DISTANCE_METERS = 100
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
    st.warning(f"Google Sheets not connected: {str(e)}. Running in Demo mode.")
    SHEETS_ENABLED = False
    punch_sheet = None
    reg_sheet = None

# ------------------ Session State ------------------
for key in ["punched_in", "punched_out", "coords"]:
    if key not in st.session_state:
        st.session_state[key] = None
if st.session_state["punched_in"] is None: st.session_state["punched_in"] = False
if st.session_state["punched_out"] is None: st.session_state["punched_out"] = False

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
                    except Exception as e:
                        st.error(f"❌ Failed to save registration: {str(e)}")
                else:
                    st.success(f"✅ Thank you {first_name}! Demo mode: registration not saved.")
                    
# ------------------ TAB 2: Punch In/Out ------------------
with tab2:
    st.markdown("<h1>⏱ Punch In/Out</h1>", unsafe_allow_html=True)
    st.markdown("<p>Enter your name, select your service, and allow location access.</p>", unsafe_allow_html=True)
    
    name = st.text_input("Full Name*", key="punch_name")
    service = st.selectbox("Select Service", ["Food Stand", "Parking", "Setup/Cleanup", "Other"], key="punch_service")

    if st.button("📍 Get My Location"):
        try:
            import streamlit_geolocation as sg
            location = sg.get_geolocation()
            if location:
                st.session_state["coords"] = location
                st.success(f"Location received: ({location['lat']:.5f}, {location['lon']:.5f})")
            else:
                st.error("Could not get location. Please enable location services.")
        except ModuleNotFoundError:
            st.error("Install streamlit_geolocation via `pip install streamlit-geolocation`")

    coords = st.session_state["coords"]
    if coords:
        lat, lon = coords['lat'], coords['lon']
        distance = geodesic(CHURCH_LOCATION, (lat, lon)).meters
        if distance > MAX_DISTANCE_METERS:
            st.error(f"❌ You are {int(distance)}m away from the church. Must be within {MAX_DISTANCE_METERS}m.")
            st.stop()
        else:
            st.success(f"✅ Location verified ({int(distance)}m from church). You can punch in/out.")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🟢 Punch In") and not st.session_state["punched_in"]:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if SHEETS_ENABLED:
                        try:
                            punch_sheet.append_row([name, service, "In", timestamp])
                            st.success(f"👋 {name}, you've punched in for **{service}**!")
                        except Exception as e:
                            st.error(f"Failed to save: {str(e)}")
                    else:
                        st.info(f"(Demo) {name} punched in for {service}")
                    st.session_state["punched_in"] = True
                    verse = random.choice(volunteer_verses)
                    st.info(f"📖 Verse: {verse}")

            with col2:
                if st.button("🔴 Punch Out") and not st.session_state["punched_out"]:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if SHEETS_ENABLED:
                        try:
                            punch_sheet.append_row([name, service, "Out", timestamp])
                            st.success(f"🎉 {name}, you've punched out from **{service}**!")
                        except Exception as e:
                            st.error(f"Failed to save: {str(e)}")
                    else:
                        st.info(f"(Demo) {name} punched out from {service}")
                    st.session_state["punched_out"] = True
                    verse = random.choice(volunteer_verses)
                    st.info(f"📖 Verse: {verse}")

    else:
        st.info("📍 Click 'Get My Location' to enable punch buttons.")
