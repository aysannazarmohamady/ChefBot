import streamlit as st
import json
from typing import Dict, List

# Page config
st.set_page_config(
    page_title="شف‌ بات | Chef Bot",
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
    """Load menu data from JSON file or return sample data"""
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
                "name_fa": "کاپوچینو",
                "name_en": "Cappuccino",
                "category_fa": "قهوه",
                "category_en": "Coffee",
                "ingredients_fa": ["اسپرسو", "شیر بخار داده شده", "فوم شیر", "دارچین"],
                "ingredients_en": ["Espresso", "Steamed milk", "Milk foam", "Cinnamon"],
                "health_flags": ["lactose", "caffeine"]
            },
            {
                "id": 3,
                "name_fa": "کیک شکلاتی",
                "name_en": "Chocolate Cake",
                "category_fa": "کیک",
                "category_en": "Cake",
                "ingredients_fa": ["آرد", "شکلات", "تخم مرغ", "شکر", "کره", "شیر"],
                "ingredients_en": ["Flour", "Chocolate", "Eggs", "Sugar", "Butter", "Milk"],
                "health_flags": ["gluten", "high_sugar", "eggs", "lactose"]
            },
            {
                "id": 4,
                "name_fa": "چیز کیک",
                "name_en": "Cheesecake",
                "category_fa": "کیک",
                "category_en": "Cake",
                "ingredients_fa": ["پنیر خامه‌ای", "بیسکویت", "کره", "شکر", "تخم مرغ"],
                "ingredients_en": ["Cream cheese", "Cookies", "Butter", "Sugar", "Eggs"],
                "health_flags": ["lactose", "gluten", "eggs", "high_sugar"]
            },
            {
                "id": 5,
                "name_fa": "پاستا کربونارا",
                "name_en": "Pasta Carbonara",
                "category_fa": "پاستا",
                "category_en": "Pasta",
                "ingredients_fa": ["اسپاگتی", "بیکن", "تخم مرغ", "پنیر پارمزان"],
                "ingredients_en": ["Spaghetti", "Bacon", "Eggs", "Parmesan cheese"],
                "health_flags": ["gluten", "eggs", "lactose", "pork"]
            },
            {
                "id": 6,
                "name_fa": "پیتزا مارگاریتا",
                "name_en": "Pizza Margherita",
                "category_fa": "پیتزا",
                "category_en": "Pizza",
                "ingredients_fa": ["خمیر پیتزا", "سس گوجه", "پنیر موزارلا", "ریحان"],
                "ingredients_en": ["Pizza dough", "Tomato sauce", "Mozzarella cheese", "Basil"],
                "health_flags": ["gluten", "lactose"]
            },
            {
                "id": 7,
                "name_fa": "سالاد سزار",
                "name_en": "Caesar Salad",
                "category_fa": "سالاد",
                "category_en": "Salad",
                "ingredients_fa": ["کاهو رومی", "پنیر پارمزان", "کروتون", "سس سزار"],
                "ingredients_en": ["Romaine lettuce", "Parmesan cheese", "Croutons", "Caesar dressing"],
                "health_flags": ["gluten", "lactose", "eggs"]
            },
            {
                "id": 8,
                "name_fa": "چای سبز",
                "name_en": "Green Tea",
                "category_fa": "دمنوش",
                "category_en": "Herbal Tea",
                "ingredients_fa": ["برگ چای سبز", "آب جوش"],
                "ingredients_en": ["Green tea leaves", "Boiling water"],
                "health_flags": ["mild_caffeine"]
            },
            {
                "id": 9,
                "name_fa": "چای بابونه",
                "name_en": "Chamomile Tea",
                "category_fa": "دمنوش",
                "category_en": "Herbal Tea",
                "ingredients_fa": ["گل بابونه خشک", "آب جوش"],
                "ingredients_en": ["Dried chamomile flowers", "Boiling water"],
                "health_flags": []
            },
            {
                "id": 10,
                "name_fa": "برگر کلاسیک",
                "name_en": "Classic Burger",
                "category_fa": "غذای اصلی",
                "category_en": "Main Course",
                "ingredients_fa": ["گوشت گاو", "نان برگر", "کاهو", "گوجه", "پنیر"],
                "ingredients_en": ["Beef patty", "Burger bun", "Lettuce", "Tomato", "Cheese"],
                "health_flags": ["gluten", "lactose", "beef", "high_calorie"]
            }
        ]
    }
    
    try:
        with open('menu_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return sample_data

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
            return f"""شما یک سرآشپز ماهر و مشاور تخصصی کافه هستید به نام "شف‌بات". با کاربران به صورت دوستانه، صمیمی و حرفه‌ای صحبت کنید.

منوی کافه:
{menu_text}

وظایف شما:
1. با کاربر گفتگوی طبیعی و دوستانه داشته باشید
2. بر اساس مود، احساسات و نیازهای کاربر پیشنهاد دهید
3. در صورت تشخیص مشکل سلامتی، سوال مناسب بپرسید (مثل دیابت برای غذاهای شیرین، آلرژی برای مواد خاص)
4. پیشنهادات شخصی‌سازی شده و علت‌دار ارائه دهید
5. فقط از آیتم‌های موجود در منو پیشنهاد دهید

راهنمای health_flags:
- lactose: حاوی لاکتوز (برای حساسیت به شیر)
- gluten: حاوی گلوتن (برای بیماری سلیاک)
- caffeine: حاوی کافئین زیاد (برای مشکلات قلبی/اضطراب)
- high_sugar: شکر زیاد (برای دیابت)
- nuts: حاوی آجیل
- eggs: حاوی تخم‌مرغ
- pork: حاوی گوشت خوک
- beef: حاوی گوشت گاو

همیشه دلیل انتخابتان را بگویید و اگر کاربر شرایط خاصی دارد، جایگزین مناسب پیشنهاد دهید."""

        elif mode == 'guided':
            return f"""شما یک مشاور تخصصی کافه هستید که سوالات مرحله‌ای و هدفمند می‌پرسید.

منوی کافه:
{menu_text}

مراحل کار شما:
1. سلامت و محدودیت‌ها: آلرژی، دیابت، حساسیت‌های غذایی، رژیم خاص
2. مود و انرژی: آیا خسته است؟ انرژی می‌خواهد؟ آرامش؟ استرس دارد؟
3. ترجیحات: طعم (شیرین/شور/تند)، بافت (نرم/سفت)، دمای غذا (گرم/سرد)
4. زمان و مناسبت: چه وعده‌ای است؟ چقدر وقت دارد؟
5. پیشنهاد نهایی: 2-3 گزینه با توضیح دلایل

در هر مرحله فقط 1-2 سوال کوتاه و مفهوم بپرسید. منتظر جواب باشید و به مرحله بعد بروید."""

        else:  # validation mode
            return f"""شما یک مشاور امنیت غذایی و سلامت هستید. کاربر یک آیتم از منو انتخاب کرده و شما باید امنیت آن را بررسی کنید.

منوی کافه:
{menu_text}

اگر آیتم انتخابی health_flag مشکوک دارد، سوال مناسب بپرسید:
- lactose → "حساسیت به لاکتوز یا شیر نداری؟"
- gluten → "سلیاک یا حساسیت به گلوتن نداری؟"  
- high_sugar → "دیابت نداری؟ این آیتم شکر زیادی داره"
- caffeine → "مشکل قلبی یا اضطراب نداری؟ کافئین زیادی داره"
- eggs → "به تخم مرغ آلرژی نداری؟"
- nuts → "به آجیل آلرژی نداری؟"
- pork → "مشکلی با مصرف گوشت خوک نداری؟"

اگر مشکلی تشخیص دادید، گزینه‌های جایگزین امن از همان دسته پیشنهاد دهید."""
    
    else:  # English
        if mode == 'free_chat':
            return f"""You are an expert chef and cafe consultant named "". Chat naturally, friendly and professionally with users.

Cafe Menu:
{menu_text}

Your tasks:
1. Have natural and friendly conversations with users
2. Make recommendations based on user's mood, feelings and needs
3. Ask appropriate health questions if you detect potential issues (like diabetes for sweet foods, allergies for specific ingredients)
4. Provide personalized recommendations with explanations
5. Only suggest items from the available menu

Health flags guide:
- lactose: Contains lactose (for lactose intolerance)
- gluten: Contains gluten (for celiac disease)
- caffeine: High caffeine content (for heart problems/anxiety)
- high_sugar: High sugar content (for diabetes)
- nuts: Contains nuts
- eggs: Contains eggs
- pork: Contains pork
- beef: Contains beef

Always explain your choices and if user has special conditions, suggest safe alternatives."""

        elif mode == 'guided':
            return f"""You are a professional cafe consultant who asks step-by-step targeted questions.

Cafe Menu:
{menu_text}

Your process steps:
1. Health & restrictions: Allergies, diabetes, dietary restrictions, special diets
2. Mood & energy: Are they tired? Need energy? Want relaxation? Stressed?
3. Preferences: Taste (sweet/savory/spicy), texture (soft/firm), temperature (hot/cold)
4. Time & occasion: Which meal? How much time do they have?
5. Final recommendation: 2-3 options with explanations

Ask only 1-2 short, clear questions per step. Wait for answers before moving to next step."""

        else:  # validation mode
            return f"""You are a food safety and health consultant. User has selected a menu item and you need to verify its safety.

Cafe Menu:
{menu_text}

If selected item has suspicious health_flags, ask appropriate questions:
- lactose → "Do you have lactose intolerance?"
- gluten → "Do you have celiac disease or gluten sensitivity?"
- high_sugar → "Do you have diabetes? This item has high sugar content"
- caffeine → "Do you have heart problems or anxiety? This has high caffeine"
- eggs → "Are you allergic to eggs?"
- nuts → "Are you allergic to nuts?"
- pork → "Any issues with consuming pork?"

If you detect issues, suggest safe alternatives from the same category."""

def chat_with_groq(messages: List[Dict], system_prompt: str):
    """Send messages to Groq and get response"""
    try:
        client = init_groq_client()
        if not client:
            return "خطا در اتصال به سرویس | Connection error"
        
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=full_messages,
            temperature=0.7,
            max_tokens=800
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"خطا در ارتباط | Connection error: {str(e)}"

def show_language_selection():
    """Language selection page with enhanced UI"""
    # Custom CSS for beautiful buttons
    st.markdown("""
    <style>
    .language-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 20px;
        font-size: 20px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .stButton > button {
        height: 100px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Centered title
    st.markdown("""
    <div style='text-align: center; padding: 50px 0;'>
        <h1>🧑‍🍳 </h1>
        <h3>Your Smart Culinary Assistant | دستیار هوشمند آشپزی شما</h3>
        <p style='font-size: 18px; color: #666;'>Choose your language to start | برای شروع زبان خود را انتخاب کنید</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selection buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🇮🇷 فارسی", use_container_width=True, key="btn_fa"):
                st.session_state.language = 'fa'
                st.session_state.step = 'mode_selection'
                st.rerun()
        
        with col_b:
            if st.button("🇺🇸 English", use_container_width=True, key="btn_en"):
                st.session_state.language = 'en'
                st.session_state.step = 'mode_selection'
                st.rerun()

def show_mode_selection():
    """Show the three interaction modes in an engaging way"""
    lang = st.session_state.language
    
    # Header with personality
    if lang == 'fa':
        st.markdown("""
        <div style='text-align: center; padding: 30px 0;'>
            <h1>🧑‍🍳 سلام! من شف‌بات هستم</h1>
            <h3 style='color: #4ECDC4;'>امروز چطور می‌تونم کمکت کنم؟</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
    else:
        st.markdown("""
        <div style='text-align: center; padding: 30px 0;'>
            <h1>🧑‍🍳 Hello! I'm </h1>
            <h3 style='color: #4ECDC4;'>How can I help you today?</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
    
    # Three attractive options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if lang == 'fa':
            st.markdown("""
            <div style='text-align: center; padding: 20px; border-radius: 15px; background: #f8f9fa; margin: 10px;'>
                <h2>🤔</h2>
                <h4>نمی‌دونم چی بخورم!</h4>
                <p>بیا با هم حرف بزنیم و ببینیم چی برات مناسبه. مثل یه دوست صمیمی راهنماییت می‌کنم!</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("💬 بیا گفتگو کنیم", use_container_width=True, key="mode_free"):
                st.session_state.mode = 'free_chat'
                st.session_state.step = 'chat_interface'
                st.rerun()
        else:
            st.markdown("""
            <div style='text-align: center; padding: 20px; border-radius: 15px; background: #f8f9fa; margin: 10px;'>
                <h2>🤔</h2>
                <h4>I don't know what to eat!</h4>
                <p>Let's chat and see what suits you best. I'll guide you like a friendly expert!</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("💬 Let's Chat", use_container_width=True, key="mode_free"):
                st.session_state.mode = 'free_chat'
                st.session_state.step = 'chat_interface'
                st.rerun()
    
    with col2:
        if lang == 'fa':
            st.markdown("""
            <div style='text-align: center; padding: 20px; border-radius: 15px; background: #f8f9fa; margin: 10px;'>
                <h2>📝</h2>
                <h4>پیشنهاد شخصی‌سازی‌شده می‌خوام</h4>
                <p>چندتا سوال ازت می‌پرسم و بهترین گزینه رو براساس سلیقه و شرایطت پیدا می‌کنیم</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📋 شروع سوالات", use_container_width=True, key="mode_guided"):
                st.session_state.mode = 'guided'
                st.session_state.step = 'chat_interface'
                st.rerun()
        else:
            st.markdown("""
            <div style='text-align: center; padding: 20px; border-radius: 15px; background: #f8f9fa; margin: 10px;'>
                <h2>📝</h2>
                <h4>I want personalized suggestions</h4>
                <p>I'll ask you a few questions to find the perfect choice based on your taste and needs</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📋 Start Questions", use_container_width=True, key="mode_guided"):
                st.session_state.mode = 'guided'
                st.session_state.step = 'chat_interface'
                st.rerun()
    
    with col3:
        if lang == 'fa':
            st.markdown("""
            <div style='text-align: center; padding: 20px; border-radius: 15px; background: #f8f9fa; margin: 10px;'>
                <h2>✅</h2>
                <h4>می‌دونم چی می‌خوام</h4>
                <p>از منو انتخاب کن، من فقط چک می‌کنم مناسب باشه و اگه مشکلی بود بهت می‌گم</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📜 نمایش منو", use_container_width=True, key="mode_validation"):
                st.session_state.mode = 'validation'
                st.session_state.step = 'menu_display'
                st.rerun()
        else:
            st.markdown("""
            <div style='text-align: center; padding: 20px; border-radius: 15px; background: #f8f9fa; margin: 10px;'>
                <h2>✅</h2>
                <h4>I know what I want</h4>
                <p>Choose from menu, I'll just check if it's suitable for you and warn if there are issues</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📜 Show Menu", use_container_width=True, key="mode_validation"):
                st.session_state.mode = 'validation'
                st.session_state.step = 'menu_display'
                st.rerun()
    
    # Back button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔙 تغییر زبان | Change Language", key="back_lang", use_container_width=True):
            st.session_state.step = 'language_selection'
            st.session_state.language = None
            st.rerun()

def show_menu_selection():
    """Display menu for selection in validation mode"""
    lang = st.session_state.language
    menu_data = st.session_state.menu_data
    
    # Header
    if lang == 'fa':
        st.title("📜 منوی کافه شف‌بات")
        st.markdown("### چی دوست داری بخوری؟")
        st.markdown("*از هر کدوم که انتخاب کنی، من چک می‌کنم که مناسب باشه*")
    else:
        st.title("📜  Cafe Menu")
        st.markdown("### What would you like to have?")
        st.markdown("*I'll check if your selection is suitable for you*")
    
    st.markdown("---")
    
    # Group items by category
    categories = {}
    for item in menu_data['cafe_menu']:
        cat = item[f'category_{lang}']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    # Display menu by categories with enhanced UI
    for category, items in categories.items():
        st.markdown(f"## {category}")
        
        # Create cards for items
        cols = st.columns(2)
        for idx, item in enumerate(items):
            with cols[idx % 2]:
                # Create item card
                health_indicators = ""
                if item['health_flags']:
                    health_indicators = "⚠️ " if any(flag in ['high_sugar', 'caffeine', 'lactose', 'gluten'] for flag in item['health_flags']) else "ℹ️ "
                
                st.markdown(f"""
                <div style='border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0; background: white;'>
                    <h4>{health_indicators}{item[f'name_{lang}']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Ingredients preview
                ingredients = ", ".join(item[f'ingredients_{lang}'][:3])
                if len(item[f'ingredients_{lang}']) > 3:
                    ingredients += "..."
                st.markdown(f"📝 *{ingredients}*")
                
                # Health flags display
                if item['health_flags']:
                    flags_text = " • ".join(item['health_flags'])
                    st.markdown(f"🏷️ `{flags_text}`")
                
                # Select button
                if st.button(f"انتخاب | Select", key=f"select_{item['id']}", use_container_width=True):
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
    if st.button("🔙 بازگشت | Back", key="back_menu"):
        st.session_state.step = 'mode_selection'
        st.rerun()

def show_chat_interface():
    """Enhanced chat interface with better UX"""
    lang = st.session_state.language
    mode = st.session_state.mode
    menu_data = st.session_state.menu_data
    
    # Mode names for display
    mode_names = {
        'fa': {
            'free_chat': '💬 گفتگوی آزاد با شف‌بات',
            'guided': '📋 راهنمایی مرحله‌ای',
            'validation': '✅ بررسی انتخاب شما'
        },
        'en': {
            'free_chat': '💬 Free Chat with ',
            'guided': '📋 Guided Assessment',
            'validation': '✅ Selection Validation'
        }
    }
    
    # Header with mode info and controls
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"### {mode_names[lang][mode]}")
        
        # Mode description
        if mode == 'free_chat':
            desc = "گفتگوی طبیعی و دوستانه" if lang == 'fa' else "Natural and friendly conversation"
        elif mode == 'guided':
            desc = "سوالات مرحله‌ای برای پیشنهاد بهتر" if lang == 'fa' else "Step-by-step questions for better recommendations"
        else:
            desc = "بررسی ایمنی انتخاب شما" if lang == 'fa' else "Safety check for your selection"
        
        st.markdown(f"*{desc}*")
    
    with col2:
        if st.button("🔄 شروع مجدد | Restart", key="restart"):
            st.session_state.step = 'mode_selection'
            st.session_state.messages = []
            st.session_state.selected_item = None
            st.rerun()
    
    st.markdown("---")
    
    # Chat messages with improved styling
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    placeholder_text = {
        'fa': "پیام خود را بنویسید... (مثل: خسته‌ام و انرژی می‌خوام)",
        'en': "Type your message... (e.g: I'm tired and need energy)"
    }
    
    if prompt := st.chat_input(placeholder_text[lang]):
        try:
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
        except Exception as e:
            st.error(f"خطا در ارسال پیام | Error: {str(e)}")
    
    # Initial message for guided mode
    if mode == 'guided' and len(st.session_state.messages) == 0:
        if lang == 'fa':
            initial_prompt = """سلام و خوش اومدی! 👋

من شف‌بات هستم و می‌خوام بهترین پیشنهاد رو برات پیدا کنم.

اول از همه، بگو آلرژی یا حساسیت خاصی داری؟ مثل:
- حساسیت به شیر (لاکتوز)
- حساسیت به گلوتن 
- آلرژی به آجیل یا تخم مرغ
- یا هیچ مشکلی نداری؟"""
        else:
            initial_prompt = """Hello and welcome! 👋

I'm  and I want to find the best recommendation for you.

First of all, do you have any allergies or sensitivities? Such as:
- Lactose intolerance
- Gluten sensitivity
- Nut or egg allergies
- Or no issues at all?"""
        
        st.session_state.messages.append({"role": "assistant", "content": initial_prompt})
        st.rerun()
    
    # Helpful suggestions for free chat mode
    if mode == 'free_chat' and len(st.session_state.messages) == 0:
        if lang == 'fa':
            st.markdown("""
            💡 **راهنمای گفتگو:**
            - بگو چه حالی داری (خسته، شاد، استرس، ...)
            - بگو چی دوست داری (شیرین، شور، گرم، سرد، ...)
            - اگر شرایط خاصی داری حتماً بگو (دیابت، آلرژی، رژیم، ...)
            
            **مثال‌ها:**
            - "خسته‌ام و یه چیز انرژی‌زا می‌خوام"
            - "استرس دارم، یه چیز آرام‌بخش پیشنهاد بده"
            - "دیابت دارم ولی دوست دارم شیرینی بخورم"
            """)
        else:
            st.markdown("""
            💡 **Chat Guide:**
            - Tell me how you're feeling (tired, happy, stressed, ...)
            - Tell me what you like (sweet, savory, hot, cold, ...)
            - Mention any special conditions (diabetes, allergies, diet, ...)
            
            **Examples:**
            - "I'm tired and need something energizing"
            - "I'm stressed, suggest something relaxing"
            - "I have diabetes but want something sweet"
            """)

def main():
    """Main application function"""
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
    try:
        if st.session_state.step == 'language_selection':
            show_language_selection()
        elif st.session_state.step == 'mode_selection':
            show_mode_selection()
        elif st.session_state.step == 'menu_display':
            show_menu_selection()
        elif st.session_state.step == 'chat_interface':
            show_chat_interface()
    except Exception as e:
        st.error(f"خطا در اجرای برنامه | Application Error: {str(e)}")
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 شروع مجدد کامل | Full Restart", use_container_width=True):
                # Reset all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

# Footer
def show_footer():
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🧑‍🍳 <strong></strong> - Your Smart Culinary Assistant | دستیار هوشمند آشپزی شما</p>
        <p>Made with ❤️ using Streamlit & Groq AI</p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
    show_footer()
