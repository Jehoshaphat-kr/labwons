from labwons.equity.fetch.price import price


class equity(price):

    def __init__(self, ticker:str):
        super().__init__(ticker=ticker, country="USA")
        return

