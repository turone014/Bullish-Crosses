#1HR Bullish


import ccxt
import pandas as pd
import pytz
from datetime import datetime
import requests
from ta.momentum import RSIIndicator
from ta.trend import MACD

# ========== CONFIGURATION ==========
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1377517181239296051/NhzrWKPqbOovOLqS6Cb3bnYdbynWldwFARZckuTJQQODT-Z_SngbN6hnT3QjgC8Kd0bK'

# Custom OKX USDT-margined Futures symbols
symbols = [
    'BTC-USDT-SWAP', 'ETH-USDT-SWAP', 'BTC-USD-SWAP', 'SOL-USDT-SWAP', 'ETH-USD-SWAP', 'DOGE-USDT-SWAP', 'XRP-USDT-SWAP', 'SUI-USDT-SWAP', 'PEPE-USDT-SWAP', 'LTC-USDT-SWAP', 'TRUMP-USDT-SWAP', 'DOGE-USD-SWAP', 'ADA-USDT-SWAP', 'SOL-USD-SWAP', 'BTC-USDC-SWAP', 'BNB-USDT-SWAP', 'AVAX-USDT-SWAP', 'AAVE-USDT-SWAP', 'BCH-USDT-SWAP', 'TON-USDT-SWAP', 'FIL-USDT-SWAP', 'LINK-USDT-SWAP', 'WLD-USDT-SWAP', 'UNI-USDT-SWAP', 'HYPE-USDT-SWAP', 'TRX-USDT-SWAP', 'WCT-USDT-SWAP', 'ETH-USDC-SWAP', 'XRP-USD-SWAP', 'ONDO-USDT-SWAP', 'OP-USDT-SWAP', 'MOODENG-USDT-SWAP', 'WIF-USDT-SWAP', 'FARTCOIN-USDT-SWAP', 'DOT-USDT-SWAP', 'ETC-USDT-SWAP', 'LTC-USD-SWAP', 'SHIB-USDT-SWAP', 'KAITO-USDT-SWAP', 'ALCH-USDT-SWAP', 'CRV-USDT-SWAP', 'TRB-USDT-SWAP', 'PI-USDT-SWAP', 'LDO-USDT-SWAP', 'PNUT-USDT-SWAP', 'PEOPLE-USDT-SWAP', 'ORDI-USDT-SWAP', 'FIL-USD-SWAP', 'NEAR-USDT-SWAP', 'APT-USDT-SWAP', 'ARB-USDT-SWAP', 'JUP-USDT-SWAP', 'TIA-USDT-SWAP', 'ETHFI-USDT-SWAP', 'MASK-USDT-SWAP', 'HBAR-USDT-SWAP', 'INJ-USDT-SWAP', 'XAUT-USDT-SWAP', 'ATH-USDT-SWAP', 'POL-USDT-SWAP', 'XLM-USDT-SWAP', 'ATOM-USDT-SWAP', 'SATS-USDT-SWAP', 'ADA-USD-SWAP', 'VIRTUAL-USDT-SWAP', 'CORE-USDT-SWAP', 'VINE-USDT-SWAP', 'IP-USDT-SWAP', 'LAYER-USDT-SWAP', 'BONK-USDT-SWAP', 'OM-USDT-SWAP', 'ETC-USD-SWAP', 'DYDX-USDT-SWAP', 'S-USDT-SWAP', 'SAND-USDT-SWAP', 'CFX-USDT-SWAP', 'NEIRO-USDT-SWAP', 'MKR-USDT-SWAP', 'ALGO-USDT-SWAP', 'LINK-USD-SWAP', 'GALA-USDT-SWAP', 'DOT-USD-SWAP', 'AIXBT-USDT-SWAP', 'CETUS-USDT-SWAP', 'PYTH-USDT-SWAP', 'GOAT-USDT-SWAP', 'NOT-USDT-SWAP', 'UNI-USD-SWAP', 'ACT-USDT-SWAP', 'JTO-USDT-SWAP', 'MERL-USDT-SWAP', 'BSV-USDT-SWAP', 'AI16Z-USDT-SWAP', 'MOVE-USDT-SWAP', 'ENS-USDT-SWAP', 'RENDER-USDT-SWAP', 'PENGU-USDT-SWAP', 'BERA-USDT-SWAP', 'SUSHI-USDT-SWAP', 'PROMPT-USDT-SWAP', 'FLM-USDT-SWAP', 'NEIROETH-USDT-SWAP', 'AUCTION-USDT-SWAP', 'HUMA-USDT-SWAP', 'ICP-USDT-SWAP', 'STRK-USDT-SWAP', 'POPCAT-USDT-SWAP', 'APE-USDT-SWAP', 'BOME-USDT-SWAP', 'IMX-USDT-SWAP', 'YGG-USDT-SWAP', 'TAO-USDT-SWAP', 'BABY-USDT-SWAP', 'TURBO-USDT-SWAP', 'RAY-USDT-SWAP', 'ZRO-USDT-SWAP', 'LPT-USDT-SWAP', 'MEW-USDT-SWAP', 'MEME-USDT-SWAP', 'LUNC-USDT-SWAP', 'AR-USDT-SWAP', 'UXLINK-USDT-SWAP', 'THETA-USDT-SWAP', 'SONIC-USDT-SWAP', 'ACH-USDT-SWAP', 'FLOKI-USDT-SWAP', 'STX-USDT-SWAP', 'SSV-USDT-SWAP', 'PARTI-USDT-SWAP', 'ANIME-USDT-SWAP', 'AXS-USDT-SWAP', 'JELLYJELLY-USDT-SWAP', 'BIGTIME-USDT-SWAP', 'X-USDT-SWAP', 'CRO-USDT-SWAP', 'INIT-USDT-SWAP', 'XTZ-USDT-SWAP', 'DOGS-USDT-SWAP', 'SOON-USDT-SWAP', 'COOKIE-USDT-SWAP', 'IOTA-USDT-SWAP', 'CATI-USDT-SWAP', 'ZEREBRO-USDT-SWAP', 'EIGEN-USDT-SWAP', 'MAGIC-USDT-SWAP', 'AVAX-USD-SWAP', 'CHZ-USDT-SWAP', 'ZETA-USDT-SWAP', 'W-USDT-SWAP', 'BCH-USD-SWAP', 'ETHW-USDT-SWAP', 'GRT-USDT-SWAP', 'CVC-USDT-SWAP', 'OL-USDT-SWAP', 'NEO-USDT-SWAP', 'ME-USDT-SWAP', 'YFI-USDT-SWAP', 'DUCK-USDT-SWAP', 'COMP-USDT-SWAP', 'BLUR-USDT-SWAP', 'DOOD-USDT-SWAP', 'ARKM-USDT-SWAP', 'DOG-USDT-SWAP', 'GRASS-USDT-SWAP', 'MANA-USDT-SWAP', 'LOOKS-USDT-SWAP', 'TRX-USD-SWAP', 'DEGEN-USDT-SWAP', 'API3-USDT-SWAP', 'ZIL-USDT-SWAP', 'ARC-USDT-SWAP', 'GMT-USDT-SWAP', 'STORJ-USDT-SWAP', 'NC-USDT-SWAP', 'RSR-USDT-SWAP', 'METIS-USDT-SWAP', 'FLOW-USDT-SWAP', 'QTUM-USDT-SWAP', 'ZRX-USDT-SWAP', 'SNX-USDT-SWAP', 'NIL-USDT-SWAP', '1INCH-USDT-SWAP', 'BIO-USDT-SWAP', 'AEVO-USDT-SWAP', 'PRCL-USDT-SWAP', 'USTC-USDT-SWAP', 'AIDOGE-USDT-SWAP', 'MORPHO-USDT-SWAP', 'CELO-USDT-SWAP', 'FXS-USDT-SWAP', 'VANA-USDT-SWAP', 'MINA-USDT-SWAP', 'HMSTR-USDT-SWAP', 'CSPR-USDT-SWAP', 'AVAAI-USDT-SWAP', 'XCH-USDT-SWAP', 'WOO-USDT-SWAP', 'SHELL-USDT-SWAP', 'EGLD-USDT-SWAP', 'SWARMS-USDT-SWAP', 'GAS-USDT-SWAP', 'MAJOR-USDT-SWAP', 'GRIFFAIN-USDT-SWAP', 'AGLD-USDT-SWAP', 'JST-USDT-SWAP', 'SUI-USD-SWAP', 'ATOM-USD-SWAP', 'J-USDT-SWAP', 'SIGN-USDT-SWAP', 'CVX-USDT-SWAP', 'CAT-USDT-SWAP', 'ALPHA-USDT-SWAP', 'UMA-USDT-SWAP', 'ACE-USDT-SWAP', 'RDNT-USDT-SWAP', 'TNSR-USDT-SWAP', 'GODS-USDT-SWAP', 'BAT-USDT-SWAP', 'XLM-USD-SWAP', 'CTC-USDT-SWAP', 'KSM-USDT-SWAP', 'RVN-USDT-SWAP', 'SLERF-USDT-SWAP', 'ONT-USDT-SWAP', 'BRETT-USDT-SWAP', 'BADGER-USDT-SWAP', 'ALGO-USD-SWAP', 'ONE-USDT-SWAP', 'SCR-USDT-SWAP', 'PIPPIN-USDT-SWAP', 'ICX-USDT-SWAP', 'LQTY-USDT-SWAP', 'T-USDT-SWAP', 'WAL-USDT-SWAP', 'USDC-USDT-SWAP', 'GMX-USDT-SWAP', 'PERP-USDT-SWAP', 'SAND-USD-SWAP', 'LRC-USDT-SWAP', 'IOST-USDT-SWAP', 'GLM-USDT-SWAP', 'BICO-USDT-SWAP', 'ID-USDT-SWAP', 'NMR-USDT-SWAP', 'SWEAT-USDT-SWAP', 'KNC-USDT-SWAP', 'BNT-USDT-SWAP', 'MOVR-USDT-SWAP', 'JOE-USDT-SWAP', 'TON-USD-SWAP', 'WAXP-USDT-SWAP', 'BAL-USDT-SWAP', 'GUN-USDT-SWAP', 'BAND-USDT-SWAP', 'DGB-USDT-SWAP', 'PLUME-USDT-SWAP', 'BR-USDT-SWAP', 'SLP-USDT-SWAP', 'PUFFER-USDT-SWAP', 'ZENT-USDT-SWAP', 'ORBS-USDT-SWAP', 'LSK-USDT-SWAP', 'SWELL-USDT-SWAP', 'ZK-USDT-SWAP', 'SOLV-USDT-SWAP', 'GPS-USDT-SWAP', 'SUNDOG-USDT-SWAP', 'LUNA-USDT-SWAP', 'OP-USD-SWAP', 'ENJ-USDT-SWAP', 'SOPH-USDT-SWAP',
    # Add more pairs if needed
]

