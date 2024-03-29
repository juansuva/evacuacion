# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:28:20 2019

@author: Juan
"""

import pandas as pd
from lib_process import *
import sys

def get_camila(orden,fecha,formatofecha):
    ##se obtiene los datos del cliente
    da_camila=get_data_all("0. Camila.xlsx")
    
    #da_camila.to_excel("salida/CONSOLIDADO_CAMILA12.xlsx")
    ##sse organiza codgidos del cliente
    data_camia,no_code,base2=set_tq_codes2(da_camila, "CAMILA",'CADENAS')    
    #se obtiene formato concatenado y codigo de negocio
    data_camila=set_concatenated_and_format(data_camia, "MAESTRA EL SALVADOR")
    #se limpian las unidades
    data_camila=elimina_unidades(data_camila)
    data_camila=elimina_descontinuado(data_camila)
    #se obtienen puntos de cod de puntos de venta
    data_camila=set_sellings_point_tq_code(data_camila, "CAMILA")
    #se obtienen precios 
    data_camila_pre,no_price=set_price_nor(data_camila,"FARMACIA CAMILA","Lista de Precios Cadenas","CADENAS")    
    #print(no_price['COD TQ'].unique())
    #se genera consolidado
    consolidado=get_consolidated_report_cadenas_su(data_camila_pre)
    #se organiza index y se elimina COD NEG
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True)     
    consolidado.to_excel("../salida/CONSOLIDADO_CAMILA.xlsx")
    extra_data_camila = {           'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 91,'CANAL': "91 Cadenas de Droguería", 'COD_CLIPADRE': 2848, 'REF_CLIENTE': "FARMACIA CAMILA",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte
    colocacion=get_form_report_NOR(con, extra_data_camila, 'FARMACIA CAMILA',0,0)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel("../salida/reportes_camila_valorizada.xlsx")
    
if len(sys.argv) >=2:
    get_camila(sys.argv[1],sys.argv[2],sys.argv[3])
else: 
    
    
    get_camila(89,"Feb 2019","201902")

