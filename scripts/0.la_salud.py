# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:28:14 2019

@author: Juan
"""

import pandas as pd
from lib_process import *
import sys

def get_lasalud(orden,fecha,formatofecha):
    ##se obtiene los datos del cliente
    da_lasalud=get_data_all("0. La Salud.xlsx")
    ##sse organiza codgidos del cliente
    data_lasalud,nocodes,code=set_tq_codes2(da_lasalud,'La Salud','MAYORISTAS')
    #elimina los datos con descontinuado 
    data_lasalud=elimina_descontinuado(data_lasalud)
    #se limpian las unidades
    data_lasalud=elimina_unidades(data_lasalud)
    #organiza codigos TQ
    data_lasalud=organiza_cod_tq_salud(data_lasalud)
    #obtiene concatenado y formato
    data_lasalud=set_concatenated_and_format(data_lasalud, "MAESTRA EL SALVADOR")
    #obtiene precios nor 
    data_lasalud,no_price=set_price_nor(data_lasalud,"La Salud","Lista de Precios Mayoristas","MAYORISTAS")
    #obtiene el consoldidado
    consolidado=get_consolidated_report_mayoristas(data_lasalud)
    #elimina la columna cod nego y reorganiza el index
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    #se genera el excel del reporte
    consolidado.to_excel("../salida/CONSOLIDADO_LA_SALUD.xlsx")
    
    extra_data_lasalud = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2852, 'REF_CLIENTE': "La Salud",
                          'FLAG_CUA_BAS': ""
             }
    colocacion=get_form_report_mayorista(con, extra_data_lasalud, 'La Salud',0,0)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel("../salida/reportes_la_salud_valorizada.xlsx")
    
    
if len(sys.argv) >=2:
    get_lasalud(sys.argv[1],sys.argv[2],sys.argv[3])
else: 
    get_lasalud(91,"Abr 2019","201904")