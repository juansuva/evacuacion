# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:28:00 2019

@author: Juan
"""

import pandas as pd
from lib_process import *

def get_labuena(orden,fecha,formatofecha):
    ##se obtiene los datos del cliente
    da_labuena=get_data_all("0. La Buena.xlsx")
    #se limpian las unidades
    da_labuena=elimina_unidades(da_labuena)
    ##sse organiza codgidos del cliente
    da_labuena,nocodes,code=set_tq_codes_str(da_labuena,'LA BUENA','CADENAS')
    #se limpian los descontinuados
    da_labuena=elimina_descontinuado(da_labuena)
    #se obtienen puntos de ventan para TQ
    da_labuena=set_sellings_point_tq_code(da_labuena,'LA BUENA')
    #se obtiene formato concatenado y codigo de negocio
    da_labuena=set_concatenated_and_format(da_labuena, "MAESTRA EL SALVADOR")
    #se obteniene los precios
    da_labuena,no_price=set_price_nor_aliados(da_labuena,"FARMACIA LA BUENA","Lista de Precios Cadenas","CADENAS")
    ##se generaa el consolidado
    consolidado=get_consolidated_report_cadenas_su(da_labuena)
    #Se resetea el index y se borra cod neg
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    
    consolidado.to_excel("../salida/CONSOLIDADO_LABUENA.xlsx")
    extra_data_labuena = {      'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha,'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 91,'CANAL': "91 Cadenas de Dorguería", 'COD_CLIPADRE': 2843, 'REF_CLIENTE': "FARMACIA LA BUENA",
                              'FLAG_CUA_BAS': ""
                 }
    #se genera reporte de valorizacion nor
    colocacion=get_form_report_NOR(con, extra_data_labuena, 'FARMACIA LA BUENA',1,0)
    colocacion.to_excel("../salida/reportes_la_buena_valorizada.xlsx")
    
get_labuena(89,"Feb 2019","201902")