# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
# Local (Streamlit)
streamlit run app.py --server.port=8501

# Docker
docker compose up --build

# Direct script execution (for testing controllers)
python app.py
```

## Environment Setup

Requires a `.env` file (gitignored) with:
```
BINANCE_API_KEY=your_api_key
PRIVATE_KEY_PATH=keys/binance_api_private.pem
```

Authentication uses RSA asymmetric keys — `PRIVATE_KEY_PATH` points to a PEM file (also gitignored). There is no `BINANCE_SECRET` string variable.

Install dependencies:
```bash
pip install -r requirements.txt
```

## Architecture

This is a Streamlit trading analysis dashboard connected to Binance via the CCXT library.

**Data flow:** `controllers/` fetch raw data from exchanges → normalize to a standard DataFrame format → `tools/` perform analysis on that standard format → Streamlit frontend in `app.py` renders results.

### Key Design Contract

`BinanceController.get_historical_data()` always returns a DataFrame with exactly these columns in this order:
```
[timestamp, open, high, low, close, volume]
```
All analysis tools in `tools/` are written to expect this schema. Never add or rename columns in the controller output.

### Module Roles

- **`controllers/`** — Exchange adapters. Each controller wraps a CCXT exchange, handles authentication, and normalizes raw API responses into the standard DataFrame format. `BinanceController` is the current implementation.
- **`tools/analysis.py`** — Analysis logic (indicators, signals, etc.) that operates on the standardized DataFrames from controllers.
- **`app.py`** — Streamlit entry point. Wires controllers and tools together for the UI.

### Adding a New Exchange

Create a new file in `controllers/` that implements at minimum:
- `get_historical_data(symbol, timeframe, limit)` → standardized DataFrame
- `get_balance()` → dict of `{asset: amount}` for non-zero balances
