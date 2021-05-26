import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import def_cal
import datetime
import re

#Titulo
st.title('Analisis de intervalos diario')
st.markdown("""
Aplicación web capaz de calcula la cantidad de horas realizadas por personal especifico durante los intervalos del día.
Principalmente utilizado como validador en casos de analisis de mapa de calor.
""")

#Cabecera Sidebar
st.sidebar.header('Introduccion de valores')

#Reporte Agent-Login-Logut
date_required = st.sidebar.date_input('Día a evaluar', min_value=datetime.date(2019,1,1) ) #Returns datetime.date
daily_report = st.sidebar.file_uploader('Reporte dia', type=['csv'], accept_multiple_files=False)
delim = st.sidebar.radio('Delimitador',(',',';'))
bd_ht = st.sidebar.file_uploader('Base de datos de referencia')
st.sidebar.text('BBDD Dotacion enviado por Yorman semanalmente')

#Base de datos Holdtech
if daily_report:
    df_report= pd.read_csv(daily_report, delimiter=delim, skipfooter=2)

    df_report.reset_index(inplace=True)
    df_report.drop(labels=['index', 'Media Type'], axis='columns', inplace=True)
    df_report.columns = ['Tenant Name', 'Agent Name', 'Start Timestamp', 'End Timestamp', 'Active Time']

    df_report['Tenant Name'] = df_report['Tenant Name'].str.replace('ï¿½', 'Ñ')

    df_report['Start Timestamp'] = pd.to_datetime(df_report['Start Timestamp'])
    df_report['End Timestamp'] = pd.to_datetime(df_report['End Timestamp'])

    df_report['fecha_inicio'] = df_report['Start Timestamp'].dt.date
    df_report['tiempo_inicio'] = df_report['Start Timestamp'].dt.time
    df_report['fecha_cierre'] = df_report['End Timestamp'].dt.date
    df_report['tiempo_cierre'] = df_report['End Timestamp'].dt.time

    df_report['Intervalo'] = df_report['Start Timestamp'].dt.floor('30min')
    df_report['users'] = df_report['Agent Name'].str.extract(r'(?<=.\()(\w+)').apply(lambda x: x.str.upper())

    columns = ['Agent Name', 'Tenant Name', 'users','Active Time', 'Start Timestamp', 'fecha_inicio', 'tiempo_inicio', 'End Timestamp', 'fecha_cierre', 'tiempo_cierre', 'Intervalo']
    df_report = df_report.reindex(columns=columns)

    st.subheader('Reporte Login-Logout')
    st.write(df_report)
    
else:
    st.write("Waiting for Agent Loging-Logout file...")


if  bd_ht and date_required:
    col_bd = ['Cargo', 'Servicio', 'RutDV', 'Usuario Red', 'Nombre Completo', 'Jornada', 'Estado', 'Fecha Baja', 'Fecha Ingreso Plataforma']
    df_bd = pd.read_excel(bd_ht, sheet_name='BBDD EAC', usecols=col_bd, dtype={'Fecha Baja': pd.datetime, 'Fecha Ingreso Plataforma':pd.datetime })

    unique_charge = list(def_cal.get_unique_cargo(df_bd))
    select_charge = st.sidebar.multiselect('Cargos', options=sorted(unique_charge), default='EAC Call Center')

    unique_service = list(def_cal.get_unique_service(df_bd))
    select_service = st.sidebar.multiselect('Servicio', options=sorted(unique_service), default=unique_service)

    df_bd_filter = def_cal.get_bd_filter(df_bd, cargo=select_charge, servicio=select_service, date=date_required)
else:
    st.write("Waiting for BD")

if daily_report and bd_ht:
    st.subheader('Reporte filtrado')
    st.markdown('De acuerdo a la seleccion de filtros de Cargo y Servicio, tenemos los siguientes ejecutivos a formar parte del analisis de horas log diarias')
    df_filter = df_report[df_report['users'].isin(df_bd_filter['Usuario Red'])]
    st.write(df_filter)

    df, sf, hf = def_cal.horas_log(df_filter)

    with st.beta_expander('Mostrar desglose...'):
        col1, col2 = st.beta_columns([3,1])
        
        col1.subheader('Línea tiempo Requerido')
        col1.line_chart(hf)
        
        col2.subheader('Horas Log')
        col2.write(df)

    #Considerar st.area_chart, para evaluar el requerido junto a las horas log
        
    df_merge = df_filter.merge(df_bd_filter, how='left', left_on='users', right_on='Usuario Red') 
    df_merge_group = df_merge.groupby(by=['users', 'Jornada'])['Active Time'].agg([('Active Time', lambda x: pd.to_timedelta(x, unit='s').sum())]).reset_index()
    #df_merge_group['Jornada'] = df_merge_group['Jornada'].astype('int')
    #st.write(df_merge_group)
    check_usuario = st.checkbox('Desglose por Usuario?')
    if check_usuario:

        fig, ax = plt.subplots(figsize=(6,30))
        lp = sns.barplot(data=df_merge_group, y = 'users', x = 'Active Time', hue = "Jornada", orient = "h")
        lp.set(ylim=[-1,len(df_merge_group)], xlabel='Tiempo (seg)', ylabel='Usuarios')
        lp.set_title('Horas produccion', fontdict={'fontsize':20, 'fontweight': 'bold', 'color':'black'}, loc='right', pad=15)

        st.pyplot(fig=fig)

    st.markdown('## Analisis cumplimiento de requerido')
    st.write('Si desea comparar el resultado mostrado junto al requerido, favor cargar archivos de requerido correspondiente al mes del día a evaluar')
    
    #Carga de archivo para requerido
    req = st.file_uploader('Ingresar Requerido')
    st.text('Ingresar rango de columnas a ser considedas como tabla de requerido. Favor considerar columna de indice.')
    inicio_col = st.text_input('Columna de inicio', value="AI")
    final_col = st.text_input('Columna de cierre', value="BN")
    
    
    if req and inicio_col and final_col:
        req_v1 = pd.read_excel(req, sheet_name='Holdtech', skiprows=3, header=0, index_col=0, usecols="{inicio}:{cierre}".format(inicio=inicio_col, cierre=final_col))
        req_v1.dropna(inplace=True)
        req_v1 = req_v1.T

        c1, c2, c3 = st.beta_columns(3)
        
        #Preprocessing del requerido
        req_min = re.search(r"(?<=, 0)\d+:\d+", hf.index.min())[0]
        req_eval = req_v1.loc[date_required, req_min:"23:30"]

        c1.write("Requerido")
        c1.write(req_eval)

        #Preprocessing de horas_log
        hf_max = hf.index.max()[0:8]+"00:00"
        hf_eval = hf.loc[hf.index.min():hf_max]

        c2.write('Horas log')
        c2.write(hf_eval)

        #Preprocessing comparacion real/requerido
        diferencia = (hf_eval.values /req_eval.values )*100
        req_diff = pd.Series(diferencia.round(2), index=req_eval.index, name=hf_eval.index.max()[0:6])

        c3.write('Req cumplimiento')
        c3.write(req_diff)

        resumen_df = pd.DataFrame(dict(requerido=req_eval.values, logs=hf_eval.values), index=hf_eval.index)
        st.line_chart(resumen_df, width=30)

            
else:
    st.write("Waiting for BD Holdtech and Agent Loging Logout to be loaded")