rsi_period = 30
macd_fast = 12
macd_slow = 26
macd_signal = 9

timezone = pytz.timezone('Asia/Manila')

# ========== INIT EXCHANGE ==========
okx = ccxt.okx({'enableRateLimit': True})

def get_ohlcv(symbol, timeframe, limit=100):
    try:
        data = okx.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"[ERROR] Fetching {timeframe} data for {symbol}: {e}")
        return None

def add_indicators(df):
    rsi = RSIIndicator(df['close'], window=rsi_period)
    macd = MACD(df['close'], window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)
    df['rsi'] = rsi.rsi()
    df['macd'] = macd.macd()
    df['signal'] = macd.macd_signal()
    return df

def get_latest_macd_cross(df):
    for i in range(len(df) - 2, 0, -1):
        prev_macd = df['macd'].iloc[i]
        prev_signal = df['signal'].iloc[i]
        curr_macd = df['macd'].iloc[i + 1]
        curr_signal = df['signal'].iloc[i + 1]
        
        if pd.notna(prev_macd) and pd.notna(prev_signal):
            if prev_macd < prev_signal and curr_macd > curr_signal:
                return 'bullish'
            elif prev_macd > prev_signal and curr_macd < curr_signal:
                return 'bearish'
    return None

def is_rsi_above_50_or_crossing(df):
    if pd.isna(df['rsi'].iloc[-1]) or pd.isna(df['rsi'].iloc[-2]):
        return False
    return df['rsi'].iloc[-1] > 50 or (df['rsi'].iloc[-2] < 50 and df['rsi'].iloc[-1] > 50)

