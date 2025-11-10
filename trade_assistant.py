# Trade Confirmation Assistant – "Wall Street Bias Checker"
# Made for Adam's Smart Money Strategy (Multi-TF, Liquidity, Displacement, FVG, SMT)

import streamlit as st

st.set_page_config(page_title="Wall Street Bias Checker", page_icon="💼", layout="centered")

st.title("💼 Wall Street Bias Checker")
st.subheader("Find confluence, avoid fakeouts, and trade like a pro")

st.markdown("---")

# --- INPUTS ---
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

st.markdown("---")

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
st.markdown(f"### 📈 Result:")
st.markdown(f"<h2 style='color:{color}; text-align:center;'>{signal}</h2>", unsafe_allow_html=True)
st.progress(min(score / 12, 1.0))
st.caption(f"Confluence Score: {score}/12")

st.markdown("---")
st.info("💡 Tip: Align Daily + 4H + 1H structure first. Trade only during NY session after displacement + FVG retrace. Confirm entry with 1M–5M reversal candle or BOS.")

