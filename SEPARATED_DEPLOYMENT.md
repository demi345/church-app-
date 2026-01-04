# St. Anthony Volunteer System - Separated Apps Deployment

## 🎯 **Four Separate Apps Ready to Deploy**

### 1. **Registration App** (`registration.py`)
- **URL**: `https://your-domain/registration`
- **Purpose**: Complete volunteer registration with 5 stations
- **Features**: Station selection, time slots, personal info collection

### 2. **Punch In App** (`punch_in.py`) 
- **URL**: `https://your-domain/punch-in`
- **Purpose**: QR code punch in system
- **Features**: Quick name entry + punch in with verses

### 3. **Punch Out App** (`punch_out.py`)
- **URL**: `https://your-domain/punch-out` 
- **Purpose**: QR code punch out system
- **Features**: Quick name entry + punch out with feedback

### 4. **Original Combined App** (`app.py`)
- **URL**: `https://your-domain/combined`
- **Purpose**: All-in-one system (backup option)

## 🚀 **Deployment Options**

### **Option 1: Streamlit Cloud (Multiple Apps)**

Deploy each as separate Streamlit apps:

1. **Create 4 GitHub repositories:**
   - `st-anthony-registration`
   - `st-anthony-punch-in` 
   - `st-anthony-punch-out`
   - `st-anthony-combined`

2. **Or create 1 repository with multiple apps:**
   - Single repo: `st-anthony-volunteer-system`
   - Deploy 4 different apps from same repo
   - Choose different main files for each deployment

### **Option 2: Single Repository - Multiple Deployments**

**Repository Structure:**
```
st-anthony-volunteer-system/
├── registration.py        # Main registration app
├── punch_in.py           # Punch in app  
├── punch_out.py          # Punch out app
├── app.py               # Combined app (backup)
├── config.py            # Shared configuration
├── requirements.txt     # Dependencies
├── service_account.json # Google Sheets
└── stanthonylogo.png    # Church logo
```

**Streamlit Cloud Deployments:**
1. **Registration**: Deploy with `registration.py` as main file
2. **Punch In**: Deploy with `punch_in.py` as main file  
3. **Punch Out**: Deploy with `punch_out.py` as main file
4. **Combined**: Deploy with `app.py` as main file

## 🔗 **URL Structure After Deployment**

### **Clean URLs:**
- **Registration**: `https://stanthony-registration.streamlit.app`
- **Punch In**: `https://stanthony-punchin.streamlit.app`
- **Punch Out**: `https://stanthony-punchout.streamlit.app`

### **QR Code URLs:**
- **Punch In QR**: `https://stanthony-punchin.streamlit.app`
- **Punch Out QR**: `https://stanthony-punchout.streamlit.app`

## 📱 **Current Local URLs (For Testing)**

### **Test Each App Locally:**
```bash
# Registration App
streamlit run registration.py --server.port 8501

# Punch In App  
streamlit run punch_in.py --server.port 8502

# Punch Out App
streamlit run punch_out.py --server.port 8503

# Combined App
streamlit run app.py --server.port 8504
```

**Local URLs:**
- Registration: `http://localhost:8501`
- Punch In: `http://localhost:8502`  
- Punch Out: `http://localhost:8503`
- Combined: `http://localhost:8504`

## ⚙️ **Configuration Setup**

### **Shared Config (`config.py`)**
- Google Sheets connection
- Common styling and functions
- Church location and settings
- Volunteer verses

### **Each App Imports:**
```python
from config import *
```

## 🎨 **Benefits of Separation**

### ✅ **Advantages:**
1. **Faster Loading**: Each app loads only what it needs
2. **Cleaner URLs**: Specific purpose URLs for QR codes  
3. **Better Mobile**: Focused mobile experience
4. **Easier Maintenance**: Update individual components
5. **Scalable**: Deploy to different services if needed

### 📋 **Use Cases:**
- **Registration**: Volunteers use before events
- **Punch In**: QR code for starting shifts
- **Punch Out**: QR code for ending shifts  
- **Combined**: Backup option with everything

## 🎯 **Next Steps**

1. **Test locally** - Run all 4 apps on different ports
2. **Choose deployment strategy** - Single repo vs multiple repos
3. **Deploy to Streamlit Cloud** - Create clean URLs
4. **Update QR codes** - Generate with new cloud URLs
5. **Test end-to-end** - Registration → QR punch in/out

## 🔄 **QR Code Update Process**

After deployment, update the QR generator:

```python
# In generate_qr_codes.py, update URLs:
PUNCH_IN_URL = "https://stanthony-punchin.streamlit.app"
PUNCH_OUT_URL = "https://stanthony-punchout.streamlit.app"
```

Then regenerate:
```bash
python generate_qr_codes.py --separate-pdfs-only
```

---

**🏛️ Ready to deploy 4 focused, fast-loading apps!** ☦️