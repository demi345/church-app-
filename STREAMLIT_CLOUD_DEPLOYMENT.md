# 🚀 Streamlit Cloud Deployment Guide

## St. Anthony Volunteer System - Complete Deployment

Your repository is ready for deployment with **3 separate apps**:

### ✅ **Apps Ready to Deploy**

1. **registration.py** - Volunteer registration (5 stations, time slots)
2. **punch_in.py** - QR code punch in (green theme)
3. **punch_out.py** - QR code punch out (red theme)
4. **app.py** - Combined system (backup option)

All apps are verified, error-free, and tested locally.

---

## 📋 **Step-by-Step Deployment**

### **Step 1: Go to Streamlit Cloud**
Visit: [share.streamlit.io](https://share.streamlit.io)
- Sign in with GitHub account
- Click "New app"

### **Step 2: Deploy Registration App**

| Setting | Value |
|---------|-------|
| **Repository** | `demi345/church-app-` |
| **Branch** | `main` |
| **Main file** | `registration.py` |
| **App URL name** | `stanthony-registration` |

**Result URL:** `https://stanthony-registration.streamlit.app`

### **Step 3: Deploy Punch In App**

| Setting | Value |
|---------|-------|
| **Repository** | `demi345/church-app-` |
| **Branch** | `main` |
| **Main file** | `punch_in.py` |
| **App URL name** | `stanthony-punchin` |

**Result URL:** `https://stanthony-punchin.streamlit.app`

### **Step 4: Deploy Punch Out App**

| Setting | Value |
|---------|-------|
| **Repository** | `demi345/church-app-` |
| **Branch** | `main` |
| **Main file** | `punch_out.py` |
| **App URL name** | `stanthony-punchout` |

**Result URL:** `https://stanthony-punchout.streamlit.app`

### **Step 5 (Optional): Deploy Combined App**

| Setting | Value |
|---------|-------|
| **Repository** | `demi345/church-app-` |
| **Branch** | `main` |
| **Main file** | `app.py` |
| **App URL name** | `stanthony-combined` |

**Result URL:** `https://stanthony-combined.streamlit.app`

---

## 🔑 **Secrets Configuration (For Google Sheets)**

If you want Google Sheets integration:

1. In Streamlit Cloud app settings, click **Secrets**
2. Add your service account JSON:

```toml
gcp_service_account = """
{
  "type": "service_account",
  "project_id": "your-project",
  ...rest of service account JSON...
}
"""
```

**Note:** App works fine WITHOUT secrets (uses local storage as fallback)

---

## 🎯 **Your Final URLs**

### **Production URLs (After Deployment)**

| App | URL |
|-----|-----|
| 📋 **Registration** | `https://stanthony-registration.streamlit.app` |
| 🟢 **Punch In** | `https://stanthony-punchin.streamlit.app` |
| 🔴 **Punch Out** | `https://stanthony-punchout.streamlit.app` |
| 🔗 **Combined** | `https://stanthony-combined.streamlit.app` |

### **QR Code URLs**
- **Punch In QR** → `https://stanthony-punchin.streamlit.app`
- **Punch Out QR** → `https://stanthony-punchout.streamlit.app`

---

## 📱 **Local Testing URLs (For Reference)**

These are your current local URLs (while running locally):

| App | Local URL |
|-----|-----------|
| 📋 Registration | `http://localhost:8501` |
| 🟢 Punch In | `http://localhost:8502` |
| 🔴 Punch Out | `http://localhost:8503` |

---

## ✅ **Deployment Checklist**

- [x] All apps verified (syntax, imports, runtime)
- [x] requirements.txt configured
- [x] GitHub repository updated
- [x] Apps tested locally
- [ ] Deploy Registration to Streamlit Cloud
- [ ] Deploy Punch In to Streamlit Cloud
- [ ] Deploy Punch Out to Streamlit Cloud
- [ ] Add Google Sheets secrets (optional)
- [ ] Generate QR codes with cloud URLs
- [ ] Test all 3 apps on cloud
- [ ] Share URLs with volunteers

---

## 🎨 **App Features**

### **Registration App**
- ☦️ Coptic cross branding
- 5 volunteer stations
- 3 days (Friday, Saturday, Sunday)
- Time slots for each day
- Personal info collection
- Station preferences

### **Punch In App** (Green Theme)
- QR code ready
- Name entry
- Instant punch in
- Inspirational verses
- Balloons celebration

### **Punch Out App** (Red Theme)
- QR code ready
- Name entry
- Instant punch out
- Feedback collection
- Service completion messages

---

## 🔄 **Update QR Codes**

After deployment, generate new QR codes with cloud URLs:

```bash
python generate_qr_codes.py --separate-pdfs-only
```

Update the URLs in `generate_qr_codes.py`:
```python
PUNCH_IN_URL = "https://stanthony-punchin.streamlit.app"
PUNCH_OUT_URL = "https://stanthony-punchout.streamlit.app"
```

---

## 📞 **Troubleshooting**

### App won't load
- Check all requirements.txt packages are available
- Verify GitHub repository is public

### Google Sheets not connecting
- Add service account JSON to Streamlit Secrets
- Or use local fallback (no sheets needed)

### QR codes not scanning
- Ensure URLs are correct and deployed
- Check QR code PDF generation

---

## 🙏 **Ready for Launch!**

Your volunteer system is deployment-ready. Follow the steps above to launch all 3 apps to production!

**Questions?** Refer to [Streamlit Cloud Docs](https://docs.streamlit.io/deploy/streamlit-cloud)