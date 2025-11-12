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

        # VOLUME ANALYSIS DISPLAY
        st.markdown("---")
        st.markdown("### 📊 VOLUME ANALYSIS")

        es_vol_pct = market_data['sp500'].get('volume_pct', 100)
        nq_vol_pct = market_data['nas100'].get('volume_pct', 100)
        avg_vol_pct = (es_vol_pct + nq_vol_pct) / 2

        # Determine volume status and color
        if avg_vol_pct >= 100:
            vol_status = "HIGH VOLUME"
            vol_color = "#00FF00"
            vol_icon = "🔥"
            vol_message = "Excellent trading conditions"
        elif avg_vol_pct >= 70:
            vol_status = "NORMAL VOLUME"
            vol_color = "#00FF00"
            vol_icon = "✅"
            vol_message = "Good trading conditions"
        elif avg_vol_pct >= 50:
            vol_status = "BELOW AVERAGE"
            vol_color = "#FFA500"
            vol_icon = "⚠️"
            vol_message = "Be cautious - reduced liquidity"
        elif avg_vol_pct >= 30:
            vol_status = "LOW VOLUME"
            vol_color = "#FF0000"
            vol_icon = "🚨"
            vol_message = "Trade with extreme caution"
        else:
            vol_status = "VERY LOW VOLUME"
            vol_color = "#FF0000"
            vol_icon = "🛑"
            vol_message = "DO NOT TRADE"

        st.markdown(f"""
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid {vol_color};">
            <p style="color: {vol_color}; font-weight: bold; margin: 0; font-size: 1.1rem;">{vol_icon} {vol_status}</p>
            <p style="color: #FFFFFF; margin: 0.5rem 0 0 0; font-size: 1.2rem; font-weight: bold;">{avg_vol_pct:.0f}% of Average</p>
            <p style="color: #AAAAAA; margin: 0.5rem 0 0 0; font-size: 0.85rem;">ES: {es_vol_pct:.0f}% • NQ: {nq_vol_pct:.0f}%</p>
            <p style="color: {vol_color}; margin: 0.5rem 0 0 0; font-size: 0.9rem;">{vol_message}</p>
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

st.markdown('<h2 style="text-align: center; letter-spacing: 4px; margin: 2rem 0;">⚡ VWAP + SMT + LIQUIDITY SCALPING ⚡</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888; font-size: 0.9rem; margin-top: -1rem;">Bias: 15m → Confirmation: 5m → Entry: 1-2m</p>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 🧭 STEP 1: FIND BIAS (15m Chart)")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Check VWAP direction + SMT divergence</p>', unsafe_allow_html=True)

    vwap_slope = st.selectbox(
        "🔹 VWAP Direction (15m)",
        ["Sloping Up (Bullish)", "Sloping Down (Bearish)", "Flat (Ranging)"],
        key="vwap_slope"
    )

    smt_divergence = st.selectbox(
        "🔹 SMT Divergence",
        [
            "Bullish SMT (NQ lower low, ES higher low)",
            "Bearish SMT (NQ higher high, ES lower high)",
            "No Divergence",
            "Not Checked"
        ],
        key="smt_div"
    )

    st.markdown("---")

    st.markdown("### 💧 STEP 2: MARK LIQUIDITY (15m/5m)")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Identify recent swing high/low for stop hunt</p>', unsafe_allow_html=True)

    liquidity_marked = st.radio("🔹 Liquidity Zone Marked?", ["Yes", "No"], key="liq_marked", horizontal=True)

    if liquidity_marked == "Yes":
        liquidity_type = st.selectbox(
            "🔹 Liquidity Type",
            [
                "Above Recent High (Buy-Side)",
                "Below Recent Low (Sell-Side)",
                "Equal Highs",
                "Equal Lows"
            ],
            key="liq_type"
        )
    else:
        liquidity_type = None

    st.markdown("---")

    st.markdown("### ⚡ STEP 3: WAIT FOR SWEEP + BOS (5m)")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Liquidity sweep + Break of Structure</p>', unsafe_allow_html=True)

    liquidity_swept = st.radio("🔹 Liquidity Swept?", ["Yes", "No"], key="liq_swept", horizontal=True)

    bos_confirmed = st.radio(
        "🔹 Break of Structure (BOS)?",
        ["Yes (Strong Move Back)", "Weak", "No"],
        key="bos",
        horizontal=True
    )

with col2:
    st.markdown("### 🎯 STEP 4: ENTRY (1-2m Chart)")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Wait for retrace + confirmation candle</p>', unsafe_allow_html=True)

    retrace_level = st.selectbox(
        "🔹 Retrace Level",
        [
            "50-70% of BOS Move",
            "Near VWAP",
            "Into FVG Zone",
            "No Retrace Yet"
        ],
        key="retrace"
    )

    confirmation_candle = st.radio(
        "🔹 Confirmation Candle?",
        ["Yes (Engulfing/Rejection)", "Weak", "No"],
        key="confirm_candle",
        horizontal=True
    )

    entry_direction = st.selectbox(
        "🔹 Entry Direction",
        ["Long", "Short", "No Entry"],
        key="entry_dir"
    )

    st.markdown("---")

    st.markdown("### 🛡️ STOP-LOSS & TAKE-PROFIT")
    st.markdown('<p style="color: #888; font-size: 0.85rem; margin-top: -0.5rem;">Risk management</p>', unsafe_allow_html=True)

    stop_placement = st.selectbox(
        "🔹 Stop-Loss Placement",
        [
            "Below Sweep Low (Longs)",
            "Above Sweep High (Shorts)",
            "Not Set"
        ],
        key="stop_placement"
    )

    tp_target = st.selectbox(
        "🔹 Take-Profit Target",
        [
            "TP1: Back to VWAP",
            "TP1: VWAP, TP2: Next Liquidity",
            "Next Liquidity Level (15m)",
            "Not Set"
        ],
        key="tp_target"
    )

    st.markdown("---")

    st.markdown("### 🕐 SESSION & FILTERS")

    session_time = st.selectbox(
        "🔹 Trading Session",
        ["NY Session (9:30 AM - 12:00 PM EST)", "Outside NY Session"],
        key="session"
    )

    news_check = st.radio("🔹 Avoid News Candles?", ["Yes", "No"], key="news_check", horizontal=True)

st.markdown("---")

# --- VWAP + SMT + LIQUIDITY SCALPING LOGIC ---
signal = "🚫 No Trade"
color = "red"
score = 0
max_score = 10  # 5 steps, 2 points each
trade_direction = None

# STEP 1: Find Bias (2 points)
bias_score = 0

# VWAP slope determines bias
if vwap_slope == "Sloping Up (Bullish)":
    bias_score += 1
    trade_direction = "LONG"
elif vwap_slope == "Sloping Down (Bearish)":
    bias_score += 1
    trade_direction = "SHORT"

# SMT divergence confirms bias
if smt_divergence == "Bullish SMT (NQ lower low, ES higher low)" and trade_direction == "LONG":
    bias_score += 1  # Perfect alignment
elif smt_divergence == "Bearish SMT (NQ higher high, ES lower high)" and trade_direction == "SHORT":
    bias_score += 1  # Perfect alignment
elif smt_divergence != "Not Checked" and smt_divergence != "No Divergence":
    bias_score += 0.5  # Partial credit for divergence even if not aligned

score += bias_score

# STEP 2: Mark Liquidity (2 points)
liquidity_score = 0
if liquidity_marked == "Yes":
    liquidity_score += 2  # Liquidity zone identified

score += liquidity_score

# STEP 3: Wait for Sweep + BOS (2 points)
sweep_bos_score = 0
if liquidity_swept == "Yes":
    sweep_bos_score += 1  # Liquidity swept (stop hunt)

if bos_confirmed == "Yes (Strong Move Back)":
    sweep_bos_score += 1  # Break of structure confirmed
elif bos_confirmed == "Weak":
    sweep_bos_score += 0.5  # Partial credit for weak BOS

score += sweep_bos_score

# STEP 4: Entry (2 points)
entry_score = 0

# Retrace quality
if retrace_level in ["50-70% of BOS Move", "Near VWAP", "Into FVG Zone"]:
    entry_score += 0.5

# Confirmation candle
if confirmation_candle == "Yes (Engulfing/Rejection)":
    entry_score += 1
elif confirmation_candle == "Weak":
    entry_score += 0.5

# Entry direction matches bias
if entry_direction == "Long" and trade_direction == "LONG":
    entry_score += 0.5
elif entry_direction == "Short" and trade_direction == "SHORT":
    entry_score += 0.5

score += entry_score

# STEP 5: Risk Management (2 points)
risk_score = 0

# Stop-loss placement
if stop_placement in ["Below Sweep Low (Longs)", "Above Sweep High (Shorts)"]:
    risk_score += 1

# Take-profit target
if tp_target in ["TP1: VWAP, TP2: Next Liquidity", "Next Liquidity Level (15m)"]:
    risk_score += 1
elif tp_target == "TP1: Back to VWAP":
    risk_score += 0.5

score += risk_score

# BONUS: Session & Filters (up to +1 point)
if session_time == "NY Session (9:30 AM - 12:00 PM EST)":
    score += 0.5

if news_check == "Yes":
    score += 0.5

# Convert to integer for display
score = int(score * 2) / 2  # Round to nearest 0.5

# Determine final trade signal
if score >= 8 and trade_direction:
    if trade_direction == "LONG":
        signal = "🚀 GO LONG"
        subtitle = "PERFECT SETUP - All 5 Steps Confirmed"
    else:
        signal = "📉 GO SHORT"
        subtitle = "PERFECT SETUP - All 5 Steps Confirmed"
    color = "#00FF00"
    box_class = "result-box-green"
elif score >= 6 and trade_direction:
    signal = f"✅ {trade_direction} SETUP"
    subtitle = "High Probability - Most Steps Confirmed"
    color = "#00FF00"
    box_class = "result-box-green"
elif 4 <= score < 6 and trade_direction:
    signal = f"⚠️ CAUTION - {trade_direction}"
    subtitle = "Moderate Setup - Reduce Position Size to 0.5-1%"
    color = "#FFA500"
    box_class = "result-box-orange"
elif 2 <= score < 4:
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
            <p style="color: #FFFFFF; margin: 0.5rem 0 0 0;">All 5 steps confirmed</p>
            <p style="color: #00FF00; margin: 0.5rem 0 0 0; font-size: 0.9rem;">✅ Risk: 1-2% max | SL: Beyond sweep | TP: VWAP or next liquidity</p>
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
        st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 2px solid #FF0000; text-align: center;"><p style="color: #FF0000; font-size: 1.2rem; margin: 0; font-weight: bold;">🚫 INCOMPLETE SETUP</p><p style="color: #FFFFFF; margin: 0.5rem 0 0 0;">Wait for all 5 steps to align</p></div>', unsafe_allow_html=True)

st.markdown("---")

# Score breakdown in expandable section
with st.expander("📊 DETAILED SCORE BREAKDOWN - 5 STEPS", expanded=False):
    st.markdown('<div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; border: 1px solid #333;">', unsafe_allow_html=True)

    breakdown_col1, breakdown_col2 = st.columns(2)

    with breakdown_col1:
        st.markdown("#### 🧭 STEP 1: FIND BIAS (Max 2pts)")
        st.markdown(f'<p style="color: {"#00FF00" if bias_score > 0 else "#FF0000"};">{"✅" if bias_score > 0 else "❌"} VWAP: {vwap_slope} <span style="float: right;">+{bias_score}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: {"#00FF00" if smt_divergence != "Not Checked" and smt_divergence != "No Divergence" else "#888"};">{"✅" if smt_divergence != "Not Checked" and smt_divergence != "No Divergence" else "○"} SMT: {smt_divergence}</p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 💧 STEP 2: MARK LIQUIDITY (Max 2pts)")
        if liquidity_marked == "Yes":
            st.markdown(f'<p style="color: #00FF00;">✅ Liquidity marked: {liquidity_type} <span style="float: right;">+{liquidity_score}</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #FF0000;">❌ No liquidity marked <span style="float: right;">0</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### ⚡ STEP 3: SWEEP + BOS (Max 2pts)")
        st.markdown(f'<p style="color: {"#00FF00" if liquidity_swept == "Yes" else "#FF0000"};">{"✅" if liquidity_swept == "Yes" else "❌"} Liquidity swept <span style="float: right;">+{1 if liquidity_swept == "Yes" else 0}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: {"#00FF00" if bos_confirmed == "Yes (Strong Move Back)" else "#FFA500" if bos_confirmed == "Weak" else "#FF0000"};">{"✅" if bos_confirmed == "Yes (Strong Move Back)" else "⚠️" if bos_confirmed == "Weak" else "❌"} BOS: {bos_confirmed} <span style="float: right;">+{1 if bos_confirmed == "Yes (Strong Move Back)" else 0.5 if bos_confirmed == "Weak" else 0}</span></p>', unsafe_allow_html=True)

    with breakdown_col2:
        st.markdown("#### 🎯 STEP 4: ENTRY (Max 2pts)")
        st.markdown(f'<p style="color: {"#00FF00" if retrace_level != "No Retrace Yet" else "#FF0000"};">{"✅" if retrace_level != "No Retrace Yet" else "❌"} Retrace: {retrace_level} <span style="float: right;">+{0.5 if retrace_level != "No Retrace Yet" else 0}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: {"#00FF00" if confirmation_candle == "Yes (Engulfing/Rejection)" else "#FFA500" if confirmation_candle == "Weak" else "#FF0000"};">{"✅" if confirmation_candle == "Yes (Engulfing/Rejection)" else "⚠️" if confirmation_candle == "Weak" else "❌"} Confirmation: {confirmation_candle} <span style="float: right;">+{1 if confirmation_candle == "Yes (Engulfing/Rejection)" else 0.5 if confirmation_candle == "Weak" else 0}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: {"#00FF00" if entry_direction != "No Entry" else "#FF0000"};">{"✅" if entry_direction != "No Entry" else "❌"} Direction: {entry_direction} <span style="float: right;">+{0.5 if entry_direction != "No Entry" else 0}</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🛡️ STEP 5: RISK MGMT (Max 2pts)")
        risk_stop_score = 1 if stop_placement in ["Below Sweep Low (Longs)", "Above Sweep High (Shorts)"] else 0
        risk_tp_score = 1 if tp_target in ["TP1: VWAP, TP2: Next Liquidity", "Next Liquidity Level (15m)"] else 0.5 if tp_target == "TP1: Back to VWAP" else 0
        st.markdown(f'<p style="color: {"#00FF00" if risk_stop_score > 0 else "#FF0000"};">{"✅" if risk_stop_score > 0 else "❌"} SL: {stop_placement} <span style="float: right;">+{risk_stop_score}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: {"#00FF00" if risk_tp_score > 0 else "#FF0000"};">{"✅" if risk_tp_score > 0 else "❌"} TP: {tp_target} <span style="float: right;">+{risk_tp_score}</span></p>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🎁 BONUS: FILTERS (Max +1pt)")
        st.markdown(f'<p style="color: {"#00FF00" if session_time == "NY Session (9:30 AM - 12:00 PM EST)" else "#888"};">{"✅" if session_time == "NY Session (9:30 AM - 12:00 PM EST)" else "○"} NY Session <span style="float: right;">+{0.5 if session_time == "NY Session (9:30 AM - 12:00 PM EST)" else 0}</span></p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: {"#00FF00" if news_check == "Yes" else "#888"};">{"✅" if news_check == "Yes" else "○"} Avoid news <span style="float: right;">+{0.5 if news_check == "Yes" else 0}</span></p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Strategy cheat sheet
st.markdown('<h3 style="text-align: center; letter-spacing: 3px;">⚡ VWAP + SMT + LIQUIDITY CHEAT SHEET ⚡</h3>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 5-step visual guide
st.markdown("""
<div style="background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%); padding: 2rem; border-radius: 10px; border: 2px solid #00FF00;">
    <h4 style="color: #00FF00; margin-top: 0; text-align: center; letter-spacing: 2px;">📋 THE 5 STEPS</h4>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1.5rem;">
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #00FF00;">
            <p style="color: #00FF00; font-weight: bold; margin: 0; font-size: 0.9rem;">STEP 1: Find Bias (15m)</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0;">VWAP slope + SMT divergence</p>
        </div>
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #00FF00;">
            <p style="color: #00FF00; font-weight: bold; margin: 0; font-size: 0.9rem;">STEP 2: Mark Liquidity (15m/5m)</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0;">Recent swing high/low</p>
        </div>
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #FFA500;">
            <p style="color: #FFA500; font-weight: bold; margin: 0; font-size: 0.9rem;">STEP 3: Sweep + BOS (5m)</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0;">Liquidity sweep + break of structure</p>
        </div>
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #FF0000;">
            <p style="color: #FF0000; font-weight: bold; margin: 0; font-size: 0.9rem;">STEP 4: Entry (1-2m)</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0;">Retrace 50-70% + confirmation candle</p>
        </div>
        <div style="background: #0a0a0a; padding: 1rem; border-radius: 8px; border-left: 4px solid #FFFFFF; grid-column: span 2;">
            <p style="color: #FFFFFF; font-weight: bold; margin: 0; font-size: 0.9rem; text-align: center;">STEP 5: Risk Management</p>
            <p style="color: #AAAAAA; font-size: 0.8rem; margin: 0.5rem 0 0 0; text-align: center;">SL: Beyond sweep | TP: VWAP or next liquidity</p>
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
            <p style="color: #AAAAAA; font-size: 0.85rem;">Wait for liquidity sweep<br>SL beyond sweep<br>Trade NY session only</p>
        </div>
        <div style="flex: 1; padding: 0 1rem;">
            <p style="color: #FF0000; font-weight: bold; margin: 0;">🚫 NEVER</p>
            <p style="color: #AAAAAA; font-size: 0.85rem;">Trade flat VWAP<br>Enter before sweep<br>Trade into news</p>
        </div>
        <div style="flex: 1; padding: 0 1rem;">
            <p style="color: #FFA500; font-weight: bold; margin: 0;">⚡ TIMEFRAMES</p>
            <p style="color: #AAAAAA; font-size: 0.85rem;">Bias: 15m<br>Confirmation: 5m<br>Entry: 1-2m</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #666; font-size: 0.9rem; letter-spacing: 2px;">VWAP + SMT + LIQUIDITY SCALPING | 5-STEP SYSTEM | ES/NQ | NY SESSION | AUTO-UPDATES EVERY 10s</p>', unsafe_allow_html=True)

