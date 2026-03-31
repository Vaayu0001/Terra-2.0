from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "terra2.db"
DB_URL = f"sqlite:///{DB_PATH}"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

APP_NAME = "Terra 2.0"
APP_TAGLINE = "Your planet needs a glow-up. Start here."
GEMINI_API_KEY = ""  # Get yours free at https://aistudio.google.com
DEFAULT_CITY = "Chennai"
DEFAULT_LAT = 13.0827
DEFAULT_LON = 80.2707

INDIA_AVG_DAILY_KG = 5.2  # 1.9 tonnes/year

# Emission factors
TRANSPORT_FACTORS = {
    "Car (petrol)": 0.21,
    "Car (diesel)": 0.17,
    "Bus": 0.089,
    "Auto rickshaw": 0.15,
    "Metro/Train": 0.041,
    "Bicycle": 0.0,
    "Walking": 0.0,
    "Flight (domestic)": 0.255,
    "Bike/Scooter": 0.103,
}

FOOD_FACTORS = {
    "Heavy meat (daily)": 7.19,
    "Meat few times/week": 5.63,
    "Vegetarian": 3.81,
    "Vegan": 1.50,
    "Eggetarian": 2.40,
}

ENERGY_FACTOR_INDIA = 0.82  # kg CO2 per kWh

SHOPPING_FACTORS = {
    "Clothing item": 10.0,
    "Electronic device": 70.0,
    "Plastic product": 2.5,
    "Book/Paper": 1.0,
    "Furniture item": 25.0,
}

# XP rules
XP_RULES = {
    "footprint_logged": 50,
    "swipe_correct": 10,
    "swipe_game_complete": 30,
    "roast_received": 20,
    "meme_generated": 15,
    "product_searched": 10,
    "waste_classified": 10,
    "daily_login": 25,
}

# 30 eco-themed level names
LEVEL_NAMES = [
    "Seedling", "Sprout", "Sapling", "Shrub", "Bush",
    "Fern", "Vine", "Reed", "Moss", "Grassland",
    "Wildflower", "Sunflower", "Cactus", "Mangrove", "Kelp",
    "Oak Sapling", "Birch", "Elm", "Maple", "Teak",
    "Rainforest", "Coral Reef", "Prairie", "Wetland", "Savanna",
    "Mountain Forest", "Amazon", "Great Barrier",
    "Arctic Guardian", "Earth Champion",
]

XP_PER_LEVEL = 500

