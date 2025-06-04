# app.py
import streamlit as st
import json
import os
from groq import Groq
from typing import Dict, List

# Page config
st.set_page_config(
    page_title="شف‌بات | ChefBot",
    page_icon="🧑‍🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Groq client
@st.cache_resource
def init_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY", "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")
    return Groq(api_key=api_key)

# Load menu data
@st.cache_data
def load_menu_data():
    try:
        with open('menu_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("فایل منو یافت نشد | Menu file not found")
        return {"cafe_menu": []}

def get_menu_item_by_id(item_id: int, menu_data: dict, language: str):
    """Get menu item by ID in specified language"""
    for item in menu_data['cafe_menu']:
        if item['id'] == item_id:
            return {
                'id': item['id'],
                'name': item[f'name_{language}'],
                'category': item[f'category_{language}'],
                'ingredients': item[f'ingredients_{language}'],
                'health_flags': item['health_flags']
            }
    return None

def generate_system_prompt(language: str, mode: str, menu_data: dict):
    """Generate system prompt based on language and mode"""
    
    menu_text = ""
    for item in menu_data['cafe_menu']:
        menu_text += f"ID: {item['id']}, Name: {item[f'name_{language}']}, Category: {item[f'category_{language}']}, Health Flags: {item['health_flags']}\n"
    
    if language == 'fa':
        if mode == 'free_chat':
            return f"""شما یک سرآشپز ماهر و مشاور تخصصی کافه هستید. با کاربران به صورت دوستانه و صمیمی صحبت کنید.
منوی کافه:
{menu_text}

وظایف شما:
1. با کاربر گفتگوی طبیعی داشته باشید
2. در صورت تشخیص مشکل سلامتی، سوال مناسب بپرسید
3. پیشنهادات شخصی‌سازی شده ارائه دهید
4. فقط از آیتم‌های موجود در منو پیشنهاد دهید

health_flags meanings:
- lactose: حاوی لاکتوز
- gluten: حاوی گلوتن  
- caffeine: حاوی کافئین زیاد
- high_sugar: شکر زیاد
- nuts: حاوی آجیل
- eggs: حاوی تخم‌مرغ"""

        elif mode == 'guided':
            return f"""شما یک مشاور تخصصی کافه هستید که سوالات مرحله‌ای می‌پرسید.
منوی کافه:
{menu_text}

مراحل کار:
1. سلامت: آلرژی، دیابت، حساسیت‌ها
2. مود: انرژی، آرامش، استرس
3. ترجیحات: طعم، بافت، دما
4. پیشنهاد نهایی

در هر مرحله فقط 1-2 سوال بپرسید."""

        else:  # validation mode
            return f"""شما یک مشاور امنیت غذایی هستید. کاربر آیتمی انتخاب کرده و شما باید بررسی کنید.
منوی کافه:
{menu_text}

اگر آیتم انتخابی health_flag خطرناک دارد، سوال مناسب بپرسید:
- lactose → "حساسیت به لاکتوز نداری؟"
- gluten → "سلیاک یا حساسیت به گلوتن نداری؟"  
- high_sugar → "دیابت نداری؟"
- caffeine → "مشکل قلبی یا اضطراب نداری؟"

اگر مشکلی بود، جایگزین مناسب پیشنهاد دهید."""
    
    else:  # English
        if mode == 'free_chat':
            return f"""You are an expert chef and cafe consultant. Chat naturally and friendly with users.
Cafe Menu:
{menu_text}

Your tasks:
1. Have natural conversations with users
2. Ask appropriate health questions if you detect potential issues
3. Provide personalized recommendations
4. Only suggest items from the available menu

health_flags meanings:
- lactose: Contains lactose
- gluten: Contains gluten
- caffeine: High caffeine content
- high_sugar: High sugar content
- nuts: Contains nuts
- eggs: Contains eggs"""

        elif mode == 'guided':
            return f"""You are a professional cafe consultant who asks step-by-step questions.
Cafe Menu:
{menu_text}

Process steps:
1. Health: Allergies, diabetes, sensitivities
2. Mood: Energy, relaxation, stress
3. Preferences: Taste, texture, temperature
4. Final recommendation

Ask only 1-2 questions per step."""

        else:  # validation mode
            return f"""You are a food safety consultant. User has selected an item and you need to verify it's safe.
Cafe Menu:
{menu_text}

If selected item has dangerous health_flags, ask appropriate questions:
- lactose → "Do you have lactose intolerance?"
- gluten → "Do you have celiac disease or gluten sensitivity?"
- high_sugar → "Do you have diabetes?"
- caffeine → "Do you have heart problems or anxiety?"

If there's an issue, suggest suitable alternatives."""

def chat_with_groq(messages: List[Dict], system_prompt: str):
    """Send messages to Groq and get response"""
    try:
        client = init_groq_client()
        
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instant",
            messages=full_messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"خطا در ارتباط | Connection error: {str(e)}"

def main():
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 'language_selection'
    if 'language' not in st.session_state:
        st.session_state.language = None
    if 'mode' not in st.session_state:
        st.session_state.mode = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'selected_item' not in st.session_state:
        st.session_state.selected_item = None
    if 'menu_data' not in st.session_state:
        st.session_state.menu_data = load_menu_data()

    # Show appropriate step
    if st.session_state.step == 'language_selection':
        show_language_selection()
    elif st.session_state.step == 'mode_selection':
        show_mode_selection()
    elif st.session_state.step == 'menu_display':
        show_menu_selection()
    elif st.session_state.step == 'chat_interface':
        show_chat_interface()

def show_language_selection():
    """Language selection page"""
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.title("🧑‍🍳 ChefBot")
    st.markdown("### Choose Your Language | زبان خود را انتخاب کنید")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.write("")
    
    with col2:
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🇮🇷 فارسی", use_container_width=True, height=80):
                st.session_state.language = 'fa'
                st.session_state.step = 'mode_selection'
                st.rerun()
        
        with col_b:
            if st.button("🇺🇸 English", use_container_width=True, height=80):
                st.session_state.language = 'en'
                st.session_state.step = 'mode_selection'
                st.rerun()
    
    with col3:
        st.write("")

def show_mode_selection():
    """Show the three interaction modes in a fun way"""
    lang = st.session_state.language
    
    # Header
    if lang == 'fa':
        st.title("🧑‍🍳 سلام! من شف‌بات هستم")
        st.markdown("### چطور می‌تونم کمکت کنم؟")
        st.markdown("---")
    else:
        st.title("🧑‍🍳 Hello! I'm ChefBot")
        st.markdown("### How can I help you today?")
        st.markdown("---")
    
    # Three fun options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if lang == 'fa':
            st.markdown("#### 🤔 نمی‌دونم چی بخورم!")
            st.markdown("بیا با هم حرف بزنیم و ببینیم چی برات مناسبه")
            if st.button("💬 گفتگو کنیم", use_container_width=True):
                st.session_state.mode = 'free_chat'
                st.session_state.step = 'chat_interface'
                st.rerun()
        else:
            st.markdown("#### 🤔 I don't know what to eat!")
            st.markdown("Let's chat and see what suits you best")
            if st.button("💬 Let's Chat", use_container_width=True):
                st.session_state.mode = 'free_chat'
                st.session_state.step = 'chat_interface'
                st.rerun()
    
    with col2:
        if lang == 'fa':
            st.markdown("#### 📝 پیشنهاد شخصی‌سازی‌شده می‌خوام")
            st.markdown("چندتا سوال ازت می‌پرسم و بهترین گزینه رو پیدا می‌کنیم")
            if st.button("📋 شروع سوالات", use_container_width=True):
                st.session_state.mode = 'guided'
                st.session_state.step = 'chat_interface'
                st.rerun()
        else:
            st.markdown("#### 📝 I want personalized suggestions")
            st.markdown("I'll ask you a few questions to find the perfect choice")
            if st.button("📋 Start Questions", use_container_width=True):
                st.session_state.mode = 'guided'
                st.session_state.step = 'chat_interface'
                st.rerun()
    
    with col3:
        if lang == 'fa':
            st.markdown("#### ✅ می‌دونم چی می‌خوام")
            st.markdown("از منو انتخاب کن، من فقط چک می‌کنم مناسب باشه")
            if st.button("📜 نمایش منو", use_container_width=True):
                st.session_state.mode = 'validation'
                st.session_state.step = 'menu_display'
                st.rerun()
        else:
            st.markdown("#### ✅ I know what I want")
            st.markdown("Choose from menu, I'll just check if it's suitable for you")
            if st.button("📜 Show Menu", use_container_width=True):
                st.session_state.mode = 'validation'
                st.session_state.step = 'menu_display'
                st.rerun()
    
    # Back button
    st.markdown("---")
    if st.button("🔙 تغییر زبان | Change Language"):
        st.session_state.step = 'language_selection'
        st.session_state.language = None
        st.rerun()

def show_menu_selection():
    """Display menu for selection in validation mode"""
    lang = st.session_state.language
    menu_data = st.session_state.menu_data
    
    if lang == 'fa':
        st.title("📜 منوی کافه")
        st.markdown("### چی دوست داری بخوری؟")
    else:
        st.title("📜 Cafe Menu")
        st.markdown("### What would you like to have?")
    
    # Group items by category
    categories = {}
    for item in menu_data['cafe_menu']:
        cat = item[f'category_{lang}']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    # Display menu by categories
    for category, items in categories.items():
        st.markdown(f"### {category}")
        
        cols = st.columns(2)
        for idx, item in enumerate(items):
            with cols[idx % 2]:
                st.markdown(f"**{item[f'name_{lang}']}**")
                ingredients = ", ".join(item[f'ingredients_{lang}'][:3])
                if len(item[f'ingredients_{lang}']) > 3:
                    ingredients += "..."
                st.markdown(f"*{ingredients}*")
                
                if st.button(f"انتخاب | Select", key=f"select_{item['id']}"):
                    st.session_state.selected_item = item['id']
                    st.session_state.step = 'chat_interface'
                    # Initialize validation conversation
                    selected_item = get_menu_item_by_id(item['id'], menu_data, lang)
                    if lang == 'fa':
                        initial_message = f"من {selected_item['name']} رو انتخاب کردم."
                    else:
                        initial_message = f"I selected {selected_item['name']}."
                    
                    st.session_state.messages = [{"role": "user", "content": initial_message}]
                    st.rerun()
                st.markdown("---")
    
    # Back button
    if st.button("🔙 بازگشت | Back"):
        st.session_state.step = 'mode_selection'
        st.rerun()

def show_chat_interface():
    """Main chat interface"""
    lang = st.session_state.language
    mode = st.session_state.mode
    menu_data = st.session_state.menu_data
    
    # Header with mode info
    mode_names = {
        'fa': {
            'free_chat': '💬 گفتگوی آزاد',
            'guided': '📋 راهنمایی مرحله‌ای',
            'validation': '✅ بررسی انتخاب'
        },
        'en': {
            'free_chat': '💬 Free Chat',
            'guided': '📋 Guided Assessment',
            'validation': '✅ Selection Validation'
        }
    }
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### {mode_names[lang][mode]}")
    with col2:
        if st.button("🔄 شروع مجدد | Restart"):
            st.session_state.step = 'mode_selection'
            st.session_state.messages = []
            st.session_state.selected_item = None
            st.rerun()
    
    # Chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("پیام خود را بنویسید | Type your message"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response
        system_prompt = generate_system_prompt(lang, mode, menu_data)
        response = chat_with_groq(st.session_state.messages, system_prompt)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
        
        st.rerun()
    
    # Initial message for guided mode
    if mode == 'guided' and len(st.session_state.messages) == 0:
        system_prompt = generate_system_prompt(lang, mode, menu_data)
        if lang == 'fa':
            initial_prompt = "سلام! بیا شروع کنیم. اول بگو آلرژی خاصی داری؟"
        else:
            initial_prompt = "Hello! Let's start. First, do you have any specific allergies?"
        
        st.session_state.messages.append({"role": "assistant", "content": initial_prompt})
        st.rerun()

if __name__ == "__main__":
    main()
