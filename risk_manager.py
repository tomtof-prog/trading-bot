import logging
from config import RISK_PERCENTAGE, SENTIMENT_THRESHOLD

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self, total_equity: float):
        self.total_equity = total_equity

    def validate_trade(self, sentiment_score: int, ticker: str) -> bool:
        """
        Verifica se l'operazione è valida secondo le regole di sentiment.
        """
        if ticker is None:
            logger.warning("Operazione rifiutata: Ticker mancante.")
            return False

        if sentiment_score > SENTIMENT_THRESHOLD:
            logger.info(f"Sentiment valido per {ticker}: {sentiment_score} > {SENTIMENT_THRESHOLD}")
            return True
        else:
            logger.info(f"Sentiment insufficiente per {ticker}: {sentiment_score} <= {SENTIMENT_THRESHOLD}")
            return False

    def calculate_position_size(self) -> float:
        """
        Calcola l'importo monetario da investire (Position Sizing).
        Non deve superare il 2% del capitale totale.
        """
        position_value = self.total_equity * RISK_PERCENTAGE
        logger.info(f"Capitale totale: ${self.total_equity:.2f} | Rischio: {RISK_PERCENTAGE*100}% | Importo trade: ${position_value:.2f}")
        return position_value

if __name__ == "__main__":
    # Test rapido
    rm = RiskManager(total_equity=100000.0) # Esempio 100k
    score = 85
    ticker = "AAPL"
    
    if rm.validate_trade(score, ticker):
        size = rm.calculate_position_size()
        print(f"Eseguire trade su {ticker} con dimensione ${size}")
    else:
        print("Operazione non valida.")
