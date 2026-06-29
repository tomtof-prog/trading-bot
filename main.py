import time
import logging
from config import LOOP_INTERVAL
from news_collector import NewsCollector
from sentiment_analyzer import SentimentAnalyzer
from risk_manager import RiskManager
from trader_executor import TraderExecutor

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TradingBot")

def main():
    logger.info("Avvio del bot di trading automatico basato sul sentiment...")
    
    try:
        # Inizializzazione moduli
        news_collector = NewsCollector()
        sentiment_analyzer = SentimentAnalyzer()
        trader_executor = TraderExecutor()
        
        # Iniziamo il loop
        while True:
            equity = 0
            try:
                logger.info("--- Inizio ciclo di scansione notizie ---")
                
                # 1. Raccoglie le ultime notizie (ultimi 5 minuti per default)
                news_list = news_collector.get_latest_news(minutes_back=5)
                
                if not news_list:
                    logger.info("Nessuna nuova notizia trovata.")
                else:
                    # Recupera l'equity corrente per il Risk Manager ad ogni ciclo
                    equity = trader_executor.get_account_equity()
                    risk_manager = RiskManager(total_equity=equity)
                    
                    # Teniamo traccia dei ticker già processati in questo ciclo per evitare duplicati
                    processed_tickers = set()

                    for news in news_list:
                        ticker = news.get('ticker')
                        
                        if not ticker:
                            continue

                        if ticker in processed_tickers:
                            continue

                        logger.info(f"Analizzando sentiment per {ticker}...")

                        # 2. Analisi del Sentiment con Gemini
                        sentiment_result = sentiment_analyzer.analyze_sentiment(news['content'])

                        if sentiment_result:
                            logger.info(f"Risultato Gemini per {ticker}: Score={sentiment_result.sentiment_score}, Confidence={sentiment_result.confidence}")
                            
                            # 3. Validazione con Risk Manager
                            if risk_manager.validate_trade(sentiment_result.sentiment_score, ticker):
                                # 4. Esecuzione Trade
                                notional_to_invest = risk_manager.calculate_position_size()

                                logger.info(f"Segnale BUY confermato per {ticker}. Esecuzione ordine...")
                                trader_executor.execute_market_order_with_bracket(ticker, notional_to_invest)

                                processed_tickers.add(ticker)
                            else:
                                logger.info(f"Operazione non valida o sentiment sotto soglia per {ticker}.")
                        else:
                            logger.warning(f"Impossibile analizzare il sentiment per {ticker}.")

                logger.info(f"Ciclo completato. In attesa di {LOOP_INTERVAL} secondi...")
            except Exception as loop_error:
                logger.error(f"Errore durante il ciclo di esecuzione: {loop_error}")
            
            time.sleep(LOOP_INTERVAL)

    except KeyboardInterrupt:
        logger.info("Bot interrotto dall'utente.")
    except Exception as e:
        logger.error(f"Errore critico non gestito: {e}")

if __name__ == "__main__":
    main()
