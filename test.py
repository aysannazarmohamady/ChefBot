import streamlit as st
import json
import os
from typing import Dict, List

# Page config
st.set_page_config(
    page_title="شف‌بات | ChefBot",
    page_icon="🧑‍🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def init_groq_client():
    """Initialize Groq client"""
    try:
        from groq import Groq
        api_key = "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"
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Groq: {str(e)}")
        return None

def load_menu_data():
    """Load menu data from JSON file"""
    sample_data = {
        "cafe_menu": [
            {
                "id": 1,
                "name_fa": "اسپرسو",
                "name_en": "Espresso",
                "category_fa": "قهوه",
                "category_en": "Coffee",
                "ingredients_fa": ["دانه قهوه آسیاب شده", "آب"],
                "ingredients_en": ["Ground coffee beans", "Water"],
                "health_flags": ["caffeine"]
            },
            {
                "id": 2,
                "name_fa": "کیک شکلاتی",
                "name_en": "Chocolate Cake",
                "category_fa": "کیک",
                "category_en": "Cake",
                "ingredients_fa": ["آرد", "شکلات", "تخم مرغ", "شکر"],
                "ingredients_en": ["Flour", "Chocolate", "Eggs", "Sugar"],
                "health_flags": ["gluten", "high_sugar", "eggs"]
            },
            {
                "id": 3,
                "name_fa": "سالاد سزار",
                "name_en": "Caesar Salad",
                "category_fa": "سالاد",
                "category_en": "Salad",
                "ingredients_fa": ["کاهو رومی", "پنیر پارمزان", "کروتون"],
                "ingredients_en": ["Romaine lettuce", "Parmesan cheese", "Croutons"],
                "health_flags": ["gluten", "lactose"]
            }
        ]
    }
    
    try:
        with open('menu_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return sample_data

def generate_system_prompt(language: str, mode: str, menu_data: dict):
    """Generate system prompt"""
    menu_text = ""
    for item in menu_data['cafe_menu']:
        menu_text += f"ID: {item['id']}, Name: {item[f'name_{language}']}, Health Flags: {item['health_flags']}\n"
    
    if language == 'fa':
        return f"""شما یک سرآشپز ماهر هستید. با کاربران دوستانه صحبت کنید.
منوی کافه:
{menu_text}

در صورت مشکل سلامتی، سوال مناسب بپرسید."""
    else:
        return f"""You are an expert chef. Chat friendly with users.
Cafe Menu:
{menu_text}

Ask appropriate health questions if needed."""

def chat_with_groq(messages: List[Dict], system_prompt: str):
    """Send messages to Groq"""
    try:
        client = init_groq_client()
        if not client:
            return "خطا در اتصال | Connection error"
        
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=full_messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"خطا | Error: {str(e)}"

def main():
    """Main app function"""
    
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 'language_selection'
    if 'language' not in st.session_state:
        st.session_state.language = None
    if 'mode' not in st.session_state:
        st.session_state.mode = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'menu_data' not in st.session_state:
        st.session_state.menu_data = load_menu_data()

    # Language Selection
    if st.session_state.step == 'language_selection':
        st.title("🧑‍🍳 ChefBot")
        st.markdown("### Choose Your Language | زبان خود را انتخاب کنید")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🇮🇷 فارسی", use_container_width=True):
                st.session_state.language = 'fa'
                st.session_state.step = 'mode_selection'
                st.rerun()
        
        with col2:
            if st.button("🇺🇸 English", use_container_width=True):
                st.session_state.language = 'en'
                st.session_state.step = 'mode_selection'
                st.rerun()

    # Mode Selection
    elif st.session_state.step == 'mode_selection':
        lang = st.session_state.language
        
        if lang == 'fa':
            st.title("🧑‍🍳 سلام! من شف‌بات هستم")
            st.markdown("### چطور می‌تونم کمکت کنم؟")
        else:
            st.title("🧑‍🍳 Hello! I'm ChefBot")
            st.markdown("### How can I help you today?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if lang == 'fa':
                st.markdown("#### 💬 گفتگوی آزاد")
                if st.button("شروع گفتگو", use_container_width=True):
                    st.session_state.mode = 'free_chat'
                    st.session_state.step = 'chat'
                    st.rerun()
            else:
                st.markdown("#### 💬 Free Chat")
                if st.button("Start Chat", use_container_width=True):
                    st.session_state.mode = 'free_chat'
                    st.session_state.step = 'chat'
                    st.rerun()
        
        with col2:
            if lang == 'fa':
                st.markdown("#### 📋 راهنمایی مرحله‌ای")
                if st.button("شروع سوالات", use_container_width=True):
                    st.session_state.mode = 'guided'
                    st.session_state.step = 'chat'
                    st.rerun()
            else:
                st.markdown("#### 📋 Guided Questions")
                if st.button("Start Questions", use_container_width=True):
                    st.session_state.mode = 'guided'
                    st.session_state.step = 'chat'
                    st.rerun()
        
        with col3:
            if lang == 'fa':
                st.markdown("#### ✅ بررسی انتخاب")
                if st.button("نمایش منو", use_container_width=True):
                    st.session_state.mode = 'validation'
                    st.session_state.step = 'menu'
                    st.rerun()
            else:
                st.markdown("#### ✅ Menu Selection")
                if st.button("Show Menu", use_container_width=True):
                    st.session_state.mode = 'validation'
                    st.session_state.step = 'menu'
                    st.rerun()
        
        if st.button("🔙 تغییر زبان | Change Language"):
            st.session_state.step = 'language_selection'
            st.rerun()

    # Menu Display
    elif st.session_state.step == 'menu':
        lang = st.session_state.language
        menu_data = st.session_state.menu_data
        
        if lang == 'fa':
            st.title("📜 منوی کافه")
        else:
            st.title("📜 Cafe Menu")
        
        for item in menu_data['cafe_menu']:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{item[f'name_{lang}']}**")
                ingredients = ", ".join(item[f'ingredients_{lang}'][:2])
                st.markdown(f"*{ingredients}...*")
            
            with col2:
                if st.button("انتخاب", key=f"select_{item['id']}"):
                    st.session_state.step = 'chat'
                    if lang == 'fa':
                        msg = f"من {item[f'name_{lang}']} رو انتخاب کردم."
                    else:
                        msg = f"I selected {item[f'name_{lang}']}."
                    st.session_state.messages = [{"role": "user", "content": msg}]
                    st.rerun()
        
        if st.button("🔙 بازگشت | Back"):
            st.session_state.step = 'mode_selection'
            st.rerun()

    # Chat Interface
    elif st.session_state.step == 'chat':
        lang = st.session_state.language
        mode = st.session_state.mode
        menu_data = st.session_state.menu_data
        
        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            if lang == 'fa':
                st.markdown("### 💬 گفتگو با شف‌بات")
            else:
                st.markdown("### 💬 Chat with ChefBot")
        
        with col2:
            if st.button("🔄 شروع مجدد"):
                st.session_state.step = 'mode_selection'
                st.session_state.messages = []
                st.rerun()
        
        # Display messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("پیام خود را بنویسید | Type your message"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response
            system_prompt = generate_system_prompt(lang, mode, menu_data)
            response = chat_with_groq(st.session_state.messages, system_prompt)
            
            # Add assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
        
        # Initial message for guided mode
        if mode == 'guided' and len(st.session_state.messages) == 0:
            if lang == 'fa':
                initial_msg = "سلام! آلرژی خاصی داری؟"
            else:
                initial_msg = "Hello! Do you have any allergies?"
            
            st.session_state.messages.append({"role": "assistant", "content": initial_msg})
            st.rerun()

if __name__ == "__main__":
    main()
