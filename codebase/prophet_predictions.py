def predict_prophet(f_paquete, start_date, forecast_end):
    '''
    Function for generating predictions of prophet model needeed for plotly visializations
    
    @params f_paquete: A preprocessed dataframe with weekly dates - DataFrame
    @params start_date: Start date (YYYY-MM-DD) from which the visualization will start (inclusive) - str
    @params forecast_end: Ending month for forecast horizon (YYYY-MM) - str
    
    @returns pm_forecast: DataFrame containing fit model between start end and forecast_end 
    @returns only_forecast: DataFrame containing out of sample predictions only in long format
    @returns f_table: DataFrame containing out of sample predictions only in wide format
    @returns pm_model: Trained prophet model used for predictions
    '''
    
    import pickle
    import pandas as pd
    import numpy as np
    import datetime
    
    def first_dow(year, month, dow):
        day = ((8 + dow) - datetime.date(year, month, 1).weekday()) % 7
        return datetime.date(year, month, day)
    
    #Load model
    with open("data/prophet_model.pkl", "rb") as file_:
        pm_model= pickle.load(file_)
        
    my_year = int(forecast_end[:4]) #Extracts year from forecast_end
    my_month = int(forecast_end[-2:]) #Extracts month from forecast_end
        
    #Create future dataframe
    pm_future = f_paquete.copy().reset_index().rename(columns = {'Fecha':'ds'})
    pm_future = pm_future[pm_future['ds']>=start_date][["ds",'P']].reset_index(drop=True)
    pm_future.set_index('ds',inplace=True)
    pm_future.loc[first_dow(my_year, my_month,6)] = 0
    pm_future = pm_future.asfreq(freq='W', fill_value=0)
    pm_future.reset_index(inplace=True)
    
    pm_forecast = pm_model.predict(pm_future)
       
    for c in ["yhat","yhat_lower","yhat_upper"]: #Round forecast values and make integer
        pm_forecast[c] = pm_forecast[c].apply(lambda x: max(0, int(round(x,0))))
  
    #Join forecast with real values
    pm_forecast = pm_forecast.merge(f_paquete.reset_index().rename(columns = {'Fecha':'ds','P':'y'}), on='ds', how='left',indicator=True)
    
    pm_forecast["color"] = pm_forecast.apply(lambda x: 'royalblue' if (x.y>=x.yhat_lower and x.y<=x.yhat_upper) else 'red', axis=1) #Format actuals
    pm_forecast["label"] = pm_forecast.apply(lambda x: 'Actual' if (x.y>=x.yhat_lower and x.y<=x.yhat_upper) else 'Anomaly', axis=1) #Format actuals / anomaly
    pm_forecast["size"] = pm_forecast.apply(lambda x: 0 if (x.y>=x.yhat_lower and x.y<=x.yhat_upper) else 6, axis=1) # Set size of markers
    pm_forecast["time_lab"] = pm_forecast["ds"].apply(lambda x: x.strftime("Week: %W (%d-%B)")) # Create time label
    
    #Create additional dataframe with forecasts only
    only_forecast = pm_forecast.copy()

    #First forecast equal value
    index_both = only_forecast.index[only_forecast["_merge"]=='both'][-1] 
    only_forecast.loc[index_both,'yhat'] = only_forecast.loc[index_both,'y']

    #Filter dataframe from last actual until end
    only_forecast = only_forecast.iloc[index_both:]
    
    g = only_forecast[["ds","yhat"]].reset_index(drop=True).rename(columns = {'ds':'Week', 'yhat':'Forecast'})
    groups = g.groupby(np.arange(len(g.index))//20)
    
    f_table = pd.DataFrame()
    
    for (frameno, frame) in groups:
        f_table = pd.concat([f_table, frame.reset_index(drop=True)], axis=1)

    f_table = f_table.astype(str).replace(to_replace =["NaT", "nan"], value ="")
    
    return pm_forecast, only_forecast, f_table, pm_model