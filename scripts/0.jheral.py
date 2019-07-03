# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:28:19 2019

@author: Juan
"""

import pandas as pd
from lib_process import *
import sys

def get_jheral(orden,fecha,formatofecha):
    ##se obtiene los datos del cliente
    da_jheral=get_data_all("0. Jheral Farma.xlsx")
    ##sse organiza codgidos del cliente
    data_jheral=set_tq_codes_of_cli(da_jheral)
        #se limpia los descontinuados
    da_jheral=elimina_descontinuado(da_jheral)
    #se limpian las unidades
    da_jheral=elimina_unidades(da_jheral)
    dar=organiza_cod_tq_jheral(data_jheral)
    dar=set_concatenated_and_format(dar, "MAESTRA EL SALVADOR")
    dar=filter_u_codtq(dar)
    #se obtienen precios 
    dar,no_price=set_price_nor(dar,"Jheral Farma","Lista de Precios Mayoristas","MAYORISTAS")
    #se genera consolidado
    consolidado=get_consolidated_report_mayoristas(dar)
    #se organiza index y se elimina COD NEG
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    
    consolidado.to_excel("../salida/CONSOLIDADO_JHERAL.xlsx")
    
    extra_data_jheral = {    'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2838, 'REF_CLIENTE': "Jheral Farma",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte
    colocacion=get_form_report_mayorista(con, extra_data_jheral, 'Jheral Farma',0,0)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel("../salida/reportes_jheral_valorizada.xlsx")
    
if len(sys.argv) >=2:
    get_jheral(sys.argv[1],sys.argv[2],sys.argv[3])
else: 
    
    get_jheral(91,"Abr 2019","201904")