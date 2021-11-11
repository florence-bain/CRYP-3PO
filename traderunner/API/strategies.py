import logging

logger = logging.getLogger()

class Strategies:

    def golden_cross(self, historical_candle_callback):

        daily_candlesticks = historical_candle_callback
        fifty_day = daily_candlesticks[-50:]
        two_hundred_day = daily_candlesticks[-200:]

        fifty_day_array_close = []
        two_hundred_day_array_close = []

        for candlestick in fifty_day:
            fifty_day_array_close.append(candlestick.close)

        for candlestick in two_hundred_day:
            two_hundred_day_array_close.append(candlestick.close)

        fifty_day_moving_average = (sum(fifty_day_array_close)/50)
        two_hundred_day_moving_average = (sum(two_hundred_day_array_close)/200)

        #print(f"This is the fifty day moving average {fifty_day_moving_average}")
        #print(f"This is the two hundred day moving average {two_hundred_day_moving_average}")

        #has_it_crossed = 'false'

        if fifty_day_moving_average > two_hundred_day_moving_average:
            has_it_crossed = fifty_day_moving_average
        elif fifty_day_moving_average < two_hundred_day_moving_average:
            has_it_crossed = 'false'

        #print(has_it_crossed)

        return has_it_crossed

    def sell_strategy(self, historical_candle_callback, ask_price):
        fifty_day = historical_candle_callback[-50:]

        fifty_day_array_close = []

        for candlestick in fifty_day:
            fifty_day_array_close.append(candlestick.close)

        fifty_day_moving_average = (sum(fifty_day_array_close)/50)

        if (fifty_day_moving_average * 0.15) < ask_price:
            message = (f"The price of {ask_price} has fallen by 15% over the last 50 days, probably time to sell off")


        #message = 'nothing defined at this moment'

        return message
