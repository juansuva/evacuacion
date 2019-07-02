# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 09:51:34 2019

@author: Juan
"""

import pandas as pd
from lib_process import *
import sys


def get_americana(orden,fecha,formatofecha):
    #cargamos los datos del cliente
    da_americana=get_data_all("0. Americana.xlsx")
    #limpiamos unidades en (0)
    da_americana=elimina_unidades(da_americana)
    #obtenemos codigos tq
    da_americana.to_excel("unida.xlsx")
    da_americana,nocode=set_tq_code(da_americana,'Americana','DEPOSITOS')
    #se eliminan los descontinuados 
    da_americana.to_excel("unidadtq.xlsx")
    da_americana=elimina_descontinuado(da_americana)
    da_americana.to_excel("unidadesc.xlsx")
    #se obtienen concateado formato y cod de negocio
    da_americana=set_concatenated_and_format(da_americana, "MAESTRA EL SALVADOR")
    #se obtiene el concatenado de municipio para obtener el grupo
    da_americana=set_concatenado_municipio(da_americana)
    #obtenermos el grupo de los pdv
    da_americana,gr=set_grupo(da_americana)
    #obtenemos precios
    da_americana,no_price=set_price_nor(da_americana,"Americana","Lista de Precios Depósitos","DEPOSITOS")
    da_americana.PRECIO.fillna(0, inplace=True)
    consolidado=get_consolidated_report_depositos_su(da_americana)
    consolidado.reset_index(level=0, inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    consolidado.to_excel("../salida/CONSOLIDADO_AMERICANA.xlsx")
    
    extra_data_cefa = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 2816, 'REF_CLIENTE': "Americana",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_cefa,"Americana",0,0)
    
    coloca.to_excel("../salida/reportes_americana_valorizada.xlsx")
    col=get_form_report_3_nor_depositos(consolidado,extra_data_cefa,0)
    col.to_excel("../salida/reporte 3 americanas.xlsx")

   
if len(sys.argv) >=2:
    get_americana(sys.argv[1],sys.argv[2],sys.argv[3])
else:        
    get_americana(91,"Abr 2019","201904")