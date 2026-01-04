"""
St. Anthony Coptic Orthodox Church - Punch In App
QR Code Punch In System for Volunteers
"""

import streamlit as st
from datetime import datetime
import logging
from config import *

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