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
| 🏆 **College Leaderboard** | Inter-college XP rankings with podium display |
| 😂 **Meme Factory** | PIL-generated eco memes with 6 templates |
| 📦 **Eco Score** | Rate 40+ products on environmental impact (1-10 scale) |
| ♻️ **Waste Classifier** | Classify 50+ waste items with disposal instructions |
| 🎮 **Full Gamification** | XP, 30 levels, 15 badges, daily streaks |

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) Add Gemini API Key

Get a free key at: https://aistudio.google.com

Edit `config.py`:
```python
GEMINI_API_KEY = "your-api-key-here"
```

> **Note:** The app works perfectly without Gemini — it uses funny fallback responses!

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

- **Background:** Animated gradient mesh with 25 floating particles
- **Cards:** Glassmorphism with backdrop blur
- **Fonts:** Plus Jakarta Sans (headings) + DM Sans (body)
- **Colors:**
  - Terra Green: `#2ECC71`
  - Terra Dark: `#0D1F1A`
  - Terra Sky: `#7EC8E3`
  - Terra Yellow: `#F4C430`
  - Terra Accent: `#FF6B35`

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
