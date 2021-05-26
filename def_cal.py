import pandas as pd
import numpy as numpy
from datetime import datetime, date, timedelta
import math

def t_seconds(stamp):
    #Total en segundos para un Timestamp
    sec = float(stamp.hour*3600+stamp.minute*60+stamp.second)
    return sec

def interv_dict(data):
    dict_intervalo = {}
    col = data['Intervalo'].dt.strftime("%d-%b, %H:%M:%S")

    for j in col:
        if j in dict_intervalo.keys():
            pass
        else:
            dict_intervalo[j] = pd.to_timedelta(0, unit='s')
            
    return dict_intervalo

def horas_log(data):
    dict_inter = interv_dict(data)

    col_horas = data[['Intervalo','Start Timestamp', 'End Timestamp']]

    for i, ti, tc in col_horas.itertuples(index=False):

        #Declarando variables
        dif = tc - ti # Timedelta
        # Diferencia entre el interv de inicio y el siguiente intervalo
        x = abs(t_seconds(ti)-t_seconds((i+timedelta(minutes=30)))) #Float
        
        if dif.total_seconds() < x :
            i_st = i.strftime("%d-%b, %H:%M:%S")
            dict_inter[i_st] += dif

        else:
            while True:
                i_st = i.strftime("%d-%b, %H:%M:%S")

                if abs((tc - i).total_seconds()) < 1800:                 
                    break

                elif i_st not in dict_inter.keys() :
                    dict_inter[i_st] = pd.to_timedelta(0, unit='s')

                else:
                    dict_inter[i_st] += pd.to_timedelta(x, unit='s') 
                    i+= timedelta(minutes=30)

                    if (i.hour != 23) & (i.minute != 30):
                        x = abs(t_seconds(i) - t_seconds((i+timedelta(minutes=30)))) #Float
                    else:
                        x = 1800 # PENDIENTE

            if i_st not in dict_inter.keys() :               
                dict_inter[i_st] = tc - i

    datetime_format = pd.Series(dict_inter, name="logs").sort_index()
    seconds_format = datetime_format.apply(lambda x : (x.total_seconds()/3600))
    hour_format = datetime_format.apply(lambda x : math.ceil((x.total_seconds()/3600))*2)
    
    return datetime_format, seconds_format, hour_format

def get_unique_cargo(data):
    """Devuelve set de valores unicos para Cargo"""
    return set(data['Cargo'].unique())

def get_unique_service(data):
    """Devuelve set de valores unicos para Servicio"""
    return set(data['Servicio'].unique())

def get_bd_filter(data, cargo:list, servicio:list, date):
    subset = data[(data['Cargo'].isin(cargo)) & (data['Servicio'].isin(servicio)) & (data['Fecha Ingreso Plataforma']<date) & ( (data['Estado']=='Vigente') | ( (data['Estado']=='No Vigente') & (data['Fecha Baja']>date) ) )]
    return subset

