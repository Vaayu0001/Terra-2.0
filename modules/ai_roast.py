"""
Terra 2.0 — AI Roast Module
Uses Google Gemini for Gen Z-style eco lifestyle roasts.
Falls back to hardcoded roasts if API is unavailable.
"""

import random

import google.generativeai as genai

from config import GEMINI_API_KEY

FALLBACK_ROASTS = [
    "Bestie, your carbon footprint is giving main character energy — in a climate disaster movie. "
    "No cap, the planet is NOT slay-ing because of choices like yours. 💀 "
    "But lowkey, you can do better! Here's your redemption arc:\n\n"
    "1) Try public transport — your solo car rides are giving delulu vibes\n"
    "2) Eat less meat — even one meatless day is a serve\n"
    "3) Shorter showers — 5 mins max, bestie, the ocean is NOT your playlist venue",

    "Oof, the audacity. 😭 Your lifestyle is giving 'I learned nothing from climate class' vibes. "
    "It's giving chaos. It's giving emissions. It's giving carbon MAIN CHARACTER. "
    "But hey, every eco-villain has a redemption arc. Here's yours:\n\n"
    "1) Carry a reusable bottle — those plastic ones are cheugy\n"
    "2) Turn off lights when you leave — the bulbs don't need an audience\n"
    "3) Eat more plants — your gut (and the planet) will thank you",

    "POV: You just asked to be eco-roasted and your footprint said 'hold my plastic cup'. 🥤 "
    "The planet is literally crying rn. Not the flex you thought it was, bestie. "
    "But real talk, small changes hit different:\n\n"
    "1) Cycle or walk short distances — legs exist for a reason\n"
    "2) Set your AC to 24°C — frostbite isn't aesthetic\n"
    "3) Buy second-hand — thrifting is the ultimate slay",

    "Not you thinking your lifestyle is sustainable 💀 The carbon footprint is giving BIG energy — "
    "and not the good kind. You're basically the final boss of climate change rn. "
    "But we believe in character development:\n\n"
    "1) Unplug devices when not charging — phantom load is real\n"
    "2) Try meatless Mondays — your tastebuds will survive, promise\n"
    "3) Compost your food waste — turning trash into treasure is peak",

    "The way your carbon footprint just entered the room with THAT energy... 😩 "
    "No shade (okay maybe a little shade), but your habits need a serious "
    "glow-up. The Earth didn't sign up for this treatment:\n\n"
    "1) Ditch fast fashion — outfit repeating is iconic, actually\n"
    "2) Take the stairs — elevators are so last season\n"
    "3) Use cloth bags — plastic bags belong in the museum of bad decisions",
]

FALLBACK_ADVICE = [
    "Great question! 🌍 Here are some eco-friendly tips: Start small — carry a reusable bag, "
    "switch to LED bulbs, and try eating one plant-based meal a day. Every small action adds up. "
    "The most sustainable choice is often the simplest one. Remember, progress over perfection!",

    "Love that you're asking! 🌱 The best thing you can do is reduce single-use items. "
    "Carry a water bottle, use cloth bags, and choose public transport when possible. "
    "Also, supporting local farmers reduces food transport emissions significantly. "
    "You've got this — the planet is cheering for you!",
]


class AIRoaster:
    """AI-powered eco lifestyle roaster using Google Gemini."""

    def __init__(self):
        self.model = None
        self._initialize()

    def _initialize(self):
        """Initialize Gemini model if API key is available."""
        if GEMINI_API_KEY:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
            except (ValueError, RuntimeError):
                self.model = None

    def roast_lifestyle(self, habits: dict) -> str:
        """
        Roast user's lifestyle choices in Gen Z slang.
        Falls back to hardcoded roasts if Gemini fails.
        """
        if self.model is None:
            return random.choice(FALLBACK_ROASTS)

        habit_text = "\n".join([
            f"- {k}: {v}" for k, v in habits.items()
        ])

        prompt = (
            "You are a Gen Z eco-advisor who roasts lifestyle choices like a "
            "savage but caring best friend. Use Gen Z slang (no cap, lowkey, "
            "bestie, slay, it's giving, delulu, rizz, etc.), be funny but "
            "educational, max 150 words. End with exactly 3 numbered practical "
            "eco-friendly tips.\n\n"
            f"Roast this lifestyle:\n{habit_text}"
        )

        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                return response.text
            return random.choice(FALLBACK_ROASTS)
        except (ValueError, RuntimeError, AttributeError):
            return random.choice(FALLBACK_ROASTS)

    def eco_advice(self, question: str) -> str:
        """
        Give eco advice in a friendly, professional tone.
        Falls back to generic advice if Gemini fails.
        """
        if self.model is None:
            return random.choice(FALLBACK_ADVICE)

        prompt = (
            "You are a friendly environmental expert. Answer this question "
            "about sustainability, climate change, or eco-friendly living "
            "in a clear, helpful way. Keep it under 200 words. "
            "Include 2-3 practical actionable tips.\n\n"
            f"Question: {question}"
        )

        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                return response.text
            return random.choice(FALLBACK_ADVICE)
        except (ValueError, RuntimeError, AttributeError):
            return random.choice(FALLBACK_ADVICE)
