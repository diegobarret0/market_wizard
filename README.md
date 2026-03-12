# Market Wizard 🧙

Plataforma de análisis financiero que centraliza datos de múltiples brokers y exchanges para brindar herramientas de análisis estadístico, técnico y fundamental sobre distintos tipos de activos.

## Activos soportados

| Tipo | Ejemplos |
|---|---|
| Criptomonedas | BTC, ETH, y cualquier par disponible en los exchanges conectados |
| Acciones | Mercado local e internacional (vía brokers conectados) |
| Bonos | Soberanos y corporativos |
| Letras | Letras del Tesoro y equivalentes |

## Arquitectura

```
market_wizard/
├── app.py                  # Entry point — Streamlit dashboard
├── controllers/            # Adaptadores de brokers y exchanges
│   └── binance_ctrl.py
├── tools/                  # Herramientas de análisis
│   └── analysis.py
├── ai/                     # Módulos de análisis asistido por IA
├── models/                 # Esquemas y modelos de datos compartidos
├── keys/                   # Claves privadas (gitignoreado)
├── Dockerfile
├── docker-compose.yaml
└── requirements.txt
```

### Controllers

Cada controller encapsula la conexión con un broker o exchange específico. Exponen una interfaz común para que las herramientas de análisis sean agnósticas a la fuente de datos.

**Interfaz estándar que todo controller debe implementar:**

```python
get_historical_data(symbol, timeframe, limit) -> DataFrame
# Columnas: [timestamp, open, high, low, close, volume]

get_balance() -> dict  # {asset: amount}
```

**Fuentes disponibles / planificadas:**

| Controller | Estado | Mercado |
|---|---|---|
| Binance | ✅ Disponible | Cripto |
| IOL (Invertir Online) | 🔜 Planificado | Acciones / Bonos / Letras (ARG) |
| Nexo | 🔜 Planificado | Cripto / Yield |
| Bull Market | 🔜 Planificado | Acciones / Bonos (ARG) |

### Tools

Herramientas de análisis que operan sobre los DataFrames estandarizados que producen los controllers. Se dividen en tres categorías:

- **Análisis técnico** — indicadores de precio y volumen (medias móviles, RSI, MACD, Bollinger Bands, etc.)
- **Análisis estadístico** — volatilidad, correlaciones, distribuciones, backtesting de estrategias
- **Análisis fundamental** — valuación de activos, métricas financieras (requiere fuentes de datos adicionales)

### AI

Módulos que complementan las tools con capacidades de lenguaje natural e interpretación automática:
- Síntesis de señales técnicas en lenguaje natural
- Análisis de sentimiento de noticias y redes sociales
- Generación de reportes automáticos

## Setup

### Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Binance
BINANCE_API_KEY=tu_api_key
PRIVATE_KEY_PATH=keys/binance_api_private.pem

# IOL (cuando esté disponible)
# IOL_USER=...
# IOL_PASSWORD=...
```

> La autenticación con Binance usa clave RSA asimétrica (archivo `.pem`). No usa un `BINANCE_SECRET` de tipo string.

### Instalación local

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Docker

```bash
docker compose up --build
```

La app queda disponible en `http://localhost:8501`.

## Agregar un nuevo controller

1. Crear `controllers/nombre_ctrl.py`
2. Implementar la interfaz estándar (`get_historical_data`, `get_balance`)
3. Normalizar la salida al esquema `[timestamp, open, high, low, close, volume]`
4. Registrar las credenciales necesarias en `.env`
