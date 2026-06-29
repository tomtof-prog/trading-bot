from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional
import json
import logging
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentResult(BaseModel):
    ticker: Optional[str] = Field(description="Il ticker dell'azione (es. AAPL, TSLA, NVDA)")
    sentiment_score: int = Field(description="Un intero da -100 (notizia pessima) a +100 (notizia eccellente)")
    confidence: int = Field(description="Un intero da 0 a 100 che rappresenta la sicurezza del modello")
    reason: str = Field(description="Una breve frase che spiega il motivo del punteggio")

class SentimentAnalyzer:
    def __init__(self):
        try:
            self.client = genai.Client(
                api_key=GEMINI_API_KEY,
                http_options=types.HttpOptions(api_version='v1')
            )
            self.model_name = GEMINI_MODEL_NAME
            logger.info(f"SentimentAnalyzer inizializzato con modello {self.model_name}.")
        except Exception as e:
            logger.error(f"Errore durante l'inizializzazione del client Gemini: {e}")
            raise

    def analyze_sentiment(self, news_text: str) -> Optional[SentimentResult]:
        """
        Invia il testo della notizia a Gemini per l'analisi del sentiment.
        Utilizza Structured Output per garantire una risposta JSON valida.
        """
        prompt = f"""
        Analizza il sentiment della seguente notizia finanziaria e restituisci un oggetto JSON.
        Identifica il ticker principale se presente.
        
        Notizia:
        {news_text}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': SentimentResult,
                }
            )

            # Il modello con response_schema dovrebbe restituire direttamente un oggetto 
            # che segue lo schema, accessibile tramite response.parsed
            # Se la libreria non lo fa automaticamente o restituisce testo, 
            # gestiamo l'estrazione.
            
            if hasattr(response, 'parsed'):
                return response.parsed
            
            # Fallback se .parsed non è disponibile (dipende dalla versione esatta del SDK)
            result_text = response.text
            data = json.loads(result_text)
            return SentimentResult(**data)

        except Exception as e:
            logger.error(f"Errore durante l'analisi del sentiment con Gemini: {e}")
            return None

if __name__ == "__main__":
    # Test rapido
    analyzer = SentimentAnalyzer()
    test_news = "Apple reports record-breaking quarterly revenue, shares surge 5% in after-hours trading."
    result = analyzer.analyze_sentiment(test_news)
    if result:
        print(f"Risultato: {result.model_dump_json(indent=2)}")
