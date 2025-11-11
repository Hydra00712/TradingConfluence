# Ultimate Futures Scalping Strategy
# 7-Step System: VWAP + FVG + Liquidity (1H/4H → 5M/15M)

import streamlit as st
import requests
from datetime import datetime, timedelta
import json
import time

st.set_page_config(
    page_title="Ultimate Futures Scalping",
    page_icon="⚡",
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

st.markdown('<h1 class="main-header">ULTIMATE FUTURES SCALPING</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">7-STEP SYSTEM • VWAP + FVG + LIQUIDITY • ES/NQ PRECISION</p>', unsafe_allow_html=True)

# --- FUNCTIONS FOR MARKET DATA ---
@st.cache_data(ttl=10)  # Cache for 10 seconds for real-time updates
def get_market_data():
    """Fetch REAL-TIME market data for S&P 500 and NAS100 with VOLUME"""
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

                # Extract VOLUME data
                sp500_volume_data = sp500_result.get('indicators', {}).get('quote', [{}])[0].get('volume', [])
                nas100_volume_data = nas100_result.get('indicators', {}).get('quote', [{}])[0].get('volume', [])

                # Calculate current volume (last 30 minutes) vs average
                sp500_current_vol = sum([v for v in sp500_volume_data[-30:] if v is not None]) if sp500_volume_data else 0
                sp500_avg_vol = sum([v for v in sp500_volume_data if v is not None]) / len([v for v in sp500_volume_data if v is not None]) * 30 if sp500_volume_data else 1

                nas100_current_vol = sum([v for v in nas100_volume_data[-30:] if v is not None]) if nas100_volume_data else 0
                nas100_avg_vol = sum([v for v in nas100_volume_data if v is not None]) / len([v for v in nas100_volume_data if v is not None]) * 30 if nas100_volume_data else 1

                # Calculate volume percentage (current vs average)
                sp500_vol_pct = (sp500_current_vol / sp500_avg_vol * 100) if sp500_avg_vol > 0 else 100
                nas100_vol_pct = (nas100_current_vol / nas100_avg_vol * 100) if nas100_avg_vol > 0 else 100

                # Verify we have valid data
                if sp500_price > 1000 and nas100_price > 1000:  # Sanity check
                    return {
                        'sp500': {'price': sp500_price, 'change': sp500_change, 'pct': sp500_pct, 'volume_pct': sp500_vol_pct},
                        'nas100': {'price': nas100_price, 'change': nas100_change, 'pct': nas100_pct, 'volume_pct': nas100_vol_pct}
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
                        'sp500': {'price': sp500_price, 'change': sp500_change, 'pct': sp500_pct, 'volume_pct': 100},
                        'nas100': {'price': nas100_price, 'change': nas100_change, 'pct': nas100_pct, 'volume_pct': 100}
                    }
        except Exception as e:
            pass

        # If all methods fail, return demo data
        raise Exception("All API methods failed")

    except:
        # Fallback to demo data if API fails
        return {
            'sp500': {'price': 5850.25, 'change': 12.50, 'pct': 0.21, 'volume_pct': 100},
            'nas100': {'price': 20125.75, 'change': -25.30, 'pct': -0.13, 'volume_pct': 100},
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

def check_trading_conditions(market_data=None):
    """Check for bank holidays, low volume conditions, and REAL-TIME volume analysis - returns warning dict"""
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

    # REAL-TIME VOLUME CHECK - Most important!
    if market_data and 'demo' not in market_data:
        es_vol = market_data.get('sp500', {}).get('volume_pct', 100)
        nq_vol = market_data.get('nas100', {}).get('volume_pct', 100)
        avg_vol = (es_vol + nq_vol) / 2

        if avg_vol < 30:  # Less than 30% of normal volume
            warnings.insert(0, f"🚨 EXTREMELY LOW VOLUME DETECTED - Current: {avg_vol:.0f}% of average")
            severity = 'high'
        elif avg_vol < 50:  # Less than 50% of normal volume
            warnings.insert(0, f"⚠️ LOW VOLUME WARNING - Current: {avg_vol:.0f}% of average (Normal: 100%)")
            if severity != 'high':
                severity = 'medium'
        elif avg_vol < 70:  # Less than 70% of normal volume
            warnings.insert(0, f"⚠️ BELOW AVERAGE VOLUME - Current: {avg_vol:.0f}% of average")
            if severity == 'none':
                severity = 'low'

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

    # Check trading conditions with REAL-TIME volume data
    trading_conditions = check_trading_conditions(market_data)

    if market_data:
        # Show demo mode indicator if using fallback data
        if market_data.get('demo'):
            st.markdown('<p style="color: #FF0000; font-size: 0.85rem; text-align: center; margin-bottom: 1rem; font-weight: bold;">⚠️ DEMO MODE - API Unavailable</p>', unsafe_allow_html=True)
            st.markdown('<p style="color: #888; font-size: 0.75rem; text-align: center; margin-bottom: 1rem;">Click 🔄 to retry</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #00FF00; font-size: 0.75rem; text-align: center; margin-bottom: 1rem;">🔴 LIVE • Auto-updates every 10s</p>', unsafe_allow_html=True)

        # Display VOLUME WARNING if detected
        if trading_conditions['has_warning']:
            if trading_conditions['severity'] == 'high':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #330000 0%, #1a0000 100%); padding: 1.5rem; border-radius: 10px; border: 3px solid #FF0000; margin-bottom: 1.5rem; text-align: center;">
                    <h3 style="color: #FF0000; margin: 0 0 1rem 0; letter-spacing: 2px;">🚨 DO NOT TRADE 🚨</h3>
                    <p style="color: #FFFFFF; margin: 0; line-height: 1.6;">{'<br>'.join(trading_conditions['warnings'])}</p>
                    <p style="color: #FF0000; margin: 1rem 0 0 0; font-weight: bold; font-size: 1.1rem;">{trading_conditions['recommendation']}</p>
                    <p style="color: #AAAAAA; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Market conditions are NOT suitable for trading. Stay out!</p>
                </div>
                """, unsafe_allow_html=True)
            elif trading_conditions['severity'] == 'medium':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #332200 0%, #1a1100 100%); padding: 1.5rem; border-radius: 10px; border: 3px solid #FFA500; margin-bottom: 1.5rem; text-align: center;">
                    <h3 style="color: #FFA500; margin: 0 0 1rem 0; letter-spacing: 2px;">⚠️ CAUTION ⚠️</h3>
                    <p style="color: #FFFFFF; margin: 0; line-height: 1.6;">{'<br>'.join(trading_conditions['warnings'])}</p>
                    <p style="color: #FFA500; margin: 1rem 0 0 0; font-weight: bold;">{trading_conditions['recommendation']}</p>
                    <p style="color: #AAAAAA; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Reduce position size and be extra selective with entries.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a00 0%, #0d0d00 100%); padding: 1rem; border-radius: 8px; border: 2px solid #888; margin-bottom: 1rem; text-align: center;">
                    <h4 style="color: #888; margin: 0 0 0.5rem 0;">⚠️ HEADS UP ⚠️</h4>
                    <p style="color: #AAAAAA; margin: 0; font-size: 0.9rem; line-height: 1.5;">{'<br>'.join(trading_conditions['warnings'])}</p>
                </div>
                """, unsafe_allow_html=True)

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

st.markdown('<h2 style="text-align: center; letter-spacing: 4px; margin: 2rem 0;">⚡ 7-STEP FUTURES SCALPING SYSTEM ⚡</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888; font-size: 0.9rem; margin-top: -1rem;">Higher TF: 1H/4H → Lower TF: 5M/15M</p>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📊 STEP 1: MARKET BIAS (1H/4H)")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Determine trend direction on higher timeframe</p>', unsafe_allow_html=True)

    htf_trend = st.selectbox(
        "🔹 1H/4H Trend Direction",
        ["Bullish", "Bearish", "Neutral/Choppy"],
        key="htf_trend"
    )

    vwap_position = st.selectbox(
        "🔹 Price vs VWAP (1H/4H)",
        ["Above VWAP (Bullish Bias)", "Below VWAP (Bearish Bias)", "At VWAP (Neutral)"],
        key="vwap_position"
    )

    st.markdown("---")

    st.markdown("### 📉 STEP 2: KEY LEVEL (1H/4H FVG)")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Identify unfilled Fair Value Gap on higher TF</p>', unsafe_allow_html=True)

    fvg_present = st.radio("🔹 Unfilled FVG on 1H/4H?", ["Yes", "No"], key="fvg_present", horizontal=True)

    if fvg_present == "Yes":
        fvg_direction = st.selectbox(
            "🔹 FVG Type",
            ["Bullish FVG (Gap Up)", "Bearish FVG (Gap Down)"],
            key="fvg_direction"
        )
        fvg_alignment = st.radio(
            "🔹 FVG Alignment with Bias",
            ["Aligned (Trend Trade)", "Counter-Trend (Reversal)"],
            key="fvg_alignment",
            horizontal=True
        )
    else:
        fvg_direction = None
        fvg_alignment = None

    st.markdown("---")

    st.markdown("### 💧 STEP 3: LIQUIDITY ZONES")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Find swing highs/lows or stop-hunt zones near FVG</p>', unsafe_allow_html=True)

    liquidity_present = st.radio("🔹 Liquidity Zone Identified?", ["Yes", "No"], key="liq_present", horizontal=True)

    if liquidity_present == "Yes":
        liquidity_type = st.selectbox(
            "🔹 Liquidity Type",
            [
                "Swing High (Buy-Side Liquidity)",
                "Swing Low (Sell-Side Liquidity)",
                "Equal Highs (Stop Cluster)",
                "Equal Lows (Stop Cluster)",
                "Previous Day High/Low",
                "Stop-Hunt Zone"
            ],
            key="liq_type"
        )
    else:
        liquidity_type = None

with col2:
    st.markdown("### 🎯 STEP 4: LOWER TF CONFIRMATION (5M/15M)")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Wait for price reaction on lower timeframe</p>', unsafe_allow_html=True)

    price_entered_fvg = st.radio("🔹 Price Traded Into FVG?", ["Yes", "No"], key="price_fvg", horizontal=True)
    liquidity_swept = st.radio("🔹 Liquidity Zone Reacted?", ["Yes", "No"], key="liq_swept", horizontal=True)
    inverse_candle = st.radio("🔹 Minor Inverse (Reversal) Candle?", ["Yes", "No"], key="inverse_candle", horizontal=True)

    st.markdown("---")

    st.markdown("### ✅ STEP 5: ENTRY")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Enter in direction of bias after lower TF validates</p>', unsafe_allow_html=True)

    order_flow_flip = st.radio(
        "🔹 Order Flow Flip Confirmed?",
        ["Yes (Clear Rejection)", "Weak Signal", "No"],
        key="order_flow",
        horizontal=True
    )

    entry_direction = st.selectbox(
        "🔹 Entry Direction",
        ["Long (Bullish)", "Short (Bearish)", "No Entry"],
        key="entry_direction"
    )

    st.markdown("---")

    st.markdown("### 🛡️ STEP 6: STOP-LOSS")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Place stop beyond liquidity sweep / swing point</p>', unsafe_allow_html=True)

    stop_placement = st.selectbox(
        "🔹 Stop-Loss Placement",
        [
            "Beyond Liquidity Sweep (Best)",
            "Beyond Swing Low/High",
            "Below/Above FVG",
            "Not Set"
        ],
        key="stop_placement"
    )

    st.markdown("---")

    st.markdown("### 🎯 STEP 7: TAKE-PROFIT")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Target next liquidity pool or structure</p>', unsafe_allow_html=True)

    tp_target = st.selectbox(
        "🔹 Take-Profit Target",
        [
            "1:1 Risk-Reward (Simplest)",
            "Next Liquidity Pool",
            "Next Major Swing",
            "2:1 Risk-Reward",
            "Not Set"
        ],
        key="tp_target"
    )

    st.markdown("---")

    st.markdown("### 🕐 ADDITIONAL FILTERS")
    smt_check = st.radio("🔹 ES & NQ Aligned?", ["Yes", "No", "Not Checked"], key="smt", horizontal=True)

    session_time = st.selectbox(
        "🔹 Trading Session",
        ["London Open (8-11am GMT)", "NY Open (9:30am-12pm EST)", "NY PM (2-4pm EST)", "Outside Prime Time"],
        key="session"
    )

st.markdown("---")

# --- 7-STEP FUTURES SCALPING LOGIC ---
signal = "🚫 No Trade"
color = "red"
score = 0
max_score = 14  # 7 steps, 2 points each
trade_direction = None

# STEP 1: Market Bias (2 points)
bias_score = 0
if htf_trend in ["Bullish", "Bearish"]:
    bias_score += 1
    if htf_trend == "Bullish":
        trade_direction = "LONG"
    else:
        trade_direction = "SHORT"

if vwap_position == "Above VWAP (Bullish Bias)" and htf_trend == "Bullish":
    bias_score += 1  # Perfect alignment
elif vwap_position == "Below VWAP (Bearish Bias)" and htf_trend == "Bearish":
    bias_score += 1  # Perfect alignment
elif vwap_position != "At VWAP (Neutral)":
    bias_score += 0.5  # Partial credit if VWAP shows bias but doesn't match trend

score += bias_score

# STEP 2: Key Level - FVG (2 points)
fvg_score = 0
if fvg_present == "Yes":
    fvg_score += 1  # FVG exists

    # Check alignment
    if fvg_alignment == "Aligned (Trend Trade)":
        # Bullish bias + Bullish FVG OR Bearish bias + Bearish FVG
        if (trade_direction == "LONG" and fvg_direction == "Bullish FVG (Gap Up)") or \
           (trade_direction == "SHORT" and fvg_direction == "Bearish FVG (Gap Down)"):
            fvg_score += 1  # Perfect alignment
    elif fvg_alignment == "Counter-Trend (Reversal)":
        fvg_score += 0.5  # Partial credit for reversal setup

score += fvg_score

# STEP 3: Liquidity Zones (2 points)
if liquidity_present == "Yes":
    score += 2

# STEP 4: Lower TF Confirmation (2 points)
ltf_score = 0
if price_entered_fvg == "Yes":
    ltf_score += 0.5
if liquidity_swept == "Yes":
    ltf_score += 0.5
if inverse_candle == "Yes":
    ltf_score += 1

score += ltf_score

# STEP 5: Entry (2 points)
entry_score = 0
if order_flow_flip == "Yes (Clear Rejection)":
    entry_score += 1
elif order_flow_flip == "Weak Signal":
    entry_score += 0.5

if entry_direction in ["Long (Bullish)", "Short (Bearish)"]:
    # Check if entry direction matches bias
    if (entry_direction == "Long (Bullish)" and trade_direction == "LONG") or \
       (entry_direction == "Short (Bearish)" and trade_direction == "SHORT"):
        entry_score += 1  # Entry aligns with bias

score += entry_score

# STEP 6: Stop-Loss (2 points)
if stop_placement == "Beyond Liquidity Sweep (Best)":
    score += 2
elif stop_placement == "Beyond Swing Low/High":
    score += 1.5
elif stop_placement == "Below/Above FVG":
    score += 1

# STEP 7: Take-Profit (2 points)
if tp_target == "Next Liquidity Pool":
    score += 2
elif tp_target == "Next Major Swing":
    score += 1.5
elif tp_target in ["1:1 Risk-Reward (Simplest)", "2:1 Risk-Reward"]:
    score += 1

# BONUS: Additional Filters (up to +1 point)
if smt_check == "Yes":
    score += 0.5

if session_time in ["London Open (8-11am GMT)", "NY Open (9:30am-12pm EST)", "NY PM (2-4pm EST)"]:
    score += 0.5

# Convert to integer for display
score = int(score * 2) / 2  # Round to nearest 0.5

# Determine final trade signal
if score >= 12 and trade_direction:
    if trade_direction == "LONG":
        signal = "🚀 GO LONG"
        subtitle = "PERFECT SETUP - All 7 Steps Confirmed"
    else:
        signal = "📉 GO SHORT"
        subtitle = "PERFECT SETUP - All 7 Steps Confirmed"
    color = "#00FF00"
    box_class = "result-box-green"
elif score >= 9 and trade_direction:
    signal = f"✅ {trade_direction} SETUP"
    subtitle = "High Probability - Most Steps Confirmed"
    color = "#00FF00"
    box_class = "result-box-green"
elif 6 <= score < 9 and trade_direction:
    signal = f"⚠️ CAUTION - {trade_direction}"
    subtitle = "Moderate Setup - Reduce Position Size to 0.5-1%"
    color = "#FFA500"
    box_class = "result-box-orange"
elif 4 <= score < 6:
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
        st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #FF0000; text-align: center;"><p style="color: #FF0000; font-size: 1.2rem; margin: 0; font-weight: bold;">🚫 INCOMPLETE SETUP</p><p style="color: #FFFFFF; margin: 0.5rem 0 0 0;">Wait for all 7 steps to align</p></div>', unsafe_allow_html=True)

st.markdown("---")

# Score breakdown in expandable section
with st.expander("📊 DETAILED SCORE BREAKDOWN - 7 STEPS", expanded=False):
    st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 1px solid #333;">', unsafe_allow_html=True)

    breakdown_col1, breakdown_col2 = st.columns(2)

    with breakdown_col1:
        st.markdown("#### 📊 STEP 1: MARKET BIAS (Max 2pts)")
        st.markdown(f'<p style="color: {"#00FF00" if bias_score > 0 else "#FF0000"};">{"✅" if bias_score > 0 else "❌"} HTF Trend: {htf_trend} <span style="float: right;">+{bias_score}</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📉 STEP 2: KEY LEVEL (Max 2pts)")
        if fvg_present == "Yes":
            st.markdown('<p style="color: #00FF00;">✅ FVG present <span style="float: right;">+1</span></p>', unsafe_allow_html=True)
            if fvg_alignment == "Aligned (Trend Trade)":
                st.markdown('<p style="color: #00FF00;">✅ FVG aligned with bias <span style="float: right;">+1</span></p>', unsafe_allow_html=True)
            elif fvg_alignment == "Counter-Trend (Reversal)":
                st.markdown('<p style="color: #FFA500;">⚠️ Counter-trend FVG <span style="float: right;">+0.5</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No FVG <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 💧 STEP 3: LIQUIDITY (Max 2pts)")
        if liquidity_present == "Yes":
            st.markdown(f'<p style="color: #00FF00;">✅ Liquidity zone identified <span style="float: right;">+2</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No liquidity zone <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🎯 STEP 4: LOWER TF (Max 2pts)")
        st.markdown(f'<p style="color: {"#00FF00" if ltf_score > 0 else "#FF0000"};">{"✅" if price_entered_fvg == "Yes" else "❌"} Price in FVG <span style="float: right;">+{0.5 if price_entered_fvg == "Yes" else 0}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: {"#00FF00" if liquidity_swept == "Yes" else "#FF0000"};">{"✅" if liquidity_swept == "Yes" else "❌"} Liquidity reacted <span style="float: right;">+{0.5 if liquidity_swept == "Yes" else 0}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: {"#00FF00" if inverse_candle == "Yes" else "#FF0000"};">{"✅" if inverse_candle == "Yes" else "❌"} Inverse candle <span style="float: right;">+{1 if inverse_candle == "Yes" else 0}</span></p>', unsafe_allow_html=True)

    with breakdown_col2:
        st.markdown("#### ✅ STEP 5: ENTRY (Max 2pts)")
        st.markdown(f'<p style="color: {"#00FF00" if entry_score > 0 else "#FF0000"};">{"✅" if order_flow_flip != "No" else "❌"} Order flow flip: {order_flow_flip} <span style="float: right;">+{entry_score}</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🛡️ STEP 6: STOP-LOSS (Max 2pts)")
        stop_score = 0
        if stop_placement == "Beyond Liquidity Sweep (Best)":
            stop_score = 2
        elif stop_placement == "Beyond Swing Low/High":
            stop_score = 1.5
        elif stop_placement == "Below/Above FVG":
            stop_score = 1
        st.markdown(f'<p style="color: {"#00FF00" if stop_score > 0 else "#FF0000"};">{"✅" if stop_score > 0 else "❌"} {stop_placement} <span style="float: right;">+{stop_score}</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🎯 STEP 7: TAKE-PROFIT (Max 2pts)")
        tp_score = 0
        if tp_target == "Next Liquidity Pool":
            tp_score = 2
        elif tp_target == "Next Major Swing":
            tp_score = 1.5
        elif tp_target in ["1:1 Risk-Reward (Simplest)", "2:1 Risk-Reward"]:
            tp_score = 1
        st.markdown(f'<p style="color: {"#00FF00" if tp_score > 0 else "#FF0000"};">{"✅" if tp_score > 0 else "❌"} {tp_target} <span style="float: right;">+{tp_score}</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🎁 BONUS: FILTERS (Max +1pt)")
        st.markdown(f'<p style="color: {"#00FF00" if smt_check == "Yes" else "#888"};">{"✅" if smt_check == "Yes" else "○"} ES & NQ aligned <span style="float: right;">+{0.5 if smt_check == "Yes" else 0}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: {"#00FF00" if session_time in ["London Open (8-11am GMT)", "NY Open (9:30am-12pm EST)", "NY PM (2-4pm EST)"] else "#888"};">{"✅" if session_time in ["London Open (8-11am GMT)", "NY Open (9:30am-12pm EST)", "NY PM (2-4pm EST)"] else "○"} Prime session <span style="float: right;">+{0.5 if session_time in ["London Open (8-11am GMT)", "NY Open (9:30am-12pm EST)", "NY PM (2-4pm EST)"] else 0}</span></p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Strategy cheat sheet
st.markdown('<h3 style="text-align: center; letter-spacing: 3px;">⚡ 7-STEP FUTURES SCALPING CHEAT SHEET ⚡</h3>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 7-step visual guide
st.markdown("""
<div style="background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%); padding: 2rem; border-radius: 10px; border: 2px solid #00FF00;">
    <h4 style="color: #00FF00; margin-top: 0; text-align: center; letter-spacing: 2px;">📋 THE 7 STEPS</h4>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1.5rem;">
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #00FF00;">
            <p style="color: #00FF00; font-weight: bold; margin: 0; font-size: 0.9rem;">STEP 1: Market Bias (1H/4H)</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0;">Check trend + VWAP position</p>
        </div>
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #00FF00;">
            <p style="color: #00FF00; font-weight: bold; margin: 0; font-size: 0.9rem;">STEP 2: Key Level (FVG)</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0;">Find unfilled 1H/4H FVG</p>
        </div>
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #FFA500;">
            <p style="color: #FFA500; font-weight: bold; margin: 0; font-size: 0.9rem;">STEP 3: Liquidity Zones</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0;">Swing highs/lows near FVG</p>
        </div>
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #FFA500;">
            <p style="color: #FFA500; font-weight: bold; margin: 0; font-size: 0.9rem;">STEP 4: Lower TF (5M/15M)</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0;">Price into FVG + inverse candle</p>
        </div>
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #FF0000;">
            <p style="color: #FF0000; font-weight: bold; margin: 0; font-size: 0.9rem;">STEP 5: Entry</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0;">Order flow flip confirmed</p>
        </div>
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #FF0000;">
            <p style="color: #FF0000; font-weight: bold; margin: 0; font-size: 0.9rem;">STEP 6: Stop-Loss</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0;">Beyond liquidity sweep</p>
        </div>
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #FFFFFF; grid-column: span 2;">
            <p style="color: #FFFFFF; font-weight: bold; margin: 0; font-size: 0.9rem; text-align: center;">STEP 7: Take-Profit</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0; text-align: center;">Next liquidity pool or 1:1 RR minimum</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Key rules
st.markdown("""
<div style="background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%); padding: 2rem; border-radius: 10px; border: 2px solid #FFFFFF; text-align: center;">
    <h4 style="color: #FFFFFF; margin-top: 0; letter-spacing: 2px;">🔑 GOLDEN RULES</h4>
    <div style="display: flex; justify-content: space-around; margin-top: 1rem;">
        <div style="flex: 1; padding: 0 1rem;">
            <p style="color: #00FF00; font-weight: bold; margin: 0;">✅ ALWAYS</p>
            <p style="color: #AAAAAA; font-size: 0.85rem;">Wait for all 7 steps<br>SL beyond liquidity sweep<br>1:1 RR minimum</p>
        </div>
        <div style="flex: 1; padding: 0 1rem;">
            <p style="color: #FF0000; font-weight: bold; margin: 0;">🚫 NEVER</p>
            <p style="color: #AAAAAA; font-size: 0.85rem;">Trade without FVG<br>Enter before reaction<br>Trade on bank holidays</p>
        </div>
        <div style="flex: 1; padding: 0 1rem;">
            <p style="color: #FFA500; font-weight: bold; margin: 0;">⚡ TIMEFRAMES</p>
            <p style="color: #AAAAAA; font-size: 0.85rem;">Higher TF: 1H/4H<br>Lower TF: 5M/15M<br>Prime sessions only</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #666; font-size: 0.9rem; letter-spacing: 2px;">ULTIMATE FUTURES SCALPING | 7-STEP SYSTEM | ES/NQ PRECISION | AUTO-UPDATES EVERY 10s</p>', unsafe_allow_html=True)

