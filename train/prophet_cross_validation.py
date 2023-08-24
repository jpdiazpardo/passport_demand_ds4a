def prophet_cross_validation(prophet_df, holidays_df ,initial, period, horizon, param_grid):
    import ast
    import itertools
    import pandas as pd
    
    from fbprophet import Prophet
    from fbprophet.diagnostics import performance_metrics
    from fbprophet.diagnostics import cross_validation
    from dask.distributed import Client
    
    Client()
    
    def create_param_combinations(**param_dict):
        param_iter = itertools.product(*param_dict.values())
        params = []
    
        for param in param_iter:
            params.append(param) 
    
        params_df = pd.DataFrame(params, columns=list(param_dict.keys()))
        return params_df

    def single_cv_run(history_df, metrics, param_dict):
        m = Prophet(interval_width=0.95, holidays= holidays_df, weekly_seasonality=False, daily_seasonality=False, **param_dict)
        m.fit(history_df)
        df_cv = cross_validation(m, initial=initial, period=period, horizon = horizon, parallel="dask")
        df_p = performance_metrics(df_cv).mean().to_frame().T
        df_p['params'] = str(param_dict)
        df_p = df_p.loc[:, metrics]
        return df_p

    metrics = ['horizon', 'rmse', 'mae', 'params'] 

    results = []


    params_df = create_param_combinations(**param_grid)

    for param in params_df.values:
        param_dict = dict(zip(params_df.keys(), param))
        cv_df = single_cv_run(prophet_df,  metrics, param_dict)
        results.append(cv_df)

    results_df = pd.concat(results).reset_index(drop=True)
    best_param = results_df.loc[results_df['mae'] == min(results_df['mae']), ['params']]
    
    final_params = best_param["params"][0]
    
    changepoint_prior_scale = ast.literal_eval(final_params)["changepoint_prior_scale"] #1 - Prior scale
    changepoint_range = ast.literal_eval(final_params)["changepoint_range"] #2 - Range
    seasonality_prior_scale = ast.literal_eval(final_params)["seasonality_prior_scale"] #3 - Seasonality
    holidays_prior_scale = ast.literal_eval(final_params)["holidays_prior_scale"] #4 - Holidays
    seasonality_mode = ast.literal_eval(final_params)["seasonality_mode"] #5 - Seasonality mode
           
    return changepoint_prior_scale, changepoint_range, seasonality_prior_scale, holidays_prior_scale, seasonality_mode