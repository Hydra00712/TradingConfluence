# 💼 Wall Street Bias Checker

A professional-grade trade confirmation assistant built for multi-timeframe Smart Money trading strategies with real-time market data and news integration.

## 🚀 New Features (v2.0)

### Real-Time Market Data
✅ **Live S&P 500 (ES) prices** - Real-time price, change, and percentage movement
✅ **Live NAS100 (NQ) prices** - Real-time futures data
✅ **Auto SMT Detection** - Automatically detects divergence between ES and NAS
✅ **60-second refresh** - Market data updates every minute

### News Integration
✅ **Futures news feed** - Latest market-moving news for ES and NQ
✅ **Auto-refresh** - News updates every 5 minutes
✅ **Timestamped updates** - Know exactly when news broke

### Enhanced UI/UX
✅ **Wide layout** - Better use of screen space with sidebar
✅ **Professional styling** - Dark theme with gradient accents
✅ **Score breakdown** - Detailed analysis of each confluence factor
✅ **Visual indicators** - Color-coded metrics (green/red for bullish/bearish)
✅ **Responsive design** - Works perfectly on mobile and desktop

### Core Trading Features
✅ Multi-timeframe bias alignment (Daily, 4H, 1H)
✅ Liquidity sweep detection
✅ Displacement & Fair Value Gap (FVG) confirmation
✅ SMT divergence checking (ES vs NAS)
✅ Session timing filters (London, NY AM/PM)
✅ Confluence scoring system (0-12 points)
✅ Clear trade signals: GO LONG, GO SHORT, or NO TRADE

## 🌐 Live Demo

**Access the app anywhere, anytime:**
👉 **[https://tradingconfluence.streamlit.app](https://tradingconfluence.streamlit.app)**

The app is deployed on Streamlit Cloud and accessible 24/7 from any device!

## Quick Start (Local Development)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
streamlit run trade_assistant.py
```

The app will automatically open in your browser at `http://localhost:8502`

### 3. Access from iPhone (Same Wi-Fi)

1. Find your PC's local IP address:
   - Windows: Run `ipconfig` in CMD, look for "IPv4 Address"
   - Example: `192.168.1.100`

2. On your iPhone browser, go to:
   ```
   http://YOUR_PC_IP:8502
   ```
   Example: `http://192.168.1.100:8502`

## How It Works

The app calculates a confluence score based on:

- **Timeframe Alignment** (up to 5 points): Daily, 4H, and 1H bias agreement
- **Liquidity Context** (2 points): Equal highs/lows swept in direction of bias
- **Displacement** (2 points): Strong directional move confirming bias
- **Fair Value Gap** (2 points): FVG formed in direction of bias
- **SMT Confirmation** (1 point): ES & NAS moving in same direction
- **Session Timing** (1 point): Trading during NY session
- **Entry Confirmation** (2 points): Lower timeframe structure shift

### Scoring System

- **10-12 points**: ✅ High probability setup - GO LONG/SHORT
- **7-9 points**: ⚠️ Weak confluence - Trade small or wait
- **0-6 points**: 🚫 No trade - Too many conflicts

## Trading Strategy

This tool is designed for ICT-style Smart Money trading:

1. **Start with higher timeframes**: Identify Daily and 4H bias
2. **Wait for liquidity sweep**: Equal highs (bearish) or equal lows (bullish)
3. **Look for displacement**: Strong move in bias direction
4. **Find the FVG**: Fair value gap to enter on retracement
5. **Check SMT**: Confirm ES and NAS correlation
6. **Time your entry**: Trade during NY session (14:30-21:00 UTC+1)
7. **Confirm on lower TF**: Wait for 1M-5M structure shift or engulfing candle

## Tips

💡 Never trade against higher timeframe bias
💡 Best setups have 10+ confluence points
💡 Always wait for lower timeframe confirmation
💡 Avoid trading outside NY session for best liquidity

---

Built for serious traders who understand market structure, liquidity, and timing.

