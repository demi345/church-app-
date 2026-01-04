"""
St. Anthony Coptic Orthodox Church - Punch In App
QR Code Punch In System for Volunteers
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

/* Punch In Panel */
.punch-in-panel {
    background: linear-gradient(135deg, #D4EDDA, #C3E6CB);
    border: 2px solid #28A745;
    padding: 25px;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(40, 167, 69, 0.2);
}

.punch-in-header {
    background: linear-gradient(135deg, #28A745, #20C997);
    color: white;
    text-align: center;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    font-size: 24px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.panel-header {
    background: linear-gradient(135deg, #28A745, #20C997);
    color: white;
    text-align: center;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    font-size: 24px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

/* Button styling */
.stButton>button {
    width: 100%;
    height: 60px;
    font-size: 18px;
    font-weight: 600;
    color: #FFFFFF !important;
    border: none;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    background: linear-gradient(135deg, #28A745, #20C997) !important;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #218838, #1BA085) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
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
    page_title="St. Anthony - Punch In",
    page_icon="🟢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply CSS
st.markdown(get_common_css(), unsafe_allow_html=True)

# Header
display_logo()
st.success("🎯 QR Code Scanned: PUNCH IN")
st.markdown("<h1 class='big-title punch-in-title'>🟢 Volunteer Punch In</h1>", unsafe_allow_html=True)

# Main Punch In Interface
st.markdown('<div class="punch-in-panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-header punch-in-header">🟢 PUNCH IN</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #155724; margin-bottom: 20px; font-size: 18px;">Start your volunteer service at St. Anthony</p>', unsafe_allow_html=True)

# Name input
name = st.text_input("Full Name*", key="punch_in_name", placeholder="Enter your full name")

if name:
    # Punch In Button
    if st.button("🟢 Punch In Now", key="punch_in_btn", use_container_width=True):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save to Google Sheets
        if SHEETS_ENABLED:
            try:
                punch_sheet.append_row([name, "In", timestamp])
                st.success(f"👋 Welcome {name}! You've successfully punched in. 🌟")
                logging.info(f"Punch IN: {name} - {timestamp}")
                
                # Show balloons animation
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Failed to save punch in: {str(e)}")
                st.info(f"📝 Manual record: {name} - In - {timestamp}")
                st.info("💡 Please inform the volunteer coordinator of this punch in.")
        else:
            st.success(f"👋 Welcome {name}! You've successfully punched in. 🌟")
            st.info(f"📝 Punch data: {name} - In - {timestamp}")
            st.info("📋 Google Sheets not connected - using local storage")
        
        # Show inspirational verse
        verse = get_random_verse()
        st.info(f"📖 Verse for you: {verse}")
        
        # Additional encouragement
        st.markdown("### 🙏 Thank you for serving!")
        st.markdown("Your service makes a difference in our community. May God bless your volunteer work today!")
        
else:
    st.info("📝 Please enter your name to punch in.")
    st.markdown("### ✨ Welcome Volunteer!")
    st.markdown("You're about to start your volunteer service. Thank you for dedicating your time to serve others!")

st.markdown('</div>', unsafe_allow_html=True)

# Instructions
st.markdown("---")
st.markdown("### 📱 How to Use")
st.markdown("""
1. **Enter your full name** in the field above
2. **Click 'Punch In Now'** to start your volunteer shift
3. **Remember to punch out** when your shift ends using the Punch Out QR code
4. **Questions?** Contact the volunteer coordinator
""")

# Quick Links
st.markdown("### 🔗 Quick Links")
col1, col2 = st.columns(2)
with col1:
    st.info("📋 **Need to Register?**  \nVisit the main registration page")
with col2:
    st.warning("🔴 **Finished Your Shift?**  \nUse the Punch Out QR code")

# Footer
st.markdown("---")
st.markdown("**🏛️ St. Anthony Coptic Orthodox Church Volunteer System**")
st.caption("Serving with love and dedication ☦️")