def send_discord_alert(symbol, message):
    now_manila = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
    content = f"🔔🟢 Bullish Alert \n Symbol: {symbol}\n{message}\n📅 Time: {now_manila}"
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
        print(f"[ALERT SENT] {symbol}")
    except Exception as e:
        print(f"[ERROR] Sending Discord alert for {symbol}: {e}")

# ========== MAIN RUN ==========
for symbol in symbols:
    print(f"\n🔍 Checking {symbol}...")

    # Fetch 1H data & check MACD bullish cross
    df_1h = get_ohlcv(symbol, '1h')
    if df_1h is None:
        continue
    df_1h = add_indicators(df_1h)
    if get_latest_macd_cross(df_1h) != 'bullish':
        print(f"[INFO] No recent bullish MACD cross on 1H for {symbol}")
        continue
    print(f"[✓] 1H Bullish MACD cross confirmed for {symbol}")

    # Fetch 15m data & check RSI and MACD
    df_15m = get_ohlcv(symbol, '15m')
    if df_15m is None:
        continue
    df_15m = add_indicators(df_15m)

    if not is_rsi_above_50_or_crossing(df_15m):
        print(f"[INFO] RSI(30) not above or crossing 50 on 15m for {symbol}")
        continue
    print(f"[✓] 15m RSI(30) condition met for {symbol}")

    if get_latest_macd_cross(df_15m) != 'bearish':
        print(f"[INFO] No recent bearish MACD cross on 15m for {symbol}")
        continue
    print(f"[✓] 15m Bearish MACD cross confirmed for {symbol}")

    # Send Discord alert
    alert_message = (
        
        "=================================="
        "\n"
    )
    send_discord_alert(symbol, alert_message)

#====================================================================================================================
#4HRS Bullish - working

import ccxt
import pandas as pd
import pytz
from datetime import datetime
import requests
from ta.momentum import RSIIndicator
from ta.trend import MACD

# ========== CONFIGURATION ==========
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1377517330610917377/pZJrDnxLnXbf-bGo1G_n9BMwwkV0xOCqXZZc910BRZg6R1KcZRjtJKJXBsajP_HNhxsZ'

