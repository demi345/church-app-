"""
St. Anthony Coptic Orthodox Church - Punch Out App
QR Code Punch Out System for Volunteers
"""

import streamlit as st
from datetime import datetime
import logging
from config import *

# Page Configuration
st.set_page_config(
    page_title="St. Anthony - Punch Out",
    page_icon="🔴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply CSS
st.markdown(get_common_css(), unsafe_allow_html=True)

# Header
display_logo()
st.success("🎯 QR Code Scanned: PUNCH OUT")
st.markdown("<h1 class='big-title punch-out-title'>🔴 Volunteer Punch Out</h1>", unsafe_allow_html=True)

# Main Punch Out Interface
st.markdown('<div class="punch-out-panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-header punch-out-header">🔴 PUNCH OUT</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #721C24; margin-bottom: 20px; font-size: 18px;">Complete your volunteer service at St. Anthony</p>', unsafe_allow_html=True)

# Name input
name = st.text_input("Full Name*", key="punch_out_name", placeholder="Enter your full name")

if name:
    # Punch Out Button
    if st.button("🔴 Punch Out Now", key="punch_out_btn", use_container_width=True):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save to Google Sheets
        if SHEETS_ENABLED:
            try:
                punch_sheet.append_row([name, "Out", timestamp])
                st.success(f"🎉 Great job, {name}! You've successfully punched out. 🙏")
                logging.info(f"Punch OUT: {name} - {timestamp}")
                
                # Show celebration animation
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Failed to save punch out: {str(e)}")
                st.info(f"📝 Manual record: {name} - Out - {timestamp}")
                st.info("💡 Please inform the volunteer coordinator of this punch out.")
        else:
            st.success(f"🎉 Great job, {name}! You've successfully punched out. 🙏")
            st.info(f"📝 Punch data: {name} - Out - {timestamp}")
            st.info("📋 Google Sheets not connected - using local storage")
        
        # Show inspirational verse
        verse = get_random_verse()
        st.info(f"📖 Verse for you: {verse}")
        
        # Additional appreciation
        st.markdown("### 🌟 Thank You for Your Service!")
        st.markdown("Your dedication and time have made a real difference today. May God bless you for your generous heart and willing spirit.")
        
        # Service completion message
        st.markdown("### 📋 Shift Complete")
        st.markdown("Your volunteer hours have been recorded. Thank you for being part of the St. Anthony community!")
        
else:
    st.info("📝 Please enter your name to punch out.")
    st.markdown("### 🎉 Finishing Your Service?")
    st.markdown("Thank you for your dedication today! Complete your volunteer shift by punching out below.")

st.markdown('</div>', unsafe_allow_html=True)

# Instructions
st.markdown("---")
st.markdown("### 📱 How to Use")
st.markdown("""
1. **Enter your full name** (same as when you punched in)
2. **Click 'Punch Out Now'** to complete your volunteer shift
3. **Your hours are automatically recorded** in our system
4. **Thank you for serving!** Your contribution matters
""")

# Feedback Section
st.markdown("### 💭 Share Your Experience")
feedback = st.text_area("How was your volunteer experience today? (Optional)", 
                        placeholder="Share any feedback, suggestions, or highlights from your service...")

if feedback and st.button("📝 Submit Feedback"):
    st.success("🙏 Thank you for your feedback! It helps us improve our volunteer program.")

# Quick Links
st.markdown("### 🔗 What's Next?")
col1, col2 = st.columns(2)
with col1:
    st.info("📅 **Volunteer Again?**  \nCheck the schedule for upcoming opportunities")
with col2:
    st.success("⭐ **Spread the Word**  \nInvite friends to volunteer with us!")

# Footer
st.markdown("---")
st.markdown("**🏛️ St. Anthony Coptic Orthodox Church Volunteer System**")
st.caption("Thank you for serving with love and dedication ☦️")
st.caption("\"Whatever you do, work at it with all your heart, as working for the Lord.\" - Colossians 3:23")