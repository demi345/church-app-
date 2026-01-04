# Deployment Guide - St. Anthony Volunteer System

## 🚀 Choose Your Deployment

### Option 1: Full System (`app.py`) - RECOMMENDED
**Best for:** Complete volunteer management with registration + QR punch system

**Features:**
- Station-based volunteer registration (5 stations)
- Tabbed interface (Friday/Saturday/Sunday)
- QR code punch in/out functionality
- Google Sheets integration
- Church branding with Coptic crosses

**Deploy Command:**
```bash
streamlit run app.py
```

### Option 2: QR-Only System (`working_qr.py`)
**Best for:** Simple punch in/out system without registration

**Features:**
- QR punch in/out only
- Lightweight and fast
- No registration complexity
- Good for backup or secondary deployment

**Deploy Command:**
```bash
streamlit run working_qr.py
```

## 🌐 Cloud Deployment Options

### Streamlit Cloud (Recommended)
1. **Push to GitHub** ✅ (You're doing this now)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. **Choose app file:** `app.py` (for full system) or `working_qr.py` (for QR-only)
5. Deploy!

**Streamlit Cloud URLs will be:**
- `https://yourapp.streamlit.app`
- `https://yourapp.streamlit.app?action=punch_in`
- `https://yourapp.streamlit.app?action=punch_out`

### Railway
```bash
# Add Procfile
echo "web: streamlit run app.py --server.port \$PORT" > Procfile
```

### Heroku
```bash
# Add runtime.txt
echo "python-3.11.0" > runtime.txt

# Add Procfile  
echo "web: streamlit run app.py --server.port \$PORT --server.address 0.0.0.0" > Procfile
```

## 📱 Current Local Setup

Your system is already running locally:
- **Full System**: `http://192.168.1.172:8501`
- **QR Punch In**: `http://192.168.1.172:8501?action=punch_in` 
- **QR Punch Out**: `http://192.168.1.172:8501?action=punch_out`

## 🔧 Pre-Deployment Checklist

### Required Files ✅
- [x] `app.py` - Main application
- [x] `working_qr.py` - QR-only backup
- [x] `requirements.txt` - Dependencies
- [x] `service_account.json` - Google Sheets credentials
- [x] `stanthonylogo.png` - Church logo
- [x] `generate_qr_codes.py` - QR PDF generator

### Configuration
- [x] Location verification removed
- [x] 5 stations configured
- [x] Time slots set up
- [x] Coptic cross branding
- [x] Light theme applied

## 🎯 After Deployment

### Update QR Codes
Once deployed to cloud, regenerate QR codes with new URLs:

```bash
# Update URLs in generate_qr_codes.py first, then:
python generate_qr_codes.py --separate-pdfs-only
```

### Test Both Systems
1. **Full Registration**: Test all 5 stations and time slots
2. **QR Functionality**: Test punch in/out from QR codes
3. **Mobile Access**: Verify mobile responsiveness
4. **Google Sheets**: Confirm data is saving properly

## 🆘 Troubleshooting

### Google Sheets Issues
- Ensure `service_account.json` is uploaded
- Check sheet names: "Volunteers" and "Punch_Records"
- Verify Google Sheets API is enabled

### QR Code Issues
- Update URLs in `generate_qr_codes.py` after deployment
- Regenerate PDFs with correct deployed URLs
- Test QR codes scan to correct endpoints

---

**Ready to deploy both systems!** 🚀