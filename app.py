import pandas as pd
from controllers.binance_ctrl import BinanceController

def test_controller():
    print("--- Iniciando Test del Controlador de Binance ---")
    
    try:
        # 1. Instanciamos el controlador
        # Esto usará automáticamente tu .env y binance_private.pem
        broker = BinanceController()
        print("✅ Controlador inicializado correctamente.")

        # 2. Probamos el balance
        balance = broker.get_balance()
        print(f"📊 Balance obtenido: {balance}")

        # 3. Probamos la descarga de histórico (El estándar)
        print("⏳ Descargando datos históricos para test...")
        df = broker.get_historical_data(symbol='BTC/USDT', timeframe='1h', limit=10)
        
        # 4. Validación del estándar
        columnas_esperadas = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        if list(df.columns) == columnas_esperadas:
            print("✅ ¡Test de Estandarización PASADO! El DataFrame tiene el formato correcto.")
        else:
            print(f"❌ Error: El formato no coincide. Columnas actuales: {list(df.columns)}")
            
        print("\n--- Vista previa de los datos ---")
        print(df.head())

    except Exception as e:
        print(f"❌ El test falló: {e}")

if __name__ == "__main__":
    test_controller()