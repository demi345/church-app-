# St. Anthony Coptic Orthodox Church - Volunteer Management System

## 🏛️ Overview
A comprehensive volunteer management system for St. Anthony Coptic Orthodox Church featuring station-based registration and QR code punch in/out functionality.

## 📱 Two Deployment Options

### 1. **Full System** (`app.py`) 
- Complete volunteer registration with 5 stations
- Tabbed interface for Friday/Saturday/Sunday
- QR code punch in/out functionality
- Google Sheets integration
- **Deploy this for full functionality**

### 2. **QR-Only System** (`working_qr.py`)
- Simplified QR punch in/out only
- No registration form
- Lightweight backup option
- **Deploy this for QR-only functionality**

## 🚀 Quick Deploy URLs

### Local Network Access
- **Full System**: `http://192.168.1.172:8501`
- **QR Punch In**: `http://192.168.1.172:8501?action=punch_in`
- **QR Punch Out**: `http://192.168.1.172:8501?action=punch_out`

### Cloud Deployment
Replace with your deployed URLs when hosting on Streamlit Cloud, Heroku, or other platforms.

## 🏗️ Installation & Setup

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run Full System
```bash
streamlit run app.py
```

### Run QR-Only System
```bash
streamlit run working_qr.py
```

## 📊 Station Configuration

### 5 Volunteer Stations:
1. **🎁 Prizes and Games**
2. **💄 Cosmetology** 
3. **🎈 Inflatables**
4. **🏀 Basketball**
5. **🍿 Snacking**

### Time Slots:
- **Friday**: 2 time slots
- **Saturday**: 4 time slots  
- **Sunday**: 2 time slots

## 🔧 Configuration

### Google Sheets Integration
- Place `service_account.json` in project root
- Update `SPREADSHEET_ID` in code with your Google Sheet ID
- Ensure sheets named "Volunteers" and "Punch_Records" exist

### Church Logo
- Place `stanthonylogo.png` in project root (150px width recommended)

## 📋 Generated Files

### QR Code PDFs
Run the QR generator:
```bash
python generate_qr_codes.py --separate-pdfs-only
```

Generates:
- `punch_in.pdf` - Green themed QR code for punch in
- `punch_out.pdf` - Red themed QR code for punch out

## 🎨 Features

### UI Improvements
- ☦️ Coptic cross branding
- Light tabbed interface
- Clean design without unnecessary panels
- Mobile-responsive layout

### Security & Verification
- Location verification removed for simplified access
- Direct punch in/out without restrictions
- Volunteer verses displayed after punch actions

## 📈 Data Management

### Registration Data
Collected fields:
- Name, Email, Phone, Emergency Contact
- Station preference and time availability
- Age group and volunteer experience

### Punch Records  
Tracked data:
- Volunteer name
- Punch in/out timestamp
- Action type (In/Out)

## 🔄 Deployment Options

### Streamlit Cloud
1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy `app.py` for full system or `working_qr.py` for QR-only

### Local Network
- Already configured for `192.168.1.172:8501`
- Access from any device on same WiFi network

### Heroku/Railway/Other
- Standard Python app deployment
- Use provided `requirements.txt`
- Set environment variables for Google Sheets if needed

## 🛠️ Development

### File Structure
```
├── app.py                 # Main application (deploy this)
├── working_qr.py          # QR-only system (alternative)
├── generate_qr_codes.py   # QR code PDF generator
├── requirements.txt       # Python dependencies
├── service_account.json   # Google Sheets credentials
├── stanthonylogo.png      # Church logo
└── qr_codes/             # Generated QR code files
```

### Recent Updates
- Removed location verification for simplified access
- Streamlined punch in/out process
- Fixed code structure and indentation issues
- Clean UI with tabbed interface
- Coptic cross branding throughout

---

**For St. Anthony Coptic Orthodox Church Volunteer Management**  
*Built with Streamlit & Python* ☦️