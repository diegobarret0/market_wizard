import ccxt
import pandas as pd
import os
from dotenv import load_dotenv

class BinanceController:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.private_key_path = os.getenv('PRIVATE_KEY_PATH')
        self.exchange = self._authenticate()

    def _authenticate(self):
        """Método privado para gestionar la conexión"""
        try:
            with open(self.private_key_path, 'r') as f:
                p_key_content = f.read()
            
            return ccxt.binance({
                'apiKey': self.api_key,
                'secret': p_key_content,
                'enableRateLimit': True,
                # 'options': {'defaultType': 'spot'} # Puedes cambiar a 'future' si lo requieres
            })
        except Exception as e:
            raise Exception(f"Error de autenticación en Binance: {e}")

    def get_historical_data(self, symbol='BTC/USDT', timeframe='1h', limit=500):
        """
        Retorna un DataFrame ESTANDARIZADO para las herramientas de análisis.
        Columnas: [timestamp, open, high, low, close, volume]
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            
            # ESTANDARIZACIÓN: Todas las tools esperan estas columnas
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Formato de datos común
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Aseguramos que los tipos sean correctos para cálculos matemáticos
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
            
            return df
        except Exception as e:
            print(f"Error al obtener datos de Binance: {e}")
            return pd.DataFrame() # Retorna vacío si falla

    def get_balance(self):
        """Retorna balance simplificado"""
        balance = self.exchange.fetch_balance()
        return {k: v for k, v in balance['total'].items() if v > 0}