"""
Shared configuration and functions for St. Anthony Volunteer System
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
    """Return common CSS styling for all apps"""
    return """
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

/* Punch Out Panel */
.punch-out-panel {
    background: linear-gradient(135deg, #F8D7DA, #F1C2C7);
    border: 2px solid #DC3545;
    padding: 25px;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(220, 53, 69, 0.2);
}

.punch-out-header {
    background: linear-gradient(135deg, #DC3545, #E83E8C);
    color: white;
    text-align: center;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    font-size: 24px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
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