# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 11:01:37 2019

@author: Juan
"""
import pandas as pd
from lib_process import *
import sys 

def get_nuevosiglo(orden,fecha,formatofecha):
    #cargamos los datos del cliente
    da_nuevosiglo=get_data_all("0. Nuevo Siglo2.xlsx")
    #limpiamos unidades en (0)
    da_nuevosiglo=elimina_unidades(da_nuevosiglo)
    
    da_nuevosiglo=organiza_tq_nuevosiglo(da_nuevosiglo)
    #obtenemos codigos tq
    da_nuevosiglo,nocode=set_tq_code(da_nuevosiglo,'Nuevo Siglo','DEPOSITOS')
    #se eliminan los descontinuados 
    da_nuevosiglo=elimina_descontinuado(da_nuevosiglo)
    #se obtienen concateado formato y cod de negocio
    da_nuevosiglo=set_concatenated_and_format(da_nuevosiglo, "MAESTRA EL SALVADOR")
    #se obtiene el concatenado de municipio para obtener el grupo
    da_nuevosiglo=set_concatenado_municipio(da_nuevosiglo)
    #obtenermos el grupo de los pdv
    da_nuevosiglo,gr=set_grupo(da_nuevosiglo)
    #obtenemos precios
    da_nuevosiglo,no_price=set_price_nor(da_nuevosiglo,"Nuevo Siglo","Lista de Precios Depósitos","DEPOSITOS")
    da_nuevosiglo.PRECIO.fillna(0, inplace=True)
    consolidado=get_consolidated_report_depositos_su(da_nuevosiglo)
    consolidado.reset_index(level=0, inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    consolidado.to_excel("../salida/CONSOLIDADO_Nuevo Siglo.xlsx")
    
    extra_data_cefa = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 9715, 'REF_CLIENTE': "Nuevo Siglo",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_cefa,"Nuevo Siglo",0,0)
    coloca['MES ORDEN']=coloca['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    coloca.to_excel("../salida/reportes_Nuevo Siglo_valorizada.xlsx")
    col=get_form_report_3_nor_depositos(consolidado,extra_data_cefa,0)
    col['MES ORDEN']=col['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    col.to_excel("../salida/reporte 3 Nuevo Siglo.xlsx")
    
    
print(len(sys.argv))    
if len(sys.argv) >=2:
    get_nuevosiglo(sys.argv[1],sys.argv[2],sys.argv[3])
else:
    get_nuevosiglo(91,"Abr 2019","201904")
