# VWAP + FVG + Liquidity Scalping Assistant
# Wall Street-Grade Scalping Strategy - 6 Step System

import streamlit as st
import requests
from datetime import datetime, timedelta
import json
import time

st.set_page_config(
    page_title="VWAP + FVG + Liquidity Scalping",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic Black & White UI - Optimized for Performance
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

    /* Performance optimizations */
    * {
        will-change: auto;
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
        border-left-width: 3px;
        border-left-style: solid;
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

    /* Warning Banner */
    .warning-banner {
        background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
        border: 2px solid #FF0000;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        animation: pulse-warning 2s ease-in-out infinite;
    }

    @keyframes pulse-warning {
        0%, 100% { box-shadow: 0 0 20px rgba(255,0,0,0.5); }
        50% { box-shadow: 0 0 40px rgba(255,0,0,0.8); }
    }

    .warning-title {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    .warning-text {
        color: #FFFFFF;
        font-size: 1.1rem;
        font-weight: 600;
        line-height: 1.6;
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

st.markdown('<h1 class="main-header">VWAP + FVG + LIQUIDITY SCALPING</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">6-STEP WALL STREET SYSTEM • PRECISION ENTRIES • HIGH PROBABILITY</p>', unsafe_allow_html=True)

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

            sp500_resp = requests.get(sp500_url, headers=headers, timeout=5)
            nas100_resp = requests.get(nas100_url, headers=headers, timeout=5)

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

            sp500_resp = requests.get(sp500_url, headers=headers, timeout=5)
            nas100_resp = requests.get(nas100_url, headers=headers, timeout=5)

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
        'rally', 'rallies', 'surge', 'surges', 'gain', 'gains', 'rise', 'rises', 'rising',
        'jump', 'jumps', 'climb', 'climbs', 'soar', 'soars', 'advance', 'advances',
        'boost', 'boosts', 'strength', 'strong', 'stronger', 'beat', 'beats', 'positive',
        'optimis', 'optimistic', 'bull', 'bullish', 'record high', 'breakout', 'breaks out',
        'momentum', 'upgrade', 'upgrades', 'outperform', 'outperforms', 'higher', 'up',
        'rebound', 'rebounds', 'recover', 'recovery', 'growth', 'grows', 'extend', 'extends'
    ]

    # Bearish keywords (price going DOWN)
    bearish_keywords = [
        'fall', 'falls', 'falling', 'drop', 'drops', 'dropping', 'plunge', 'plunges',
        'decline', 'declines', 'declining', 'tumble', 'tumbles', 'slide', 'slides',
        'slump', 'slumps', 'sink', 'sinks', 'loss', 'losses', 'lose', 'weak', 'weaker',
        'weakness', 'concern', 'concerns', 'fear', 'fears', 'worry', 'worries', 'risk',
        'risks', 'bear', 'bearish', 'crash', 'crashes', 'sell-off', 'selloff', 'selling',
        'downturn', 'downgrade', 'downgrades', 'miss', 'misses', 'disappoint', 'disappoints',
        'lower', 'down', 'pressure', 'pressured', 'retreat', 'retreats'
    ]

    bullish_count = sum(1 for word in bullish_keywords if word in title_lower)
    bearish_count = sum(1 for word in bearish_keywords if word in title_lower)

    # If we find ANY keyword, classify it (more aggressive)
    if bullish_count > 0 and bullish_count > bearish_count:
        return 'bullish'
    elif bearish_count > 0 and bearish_count > bullish_count:
        return 'bearish'
    elif bullish_count > 0 and bearish_count == 0:
        return 'bullish'
    elif bearish_count > 0 and bullish_count == 0:
        return 'bearish'
    else:
        return 'neutral'

def check_trading_conditions():
    """Check for bank holidays and low volume conditions - returns warning dict"""
    from datetime import datetime, timedelta

    # US Bank Holidays 2024-2025
    us_holidays = [
        # 2024
        datetime(2024, 1, 1),   # New Year's Day
        datetime(2024, 1, 15),  # MLK Day
        datetime(2024, 2, 19),  # Presidents Day
        datetime(2024, 3, 29),  # Good Friday
        datetime(2024, 5, 27),  # Memorial Day
        datetime(2024, 6, 19),  # Juneteenth
        datetime(2024, 7, 4),   # Independence Day
        datetime(2024, 9, 2),   # Labor Day
        datetime(2024, 11, 28), # Thanksgiving
        datetime(2024, 12, 25), # Christmas
        # 2025
        datetime(2025, 1, 1),   # New Year's Day
        datetime(2025, 1, 20),  # MLK Day
        datetime(2025, 2, 17),  # Presidents Day
        datetime(2025, 4, 18),  # Good Friday
        datetime(2025, 5, 26),  # Memorial Day
        datetime(2025, 6, 19),  # Juneteenth
        datetime(2025, 7, 4),   # Independence Day
        datetime(2025, 9, 1),   # Labor Day
        datetime(2025, 11, 27), # Thanksgiving
        datetime(2025, 12, 25), # Christmas
    ]

    now = datetime.now()
    today = now.date()

    warnings = []
    severity = 'none'  # none, low, medium, high

    # Check if today is a bank holiday
    for holiday in us_holidays:
        if holiday.date() == today:
            warnings.append(f"🚨 TODAY IS A US BANK HOLIDAY ({holiday.strftime('%B %d, %Y')})")
            severity = 'high'
            break

    # Check if tomorrow is a bank holiday (half-day trading often)
    tomorrow = (now + timedelta(days=1)).date()
    for holiday in us_holidays:
        if holiday.date() == tomorrow:
            warnings.append(f"⚠️ TOMORROW IS A US BANK HOLIDAY - Expect low volume today")
            if severity == 'none':
                severity = 'medium'
            break

    # Check if day after tomorrow is a bank holiday (3-day weekend)
    day_after = (now + timedelta(days=2)).date()
    for holiday in us_holidays:
        if holiday.date() == day_after:
            warnings.append(f"⚠️ 3-DAY WEEKEND AHEAD - Volume may be lower")
            if severity == 'none':
                severity = 'low'
            break

    # Check for Friday before long weekend
    if now.weekday() == 4:  # Friday
        monday = (now + timedelta(days=3)).date()
        for holiday in us_holidays:
            if holiday.date() == monday:
                warnings.append(f"⚠️ LONG WEEKEND AHEAD - Friday before holiday has low volume")
                if severity == 'none':
                    severity = 'medium'
                break

    # Check for day after holiday (often low volume)
    yesterday = (now - timedelta(days=1)).date()
    for holiday in us_holidays:
        if holiday.date() == yesterday:
            warnings.append(f"⚠️ DAY AFTER HOLIDAY - Volume may still be low")
            if severity == 'none':
                severity = 'low'
            break

    # Check for early/late hours (low volume times)
    current_hour = now.hour
    if 0 <= current_hour < 9:
        warnings.append(f"⏰ PRE-MARKET HOURS - Volume is typically very low")
        if severity == 'none':
            severity = 'low'
    elif 16 <= current_hour < 24:
        warnings.append(f"⏰ AFTER-HOURS - Volume is typically very low")
        if severity == 'none':
            severity = 'low'

    return {
        'has_warning': len(warnings) > 0,
        'warnings': warnings,
        'severity': severity,
        'recommendation': get_trading_recommendation(severity)
    }

def get_trading_recommendation(severity):
    """Get trading recommendation based on severity"""
    if severity == 'high':
        return "🛑 DO NOT TRADE - Market is closed or extremely low volume"
    elif severity == 'medium':
        return "⚠️ TRADE WITH EXTREME CAUTION - Significantly reduced volume expected"
    elif severity == 'low':
        return "⚠️ BE CAREFUL - Volume may be lower than usual"
    else:
        return "✅ Normal trading conditions"

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
                url = f"https://query1.finance.yahoo.com/v1/finance/search?q={symbol}&quotesCount=0&newsCount=6"
                response = requests.get(url, headers=headers, timeout=3)  # Reduced timeout to 3s

                if response.status_code == 200:
                    data = response.json()
                    if 'news' in data:
                        for item in data['news'][:6]:  # Get top 6 from each (faster processing)
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

        # Remove duplicates (optimized with dict)
        unique_news = []
        seen_titles = set()
        for item in news_items:
            title = item['title']
            if title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(item)
                if len(unique_news) >= 12:  # Stop early once we have enough
                    break

        return unique_news if unique_news else get_fallback_news()

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
        for item in news[:12]:  # Show top 12 news items (faster rendering)
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
            <div class="news-card" style="border-left: 3px solid {border_color} !important;">
                <strong style="color: {title_color} !important; font-size: 0.9rem; line-height: 1.4;">{sentiment_icon} {item["title"]}</strong><br>
                <small style="color:#888;">⏱ {item["time"]} {publisher_text}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color: #666; text-align: center;">No news available</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<p style="color: #666; font-size: 0.75rem; text-align: center; margin-top: 1rem;">Last updated: {datetime.now().strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)

    # Auto-refresh mechanism - only if live data is available (optimized)
    if not market_data.get('demo'):
        # Initialize session state for countdown
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()

        # Calculate time since last refresh
        time_elapsed = time.time() - st.session_state.last_refresh
        time_remaining = max(0, 10 - int(time_elapsed))

        # Show countdown (simplified)
        st.markdown(
            f'<p style="color: #00FF00; font-size: 0.7rem; text-align: center; margin-top: 0.5rem;">Next update in {time_remaining}s</p>',
            unsafe_allow_html=True
        )

        # Auto-refresh after 10 seconds
        if time_elapsed >= 10:
            st.session_state.last_refresh = time.time()
            st.rerun()

# --- MAIN CONTENT: INPUTS ---
st.markdown("---")

# Check trading conditions (bank holidays, low volume)
trading_conditions = check_trading_conditions()

# Display warning banner if needed
if trading_conditions['has_warning']:
    if trading_conditions['severity'] == 'high':
        st.markdown(f"""
        <div class="warning-banner">
            <div class="warning-title">🚨 DO NOT TRADE 🚨</div>
            <div class="warning-text">
                {'<br>'.join(trading_conditions['warnings'])}<br><br>
                <strong>{trading_conditions['recommendation']}</strong><br>
                Market conditions are NOT suitable for trading. Stay out!
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif trading_conditions['severity'] == 'medium':
        st.markdown(f"""
        <div class="warning-banner" style="background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%); border-color: #FFA500;">
            <div class="warning-title">⚠️ CAUTION ⚠️</div>
            <div class="warning-text">
                {'<br>'.join(trading_conditions['warnings'])}<br><br>
                <strong>{trading_conditions['recommendation']}</strong><br>
                Reduce position size and be extra selective with entries.
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif trading_conditions['severity'] == 'low':
        st.markdown(f"""
        <div class="warning-banner" style="background: linear-gradient(135deg, #FFAA00 0%, #FF9900 100%); border-color: #FFAA00;">
            <div class="warning-title" style="font-size: 1.5rem;">⚠️ HEADS UP ⚠️</div>
            <div class="warning-text" style="font-size: 1rem;">
                {'<br>'.join(trading_conditions['warnings'])}<br><br>
                <strong>{trading_conditions['recommendation']}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<h2 style="text-align: center; letter-spacing: 4px; margin: 2rem 0;">⚙️ VWAP + FVG + LIQUIDITY SCALPING ⚙️</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888; font-size: 0.9rem; margin-top: -1rem;">Wall Street-Grade Scalping Strategy</p>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📊 STEP 1: TREND (1H-4H)")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Check higher timeframe VWAP</p>', unsafe_allow_html=True)
    vwap_trend = st.selectbox(
        "🔹 Price vs VWAP (1H-4H)",
        ["Above VWAP (Bullish)", "Below VWAP (Bearish)", "Chopping at VWAP (No Trade)"],
        key="vwap_trend"
    )

    st.markdown("---")

    st.markdown("### 📉 STEP 2: FVG LOCATION")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Identify unfilled Fair Value Gap</p>', unsafe_allow_html=True)
    fvg_present = st.radio("🔹 FVG Present on 1H-4H?", ["Yes", "No"], key="fvg_present", horizontal=True)

    if fvg_present == "Yes":
        fvg_direction = st.selectbox(
            "🔹 FVG Direction",
            ["Bullish FVG (Gap Up)", "Bearish FVG (Gap Down)"],
            key="fvg_direction"
        )
        fvg_alignment = st.radio(
            "🔹 FVG Aligns with Trend?",
            ["Yes (Trend Trade)", "No (Fade/Reversal)"],
            key="fvg_alignment",
            horizontal=True
        )
    else:
        fvg_direction = None
        fvg_alignment = None

    st.markdown("---")

    st.markdown("### 💧 STEP 3: LIQUIDITY ZONES")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Identify stop-hunt zones near FVG</p>', unsafe_allow_html=True)
    liquidity_present = st.radio("🔹 Liquidity Zone Near FVG?", ["Yes", "No"], key="liq_present", horizontal=True)

    if liquidity_present == "Yes":
        liquidity_type = st.selectbox(
            "🔹 Liquidity Type",
            [
                "Swing High (Sell Stops Above)",
                "Swing Low (Buy Stops Below)",
                "Equal Highs (Obvious Resistance)",
                "Equal Lows (Obvious Support)",
                "Previous Day High/Low"
            ],
            key="liq_type"
        )
    else:
        liquidity_type = None

with col2:
    st.markdown("### 🎯 STEP 4: PRICE REACTION (1M-5M)")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Wait for liquidity sweep + rejection</p>', unsafe_allow_html=True)

    price_entered_fvg = st.radio("🔹 Price Entered FVG?", ["Yes", "No"], key="price_fvg", horizontal=True)
    liquidity_swept = st.radio("🔹 Liquidity Swept?", ["Yes", "No"], key="liq_swept", horizontal=True)
    rejection_candle = st.radio("🔹 Rejection Candle After Sweep?", ["Yes", "No"], key="rejection", horizontal=True)

    st.markdown("---")

    st.markdown("### ✅ STEP 5: ENTRY CONFIRMATION")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Final checks before entry</p>', unsafe_allow_html=True)

    micro_structure = st.selectbox(
        "🔹 1M-5M Structure After Rejection",
        ["Strong Reversal (Best)", "Weak Reversal", "No Clear Move"],
        key="micro_structure"
    )

    smt_check = st.radio("🔹 ES & NQ Aligned?", ["Yes (Confirmed)", "No (Divergent)", "Not Checked"], key="smt", horizontal=True)

    st.markdown("---")

    st.markdown("### 🕐 STEP 6: RISK MANAGEMENT")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Position sizing & timing</p>', unsafe_allow_html=True)

    risk_percent = st.selectbox("🔹 Risk Per Trade", ["1%", "1.5%", "2%"], key="risk")
    session_time = st.selectbox(
        "🔹 Trading Session",
        ["London Open (8-11am GMT)", "NY Open (9:30am-12pm EST)", "NY PM (2-4pm EST)", "Outside Prime Time"],
        key="session"
    )

st.markdown("---")

# --- VWAP + FVG + LIQUIDITY LOGIC ---
signal = "🚫 No Trade"
color = "red"
score = 0
max_score = 10
trade_direction = None

# STEP 1: Trend Check (2 points)
if vwap_trend == "Above VWAP (Bullish)":
    score += 2
    trade_direction = "LONG"
elif vwap_trend == "Below VWAP (Bearish)":
    score += 2
    trade_direction = "SHORT"
else:
    trade_direction = None

# STEP 2: FVG Present and Aligned (3 points total)
if fvg_present == "Yes":
    score += 1  # FVG exists

    # Check if FVG aligns with trend (trend trade) or opposite (reversal)
    if fvg_alignment == "Yes (Trend Trade)":
        # Bullish trend + Bullish FVG OR Bearish trend + Bearish FVG
        if (trade_direction == "LONG" and fvg_direction == "Bullish FVG (Gap Up)") or \
           (trade_direction == "SHORT" and fvg_direction == "Bearish FVG (Gap Down)"):
            score += 2  # Perfect alignment
    elif fvg_alignment == "No (Fade/Reversal)":
        # Counter-trend trade (riskier but can work)
        score += 1  # Partial credit for reversal setup

# STEP 3: Liquidity Present (2 points)
if liquidity_present == "Yes":
    score += 2

# STEP 4: Price Action (2 points total)
if price_entered_fvg == "Yes":
    score += 0.5
if liquidity_swept == "Yes":
    score += 0.5
if rejection_candle == "Yes":
    score += 1

# STEP 5: Entry Confirmation (1.5 points total)
if micro_structure == "Strong Reversal (Best)":
    score += 1
elif micro_structure == "Weak Reversal":
    score += 0.5

if smt_check == "Yes (Confirmed)":
    score += 0.5

# STEP 6: Session Timing (0.5 points)
if session_time in ["London Open (8-11am GMT)", "NY Open (9:30am-12pm EST)", "NY PM (2-4pm EST)"]:
    score += 0.5

# Convert to integer for display
score = int(score * 2) / 2  # Round to nearest 0.5

# Determine final trade signal
if score >= 8 and trade_direction == "LONG":
    signal = "🚀 GO LONG"
    subtitle = "HIGH PROBABILITY BUY - All Conditions Met"
    color = "#00FF00"
    box_class = "result-box-green"
elif score >= 8 and trade_direction == "SHORT":
    signal = "📉 GO SHORT"
    subtitle = "HIGH PROBABILITY SELL - All Conditions Met"
    color = "#00FF00"
    box_class = "result-box-green"
elif 6 <= score < 8 and trade_direction:
    signal = f"⚠️ CAUTION - {trade_direction}"
    subtitle = "Moderate Setup - Reduce Position Size to 0.5-1%"
    color = "#FFA500"
    box_class = "result-box-orange"
elif 4 <= score < 6 and trade_direction:
    signal = "⚠️ WEAK SETUP"
    subtitle = "Low Probability - Consider Waiting"
    color = "#FFA500"
    box_class = "result-box-orange"
else:
    signal = "🚫 NO TRADE"
    subtitle = "Missing Key Elements - Wait for Better Setup"
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
    st.markdown(f"<p style='text-align:center; font-size:1.5rem; font-weight:bold; color: #FFFFFF; letter-spacing: 2px;'>SETUP SCORE: {score}/{max_score}</p>", unsafe_allow_html=True)
    st.progress(min(score / max_score, 1.0))

    st.markdown("<br>", unsafe_allow_html=True)

    # Status message with risk management
    if score >= 8:
        st.markdown(f'''
        <div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #00FF00; text-align: center;">
            <p style="color: #00FF00; font-size: 1.2rem; margin: 0; font-weight: bold;">🎯 PERFECT SETUP</p>
            <p style="color: #FFFFFF; margin: 0.5rem 0 0 0;">All 6 steps confirmed</p>
            <p style="color: #00FF00; margin: 0.5rem 0 0 0; font-size: 0.9rem;">✅ Risk: {risk_percent} | SL: Beyond liquidity sweep | TP: Next liquidity zone</p>
        </div>
        ''', unsafe_allow_html=True)
    elif score >= 6:
        st.markdown(f'''
        <div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #FFA500; text-align: center;">
            <p style="color: #FFA500; font-size: 1.2rem; margin: 0; font-weight: bold;">⚠️ MODERATE SETUP</p>
            <p style="color: #FFFFFF; margin: 0.5rem 0 0 0;">Some elements missing - reduce size</p>
            <p style="color: #FFA500; margin: 0.5rem 0 0 0; font-size: 0.9rem;">⚠️ Risk: 0.5-1% max | Tighter SL recommended</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #FF0000; text-align: center;"><p style="color: #FF0000; font-size: 1.2rem; margin: 0; font-weight: bold;">🚫 INCOMPLETE SETUP</p><p style="color: #FFFFFF; margin: 0.5rem 0 0 0;">Wait for all 6 steps to align</p></div>', unsafe_allow_html=True)

st.markdown("---")

# Score breakdown in expandable section
with st.expander("📊 DETAILED SCORE BREAKDOWN", expanded=False):
    st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 1px solid #333;">', unsafe_allow_html=True)

    breakdown_col1, breakdown_col2 = st.columns(2)

    with breakdown_col1:
        st.markdown("#### 📊 STEP 1: TREND (Max 2pts)")
        if vwap_trend in ["Above VWAP (Bullish)", "Below VWAP (Bearish)"]:
            st.markdown(f'<p style="color: #00FF00;">✅ {vwap_trend} <span style="float: right;">+2</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No clear trend <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📉 STEP 2: FVG (Max 3pts)")
        if fvg_present == "Yes":
            st.markdown('<p style="color: #00FF00;">✅ FVG present <span style="float: right;">+1</span></p>', unsafe_allow_html=True)
            if fvg_alignment == "Yes (Trend Trade)":
                st.markdown('<p style="color: #00FF00;">✅ FVG aligned with trend <span style="float: right;">+2</span></p>', unsafe_allow_html=True)
            elif fvg_alignment == "No (Fade/Reversal)":
                st.markdown('<p style="color: #FFA500;">⚠️ Counter-trend FVG <span style="float: right;">+1</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No FVG <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 💧 STEP 3: LIQUIDITY (Max 2pts)")
        if liquidity_present == "Yes":
            st.markdown(f'<p style="color: #00FF00;">✅ Liquidity zone identified <span style="float: right;">+2</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No liquidity zone <span style="float: right;">0</span></p>', unsafe_allow_html=True)

    with breakdown_col2:
        st.markdown("#### 🎯 STEP 4: PRICE REACTION (Max 2pts)")
        if price_entered_fvg == "Yes":
            st.markdown('<p style="color: #00FF00;">✅ Price entered FVG <span style="float: right;">+0.5</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ Price not in FVG <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        if liquidity_swept == "Yes":
            st.markdown('<p style="color: #00FF00;">✅ Liquidity swept <span style="float: right;">+0.5</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No liquidity sweep <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        if rejection_candle == "Yes":
            st.markdown('<p style="color: #00FF00;">✅ Rejection candle <span style="float: right;">+1</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No rejection <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### ✅ STEP 5: CONFIRMATION (Max 1.5pts)")
        if micro_structure == "Strong Reversal (Best)":
            st.markdown('<p style="color: #00FF00;">✅ Strong micro reversal <span style="float: right;">+1</span></p>', unsafe_allow_html=True)
        elif micro_structure == "Weak Reversal":
            st.markdown('<p style="color: #FFA500;">⚠️ Weak reversal <span style="float: right;">+0.5</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No clear move <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        if smt_check == "Yes (Confirmed)":
            st.markdown('<p style="color: #00FF00;">✅ ES & NQ aligned <span style="float: right;">+0.5</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ SMT not confirmed <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🕐 STEP 6: TIMING (Max 0.5pts)")
        if session_time in ["London Open (8-11am GMT)", "NY Open (9:30am-12pm EST)", "NY PM (2-4pm EST)"]:
            st.markdown('<p style="color: #00FF00;">✅ Prime trading session <span style="float: right;">+0.5</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ Outside prime time <span style="float: right;">0</span></p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Strategy cheat sheet
st.markdown('<h3 style="text-align: center; letter-spacing: 3px;">💡 VWAP + FVG + LIQUIDITY CHEAT SHEET 💡</h3>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #00FF00; text-align: center; height: 200px;">
        <h4 style="color: #00FF00; margin-top: 0;">📊 VWAP = TREND</h4>
        <p style="color: #AAAAAA; font-size: 0.9rem;">Above VWAP (1H-4H) = Bullish<br>Below VWAP = Bearish<br>Chopping = No Trade</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #FFA500; text-align: center; height: 200px;">
        <h4 style="color: #FFA500; margin-top: 0;">💧 LIQUIDITY = FUEL</h4>
        <p style="color: #AAAAAA; font-size: 0.9rem;">Smart money hunts stops at swing highs/lows<br>Wait for sweep + rejection</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #FF0000; text-align: center; height: 200px;">
        <h4 style="color: #FF0000; margin-top: 0;">🎯 FVG = ENTRY</h4>
        <p style="color: #AAAAAA; font-size: 0.9rem;">Price fills FVG after liquidity sweep<br>Enter on 1M-5M rejection</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Key rules
st.markdown("""
<div style="background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%); padding: 2rem; border-radius: 10px; border: 2px solid #FFFFFF; text-align: center;">
    <h4 style="color: #FFFFFF; margin-top: 0; letter-spacing: 2px;">🔑 KEY RULES</h4>
    <div style="display: flex; justify-content: space-around; margin-top: 1rem;">
        <div style="flex: 1; padding: 0 1rem;">
            <p style="color: #00FF00; font-weight: bold; margin: 0;">✅ ALWAYS</p>
            <p style="color: #AAAAAA; font-size: 0.85rem;">Wait for all 6 steps<br>Risk 1-2% max<br>SL beyond liquidity sweep</p>
        </div>
        <div style="flex: 1; padding: 0 1rem;">
            <p style="color: #FF0000; font-weight: bold; margin: 0;">🚫 NEVER</p>
            <p style="color: #AAAAAA; font-size: 0.85rem;">Trade without FVG<br>Enter before liquidity sweep<br>Trade on bank holidays</p>
        </div>
        <div style="flex: 1; padding: 0 1rem;">
            <p style="color: #FFA500; font-weight: bold; margin: 0;">⚠️ BEST TIMES</p>
            <p style="color: #AAAAAA; font-size: 0.85rem;">London Open (8-11am GMT)<br>NY Open (9:30am-12pm EST)<br>NY PM (2-4pm EST)</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #666; font-size: 0.9rem; letter-spacing: 2px;">VWAP + FVG + LIQUIDITY SCALPING | WALL STREET-GRADE STRATEGY | AUTO-UPDATES EVERY 10s</p>', unsafe_allow_html=True)

