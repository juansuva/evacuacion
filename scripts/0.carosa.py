# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:38:22 2019

@author: Juan
"""


import pandas as pd
from lib_process import *
import sys


def get_Carosa(orden,fecha,formatofecha):
    #cargamos los datos del cliente
    da_carosa=get_data_all("0. Grupo Carosa.xlsx")
    #limpiamos unidades en (0)
    da_carosa=elimina_unidades(da_carosa)
    #obtenemos codigos tq
    da_carosa,nocode=set_tq_code(da_carosa,'Grupo Carosa','DEPOSITOS')
    #se eliminan los descontinuados 
    da_carosa=elimina_descontinuado(da_carosa)
    #se obtienen concateado formato y cod de negocio
    da_carosa=set_concatenated_and_format(da_carosa, "MAESTRA EL SALVADOR")
    #se obtiene el concatenado de municipio para obtener el grupo
    da_carosa=set_concatenado_municipio(da_carosa)
    #obtenermos el grupo de los pdv
    da_carosa,gr=set_grupo(da_carosa)
    #obtenemos precios
    da_carosa,no_price=set_price_nor(da_carosa,"Grupo Carosa","Lista de Precios Depósitos","DEPOSITOS")
    da_carosa.PRECIO.fillna(0, inplace=True)
    consolidado=get_consolidated_report_depositos_su(da_carosa)
    consolidado.reset_index(level=0, inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    consolidado.to_excel("../salida/CONSOLIDADO_Grupo Carosa.xlsx")
    
    extra_data_cefa = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 9712, 'REF_CLIENTE': "Grupo Carosa",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_cefa,"Grupo Carosa",0,0)
    coloca.to_excel("../salida/reportes_Grupo Carosa_valorizada.xlsx")
    col=get_form_report_3_nor_depositos(consolidado,extra_data_cefa,0)
    col.to_excel("../salida/reporte 3 Grupo Carosa.xlsx")
    
    

if len(sys.argv) >=2:
    get_Carosa(sys.argv[1],sys.argv[2],sys.argv[3])
else:
    
    get_Carosa(91,"Abr 2019","201904")