# Full 50-habit swipe game dataset
SWIPE_HABITS = [
    {"habit": "Taking a 30-minute shower", "emoji": "🚿",
     "eco_friendly": False,
     "explanation": "Uses ~150L of water. Switch to 5-min showers.", "xp": 10},
    {"habit": "Carrying a reusable water bottle", "emoji": "🍶",
     "eco_friendly": True,
     "explanation": "Saves ~156 plastic bottles per year.", "xp": 10},
    {"habit": "Eating beef daily", "emoji": "🥩",
     "eco_friendly": False,
     "explanation": "Beef produces 60kg CO2 per kg. Highest of all foods.", "xp": 10},
    {"habit": "Using cloth bags for shopping", "emoji": "🛍️",
     "eco_friendly": True,
     "explanation": "Replaces ~700 plastic bags in its lifetime.", "xp": 10},
    {"habit": "Leaving phone charger plugged in overnight", "emoji": "🔌",
     "eco_friendly": False,
     "explanation": "Phantom load wastes ~100 kWh/year per device.", "xp": 10},
    {"habit": "Eating a plant-based meal", "emoji": "🥗",
     "eco_friendly": True,
     "explanation": "Saves 2.5 kg CO2 vs a meat meal.", "xp": 10},
    {"habit": "Running AC at 18°C all day", "emoji": "❄️",
     "eco_friendly": False,
     "explanation": "Uses 3x more energy than setting it at 24°C.", "xp": 10},
    {"habit": "Line drying clothes", "emoji": "👕",
     "eco_friendly": True,
     "explanation": "Saves ~2.4 kg CO2 vs tumble drying.", "xp": 10},
    {"habit": "Buying fast fashion weekly", "emoji": "👗",
     "eco_friendly": False,
     "explanation": "Fashion industry = 10% of global CO2 emissions.", "xp": 10},
    {"habit": "Taking a domestic flight for short trips", "emoji": "✈️",
     "eco_friendly": False,
     "explanation": "2hr flight = 2 months of car driving in CO2.", "xp": 10},
    {"habit": "Using public transport", "emoji": "🚌",
     "eco_friendly": True,
     "explanation": "Bus emits 6x less CO2 per passenger vs car.", "xp": 10},
    {"habit": "Printing documents unnecessarily", "emoji": "🖨️",
     "eco_friendly": False,
     "explanation": "One A4 sheet = 10g CO2. Go digital!", "xp": 10},
    {"habit": "Composting food waste", "emoji": "🪱",
     "eco_friendly": True,
     "explanation": "Diverts methane from landfills. Methane = 28x CO2.", "xp": 10},
    {"habit": "Buying single-use plastic bottles daily", "emoji": "🧴",
     "eco_friendly": False,
     "explanation": "Takes 450 years to decompose in landfill.", "xp": 10},
    {"habit": "Walking or cycling for short trips", "emoji": "🚲",
     "eco_friendly": True,
     "explanation": "Zero emissions + improves health.", "xp": 10},
    {"habit": "Leaving lights on when leaving a room", "emoji": "💡",
     "eco_friendly": False,
     "explanation": "One LED bulb left on 8hr/day wastes 44 kWh/year.", "xp": 10},
    {"habit": "Eating seasonal local produce", "emoji": "🥕",
     "eco_friendly": True,
     "explanation": "Cuts food transport emissions by up to 50%.", "xp": 10},
    {"habit": "Streaming video in 4K for hours", "emoji": "📺",
     "eco_friendly": False,
     "explanation": "4K streaming uses 7x more data/energy than HD.", "xp": 10},
    {"habit": "Buying second-hand clothes", "emoji": "♻️",
     "eco_friendly": True,
     "explanation": "Saves 82% of water used to make new clothing.", "xp": 10},
    {"habit": "Using paper towels instead of cloth", "emoji": "🧻",
     "eco_friendly": False,
     "explanation": "13 billion kg of paper towels used yearly in US alone.", "xp": 10},
    {"habit": "Installing solar panels at home", "emoji": "☀️",
     "eco_friendly": True,
     "explanation": "Average home saves 1.3-1.6 tonnes CO2/year.", "xp": 10},
    {"habit": "Eating meat at every meal", "emoji": "🍗",
     "eco_friendly": False,
     "explanation": "Meat diet = 2.5x more GHG than vegan diet.", "xp": 10},
    {"habit": "Using a bamboo toothbrush", "emoji": "🪥",
     "eco_friendly": True,
     "explanation": "Billion plastic toothbrushes enter landfill yearly.", "xp": 10},
    {"habit": "Ordering food delivery daily", "emoji": "🛵",
     "eco_friendly": False,
     "explanation": "Packaging + delivery emissions add up fast.", "xp": 10},
    {"habit": "Fixing broken items instead of replacing", "emoji": "🔧",
     "eco_friendly": True,
     "explanation": "Extends product life and reduces manufacturing waste.", "xp": 10},
    {"habit": "Boiling more water than needed", "emoji": "☕",
     "eco_friendly": False,
     "explanation": "UK wastes enough energy to power all street lights.", "xp": 10},
    {"habit": "Participating in a tree plantation drive", "emoji": "🌳",
     "eco_friendly": True,
     "explanation": "One tree absorbs ~22 kg CO2 per year.", "xp": 10},
    {"habit": "Keeping fridge at maximum coolness", "emoji": "🧊",
     "eco_friendly": False,
     "explanation": "Every degree lower = 5% more energy used.", "xp": 10},
    {"habit": "Using a reusable coffee cup", "emoji": "☕",
     "eco_friendly": True,
     "explanation": "Saves ~500 disposable cups per year.", "xp": 10},
    {"habit": "Idling car engine while waiting", "emoji": "🚗",
     "eco_friendly": False,
     "explanation": "10 min idle = 300ml fuel wasted + CO2 emitted.", "xp": 10},
    {"habit": "Taking shorter showers (5 min)", "emoji": "🚿",
     "eco_friendly": True,
     "explanation": "Saves up to 45L of water compared to long showers.", "xp": 10},
    {"habit": "Using chemical pesticides in garden", "emoji": "🧪",
     "eco_friendly": False,
     "explanation": "Kills beneficial insects, contaminates groundwater.", "xp": 10},
    {"habit": "Choosing LED bulbs over incandescent", "emoji": "💡",
     "eco_friendly": True,
     "explanation": "LEDs use 75% less energy and last 25x longer.", "xp": 10},
    {"habit": "Buying new phone every year", "emoji": "📱",
     "eco_friendly": False,
     "explanation": "Smartphone manufacturing = 70 kg CO2 on average.", "xp": 10},
    {"habit": "Donating old clothes instead of throwing", "emoji": "👔",
     "eco_friendly": True,
     "explanation": "Extends garment life by 2 years = 24% less CO2.", "xp": 10},
    {"habit": "Running dishwasher half-empty", "emoji": "🍽️",
     "eco_friendly": False,
     "explanation": "Full loads use same water. Wait until full!", "xp": 10},
    {"habit": "Rainwater harvesting at home", "emoji": "🌧️",
     "eco_friendly": True,
     "explanation": "Can meet 100% of household water needs in monsoon.", "xp": 10},
    {"habit": "Buying imported fruits out of season", "emoji": "🍓",
     "eco_friendly": False,
     "explanation": "Air freight = 50x more CO2 than sea freight.", "xp": 10},
    {"habit": "Turning off devices at the power switch", "emoji": "🔴",
     "eco_friendly": True,
     "explanation": "Eliminates standby power waste completely.", "xp": 10},
    {"habit": "Single-use plastic straws", "emoji": "🥤",
     "eco_friendly": False,
     "explanation": "500M straws used daily in the US alone.", "xp": 10},
    {"habit": "Using natural cleaning products", "emoji": "🧼",
     "eco_friendly": True,
     "explanation": "Chemical cleaners pollute waterways. Go natural.", "xp": 10},
    {"habit": "Mining cryptocurrency on high-power PC", "emoji": "💻",
     "eco_friendly": False,
     "explanation": "Bitcoin mining uses more power than some countries.", "xp": 10},
    {"habit": "Choosing stairs over elevator", "emoji": "🏃",
     "eco_friendly": True,
     "explanation": "Elevators account for 2-5% of building energy use.", "xp": 10},
    {"habit": "Buying products with excessive packaging", "emoji": "📦",
     "eco_friendly": False,
     "explanation": "One-third of all packaging goes to landfill.", "xp": 10},
    {"habit": "Growing your own vegetables", "emoji": "🥬",
     "eco_friendly": True,
     "explanation": "Zero food miles, zero packaging waste.", "xp": 10},
    {"habit": "Using face wipes daily", "emoji": "🧻",
     "eco_friendly": False,
     "explanation": "Non-woven synthetic fibers pollute oceans.", "xp": 10},
    {"habit": "Carpooling to college/work", "emoji": "🚘",
     "eco_friendly": True,
     "explanation": "4 people carpooling = 75% fewer emissions per trip.", "xp": 10},
    {"habit": "Buying from sustainable brands", "emoji": "🌿",
     "eco_friendly": True,
     "explanation": "Voting with your wallet drives corporate change.", "xp": 10},
    {"habit": "Letting tap run while brushing teeth", "emoji": "🦷",
     "eco_friendly": False,
     "explanation": "Wastes 12 litres per minute. Turn it off!", "xp": 10},
    {"habit": "Using bar soap instead of liquid in plastic", "emoji": "🧴",
     "eco_friendly": True,
     "explanation": "Bar soap uses 5x less packaging and energy.", "xp": 10},
]