# Custom OKX USDT-margined Futures symbols
symbols = [
    'BTC-USDT-SWAP', 'ETH-USDT-SWAP', 'BTC-USD-SWAP', 'SOL-USDT-SWAP', 'ETH-USD-SWAP', 'DOGE-USDT-SWAP', 'XRP-USDT-SWAP', 'SUI-USDT-SWAP', 'PEPE-USDT-SWAP', 'LTC-USDT-SWAP', 'TRUMP-USDT-SWAP', 'DOGE-USD-SWAP', 'ADA-USDT-SWAP', 'SOL-USD-SWAP', 'BTC-USDC-SWAP', 'BNB-USDT-SWAP', 'AVAX-USDT-SWAP', 'AAVE-USDT-SWAP', 'BCH-USDT-SWAP', 'TON-USDT-SWAP', 'FIL-USDT-SWAP', 'LINK-USDT-SWAP', 'WLD-USDT-SWAP', 'UNI-USDT-SWAP', 'HYPE-USDT-SWAP', 'TRX-USDT-SWAP', 'WCT-USDT-SWAP', 'ETH-USDC-SWAP', 'XRP-USD-SWAP', 'ONDO-USDT-SWAP', 'OP-USDT-SWAP', 'MOODENG-USDT-SWAP', 'WIF-USDT-SWAP', 'FARTCOIN-USDT-SWAP', 'DOT-USDT-SWAP', 'ETC-USDT-SWAP', 'LTC-USD-SWAP', 'SHIB-USDT-SWAP', 'KAITO-USDT-SWAP', 'ALCH-USDT-SWAP', 'CRV-USDT-SWAP', 'TRB-USDT-SWAP', 'PI-USDT-SWAP', 'LDO-USDT-SWAP', 'PNUT-USDT-SWAP', 'PEOPLE-USDT-SWAP', 'ORDI-USDT-SWAP', 'FIL-USD-SWAP', 'NEAR-USDT-SWAP', 'APT-USDT-SWAP', 'ARB-USDT-SWAP', 'JUP-USDT-SWAP', 'TIA-USDT-SWAP', 'ETHFI-USDT-SWAP', 'MASK-USDT-SWAP', 'HBAR-USDT-SWAP', 'INJ-USDT-SWAP', 'XAUT-USDT-SWAP', 'ATH-USDT-SWAP', 'POL-USDT-SWAP', 'XLM-USDT-SWAP', 'ATOM-USDT-SWAP', 'SATS-USDT-SWAP', 'ADA-USD-SWAP', 'VIRTUAL-USDT-SWAP', 'CORE-USDT-SWAP', 'VINE-USDT-SWAP', 'IP-USDT-SWAP', 'LAYER-USDT-SWAP', 'BONK-USDT-SWAP', 'OM-USDT-SWAP', 'ETC-USD-SWAP', 'DYDX-USDT-SWAP', 'S-USDT-SWAP', 'SAND-USDT-SWAP', 'CFX-USDT-SWAP', 'NEIRO-USDT-SWAP', 'MKR-USDT-SWAP', 'ALGO-USDT-SWAP', 'LINK-USD-SWAP', 'GALA-USDT-SWAP', 'DOT-USD-SWAP', 'AIXBT-USDT-SWAP', 'CETUS-USDT-SWAP', 'PYTH-USDT-SWAP', 'GOAT-USDT-SWAP', 'NOT-USDT-SWAP', 'UNI-USD-SWAP', 'ACT-USDT-SWAP', 'JTO-USDT-SWAP', 'MERL-USDT-SWAP', 'BSV-USDT-SWAP', 'AI16Z-USDT-SWAP', 'MOVE-USDT-SWAP', 'ENS-USDT-SWAP', 'RENDER-USDT-SWAP', 'PENGU-USDT-SWAP', 'BERA-USDT-SWAP', 'SUSHI-USDT-SWAP', 'PROMPT-USDT-SWAP', 'FLM-USDT-SWAP', 'NEIROETH-USDT-SWAP', 'AUCTION-USDT-SWAP', 'HUMA-USDT-SWAP', 'ICP-USDT-SWAP', 'STRK-USDT-SWAP', 'POPCAT-USDT-SWAP', 'APE-USDT-SWAP', 'BOME-USDT-SWAP', 'IMX-USDT-SWAP', 'YGG-USDT-SWAP', 'TAO-USDT-SWAP', 'BABY-USDT-SWAP', 'TURBO-USDT-SWAP', 'RAY-USDT-SWAP', 'ZRO-USDT-SWAP', 'LPT-USDT-SWAP', 'MEW-USDT-SWAP', 'MEME-USDT-SWAP', 'LUNC-USDT-SWAP', 'AR-USDT-SWAP', 'UXLINK-USDT-SWAP', 'THETA-USDT-SWAP', 'SONIC-USDT-SWAP', 'ACH-USDT-SWAP', 'FLOKI-USDT-SWAP', 'STX-USDT-SWAP', 'SSV-USDT-SWAP', 'PARTI-USDT-SWAP', 'ANIME-USDT-SWAP', 'AXS-USDT-SWAP', 'JELLYJELLY-USDT-SWAP', 'BIGTIME-USDT-SWAP', 'X-USDT-SWAP', 'CRO-USDT-SWAP', 'INIT-USDT-SWAP', 'XTZ-USDT-SWAP', 'DOGS-USDT-SWAP', 'SOON-USDT-SWAP', 'COOKIE-USDT-SWAP', 'IOTA-USDT-SWAP', 'CATI-USDT-SWAP', 'ZEREBRO-USDT-SWAP', 'EIGEN-USDT-SWAP', 'MAGIC-USDT-SWAP', 'AVAX-USD-SWAP', 'CHZ-USDT-SWAP', 'ZETA-USDT-SWAP', 'W-USDT-SWAP', 'BCH-USD-SWAP', 'ETHW-USDT-SWAP', 'GRT-USDT-SWAP', 'CVC-USDT-SWAP', 'OL-USDT-SWAP', 'NEO-USDT-SWAP', 'ME-USDT-SWAP', 'YFI-USDT-SWAP', 'DUCK-USDT-SWAP', 'COMP-USDT-SWAP', 'BLUR-USDT-SWAP', 'DOOD-USDT-SWAP', 'ARKM-USDT-SWAP', 'DOG-USDT-SWAP', 'GRASS-USDT-SWAP', 'MANA-USDT-SWAP', 'LOOKS-USDT-SWAP', 'TRX-USD-SWAP', 'DEGEN-USDT-SWAP', 'API3-USDT-SWAP', 'ZIL-USDT-SWAP', 'ARC-USDT-SWAP', 'GMT-USDT-SWAP', 'STORJ-USDT-SWAP', 'NC-USDT-SWAP', 'RSR-USDT-SWAP', 'METIS-USDT-SWAP', 'FLOW-USDT-SWAP', 'QTUM-USDT-SWAP', 'ZRX-USDT-SWAP', 'SNX-USDT-SWAP', 'NIL-USDT-SWAP', '1INCH-USDT-SWAP', 'BIO-USDT-SWAP', 'AEVO-USDT-SWAP', 'PRCL-USDT-SWAP', 'USTC-USDT-SWAP', 'AIDOGE-USDT-SWAP', 'MORPHO-USDT-SWAP', 'CELO-USDT-SWAP', 'FXS-USDT-SWAP', 'VANA-USDT-SWAP', 'MINA-USDT-SWAP', 'HMSTR-USDT-SWAP', 'CSPR-USDT-SWAP', 'AVAAI-USDT-SWAP', 'XCH-USDT-SWAP', 'WOO-USDT-SWAP', 'SHELL-USDT-SWAP', 'EGLD-USDT-SWAP', 'SWARMS-USDT-SWAP', 'GAS-USDT-SWAP', 'MAJOR-USDT-SWAP', 'GRIFFAIN-USDT-SWAP', 'AGLD-USDT-SWAP', 'JST-USDT-SWAP', 'SUI-USD-SWAP', 'ATOM-USD-SWAP', 'J-USDT-SWAP', 'SIGN-USDT-SWAP', 'CVX-USDT-SWAP', 'CAT-USDT-SWAP', 'ALPHA-USDT-SWAP', 'UMA-USDT-SWAP', 'ACE-USDT-SWAP', 'RDNT-USDT-SWAP', 'TNSR-USDT-SWAP', 'GODS-USDT-SWAP', 'BAT-USDT-SWAP', 'XLM-USD-SWAP', 'CTC-USDT-SWAP', 'KSM-USDT-SWAP', 'RVN-USDT-SWAP', 'SLERF-USDT-SWAP', 'ONT-USDT-SWAP', 'BRETT-USDT-SWAP', 'BADGER-USDT-SWAP', 'ALGO-USD-SWAP', 'ONE-USDT-SWAP', 'SCR-USDT-SWAP', 'PIPPIN-USDT-SWAP', 'ICX-USDT-SWAP', 'LQTY-USDT-SWAP', 'T-USDT-SWAP', 'WAL-USDT-SWAP', 'USDC-USDT-SWAP', 'GMX-USDT-SWAP', 'PERP-USDT-SWAP', 'SAND-USD-SWAP', 'LRC-USDT-SWAP', 'IOST-USDT-SWAP', 'GLM-USDT-SWAP', 'BICO-USDT-SWAP', 'ID-USDT-SWAP', 'NMR-USDT-SWAP', 'SWEAT-USDT-SWAP', 'KNC-USDT-SWAP', 'BNT-USDT-SWAP', 'MOVR-USDT-SWAP', 'JOE-USDT-SWAP', 'TON-USD-SWAP', 'WAXP-USDT-SWAP', 'BAL-USDT-SWAP', 'GUN-USDT-SWAP', 'BAND-USDT-SWAP', 'DGB-USDT-SWAP', 'PLUME-USDT-SWAP', 'BR-USDT-SWAP', 'SLP-USDT-SWAP', 'PUFFER-USDT-SWAP', 'ZENT-USDT-SWAP', 'ORBS-USDT-SWAP', 'LSK-USDT-SWAP', 'SWELL-USDT-SWAP', 'ZK-USDT-SWAP', 'SOLV-USDT-SWAP', 'GPS-USDT-SWAP', 'SUNDOG-USDT-SWAP', 'LUNA-USDT-SWAP', 'OP-USD-SWAP', 'ENJ-USDT-SWAP', 'SOPH-USDT-SWAP',
    # Add more symbols as needed
]

