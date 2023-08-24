def train_prophet(f_paquete, start_date, final_date, cap=50, floor=0, cv=False, initial='340 W', period='5 W', horizon='10 W', 
                  changepoint_prior_scale=0.005,changepoint_range=0.8,seasonality_prior_scale=0.1, holidays_prior_scale= 10, seasonality_mode= 'additive',
                  param_grid = {'changepoint_prior_scale': [0.005, 0.05, 0.5, 5], 
                                'changepoint_range': [0.8, 0.9], 
                                'seasonality_prior_scale':[0.1, 1, 10], 
                                'holidays_prior_scale':[0.1, 1, 10], 
                                'seasonality_mode': ['multiplicative','additive']}):
    '''
    Method for training a prophet model
    
    @params f_paquete: A preprocessed dataframe with weekly dates - DataFrame
    @params start_date: Start date (YYYY-MM-DD) used for training (inclusive) - str
    @params final_date: Final date (YYYY-MM-DD) used for training (inclusive) - str
    @params cap: Cap used for Prophet
    @params floor: Floor used for Prophet
    @params cv: Whether to apply cross validation for hyperparameters or not - boolean
    @params initial: Initial period for cv training  int
    @params period: Rolling period for cv - int
    @params horizon: Horizon for cv predictions - int
    @params changepoint_prior_scale: Changepoint prior scale for prophet model
    @params changepoint_range: Changepoint range for prophet model
    @params seasonality_prior_scale: Seasonality prior scale for prophet model
    @params holidays_prior_scale: Holidays prior scale for prohet model
    @params seasonality_mode: Seasonality mode for prophet model
    @params parameter_grid: Parameter grid to use for cross-validation if cv=True
        
    '''
    
    #Import packages
    import holidays
    import pandas as pd
    
    import pickle
    import datetime
    
    from fbprophet import Prophet
    from prophet_cross_validation import prophet_cross_validation
        
    
    def next_sunday(test_date, weekday_idx): return test_date + datetime.timedelta(days=(weekday_idx - test_date.weekday() + 7) % 7)

    
    #Create prophet dataframe
    prophet_df = f_paquete.reset_index().rename(columns = {'P':'y', 'Fecha':'ds'})
    prophet_df = prophet_df[(prophet_df["ds"]>=start_date) & (prophet_df["ds"]<=final_date)]
    prophet_df['cap'] = cap
    prophet_df['floor'] = floor
    
    
    #Create holiday dataframe
    holiday_list = []
    for holiday in holidays.Colombia(years=list(range(1995, 2045))).items():
        holiday_list.append(holiday)

    holidays_df = pd.DataFrame(holiday_list, columns=["date", "holiday"])
    holidays_df['date'] = holidays_df['date'].astype('datetime64[ns]')
    holidays_df["ds"] = holidays_df['date'].apply(lambda x: next_sunday(x, 6))
    
    if cv==True:
        #Tine hyperparameters if cv=True, else use default values
        changepoint_prior_scale, changepoint_range, seasonality_prior_scale, holidays_prior_scale, seasonality_mode = prophet_cross_validation(
                prophet_df = prophet_df, 
                holidays_df = holidays_df, 
                initial = initial, 
                period = period,
                horizon = horizon,
                param_grid=param_grid)
        
    pm = Prophet(
            changepoint_prior_scale = changepoint_prior_scale, 
                 changepoint_range = changepoint_range,
                 seasonality_prior_scale = seasonality_prior_scale,
                 holidays_prior_scale = holidays_prior_scale,
                 seasonality_mode = seasonality_mode,
                 interval_width=0.95,
                 yearly_seasonality=True,
                 holidays= holidays_df,
                 weekly_seasonality = False,
                 daily_seasonality=False
                 )

    #Fit model
    pm_model = pm.fit(prophet_df)
    
    #Save model
    with open("prophet_model.pkl", "wb") as file_:
        pickle.dump(pm_model, file_)