# Terra 2.0 🌍

> **Your planet needs a glow-up. Start here.**

A Gamified Environmental Education Platform built for Gen Z college students. Built with Python, Streamlit, SQLAlchemy 2.0, and optional Google Gemini AI.

![Python](https://img.shields.io/badge/Python-3.10+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌿 **Carbon Footprint Tracker** | 4-step wizard tracking transport, food, energy & shopping emissions with PDF reports |
| 🔥 **AI Roast My Lifestyle** | Gemini-powered Gen Z-style eco roasts with practical tips |
| 🃏 **Eco Swipe Game** | Tinder-style game with 50 eco habits — swipe right or left |
| 🏆 **College Leaderboard** | Inter-college XP rankings with podium display (gold/silver/bronze medals) |
| 😂 **Meme Factory** | PIL-generated eco memes with 6 templates |
| 📦 **Eco Score** | Rate 40+ products on environmental impact (1-10 scale) |
| ♻️ **Waste Classifier** | Classify 50+ waste items with disposal instructions |
| 🎮 **Full Gamification** | XP, 30 levels, 15 badges, daily streaks, level progress |
| 👤 **User Profile Dashboard** | Beautiful profile page with stats, badges, activity history |
| 🔐 **Session Persistence** | Stay logged in even after browser refresh |

---

## 🆕 Recent Updates (v2.1)

✅ **Warm Light Theme Redesign** — Switched from dark theme to beautiful warm beige/earth-tone color palette  
✅ **Session Persistence** — Authentication tokens in URL params ensure users stay logged in on refresh  
✅ **Profile Page Redesign** — Impressive hero card with level progress, activity summary, and badges display  
✅ **Enhanced Sidebar** — User info card now shows user ID, level, and XP progress bar  
✅ **Accent Colors** — Added terracotta, gold, and green accent colors for visual hierarchy  
✅ **Beautiful Login Page** — Centered card design with smooth tab-based authentication forms  
✅ **Form Element Styling** — Improved selectbox, input, and label visibility with proper hover states  
✅ **Feature Card Navigation** — All 8 feature cards now navigate smoothly with proper routing  

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) Add Gemini API Key

Get a free key at: https://aistudio.google.com

Set the environment variable (do NOT add to config.py):

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root and add:
```
GEMINI_API_KEY=your-api-key-here
```

> **Note:** The app works perfectly without Gemini — it uses funny fallback responses! Never commit your API key to git.

### 3. Run the App

```bash
streamlit run app.py
```

The database (`terra2.db`) is created automatically on first run. No manual setup needed.

---

## 📁 Project Structure

```
terra2/
├── app.py                    # Main entry point
├── config.py                 # All configuration, constants, game data
├── requirements.txt          # Dependencies
├── README.md                 # This file
│
├── database/
│   ├── __init__.py
│   └── db_setup.py           # SQLAlchemy 2.0 models & engine
│
├── modules/
│   ├── __init__.py
│   ├── auth.py               # Authentication (bcrypt)
│   ├── gamification.py       # XP, levels, badges
│   ├── carbon_tracker.py     # Emission calculations & PDF reports
│   ├── swipe_game.py         # Eco swipe game logic
│   ├── ai_roast.py           # Gemini AI integration
│   ├── meme_generator.py     # PIL-based meme creation
│   ├── eco_score.py          # Product eco scoring
│   ├── waste_classifier.py   # Waste classification
│   └── leaderboard.py        # College rankings
│
├── api/
│   ├── __init__.py
│   └── climate_api.py        # Open-Meteo weather & AQI
│
├── ui/
│   ├── __init__.py
│   ├── styles.py             # Global CSS (glassmorphism, particles)
│   ├── components.py         # Reusable UI components
│   └── pages/
│       ├── __init__.py
│       ├── home.py           # Dashboard
│       ├── carbon.py         # Carbon tracker
│       ├── roast.py          # AI roast
│       ├── swipe.py          # Swipe game
│       ├── leaderboard_page.py
│       ├── meme.py           # Meme factory
│       ├── eco_score_page.py
│       ├── waste.py          # Waste classifier
│       └── profile.py        # User profile
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_carbon.py
│   └── test_gamification.py
│
└── reports/                  # Generated PDF reports
```

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

Or individually:
```bash
python -m unittest tests.test_carbon -v
python -m unittest tests.test_gamification -v
python -m unittest tests.test_auth -v
```

---

## 🎨 Design System

**Theme:** Warm Light Theme (Beige & Earth-tone)

- **Primary Background:** Warm off-white `#FAF7F2`
- **Secondary Background:** Light beige `#F2EDE4`
- **Cards:** Pure white `#FFFFFF` with subtle borders
- **Fonts:** Plus Jakarta Sans (headings) + Inter (body)

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Deep Forest Green | `#3D7A5E` | Primary buttons, active states |
| Sage Green | `#6BAF8A` | Progress bars, success states |
| Warm Terracotta | `#C8794A` | Streak badges, 3rd place medals |
| Warm Gold | `#D4A853` | Level badges, 1st place medals |
| Silver | `#B0B0B0` | 2nd place medals |
| Primary Text | `#2C2C2C` | Headings, main content |
| Secondary Text | `#5C5C5C` | Body text, descriptions |
| Muted Text | `#9A9A9A` | Tertiary info, hints |
| Borders | `#E8E0D5` | Card and input borders |

### Key UI Features

- **Beautiful Login/Signup Page:** Centered card design with tab-based forms
- **Responsive Sidebar:** User profile card with avatar, level, and XP progress
- **Session Persistence:** Stay logged in even after browser refresh
- **Impressive Profile Dashboard:** Hero card, activity summary, badges, user info
- **Accent Colors:** Terracotta, gold, and green accents for visual hierarchy

---

## 🏗️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Streamlit 1.32** | Web framework |
| **SQLAlchemy 2.0** | ORM & database |
| **SQLite** | Database engine |
| **bcrypt** | Password hashing |
| **Plotly** | Interactive charts |
| **ReportLab** | PDF generation |
| **Pillow** | Meme image generation |
| **Google Gemini** | AI-powered roasts (optional) |
| **Open-Meteo** | Weather & AQI data (free, no key) |

---

## 📝 Emission Factors

All emission factors are based on published research:
- Transport: DEFRA 2023 emission factors
- Food: Our World in Data lifecycle analysis
- Energy: India Central Electricity Authority (0.82 kg CO2/kWh)
- India average: 1.9 tonnes/year ≈ 5.2 kg/day

---

## 📜 License

MIT License — feel free to use, modify, and share!

---

**Built with 💚 for the planet.**
