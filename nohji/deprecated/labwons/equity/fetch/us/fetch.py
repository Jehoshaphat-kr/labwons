from nohji.deprecated.labwons.equity import price


class equity(price):

    def __init__(self, ticker:str):
        super().__init__(ticker=ticker, country="USA")
        return

