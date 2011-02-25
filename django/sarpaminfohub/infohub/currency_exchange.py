from sarpaminfohub.infohub.models import ExchangeRate

class CurrencyExchange:
    def exchange(self, local_price, currency, year):
        if local_price is None: 
            return None
        
        if currency is None:
            return None
        
        exchange = ExchangeRate.objects.get(symbol=currency, year=year)

        return local_price * exchange.rate
