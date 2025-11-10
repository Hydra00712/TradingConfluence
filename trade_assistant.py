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

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
    .market-card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .news-card {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
        border-left: 3px solid #ff7f0e;
    }
    .metric-positive {
        color: #00ff00;
        font-weight: bold;
    }
    .metric-negative {
        color: #ff4444;
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ff4444, #ffaa00, #00ff00);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">💼 Wall Street Bias Checker</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Find confluence, avoid fakeouts, and trade like a pro</p>', unsafe_allow_html=True)

# --- FUNCTIONS FOR MARKET DATA ---
@st.cache_data(ttl=60)  # Cache for 1 minute
def get_market_data():
    """Fetch real-time market data for S&P 500 and NAS100"""
    try:
        # Using Yahoo Finance API (free, no key needed)
        sp500_url = "https://query1.finance.yahoo.com/v8/finance/chart/ES%3DF"
        nas100_url = "https://query1.finance.yahoo.com/v8/finance/chart/NQ%3DF"

        sp500_data = requests.get(sp500_url, timeout=5).json()
        nas100_data = requests.get(nas100_url, timeout=5).json()

        # Extract data
        sp500_price = sp500_data['chart']['result'][0]['meta']['regularMarketPrice']
        sp500_prev = sp500_data['chart']['result'][0]['meta']['previousClose']
        sp500_change = sp500_price - sp500_prev
        sp500_pct = (sp500_change / sp500_prev) * 100

        nas100_price = nas100_data['chart']['result'][0]['meta']['regularMarketPrice']
        nas100_prev = nas100_data['chart']['result'][0]['meta']['previousClose']
        nas100_change = nas100_price - nas100_prev
        nas100_pct = (nas100_change / nas100_prev) * 100

        return {
            'sp500': {'price': sp500_price, 'change': sp500_change, 'pct': sp500_pct},
            'nas100': {'price': nas100_price, 'change': nas100_change, 'pct': nas100_pct}
        }
    except:
        return None

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
    st.header("📊 Live Market Data")

    market_data = get_market_data()

    if market_data:
        # S&P 500
        st.markdown('<div class="market-card">', unsafe_allow_html=True)
        st.subheader("S&P 500 (ES)")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Price", f"${market_data['sp500']['price']:.2f}")
        with col2:
            change_class = "metric-positive" if market_data['sp500']['change'] >= 0 else "metric-negative"
            st.markdown(f"<p class='{change_class}' style='font-size:1.2rem;'>{market_data['sp500']['change']:+.2f} ({market_data['sp500']['pct']:+.2f}%)</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # NAS100
        st.markdown('<div class="market-card">', unsafe_allow_html=True)
        st.subheader("NAS100 (NQ)")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Price", f"${market_data['nas100']['price']:.2f}")
        with col2:
            change_class = "metric-positive" if market_data['nas100']['change'] >= 0 else "metric-negative"
            st.markdown(f"<p class='{change_class}' style='font-size:1.2rem;'>{market_data['nas100']['change']:+.2f} ({market_data['nas100']['pct']:+.2f}%)</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # SMT Divergence Auto-Detection
        st.markdown("---")
        st.subheader("🔍 SMT Analysis")
        sp_direction = "Bullish" if market_data['sp500']['change'] > 0 else "Bearish"
        nas_direction = "Bullish" if market_data['nas100']['change'] > 0 else "Bearish"

        if sp_direction == nas_direction:
            st.success(f"✅ Confirmed: Both {sp_direction}")
        else:
            st.warning(f"⚠️ Divergence: ES {sp_direction}, NQ {nas_direction}")
    else:
        st.warning("⚠️ Market data unavailable")

    st.markdown("---")
    st.header("📰 Futures News")

    news = get_futures_news()
    for item in news[:4]:  # Show top 4
        st.markdown(f'<div class="news-card"><strong>{item["title"]}</strong><br><small style="color:#888;">{item["time"]}</small></div>', unsafe_allow_html=True)

    st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# --- MAIN CONTENT: INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.header("📊 1️⃣ Timeframe Biases")
    daily = st.selectbox("Daily Bias", ["Bullish", "Bearish", "Neutral"])
    h4 = st.selectbox("4H Bias", ["Bullish", "Bearish", "Neutral"])
    h1 = st.selectbox("1H Structure", ["Bullish", "Bearish", "Choppy/Neutral"])

    st.markdown("---")

    st.header("📉 2️⃣ Market Context")
    liquidity = st.selectbox("Liquidity recently swept?", ["None", "Equal Highs (Sell Liquidity)", "Equal Lows (Buy Liquidity)"])
    displacement = st.radio("Strong Displacement in Direction of Bias?", ["Yes", "No"])
    fvg = st.radio("Fair Value Gap Formed?", ["Yes", "No"])
    fvg_dir = st.selectbox("FVG Direction", ["Bullish", "Bearish", "None"])

with col2:
    st.header("🔁 3️⃣ Correlation (SMT Check)")
    smt = st.selectbox("SMT Divergence between ES & NAS?", ["Confirmed (Same Direction)", "Divergent", "Not Checked"])

    st.markdown("---")

    st.header("🕓 4️⃣ Execution Filters")
    session = st.selectbox("Trading Session", ["London", "NY AM (14:30–17:00 UTC+1)", "NY PM (19:00–21:00 UTC+1)", "Outside Session"])
    confirmation = st.radio("Lower Timeframe Confirmation (1M–5M structure shift or engulfing)?", ["Yes", "No"])

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
    signal = "✅ GO LONG – High Probability Buy Setup"
    color = "green"
elif score >= 10 and daily == "Bearish":
    signal = "🔻 GO SHORT – High Probability Sell Setup"
    color = "blue"
elif 7 <= score < 10:
    signal = "⚠️ Weak Confluence – Trade Small or Wait for Better Alignment"
    color = "orange"
else:
    signal = "🚫 No Trade – Too Many Conflicts"
    color = "red"

# --- OUTPUT ---
st.markdown("---")

# Create a visually appealing result section
result_col1, result_col2, result_col3 = st.columns([1, 2, 1])

with result_col2:
    st.markdown(f"### 📈 Trade Decision:")
    st.markdown(f"<h2 style='color:{color}; text-align:center; padding: 2rem; background-color: #262730; border-radius: 10px; border: 2px solid {color};'>{signal}</h2>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Progress bar with label
    st.markdown(f"<p style='text-align:center; font-size:1.2rem; font-weight:bold;'>Confluence Score: {score}/12</p>", unsafe_allow_html=True)
    st.progress(min(score / 12, 1.0))

    # Score breakdown
    st.markdown("<br>", unsafe_allow_html=True)

    if score >= 10:
        st.success("🎯 **High Probability Setup** - All systems aligned!")
    elif score >= 7:
        st.warning("⚠️ **Moderate Setup** - Consider smaller position or wait")
    else:
        st.error("🚫 **Low Probability** - Stay out or wait for better confluence")

st.markdown("---")

# Score breakdown in expandable section
with st.expander("📊 See Score Breakdown"):
    breakdown_col1, breakdown_col2 = st.columns(2)

    with breakdown_col1:
        st.markdown("**Timeframe Alignment:**")
        if daily == h4 and daily != "Neutral":
            st.success("✅ Daily & 4H aligned (+3)")
        else:
            st.error("❌ Daily & 4H not aligned (0)")

        if h1 == daily:
            st.success("✅ 1H matches Daily (+2)")
        else:
            st.error("❌ 1H doesn't match (0)")

        st.markdown("**Market Context:**")
        if (liquidity.startswith("Equal Lows") and daily == "Bullish") or (liquidity.startswith("Equal Highs") and daily == "Bearish"):
            st.success("✅ Liquidity swept (+2)")
        else:
            st.error("❌ No liquidity sweep (0)")

        if displacement == "Yes":
            st.success("✅ Displacement confirmed (+2)")
        else:
            st.error("❌ No displacement (0)")

    with breakdown_col2:
        if fvg == "Yes" and fvg_dir == daily:
            st.success("✅ FVG aligned (+2)")
        else:
            st.error("❌ No FVG alignment (0)")

        st.markdown("**Execution Filters:**")
        if smt == "Confirmed (Same Direction)":
            st.success("✅ SMT confirmed (+1)")
        else:
            st.error("❌ SMT not confirmed (0)")

        if session.startswith("NY"):
            st.success("✅ NY session (+1)")
        else:
            st.error("❌ Outside NY session (0)")

        if confirmation == "Yes":
            st.success("✅ Lower TF confirmation (+2)")
        else:
            st.error("❌ No confirmation (0)")

st.markdown("---")

# Tips section with better formatting
st.markdown("### 💡 Pro Trading Tips")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**📊 Structure First**\n\nAlign Daily + 4H + 1H before considering any trade")

with col2:
    st.info("**⏰ Timing Matters**\n\nTrade during NY session (14:30-21:00 UTC+1) for best liquidity")

with col3:
    st.info("**✅ Confirm Entry**\n\nWait for 1M-5M reversal candle or BOS before entering")

# Footer
st.markdown("---")
st.caption("Built for Smart Money traders | Real-time data updates every 60 seconds")

