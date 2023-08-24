def year_on_year(f_paquete):
    '''
    Function for generating year on year visualization for plotly
    
    @params f_paquete: A preprocessed dataframe with weekly dates - DataFrame
    
    @returns YoY: DataFrame with format needed for plotly YoY 
    @returns cyear: Returns current year in f_paquete 
    @returns lyear: Returns last year in f_paquete 
    '''
    
    import pandas as pd    
    
    YoY = pd.DataFrame(columns = ["Current Year","Last Year"])
    YoY["Current Year"]= f_paquete[str(f_paquete.index.max().year)]["P"].tolist()
    YoY["Last Year"]=f_paquete[str(f_paquete.index.max().year-1)]["P"].tolist()[:len(YoY)]
    YoY["% Change"] = 100*((YoY["Current Year"] - YoY["Last Year"])/ YoY["Last Year"])
    YoY["% Change"] = YoY["% Change"].apply(lambda x: "N/A" if x==float("inf") else str(round(x,1))+"%")
    YoY.index = f_paquete[str(f_paquete.index.max().year)]["P"].index

    cyear = YoY.index.year[0]
    lyear = cyear-1
    
    return YoY, cyear, lyear