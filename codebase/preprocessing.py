def pre_process_paquete(paquete_csv, entrega_csv):
    '''
    Method for preprocessing passport paquete into a weekly frequency for time series model training
    
    @params inputs: A path for csv file "paquete.csv"
    
    @returns f_paquete: DataFrame containing weekly passport requests
    @returns paquete: DataFrame containing read paquete.csv as DataFrame
    @returns entrega: DataFrame containing read entrega.csv as DataFrame
    '''
    
    import pandas as pd
    from datetime import date
        
    #Read paquete.csv
    paquete = pd.read_csv(paquete_csv , sep=";", encoding='latin1', header=None).rename(columns={1:"Pasaporte", 3:"Fecha"})
    
    #Read entrega.csv
    entrega = pd.read_csv(entrega_csv, sep=";", encoding='latin1', header=None).rename(columns={0:"Pasaporte",1:"Cantidad",2:"Fecha"})

    #Convert fecha columns to datetime
    entrega['Fecha'] = pd.to_datetime(entrega['Fecha'])
    paquete['Fecha'] = pd.to_datetime(paquete['Fecha'])


    if date.today().strftime("%Y-%m") > '2022-07':
        paquete = paquete[paquete["Fecha"] < date.today().strftime("%Y-%m")] #Remove ex ante observations
    
    else:
        paquete = paquete[paquete["Fecha"]<='2022-02'] #Remove ex ante observation
    


    #Preprocess .csv
    f_paquete = paquete.groupby(paquete['Fecha'].dt.strftime('%Y-%W')).size() #Group by year week
    f_paquete = pd.DataFrame(f_paquete).reset_index()
    f_paquete['Fecha'] = pd.to_datetime(f_paquete.Fecha +'-0', format='%Y-%W-%w') #Add days to week in order to convert to date
    f_paquete = f_paquete.groupby('Fecha').sum() #Group again
    f_paquete.sort_index(inplace=True, ascending=True) 
    f_paquete.rename(columns = {0:'P'}, inplace = True) #Rename column
    f_paquete = f_paquete.asfreq(freq='W', fill_value=0) #Fill in missing weeks
    
    return f_paquete, paquete, entrega