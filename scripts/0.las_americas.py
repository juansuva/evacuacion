# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:33:15 2019

@author: Juan
"""

import pandas as pd
from lib_process import *

def get_americas(orden,fecha,formatofecha):
    ##se obtiene los datos del cliente
    las_americas="0. Las Americas.xlsx"
    data_lasamerica=get_data_all(las_americas)
    ##sse organiza codgidos del cliente
    data_lasamericas,no_code,code=set_tq_codes2(data_lasamerica, "LAS AMERICAS",'CADENAS')
    #se limpian descontinuados
    data_lasamericas=elimina_descontinuado(data_lasamericas)
    #se limpian unidades
    data_lasamericas=elimina_unidades(data_lasamericas)    
    #se obtiene formato concatenado y codigo de negocio
    data_lasamericas=set_concatenated_and_format(data_lasamericas, "MAESTRA EL SALVADOR")
    #se obtienen puntos de cod de puntos de venta
    data_lasamericas=set_sellings_point_tq_code(data_lasamericas, "LAS AMERICAS ")
    #se obtienen precios 
    data_lasamericas,noprice=set_price_hist(data_lasamericas,'FARMACIA LAS AMERICAS','CADENAS')
    
    #se genera consolidado
    consolidado=get_consolidated_report_cadenas_su(data_lasamericas)   
    
    #se organiza index y se elimina COD NEG
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True)
    consolidado.to_excel("../salida/CONSOLIDADO_LAS_AMERICAS.xlsx")
    
    extra_data_america = { 'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                         'COD_CANAL': 92,'CANAL': "91 Cadenas de Dorguería", 'COD_CLIPADRE': 9004, 'REF_CLIENTE': "FARMACIA LAS AMERICAS",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte
    colocacion,resto=get_form_report(con, extra_data_america, 'FARMACIA LAS AMERICAS')
    colocacion['ORDEN']=91
    colocacion.to_excel("../salida/reportes_las_americas_valorizada.xlsx")
    
get_americas(89,"Feb 2019","201902")