# 🏛️ St. Anthony Coptic Orthodox Church - Volunteer Management System

## 📋 Project Overview

This is a production-ready volunteer management system for St. Anthony Coptic Orthodox Church, featuring:
- 📝 Volunteer registration with availability tracking
- ⏱️ Location-verified punch in/out system
- 🌍 IP-based location detection with street address lookup
- 📊 Google Sheets integration for data storage
- 📱 Mobile-optimized responsive design
- 🔒 Enterprise-grade security and logging

## 🚀 Quick Deployment (Recommended: Streamlit Community Cloud)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: St. Anthony Volunteer System"
git remote add origin https://github.com/yourusername/st-anthony-volunteers.git
git push -u origin main
```

### 2. Deploy to Streamlit Cloud (FREE)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Add secrets in the Streamlit Cloud dashboard:
   ```toml
   [secrets]
   gcp_service_account = '''
   {
     "type": "service_account",
     "project_id": "your-project-id",
     "private_key_id": "your-private-key-id",
     "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
     "client_email": "your-service-account@your-project.iam.gserviceaccount.com"
   }
   '''
   ```
4. Deploy!

## 🔧 Google Cloud Setup

### 1. Create Google Cloud Project
```bash
# Create new project
gcloud projects create st-anthony-volunteer-system
gcloud config set project st-anthony-volunteer-system

# Enable APIs
gcloud services enable sheets.googleapis.com
gcloud services enable drive.googleapis.com

# Create service account
gcloud iam service-accounts create volunteer-system \
    --display-name="Volunteer System Service Account"

# Create and download key
gcloud iam service-accounts keys create service-account.json \
    --iam-account=volunteer-system@st-anthony-volunteer-system.iam.gserviceaccount.com
```

### 2. Setup Google Sheets
1. Create a Google Sheet named "Volunteer Hours"
2. Create two worksheets: "Sheet1" and "Registration"
3. Share with your service account email
4. Grant "Editor" permissions

## 📁 Project Structure

```
st-anthony-volunteer-system/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── start.sh                 # Production startup script
├── README.md                # This documentation
├── .gitignore              # Git ignore rules
├── .streamlit/
│   └── config.toml         # Streamlit configuration
└── secrets.template.toml   # Template for secrets
```

## 🛡️ Security Features

### ✅ Production Security
- **Strict Location Verification**: 100m radius enforcement
- **Real Location Detection**: No fallback locations
- **Secure Secrets Management**: Environment-based configuration
- **Input Validation**: All forms validated and sanitized
- **Audit Logging**: Complete activity tracking
- **HTTPS Ready**: CORS and XSRF protection enabled

## 📱 Features

### 🌟 Volunteer Registration
- Personal information collection
- Availability scheduling (Thursday-Sunday)
- Automatic timestamping
- Google Sheets integration

### ⏱️ Punch In/Out System
- IP-based location detection
- Street address lookup
- Distance verification (100m radius)
- Service selection (Food Stand, Parking, Setup/Cleanup, Other)
- Inspirational Bible verses
- Complete audit trail

### 🌍 Location Detection
- **Multiple IP Services**: ipapi.co, ip-api.com, ipinfo.io
- **Reverse Geocoding**: Full street addresses
- **Fallback Protection**: Multiple service redundancy
- **Caching**: 5-minute TTL for performance

## 📊 Monitoring & Health Check

### Health Check Endpoint
Access `https://your-app-url.streamlit.app/?health=check` to get system status.

### Application Logs
- All volunteer registrations logged
- Punch in/out activities tracked
- Error conditions recorded
- Service usage monitored

## 🛠️ Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/st-anthony-volunteers.git
cd st-anthony-volunteers

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

## 📞 Support & Maintenance

### Regular Tasks
- **Monthly**: Review volunteer data and usage analytics
- **Quarterly**: Update dependencies and security patches
- **Yearly**: Rotate service account keys and review permissions

### Troubleshooting
- Check Google Sheets API quotas and permissions
- Monitor location detection accuracy and service availability
- Review application logs for errors or unusual patterns

---

## 🙏 About

This volunteer management system was built specifically for St. Anthony Coptic Orthodox Church to streamline volunteer coordination and track service hours. The system ensures volunteers are physically present at the church location while providing a seamless, mobile-friendly experience.

**Version**: 1.0.0  
**Built with**: Streamlit, Google Sheets API, Python  
**Deployment**: Production-ready for immediate use

🏛️ **May this system serve St. Anthony Coptic Orthodox Church faithfully!**
