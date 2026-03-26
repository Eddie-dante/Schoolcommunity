import streamlit as st
from datetime import datetime, timedelta
import hashlib
import json
import random
import string
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="✨ School Community Hub ✨",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ RESPONSIVE DESIGN META TAG ============
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
<style>
    @media (max-width: 768px) {
        .main .block-container { padding: 0.8rem !important; }
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.3rem !important; }
        .stButton button { font-size: 0.9rem !important; padding: 0.4rem 0.8rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ============ KENYAN CURRICULUM DATA ============
PRIMARY_SUBJECTS = [
    "Mathematics", "English", "Kiswahili", "Science and Technology",
    "Social Studies", "CRE / IRE / HRE", "Agriculture", "Home Science",
    "Art and Craft", "Music", "Physical Education"
]

JUNIOR_SECONDARY_SUBJECTS = [
    "Mathematics", "English", "Kiswahili", "Integrated Science",
    "Social Studies", "CRE / IRE / HRE", "Business Studies",
    "Agriculture", "Home Science", "Computer Science",
    "Pre-Technical Studies", "Visual Arts", "Performing Arts",
    "Physical Education"
]

SENIOR_SECONDARY_SUBJECTS = {
    "Mathematics": ["Mathematics"],
    "English": ["English"],
    "Kiswahili": ["Kiswahili"],
    "Sciences": ["Biology", "Chemistry", "Physics", "General Science"],
    "Humanities": ["History", "Geography", "CRE", "IRE", "HRE"],
    "Technical": ["Computer Studies", "Business Studies", "Agriculture", "Home Science"],
    "Languages": ["French", "German", "Arabic", "Sign Language"]
}

KENYAN_GRADES = [
    "Grade 1 (7 subjects)", "Grade 2 (7 subjects)", "Grade 3 (7 subjects)",
    "Grade 4 (7 subjects)", "Grade 5 (7 subjects)", "Grade 6 (7 subjects)",
    "Grade 7 (12 subjects)", "Grade 8 (12 subjects)", "Grade 9 (12 subjects)",
    "Form 1 (11 subjects)", "Form 2 (11 subjects)", "Form 3 (11 subjects)", "Form 4 (11 subjects)"
]

# ============ THEMES ============
THEMES = {
    "Sunrise Glow": {
        "primary": "#ff6b6b",
        "secondary": "#feca57",
        "accent": "#48dbfb",
        "background": "linear-gradient(135deg, #ff6b6b, #feca57, #ff9ff3, #48dbfb)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #cfa668, #e5b873, #f5d742)"
    },
    "Ocean Breeze": {
        "primary": "#00d2ff",
        "secondary": "#3a1c71",
        "accent": "#00ff00",
        "background": "linear-gradient(135deg, #00d2ff, #3a1c71, #d76d77, #ffaf7b)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #4facfe, #00f2fe, #43e97b)"
    },
    "Purple Haze": {
        "primary": "#8E2DE2",
        "secondary": "#4A00E0",
        "accent": "#a044ff",
        "background": "linear-gradient(135deg, #8E2DE2, #4A00E0, #6a3093, #a044ff)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #c471ed, #f64f59, #c471ed)"
    },
    "Tropical Paradise": {
        "primary": "#00b09b",
        "secondary": "#96c93d",
        "accent": "#fbd786",
        "background": "linear-gradient(135deg, #00b09b, #96c93d, #c6ffdd, #fbd786)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #4facfe, #00f2fe, #43e97b)"
    },
    "Cherry Blossom": {
        "primary": "#ff9a9e",
        "secondary": "#fad0c4",
        "accent": "#a1c4fd",
        "background": "linear-gradient(135deg, #ff9a9e, #fad0c4, #ffd1ff, #a1c4fd)",
        "text": "#333333",
        "sidebar": "linear-gradient(135deg, #fbc2eb, #a6c1ee, #fbc2eb)"
    },
    "Midnight City": {
        "primary": "#232526",
        "secondary": "#414345",
        "accent": "#4b6cb7",
        "background": "linear-gradient(135deg, #232526, #414345, #2c3e50, #4b6cb7)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #182848, #4b6cb7, #182848)"
    },
    "Autumn Leaves": {
        "primary": "#e44d2e",
        "secondary": "#f39c12",
        "accent": "#f1c40f",
        "background": "linear-gradient(135deg, #e44d2e, #f39c12, #d35400, #e67e22)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #f1c40f, #e67e22, #d35400)"
    },
    "Northern Lights": {
        "primary": "#43C6AC",
        "secondary": "#191654",
        "accent": "#00CDAC",
        "background": "linear-gradient(135deg, #43C6AC, #191654, #02AAB0, #00CDAC)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #02AAB0, #00CDAC, #191654)"
    },
    "Forest Mist": {
        "primary": "#11998e",
        "secondary": "#38ef7d",
        "accent": "#38ef7d",
        "background": "linear-gradient(135deg, #11998e, #38ef7d, #11998e, #38ef7d)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #11998e, #38ef7d, #11998e)"
    },
    "Lavender Dream": {
        "primary": "#aa4b6b",
        "secondary": "#6b6b83",
        "accent": "#3b8d99",
        "background": "linear-gradient(135deg, #aa4b6b, #6b6b83, #3b8d99, #aa4b6b)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #aa4b6b, #6b6b83, #3b8d99)"
    },
    "Sunset Orange": {
        "primary": "#f12711",
        "secondary": "#f5af19",
        "accent": "#f5af19",
        "background": "linear-gradient(135deg, #f12711, #f5af19, #f12711, #f5af19)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #f12711, #f5af19, #f12711)"
    },
    "Electric Blue": {
        "primary": "#00c6fb",
        "secondary": "#005bea",
        "accent": "#00c6fb",
        "background": "linear-gradient(135deg, #00c6fb, #005bea, #00c6fb, #005bea)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #00c6fb, #005bea, #00c6fb)"
    },
    "Pink Flamingo": {
        "primary": "#f857a6",
        "secondary": "#ff5858",
        "accent": "#f857a6",
        "background": "linear-gradient(135deg, #f857a6, #ff5858, #f857a6, #ff5858)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #f857a6, #ff5858, #f857a6)"
    },
    "Emerald City": {
        "primary": "#348f50",
        "secondary": "#56ab2f",
        "accent": "#56ab2f",
        "background": "linear-gradient(135deg, #348f50, #56ab2f, #348f50, #56ab2f)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #348f50, #56ab2f, #348f50)"
    },
    "Ruby Red": {
        "primary": "#cb356b",
        "secondary": "#bd3f32",
        "accent": "#cb356b",
        "background": "linear-gradient(135deg, #cb356b, #bd3f32, #cb356b, #bd3f32)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #cb356b, #bd3f32, #cb356b)"
    },
    "Sapphire Blue": {
        "primary": "#0f0c29",
        "secondary": "#302b63",
        "accent": "#24243e",
        "background": "linear-gradient(135deg, #0f0c29, #302b63, #24243e, #0f0c29)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #182848, #4b6cb7, #182848)"
    },
    "Amber Glow": {
        "primary": "#ff8008",
        "secondary": "#ffc837",
        "accent": "#ff8008",
        "background": "linear-gradient(135deg, #ff8008, #ffc837, #ff8008, #ffc837)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #ff8008, #ffc837, #ff8008)"
    },
    "Teal Tide": {
        "primary": "#1d976c",
        "secondary": "#93f9b9",
        "accent": "#1d976c",
        "background": "linear-gradient(135deg, #1d976c, #93f9b9, #1d976c, #93f9b9)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #1d976c, #93f9b9, #1d976c)"
    },
    "Grape Escape": {
        "primary": "#8e2de2",
        "secondary": "#4a00e0",
        "accent": "#8e2de2",
        "background": "linear-gradient(135deg, #8e2de2, #4a00e0, #8e2de2, #4a00e0)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #8e2de2, #4a00e0, #8e2de2)"
    },
    "Peach Perfect": {
        "primary": "#ff6a88",
        "secondary": "#ff99ac",
        "accent": "#ff6a88",
        "background": "linear-gradient(135deg, #ff6a88, #ff99ac, #ff6a88, #ff99ac)",
        "text": "#333333",
        "sidebar": "linear-gradient(135deg, #ff6a88, #ff99ac, #ff6a88)"
    }
}

# ============ 100+ WALLPAPERS ============
WALLPAPERS = {
    "None": "",
    "Misty Mountains": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=2400",
    "Sunset Beach": "https://images.unsplash.com/photo-1507525425510-56b1e2d6c4f2?w=2400",
    "Forest Path": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=2400",
    "Aurora Borealis": "https://images.unsplash.com/photo-1483347756197-71ef80e95f73?w=2400",
    "Desert Dunes": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=2400",
    "Waterfall": "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=2400",
    "Lake Reflection": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=2400",
    "Autumn Forest": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=2400",
    "Snow Mountain": "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=2400",
    "Tropical Beach": "https://images.unsplash.com/photo-1506953823976-52e1fdc0149a?w=2400",
    "Cherry Blossom": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=2400",
    "Grand Canyon": "https://images.unsplash.com/photo-1474044159687-1ee9f3a08322?w=2400",
    "Northern Lights": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=2400",
    "Green Valley": "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=2400",
    "Ocean Waves": "https://images.unsplash.com/photo-1439405326854-014607f694d7?w=2400",
    "Sunrise Field": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=2400",
    "Rainforest": "https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=2400",
    "Volcano": "https://images.unsplash.com/photo-1462332420958-a05d1e002413?w=2400",
    "Glacier": "https://images.unsplash.com/photo-1498855926480-d98e83099315?w=2400",
    "Canyon": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=2400",
    "Lavender Fields": "https://images.unsplash.com/photo-1500930240393-352b6b88c6b6?w=2400",
    "Bamboo Forest": "https://images.unsplash.com/photo-1448043552756-e747b7a2b9b8?w=2400",
    "Abstract Waves": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=2400",
    "Geometric Pattern": "https://images.unsplash.com/photo-1557683311-eac922347aa1?w=2400",
    "Color Splash": "https://images.unsplash.com/photo-1557683304-6733ba7e4d6f?w=2400",
    "Gradient Flow": "https://images.unsplash.com/photo-1557683316-973673baf926?w=2400",
    "Neon Lights": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469?w=2400",
    "City Skyline": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=2400",
    "Tokyo Night": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=2400",
    "New York": "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?w=2400",
    "Milky Way": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=2400",
    "Galaxy": "https://images.unsplash.com/photo-1506703719100-f0b3c5fd7e5d?w=2400",
    "Nebula": "https://images.unsplash.com/photo-1543722530-d2c3201371e5?w=2400",
    "Stars": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=2400",
    "Planet Earth": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=2400",
    "Spring Blossoms": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=2400",
    "Summer Beach": "https://images.unsplash.com/photo-1507525425510-56b1e2d6c4f2?w=2400",
    "Autumn Leaves": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=2400",
    "Winter Snow": "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=2400",
    "Rainbow": "https://images.unsplash.com/photo-1511300636408-a63a89df3482?w=2400",
    "Sunset": "https://images.unsplash.com/photo-1506815444479-bfdb1e96c566?w=2400"
}

def get_theme_css(theme_name, wallpaper=None):
    theme = THEMES.get(theme_name, THEMES["Sunrise Glow"])
    wallpaper_url = WALLPAPERS.get(wallpaper, "") if wallpaper else ""
    
    background_style = f"url('{wallpaper_url}') no-repeat center center fixed" if wallpaper_url else theme["background"]
    background_size = "cover" if wallpaper_url else "400% 400%"
    
    return f"""
    <style>
        body {{
            background: {background_style};
            background-size: {background_size};
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }}
        
        .stApp {{
            background: transparent !important;
        }}
        
        .main .block-container {{
            background: rgba(0, 0, 0, 0.65);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 215, 0, 0.4);
        }}
        
        section[data-testid="stSidebar"] {{
            background: {theme["sidebar"]};
            background-size: 300% 300%;
            animation: golden-shimmer 8s ease infinite;
            border-right: 2px solid rgba(255, 215, 0, 0.4);
        }}
        
        section[data-testid="stSidebar"] > div {{
            background: rgba(0, 0, 0, 0.3);
        }}
        
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] div {{
            color: #FFD700 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
            font-weight: 600;
        }}
        
        .golden-card {{
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(10px);
            border-left: 6px solid #FFD700;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            color: white;
        }}
        
        .stButton button {{
            background: linear-gradient(135deg, #FFD700, #DAA520);
            color: black;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }}
        
        .stButton button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
        }}
        
        .performance-excellent {{
            background: #00ff00;
            color: black;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
        }}
        
        .performance-good {{
            background: #00ffff;
            color: black;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
        }}
        
        .performance-average {{
            background: #ffff00;
            color: black;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
        }}
        
        .performance-needs-improvement {{
            background: #ff4444;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
        }}
        
        .chat-container {{
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            border: 1px solid #FFD700;
        }}
        
        .chat-bubble {{
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid #FFD700;
            border-radius: 20px;
            padding: 10px 15px;
            margin: 5px;
            max-width: 70%;
        }}
        
        .chat-message-sent {{
            text-align: right;
        }}
        
        .chat-message-received {{
            text-align: left;
        }}
        
        .school-header {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid #FFD700;
            border-radius: 12px;
            padding: 10px;
            text-align: center;
        }}
        
        .profile-card {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid #FFD700;
            border-radius: 12px;
            padding: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        @keyframes golden-shimmer {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
    </style>
    """

def get_subjects_for_grade(grade):
    if "Grade" in grade and any(str(i) in grade for i in range(1, 7)):
        return PRIMARY_SUBJECTS
    elif "Grade" in grade and any(str(i) in grade for i in range(7, 10)):
        return JUNIOR_SECONDARY_SUBJECTS
    elif "Form" in grade:
        subjects = []
        for category, subj_list in SENIOR_SECONDARY_SUBJECTS.items():
            subjects.extend(subj_list)
        return subjects
    else:
        return PRIMARY_SUBJECTS

# ============ CODE GENERATOR ============
def generate_id(prefix, length=8):
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f"{prefix}{random_part}"

def generate_school_code():
    chars = string.ascii_uppercase + string.digits
    return 'SCH' + ''.join(random.choices(chars, k=6))

def generate_class_code():
    return 'CLS' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_group_code():
    return 'GRP' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_admission_number():
    year = datetime.now().strftime("%y")
    random_num = ''.join(random.choices(string.digits, k=4))
    return f"ADM/{year}/{random_num}"

def generate_teacher_code():
    dept = random.choice(['MATH', 'ENG', 'SCI', 'SOC', 'CRE', 'BUS', 'TECH'])
    num = ''.join(random.choices(string.digits, k=3))
    return f"{dept}{num}"

def generate_book_id():
    return 'BOK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_transaction_id():
    return 'TRN' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_call_id():
    return 'CAL' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_notification_id():
    return 'NOT' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_request_id():
    return 'REQ' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# ============ DATA STORAGE ============
DATA_DIR = Path("school_data")
DATA_DIR.mkdir(exist_ok=True)

SCHOOLS_FILE = DATA_DIR / "all_schools.json"

def load_all_schools():
    if SCHOOLS_FILE.exists():
        with open(SCHOOLS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_all_schools(schools):
    with open(SCHOOLS_FILE, 'w') as f:
        json.dump(schools, f, indent=2)

def load_school_data(school_code, filename, default):
    if not school_code:
        return default
    filepath = DATA_DIR / f"{school_code}_{filename}"
    if filepath.exists():
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return default
    return default

def save_school_data(school_code, filename, data):
    if school_code:
        with open(DATA_DIR / f"{school_code}_{filename}", 'w') as f:
            json.dump(data, f, indent=2)

def load_user_settings(school_code, user_email):
    settings = load_school_data(school_code, "user_settings.json", {})
    return settings.get(user_email, {"theme": "Sunrise Glow", "wallpaper": "None"})

def save_user_settings(school_code, user_email, settings):
    all_settings = load_school_data(school_code, "user_settings.json", {})
    all_settings[user_email] = settings
    save_school_data(school_code, "user_settings.json", all_settings)

# ============ NOTIFICATION SYSTEM ============
def create_notification(school_code, user_email, notification_type, title, message, data=None):
    notifications = load_school_data(school_code, "notifications.json", [])
    notification = {
        "id": generate_notification_id(),
        "user_email": user_email,
        "type": notification_type,
        "title": title,
        "message": message,
        "data": data or {},
        "read": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expires_at": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    }
    notifications.append(notification)
    save_school_data(school_code, "notifications.json", notifications)
    return notification

def mark_notification_read(school_code, notification_id):
    notifications = load_school_data(school_code, "notifications.json", [])
    for n in notifications:
        if n['id'] == notification_id:
            n['read'] = True
            break
    save_school_data(school_code, "notifications.json", notifications)

def get_unread_notifications_count(school_code, user_email):
    notifications = load_school_data(school_code, "notifications.json", [])
    return len([n for n in notifications if n['user_email'] == user_email and not n['read']])

def get_user_notifications(school_code, user_email, include_read=False):
    notifications = load_school_data(school_code, "notifications.json", [])
    user_notifications = [n for n in notifications if n['user_email'] == user_email]
    if not include_read:
        user_notifications = [n for n in user_notifications if not n['read']]
    return sorted(user_notifications, key=lambda x: x['created_at'], reverse=True)

# ============ CALL SYSTEM ============
CALL_TYPES = {
    "audio": {"icon": "🎧", "name": "Audio Call"},
    "video": {"icon": "📹", "name": "Video Call"}
}

def initiate_call(school_code, caller_email, recipients, call_type, room_name=None):
    calls = load_school_data(school_code, "calls.json", [])
    call_id = generate_call_id()
    
    if not room_name:
        room_name = f"call_{call_id}"
    
    call = {
        "id": call_id,
        "caller": caller_email,
        "recipients": recipients,
        "call_type": call_type,
        "room_name": room_name,
        "status": "ringing",
        "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ended_at": None,
        "answered_by": [],
        "call_log": []
    }
    calls.append(call)
    save_school_data(school_code, "calls.json", calls)
    
    users = load_school_data(school_code, "users.json", [])
    caller = next((u for u in users if u['email'] == caller_email), None)
    caller_name = caller['fullname'] if caller else caller_email
    
    for recipient in recipients:
        create_notification(
            school_code,
            recipient,
            "incoming_call",
            f"{CALL_TYPES[call_type]['icon']} Incoming {call_type.title()} Call",
            f"{caller_name} is calling you",
            {"call_id": call_id, "caller": caller_email, "call_type": call_type, "room_name": room_name}
        )
    
    return call

def answer_call(school_code, call_id, user_email):
    calls = load_school_data(school_code, "calls.json", [])
    for call in calls:
        if call['id'] == call_id:
            if call['status'] == 'ringing':
                call['status'] = 'active'
                call['answered_by'].append(user_email)
                save_school_data(school_code, "calls.json", calls)
                create_notification(
                    school_code,
                    call['caller'],
                    "call_answered",
                    "📞 Call Answered",
                    f"{user_email} answered your call",
                    {"call_id": call_id}
                )
                return True
    return False

def end_call(school_code, call_id, user_email):
    calls = load_school_data(school_code, "calls.json", [])
    for call in calls:
        if call['id'] == call_id:
            call['status'] = 'ended'
            call['ended_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_school_data(school_code, "calls.json", calls)
            return True
    return False

def get_active_calls(school_code, user_email):
    calls = load_school_data(school_code, "calls.json", [])
    active_calls = []
    for call in calls:
        if call['status'] in ['ringing', 'active']:
            if user_email in [call['caller']] + call['recipients']:
                active_calls.append(call)
    return active_calls

# ============ CHAT & FRIENDSHIP FUNCTIONS ============
def send_friend_request(school_code, from_email, to_email):
    requests = load_school_data(school_code, "friend_requests.json", [])
    if not any(r['from'] == from_email and r['to'] == to_email and r['status'] == 'pending' for r in requests):
        request_id = generate_request_id()
        requests.append({
            "id": request_id,
            "from": from_email,
            "to": to_email,
            "status": "pending",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save_school_data(school_code, "friend_requests.json", requests)
        
        users = load_school_data(school_code, "users.json", [])
        from_user = next((u for u in users if u['email'] == from_email), None)
        from_name = from_user['fullname'] if from_user else from_email
        
        create_notification(
            school_code,
            to_email,
            "friend_request",
            "🤝 New Friend Request",
            f"{from_name} sent you a friend request",
            {"request_id": request_id, "from": from_email}
        )
        return True
    return False

def accept_friend_request(school_code, request_id):
    requests = load_school_data(school_code, "friend_requests.json", [])
    friendships = load_school_data(school_code, "friendships.json", [])
    
    for req in requests:
        if req['id'] == request_id:
            req['status'] = 'accepted'
            friendships.append({
                "user1": min(req['from'], req['to']),
                "user2": max(req['from'], req['to']),
                "since": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            create_notification(
                school_code,
                req['from'],
                "friend_accepted",
                "✅ Friend Request Accepted",
                f"{req['to']} accepted your friend request",
                {"friend": req['to']}
            )
            break
    
    save_school_data(school_code, "friend_requests.json", requests)
    save_school_data(school_code, "friendships.json", friendships)

def decline_friend_request(school_code, request_id):
    requests = load_school_data(school_code, "friend_requests.json", [])
    for req in requests:
        if req['id'] == request_id:
            req['status'] = 'declined'
            break
    save_school_data(school_code, "friend_requests.json", requests)

def get_friends(school_code, user_email):
    friendships = load_school_data(school_code, "friendships.json", [])
    friends = []
    for f in friendships:
        if f['user1'] == user_email:
            friends.append(f['user2'])
        elif f['user2'] == user_email:
            friends.append(f['user1'])
    return friends

def get_pending_requests(school_code, user_email):
    requests = load_school_data(school_code, "friend_requests.json", [])
    return [r for r in requests if r['to'] == user_email and r['status'] == 'pending']

def send_message(school_code, sender_email, recipient_email, message, attachment=None):
    messages = load_school_data(school_code, "messages.json", [])
    message_id = generate_id("MSG")
    messages.append({
        "id": message_id,
        "sender": sender_email,
        "recipient": recipient_email,
        "message": message,
        "attachment": attachment,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read": False,
        "deleted": False,
        "deleted_by": [],
        "conversation_id": f"{min(sender_email, recipient_email)}_{max(sender_email, recipient_email)}"
    })
    save_school_data(school_code, "messages.json", messages)
    
    users = load_school_data(school_code, "users.json", [])
    sender = next((u for u in users if u['email'] == sender_email), None)
    sender_name = sender['fullname'] if sender else sender_email
    
    create_notification(
        school_code,
        recipient_email,
        "new_message",
        "💬 New Message",
        f"{sender_name}: {message[:50]}..." if len(message) > 50 else message,
        {"message_id": message_id, "sender": sender_email}
    )
    
    return message_id

def get_conversation_messages(school_code, user_email, other_email):
    messages = load_school_data(school_code, "messages.json", [])
    conv_id = f"{min(user_email, other_email)}_{max(user_email, other_email)}"
    conv_msgs = [m for m in messages if m['conversation_id'] == conv_id and not m.get('deleted', False)]
    
    filtered_msgs = []
    for msg in conv_msgs:
        if user_email not in msg.get('deleted_by', []):
            filtered_msgs.append(msg)
    
    return sorted(filtered_msgs, key=lambda x: x['timestamp'])

def get_unread_count(user_email, school_code):
    messages = load_school_data(school_code, "messages.json", [])
    return len([m for m in messages if m['recipient'] == user_email and not m.get('read', False) and not m.get('deleted', False)])

# ============ GROUP CHAT FUNCTIONS ============
def create_group_chat(school_code, group_name, created_by, members):
    group_chats = load_school_data(school_code, "group_chats.json", [])
    group_chat = {
        "id": generate_id("GPC"),
        "name": group_name,
        "created_by": created_by,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "members": members,
        "messages": [],
        "admins": [created_by]
    }
    group_chats.append(group_chat)
    save_school_data(school_code, "group_chats.json", group_chats)
    
    users = load_school_data(school_code, "users.json", [])
    creator = next((u for u in users if u['email'] == created_by), None)
    creator_name = creator['fullname'] if creator else created_by
    
    for member in members:
        if member != created_by:
            create_notification(
                school_code,
                member,
                "group_created",
                "👥 Added to Group",
                f"{creator_name} added you to '{group_name}'",
                {"group_id": group_chat['id']}
            )
    
    return group_chat['id']

def send_group_message(school_code, group_id, sender_email, message, attachment=None):
    group_chats = load_school_data(school_code, "group_chats.json", [])
    message_id = generate_id("GPM")
    
    for group in group_chats:
        if group['id'] == group_id:
            group['messages'].append({
                "id": message_id,
                "sender": sender_email,
                "message": message,
                "attachment": attachment,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "read_by": [sender_email],
                "deleted": False
            })
            break
    
    save_school_data(school_code, "group_chats.json", group_chats)

def get_user_groups(school_code, user_email):
    groups = load_school_data(school_code, "groups.json", [])
    group_chats = load_school_data(school_code, "group_chats.json", [])
    user_groups = []
    
    for group in groups:
        if user_email in group.get('members', []):
            user_groups.append({
                "id": group['code'],
                "name": group['name'],
                "type": "regular",
                "members": group.get('members', [])
            })
    
    for chat in group_chats:
        if user_email in chat.get('members', []):
            user_groups.append({
                "id": chat['id'],
                "name": chat['name'],
                "type": "chat",
                "members": chat.get('members', [])
            })
    
    return user_groups

# ============ ATTACHMENT FUNCTIONS ============
def save_attachment(uploaded_file):
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        b64 = base64.b64encode(bytes_data).decode()
        return {
            "name": uploaded_file.name,
            "type": uploaded_file.type,
            "data": b64,
            "size": len(bytes_data)
        }
    return None

def display_attachment(attachment):
    if attachment:
        file_ext = attachment['name'].split('.')[-1].lower()
        if file_ext in ['jpg', 'jpeg', 'png', 'gif']:
            st.image(f"data:{attachment['type']};base64,{attachment['data']}", width=200)
        else:
            st.markdown(f"📎 [{attachment['name']}]")

# ============ SCHOOL MANAGEMENT FUNCTIONS ============
def calculate_student_performance(grades, student_email):
    student_grades = [g for g in grades if g['student_email'] == student_email]
    if not student_grades:
        return {"average": 0, "subjects": {}, "rank": "N/A", "subject_details": []}
    
    subjects = {}
    subject_details = []
    total = 0
    for grade in student_grades:
        subjects[grade['subject']] = grade['score']
        subject_details.append({
            "subject": grade['subject'],
            "score": grade['score'],
            "term": grade['term'],
            "year": grade['year']
        })
        total += grade['score']
    
    avg = total / len(student_grades)
    
    if avg >= 80:
        rank = "Excellent"
    elif avg >= 70:
        rank = "Good"
    elif avg >= 50:
        rank = "Average"
    else:
        rank = "Needs Improvement"
    
    return {"average": round(avg, 2), "subjects": subjects, "rank": rank, "subject_details": subject_details}

def add_academic_record(school_code, student_email, subject, score, term, year, teacher_email, class_name=None):
    grades = load_school_data(school_code, "academic_records.json", [])
    grades.append({
        "id": generate_id("GRD"),
        "student_email": student_email,
        "subject": subject,
        "score": score,
        "term": term,
        "year": year,
        "teacher_email": teacher_email,
        "class_name": class_name,
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    save_school_data(school_code, "academic_records.json", grades)

# ============ LIBRARY FUNCTIONS ============
def add_book(school_code, title, author, book_type, quantity, isbn=None, publisher=None, year=None):
    books = load_school_data(school_code, "library_books.json", [])
    book = {
        "id": generate_book_id(),
        "title": title,
        "author": author,
        "type": book_type,
        "quantity": quantity,
        "available": quantity,
        "isbn": isbn,
        "publisher": publisher,
        "year": year,
        "added_by": st.session_state.user['email'],
        "added_date": datetime.now().strftime("%Y-%m-%d")
    }
    books.append(book)
    save_school_data(school_code, "library_books.json", books)
    return book['id']

def add_library_member(school_code, user_email, member_type="student"):
    members = load_school_data(school_code, "library_members.json", [])
    if not any(m['email'] == user_email for m in members):
        members.append({
            "email": user_email,
            "member_type": member_type,
            "joined_date": datetime.now().strftime("%Y-%m-%d"),
            "borrowed_books": [],
            "status": "active"
        })
        save_school_data(school_code, "library_members.json", members)

def borrow_book(school_code, user_email, book_id, due_days=14):
    books = load_school_data(school_code, "library_books.json", [])
    transactions = load_school_data(school_code, "library_transactions.json", [])
    members = load_school_data(school_code, "library_members.json", [])
    
    book = next((b for b in books if b['id'] == book_id), None)
    if not book or book['available'] <= 0:
        return False, "Book not available"
    
    member = next((m for m in members if m['email'] == user_email), None)
    if not member:
        add_library_member(school_code, user_email)
        members = load_school_data(school_code, "library_members.json", [])
        member = next((m for m in members if m['email'] == user_email), None)
    
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=due_days)
    
    transaction = {
        "id": generate_transaction_id(),
        "book_id": book_id,
        "book_title": book['title'],
        "user_email": user_email,
        "borrow_date": borrow_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "return_date": None,
        "status": "borrowed"
    }
    transactions.append(transaction)
    
    book['available'] -= 1
    
    member.setdefault('borrowed_books', []).append({
        "book_id": book_id,
        "transaction_id": transaction['id'],
        "borrow_date": borrow_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "status": "borrowed"
    })
    
    save_school_data(school_code, "library_books.json", books)
    save_school_data(school_code, "library_transactions.json", transactions)
    save_school_data(school_code, "library_members.json", members)
    
    return True, "Book borrowed successfully"

def return_book(school_code, transaction_id):
    books = load_school_data(school_code, "library_books.json", [])
    transactions = load_school_data(school_code, "library_transactions.json", [])
    members = load_school_data(school_code, "library_members.json", [])
    
    transaction = next((t for t in transactions if t['id'] == transaction_id), None)
    if not transaction or transaction['status'] != 'borrowed':
        return False, "Invalid transaction"
    
    transaction['return_date'] = datetime.now().strftime("%Y-%m-%d")
    transaction['status'] = 'returned'
    
    book = next((b for b in books if b['id'] == transaction['book_id']), None)
    if book:
        book['available'] += 1
    
    member = next((m for m in members if m['email'] == transaction['user_email']), None)
    if member:
        for b in member.get('borrowed_books', []):
            if b['transaction_id'] == transaction_id:
                b['status'] = 'returned'
                break
    
    save_school_data(school_code, "library_books.json", books)
    save_school_data(school_code, "library_transactions.json", transactions)
    save_school_data(school_code, "library_members.json", members)
    
    return True, "Book returned successfully"

# ============ SESSION STATE ============
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_school' not in st.session_state:
    st.session_state.current_school = None
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'menu_index' not in st.session_state:
    st.session_state.menu_index = 0
if 'chat_with' not in st.session_state:
    st.session_state.chat_with = None
if 'group_chat_with' not in st.session_state:
    st.session_state.group_chat_with = None
if 'main_nav' not in st.session_state:
    st.session_state.main_nav = 'School Community'
if 'selected_class' not in st.session_state:
    st.session_state.selected_class = None
if 'theme' not in st.session_state:
    st.session_state.theme = "Sunrise Glow"
if 'wallpaper' not in st.session_state:
    st.session_state.wallpaper = "None"
if 'viewing_student' not in st.session_state:
    st.session_state.viewing_student = None
if 'current_feature' not in st.session_state:
    st.session_state.current_feature = None
if 'current_call' not in st.session_state:
    st.session_state.current_call = None
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

# ============ RENDER FUNCTIONS ============
def render_notifications():
    if st.session_state.user and st.session_state.current_school:
        unread_count = get_unread_notifications_count(
            st.session_state.current_school['code'],
            st.session_state.user['email']
        )
        
        with st.sidebar.expander(f"🔔 Notifications {f'({unread_count})' if unread_count > 0 else ''}", expanded=False):
            notifications = get_user_notifications(
                st.session_state.current_school['code'],
                st.session_state.user['email'],
                include_read=False
            )
            
            if notifications:
                for notification in notifications[:5]:
                    st.markdown(f"**{notification['title']}**")
                    st.markdown(f"<small>{notification['message']}</small>", unsafe_allow_html=True)
                    if st.button("✓", key=f"read_{notification['id']}"):
                        mark_notification_read(
                            st.session_state.current_school['code'],
                            notification['id']
                        )
                        st.rerun()
                    st.divider()
            else:
                st.info("No new notifications")

def render_video_meeting():
    st.markdown("### 🎥 Video/Audio Calls")
    
    tab1, tab2 = st.tabs(["📞 Make a Call", "📋 Active Calls"])
    
    with tab1:
        st.markdown("#### Start a Call")
        
        if st.session_state.user and st.session_state.current_school:
            users = load_school_data(st.session_state.current_school['code'], "users.json", [])
            all_users = [u for u in users if u['email'] != st.session_state.user['email']]
            
            col1, col2 = st.columns(2)
            
            with col1:
                call_type = st.radio("Call Type", ["🎧 Audio Call", "📹 Video Call"])
                actual_call_type = "audio" if "Audio" in call_type else "video"
            
            with col2:
                selected_users = st.multiselect(
                    "Select recipients",
                    [f"{u['fullname']} ({u['role']})" for u in all_users]
                )
                recipients = [u.split('(')[1].rstrip(')').strip() for u in selected_users]
            
            if st.button("🚀 Start Call", use_container_width=True, type="primary"):
                if recipients:
                    call = initiate_call(
                        st.session_state.current_school['code'],
                        st.session_state.user['email'],
                        recipients,
                        actual_call_type
                    )
                    st.success(f"Call initiated! Ringing {len(recipients)} participant(s)...")
                    st.session_state.current_call = call
                    st.rerun()
                else:
                    st.error("Please select at least one recipient")
    
    with tab2:
        st.markdown("#### Active Calls")
        
        if st.session_state.user and st.session_state.current_school:
            active_calls = get_active_calls(
                st.session_state.current_school['code'],
                st.session_state.user['email']
            )
            
            if active_calls:
                for call in active_calls:
                    with st.container():
                        call_icon = "🎧" if call['call_type'] == 'audio' else "📹"
                        st.markdown(f"**{call_icon} Call with {len(call['recipients'])} participants**")
                        st.markdown(f"Status: {call['status'].title()}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Join", key=f"join_{call['id']}", use_container_width=True):
                                if call['status'] == 'ringing':
                                    answer_call(
                                        st.session_state.current_school['code'],
                                        call['id'],
                                        st.session_state.user['email']
                                    )
                                st.session_state.current_call = call
                                st.rerun()
                        with col2:
                            if st.button("End", key=f"end_{call['id']}", use_container_width=True):
                                end_call(
                                    st.session_state.current_school['code'],
                                    call['id'],
                                    st.session_state.user['email']
                                )
                                st.rerun()
                        st.divider()
            else:
                st.info("No active calls")

def render_call_room():
    if 'current_call' not in st.session_state:
        return
    
    call = st.session_state.current_call
    
    st.markdown(f"### {call['room_name']}")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        call_icon = "🎧" if call['call_type'] == 'audio' else "📹"
        st.markdown(f"## {call_icon} {call['call_type'].title()} Call")
        
        st.markdown("#### Participants")
        users = load_school_data(st.session_state.current_school['code'], "users.json", [])
        all_participants = [call['caller']] + call.get('recipients', [])
        
        for participant in all_participants:
            user = next((u for u in users if u['email'] == participant), None)
            name = user['fullname'] if user else participant
            if participant in call.get('answered_by', []):
                st.markdown(f"🟢 {name} (Connected)")
            else:
                st.markdown(f"🔴 {name} (Ringing...)")
        
        if st.button("🚫 End Call", use_container_width=True, type="primary"):
            end_call(
                st.session_state.current_school['code'],
                call['id'],
                st.session_state.user['email']
            )
            del st.session_state.current_call
            st.rerun()
    
    with col2:
        st.markdown("#### Call Info")
        st.markdown(f"**Type:** {call['call_type'].title()}")
        st.markdown(f"**Started:** {call['started_at']}")
        st.markdown(f"**Status:** {call['status'].title()}")

def render_selected_feature():
    if 'current_feature' in st.session_state and st.session_state.current_feature:
        if st.session_state.current_feature == 'video':
            if 'current_call' in st.session_state and st.session_state.current_call:
                render_call_room()
            else:
                render_video_meeting()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("← Back to Dashboard", key="back_to_dash", use_container_width=True):
                st.session_state.current_feature = None
                st.session_state.current_call = None
                st.rerun()
        return True
    return False

def render_enhanced_sidebar_additions():
    if st.session_state.user:
        st.sidebar.divider()
        render_notifications()
        
        st.sidebar.divider()
        st.sidebar.markdown("### 🆕 Quick Access")
        
        if st.sidebar.button("🎥 Video/Audio Calls", key="nav_video", use_container_width=True):
            st.session_state.current_feature = 'video'
            st.rerun()

# ============ MAIN APP ============

# Load user settings if logged in
if st.session_state.user and st.session_state.current_school:
    settings = load_user_settings(st.session_state.current_school['code'], st.session_state.user['email'])
    st.session_state.theme = settings.get("theme", "Sunrise Glow")
    st.session_state.wallpaper = settings.get("wallpaper", "None")

# Apply theme CSS
st.markdown(get_theme_css(st.session_state.theme, st.session_state.wallpaper), unsafe_allow_html=True)

# Welcome Page
if st.session_state.page == 'welcome':
    st.markdown('<h1>✨ School Community Hub ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #FFD700; font-size: 1.2rem;">Connect • Collaborate • Manage • Shine</p>', unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏫 School Community", key="nav_community", use_container_width=True):
            st.session_state.main_nav = 'School Community'
    
    with col2:
        if st.button("📊 School Management", key="nav_management", use_container_width=True):
            st.session_state.main_nav = 'School Management'
    
    with col3:
        if st.button("👤 Personal Dashboard", key="nav_personal", use_container_width=True):
            st.session_state.main_nav = 'Personal Dashboard'
    
    st.divider()
    
    if st.session_state.main_nav == 'School Community':
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["👑 Admin Login", "🏫 Create School", "👨‍🏫 Teacher", "👨‍🎓 Student", "👪 Guardian"])
        
        with tab1:
            with st.form("admin_login"):
                st.subheader("Admin Login")
                school_code = st.text_input("School Code")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Login", use_container_width=True):
                    if school_code and email and password:
                        all_schools = load_all_schools()
                        if school_code in all_schools:
                            school = all_schools[school_code]
                            users = load_school_data(school_code, "users.json", [])
                            hashed = hashlib.sha256(password.encode()).hexdigest()
                            for u in users:
                                if u['email'] == email and u['password'] == hashed and u['role'] == 'admin':
                                    st.session_state.current_school = school
                                    st.session_state.user = u
                                    st.session_state.page = 'dashboard'
                                    st.rerun()
                            st.error("Invalid credentials")
                        else:
                            st.error("School not found")
        
        with tab2:
            with st.form("create_school"):
                st.subheader("Create New School")
                school_name = st.text_input("School Name")
                admin_name = st.text_input("Your Full Name")
                admin_email = st.text_input("Your Email")
                password = st.text_input("Password", type="password")
                confirm = st.text_input("Confirm Password", type="password")
                
                if st.form_submit_button("Create School", use_container_width=True):
                    if school_name and admin_email and password:
                        if password != confirm:
                            st.error("Passwords don't match")
                        else:
                            all_schools = load_all_schools()
                            code = generate_school_code()
                            while code in all_schools:
                                code = generate_school_code()
                            
                            new_school = {
                                "code": code,
                                "name": school_name,
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "admin_email": admin_email,
                                "admin_name": admin_name
                            }
                            all_schools[code] = new_school
                            save_all_schools(all_schools)
                            
                            users = [{
                                "user_id": generate_id("USR"),
                                "email": admin_email,
                                "fullname": admin_name,
                                "password": hashlib.sha256(password.encode()).hexdigest(),
                                "role": "admin",
                                "joined": datetime.now().strftime("%Y-%m-%d"),
                                "school_code": code
                            }]
                            save_school_data(code, "users.json", users)
                            
                            save_school_data(code, "classes.json", [])
                            save_school_data(code, "groups.json", [])
                            save_school_data(code, "announcements.json", [])
                            save_school_data(code, "messages.json", [])
                            save_school_data(code, "calls.json", [])
                            save_school_data(code, "notifications.json", [])
                            save_school_data(code, "library_books.json", [])
                            save_school_data(code, "library_members.json", [])
                            save_school_data(code, "library_transactions.json", [])
                            save_school_data(code, "academic_records.json", [])
                            
                            st.session_state.current_school = new_school
                            st.session_state.user = users[0]
                            st.session_state.page = 'dashboard'
                            st.success(f"✅ School Created! Code: **{code}**")
                            st.rerun()
        
        with tab3:
            with st.form("teacher_login"):
                st.subheader("Teacher Login")
                school_code = st.text_input("School Code")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Login", use_container_width=True):
                    if school_code and email and password:
                        all_schools = load_all_schools()
                        if school_code in all_schools:
                            school = all_schools[school_code]
                            users = load_school_data(school_code, "users.json", [])
                            hashed = hashlib.sha256(password.encode()).hexdigest()
                            for u in users:
                                if u['email'] == email and u['password'] == hashed and u['role'] == 'teacher':
                                    st.session_state.current_school = school
                                    st.session_state.user = u
                                    st.session_state.page = 'dashboard'
                                    st.rerun()
                            st.error("Invalid credentials")
                        else:
                            st.error("School not found")
        
        with tab4:
            with st.form("student_login"):
                st.subheader("Student Login")
                school_code = st.text_input("School Code")
                admission = st.text_input("Admission Number")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Login", use_container_width=True):
                    if school_code and admission and password:
                        all_schools = load_all_schools()
                        if school_code in all_schools:
                            school = all_schools[school_code]
                            users = load_school_data(school_code, "users.json", [])
                            hashed = hashlib.sha256(password.encode()).hexdigest()
                            for u in users:
                                if u.get('admission_number') == admission and u['password'] == hashed and u['role'] == 'student':
                                    st.session_state.current_school = school
                                    st.session_state.user = u
                                    st.session_state.page = 'dashboard'
                                    st.rerun()
                            st.error("Invalid credentials")
                        else:
                            st.error("School not found")
        
        with tab5:
            with st.form("guardian_login"):
                st.subheader("Guardian Login")
                school_code = st.text_input("School Code")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Login", use_container_width=True):
                    if school_code and email and password:
                        all_schools = load_all_schools()
                        if school_code in all_schools:
                            school = all_schools[school_code]
                            users = load_school_data(school_code, "users.json", [])
                            hashed = hashlib.sha256(password.encode()).hexdigest()
                            for u in users:
                                if u['email'] == email and u['password'] == hashed and u['role'] == 'guardian':
                                    st.session_state.current_school = school
                                    st.session_state.user = u
                                    st.session_state.page = 'dashboard'
                                    st.rerun()
                            st.error("Invalid credentials")
                        else:
                            st.error("School not found")

# Dashboard
elif st.session_state.page == 'dashboard' and st.session_state.current_school and st.session_state.user:
    school = st.session_state.current_school
    user = st.session_state.user
    school_code = school['code']
    
    users = load_school_data(school_code, "users.json", [])
    classes = load_school_data(school_code, "classes.json", [])
    groups = load_school_data(school_code, "groups.json", [])
    announcements = load_school_data(school_code, "announcements.json", [])
    unread_count = get_unread_count(user['email'], school_code)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div class="school-header">
            <h2>{school['name']}</h2>
            <div class="school-code">
                <code>{school['code']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        
        if user.get('profile_pic'):
            st.image(user['profile_pic'], width=50)
        else:
            emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓" if user['role'] == 'student' else "👪"
            st.markdown(f"<h1 style='font-size: 2rem;'>{emoji}</h1>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="color: #FFD700;">
            <strong>{user['fullname']}</strong><br>
            <span>{user['role'].upper()}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        options = ["Dashboard", "Announcements", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}"]
        
        if user['role'] == 'admin':
            options.extend(["Users", "Classes", "Groups", "Library", "Settings"])
        elif user['role'] == 'teacher':
            options.extend(["My Classes", "Groups", "Library", "Settings"])
        elif user['role'] == 'student':
            options.extend(["My Classes", "Groups", "Library", "Settings"])
        else:
            options.extend(["My Students", "Settings"])
        
        options.append("Profile")
        
        if st.session_state.menu_index >= len(options):
            st.session_state.menu_index = 0
        
        menu = st.radio("Navigation", options, index=st.session_state.menu_index, label_visibility="collapsed")
        st.session_state.menu_index = options.index(menu)
        
        st.divider()
        
        render_enhanced_sidebar_additions()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # Main content
    if render_selected_feature():
        pass
    
    elif menu == "Dashboard":
        st.markdown(f"<h2>Welcome, {user['fullname']}!</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Members", len(users))
        with col2:
            st.metric("Announcements", len(announcements))
        with col3:
            if user['role'] == 'student':
                st.metric("Classes", len([c for c in classes if user['email'] in c.get('students', [])]))
        
        if announcements:
            st.subheader("📢 Latest Announcements")
            for ann in announcements[-3:]:
                st.markdown(f"""
                <div class="golden-card">
                    <h4>{ann['title']}</h4>
                    <p><small>By {ann['author']} • {ann['date'][:16]}</small></p>
                    <p>{ann['content'][:100]}...</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif menu == "Announcements":
        st.markdown("<h2>📢 Announcements</h2>", unsafe_allow_html=True)
        
        if user['role'] in ['admin', 'teacher']:
            with st.expander("➕ New Announcement"):
                with st.form("new_announcement"):
                    title = st.text_input("Title")
                    content = st.text_area("Content")
                    
                    if st.form_submit_button("Post", use_container_width=True):
                        if title and content:
                            announcements.append({
                                "id": generate_id("ANN"),
                                "title": title,
                                "content": content,
                                "author": user['fullname'],
                                "author_email": user['email'],
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            save_school_data(school_code, "announcements.json", announcements)
                            st.success("Announcement posted!")
                            st.rerun()
        
        if announcements:
            for ann in reversed(announcements):
                st.markdown(f"""
                <div class="golden-card">
                    <h4>{ann['title']}</h4>
                    <p><small>By {ann['author']} • {ann['date'][:16]}</small></p>
                    <p>{ann['content']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No announcements yet")
    
    elif menu.startswith("Chat"):
        st.markdown("<h2>💬 Messages</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Chats")
            friends = get_friends(school_code, user['email'])
            
            if friends:
                for friend_email in friends:
                    friend = next((u for u in users if u['email'] == friend_email), None)
                    if friend:
                        if st.button(f"👤 {friend['fullname']}", key=f"chat_{friend_email}", use_container_width=True):
                            st.session_state.chat_with = friend_email
                            st.rerun()
            else:
                st.info("No friends yet")
            
            st.markdown("### Find Friends")
            other_users = [u for u in users if u['email'] != user['email'] and u['email'] not in friends]
            if other_users:
                for other in other_users[:5]:
                    if st.button(f"➕ {other['fullname']}", key=f"add_{other['email']}", use_container_width=True):
                        send_friend_request(school_code, user['email'], other['email'])
                        st.success("Friend request sent!")
                        st.rerun()
        
        with col2:
            if st.session_state.chat_with:
                other_email = st.session_state.chat_with
                other_user = next((u for u in users if u['email'] == other_email), None)
                
                if other_user:
                    st.markdown(f"### Chat with {other_user['fullname']}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("🎧 Audio Call", use_container_width=True):
                            call = initiate_call(
                                school_code,
                                user['email'],
                                [other_email],
                                "audio"
                            )
                            st.session_state.current_call = call
                            st.session_state.current_feature = 'video'
                            st.rerun()
                    
                    with col_b:
                        if st.button("📹 Video Call", use_container_width=True):
                            call = initiate_call(
                                school_code,
                                user['email'],
                                [other_email],
                                "video"
                            )
                            st.session_state.current_call = call
                            st.session_state.current_feature = 'video'
                            st.rerun()
                    
                    messages = get_conversation_messages(school_code, user['email'], other_email)
                    
                    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                    
                    for msg in messages:
                        is_sent = msg['sender'] == user['email']
                        sender_name = "You" if is_sent else other_user['fullname']
                        
                        st.markdown(f"""
                        <div class="chat-message-{'sent' if is_sent else 'received'}">
                            <div class="chat-bubble">
                                <strong>{sender_name}</strong><br>
                                {msg['message']}<br>
                                <small>{msg['timestamp'][:16]}</small>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.form("send_message", clear_on_submit=True):
                        message = st.text_area("Message", height=60, placeholder="Type a message...")
                        if st.form_submit_button("📤 Send", use_container_width=True):
                            if message:
                                send_message(school_code, user['email'], other_email, message, None)
                                st.rerun()
            else:
                st.info("Select a chat to start messaging")
    
    elif menu == "Settings":
        st.markdown("<h2>⚙️ Settings</h2>", unsafe_allow_html=True)
        
        st.subheader("Theme Selection")
        
        selected_theme = st.selectbox("Choose Theme", list(THEMES.keys()), 
                                     index=list(THEMES.keys()).index(st.session_state.theme))
        
        selected_wallpaper = st.selectbox("Choose Wallpaper", list(WALLPAPERS.keys()),
                                        index=list(WALLPAPERS.keys()).index(st.session_state.wallpaper))
        
        if st.button("💾 Save Theme", use_container_width=True):
            st.session_state.theme = selected_theme
            st.session_state.wallpaper = selected_wallpaper
            save_user_settings(school_code, user['email'], {
                "theme": selected_theme,
                "wallpaper": selected_wallpaper
            })
            st.success("Settings saved!")
            st.rerun()
    
    elif menu == "Profile":
        st.markdown("<h2>👤 My Profile</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if user.get('profile_pic'):
                st.image(user['profile_pic'], width=150)
            else:
                emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓" if user['role'] == 'student' else "👪"
                st.markdown(f"<h1 style='font-size: 5rem;'>{emoji}</h1>", unsafe_allow_html=True)
            
            pic = st.file_uploader("📸 Upload Photo", type=['png', 'jpg', 'jpeg'])
            if pic:
                img = Image.open(pic)
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                b64 = base64.b64encode(buffered.getvalue()).decode()
                for u in users:
                    if u['email'] == user['email']:
                        u['profile_pic'] = f"data:image/png;base64,{b64}"
                save_school_data(school_code, "users.json", users)
                user['profile_pic'] = f"data:image/png;base64,{b64}"
                st.rerun()
        
        with col2:
            with st.form("edit_profile"):
                name = st.text_input("Full Name", user['fullname'])
                phone = st.text_input("Phone", user.get('phone', ''))
                bio = st.text_area("Bio", user.get('bio', ''), height=100)
                
                if st.form_submit_button("💾 Update", use_container_width=True):
                    for u in users:
                        if u['email'] == user['email']:
                            u['fullname'] = name
                            u['phone'] = phone
                            u['bio'] = bio
                    save_school_data(school_code, "users.json", users)
                    user.update({'fullname': name, 'phone': phone, 'bio': bio})
                    st.success("Profile updated!")
                    st.rerun()

else:
    st.error("Something went wrong. Please restart.")
    if st.button("Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