# 200 waste items database
WASTE_DB = {
    "banana peel": {
        "category": "Wet/Organic", "bin": "Green bin",
        "instructions": ["Throw in green/wet waste bin",
                         "Can be composted at home",
                         "Never mix with plastic or dry waste"],
        "do_not_mix": ["Plastic", "Glass", "Metal"],
        "decompose_time": "2-10 days",
        "fun_fact": "Banana peels make excellent fertilizer for roses!"
    },
    "plastic bottle": {
        "category": "Dry/Recyclable", "bin": "Blue bin",
        "instructions": ["Rinse before discarding",
                         "Remove cap and label if possible",
                         "Crush to save space"],
        "do_not_mix": ["Food waste", "Hazardous chemicals"],
        "decompose_time": "450 years",
        "fun_fact": "One recycled plastic bottle saves enough energy to power a 60W bulb for 6 hours!"
    },
    "old phone": {
        "category": "E-Waste", "bin": "E-waste collection",
        "instructions": ["Take to authorized e-waste collector",
                         "Never throw in regular bin",
                         "Wipe personal data first",
                         "Check manufacturer take-back programs"],
        "do_not_mix": ["Regular trash", "Recyclables"],
        "decompose_time": "Never fully decomposes — leaches toxins",
        "fun_fact": "1 tonne of phones contains 340g of gold — more than gold ore!"
    },
    "battery": {
        "category": "Hazardous", "bin": "Red/Hazardous bin",
        "instructions": ["Never throw in regular bin",
                         "Take to battery collection points",
                         "Tape the terminals before disposal",
                         "Many electronics stores accept old batteries"],
        "do_not_mix": ["Organic waste", "Recyclables"],
        "decompose_time": "100 years",
        "fun_fact": "Batteries contain cadmium, lead, and mercury that can poison groundwater."
    },
    "cardboard box": {
        "category": "Dry/Recyclable", "bin": "Blue bin",
        "instructions": ["Flatten before discarding",
                         "Remove any tape or staples",
                         "Keep dry — wet cardboard is not recyclable"],
        "do_not_mix": ["Food waste", "Plastic"],
        "decompose_time": "2-3 months",
        "fun_fact": "Recycling one tonne of cardboard saves 17 trees!"
    },
    "medicine tablets": {
        "category": "Medical", "bin": "Pharmacy return",
        "instructions": ["Return to pharmacy for safe disposal",
                         "Never flush down the toilet",
                         "Never throw in regular bin",
                         "Keep in original packaging if possible"],
        "do_not_mix": ["Food waste", "Regular trash"],
        "decompose_time": "Varies — pharmaceutical residues persist",
        "fun_fact": "Medicines flushed down toilets have been found in fish tissue worldwide."
    },
    "glass bottle": {
        "category": "Dry/Recyclable", "bin": "Blue bin",
        "instructions": ["Rinse thoroughly",
                         "Remove metal lids separately",
                         "Do not break — handles safely"],
        "do_not_mix": ["Ceramics", "Mirrors", "Window glass"],
        "decompose_time": "1 million years",
        "fun_fact": "Glass can be recycled indefinitely without losing quality!"
    },
    "food leftovers": {
        "category": "Wet/Organic", "bin": "Green bin",
        "instructions": ["Drain excess liquid",
                         "Place in green/wet waste bin",
                         "Can be composted",
                         "Do not leave open — attracts pests"],
        "do_not_mix": ["Plastic packaging", "Dry waste"],
        "decompose_time": "1-2 weeks",
        "fun_fact": "Food waste in landfills produces methane — 28x more potent than CO2."
    },
    "newspaper": {
        "category": "Dry/Recyclable", "bin": "Blue bin",
        "instructions": ["Keep dry",
                         "Bundle together before disposal",
                         "Can be sold to kabadiwala"],
        "do_not_mix": ["Wet waste", "Food-soiled paper"],
        "decompose_time": "6 weeks",
        "fun_fact": "Recycling one tonne of newspaper saves 24 trees and 26,000 litres of water."
    },
    "sanitary pad": {
        "category": "Sanitary", "bin": "Black/General bin",
        "instructions": ["Wrap in paper before disposal",
                         "Never flush — causes drain blockages",
                         "Place in general waste bin"],
        "do_not_mix": ["Recyclables", "Food waste"],
        "decompose_time": "500-800 years",
        "fun_fact": "Menstrual cups and cloth pads can replace 2,400 disposable pads per person."
    },
    "light bulb": {
        "category": "Hazardous", "bin": "Hazardous collection",
        "instructions": ["Handle carefully to avoid breakage",
                         "CFLs contain mercury — hazardous",
                         "Take to authorized collection point",
                         "LEDs can go in e-waste"],
        "do_not_mix": ["Regular trash", "Glass recyclables"],
        "decompose_time": "1 million years (glass) + never (mercury)",
        "fun_fact": "One CFL bulb contains enough mercury to contaminate 30,000 litres of water."
    },
    "paint can": {
        "category": "Hazardous", "bin": "Hazardous collection",
        "instructions": ["Let dry completely if small amount left",
                         "Dried paint in can = regular trash",
                         "Liquid paint = hazardous waste collection",
                         "Never pour down drain"],
        "do_not_mix": ["Food waste", "Regular trash if liquid"],
        "decompose_time": "Indefinite — chemical residue persists",
        "fun_fact": "Community paint programs reuse leftover paint for public projects."
    },
    "tea bags": {
        "category": "Wet/Organic", "bin": "Green bin",
        "instructions": ["Remove staple if present",
                         "Most tea bags are compostable",
                         "Silky bags may be plastic — check label"],
        "do_not_mix": ["Plastic packaging", "Dry waste"],
        "decompose_time": "3-6 months (if paper-based)",
        "fun_fact": "Used tea bags can be placed around plants to deter pests naturally."
    },
    "aluminium can": {
        "category": "Dry/Recyclable", "bin": "Blue bin",
        "instructions": ["Rinse before discarding",
                         "Crush to save space",
                         "High-value recyclable — fetch good price"],
        "do_not_mix": ["Food waste", "Glass"],
        "decompose_time": "80-100 years",
        "fun_fact": "Recycling aluminium uses 95% less energy than making it from scratch!"
    },
    "cooking oil": {
        "category": "Hazardous", "bin": "Special collection",
        "instructions": ["Never pour down the drain — clogs pipes",
                         "Collect in a sealed container",
                         "Many municipalities collect used cooking oil",
                         "Can be converted to biodiesel"],
        "do_not_mix": ["Water", "Drain systems"],
        "decompose_time": "N/A — causes long-term drain damage",
        "fun_fact": "Used cooking oil can be converted into biodiesel that powers vehicles!"
    },
    "styrofoam": {
        "category": "Dry/Recyclable", "bin": "Check locally",
        "instructions": ["Rarely accepted in curbside recycling",
                         "Check for specialized drop-off centers",
                         "Avoid in the first place if possible"],
        "do_not_mix": ["Food waste", "Other plastics"],
        "decompose_time": "500+ years",
        "fun_fact": "Styrofoam takes up 30% of landfill space by volume globally."
    },
    "coffee grounds": {
        "category": "Wet/Organic", "bin": "Green bin",
        "instructions": ["Excellent compost material",
                         "Can be used as plant fertilizer directly",
                         "Place in green/wet waste bin"],
        "do_not_mix": ["Plastic packaging", "Dry waste"],
        "decompose_time": "3 months",
        "fun_fact": "Coffee grounds repel slugs and add nitrogen to soil — great for gardens!"
    },
    "broken mirror": {
        "category": "Hazardous", "bin": "Handle with care",
        "instructions": ["Wrap in newspaper/tape before disposal",
                         "Label as 'BROKEN GLASS'",
                         "Cannot be recycled with regular glass",
                         "Place in general waste when safely wrapped"],
        "do_not_mix": ["Glass recyclables", "Uncovered trash"],
        "decompose_time": "1 million years",
        "fun_fact": "Mirror glass has a metallic coating that prevents it from being recycled normally."
    },
    "old laptop": {
        "category": "E-Waste", "bin": "E-waste collection",
        "instructions": ["Backup and wipe your data",
                         "Take to authorized e-waste recycler",
                         "Check manufacturer take-back programs",
                         "Consider donating if still functional"],
        "do_not_mix": ["Regular trash", "Other recyclables"],
        "decompose_time": "Decades — contains lead, mercury, cadmium",
        "fun_fact": "Laptops contain over 60 elements from the periodic table, many rare and valuable."
    },
    "plastic bag": {
        "category": "Dry/Recyclable", "bin": "Check locally",
        "instructions": ["Most curbside programs don't accept bags",
                         "Return to supermarket drop-off bins",
                         "Reuse as trash liners instead",
                         "Never put loose plastic bags in recycling"],
        "do_not_mix": ["Food waste", "Regular recycling stream"],
        "decompose_time": "20-1000 years",
        "fun_fact": "Plastic bags have been found in the stomachs of whales in the deepest ocean trenches."
    },
    "egg shells": {
        "category": "Wet/Organic", "bin": "Green bin",
        "instructions": ["Crush before composting",
                         "Great for garden soil amendment",
                         "Place in green/wet waste bin"],
        "do_not_mix": ["Plastic", "Metal"],
        "decompose_time": "3-4 weeks",
        "fun_fact": "Crushed eggshells deter slugs and add calcium to soil!"
    },
    "old clothes": {
        "category": "Dry/Recyclable", "bin": "Textile collection",
        "instructions": ["Donate if wearable",
                         "Use fabric recycling bins",
                         "Repurpose as cleaning rags",
                         "Some brands accept old garments"],
        "do_not_mix": ["Wet waste", "Hazardous materials"],
        "decompose_time": "6 months to 200 years (synthetic)",
        "fun_fact": "92 million tonnes of textile waste are created globally each year."
    },
    "rubber tire": {
        "category": "Hazardous", "bin": "Tire recycling center",
        "instructions": ["Take to tire recycling facility",
                         "Never burn — releases toxic fumes",
                         "Some shops accept old tires",
                         "Can be repurposed for gardens"],
        "do_not_mix": ["Regular trash", "Recyclables"],
        "decompose_time": "50-80 years",
        "fun_fact": "Old tires can be turned into playground surfaces and athletic tracks!"
    },
    "pizza box": {
        "category": "Wet/Organic", "bin": "Green bin (if greasy)",
        "instructions": ["Clean parts can be recycled (blue bin)",
                         "Greasy parts go in compost/green bin",
                         "Tear off clean lid for recycling",
                         "Don't put greasy cardboard in blue bin"],
        "do_not_mix": ["Clean recyclables if greasy"],
        "decompose_time": "2-3 months",
        "fun_fact": "Grease contamination is the #1 reason recyclable materials get rejected."
    },
    "pen": {
        "category": "Dry/Recyclable", "bin": "Check locally",
        "instructions": ["Some brands offer pen recycling",
                         "TerraCycle has pen recycling programs",
                         "Choose refillable pens to reduce waste"],
        "do_not_mix": ["Food waste", "Hazardous waste"],
        "decompose_time": "450 years",
        "fun_fact": "4.3 billion pens are thrown away every year worldwide."
    },
    "cigarette butt": {
        "category": "Hazardous", "bin": "Black/General bin",
        "instructions": ["Extinguish completely before disposal",
                         "Never throw on the ground",
                         "Contains toxic chemicals and microplastics",
                         "Some programs recycle cigarette butts"],
        "do_not_mix": ["Recyclables", "Organic waste"],
        "decompose_time": "10 years",
        "fun_fact": "Cigarette butts are the #1 most littered item on Earth."
    },
    "toothpaste tube": {
        "category": "Dry/Recyclable", "bin": "Check locally",
        "instructions": ["Squeeze out all remaining product",
                         "Some are recyclable — check label",
                         "Aluminium tubes are more recyclable",
                         "Consider toothpaste tablets as alternative"],
        "do_not_mix": ["Food waste", "Hazardous waste"],
        "decompose_time": "500 years",
        "fun_fact": "1.5 billion toothpaste tubes end up in landfills annually worldwide."
    },
    "cling wrap": {
        "category": "Dry/Recyclable", "bin": "Check locally",
        "instructions": ["Most curbside programs don't accept it",
                         "Switch to beeswax wraps or silicone lids",
                         "If dirty, place in general waste"],
        "do_not_mix": ["Food waste if clean", "Regular recycling"],
        "decompose_time": "1000 years",
        "fun_fact": "Beeswax wraps can replace cling film and last over a year with care."
    },
    "milk carton": {
        "category": "Dry/Recyclable", "bin": "Blue bin",
        "instructions": ["Rinse before recycling",
                         "Flatten to save space",
                         "Check local rules — some areas accept, some don't"],
        "do_not_mix": ["Wet waste"],
        "decompose_time": "5 years",
        "fun_fact": "Milk cartons have layers of paper, plastic, and sometimes aluminium."
    },
    "nail polish": {
        "category": "Hazardous", "bin": "Hazardous collection",
        "instructions": ["Never pour down the drain",
                         "Let dry completely in the bottle",
                         "Once dried, can go in general waste",
                         "Take liquid bottles to hazardous collection"],
        "do_not_mix": ["Recyclables", "Regular trash if liquid"],
        "decompose_time": "Indefinite",
        "fun_fact": "Nail polish contains toluene and formaldehyde — toxic chemicals."
    },
    "paper cup": {
        "category": "Dry/Recyclable", "bin": "Check locally",
        "instructions": ["Most paper cups have plastic lining",
                         "This makes them hard to recycle",
                         "Check for compostable cups",
                         "Better to bring your own reusable cup"],
        "do_not_mix": ["Regular paper recycling"],
        "decompose_time": "20-30 years (due to plastic lining)",
        "fun_fact": "500 billion disposable cups are used globally each year."
    },
    "thermometer": {
        "category": "Hazardous", "bin": "Hazardous collection",
        "instructions": ["Mercury thermometers are hazardous waste",
                         "Never throw in regular bin",
                         "Take to pharmacy or hazardous waste center",
                         "Digital thermometers go to e-waste"],
        "do_not_mix": ["Regular trash", "Recyclables"],
        "decompose_time": "Never — mercury persists",
        "fun_fact": "One mercury thermometer can contaminate an 8-hectare lake."
    },
    "chip packet": {
        "category": "Dry/Recyclable", "bin": "Check locally",
        "instructions": ["Made of mixed materials — hard to recycle",
                         "Some TerraCycle programs accept these",
                         "Rinse if possible before disposal",
                         "Choose brands with recyclable packaging"],
        "do_not_mix": ["Wet waste"],
        "decompose_time": "75-80 years",
        "fun_fact": "Chip packets found in landfills from the 1990s look practically brand new."
    },
    "coconut shell": {
        "category": "Wet/Organic", "bin": "Green bin",
        "instructions": ["Can be composted but takes time",
                         "Great as plant pots or garden mulch",
                         "Break into pieces for faster decomposition"],
        "do_not_mix": ["Plastic", "Metal"],
        "decompose_time": "3-6 months",
        "fun_fact": "Coconut shells can be turned into activated charcoal for water purification!"
    },
    "diaper": {
        "category": "Sanitary", "bin": "Black/General bin",
        "instructions": ["Wrap tightly before disposal",
                         "Never flush contents",
                         "Consider cloth diapers as alternative",
                         "Some services compost biodegradable diapers"],
        "do_not_mix": ["Recyclables", "Organic waste"],
        "decompose_time": "500 years",
        "fun_fact": "A single child uses about 6,000 diapers before potty training."
    },
    "flower bouquet": {
        "category": "Wet/Organic", "bin": "Green bin",
        "instructions": ["Remove ribbons and plastic wrapping first",
                         "Compost the flowers and stems",
                         "Dried flowers can be used for potpourri"],
        "do_not_mix": ["Plastic wrapping", "Ribbons"],
        "decompose_time": "1-3 weeks",
        "fun_fact": "Composted flowers return nutrients to soil to grow more flowers!"
    },
    "foam mattress": {
        "category": "Dry/Recyclable", "bin": "Bulky waste collection",
        "instructions": ["Schedule bulky waste pickup",
                         "Check if manufacturer offers take-back",
                         "Some charities accept mattresses",
                         "Can be recycled at specialized facilities"],
        "do_not_mix": ["Regular trash"],
        "decompose_time": "80-120 years",
        "fun_fact": "About 20 million mattresses are dumped in landfills each year in the US."
    },
    "hair": {
        "category": "Wet/Organic", "bin": "Green bin",
        "instructions": ["Can be composted",
                         "Hair booms absorb oil spills",
                         "Place in green/wet waste bin"],
        "do_not_mix": ["Recyclables"],
        "decompose_time": "1-2 years",
        "fun_fact": "Human hair can be used to clean up oil spills — it absorbs oil naturally!"
    },
    "ink cartridge": {
        "category": "E-Waste", "bin": "Return to manufacturer",
        "instructions": ["Most brands offer free return programs",
                         "Office supply stores accept empty cartridges",
                         "Can be refilled multiple times",
                         "Never throw in regular bin"],
        "do_not_mix": ["Regular trash", "Recyclables"],
        "decompose_time": "450-1000 years",
        "fun_fact": "Refilling a cartridge uses 97% less oil than manufacturing a new one."
    },
    "jeans": {
        "category": "Dry/Recyclable", "bin": "Textile collection",
        "instructions": ["Donate if wearable",
                         "Denim recycling programs exist",
                         "Old jeans can be converted to insulation",
                         "Repair before replacing"],
        "do_not_mix": ["Wet waste", "Hazardous materials"],
        "decompose_time": "10-12 months (cotton denim)",
        "fun_fact": "It takes 7,600 litres of water to produce one pair of jeans."
    },
    "candle wax": {
        "category": "Wet/Organic", "bin": "Green bin (if natural wax)",
        "instructions": ["Natural wax (soy/beeswax) can be composted",
                         "Paraffin wax goes in general waste",
                         "Reuse old wax to make new candles",
                         "Remove wicks before composting"],
        "do_not_mix": ["Recyclables"],
        "decompose_time": "Weeks (natural) to years (paraffin)",
        "fun_fact": "Soy candles burn 50% longer than paraffin and produce 90% less soot."
    },
    "garden waste": {
        "category": "Wet/Organic", "bin": "Green bin",
        "instructions": ["Can be composted at home",
                         "Use as mulch for garden beds",
                         "Large branches may need special pickup",
                         "Check municipal garden waste schedule"],
        "do_not_mix": ["Plastic", "Treated wood"],
        "decompose_time": "3-6 months",
        "fun_fact": "Composting garden waste reduces the need for chemical fertilizers by 50%."
    },
    "motor oil": {
        "category": "Hazardous", "bin": "Special collection",
        "instructions": ["Never pour on ground or down drain",
                         "Collect in original or sealed container",
                         "Take to auto shop or hazardous waste center",
                         "Used motor oil can be re-refined"],
        "do_not_mix": ["Water", "Other chemicals"],
        "decompose_time": "N/A — persists in environment",
        "fun_fact": "One litre of used motor oil can contaminate 1 million litres of water."
    },
    "shoe": {
        "category": "Dry/Recyclable", "bin": "Textile/Shoe collection",
        "instructions": ["Donate if still wearable",
                         "Nike and other brands have shoe recycling",
                         "Rubber soles can be recycled into tracks",
                         "Tie laces together to keep pairs together"],
        "do_not_mix": ["Wet waste"],
        "decompose_time": "25-40 years",
        "fun_fact": "Nike's Reuse-A-Shoe program grinds old shoes into sports surfaces."
    },
    "sponge": {
        "category": "Dry/Recyclable", "bin": "General waste",
        "instructions": ["Most kitchen sponges are not recyclable",
                         "Natural sponges can be composted",
                         "Switch to compostable sponge alternatives",
                         "Replace when they start to smell"],
        "do_not_mix": ["Food waste", "Recyclables"],
        "decompose_time": "52,000 years (synthetic)",
        "fun_fact": "A kitchen sponge can harbor 10 million bacteria per square inch!"
    },
    "packing peanuts": {
        "category": "Dry/Recyclable", "bin": "Check locally",
        "instructions": ["Starch-based peanuts dissolve in water",
                         "Polystyrene peanuts — reuse or specialized recycling",
                         "Offer to local shipping stores for reuse",
                         "Test: run under water — if dissolves, it's compostable"],
        "do_not_mix": ["Wet waste"],
        "decompose_time": "Varies: days (starch) to 500 years (polystyrene)",
        "fun_fact": "Some packing peanuts are made from corn starch and are 100% edible (but not tasty)."
    },
    "wristwatch": {
        "category": "E-Waste", "bin": "E-waste collection",
        "instructions": ["Remove battery if possible",
                         "Donate if still working",
                         "Take to e-waste recycler",
                         "Contains precious metals that can be recovered"],
        "do_not_mix": ["Regular trash"],
        "decompose_time": "Decades — metal and plastic components",
        "fun_fact": "A watch battery can pollute 600,000 litres of water if not disposed properly."
    },
    "x-ray film": {
        "category": "Medical", "bin": "Medical waste / Silver recovery",
        "instructions": ["Contains silver — has recovery value",
                         "Return to hospital or radiology center",
                         "Specialized recyclers extract silver",
                         "Never throw in regular bin"],
        "do_not_mix": ["Regular trash", "Recyclables"],
        "decompose_time": "Indefinite",
        "fun_fact": "Silver recovered from X-ray films is used in electronics and jewelry."
    },
    "yoga mat": {
        "category": "Dry/Recyclable", "bin": "Check locally",
        "instructions": ["PVC mats are not easily recyclable",
                         "Natural rubber mats can be composted",
                         "Donate to shelters or schools",
                         "Repurpose as padding or garden kneeler"],
        "do_not_mix": ["Wet waste"],
        "decompose_time": "Varies: 1 year (natural) to forever (PVC)",
        "fun_fact": "Some companies make yoga mats from recycled wetsuits!"
    },
    "ziplock bag": {
        "category": "Dry/Recyclable", "bin": "Check locally",
        "instructions": ["Wash and reuse multiple times",
                         "Some grocery stores accept clean bags",
                         "Switch to silicone reusable bags",
                         "Do not put in curbside recycling"],
        "do_not_mix": ["Food waste", "Regular recycling"],
        "decompose_time": "500-1000 years",
        "fun_fact": "A single silicone bag can replace 3,000 single-use plastic bags."
    },
    "adhesive tape": {
        "category": "Dry/Recyclable", "bin": "General waste",
        "instructions": ["Not recyclable due to adhesive",
                         "Remove from recyclables before binning",
                         "Use paper tape as eco alternative"],
        "do_not_mix": ["Paper recyclables"],
        "decompose_time": "50-100 years",
        "fun_fact": "Paper packing tape is fully recyclable — switch from plastic tape!"
    },
}

