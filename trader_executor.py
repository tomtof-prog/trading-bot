from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, TakeProfitRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TraderExecutor:
    def __init__(self):
        try:
            # Inizializza il client di trading (Paper per default)
            self.client = TradingClient(api_key=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, paper=True)
            logger.info("TradingClient inizializzato correttamente.")
        except Exception as e:
            logger.error(f"Errore durante l'inizializzazione di TradingClient: {e}")
            raise

    def get_account_equity(self) -> float:
        """
        Recupera il capitale totale (equity) dell'account.
        """
        try:
            account = self.client.get_account()
            return float(account.equity)
        except Exception as e:
            logger.error(f"Errore nel recupero dell'equity dell'account: {e}")
            return 0.0

    def get_latest_price(self, symbol: str) -> float:
        """
        Recupera l'ultimo prezzo di mercato per un ticker.
        Nota: Alpaca fornisce diverse API per i dati, usiamo una stima o un'interrogazione semplice.
        """
        try:
            # Per semplicità usiamo l'ultimo prezzo disponibile tramite l'asset o una richiesta di quote
            # In un bot reale, si userebbe il client dei dati storici/real-time
            # Qui assumiamo di poterlo ottenere o stimare.
            # Per ora, usiamo una placeholder logic o integriamo NewsClient/StockClient se necessario.
            # In alpaca-py, per i dati si usa StockHistoricalDataClient
            from alpaca.data.historical import StockHistoricalDataClient
            from alpaca.data.requests import StockLatestQuoteRequest
            
            data_client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)
            request_params = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            latest_quote = data_client.get_stock_latest_quote(request_params)
            
            # Usiamo il prezzo ask per l'acquisto
            return float(latest_quote[symbol].ask_price)
        except Exception as e:
            logger.error(f"Errore nel recupero del prezzo per {symbol}: {e}")
            return 0.0

    def execute_market_order_with_bracket(self, symbol: str, notional_amount: float):
        """
        Esegue un ordine a mercato con Take Profit (3%) e Stop Loss (1.5%).
        """
        try:
            # Recupera il prezzo attuale per calcolare SL e TP
            current_price = self.get_latest_price(symbol)
            if current_price <= 0:
                logger.error(f"Prezzo non valido per {symbol}. Ordine annullato.")
                return

            # Calcolo prezzi per bracket order
            take_profit_price = round(current_price * 1.03, 2)
            stop_loss_price = round(current_price * 0.985, 2)

            # Preparazione Bracket Order
            # Un bracket order in alpaca-py si fa specificando take_profit e stop_loss nel MarketOrderRequest
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                notional=notional_amount, # Usiamo notional per investire un importo fisso in USD
                side=OrderSide.BUY,
                time_in_force=TimeInForce.GTC,
                order_class=OrderClass.BRACKET,
                take_profit=TakeProfitRequest(limit_price=take_profit_price),
                stop_loss=StopLossRequest(stop_price=stop_loss_price)
            )

            # Invio ordine
            order = self.client.submit_order(order_data=market_order_data)
            logger.info(f"Ordine BRACKET inviato per {symbol}: Investimento ${notional_amount}, TP ${take_profit_price}, SL ${stop_loss_price}")
            return order

        except Exception as e:
            logger.error(f"Errore durante l'esecuzione dell'ordine per {symbol}: {e}")
            return None

if __name__ == "__main__":
    # Test rapido (Attenzione: esegue trade reali in Paper Trading se le chiavi sono valide)
    executor = TraderExecutor()
    # print(executor.get_account_equity())
    # executor.execute_market_order_with_bracket("AAPL", 100.0)
