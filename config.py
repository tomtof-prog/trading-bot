import os

# Configurazione API Keys (da impostare come variabili d'ambiente)
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "your_api_key_here")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "your_secret_key_here")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_key_here")

# Parametri Alpaca
# Utilizziamo l'endpoint di Paper Trading per default
ALPACA_PAPER_URL = "https://paper-api.alpaca.markets"

# Parametri Strategia
RISK_PERCENTAGE = 0.02  # Massimo 2% del capitale per operazione
SENTIMENT_THRESHOLD = 80  # Soglia minima di sentiment per entrare in posizione
CONFIDENCE_THRESHOLD = 70 # Soglia minima di confidenza dell'analisi

# Parametri Modello AI
GEMINI_MODEL_NAME = "gemini-2.0-flash"

# Intervallo del loop principale (in secondi)
LOOP_INTERVAL = 300  # 5 minuti
