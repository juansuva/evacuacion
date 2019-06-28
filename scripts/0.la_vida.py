# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:28:09 2019

@author: Juan
"""

import pandas as pd
from lib_process import *
import sys

def get_lavida(orden,fecha,formatofecha):
    ##se obtiene los datos del cliente
    da_lavida=get_data_all("0. La Vida.xlsx")
    #organiza tipod e datos la vida
    da_lavida=organiza_tipo_lavida(da_lavida)    
    #se limpian las unidades
    da_lavida=elimina_unidades(da_lavida)
    ##sse organiza codgidos del cliente
    data_lavida,nocode=set_tq_code_descripcion(da_lavida,"LA VIDA",'MAYORISTAS')
    #se limpian descontinuados
    data_lavida=elimina_descontinuado(data_lavida)
    #se obtienen puntos de cod de puntos de venta
    data_lavida=set_sellings_point_tq_code_names(data_lavida,"LA VIDA")
    #se obtiene formato concatenado y codigo de negocio
    data_lavida=set_concatenated_and_format(data_lavida, "MAESTRA EL SALVADOR")
    #se obtienen precios 
    data_lavida,no_price=set_price_nor_aliados(data_lavida,"FARMACIA LA VIDA","Lista de Precios Cadenas","CADENAS")
    #se genera consolidado
    consolidado=get_consolidated_report_cadenas_su(data_lavida)
    #se organiza index y se elimina COD NEG
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True)     
    consolidado.to_excel("../salida/CONSOLIDADO_LAVIDA.xlsx")
    extra_data_lavida = { 'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 91,'CANAL': "91 Cadenas de Dorguería", 'COD_CLIPADRE': 2844, 'REF_CLIENTE': "FARMACIA LA VIDA",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte
    colocacion=get_form_report_NOR(con, extra_data_lavida, 'FARMACIA LA VIDA',1,0)
    colocacion.to_excel("../salida/reportes_la_vida_valorizada.xlsx")
    
    
    
if len(sys.argv) >=2:
    get_lavida(sys.argv[1],sys.argv[2],sys.argv[3])
else: 
    get_lavida(89,"Feb 2019","201902")