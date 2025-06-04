import streamlit as st
import json

# Page config
st.set_page_config(
    page_title="ChefBot",
    page_icon="🧑‍🍳",
    layout="wide"
)

def get_groq_response(messages, system_prompt):
    """Get response from Groq API"""
    try:
        from groq import Groq
        client = Groq(api_key="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")
        
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=full_messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Sample menu data
MENU_DATA = {
    "items": [
        {"id": 1, "name_fa": "اسپرسو", "name_en": "Espresso", "flags": ["caffeine"]},
        {"id": 2, "name_fa": "کیک شکلاتی", "name_en": "Chocolate Cake", "flags": ["sugar", "gluten"]},
        {"id": 3, "name_fa": "سالاد سزار", "name_en": "Caesar Salad", "flags": ["lactose"]},
        {"id": 4, "name_fa": "پیتزا مارگاریتا", "name_en": "Pizza Margherita", "flags": ["gluten", "lactose"]},
        {"id": 5, "name_fa": "چای سبز", "name_en": "Green Tea", "flags": []}
    ]
}

def main():
    # Initialize session state
    if 'language' not in st.session_state:
        st.session_state.language = None
    if 'mode' not in st.session_state:
        st.session_state.mode = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Step 1: Language Selection
    if st.session_state.language is None:
        st.title("🧑‍🍳 ChefBot")
        st.markdown("### Choose Language | انتخاب زبان")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("فارسی 🇮🇷", use_container_width=True):
                st.session_state.language = 'fa'
                st.rerun()
        with col2:
            if st.button("English 🇺🇸", use_container_width=True):
                st.session_state.language = 'en'
                st.rerun()
        return

    # Step 2: Mode Selection
    if st.session_state.mode is None:
        lang = st.session_state.language
        
        if lang == 'fa':
            st.title("🧑‍🍳 سلام! من شف‌بات هستم")
            st.markdown("چطور کمکت کنم؟")
        else:
            st.title("🧑‍🍳 Hello! I'm ChefBot")
            st.markdown("How can I help you?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            label = "💬 گفتگو آزاد" if lang == 'fa' else "💬 Free Chat"
            if st.button(label, use_container_width=True):
                st.session_state.mode = 'chat'
                st.rerun()
        
        with col2:
            label = "📋 سوالات مرحله‌ای" if lang == 'fa' else "📋 Guided Questions"
            if st.button(label, use_container_width=True):
                st.session_state.mode = 'guided'
                st.rerun()
        
        with col3:
            label = "📜 انتخاب از منو" if lang == 'fa' else "📜 Menu Selection"
            if st.button(label, use_container_width=True):
                st.session_state.mode = 'menu'
                st.rerun()
        
        # Back button
        back_label = "🔙 تغییر زبان" if lang == 'fa' else "🔙 Change Language"
        if st.button(back_label):
            st.session_state.language = None
            st.rerun()
        return

    # Step 3: Menu Selection (if mode is menu)
    if st.session_state.mode == 'menu':
        lang = st.session_state.language
        
        title = "📜 منوی کافه" if lang == 'fa' else "📜 Cafe Menu"
        st.title(title)
        
        for item in MENU_DATA['items']:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{item[f'name_{lang}']}**")
            with col2:
                select_label = "انتخاب" if lang == 'fa' else "Select"
                if st.button(select_label, key=f"item_{item['id']}"):
                    st.session_state.mode = 'chat'
                    name = item[f'name_{lang}']
                    msg = f"من {name} رو انتخاب کردم" if lang == 'fa' else f"I selected {name}"
                    st.session_state.messages = [{"role": "user", "content": msg}]
                    st.rerun()
        
        # Back button
        back_label = "🔙 بازگشت" if lang == 'fa' else "🔙 Back"
        if st.button(back_label):
            st.session_state.mode = None
            st.rerun()
        return

    # Step 4: Chat Interface
    if st.session_state.mode in ['chat', 'guided']:
        lang = st.session_state.language
        
        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            title = "💬 چت با شف‌بات" if lang == 'fa' else "💬 Chat with ChefBot"
            st.markdown(f"### {title}")
        with col2:
            restart_label = "🔄 شروع مجدد" if lang == 'fa' else "🔄 Restart"
            if st.button(restart_label):
                st.session_state.mode = None
                st.session_state.messages = []
                st.rerun()

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        placeholder = "پیام خود را بنویسید..." if lang == 'fa' else "Type your message..."
        if prompt := st.chat_input(placeholder):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Create system prompt
            menu_text = ""
            for item in MENU_DATA['items']:
                menu_text += f"{item[f'name_{lang}']}, "
            
            if lang == 'fa':
                system_prompt = f"شما یک سرآشپز ماهر هستید. منو: {menu_text}"
            else:
                system_prompt = f"You are an expert chef. Menu: {menu_text}"
            
            # Get AI response
            response = get_groq_response(st.session_state.messages, system_prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()

        # Initial message for guided mode
        if st.session_state.mode == 'guided' and len(st.session_state.messages) == 0:
            initial = "سلام! آلرژی خاصی داری؟" if lang == 'fa' else "Hello! Any allergies?"
            st.session_state.messages.append({"role": "assistant", "content": initial})
            st.rerun()

if __name__ == "__main__":
    main()
