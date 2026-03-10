import ccxt
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Configuración
api_key = os.getenv('BINANCE_API_KEY')
private_key_path = os.getenv('PRIVATE_KEY_PATH')

with open(private_key_path, 'r') as f:
    private_key_content = f.read()

# Inicialización
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': private_key_content,
    'enableRateLimit': True,
})

def obtener_historico(simbolo='BTC/USDT', temporalidad='1h', limite=500):
    print(f"Descargando {limite} velas de {temporalidad} para {simbolo}...")
    
    # fetch_ohlcv es el método estándar de CCXT
    ohlcv = exchange.fetch_ohlcv(simbolo, timeframe=temporalidad, limit=limite)
    
    # Creamos el DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # Convertimos el timestamp (ms) a fechas legibles
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    return df

# Ejecución
df_btc = obtener_historico(temporalidad='1h', limite=1000)
print(df_btc) # Muestra las primeras 5 filas