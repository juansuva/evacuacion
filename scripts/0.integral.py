# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:22:29 2019

@author: Juan
"""



import pandas as pd
from lib_process import *
import sys 

def get_integral(orden,fecha,formatofecha):
    #cargamos los datos del cliente
    da_integral=get_data_all("0. Integral.xlsx")
    #limpiamos unidades en (0)
    da_integral=elimina_unidades(da_integral)
    
    da_integral=organiza_tq_integral(da_integral)
    #obtenemos codigos tq
    da_integral,nocode=set_tq_code(da_integral,'Integral','DEPOSITOS')
    #se eliminan los descontinuados 
    da_integral=elimina_descontinuado(da_integral)
    #se obtienen concateado formato y cod de negocio
    da_integral=set_concatenated_and_format(da_integral, "MAESTRA EL SALVADOR")
    #se obtiene el concatenado de municipio para obtener el grupo
    da_integral=set_concatenado_municipio(da_integral)
    #obtenermos el grupo de los pdv
    da_integral,gr=set_grupo(da_integral)
    #obtenemos precios
    da_integral,no_price=set_price_nor(da_integral,"Integral","Lista de Precios Depósitos","DEPOSITOS")
    da_integral.PRECIO.fillna(0, inplace=True)
    consolidado=get_consolidated_report_depositos_su(da_integral)
    consolidado.reset_index(level=0, inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    consolidado.to_excel("../salida/CONSOLIDADO_Integral.xlsx")
    
    extra_data_cefa = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 9715, 'REF_CLIENTE': "Integral",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_cefa,"Integral",0,0)
    coloca.to_excel("../salida/reportes_Integral_valorizada.xlsx")
    col=get_form_report_3_nor_depositos(consolidado,extra_data_cefa,0)
    col.to_excel("../salida/reporte 3 Integral.xlsx")
    
    
print(len(sys.argv))    
if len(sys.argv) >=2:
    get_integral(sys.argv[1],sys.argv[2],sys.argv[3])
else:
    get_integral(91,"Abr 2019","201904")