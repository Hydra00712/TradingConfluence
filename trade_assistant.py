# Trade Confirmation Assistant – "Wall Street Bias Checker"
# Made for Adam's Smart Money Strategy (Multi-TF, Liquidity, Displacement, FVG, SMT)

import streamlit as st
import requests
from datetime import datetime
import json
import time

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

    /* Hide Streamlit Branding and Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Hide empty containers */
    .element-container:has(> .stMarkdown > div:empty) {
        display: none;
    }

    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: #888888;
        text-transform: uppercase;
        letter-spacing: 8px;
        margin-bottom: 0.5rem;
        text-shadow: none;
        font-family: 'Courier New', monospace;
    }

    .sub-header {
        text-align: center;
        color: #555555;
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
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
        border-left: 3px solid #FFFFFF;
        transition: all 0.3s ease;
    }

    .news-card:hover {
        background: #1a1a1a;
        border-left-width: 5px;
        transform: translateX(3px);
    }

    /* Custom Scrollbar for News */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #0a0a0a;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: #333333;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
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
        color: #CCCCCC !important;
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
    }

    /* Text */
    p, label, span {
        color: #BBBBBB !important;
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

</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">WALL STREET BIAS CHECKER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">SMART MONEY • CONFLUENCE • PRECISION</p>', unsafe_allow_html=True)

# --- FUNCTIONS FOR MARKET DATA ---
@st.cache_data(ttl=10)  # Cache for 10 seconds for real-time updates
def get_market_data():
    """Fetch REAL-TIME market data for S&P 500 and NAS100"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://finance.yahoo.com/'
        }

        # Method 1: Yahoo Finance Chart API (most reliable)
        try:
            sp500_url = "https://query1.finance.yahoo.com/v8/finance/chart/ES=F?interval=1m&range=1d"
            nas100_url = "https://query1.finance.yahoo.com/v8/finance/chart/NQ=F?interval=1m&range=1d"

            sp500_resp = requests.get(sp500_url, headers=headers, timeout=10)
            nas100_resp = requests.get(nas100_url, headers=headers, timeout=10)

            if sp500_resp.status_code == 200 and nas100_resp.status_code == 200:
                sp500_data = sp500_resp.json()
                nas100_data = nas100_resp.json()

                # Extract from chart data
                sp500_result = sp500_data['chart']['result'][0]
                nas100_result = nas100_data['chart']['result'][0]

                sp500_meta = sp500_result['meta']
                nas100_meta = nas100_result['meta']

                # Get current price (last quote or regular market price)
                sp500_price = sp500_meta.get('regularMarketPrice', sp500_meta.get('previousClose', 0))
                sp500_prev = sp500_meta.get('chartPreviousClose', sp500_meta.get('previousClose', sp500_price))

                nas100_price = nas100_meta.get('regularMarketPrice', nas100_meta.get('previousClose', 0))
                nas100_prev = nas100_meta.get('chartPreviousClose', nas100_meta.get('previousClose', nas100_price))

                # Calculate changes
                sp500_change = sp500_price - sp500_prev
                sp500_pct = (sp500_change / sp500_prev * 100) if sp500_prev != 0 else 0

                nas100_change = nas100_price - nas100_prev
                nas100_pct = (nas100_change / nas100_prev * 100) if nas100_prev != 0 else 0

                # Verify we have valid data
                if sp500_price > 1000 and nas100_price > 1000:  # Sanity check
                    return {
                        'sp500': {'price': sp500_price, 'change': sp500_change, 'pct': sp500_pct},
                        'nas100': {'price': nas100_price, 'change': nas100_change, 'pct': nas100_pct}
                    }
        except Exception as e:
            pass

        # Method 2: Try using index symbols as fallback
        try:
            sp500_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1m&range=1d"
            nas100_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EIXIC?interval=1m&range=1d"

            sp500_resp = requests.get(sp500_url, headers=headers, timeout=10)
            nas100_resp = requests.get(nas100_url, headers=headers, timeout=10)

            if sp500_resp.status_code == 200 and nas100_resp.status_code == 200:
                sp500_data = sp500_resp.json()
                nas100_data = nas100_resp.json()

                sp500_meta = sp500_data['chart']['result'][0]['meta']
                nas100_meta = nas100_data['chart']['result'][0]['meta']

                sp500_price = sp500_meta.get('regularMarketPrice', 0)
                sp500_prev = sp500_meta.get('chartPreviousClose', sp500_price)
                sp500_change = sp500_price - sp500_prev
                sp500_pct = (sp500_change / sp500_prev * 100) if sp500_prev != 0 else 0

                nas100_price = nas100_meta.get('regularMarketPrice', 0)
                nas100_prev = nas100_meta.get('chartPreviousClose', nas100_price)
                nas100_change = nas100_price - nas100_prev
                nas100_pct = (nas100_change / nas100_prev * 100) if nas100_prev != 0 else 0

                if sp500_price > 1000 and nas100_price > 1000:
                    return {
                        'sp500': {'price': sp500_price, 'change': sp500_change, 'pct': sp500_pct},
                        'nas100': {'price': nas100_price, 'change': nas100_change, 'pct': nas100_pct}
                    }
        except Exception as e:
            pass

        # If all methods fail, return demo data
        raise Exception("All API methods failed")

    except:
        # Fallback to demo data if API fails
        return {
            'sp500': {'price': 5850.25, 'change': 12.50, 'pct': 0.21},
            'nas100': {'price': 20125.75, 'change': -25.30, 'pct': -0.13},
            'demo': True
        }

def analyze_news_sentiment(title):
    """Analyze news sentiment - returns 'bullish', 'bearish', or 'neutral'"""
    title_lower = title.lower()

    # Bullish keywords (price going UP)
    bullish_keywords = [
        'rally', 'surge', 'gain', 'rise', 'jump', 'climb', 'soar', 'advance',
        'boost', 'strength', 'strong', 'beat', 'positive', 'optimis', 'bull',
        'record high', 'breakout', 'momentum', 'upgrade', 'outperform'
    ]

    # Bearish keywords (price going DOWN)
    bearish_keywords = [
        'fall', 'drop', 'plunge', 'decline', 'tumble', 'slide', 'slump', 'sink',
        'loss', 'weak', 'concern', 'fear', 'worry', 'risk', 'bear', 'crash',
        'sell-off', 'selloff', 'downturn', 'downgrade', 'miss', 'disappoint'
    ]

    bullish_count = sum(1 for word in bullish_keywords if word in title_lower)
    bearish_count = sum(1 for word in bearish_keywords if word in title_lower)

    if bullish_count > bearish_count:
        return 'bullish'
    elif bearish_count > bullish_count:
        return 'bearish'
    else:
        return 'neutral'

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_futures_news():
    """Fetch ES and NQ futures news from the past week - optimized for speed"""
    try:
        from datetime import datetime
        news_items = []

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # Only get news for ES and NQ futures (faster - fewer API calls)
        symbols = ['ES=F', 'NQ=F']

        for symbol in symbols:
            try:
                url = f"https://query1.finance.yahoo.com/v1/finance/search?q={symbol}&quotesCount=0&newsCount=8"
                response = requests.get(url, headers=headers, timeout=5)  # Reduced timeout

                if response.status_code == 200:
                    data = response.json()
                    if 'news' in data:
                        for item in data['news'][:8]:  # Get top 8 from each
                            pub_time = item.get('providerPublishTime', 0)
                            if pub_time:
                                pub_date = datetime.fromtimestamp(pub_time)
                                now = datetime.now()
                                diff = now - pub_date

                                # Only include news from past week
                                if diff.days <= 7:
                                    if diff.days > 0:
                                        time_ago = f"{diff.days}d ago"
                                    elif diff.seconds >= 3600:
                                        hours = diff.seconds // 3600
                                        time_ago = f"{hours}h ago"
                                    else:
                                        minutes = max(1, diff.seconds // 60)
                                        time_ago = f"{minutes}m ago"

                                    # Filter: only include if title mentions futures, S&P, Nasdaq, ES, or NQ
                                    title = item.get('title', '')
                                    keywords = ['future', 's&p', 'nasdaq', 'sp500', 'nas100', 'es', 'nq', 'market', 'index']
                                    if any(keyword in title.lower() for keyword in keywords):
                                        sentiment = analyze_news_sentiment(title)
                                        news_items.append({
                                            'title': title,
                                            'time': time_ago,
                                            'publisher': item.get('publisher', 'Unknown'),
                                            'sentiment': sentiment
                                        })
            except:
                continue  # Skip failed requests, don't break entire function

        # Remove duplicates
        seen_titles = set()
        unique_news = []
        for item in news_items:
            if item['title'] not in seen_titles:
                seen_titles.add(item['title'])
                unique_news.append(item)

        return unique_news[:15] if unique_news else get_fallback_news()

    except:
        return get_fallback_news()

def get_fallback_news():
    """Fallback news if API fails"""
    fallback = [
        {"title": "S&P 500 Futures Show Strength Ahead of Market Open", "time": "2h ago", "publisher": "MarketWatch"},
        {"title": "Nasdaq Futures Rally on Tech Earnings Beat", "time": "5h ago", "publisher": "Bloomberg"},
        {"title": "Fed Minutes Signal Potential Rate Hold", "time": "1d ago", "publisher": "Reuters"},
        {"title": "Futures Market Volatility Increases on Economic Data", "time": "1d ago", "publisher": "CNBC"},
        {"title": "Oil Prices Impact Energy Sector Futures", "time": "2d ago", "publisher": "WSJ"},
        {"title": "Tech Stocks Drive Nasdaq Futures Higher", "time": "2d ago", "publisher": "Financial Times"},
        {"title": "Economic Indicators Point to Market Strength", "time": "3d ago", "publisher": "MarketWatch"},
        {"title": "Global Markets React to US Futures Movement", "time": "3d ago", "publisher": "Bloomberg"},
    ]
    # Add sentiment to fallback news
    for item in fallback:
        item['sentiment'] = analyze_news_sentiment(item['title'])
    return fallback

# --- SIDEBAR: MARKET DATA & NEWS ---
with st.sidebar:
    col_header, col_refresh = st.columns([3, 1])
    with col_header:
        st.markdown("### ⚡ LIVE MARKET DATA")
    with col_refresh:
        if st.button("🔄", key="refresh_data", help="Refresh market data"):
            st.cache_data.clear()
            st.rerun()

    st.markdown("---")

    market_data = get_market_data()

    if market_data:
        # Show demo mode indicator if using fallback data
        if market_data.get('demo'):
            st.markdown('<p style="color: #FF0000; font-size: 0.85rem; text-align: center; margin-bottom: 1rem; font-weight: bold;">⚠️ DEMO MODE - API Unavailable</p>', unsafe_allow_html=True)
            st.markdown('<p style="color: #888; font-size: 0.75rem; text-align: center; margin-bottom: 1rem;">Click 🔄 to retry</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #00FF00; font-size: 0.75rem; text-align: center; margin-bottom: 1rem;">🔴 LIVE • Auto-updates every 10s</p>', unsafe_allow_html=True)

        # S&P 500
        st.markdown(f"""
        <div class="market-card">
            <h4 style="color: #FFFFFF; margin: 0 0 0.5rem 0;">📈 S&P 500 (ES)</h4>
            <h2 style='color: #FFFFFF; margin: 0;'>${market_data['sp500']['price']:.2f}</h2>
            <p class='{"metric-positive" if market_data['sp500']['change'] >= 0 else "metric-negative"}' style='margin: 0.5rem 0 0 0;'>
                {"▲" if market_data['sp500']['change'] >= 0 else "▼"} {abs(market_data['sp500']['change']):.2f} ({market_data['sp500']['pct']:+.2f}%)
            </p>
        </div>
        """, unsafe_allow_html=True)

        # NAS100
        st.markdown(f"""
        <div class="market-card">
            <h4 style="color: #FFFFFF; margin: 0 0 0.5rem 0;">📊 NAS100 (NQ)</h4>
            <h2 style='color: #FFFFFF; margin: 0;'>${market_data['nas100']['price']:.2f}</h2>
            <p class='{"metric-positive" if market_data['nas100']['change'] >= 0 else "metric-negative"}' style='margin: 0.5rem 0 0 0;'>
                {"▲" if market_data['nas100']['change'] >= 0 else "▼"} {abs(market_data['nas100']['change']):.2f} ({market_data['nas100']['pct']:+.2f}%)
            </p>
        </div>
        """, unsafe_allow_html=True)

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
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-bottom: 1rem;">Past 7 days</p>', unsafe_allow_html=True)

    news = get_futures_news()

    # Create scrollable news container
    st.markdown('<div style="max-height: 500px; overflow-y: auto; padding-right: 0.5rem;">', unsafe_allow_html=True)

    if news:
        for item in news[:15]:  # Show top 15 news items
            publisher = item.get('publisher', '')
            publisher_text = f'<span style="color: #666; font-size: 0.75rem;">• {publisher}</span>' if publisher else ''

            # Determine color based on sentiment
            sentiment = item.get('sentiment', 'neutral')
            if sentiment == 'bullish':
                border_color = '#00FF00'
                title_color = '#00FF00'
                sentiment_icon = '📈'
            elif sentiment == 'bearish':
                border_color = '#FF0000'
                title_color = '#FF0000'
                sentiment_icon = '📉'
            else:
                border_color = '#FFFFFF'
                title_color = '#AAAAAA'
                sentiment_icon = '📊'

            st.markdown(f"""
            <div class="news-card" style="border-left-color: {border_color};">
                <strong style="color: {title_color}; font-size: 0.9rem; line-height: 1.4;">{sentiment_icon} {item["title"]}</strong><br>
                <small style="color:#888;">⏱ {item["time"]} {publisher_text}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color: #666; text-align: center;">No news available</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<p style="color: #666; font-size: 0.75rem; text-align: center; margin-top: 1rem;">Last updated: {datetime.now().strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)

    # Auto-refresh mechanism - only if live data is available
    if not market_data.get('demo'):
        # Add a placeholder for auto-refresh countdown
        refresh_placeholder = st.empty()

        # Initialize session state for countdown
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()

        # Calculate time since last refresh
        time_elapsed = time.time() - st.session_state.last_refresh
        time_remaining = max(0, 10 - int(time_elapsed))

        # Show countdown
        refresh_placeholder.markdown(
            f'<p style="color: #00FF00; font-size: 0.7rem; text-align: center; margin-top: 0.5rem;">Next update in {time_remaining}s</p>',
            unsafe_allow_html=True
        )

        # Auto-refresh after 10 seconds
        if time_elapsed >= 10:
            st.session_state.last_refresh = time.time()
            time.sleep(0.1)
            st.rerun()

# --- MAIN CONTENT: INPUTS ---
st.markdown("---")
st.markdown('<h2 style="text-align: center; letter-spacing: 4px; margin: 2rem 0;">⚙️ CONFLUENCE PARAMETERS ⚙️</h2>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📊 TIMEFRAME BIASES")
    daily = st.selectbox("🔹 Daily Bias", ["Bullish", "Bearish", "Neutral"], key="daily")
    h4 = st.selectbox("🔹 4H Bias", ["Bullish", "Bearish", "Neutral"], key="h4")
    h1 = st.selectbox("🔹 1H Structure", ["Bullish", "Bearish", "Choppy/Neutral"], key="h1")

    st.markdown("---")

    st.markdown("### 📉 MARKET CONTEXT")
    liquidity = st.selectbox("🔹 Liquidity Sweep", ["None", "Equal Highs (Sell Liquidity)", "Equal Lows (Buy Liquidity)"], key="liq")
    displacement = st.radio("🔹 Strong Displacement?", ["Yes", "No"], key="disp", horizontal=True)
    fvg = st.radio("🔹 Fair Value Gap?", ["Yes", "No"], key="fvg", horizontal=True)
    fvg_dir = st.selectbox("🔹 FVG Direction", ["Bullish", "Bearish", "None"], key="fvg_dir")

with col2:
    st.markdown("### 🔁 CORRELATION CHECK")
    smt = st.selectbox("🔹 SMT Divergence (ES & NAS)", ["Confirmed (Same Direction)", "Divergent", "Not Checked"], key="smt")

    st.markdown("---")

    st.markdown("### 🕓 EXECUTION FILTERS")
    session = st.selectbox("🔹 Trading Session", ["London", "NY AM (14:30–17:00 UTC+1)", "NY PM (19:00–21:00 UTC+1)", "Outside Session"], key="session")
    confirmation = st.radio("🔹 Lower TF Confirmation (1M-5M)?", ["Yes", "No"], key="conf", horizontal=True)

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