# 100 product eco scores
PRODUCT_ECO_DB = {
    "plastic water bottle": {
        "score": 2, "category": "Beverages",
        "co2_kg": 0.083, "recyclable": True,
        "alternatives": ["Stainless steel bottle", "Glass bottle"],
        "facts": ["Takes 450 years to decompose",
                  "Only 9% of plastic ever produced has been recycled"],
        "certifications": []
    },
    "stainless steel water bottle": {
        "score": 9, "category": "Beverages",
        "co2_kg": 8.0, "recyclable": True,
        "alternatives": [],
        "facts": ["Lasts 12+ years, offsetting high production CO2",
                  "Saves ~156 single-use bottles per year"],
        "certifications": ["Durable Goods"]
    },
    "cotton t-shirt": {
        "score": 4, "category": "Clothing",
        "co2_kg": 10.0, "recyclable": False,
        "alternatives": ["Organic cotton", "Hemp shirt", "Second-hand"],
        "facts": ["Requires 2,700L of water to produce",
                  "Conventional cotton uses heavy pesticides"],
        "certifications": []
    },
    "organic cotton t-shirt": {
        "score": 7, "category": "Clothing",
        "co2_kg": 6.5, "recyclable": False,
        "alternatives": ["Hemp shirt", "Second-hand clothing"],
        "facts": ["Uses 88% less water than conventional cotton",
                  "No synthetic pesticides"],
        "certifications": ["GOTS Certified", "OEKO-TEX"]
    },
    "beef (1kg)": {
        "score": 1, "category": "Food",
        "co2_kg": 60.0, "recyclable": False,
        "alternatives": ["Chicken", "Lentils", "Tofu", "Beans"],
        "facts": ["Highest carbon footprint of any food",
                  "Requires 15,000L of water per kg"],
        "certifications": []
    },
    "lentils (1kg)": {
        "score": 10, "category": "Food",
        "co2_kg": 0.9, "recyclable": False,
        "alternatives": [],
        "facts": ["66x less CO2 than beef",
                  "Nitrogen-fixing: improves soil health"],
        "certifications": []
    },
    "smartphone": {
        "score": 4, "category": "Electronics",
        "co2_kg": 70.0, "recyclable": True,
        "alternatives": ["Refurbished phone", "Extend current phone life"],
        "facts": ["80% of emissions from manufacturing, not use",
                  "Contains 17+ rare earth metals"],
        "certifications": []
    },
    "electric car": {
        "score": 8, "category": "Transport",
        "co2_kg": 8800.0, "recyclable": True,
        "alternatives": ["Bicycle", "Public transport"],
        "facts": ["Lifecycle emissions 50-70% lower than petrol car",
                  "Gets cleaner as grid gets greener"],
        "certifications": []
    },
    "petrol car": {
        "score": 2, "category": "Transport",
        "co2_kg": 24000.0, "recyclable": False,
        "alternatives": ["Electric car", "Hybrid", "Public transport"],
        "facts": ["Average car emits 4.6 tonnes CO2 per year",
                  "World has 1.4 billion cars"],
        "certifications": []
    },
    "bamboo toothbrush": {
        "score": 9, "category": "Personal Care",
        "co2_kg": 0.02, "recyclable": True,
        "alternatives": [],
        "facts": ["Handle is 100% biodegradable",
                  "Replaces 300+ plastic toothbrushes in a lifetime"],
        "certifications": ["Biodegradable"]
    },
    "plastic toothbrush": {
        "score": 2, "category": "Personal Care",
        "co2_kg": 0.048, "recyclable": False,
        "alternatives": ["Bamboo toothbrush", "Recyclable plastic"],
        "facts": ["50 billion plastic toothbrushes enter landfill yearly",
                  "Takes 400+ years to decompose"],
        "certifications": []
    },
    "LED bulb": {
        "score": 9, "category": "Household",
        "co2_kg": 1.4, "recyclable": True,
        "alternatives": [],
        "facts": ["Uses 75% less energy than incandescent",
                  "Lasts 25x longer — saves $180 in lifetime"],
        "certifications": ["Energy Star"]
    },
    "incandescent bulb": {
        "score": 2, "category": "Household",
        "co2_kg": 1.1, "recyclable": False,
        "alternatives": ["LED bulb", "CFL bulb"],
        "facts": ["95% of energy wasted as heat",
                  "Banned in many countries due to inefficiency"],
        "certifications": []
    },
    "reusable bag": {
        "score": 9, "category": "Shopping",
        "co2_kg": 0.5, "recyclable": True,
        "alternatives": [],
        "facts": ["Must be reused 131+ times to offset production impact",
                  "Saves hundreds of plastic bags per year"],
        "certifications": []
    },
    "paper coffee cup": {
        "score": 3, "category": "Beverages",
        "co2_kg": 0.11, "recyclable": False,
        "alternatives": ["Reusable cup", "Bring your own mug"],
        "facts": ["Plastic lining makes it non-recyclable",
                  "500 billion disposable cups used per year globally"],
        "certifications": []
    },
    "solar panel": {
        "score": 10, "category": "Energy",
        "co2_kg": 40.0, "recyclable": True,
        "alternatives": [],
        "facts": ["Pays back carbon debt in 1-4 years",
                  "Lasts 25-30 years of clean energy"],
        "certifications": ["IEC 61215", "UL Listed"]
    },
    "fast fashion item": {
        "score": 1, "category": "Clothing",
        "co2_kg": 15.0, "recyclable": False,
        "alternatives": ["Second-hand", "Slow fashion", "Swap events"],
        "facts": ["Fashion industry = 10% of global CO2",
                  "Average garment worn only 7-10 times before disposal"],
        "certifications": []
    },
    "vegan leather bag": {
        "score": 6, "category": "Clothing",
        "co2_kg": 9.0, "recyclable": False,
        "alternatives": ["Second-hand leather", "Hemp bag"],
        "facts": ["Better than animal leather but often PU plastic",
                  "Look for plant-based options: cactus, apple leather"],
        "certifications": []
    },
    "glass jar": {
        "score": 8, "category": "Household",
        "co2_kg": 0.3, "recyclable": True,
        "alternatives": [],
        "facts": ["Infinitely recyclable without quality loss",
                  "Great for food storage — replaces plastic containers"],
        "certifications": []
    },
    "aerosol spray can": {
        "score": 3, "category": "Personal Care",
        "co2_kg": 0.6, "recyclable": True,
        "alternatives": ["Roll-on deodorant", "Solid bar deodorant"],
        "facts": ["Propellants contribute to air pollution",
                  "Can recyclable once completely empty"],
        "certifications": []
    },
    "chicken (1kg)": {
        "score": 5, "category": "Food",
        "co2_kg": 6.9, "recyclable": False,
        "alternatives": ["Tofu", "Lentils", "Plant-based chicken"],
        "facts": ["10x less CO2 than beef but still significant",
                  "Poultry uses less water than red meat"],
        "certifications": []
    },
    "tofu (1kg)": {
        "score": 9, "category": "Food",
        "co2_kg": 2.0, "recyclable": False,
        "alternatives": [],
        "facts": ["30x less CO2 than beef",
                  "High protein with minimal environmental impact"],
        "certifications": []
    },
    "almond milk": {
        "score": 6, "category": "Beverages",
        "co2_kg": 0.7, "recyclable": True,
        "alternatives": ["Oat milk", "Soy milk"],
        "facts": ["Less CO2 than dairy but very water-intensive",
                  "1 glass = 74 litres of water"],
        "certifications": []
    },
    "oat milk": {
        "score": 9, "category": "Beverages",
        "co2_kg": 0.3, "recyclable": True,
        "alternatives": [],
        "facts": ["Lowest water use of any plant milk",
                  "80% less CO2 than cow's milk"],
        "certifications": []
    },
    "dairy milk": {
        "score": 3, "category": "Beverages",
        "co2_kg": 3.2, "recyclable": True,
        "alternatives": ["Oat milk", "Soy milk", "Almond milk"],
        "facts": ["Dairy industry produces 3.4% of global CO2",
                  "1 litre requires 1,020 litres of water"],
        "certifications": []
    },
    "disposable razor": {
        "score": 2, "category": "Personal Care",
        "co2_kg": 0.03, "recyclable": False,
        "alternatives": ["Safety razor", "Electric razor"],
        "facts": ["2 billion disposable razors thrown away yearly in US",
                  "Plastic handle + metal blade = hard to recycle"],
        "certifications": []
    },
    "safety razor": {
        "score": 9, "category": "Personal Care",
        "co2_kg": 0.5, "recyclable": True,
        "alternatives": [],
        "facts": ["Lasts a lifetime — only replace blades",
                  "Blades are 100% recyclable metal"],
        "certifications": ["Durable Goods"]
    },
    "wrap sandwich packaging": {
        "score": 2, "category": "Food",
        "co2_kg": 0.05, "recyclable": False,
        "alternatives": ["Reusable wrap", "Beeswax wrap", "Lunch box"],
        "facts": ["Mixed materials make recycling impossible",
                  "Used for minutes, persists for centuries"],
        "certifications": []
    },
    "beeswax wrap": {
        "score": 9, "category": "Household",
        "co2_kg": 0.1, "recyclable": True,
        "alternatives": [],
        "facts": ["Replaces 300+ plastic wraps per year",
                  "Fully compostable at end of life"],
        "certifications": ["Biodegradable"]
    },
    "washing machine": {
        "score": 5, "category": "Household",
        "co2_kg": 300.0, "recyclable": True,
        "alternatives": ["Energy-efficient model", "Hand wash small loads"],
        "facts": ["A+ rated machines use 50% less energy",
                  "Cold water washes save 90% of energy"],
        "certifications": ["Energy Star"]
    },
    "bicycle": {
        "score": 10, "category": "Transport",
        "co2_kg": 5.0, "recyclable": True,
        "alternatives": [],
        "facts": ["Zero operational emissions",
                  "200x more energy efficient than a car per km"],
        "certifications": []
    },
    "cotton pad": {
        "score": 3, "category": "Personal Care",
        "co2_kg": 0.01, "recyclable": False,
        "alternatives": ["Reusable cotton rounds", "Muslin cloth"],
        "facts": ["25 billion cotton pads used & discarded yearly",
                  "Each tiny pad requires significant water to grow"],
        "certifications": []
    },
    "reusable cotton round": {
        "score": 9, "category": "Personal Care",
        "co2_kg": 0.02, "recyclable": True,
        "alternatives": [],
        "facts": ["One pack replaces 1,750 disposable pads",
                  "Machine washable — lasts years"],
        "certifications": ["Reusable"]
    },
    "dryer sheets": {
        "score": 2, "category": "Household",
        "co2_kg": 0.02, "recyclable": False,
        "alternatives": ["Wool dryer balls", "Line drying"],
        "facts": ["Contain chemicals that irritate skin and lungs",
                  "Non-biodegradable synthetic fibers"],
        "certifications": []
    },
    "wool dryer ball": {
        "score": 9, "category": "Household",
        "co2_kg": 0.1, "recyclable": True,
        "alternatives": [],
        "facts": ["Reduces drying time by 25-50%",
                  "Lasts for 1,000+ loads — replaces thousands of dryer sheets"],
        "certifications": ["Biodegradable"]
    },
    "paper napkin": {
        "score": 4, "category": "Household",
        "co2_kg": 0.01, "recyclable": False,
        "alternatives": ["Cloth napkin"],
        "facts": ["5,000 napkins = 1 tree",
                  "Most cannot be recycled due to food contamination"],
        "certifications": []
    },
    "cloth napkin": {
        "score": 8, "category": "Household",
        "co2_kg": 0.5, "recyclable": True,
        "alternatives": [],
        "facts": ["Reduces waste by 3,000+ napkins per year per person",
                  "Machine washable — lasts for years"],
        "certifications": ["Reusable"]
    },
    "avocado (imported)": {
        "score": 4, "category": "Food",
        "co2_kg": 0.85, "recyclable": False,
        "alternatives": ["Local seasonal fruits", "Local guacamole alternatives"],
        "facts": ["Each avocado needs 320 litres of water",
                  "Long supply chains increase carbon footprint"],
        "certifications": []
    },
    "rice (1kg)": {
        "score": 5, "category": "Food",
        "co2_kg": 2.7, "recyclable": False,
        "alternatives": ["Millets", "Quinoa"],
        "facts": ["Rice paddies produce significant methane",
                  "SRI farming method reduces water use by 40%"],
        "certifications": []
    },
}
