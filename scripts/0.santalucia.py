# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:32:33 2019

@author: Juan
"""

import pandas as pd
from lib_process import *
import sys 


def get_laSantaLucia(orden,fecha,formatofecha):
    #cargamos los datos del cliente
    da_santalucia=get_data_all("0. Santa Lucia.xlsx")
    #limpiamos unidades en (0)
    da_santalucia=elimina_unidades(da_santalucia)
    #obtenemos codigos tq
    
    da_santalucia,nocode=set_tq_code(da_santalucia,'Santa Lucia','DEPOSITOS')
    #se eliminan los descontinuados 
    
    da_santalucia=elimina_descontinuado(da_santalucia)
    #se obtienen concateado formato y cod de negocio
    
    
    da_santalucia=organiza_tq_santalucia2(da_santalucia)
    
    da_santalucia=set_concatenated_and_format(da_santalucia, "MAESTRA EL SALVADOR")
    #se obtiene el concatenado de municipio para obtener el grupo
    
    da_santalucia=set_concatenado_municipio(da_santalucia)
    #obtenermos el grupo de los pdv
    
    da_santalucia,gr=set_grupo(da_santalucia)
    #obtenemos precios
    
    da_santalucia,no_price=set_price_nor(da_santalucia,"Santa Lucia","Lista de Precios Depósitos","DEPOSITOS")
    
    da_santalucia=calculate_units_santalucia(da_santalucia)
    
    consolidado=get_consolidated_report_depositos(da_santalucia)
    consolidado.reset_index(level=0, inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    consolidado.to_excel("../salida/CONSOLIDADO_Santa Lucia.xlsx")
    
    extra_data_SantaLucia = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 2815, 'REF_CLIENTE': "Santa Lucia",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_SantaLucia,"Santa Lucia",0,1)
    coloca['MES ORDEN']=coloca['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    coloca.to_excel("../salida/reportes_Santa Lucia_valorizada.xlsx")
    col=get_form_report_3_nor_depositos(consolidado,extra_data_SantaLucia,1)
    col['MES ORDEN']=col['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    col.to_excel("../salida/reporte 3 Santa Lucia.xlsx")
    
    
if len(sys.argv) >=2:
    get_laSantaLucia(sys.argv[1],sys.argv[2],sys.argv[3])
else:   
    get_laSantaLucia(91,"Abr 2019","201904")