import streamlit as st
import requests
from PIL import Image
from io import BytesIO

from apps.atm_core import AtmAccount
from apps.calc_engine import evaluate, sqrt

# Page Configuration
st.set_page_config(
    page_title="Python App Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Glassmorphic UI)
st.markdown("""
<style>
    /* Dark Theme & Custom Fonts */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #1C1C1E 0%, #2C2C2E 100%);
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 25px;
        border: 1px solid #3A3A3C;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .app-card {
        background: #1C1C1E;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #2C2C2E;
        margin-bottom: 15px;
        transition: transform 0.2s ease;
    }
    .credit-card {
        background: linear-gradient(135deg, #0A84FF 0%, #0056B3 100%);
        padding: 24px;
        border-radius: 18px;
        color: white;
        box-shadow: 0 10px 30px rgba(10, 132, 255, 0.3);
        margin-bottom: 20px;
    }
    .badge {
        background-color: #30D158;
        color: black;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 12px;
    }
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State Variables
if "calc_expr" not in st.session_state:
    st.session_state.calc_expr = ""
if "atm_account" not in st.session_state:
    st.session_state.atm_account = AtmAccount()
if "atm_authenticated" not in st.session_state:
    st.session_state.atm_authenticated = False
if "cart" not in st.session_state:
    st.session_state.cart = []

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/isometric-folders/100/code.png", width=70)
st.sidebar.title("Desktop Suite Web")
st.sidebar.caption("Sleek Python Applications")

choice = st.sidebar.radio(
    "Select Application",
    ["🏠 Suite Dashboard", "🧮 Pro Calculator", "📰 Global News Hub", "🏧 ATM Terminal", "🛍️ Flipkart Store"]
)

st.sidebar.markdown("---")
st.sidebar.info("🚀 **Live Streamlit App**\nDeployed directly from GitHub!")

# ---------------------------------------------------------
# 1. DASHBOARD
# ---------------------------------------------------------
if choice == "🏠 Suite Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0;">🚀 Python Web App Suite</h1>
        <p style="color: #8E8E93; margin-top: 5px;">A collection of modern interactive web applications powered by Streamlit.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="app-card">
            <h3>🧮 Pro Calculator</h3>
            <p style="color: #A1A1A6;">Scientific calculator with interactive display, expression history, and mathematical operations.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="app-card">
            <h3>📰 Global News Hub</h3>
            <p style="color: #A1A1A6;">Live news feed with category switching (Tech, Business, Sports) and full article links.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="app-card">
            <h3>🏧 Nexus ATM Terminal</h3>
            <p style="color: #A1A1A6;">Interactive banking simulator with PIN authorization, deposit/withdrawal, and digital receipts.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="app-card">
            <h3>🛍️ Flipkart Store</h3>
            <p style="color: #A1A1A6;">E-commerce store with product cards, live cart tracking, and instant order checkout.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. CALCULATOR
# ---------------------------------------------------------
elif choice == "🧮 Pro Calculator":
    st.title("🧮 Pro Calculator")
    st.caption("Interactive Web Calculator")

    # Display Screen
    expr_display = st.session_state.calc_expr if st.session_state.calc_expr else "0"
    st.text_input("Expression Display", value=expr_display, key="display", disabled=True)

    # Calculator Buttons Grid
    col1, col2, col3, col4 = st.columns(4)

    def append_calc(val):
        st.session_state.calc_expr += str(val)

    with col1:
        if st.button("C", use_container_width=True, type="primary"):
            st.session_state.calc_expr = ""
            st.rerun()
        if st.button("7", use_container_width=True):
            append_calc("7")
            st.rerun()
        if st.button("4", use_container_width=True):
            append_calc("4")
            st.rerun()
        if st.button("1", use_container_width=True):
            append_calc("1")
            st.rerun()
        if st.button("0", use_container_width=True):
            append_calc("0")
            st.rerun()

    with col2:
        if st.button("⌫", use_container_width=True):
            st.session_state.calc_expr = st.session_state.calc_expr[:-1]
            st.rerun()
        if st.button("8", use_container_width=True):
            append_calc("8")
            st.rerun()
        if st.button("5", use_container_width=True):
            append_calc("5")
            st.rerun()
        if st.button("2", use_container_width=True):
            append_calc("2")
            st.rerun()
        if st.button(".", use_container_width=True):
            append_calc(".")
            st.rerun()

    with col3:
        if st.button("%", use_container_width=True):
            append_calc("%")
            st.rerun()
        if st.button("9", use_container_width=True):
            append_calc("9")
            st.rerun()
        if st.button("6", use_container_width=True):
            append_calc("6")
            st.rerun()
        if st.button("3", use_container_width=True):
            append_calc("3")
            st.rerun()
        if st.button("√", use_container_width=True):
            result = sqrt(st.session_state.calc_expr)
            st.session_state.calc_expr = result if result is not None else "Error"
            st.rerun()

    with col4:
        if st.button("/", use_container_width=True):
            append_calc("/")
            st.rerun()
        if st.button("*", use_container_width=True):
            append_calc("*")
            st.rerun()
        if st.button("-", use_container_width=True):
            append_calc("-")
            st.rerun()
        if st.button("+", use_container_width=True):
            append_calc("+")
            st.rerun()
        if st.button("=", use_container_width=True, type="primary"):
            result = evaluate(st.session_state.calc_expr)
            st.session_state.calc_expr = result if result is not None else "Error"
            st.rerun()

# ---------------------------------------------------------
# 3. NEWS HUB
# ---------------------------------------------------------
elif choice == "📰 Global News Hub":
    st.title("📰 Global News Hub")
    st.caption("Latest Top Headlines")

    category = st.selectbox("Select News Category", ["General", "Technology", "Business", "Sports"])

    SAMPLE_NEWS = [
        {
            "title": "Quantum Computing Reaches Major Error Correction Milestone",
            "description": "Researchers demonstrate a fault-tolerant quantum architecture that reduces computational noise by 90%, opening new doors for cryptography and materials science.",
            "url": "https://news.google.com",
            "image": "https://picsum.photos/600/300?random=10",
            "source": "Tech Daily"
        },
        {
            "title": "Global Clean Energy Investment Reaches $1.8 Trillion Record",
            "description": "Solar and wind energy projects dominated capital flows worldwide, outpacing traditional fossil fuel infrastructure investments.",
            "url": "https://news.google.com",
            "image": "https://picsum.photos/600/300?random=11",
            "source": "World Finance"
        },
        {
            "title": "Next-Generation Space Telescope Captures Deepest Cosmic View",
            "description": "Astronomers reveal stellar nurseries and primordial galaxies formed just 300 million years after the Big Bang.",
            "url": "https://news.google.com",
            "image": "https://picsum.photos/600/300?random=12",
            "source": "Astro Science"
        }
    ]

    for item in SAMPLE_NEWS:
        with st.container():
            st.markdown(f"#### {item['title']}")
            st.caption(f"Source: {item['source']} | Category: {category}")
            st.image(item['image'], use_column_width=True)
            st.write(item['description'])
            st.link_button("Read Full Story 🔗", item['url'])
            st.markdown("---")

# ---------------------------------------------------------
# 4. ATM TERMINAL
# ---------------------------------------------------------
elif choice == "🏧 ATM Terminal":
    st.title("🏧 Nexus Digital ATM Terminal")

    account = st.session_state.atm_account

    st.markdown(f"""
    <div class="credit-card">
        <h3>PLATINUM DEBIT CARD</h3>
        <h2>•••• •••• •••• 8842</h2>
        <p style="text-align: right; font-size: 18px; margin: 0;"><b>Balance: ${account.balance:,.2f}</b></p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.atm_authenticated:
        st.subheader("🔒 PIN Authentication Required")
        input_pin = st.text_input("Enter 4-Digit Security PIN", type="password")
        if st.button("Unlock Account", type="primary"):
            if account.verify_pin(input_pin):
                st.session_state.atm_authenticated = True
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Incorrect PIN!")
    else:
        st.success("Account Unlocked")

        tab1, tab2, tab3 = st.tabs(["💵 Deposit Cash", "💳 Withdraw Cash", "🧾 Receipt Log"])

        with tab1:
            dep_amt = st.number_input("Deposit Amount ($)", min_value=1.0, step=50.0)
            if st.button("Confirm Deposit", type="primary"):
                success, message = account.deposit(dep_amt)
                if success:
                    st.success(message)
                else:
                    st.error(message)
                st.rerun()

        with tab2:
            wth_amt = st.number_input("Withdrawal Amount ($)", min_value=1.0, max_value=float(account.balance), step=50.0)
            if st.button("Confirm Withdrawal", type="primary"):
                success, message = account.withdraw(wth_amt)
                if success:
                    st.success(message)
                else:
                    st.error(message)
                st.rerun()

        with tab3:
            st.subheader("Transaction History")
            if not account.transactions:
                st.info("No recent transactions.")
            else:
                for entry in account.transactions:
                    st.write(f"• {entry}")

        if st.button("Lock ATM Session"):
            st.session_state.atm_authenticated = False
            st.rerun()

# ---------------------------------------------------------
# 5. FLIPKART STORE
# ---------------------------------------------------------
elif choice == "🛍️ Flipkart Store":
    st.title("🛍️ Flipkart E-Commerce Store")

    PRODUCTS = [
        {"id": 1, "name": "Wireless Headphones", "price": 299.99, "badge": "BESTSELLER", "icon": "🎧"},
        {"id": 2, "name": "Gaming Monitor 34\"", "price": 649.00, "badge": "SALE", "icon": "🖥️"},
        {"id": 3, "name": "Mechanical Keyboard", "price": 149.50, "badge": "POPULAR", "icon": "⌨️"},
        {"id": 4, "name": "Smart Watch Series 9", "price": 399.00, "badge": "NEW", "icon": "⌚"}
    ]

    col_prod, col_cart = st.columns([2, 1])

    with col_prod:
        st.subheader("Product Catalog")
        for item in PRODUCTS:
            with st.container():
                st.markdown(f"### {item['icon']} {item['name']}")
                st.write(f"Price: **${item['price']:.2f}** | Badge: `{item['badge']}`")
                if st.button(f"+ Add to Cart", key=f"btn_{item['id']}"):
                    st.session_state.cart.append(item)
                    st.success(f"Added {item['name']} to cart!")
                    st.rerun()
                st.markdown("---")

    with col_cart:
        st.subheader(f"🛒 Shopping Cart ({len(st.session_state.cart)})")
        if not st.session_state.cart:
            st.info("Cart is empty.")
        else:
            total = 0
            for i, p in enumerate(st.session_state.cart):
                st.write(f"• {p['name']} - ${p['price']:.2f}")
                total += p['price']

            st.markdown(f"### Total: **${total:,.2f}**")
            if st.button("Proceed to Checkout 💳", type="primary"):
                st.balloons()
                st.success(f"Order Placed! Total: ${total:,.2f}")
                st.session_state.cart = []
                st.rerun()