rsi_period = 30
macd_fast = 12
macd_slow = 26
macd_signal = 9

timezone = pytz.timezone('Asia/Manila')

# ========== INIT EXCHANGE ==========
okx = ccxt.okx({'enableRateLimit': True})

def get_ohlcv(symbol, timeframe, limit=100):
    try:
        data = okx.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"[ERROR] Fetching {timeframe} data for {symbol}: {e}")
        return None

def add_indicators(df):
    rsi = RSIIndicator(df['close'], window=rsi_period)
    macd = MACD(df['close'], window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)
    df['rsi'] = rsi.rsi()
    df['macd'] = macd.macd()
    df['signal'] = macd.macd_signal()
    return df

def get_latest_macd_cross(df):
    for i in range(len(df) - 2, 0, -1):
        prev_macd = df['macd'].iloc[i]
        prev_signal = df['signal'].iloc[i]
        curr_macd = df['macd'].iloc[i + 1]
        curr_signal = df['signal'].iloc[i + 1]
        if pd.notna(prev_macd) and pd.notna(prev_signal):
            if prev_macd < prev_signal and curr_macd > curr_signal:
                return 'bullish'
            elif prev_macd > prev_signal and curr_macd < curr_signal:
                return 'bearish'
    return None

def is_rsi_above_50_or_crossing(df):
    if pd.isna(df['rsi'].iloc[-1]) or pd.isna(df['rsi'].iloc[-2]):
        return False
    return df['rsi'].iloc[-1] > 50 or (df['rsi'].iloc[-2] < 50 and df['rsi'].iloc[-1] > 50)

