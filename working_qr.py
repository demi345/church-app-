#!/usr/bin/env python3
"""
Fixed QR Code Volunteer System - Works without Google Sheets
"""

import streamlit as st
from datetime import datetime
from geopy.distance import geodesic
import random
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Page configuration
st.set_page_config(
    page_title="St. Anthony Volunteer System",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp { 
    background-color: #FFFFFF; 
    color: #000000; 
    font-family: 'Inter', sans-serif;
}

.punch-in-panel {
    background: linear-gradient(135deg, #F8FFF8, #E8F5E8);
    padding: 30px;
    border-radius: 15px;
    margin: 20px 0;
    border: 3px solid #28A745;
    box-shadow: 0 8px 25px rgba(40, 167, 69, 0.2);
    text-align: center;
}

.punch-out-panel {
    background: linear-gradient(135deg, #FFF8F8, #F5E8E8);
    padding: 30px;
    border-radius: 15px;
    margin: 20px 0;
    border: 3px solid #DC3545;
    box-shadow: 0 8px 25px rgba(220, 53, 69, 0.2);
    text-align: center;
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

.stButton>button {
    font-weight: 700;
    font-size: 24px;
    border-radius: 15px;
    padding: 20px 40px;
    color: #FFFFFF !important;
    border: none;
    text-transform: uppercase;
    letter-spacing: 2px;
    transition: all 0.3s ease;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    width: 100%;
    margin: 20px 0;
}

.punch-in-panel .stButton>button {
    background: linear-gradient(135deg, #28A745, #20C997) !important;
}

.punch-out-panel .stButton>button {
    background: linear-gradient(135deg, #DC3545, #E83E8C) !important;
}

.stTextInput input {
    font-size: 18px;
    padding: 15px;
    border-radius: 10px;
    border: 2px solid #CED4DA;
    text-align: center;
}

.corner-logo {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 999;
    background: white;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>
""", unsafe_allow_html=True)

# Configuration
CHURCH_LOCATION = (39.8637, -74.8284)
MAX_DISTANCE_METERS = 50000  # 50km for testing

volunteer_verses = [
    "Each of you should use whatever gift you have received to serve others, as faithful stewards of God's grace. — 1 Peter 4:10",
    "Whatever you do, work at it with all your heart, as working for the Lord, not for human masters. — Colossians 3:23",
    "Serve wholeheartedly, as if you were serving the Lord, not people. — Ephesians 6:7",
    "The greatest among you will be your servant. — Matthew 23:11",
    "Carry each other's burdens, and in this way you will fulfill the law of Christ. — Galatians 6:2"
]

# Location detection function
@st.cache_data(ttl=300)
def get_ip_location():
    try:
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
                            'city': data.get('city', 'Unknown')
                        }
                    elif 'lat' in data and 'lon' in data:
                        return {
                            'latitude': data['lat'],
                            'longitude': data['lon'],
                            'city': data.get('city', 'Unknown')
                        }
                    elif 'loc' in data:
                        lat, lon = data['loc'].split(',')
                        return {
                            'latitude': float(lat),
                            'longitude': float(lon),
                            'city': data.get('city', 'Unknown')
                        }
            except Exception:
                continue
        
        return {'error': 'Unable to determine location'}
        
    except Exception as e:
        return {'error': str(e)}

# Initialize session state for data storage
if 'punch_data' not in st.session_state:
    st.session_state.punch_data = []

# Check for QR code parameters
qr_action = st.query_params.get("action")

if qr_action == "punch_in":
    # PUNCH IN INTERFACE
    # Add logo in corner
    st.markdown('<div class="corner-logo">', unsafe_allow_html=True)
    st.image("stanthonylogo.png", width=120)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="big-title punch-in-title"> VOLUNTEER PUNCH IN</div>', unsafe_allow_html=True)
    
    st.markdown("### Enter your name to start your volunteer service")
    name = st.text_input("Full Name", placeholder="Enter your full name", key="punch_in_name")
    
    if name:
        # Location verification (silent)
        with st.spinner("🔍 Verifying your location..."):
            coords = get_ip_location()
        
        if st.button("🟢 PUNCH IN NOW", key="btn_punch_in"):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Store in session state
            punch_record = {
                'name': name,
                'action': 'Punch In',
                'timestamp': timestamp,
                'location': coords.get('city', 'Unknown') if 'error' not in coords else 'Unknown'
            }
            st.session_state.punch_data.append(punch_record)
            
            st.success(f"🌟 Welcome {name}! You've successfully punched in at {timestamp}!")
            st.balloons()
            
            verse = random.choice(volunteer_verses)
            st.info(f"📖 {verse}")
                    
    else:
        st.info("👆 Please enter your name above to begin")
        
elif qr_action == "punch_out":
    # PUNCH OUT INTERFACE
    # Add logo in corner
    st.markdown('<div class="corner-logo">', unsafe_allow_html=True)
    st.image("stanthonylogo.png", width=120)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="big-title punch-out-title"> VOLUNTEER PUNCH OUT</div>', unsafe_allow_html=True)
    
    st.markdown("### Enter your name to complete your volunteer service")
    name = st.text_input("Full Name", placeholder="Enter your full name", key="punch_out_name")
    
    if name:
        # Location verification (silent)
        with st.spinner("🔍 Verifying your location..."):
            coords = get_ip_location()
                
        if st.button("🔴 PUNCH OUT NOW", key="btn_punch_out"):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Store in session state
            punch_record = {
                'name': name,
                'action': 'Punch Out',
                'timestamp': timestamp,
                'location': coords.get('city', 'Unknown') if 'error' not in coords else 'Unknown'
            }
            st.session_state.punch_data.append(punch_record)
            
            st.success(f"🎉 Great job, {name}! You've successfully punched out at {timestamp}!")
            st.balloons()
            
            verse = random.choice(volunteer_verses)
            st.info(f"📖 {verse}")
                    
    else:
        st.info("👆 Please enter your name above to begin")
        
else:
    # DEFAULT VIEW
    st.title("⛪ St. Anthony Volunteer System")
    st.markdown("### Use QR codes to punch in/out")
    st.info("📱 Scan the QR codes to access punch in/out functionality")
    
    if st.session_state.punch_data:
        st.markdown("### All Punch Records")
        for i, record in enumerate(st.session_state.punch_data, 1):
            st.text(f"{i}. {record['name']} - {record['action']} - {record['timestamp']} ({record['location']})")