# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:28:07 2019

@author: Juan
"""

import pandas as pd
import sys
from lib_process import *


def get_launo(orden,fecha,formatofecha):
    ##se obtiene los datos del cliente
    da_launo=get_data_all("0. La Uno.xlsx")
    ##sse organiza codgidos del cliente
    da_launo,nocodes,code=set_tq_codes_str(da_launo,'LA UNO','CADENAS')
    #se limpian las unidades
    da_launo=elimina_unidades(da_launo)
    #se limpia los descontinuados
    da_launo=elimina_descontinuado(da_launo)
    #se obtienen Cod de  puntos de ventas para TQ
    da_launo=set_sellings_point_tq_code_names(da_launo,'UNO ')
    #se obtiene concatenado formato y cod de neg
    da_launo=set_concatenated_and_format(da_launo, "MAESTRA EL SALVADOR")
    #se obtienen precios
    da_launo,no_price=set_price_nor(da_launo,"FARMACIA UNO","Lista de Precios Cadenas","CADENAS")
    #como el cliente blitea se organizan las unidades
    da_launo=calculate_units_s(da_launo,"LA UNO")
    #se genera el consolidado
    consolidado=get_consolidated_report_cadenas(da_launo)
    #se reset el index y se borra cod neg
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    
    consolidado.to_excel("../salida/CONSOLIDADO_UNO.xlsx")
    extra_data_launo = { 'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 91,'CANAL': "91 Cadenas de Dorguería", 'COD_CLIPADRE': 2851, 'REF_CLIENTE': "FARMACIA UNO",
                          'FLAG_CUA_BAS': ""
             }
    #se genera reporte de valorizacion nor 
    colocacion=get_form_report_NOR(con, extra_data_launo, 'FARMACIA UNO',0,1)
    colocacion.to_excel("../salida/reportes_la_uno_valorizada.xlsx")

if len(sys.argv) >=2:
    get_launo(sys.argv[1],sys.argv[2],sys.argv[3])
else: 
    get_launo(89,"Feb 2019","201902")