def send_discord_alert(symbol, message):
    now_manila = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
    content = f"🔔🟢 Bullish Alert \n Symbol: {symbol}\n{message}\n📅 Time: {now_manila}"
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
        print(f"[ALERT SENT] {symbol}")
    except Exception as e:
        print(f"[ERROR] Sending Discord alert for {symbol}: {e}")

# ========== MAIN RUN ==========
for symbol in symbols:
    print(f"\n🔍 Checking {symbol}...")

    # Fetch 4H data & check MACD bullish cross
    df_4h = get_ohlcv(symbol, '4h')
    if df_4h is None:
        continue
    df_4h = add_indicators(df_4h)
    if get_latest_macd_cross(df_4h) != 'bullish':
        print(f"[INFO] No recent bullish MACD cross on 4H for {symbol}")
        continue
    print(f"[✓] 4H Bullish MACD cross confirmed for {symbol}")

    # Fetch 1H data
    df_1h = get_ohlcv(symbol, '1h')
    if df_1h is None:
        continue
    df_1h = add_indicators(df_1h)

    if not is_rsi_above_50_or_crossing(df_1h):
        print(f"[INFO] RSI(30) not above or crossing 50 on 1H for {symbol}")
        continue
    print(f"[✓] 1H RSI(30) condition met for {symbol}")

    if get_latest_macd_cross(df_1h) != 'bearish':
        print(f"[INFO] No recent bearish MACD cross on 1H for {symbol}")
        continue
    print(f"[✓] 1H Bearish MACD cross confirmed for {symbol}")

    # Send Discord alert
    alert_message = (
        "=================================="
        "\n"
    )
    send_discord_alert(symbol, alert_message)


#=============================================================================================

#1Day Bullish

import ccxt
import pandas as pd
import pytz
import requests
from datetime import datetime
from ta.momentum import RSIIndicator
from ta.trend import MACD

# ========== CONFIG ==========
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1377517417072169062/WDWC4YG8n8OG58G0SDVoYJ2ARFgsQD4MHPmv-aN1xWp_K4EXaWbd3lwkCTPUuenc_H9H'  # Replace this

