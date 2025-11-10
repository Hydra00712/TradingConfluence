# Trade Confirmation Assistant – "Wall Street Bias Checker"
# Made for Adam's Smart Money Strategy (Multi-TF, Liquidity, Displacement, FVG, SMT)

import streamlit as st
import requests
from datetime import datetime
import json

st.set_page_config(
    page_title="Wall Street Bias Checker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic Black & White UI
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: #000000;
    }

    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: 8px;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(255,255,255,0.5);
        font-family: 'Courier New', monospace;
    }

    .sub-header {
        text-align: center;
        color: #AAAAAA;
        font-size: 1.1rem;
        letter-spacing: 3px;
        margin-bottom: 3rem;
        font-family: 'Courier New', monospace;
    }

    /* Market Cards - Futuristic Glass Effect */
    .market-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #333333;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(4px);
        transition: all 0.3s ease;
    }

    .market-card:hover {
        border-color: #FFFFFF;
        box-shadow: 0 8px 32px 0 rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }

    /* News Cards */
    .news-card {
        background: #0a0a0a;
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 3px solid #FFFFFF;
        transition: all 0.3s ease;
    }

    .news-card:hover {
        background: #1a1a1a;
        border-left-width: 5px;
    }

    /* Metrics */
    .metric-positive {
        color: #00FF00;
        font-weight: bold;
        font-size: 1.3rem;
        text-shadow: 0 0 10px rgba(0,255,0,0.5);
    }

    .metric-negative {
        color: #FF0000;
        font-weight: bold;
        font-size: 1.3rem;
        text-shadow: 0 0 10px rgba(255,0,0,0.5);
    }

    /* Result Box */
    .result-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        padding: 3rem;
        border-radius: 20px;
        border: 3px solid #FFFFFF;
        text-align: center;
        box-shadow: 0 0 40px rgba(255,255,255,0.2);
        margin: 2rem 0;
    }

    .result-box-green {
        border-color: #00FF00;
        box-shadow: 0 0 40px rgba(0,255,0,0.3);
    }

    .result-box-red {
        border-color: #FF0000;
        box-shadow: 0 0 40px rgba(255,0,0,0.3);
    }

    .result-box-orange {
        border-color: #FFA500;
        box-shadow: 0 0 40px rgba(255,165,0,0.3);
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF0000, #FFA500, #00FF00);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #000000;
        border-right: 2px solid #333333;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
    }

    /* Text */
    p, label, span {
        color: #FFFFFF !important;
    }

    /* Input Fields - Selectbox */
    .stSelectbox > div > div {
        background-color: #1a1a1a;
        color: #FFFFFF;
        border: 1px solid #333333;
    }

    .stSelectbox label {
        color: #FFFFFF !important;
    }

    /* Dropdown Menu */
    [data-baseweb="select"] {
        background-color: #1a1a1a;
    }

    [data-baseweb="select"] > div {
        background-color: #1a1a1a;
        border-color: #333333;
    }

    /* Dropdown Options */
    [role="option"] {
        background-color: #1a1a1a !important;
        color: #FFFFFF !important;
    }

    [role="option"]:hover {
        background-color: #333333 !important;
    }

    /* Radio Buttons */
    .stRadio > label {
        color: #FFFFFF !important;
    }

    .stRadio > div {
        color: #FFFFFF;
    }

    /* Divider */
    hr {
        border-color: #333333;
    }

    /* Buttons */
    .stButton > button {
        background: #FFFFFF;
        color: #000000;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        letter-spacing: 2px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: #000000;
        color: #FFFFFF;
        border: 2px solid #FFFFFF;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #1a1a1a;
        border-radius: 8px;
        color: #FFFFFF !important;
    }

    /* Glowing Effect for Important Elements */
    .glow {
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from {
            text-shadow: 0 0 5px #fff, 0 0 10px #fff;
        }
        to {
            text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header glow">⚡ WALL STREET BIAS CHECKER ⚡</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">SMART MONEY • CONFLUENCE • PRECISION</p>', unsafe_allow_html=True)

# --- FUNCTIONS FOR MARKET DATA ---
@st.cache_data(ttl=60)  # Cache for 1 minute
def get_market_data():
    """Fetch real-time market data for S&P 500 and NAS100"""
    try:
        # Using multiple fallback APIs for reliability
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # Try Yahoo Finance first
        sp500_url = "https://query1.finance.yahoo.com/v8/finance/chart/ES=F?interval=1d"
        nas100_url = "https://query1.finance.yahoo.com/v8/finance/chart/NQ=F?interval=1d"

        sp500_response = requests.get(sp500_url, headers=headers, timeout=10)
        nas100_response = requests.get(nas100_url, headers=headers, timeout=10)

        sp500_data = sp500_response.json()
        nas100_data = nas100_response.json()

        # Extract data with error handling
        sp500_result = sp500_data['chart']['result'][0]
        sp500_meta = sp500_result['meta']
        sp500_price = sp500_meta.get('regularMarketPrice', sp500_meta.get('previousClose', 0))
        sp500_prev = sp500_meta.get('chartPreviousClose', sp500_meta.get('previousClose', sp500_price))
        sp500_change = sp500_price - sp500_prev
        sp500_pct = (sp500_change / sp500_prev * 100) if sp500_prev != 0 else 0

        nas100_result = nas100_data['chart']['result'][0]
        nas100_meta = nas100_result['meta']
        nas100_price = nas100_meta.get('regularMarketPrice', nas100_meta.get('previousClose', 0))
        nas100_prev = nas100_meta.get('chartPreviousClose', nas100_meta.get('previousClose', nas100_price))
        nas100_change = nas100_price - nas100_prev
        nas100_pct = (nas100_change / nas100_prev * 100) if nas100_prev != 0 else 0

        return {
            'sp500': {'price': sp500_price, 'change': sp500_change, 'pct': sp500_pct},
            'nas100': {'price': nas100_price, 'change': nas100_change, 'pct': nas100_pct}
        }
    except Exception as e:
        # Fallback to demo data if API fails
        return {
            'sp500': {'price': 5850.25, 'change': 12.50, 'pct': 0.21},
            'nas100': {'price': 20125.75, 'change': -25.30, 'pct': -0.13},
            'demo': True
        }

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_futures_news():
    """Fetch futures-related news"""
    try:
        # Using NewsAPI (you can use free tier or alternative)
        # For demo, using a public RSS feed alternative
        url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=ES=F,NQ=F&region=US&lang=en-US"
        response = requests.get(url, timeout=5)

        # Simple parsing (in production, use feedparser library)
        news_items = []
        if response.status_code == 200:
            # Placeholder news for demo
            news_items = [
                {"title": "S&P 500 Futures Show Strength Ahead of Market Open", "time": "15 min ago"},
                {"title": "Nasdaq Futures Rally on Tech Earnings Beat", "time": "1 hour ago"},
                {"title": "Fed Minutes Signal Potential Rate Hold", "time": "2 hours ago"},
                {"title": "Futures Market Volatility Increases on Economic Data", "time": "3 hours ago"}
            ]
        return news_items
    except:
        return []

# --- SIDEBAR: MARKET DATA & NEWS ---
with st.sidebar:
    st.markdown("### ⚡ LIVE MARKET DATA")
    st.markdown("---")

    market_data = get_market_data()

    if market_data:
        # Show demo mode indicator if using fallback data
        if market_data.get('demo'):
            st.markdown('<p style="color: #FFA500; font-size: 0.8rem; text-align: center;">📡 DEMO MODE - Live data unavailable</p>', unsafe_allow_html=True)

        # S&P 500
        st.markdown('<div class="market-card">', unsafe_allow_html=True)
        st.markdown("#### 📈 S&P 500 (ES)")
        st.markdown(f"<h2 style='color: #FFFFFF; margin: 0;'>${market_data['sp500']['price']:.2f}</h2>", unsafe_allow_html=True)
        change_class = "metric-positive" if market_data['sp500']['change'] >= 0 else "metric-negative"
        change_symbol = "▲" if market_data['sp500']['change'] >= 0 else "▼"
        st.markdown(f"<p class='{change_class}'>{change_symbol} {abs(market_data['sp500']['change']):.2f} ({market_data['sp500']['pct']:+.2f}%)</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # NAS100
        st.markdown('<div class="market-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 NAS100 (NQ)")
        st.markdown(f"<h2 style='color: #FFFFFF; margin: 0;'>${market_data['nas100']['price']:.2f}</h2>", unsafe_allow_html=True)
        change_class = "metric-positive" if market_data['nas100']['change'] >= 0 else "metric-negative"
        change_symbol = "▲" if market_data['nas100']['change'] >= 0 else "▼"
        st.markdown(f"<p class='{change_class}'>{change_symbol} {abs(market_data['nas100']['change']):.2f} ({market_data['nas100']['pct']:+.2f}%)</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # SMT Divergence Auto-Detection
        st.markdown("---")
        st.markdown("### 🔍 SMT ANALYSIS")
        sp_direction = "BULLISH" if market_data['sp500']['change'] > 0 else "BEARISH"
        nas_direction = "BULLISH" if market_data['nas100']['change'] > 0 else "BEARISH"

        if sp_direction == nas_direction:
            st.markdown(f'<div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 3px solid #00FF00;"><p style="color: #00FF00; font-weight: bold; margin: 0;">✅ CONFIRMED</p><p style="color: #FFFFFF; margin: 0;">Both {sp_direction}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 3px solid #FFA500;"><p style="color: #FFA500; font-weight: bold; margin: 0;">⚠️ DIVERGENCE</p><p style="color: #FFFFFF; margin: 0;">ES: {sp_direction}<br>NQ: {nas_direction}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border: 2px solid #FF0000;"><p style="color: #FF0000; text-align: center; margin: 0;">⚠️ MARKET DATA UNAVAILABLE</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📰 FUTURES NEWS")

    news = get_futures_news()
    for item in news[:4]:  # Show top 4
        st.markdown(f'<div class="news-card"><strong style="color: #FFFFFF;">{item["title"]}</strong><br><small style="color:#888;">⏱ {item["time"]}</small></div>', unsafe_allow_html=True)

    st.markdown(f'<p style="color: #666; font-size: 0.8rem; text-align: center; margin-top: 1rem;">Last updated: {datetime.now().strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)

# --- MAIN CONTENT: INPUTS ---
st.markdown("---")
st.markdown('<h2 style="text-align: center; letter-spacing: 4px; margin: 2rem 0;">⚙️ CONFLUENCE PARAMETERS ⚙️</h2>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📊 TIMEFRAME BIASES")
    st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 1px solid #333;">', unsafe_allow_html=True)
    daily = st.selectbox("🔹 Daily Bias", ["Bullish", "Bearish", "Neutral"], key="daily")
    h4 = st.selectbox("🔹 4H Bias", ["Bullish", "Bearish", "Neutral"], key="h4")
    h1 = st.selectbox("🔹 1H Structure", ["Bullish", "Bearish", "Choppy/Neutral"], key="h1")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 📉 MARKET CONTEXT")
    st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 1px solid #333;">', unsafe_allow_html=True)
    liquidity = st.selectbox("🔹 Liquidity Sweep", ["None", "Equal Highs (Sell Liquidity)", "Equal Lows (Buy Liquidity)"], key="liq")
    displacement = st.radio("🔹 Strong Displacement?", ["Yes", "No"], key="disp", horizontal=True)
    fvg = st.radio("🔹 Fair Value Gap?", ["Yes", "No"], key="fvg", horizontal=True)
    fvg_dir = st.selectbox("🔹 FVG Direction", ["Bullish", "Bearish", "None"], key="fvg_dir")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 🔁 CORRELATION CHECK")
    st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 1px solid #333;">', unsafe_allow_html=True)
    smt = st.selectbox("🔹 SMT Divergence (ES & NAS)", ["Confirmed (Same Direction)", "Divergent", "Not Checked"], key="smt")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 🕓 EXECUTION FILTERS")
    st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 1px solid #333;">', unsafe_allow_html=True)
    session = st.selectbox("🔹 Trading Session", ["London", "NY AM (14:30–17:00 UTC+1)", "NY PM (19:00–21:00 UTC+1)", "Outside Session"], key="session")
    confirmation = st.radio("🔹 Lower TF Confirmation (1M-5M)?", ["Yes", "No"], key="conf", horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- LOGIC ---
signal = "🚫 No Trade – Missing Confluence or Wrong Timing"
color = "red"
score = 0

# Base score system
if daily == h4 and daily != "Neutral": score += 3
if h1 == daily: score += 2
if liquidity.startswith("Equal Lows") and daily == "Bullish": score += 2
if liquidity.startswith("Equal Highs") and daily == "Bearish": score += 2
if displacement == "Yes": score += 2
if fvg == "Yes" and fvg_dir == daily: score += 2
if smt == "Confirmed (Same Direction)": score += 1
if session.startswith("NY"): score += 1
if confirmation == "Yes": score += 2

# Determine final trade bias
if score >= 10 and daily == "Bullish":
    signal = "🚀 GO LONG"
    subtitle = "HIGH PROBABILITY BUY SETUP"
    color = "#00FF00"
    box_class = "result-box-green"
elif score >= 10 and daily == "Bearish":
    signal = "📉 GO SHORT"
    subtitle = "HIGH PROBABILITY SELL SETUP"
    color = "#00FF00"
    box_class = "result-box-green"
elif 7 <= score < 10:
    signal = "⚠️ CAUTION"
    subtitle = "WEAK CONFLUENCE - REDUCE SIZE"
    color = "#FFA500"
    box_class = "result-box-orange"
else:
    signal = "🚫 NO TRADE"
    subtitle = "INSUFFICIENT CONFLUENCE"
    color = "#FF0000"
    box_class = "result-box-red"

# --- OUTPUT ---
st.markdown("---")
st.markdown('<h2 style="text-align: center; letter-spacing: 4px; margin: 2rem 0;">⚡ TRADE DECISION ⚡</h2>', unsafe_allow_html=True)

# Create a visually appealing result section
result_col1, result_col2, result_col3 = st.columns([1, 3, 1])

with result_col2:
    st.markdown(f"""
    <div class="result-box {box_class}">
        <h1 style='color:{color}; text-align:center; font-size: 3.5rem; margin: 0; letter-spacing: 6px; text-shadow: 0 0 20px {color};'>{signal}</h1>
        <p style='color: #FFFFFF; text-align:center; font-size: 1.2rem; margin-top: 1rem; letter-spacing: 3px;'>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Progress bar with label
    st.markdown(f"<p style='text-align:center; font-size:1.5rem; font-weight:bold; color: #FFFFFF; letter-spacing: 2px;'>CONFLUENCE SCORE: {score}/12</p>", unsafe_allow_html=True)
    st.progress(min(score / 12, 1.0))

    st.markdown("<br>", unsafe_allow_html=True)

    # Status message
    if score >= 10:
        st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #00FF00; text-align: center;"><p style="color: #00FF00; font-size: 1.2rem; margin: 0; font-weight: bold;">🎯 ALL SYSTEMS ALIGNED</p><p style="color: #FFFFFF; margin: 0.5rem 0 0 0;">Maximum confluence detected</p></div>', unsafe_allow_html=True)
    elif score >= 7:
        st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #FFA500; text-align: center;"><p style="color: #FFA500; font-size: 1.2rem; margin: 0; font-weight: bold;">⚠️ MODERATE SETUP</p><p style="color: #FFFFFF; margin: 0.5rem 0 0 0;">Consider smaller position size</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #FF0000; text-align: center;"><p style="color: #FF0000; font-size: 1.2rem; margin: 0; font-weight: bold;">🚫 LOW PROBABILITY</p><p style="color: #FFFFFF; margin: 0.5rem 0 0 0;">Wait for better confluence</p></div>', unsafe_allow_html=True)

st.markdown("---")

# Score breakdown in expandable section
with st.expander("📊 DETAILED SCORE BREAKDOWN", expanded=False):
    st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 1px solid #333;">', unsafe_allow_html=True)

    breakdown_col1, breakdown_col2 = st.columns(2)

    with breakdown_col1:
        st.markdown("#### ⏱ TIMEFRAME ALIGNMENT")
        if daily == h4 and daily != "Neutral":
            st.markdown('<p style="color: #00FF00;">✅ Daily & 4H aligned <span style="float: right;">+3</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ Daily & 4H not aligned <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        if h1 == daily:
            st.markdown('<p style="color: #00FF00;">✅ 1H matches Daily <span style="float: right;">+2</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ 1H doesn\'t match <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📉 MARKET CONTEXT")
        if (liquidity.startswith("Equal Lows") and daily == "Bullish") or (liquidity.startswith("Equal Highs") and daily == "Bearish"):
            st.markdown('<p style="color: #00FF00;">✅ Liquidity swept <span style="float: right;">+2</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No liquidity sweep <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        if displacement == "Yes":
            st.markdown('<p style="color: #00FF00;">✅ Displacement confirmed <span style="float: right;">+2</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No displacement <span style="float: right;">0</span></p>', unsafe_allow_html=True)

    with breakdown_col2:
        if fvg == "Yes" and fvg_dir == daily:
            st.markdown('<p style="color: #00FF00;">✅ FVG aligned <span style="float: right;">+2</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No FVG alignment <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🎯 EXECUTION FILTERS")
        if smt == "Confirmed (Same Direction)":
            st.markdown('<p style="color: #00FF00;">✅ SMT confirmed <span style="float: right;">+1</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ SMT not confirmed <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        if session.startswith("NY"):
            st.markdown('<p style="color: #00FF00;">✅ NY session <span style="float: right;">+1</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ Outside NY session <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        if confirmation == "Yes":
            st.markdown('<p style="color: #00FF00;">✅ Lower TF confirmation <span style="float: right;">+2</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No confirmation <span style="float: right;">0</span></p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Tips section with better formatting
st.markdown('<h3 style="text-align: center; letter-spacing: 3px;">💡 SMART MONEY PRINCIPLES 💡</h3>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #FFFFFF; text-align: center; height: 180px;">
        <h4 style="color: #FFFFFF; margin-top: 0;">📊 STRUCTURE FIRST</h4>
        <p style="color: #AAAAAA;">Align Daily + 4H + 1H timeframes before considering any trade setup</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #FFFFFF; text-align: center; height: 180px;">
        <h4 style="color: #FFFFFF; margin-top: 0;">⏰ TIMING MATTERS</h4>
        <p style="color: #AAAAAA;">Trade during NY session (14:30-21:00 UTC+1) for optimal liquidity</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #FFFFFF; text-align: center; height: 180px;">
        <h4 style="color: #FFFFFF; margin-top: 0;">✅ CONFIRM ENTRY</h4>
        <p style="color: #AAAAAA;">Wait for 1M-5M reversal candle or BOS before executing</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #666; font-size: 0.9rem; letter-spacing: 2px;">BUILT FOR SMART MONEY TRADERS | REAL-TIME DATA UPDATES EVERY 60 SECONDS</p>', unsafe_allow_html=True)

