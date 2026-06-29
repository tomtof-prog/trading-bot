from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
from datetime import datetime, timedelta, timezone
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self):
        # Inizializza il client delle news di Alpaca
        try:
            self.client = NewsClient(api_key=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY)
            logger.info("NewsClient inizializzato con successo.")
        except Exception as e:
            logger.error(f"Errore durante l'inizializzazione di NewsClient: {e}")
            raise

    def get_latest_news(self, minutes_back=5):
        """
        Raccoglie le ultime notizie finanziarie.
        """
        try:
            # Calcola l'intervallo di tempo per la ricerca
            now = datetime.now(timezone.utc)
            start_time = now - timedelta(minutes=minutes_back)

            # Crea la richiesta per le news
            # Non specifichiamo simboli per ottenere un feed generale, 
            # limitiamo a 10 notizie per volta per il loop
            request_params = NewsRequest(
                start=start_time,
                end=now,
                limit=10
            )

            # Esegue la richiesta
            news_response = self.client.get_news(request_params)
            
            processed_news = []
            # news_response.data restituisce un dizionario la cui chiave 'news' contiene la lista degli articoli
            for news in news_response.data.get('news', []):
                # Estraiamo le informazioni rilevanti
                # news.symbols contiene la lista dei ticker associati
                # news.headline e news.summary per il contenuto
                
                content = f"{news.headline}. {news.summary}"
                
                # Se ci sono simboli associati, prendiamo il primo per semplicità
                # o restituiamo l'intera lista se preferito. Il requisito chiede il ticker.
                ticker = news.symbols[0] if news.symbols else None
                
                processed_news.append({
                    "ticker": ticker,
                    "headline": news.headline,
                    "summary": news.summary,
                    "content": content,
                    "url": news.url,
                    "timestamp": news.created_at
                })
                
            logger.info(f"Raccolte {len(processed_news)} notizie negli ultimi {minutes_back} minuti.")
            return processed_news

        except Exception as e:
            logger.error(f"Errore durante la raccolta delle notizie: {e}")
            return []

if __name__ == "__main__":
    # Test rapido del modulo
    collector = NewsCollector()
    news = collector.get_latest_news(60) # Ultime 1 ora per il test
    for n in news:
        print(f"Ticker: {n['ticker']} - Headline: {n['headline']}")