symbols = [
    'BTC-USDT-SWAP', 'ETH-USDT-SWAP', 'BTC-USD-SWAP', 'SOL-USDT-SWAP', 'ETH-USD-SWAP', 'DOGE-USDT-SWAP', 'XRP-USDT-SWAP', 'SUI-USDT-SWAP', 'PEPE-USDT-SWAP', 'LTC-USDT-SWAP', 'TRUMP-USDT-SWAP', 'DOGE-USD-SWAP', 'ADA-USDT-SWAP', 'SOL-USD-SWAP', 'BTC-USDC-SWAP', 'BNB-USDT-SWAP', 'AVAX-USDT-SWAP', 'AAVE-USDT-SWAP', 'BCH-USDT-SWAP', 'TON-USDT-SWAP', 'FIL-USDT-SWAP', 'LINK-USDT-SWAP', 'WLD-USDT-SWAP', 'UNI-USDT-SWAP', 'HYPE-USDT-SWAP', 'TRX-USDT-SWAP', 'WCT-USDT-SWAP', 'ETH-USDC-SWAP', 'XRP-USD-SWAP', 'ONDO-USDT-SWAP', 'OP-USDT-SWAP', 'MOODENG-USDT-SWAP', 'WIF-USDT-SWAP', 'FARTCOIN-USDT-SWAP', 'DOT-USDT-SWAP', 'ETC-USDT-SWAP', 'LTC-USD-SWAP', 'SHIB-USDT-SWAP', 'KAITO-USDT-SWAP', 'ALCH-USDT-SWAP', 'CRV-USDT-SWAP', 'TRB-USDT-SWAP', 'PI-USDT-SWAP', 'LDO-USDT-SWAP', 'PNUT-USDT-SWAP', 'PEOPLE-USDT-SWAP', 'ORDI-USDT-SWAP', 'FIL-USD-SWAP', 'NEAR-USDT-SWAP', 'APT-USDT-SWAP', 'ARB-USDT-SWAP', 'JUP-USDT-SWAP', 'TIA-USDT-SWAP', 'ETHFI-USDT-SWAP', 'MASK-USDT-SWAP', 'HBAR-USDT-SWAP', 'INJ-USDT-SWAP', 'XAUT-USDT-SWAP', 'ATH-USDT-SWAP', 'POL-USDT-SWAP', 'XLM-USDT-SWAP', 'ATOM-USDT-SWAP', 'SATS-USDT-SWAP', 'ADA-USD-SWAP', 'VIRTUAL-USDT-SWAP', 'CORE-USDT-SWAP', 'VINE-USDT-SWAP', 'IP-USDT-SWAP', 'LAYER-USDT-SWAP', 'BONK-USDT-SWAP', 'OM-USDT-SWAP', 'ETC-USD-SWAP', 'DYDX-USDT-SWAP', 'S-USDT-SWAP', 'SAND-USDT-SWAP', 'CFX-USDT-SWAP', 'NEIRO-USDT-SWAP', 'MKR-USDT-SWAP', 'ALGO-USDT-SWAP', 'LINK-USD-SWAP', 'GALA-USDT-SWAP', 'DOT-USD-SWAP', 'AIXBT-USDT-SWAP', 'CETUS-USDT-SWAP', 'PYTH-USDT-SWAP', 'GOAT-USDT-SWAP', 'NOT-USDT-SWAP', 'UNI-USD-SWAP', 'ACT-USDT-SWAP', 'JTO-USDT-SWAP', 'MERL-USDT-SWAP', 'BSV-USDT-SWAP', 'AI16Z-USDT-SWAP', 'MOVE-USDT-SWAP', 'ENS-USDT-SWAP', 'RENDER-USDT-SWAP', 'PENGU-USDT-SWAP', 'BERA-USDT-SWAP', 'SUSHI-USDT-SWAP', 'PROMPT-USDT-SWAP', 'FLM-USDT-SWAP', 'NEIROETH-USDT-SWAP', 'AUCTION-USDT-SWAP', 'HUMA-USDT-SWAP', 'ICP-USDT-SWAP', 'STRK-USDT-SWAP', 'POPCAT-USDT-SWAP', 'APE-USDT-SWAP', 'BOME-USDT-SWAP', 'IMX-USDT-SWAP', 'YGG-USDT-SWAP', 'TAO-USDT-SWAP', 'BABY-USDT-SWAP', 'TURBO-USDT-SWAP', 'RAY-USDT-SWAP', 'ZRO-USDT-SWAP', 'LPT-USDT-SWAP', 'MEW-USDT-SWAP', 'MEME-USDT-SWAP', 'LUNC-USDT-SWAP', 'AR-USDT-SWAP', 'UXLINK-USDT-SWAP', 'THETA-USDT-SWAP', 'SONIC-USDT-SWAP', 'ACH-USDT-SWAP', 'FLOKI-USDT-SWAP', 'STX-USDT-SWAP', 'SSV-USDT-SWAP', 'PARTI-USDT-SWAP', 'ANIME-USDT-SWAP', 'AXS-USDT-SWAP', 'JELLYJELLY-USDT-SWAP', 'BIGTIME-USDT-SWAP', 'X-USDT-SWAP', 'CRO-USDT-SWAP', 'INIT-USDT-SWAP', 'XTZ-USDT-SWAP', 'DOGS-USDT-SWAP', 'SOON-USDT-SWAP', 'COOKIE-USDT-SWAP', 'IOTA-USDT-SWAP', 'CATI-USDT-SWAP', 'ZEREBRO-USDT-SWAP', 'EIGEN-USDT-SWAP', 'MAGIC-USDT-SWAP', 'AVAX-USD-SWAP', 'CHZ-USDT-SWAP', 'ZETA-USDT-SWAP', 'W-USDT-SWAP', 'BCH-USD-SWAP', 'ETHW-USDT-SWAP', 'GRT-USDT-SWAP', 'CVC-USDT-SWAP', 'OL-USDT-SWAP', 'NEO-USDT-SWAP', 'ME-USDT-SWAP', 'YFI-USDT-SWAP', 'DUCK-USDT-SWAP', 'COMP-USDT-SWAP', 'BLUR-USDT-SWAP', 'DOOD-USDT-SWAP', 'ARKM-USDT-SWAP', 'DOG-USDT-SWAP', 'GRASS-USDT-SWAP', 'MANA-USDT-SWAP', 'LOOKS-USDT-SWAP', 'TRX-USD-SWAP', 'DEGEN-USDT-SWAP', 'API3-USDT-SWAP', 'ZIL-USDT-SWAP', 'ARC-USDT-SWAP', 'GMT-USDT-SWAP', 'STORJ-USDT-SWAP', 'NC-USDT-SWAP', 'RSR-USDT-SWAP', 'METIS-USDT-SWAP', 'FLOW-USDT-SWAP', 'QTUM-USDT-SWAP', 'ZRX-USDT-SWAP', 'SNX-USDT-SWAP', 'NIL-USDT-SWAP', '1INCH-USDT-SWAP', 'BIO-USDT-SWAP', 'AEVO-USDT-SWAP', 'PRCL-USDT-SWAP', 'USTC-USDT-SWAP', 'AIDOGE-USDT-SWAP', 'MORPHO-USDT-SWAP', 'CELO-USDT-SWAP', 'FXS-USDT-SWAP', 'VANA-USDT-SWAP', 'MINA-USDT-SWAP', 'HMSTR-USDT-SWAP', 'CSPR-USDT-SWAP', 'AVAAI-USDT-SWAP', 'XCH-USDT-SWAP', 'WOO-USDT-SWAP', 'SHELL-USDT-SWAP', 'EGLD-USDT-SWAP', 'SWARMS-USDT-SWAP', 'GAS-USDT-SWAP', 'MAJOR-USDT-SWAP', 'GRIFFAIN-USDT-SWAP', 'AGLD-USDT-SWAP', 'JST-USDT-SWAP', 'SUI-USD-SWAP', 'ATOM-USD-SWAP', 'J-USDT-SWAP', 'SIGN-USDT-SWAP', 'CVX-USDT-SWAP', 'CAT-USDT-SWAP', 'ALPHA-USDT-SWAP', 'UMA-USDT-SWAP', 'ACE-USDT-SWAP', 'RDNT-USDT-SWAP', 'TNSR-USDT-SWAP', 'GODS-USDT-SWAP', 'BAT-USDT-SWAP', 'XLM-USD-SWAP', 'CTC-USDT-SWAP', 'KSM-USDT-SWAP', 'RVN-USDT-SWAP', 'SLERF-USDT-SWAP', 'ONT-USDT-SWAP', 'BRETT-USDT-SWAP', 'BADGER-USDT-SWAP', 'ALGO-USD-SWAP', 'ONE-USDT-SWAP', 'SCR-USDT-SWAP', 'PIPPIN-USDT-SWAP', 'ICX-USDT-SWAP', 'LQTY-USDT-SWAP', 'T-USDT-SWAP', 'WAL-USDT-SWAP', 'USDC-USDT-SWAP', 'GMX-USDT-SWAP', 'PERP-USDT-SWAP', 'SAND-USD-SWAP', 'LRC-USDT-SWAP', 'IOST-USDT-SWAP', 'GLM-USDT-SWAP', 'BICO-USDT-SWAP', 'ID-USDT-SWAP', 'NMR-USDT-SWAP', 'SWEAT-USDT-SWAP', 'KNC-USDT-SWAP', 'BNT-USDT-SWAP', 'MOVR-USDT-SWAP', 'JOE-USDT-SWAP', 'TON-USD-SWAP', 'WAXP-USDT-SWAP', 'BAL-USDT-SWAP', 'GUN-USDT-SWAP', 'BAND-USDT-SWAP', 'DGB-USDT-SWAP', 'PLUME-USDT-SWAP', 'BR-USDT-SWAP', 'SLP-USDT-SWAP', 'PUFFER-USDT-SWAP', 'ZENT-USDT-SWAP', 'ORBS-USDT-SWAP', 'LSK-USDT-SWAP', 'SWELL-USDT-SWAP', 'ZK-USDT-SWAP', 'SOLV-USDT-SWAP', 'GPS-USDT-SWAP', 'SUNDOG-USDT-SWAP', 'LUNA-USDT-SWAP', 'OP-USD-SWAP', 'ENJ-USDT-SWAP', 'SOPH-USDT-SWAP',
    # Add more as needed
]

