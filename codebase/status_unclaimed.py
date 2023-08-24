def status_unclaimed(paquete, entrega):
    """
    Method for creating status and unclaimed passport dataframes
    
    @params paquete: Paquete dataframe from .csv
    @params entrega: Entrega dataframe from .csv
    
    
    @returns stat_paquete: DataFrame containing near expiry passports
    @returns unclaimed_f: DataFrame containing unclaimed passports
    """
    
    from dateutil.relativedelta import relativedelta    
    import pandas as pd
     
    stat_paquete = paquete.copy() #Create copy from paquete
    stat_paquete["Fecha"] = stat_paquete["Fecha"].apply(lambda x: x + relativedelta(years=10)) #Lag date by ten years  
    stat_paquete = stat_paquete.groupby(stat_paquete['Fecha'].dt.strftime('%Y-%m')).size() #Group by year month
    stat_paquete.rename("Expiry passports", inplace=True) #Rename column
    
    #Merge paquete and entrega datasets
    paquete["Pasaporte"] = paquete["Pasaporte"].str.upper()
    entrega["Pasaporte"] = entrega["Pasaporte"].str.upper()
    paq_entrega = pd.merge(paquete, entrega, how='inner', on = "Pasaporte", suffixes=('_solicitud', '_entrega'))
    
       
    #Filter unclaimed passports
    unclaimed = paq_entrega.loc[paq_entrega.Fecha_entrega.isnull()]
        
    #Group by year month
    unclaimed_f = unclaimed.groupby(unclaimed['Fecha_solicitud'].dt.strftime('%Y-%m')).size() #Group by year month
    unclaimed_f.rename("Unclaimed passports", inplace=True)
    
    return stat_paquete, unclaimed_f
