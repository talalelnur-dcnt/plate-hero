import streamlit as st
import os
import json
import time
from datetime import datetime
from PIL import Image
import io

# ==============================================================================
# PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="Plate Hero: Sibling Nutrition & Fitness Arena",
    page_icon="🦸‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# CUSTOM STYLING (KID-FRIENDLY, VIBRANT, GAMIFIED THEME)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Nunito:wght@400;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    h1, h2, h3, h4, .hero-title {
        font-family: 'Fredoka', cursive, sans-serif !important;
        font-weight: 700 !important;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #FFA07A 100%);
        padding: 24px 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }

    .hero-banner h1 {
        margin: 0;
        font-size: 2.2rem;
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .hero-banner p {
        margin: 4px 0 0 0;
        font-size: 1.05rem;
        font-weight: 600;
        opacity: 0.95;
    }

    /* Card Containers */
    .hero-card {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 20px;
        border: 2px solid #F1F3F5;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .hero-card:hover {
        box-shadow: 0 10px 22px rgba(0,0,0,0.09);
    }

    /* Sibling Profile Card in Sidebar */
    .profile-badge-card {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 18px;
        box-shadow: 0 6px 18px rgba(124, 58, 237, 0.3);
    }

    .profile-badge-card h3 {
        margin: 0;
        color: white !important;
        font-size: 1.4rem;
    }

    /* Metabolism Story Box */
    .story-box {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-left: 6px solid #3B82F6;
        padding: 18px 22px;
        border-radius: 14px;
        margin: 15px 0;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #1E3A8A;
    }

    /* Quest Card */
    .quest-card {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 2px dashed #10B981;
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .quest-title {
        color: #065F46;
        font-weight: 800;
        font-size: 1.25rem;
        margin-bottom: 8px;
    }

    /* Macro Bars Custom Container */
    .macro-bar-row {
        margin: 12px 0;
    }

    .macro-label {
        font-weight: 700;
        font-size: 0.95rem;
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
    }

    /* Stat Badges */
    .badge-chip {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.88rem;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .badge-protein { background-color: #DBEAFE; color: #1D4ED8; border: 1px solid #BFDBFE; }
    .badge-battery { background-color: #DCFCE7; color: #15803D; border: 1px solid #BBF7D0; }
    .badge-sugar-low { background-color: #FEF3C7; color: #B45309; border: 1px solid #FDE68A; }
    .badge-sugar-high { background-color: #FEE2E2; color: #B91C1C; border: 1px solid #FECACA; }
    .badge-brain { background-color: #F3E8FF; color: #7E22CE; border: 1px solid #E9D5FF; }

    /* Custom Buttons */
    div.stButton > button {
        border-radius: 12px;
        font-weight: 700;
        font-family: 'Fredoka', cursive, sans-serif;
        font-size: 1.05rem;
        transition: all 0.2s ease-in-out;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 2px solid #E2E8F0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# SOUND EFFECTS & AUDIO JAVASCRIPT
# ==============================================================================
def play_sound(sound_type="fanfare"):
    """Injects lightweight web audio synthesis for rewarding sound effects."""
    if sound_type == "fanfare":
        audio_js = """
        <script>
        (function() {
            try {
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                if (!AudioCtx) return;
                const ctx = new AudioCtx();
                const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
                notes.forEach((freq, idx) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.12);
                    gain.gain.setValueAtTime(0.15, ctx.currentTime + idx * 0.12);
                    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.12 + 0.35);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(ctx.currentTime + idx * 0.12);
                    osc.stop(ctx.currentTime + idx * 0.12 + 0.36);
                });
            } catch(e) { console.log('Audio disabled:', e); }
        })();
        </script>
        """
        st.components.v1.html(audio_js, height=0, width=0)


# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
DEFAULT_SIBLINGS = {
    "kid_leo": {
        "name": "Leo",
        "avatar": "⚡",
        "xp": 340,
        "streak": 5,
        "cash_redeemed": 1.00,
        "history": [
            {
                "time": "Today, 11:30 AM",
                "type": "Plate Scan",
                "food": "Grilled Chicken & Broccoli",
                "xp": 50,
                "note": "Super muscle bricks unlocked!"
            },
            {
                "time": "Today, 11:45 AM",
                "type": "Hero Quest",
                "food": "10 Super Squats & Jump",
                "xp": 30,
                "note": "Quest completed with high energy"
            },
            {
                "time": "Yesterday, 4:00 PM",
                "type": "Hero Quest",
                "food": "15 Star Jumps",
                "xp": 25,
                "note": "Afternoon boost completed"
            }
        ]
    },
    "kid_maya": {
        "name": "Maya",
        "avatar": "🌟",
        "xp": 480,
        "streak": 8,
        "cash_redeemed": 2.50,
        "history": [
            {
                "time": "Today, 9:00 AM",
                "type": "Plate Scan",
                "food": "Berry Oatmeal & Almonds",
                "xp": 55,
                "note": "Brain armor + steady battery power"
            },
            {
                "time": "Today, 9:20 AM",
                "type": "Hero Quest",
                "food": "10 Min Bike Patrol",
                "xp": 40,
                "note": "Patrolled the whole block!"
            }
        ]
    },
    "kid_sam": {
        "name": "Sammy",
        "avatar": "🚀",
        "xp": 160,
        "streak": 3,
        "cash_redeemed": 0.00,
        "history": [
            {
                "time": "Today, 8:15 AM",
                "type": "Plate Scan",
                "food": "Whole Grain Toast & Egg",
                "xp": 45,
                "note": "Great morning fuel"
            }
        ]
    }
}

if "siblings" not in st.session_state:
    st.session_state.siblings = DEFAULT_SIBLINGS.copy()

if "active_sibling_id" not in st.session_state:
    st.session_state.active_sibling_id = "kid_leo"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "👋 Hey there, Plate Hero! I'm **Coach Crunch**, your super nutrition and energy guide! 🥦⚡ Ask me anything about what fuel gives you superpowers, why veggies make you jump higher, or how to blast away the sugar crash!"
        }
    ]

if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

if "scan_image_display" not in st.session_state:
    st.session_state.scan_image_display = None

if "scan_base_claimed" not in st.session_state:
    st.session_state.scan_base_claimed = False

if "quest_claimed" not in st.session_state:
    st.session_state.quest_claimed = False


# ==============================================================================
# HELPER FUNCTIONS & GEMINI API CALLS
# ==============================================================================
def get_level_info(xp):
    """Calculates level name, badge, and progress to next level."""
    levels = [
        (0, 99, "Level 1: 🥦 Rookie Nibbler", 100),
        (100, 249, "Level 2: ⚡ Power Snacker", 250),
        (250, 499, "Level 3: 🛡️ Veggie Titan", 500),
        (500, 999, "Level 4: 🦸 Macro Master", 1000),
        (1000, 99999, "Level 5: 👑 Ultimate Plate Hero", 1500)
    ]
    for min_xp, max_xp, title, next_cap in levels:
        if min_xp <= xp <= max_xp:
            progress = min(1.0, max(0.0, (xp - min_xp) / (next_cap - min_xp)))
            return title, progress, next_cap
    return "Level 5: 👑 Ultimate Plate Hero", 1.0, xp


def get_available_cash(xp, cash_redeemed):
    """100 XP = $1.00. Returns total earned and unredeemed cash."""
    total_earned = xp / 100.0
    available = max(0.0, total_earned - cash_redeemed)
    return total_earned, available


# Preloaded Demo Plates Data
DEMO_DATA = {
    "apple_pb": {
        "food_items": [
            "Crispy Green Apple Slices 🍏",
            "Creamy All-Natural Peanut Butter 🥜",
            "Crunchy Chia & Hemp Sprinkles ✨"
        ],
        "macro_breakdown": {
            "protein_bricks": "Medium",
            "battery_fuel": "High",
            "sugar_spike": "Low",
            "brain_armor": "High"
        },
        "metabolism_story": "🔥 **Hero Metabolism Ignition:** Your stomach turns the crisp apple fiber into steady, long-lasting rocket fuel while the peanut butter builds tough muscle armor! Zero sugar crashes—just 3 full hours of turbocharged playground stamina!",
        "base_xp": 50,
        "hero_quest": {
            "activity": "🏃 15 Sonic Speed High-Knees + 10 Super Hero Lunges",
            "xp_reward": 35
        }
    },
    "frosted_donut": {
        "food_items": [
            "Frosted Strawberry Donut 🍩",
            "Sugar Glaze & Rainbow Sprinkles 🌈",
            "Refined Sweet Dough 🌾"
        ],
        "macro_breakdown": {
            "protein_bricks": "Low",
            "battery_fuel": "Low",
            "sugar_spike": "High",
            "brain_armor": "Low"
        },
        "metabolism_story": "🚨 **Sugar Goblin Alert!** A massive wave of fast sugar rushes your bloodstream for a quick 10-minute turbo buzz. But watch out! Without protein bricks to hold the fort, the sugar rollercoaster drops fast, leaving your hero body feeling sluggish and sleepy!",
        "base_xp": 15,
        "hero_quest": {
            "activity": "⚡ 20 Donut-Buster Jumping Jacks + 3 Laps Around the Living Room",
            "xp_reward": 45
        }
    }
}


def call_gemini_plate_scanner(image_pil, api_key=None):
    """Calls Gemini 2.5 Flash to analyze the plate with structured JSON output."""
    effective_key = api_key or os.environ.get("GEMINI_API_KEY")
    
    # If no key, generate smart fallback based on image or default
    if not effective_key:
        return {
            "food_items": [
                "Superhero Balanced Plate 🥗",
                "Lean Protein Power Cubes 🍗",
                "Rainbow Garden Veggies 🥕"
            ],
            "macro_breakdown": {
                "protein_bricks": "High",
                "battery_fuel": "High",
                "sugar_spike": "Low",
                "brain_armor": "High"
            },
            "metabolism_story": "🌟 **Metabolism Reactor Online:** Your body enzymes break down the nutrients into high-efficiency energy cells! Protein bricks are rushed directly to your muscles for super strength!",
            "base_xp": 45,
            "hero_quest": {
                "activity": "🦸‍♂️ 12 Super Squats + 10 Power Punches in the Air",
                "xp_reward": 30
            }
        }
    
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=effective_key)
        
        prompt = """
        You are Plate Hero AI, a nutrition and metabolism simulator for kids.
        Analyze the food items in this meal/plate image.
        
        Return a strict JSON object with these EXACT keys:
        {
          "food_items": ["item 1", "item 2", ...],
          "macro_breakdown": {
            "protein_bricks": "High" | "Med" | "Low",
            "battery_fuel": "High" | "Med" | "Low",
            "sugar_spike": "High" | "Med" | "Low",
            "brain_armor": "High" | "Med" | "Low"
          },
          "metabolism_story": "A short, exciting, 2-3 sentence kid-friendly story explaining how their metabolism processes this food (e.g., whether it burns cleanly as super stamina rocket fuel or spikes blood sugar and causes a sleepy crash).",
          "base_xp": integer between 10 and 60 (award high XP like 40-60 for whole foods, veggies, and proteins; lower XP like 10-20 for high-sugar junk foods),
          "hero_quest": {
            "activity": "A fun, active physical exercise for kids to do right now (e.g., '10 Jumping Jacks + 5 High-Knees')",
            "xp_reward": integer between 20 and 50
          }
        }
        """
        
        # Convert PIL to bytes
        img_byte_arr = io.BytesIO()
        image_pil.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        
        result_json = json.loads(response.text)
        return result_json
    except Exception as e:
        st.error(f"Gemini API Notice: {str(e)}. Using fallback hero analysis.")
        return DEMO_DATA["apple_pb"]


def call_gemini_hero_coach(prompt_text, chat_history, api_key=None):
    """Calls Gemini 2.5 Flash for the Hero Coach Q&A persona."""
    effective_key = api_key or os.environ.get("GEMINI_API_KEY")
    
    if not effective_key:
        # Fun fallback replies
        fallbacks = {
            "protein": "🧱 **Protein is your Muscle Armor!** When you run and kick soccer balls, tiny muscle fibers work super hard. Protein foods like eggs, chicken, nuts, and yogurt act like building bricks that rebuild your muscles into stronger titanium superhero armor while you rest!",
            "sugar": "⚡ **The Sugar Rollercoaster!** Sugar gives you a super fast boost for 10 minutes like a rocket booster, but then it quickly runs out of fuel and you crash! That's why pairing fruit with protein or peanut butter keeps your energy steady all afternoon!",
            "water": "💧 **Hydration = Superhero Engine Coolant!** Water delivers oxygen to your brain and keeps your muscles from cramping when you sprint. Without water, your superhero speed drops by half!",
            "default": f"🦸‍♂️ **Coach Crunch says:** Great question! When you fuel your body with real foods (colorful veggies, strong proteins, and whole grains), your metabolism turns it into legendary hero power! Keep crushing your quests!"
        }
        for k in ["protein", "sugar", "water"]:
            if k in prompt_text.lower():
                return fallbacks[k]
        return fallbacks["default"]
    
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=effective_key)
        
        system_instruction = """
        You are 'Coach Crunch', a world-class, energetic, gamified nutrition coach for kids.
        Explain nutrition, metabolism, exercise, and healthy eating using superhero metaphors, video game analogies (armor, rocket fuel, shields, stamina meters, power-ups), and enthusiastic, age-appropriate language (ages 6-14).
        Keep responses concise (2-4 paragraphs max), positive, actionable, and fun! Include emojis.
        """
        
        # Build contents from recent chat
        formatted_contents = []
        for msg in chat_history[-6:]:
            formatted_contents.append(f"{msg['role'].upper()}: {msg['content']}")
        formatted_contents.append(f"USER: {prompt_text}")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="\n\n".join(formatted_contents),
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        return f"🦸‍♂️ **Coach Crunch:** Whoops! My superhero comms glitched ({str(e)}), but remember: eating colorful veggies and drinking plenty of water always gives you +100 Hero Vitality!"


# ==============================================================================
# SIDEBAR: SIBLING PROFILES, SWITCHER & LEADERBOARD PREVIEW
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#4F46E5; margin-bottom:0;'>👦👧 Hero Squad</h2>", unsafe_allow_html=True)
    st.caption("Switch active sibling profile or add a new hero!")
    
    siblings_dict = st.session_state.siblings
    sibling_keys = list(siblings_dict.keys())
    
    # Active Sibling Selector
    current_idx = sibling_keys.index(st.session_state.active_sibling_id) if st.session_state.active_sibling_id in sibling_keys else 0
    selected_sibling_id = st.selectbox(
        "Active Hero Profile",
        options=sibling_keys,
        index=current_idx,
        format_func=lambda k: f"{siblings_dict[k]['avatar']} {siblings_dict[k]['name']}"
    )
    st.session_state.active_sibling_id = selected_sibling_id
    active_sibling = siblings_dict[selected_sibling_id]
    
    # Active Sibling Stats Card
    lvl_title, lvl_prog, next_cap = get_level_info(active_sibling["xp"])
    tot_earned, unredeemed_cash = get_available_cash(active_sibling["xp"], active_sibling["cash_redeemed"])
    
    st.markdown(
        f"""
        <div class="profile-badge-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 2.2rem;">{active_sibling['avatar']}</span>
                <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.9rem;">
                    🔥 {active_sibling['streak']} Day Streak
                </span>
            </div>
            <h3 style="margin-top: 8px;">{active_sibling['name']}</h3>
            <p style="margin: 2px 0 8px 0; font-size: 0.85rem; opacity: 0.9;">{lvl_title}</p>
            <div style="background: rgba(0,0,0,0.2); border-radius: 8px; height: 10px; overflow: hidden; margin-bottom: 8px;">
                <div style="background: #10B981; width: {lvl_prog*100}%; height: 100%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 700;">
                <span>⚡ {active_sibling['xp']} Total XP</span>
                <span>💵 ${unredeemed_cash:.2f} Cash</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Add Sibling Expander
    with st.expander("➕ Add New Sibling / Hero"):
        with st.form("add_sibling_form", clear_on_submit=True):
            new_name = st.text_input("Hero Name", placeholder="e.g., Alex, Jordan")
            new_avatar = st.selectbox("Choose Avatar", ["⚡", "🌟", "🚀", "🐯", "🦖", "🦄", "⚽", "🏀", "🎨", "🛹"])
            submitted = st.form_submit_button("Join Hero Squad 🚀")
            if submitted and new_name.strip():
                new_key = f"kid_{len(siblings_dict)+1}_{new_name.lower().replace(' ', '_')}"
                st.session_state.siblings[new_key] = {
                    "name": new_name.strip(),
                    "avatar": new_avatar,
                    "xp": 50,
                    "streak": 1,
                    "cash_redeemed": 0.0,
                    "history": [
                        {
                            "time": "Just now",
                            "type": "Welcome Bonus",
                            "food": "Joined Plate Hero Squad",
                            "xp": 50,
                            "note": "Starter XP awarded!"
                        }
                    ]
                }
                st.session_state.active_sibling_id = new_key
                st.toast(f"🎉 Welcome to the squad, {new_name}!", icon="🦸‍♂️")
                st.rerun()

    st.markdown("---")
    
    # Preloaded Demo Quick Launchers
    st.markdown("<h4 style='color:#1E293B; margin-bottom: 6px;'>⚡ Quick Demo Plates</h4>", unsafe_allow_html=True)
    col_demo1, col_demo2 = st.columns(2)
    with col_demo1:
        if st.button("🍏 Apple & PB", use_container_width=True, help="Load Healthy Plate"):
            st.session_state.scan_result = DEMO_DATA["apple_pb"]
            if os.path.exists("assets/apple_peanut_butter.png"):
                st.session_state.scan_image_display = Image.open("assets/apple_peanut_butter.png")
            st.session_state.scan_base_claimed = False
            st.session_state.quest_claimed = False
            st.toast("Loaded Apple & Peanut Butter Plate!", icon="🍏")
            st.rerun()
            
    with col_demo2:
        if st.button("🍩 Frosted Donut", use_container_width=True, help="Load Sugary Plate"):
            st.session_state.scan_result = DEMO_DATA["frosted_donut"]
            if os.path.exists("assets/frosted_donut.png"):
                st.session_state.scan_image_display = Image.open("assets/frosted_donut.png")
            st.session_state.scan_base_claimed = False
            st.session_state.quest_claimed = False
            st.toast("Loaded Frosted Sugar Donut Plate!", icon="🍩")
            st.rerun()

    st.markdown("---")
    
    # API Key Settings & Reset
    with st.expander("⚙️ Settings & Gemini Key"):
        user_key = st.text_input(
            "Gemini API Key",
            value=st.session_state.get("api_key", os.environ.get("GEMINI_API_KEY", "")),
            type="password",
            help="Optional: Enter your Gemini API key to call live Gemini 2.5 Flash for custom photos."
        )
        if user_key:
            st.session_state.api_key = user_key
            
        if st.button("🔄 Reset Demo State", use_container_width=True):
            st.session_state.siblings = DEFAULT_SIBLINGS.copy()
            st.session_state.active_sibling_id = "kid_leo"
            st.session_state.scan_result = None
            st.session_state.scan_image_display = None
            st.session_state.scan_base_claimed = False
            st.session_state.quest_claimed = False
            st.toast("Demo state reset to default!", icon="🔄")
            st.rerun()


# ==============================================================================
# MAIN PAGE HEADER BANNER
# ==============================================================================
st.markdown(
    f"""
    <div class="hero-banner">
        <div>
            <h1>🦸‍♂️ Plate Hero: Sibling Nutrition & Fitness Arena</h1>
            <p>Scan your meal, simulate your metabolism, defeat sugar spikes, and earn Hero Cash!</p>
        </div>
        <div style="background: rgba(255,255,255,0.25); padding: 10px 18px; border-radius: 14px; text-align: center;">
            <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 800;">Active Hero</div>
            <div style="font-size: 1.4rem; font-weight: 800;">{active_sibling['avatar']} {active_sibling['name']}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# TABS SETUP
# ==============================================================================
tab1, tab2, tab3 = st.tabs([
    "📸 Plate Scanner & Metabolism Simulator",
    "💬 Hero Coach Q&A",
    "🏆 Sibling Scorecard & Cash Bank"
])


# ==============================================================================
# TAB 1: PLATE SCANNER & METABOLISM SIMULATOR
# ==============================================================================
with tab1:
    st.markdown("### 📸 Scan Your Plate & Power Up")
    st.caption("Snap a photo of your meal or snack to see what superhero superpowers it gives your body!")
    
    col_input, col_analysis = st.columns([1.1, 1.3], gap="large")
    
    with col_input:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        st.markdown("#### 📷 Capture or Upload Meal")
        
        input_mode = st.radio("Choose Input Method:", ["📸 Live Camera", "📁 File Upload", "✨ Preloaded Demos"], horizontal=True)
        
        uploaded_file = None
        if input_mode == "📸 Live Camera":
            camera_img = st.camera_input("Take a photo of your plate")
            if camera_img:
                uploaded_file = camera_img
        elif input_mode == "📁 File Upload":
            file_img = st.file_uploader("Upload plate image", type=["png", "jpg", "jpeg", "webp"])
            if file_img:
                uploaded_file = file_img
        else:
            st.info("👈 You can also click the quick demo buttons on the sidebar anytime!")
            demo_choice = st.selectbox("Select a demo plate:", ["🍏 Crunchy Apple & Peanut Butter", "🍩 Frosted Sugar Donut"])
            if st.button("🚀 Load Selected Demo Plate", use_container_width=True):
                if "Apple" in demo_choice:
                    st.session_state.scan_result = DEMO_DATA["apple_pb"]
                    if os.path.exists("assets/apple_peanut_butter.png"):
                        st.session_state.scan_image_display = Image.open("assets/apple_peanut_butter.png")
                else:
                    st.session_state.scan_result = DEMO_DATA["frosted_donut"]
                    if os.path.exists("assets/frosted_donut.png"):
                        st.session_state.scan_image_display = Image.open("assets/frosted_donut.png")
                st.session_state.scan_base_claimed = False
                st.session_state.quest_claimed = False
                st.rerun()

        if uploaded_file is not None:
            pil_img = Image.open(uploaded_file)
            st.session_state.scan_image_display = pil_img
            st.image(pil_img, caption="Plate to Analyze", use_container_width=True)
            
            if st.button("⚡ Analyze Plate with Gemini 2.5 Flash", type="primary", use_container_width=True):
                with st.spinner("🤖 Gemini 2.5 Flash is inspecting your nutrients and building your quest..."):
                    api_key_val = st.session_state.get("api_key", os.environ.get("GEMINI_API_KEY"))
                    result = call_gemini_plate_scanner(pil_img, api_key=api_key_val)
                    st.session_state.scan_result = result
                    st.session_state.scan_base_claimed = False
                    st.session_state.quest_claimed = False
                    st.rerun()
                    
        elif st.session_state.scan_image_display is not None:
            st.image(st.session_state.scan_image_display, caption="Current Plate in Simulator", use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_analysis:
        if st.session_state.scan_result is None:
            st.markdown('<div class="hero-card" style="text-align:center; padding: 40px 20px;">', unsafe_allow_html=True)
            st.markdown("### 🍽️ No Plate Scanned Yet!")
            st.markdown("Snap a picture on the left or try the **🍏 Apple & PB** or **🍩 Frosted Donut** buttons in the sidebar to simulate your metabolism!")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            scan = st.session_state.scan_result
            macros = scan.get("macro_breakdown", {})
            food_items = scan.get("food_items", [])
            story = scan.get("metabolism_story", "")
            base_xp = scan.get("base_xp", 30)
            quest = scan.get("hero_quest", {"activity": "10 Jumping Jacks", "xp_reward": 25})
            
            st.markdown('<div class="hero-card">', unsafe_allow_html=True)
            
            # Header with Food Items Badges
            st.markdown("#### 🥗 Identified Foods & Nutrients")
            badges_html = "".join([f'<span class="badge-chip badge-protein">{item}</span>' for item in food_items])
            st.markdown(badges_html, unsafe_allow_html=True)
            
            # Base XP Claim Box
            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            col_xp_txt, col_xp_btn = st.columns([1.5, 1])
            with col_xp_txt:
                st.markdown(f"**Plate Scan Reward:** `+{base_xp} Base XP`")
            with col_xp_btn:
                if not st.session_state.scan_base_claimed:
                    if st.button(f"🎁 Claim +{base_xp} XP", use_container_width=True):
                        st.session_state.siblings[st.session_state.active_sibling_id]["xp"] += base_xp
                        st.session_state.siblings[st.session_state.active_sibling_id]["history"].insert(0, {
                            "time": datetime.now().strftime("%I:%M %p"),
                            "type": "Plate Scan",
                            "food": ", ".join(food_items[:2]),
                            "xp": base_xp,
                            "note": "Nutrient scan verified"
                        })
                        st.session_state.scan_base_claimed = True
                        play_sound("fanfare")
                        st.balloons()
                        st.toast(f"🌟 +{base_xp} XP added to {active_sibling['name']}'s Bank!", icon="🎉")
                        st.rerun()
                else:
                    st.success("✅ Base XP Claimed!")

            st.markdown("---")

            # Macro Progress Bars
            st.markdown("#### ⚡ Super Macro Breakdown")
            
            def macro_to_val(level_str):
                lvl = str(level_str).lower()
                if "high" in lvl:
                    return 0.90, "HIGH (90%)", "#10B981"
                elif "med" in lvl:
                    return 0.55, "MED (55%)", "#3B82F6"
                else:
                    return 0.20, "LOW (20%)", "#9CA3AF"

            def sugar_to_val(level_str):
                lvl = str(level_str).lower()
                if "high" in lvl:
                    return 0.90, "HIGH (Risk of Crash!) 🚨", "#EF4444"
                elif "med" in lvl:
                    return 0.50, "MED (Moderate)", "#F59E0B"
                else:
                    return 0.15, "LOW (Stable Stamina) 🛡️", "#10B981"

            # Protein Bricks
            p_val, p_lbl, _ = macro_to_val(macros.get("protein_bricks", "Med"))
            st.markdown(f"**🧱 Protein Bricks (Muscle Building & Repair):** `{p_lbl}`")
            st.progress(p_val)
            
            # Battery Fuel
            b_val, b_lbl, _ = macro_to_val(macros.get("battery_fuel", "Med"))
            st.markdown(f"**⚡ Battery Fuel (Long-Lasting Stamina):** `{b_lbl}`")
            st.progress(b_val)
            
            # Sugar Spike
            s_val, s_lbl, _ = sugar_to_val(macros.get("sugar_spike", "Low"))
            st.markdown(f"**🚨 Sugar Spike (Rush vs Crash Level):** `{s_lbl}`")
            st.progress(s_val)

            # Brain Armor
            br_val, br_lbl, _ = macro_to_val(macros.get("brain_armor", "Med"))
            st.markdown(f"**🛡️ Brain Armor (Vitamins & Shielding):** `{br_lbl}`")
            st.progress(br_val)

            # Metabolism Simulator Story
            st.markdown("#### 🧬 Metabolism Simulator Story")
            st.markdown(f'<div class="story-box">{story}</div>', unsafe_allow_html=True)

            # Hero Quest Card
            st.markdown(
                f"""
                <div class="quest-card">
                    <div class="quest-title">🎯 Active Hero Quest: Burn Fuel & Boost Metabolism!</div>
                    <p style="font-size: 1.1rem; margin: 0; color: #064E3B; font-weight:700;">{quest.get('activity', '10 Jumping Jacks')}</p>
                    <div style="margin-top: 8px; font-weight: 800; color: #047857;">🏆 Quest Reward: +{quest.get('xp_reward', 30)} XP</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Complete Quest Button
            if not st.session_state.quest_claimed:
                if st.button(f"✅ Complete Quest & Claim +{quest.get('xp_reward', 30)} XP", type="primary", use_container_width=True):
                    q_xp = quest.get("xp_reward", 30)
                    st.session_state.siblings[st.session_state.active_sibling_id]["xp"] += q_xp
                    st.session_state.siblings[st.session_state.active_sibling_id]["history"].insert(0, {
                        "time": datetime.now().strftime("%I:%M %p"),
                        "type": "Hero Quest",
                        "food": quest.get("activity", "Physical Quest"),
                        "xp": q_xp,
                        "note": "Quest completed!"
                    })
                    st.session_state.quest_claimed = True
                    play_sound("fanfare")
                    st.balloons()
                    st.toast(f"🔥 Quest Completed! +{q_xp} XP for {active_sibling['name']}!", icon="💪")
                    st.rerun()
            else:
                st.success(f"🎉 Quest Completed! +{quest.get('xp_reward', 30)} XP Claimed by {active_sibling['name']}!")

            st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# TAB 2: HERO COACH Q&A
# ==============================================================================
with tab2:
    st.markdown("### 💬 Hero Coach Q&A with Coach Crunch")
    st.caption("Ask questions about muscles, sports energy, vegetables, or how snacks power your hero moves!")
    
    col_chat_main, col_chat_side = st.columns([2, 1], gap="large")
    
    with col_chat_side:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        st.markdown("#### 💡 Quick Questions")
        st.caption("Click any question to ask Coach Crunch instantly:")
        
        sample_questions = [
            "Why do I need protein after soccer? ⚽",
            "What does sugar do to my brain? 🧠",
            "Why is water better than soda for sprinting? 🏃‍♂️",
            "How do carrots and spinach give me super vision? 🥕",
            "What is a good pre-game superhero snack? 🍌"
        ]
        
        for q in sample_questions:
            if st.button(q, use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": q})
                with st.spinner("Coach Crunch is thinking..."):
                    api_key_val = st.session_state.get("api_key", os.environ.get("GEMINI_API_KEY"))
                    reply = call_gemini_hero_coach(q, st.session_state.chat_history, api_key=api_key_val)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()
                
        if st.button("🧹 Clear Chat History", use_container_width=True):
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": f"👋 Hey {active_sibling['name']}! Ready for more nutrition power-ups? Ask me anything!"
                }
            ]
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_chat_main:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        
        # Render Chat History
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user", avatar=active_sibling["avatar"]):
                    st.markdown(f"**{active_sibling['name']}:** {message['content']}")
            else:
                with st.chat_message("assistant", avatar="🥦"):
                    st.markdown(message["content"])

        # Chat Input
        user_input = st.chat_input("Ask Coach Crunch a question about food, energy, or training...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user", avatar=active_sibling["avatar"]):
                st.markdown(f"**{active_sibling['name']}:** {user_input}")
                
            with st.chat_message("assistant", avatar="🥦"):
                with st.spinner("Coach Crunch is analyzing your hero question..."):
                    api_key_val = st.session_state.get("api_key", os.environ.get("GEMINI_API_KEY"))
                    coach_response = call_gemini_hero_coach(user_input, st.session_state.chat_history, api_key=api_key_val)
                    st.markdown(coach_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": coach_response})
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# TAB 3: SIBLING SCORECARD & CASH BANK
# ==============================================================================
with tab3:
    st.markdown("### 🏆 Sibling Scorecard & Hero Cash Bank")
    st.caption("Track family ranks, redeem allowance cash rewards (100 XP = $1.00), and view activity history!")
    
    # Leaderboard Cards
    ranked_siblings = sorted(
        st.session_state.siblings.items(),
        key=lambda item: item[1]["xp"],
        reverse=True
    )
    
    col_lb, col_bank = st.columns([1.4, 1], gap="large")
    
    with col_lb:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        st.markdown("#### 🥇 Global Sibling Leaderboard")
        
        rank_medals = ["🥇 1st Place", "🥈 2nd Place", "🥉 3rd Place", "4th Place", "5th Place"]
        
        for rank_idx, (sib_id, sib_data) in enumerate(ranked_siblings):
            is_active = (sib_id == st.session_state.active_sibling_id)
            lvl_lbl, _, _ = get_level_info(sib_data["xp"])
            _, unredeemed = get_available_cash(sib_data["xp"], sib_data["cash_redeemed"])
            medal = rank_medals[rank_idx] if rank_idx < len(rank_medals) else f"#{rank_idx+1}"
            
            border_style = "border: 2px solid #6366F1; background: #F5F3FF;" if is_active else "border: 1px solid #E5E7EB; background: #FFFFFF;"
            
            st.markdown(
                f"""
                <div style="padding: 14px 18px; border-radius: 14px; margin-bottom: 10px; {border_style} display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-weight: 800; font-size: 1.1rem; color: #4338CA;">{medal}</span>
                        <span style="font-size: 1.8rem;">{sib_data['avatar']}</span>
                        <div>
                            <div style="font-weight: 800; font-size: 1.15rem; color: #1E293B;">
                                {sib_data['name']} {'⭐ (Active)' if is_active else ''}
                            </div>
                            <div style="font-size: 0.85rem; color: #64748B;">{lvl_lbl}</div>
                        </div>
                    </div>
                    <div style="text-align: right; margin-top: 4px;">
                        <div style="font-weight: 800; font-size: 1.1rem; color: #059669;">⚡ {sib_data['xp']} XP</div>
                        <div style="font-size: 0.85rem; font-weight: 700; color: #D97706;">🔥 {sib_data['streak']} Days | 💵 ${unredeemed:.2f}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_bank:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        st.markdown("#### 💰 Hero Cash Bank (Parent Console)")
        
        # Calculate Total Family Bank
        total_family_xp = sum(s["xp"] for s in st.session_state.siblings.values())
        total_family_cash_earned = total_family_xp / 100.0
        total_family_redeemed = sum(s["cash_redeemed"] for s in st.session_state.siblings.values())
        total_family_unredeemed = max(0.0, total_family_cash_earned - total_family_redeemed)
        
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); color: white; padding: 18px; border-radius: 16px; text-align: center; margin-bottom: 16px;">
                <div style="font-size: 0.9rem; text-transform: uppercase; font-weight: 700; opacity: 0.9;">Total Payout Available</div>
                <div style="font-size: 2.3rem; font-weight: 800; margin: 4px 0;">${total_family_unredeemed:.2f}</div>
                <div style="font-size: 0.85rem; opacity: 0.95;">100 XP = $1.00 USD Real Reward Allowance</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("##### 💵 Redeem Cash Payout")
        target_sibling_id = st.selectbox(
            "Select Sibling to Redeem Cash:",
            options=sibling_keys,
            format_func=lambda k: f"{siblings_dict[k]['avatar']} {siblings_dict[k]['name']}"
        )
        
        target_sib = st.session_state.siblings[target_sibling_id]
        _, target_unredeemed = get_available_cash(target_sib["xp"], target_sib["cash_redeemed"])
        
        st.write(f"**Available for {target_sib['name']}:** `${target_unredeemed:.2f}` (Total XP: {target_sib['xp']})")
        
        if target_unredeemed > 0:
            redeem_amount = st.number_input(
                "Redeem Amount ($)",
                min_value=0.50,
                max_value=float(target_unredeemed),
                value=min(1.00, float(target_unredeemed)),
                step=0.50
            )
            
            parent_confirm = st.checkbox("🔒 Parent Verification: I have handed real cash/coins to the hero!")
            
            if st.button(f"💵 Redeem ${redeem_amount:.2f} for {target_sib['name']}", type="primary", use_container_width=True):
                if parent_confirm:
                    st.session_state.siblings[target_sibling_id]["cash_redeemed"] += redeem_amount
                    st.session_state.siblings[target_sibling_id]["history"].insert(0, {
                        "time": datetime.now().strftime("%I:%M %p"),
                        "type": "Cash Payout",
                        "food": f"Redeemed ${redeem_amount:.2f} Hero Cash",
                        "xp": 0,
                        "note": "Paid out by parent"
                    })
                    play_sound("fanfare")
                    st.snow()
                    st.success(f"🎉 Paid out ${redeem_amount:.2f} to {target_sib['name']}! Great job fueling up healthy!")
                    st.rerun()
                else:
                    st.warning("Please check parent verification box above to confirm payout.")
        else:
            st.info(f"{target_sib['name']} has redeemed all available cash! Scan more healthy plates to earn more!")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # Activity History Log Section
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    st.markdown("#### 📜 Activity History Log")
    
    col_filter_sib, col_filter_type = st.columns([1, 1])
    with col_filter_sib:
        hist_filter = st.selectbox(
            "Filter History by Sibling:",
            options=["All Siblings"] + sibling_keys,
            format_func=lambda k: "All Siblings" if k == "All Siblings" else f"{siblings_dict[k]['avatar']} {siblings_dict[k]['name']}"
        )
        
    all_history_entries = []
    if hist_filter == "All Siblings":
        for s_id, s_data in st.session_state.siblings.items():
            for item in s_data.get("history", []):
                all_history_entries.append({
                    "sibling_name": s_data["name"],
                    "avatar": s_data["avatar"],
                    **item
                })
    else:
        s_data = st.session_state.siblings[hist_filter]
        for item in s_data.get("history", []):
            all_history_entries.append({
                "sibling_name": s_data["name"],
                "avatar": s_data["avatar"],
                **item
            })
            
    if all_history_entries:
        for entry in all_history_entries[:15]:
            icon_type = "📸" if entry.get("type") == "Plate Scan" else ("🎯" if entry.get("type") == "Hero Quest" else "💵")
            st.markdown(
                f"""
                <div style="border-bottom: 1px solid #F1F5F9; padding: 10px 0; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-size: 1.2rem; margin-right: 6px;">{entry.get('avatar', '🦸')}</span>
                        <strong style="color: #1E293B;">{entry.get('sibling_name', '')}</strong>
                        <span style="color: #64748B; margin-left: 8px;">{icon_type} {entry.get('type')}: {entry.get('food')}</span>
                        <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 2px;">{entry.get('note', '')} • {entry.get('time')}</div>
                    </div>
                    <div>
                        <span style="font-weight: 800; color: {'#059669' if entry.get('xp', 0) > 0 else '#2563EB'};">
                            {f'+{entry.get("xp")} XP' if entry.get("xp", 0) > 0 else 'Cash Claimed'}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("No activity history yet. Complete scans and quests to fill the log!")
        
    st.markdown('</div>', unsafe_allow_html=True)