macd_fast = 12
macd_slow = 26
macd_signal = 9
rsi_period = 30

timezone = pytz.timezone('Asia/Manila')
okx = ccxt.okx({'enableRateLimit': True})

# ========== FUNCTIONS ==========

def get_ohlcv(symbol, timeframe, limit=100):
    try:
        ohlcv = okx.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"[ERROR] Fetching {timeframe} data for {symbol}: {e}")
        return None

def add_indicators(df):
    rsi = RSIIndicator(df['close'], window=rsi_period)
    macd = MACD(df['close'], window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)
    df['rsi'] = rsi.rsi()
    df['macd'] = macd.macd()
    df['signal'] = macd.macd_signal()
    return df

def get_latest_macd_cross(df):
    for i in range(len(df) - 2, 0, -1):
        prev_macd = df['macd'].iloc[i]
        prev_signal = df['signal'].iloc[i]
        curr_macd = df['macd'].iloc[i + 1]
        curr_signal = df['signal'].iloc[i + 1]
        if pd.notna(prev_macd) and pd.notna(prev_signal):
            if prev_macd < prev_signal and curr_macd > curr_signal:
                return 'bullish'
            elif prev_macd > prev_signal and curr_macd < curr_signal:
                return 'bearish'
    return None

def is_rsi_above_50_or_crossing(df):
    if pd.isna(df['rsi'].iloc[-1]) or pd.isna(df['rsi'].iloc[-2]):
        return False
    return df['rsi'].iloc[-1] > 50 or (df['rsi'].iloc[-2] < 50 and df['rsi'].iloc[-1] > 50)

def send_discord_alert(symbol, message):
    now_manila = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
    content = f"🔔🟢 Bullish Alert \n Symbol: {symbol}\n{message}\n📅 Time: {now_manila}"
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
        print(f"[ALERT SENT] {symbol}")
    except Exception as e:
        print(f"[ERROR] Sending Discord alert: {e}")

# ========== MAIN ==========
for symbol in symbols:
    print(f"\n🔍 Checking {symbol}...")

    # 1D MACD Bullish Cross
    df_1d = get_ohlcv(symbol, '1d')
    if df_1d is None:
        continue
    df_1d = add_indicators(df_1d)
    if get_latest_macd_cross(df_1d) != 'bullish':
        print(f"[INFO] No bullish MACD cross on 1D for {symbol}")
        continue
    print(f"[✓] 1D MACD Bullish cross detected for {symbol}")

    # 4H RSI > 50 or crossed
    df_4h = get_ohlcv(symbol, '4h')
    if df_4h is None:
        continue
    df_4h = add_indicators(df_4h)
    if not is_rsi_above_50_or_crossing(df_4h):
        print(f"[INFO] RSI(30) not above or crossing 50 on 4H for {symbol}")
        continue
    print(f"[✓] 4H RSI(30) > 50 or crossing confirmed for {symbol}")

    # 4H MACD Bearish Cross
    if get_latest_macd_cross(df_4h) != 'bearish':
        print(f"[INFO] No bearish MACD cross on 4H for {symbol}")
        continue
    print(f"[✓] 4H MACD Bearish cross detected for {symbol}")

    # All conditions met - Send alert
    alert_message = (
        "=================================="
        "\n"
    )
    send_discord_alert(symbol, alert_message)

#============================================================================================





