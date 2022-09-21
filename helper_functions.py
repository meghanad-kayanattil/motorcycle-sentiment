import datetime as dt
def time_frame_calculator(timeframe):
    """
    convering user input of search interval to date for the main function
    """
    timeframe_defenitions = ['Last 30 days', 'Last 6 months', 'Last 1 year',
                             'Last 2 years', 'Last 3 years', 'Last 4 years', 'Last 5 years']
    days_to_subtract = [30, 160, 365, 365*2, 365*3, 365*4, 365*5]
    for i in range(len(timeframe_defenitions)):
        if timeframe == timeframe_defenitions[i]:
            current_epoch = dt.date.today()
            begenning_epoch = current_epoch - \
                dt.timedelta(days=days_to_subtract[i])
            return current_epoch, begenning_epoch
