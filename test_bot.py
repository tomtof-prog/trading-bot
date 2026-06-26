import unittest
from unittest.mock import MagicMock, patch
from risk_manager import RiskManager
from sentiment_analyzer import SentimentResult
import os

# Impostiamo variabili d'ambiente fittizie per evitare errori di caricamento
os.environ["ALPACA_API_KEY"] = "test"
os.environ["ALPACA_SECRET_KEY"] = "test"
os.environ["GEMINI_API_KEY"] = "test"

class TestTradingBotLogic(unittest.TestCase):

    def test_risk_manager_validation(self):
        rm = RiskManager(total_equity=10000.0)
        
        # Test sentiment alto
        self.assertTrue(rm.validate_trade(85, "AAPL"))
        
        # Test sentiment basso
        self.assertFalse(rm.validate_trade(70, "TSLA"))
        
        # Test ticker mancante
        self.assertFalse(rm.validate_trade(90, None))

    def test_risk_manager_position_sizing(self):
        equity = 50000.0
        rm = RiskManager(total_equity=equity)
        
        # 2% di 50000 è 1000
        expected_size = equity * 0.02
        self.assertEqual(rm.calculate_position_size(), expected_size)

    @patch('sentiment_analyzer.genai.Client')
    def test_sentiment_analyzer_mock(self, mock_genai):
        from sentiment_analyzer import SentimentAnalyzer
        
        # Mocking the response from Gemini
        mock_client = MagicMock()
        mock_genai.return_value = mock_client
        
        analyzer = SentimentAnalyzer()
        
        mock_response = MagicMock()
        mock_response.parsed = SentimentResult(
            ticker="NVDA",
            sentiment_score=90,
            confidence=95,
            reason="Ottimi guadagni trimestrali"
        )
        mock_client.models.generate_content.return_value = mock_response
        
        result = analyzer.analyze_sentiment("Nvidia reports record earnings.")
        
        self.assertEqual(result.ticker, "NVDA")
        self.assertEqual(result.sentiment_score, 90)
        self.assertTrue(result.sentiment_score > 80)

if __name__ == '__main__':
    unittest.main()
