# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 13:58:24 2019

@author: Juan
"""

import pandas as pd
#from lib_process import *
from evacuacion.lib_process import *
import sys, datetime 


def crea_periodo(date):
    '''crea el periodo para que pueda encontrar los datos en las maestras,
    el formato ingresado debe ser el siguiente '2019-04-01'    '''
    periodo = datetime.datetime.strptime(date, '%Y-%m-%d')
    arg1 = "{0} {1}".format(settings.MESES[periodo.strftime('%b')], periodo.strftime('%Y'))
    arg2 = "{0}{1}".format(periodo.strftime('%Y'), periodo.strftime('%m'))
    return arg1, arg2


def get_lacefa(orden,fecha,archivo_cliente):
    fecha,formatofecha=crea_periodo(fecha)
    #cargamos los datos del cliente
    da_cefa=get_data_all(archivo_cliente)
    #limpiamos unidades en (0)
    da_cefa=elimina_unidades(da_cefa)
    #obtenemos codigos tq
    da_cefa,nocode,c=set_tq_codes2(da_cefa,'Cefa','DEPOSITOS')
    #se eliminan los descontinuados 
    da_cefa=elimina_descontinuado(da_cefa)
    #se obtienen concateado formato y cod de negocio
    da_cefa=set_concatenated_and_format(da_cefa, "MAESTRA EL SALVADOR")
    #se obtiene el concatenado de municipio para obtener el grupo
    da_cefa=set_concatenado_municipio(da_cefa)
    #obtenermos el grupo de los pdv
    da_cefa,gr=set_grupo(da_cefa)
    #obtenemos precios
    da_cefa,no_price=set_price_nor(da_cefa,"Cefa","Lista de Precios Depósitos","DEPOSITOS")
    consolidado=get_consolidated_report_depositos_su(da_cefa)
    consolidado.reset_index(level=0, inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    consolidado.to_excel("{0}/CONSOLIDADO_CEFA.xlsx".format(settings.ROUTE_OUTPUT_FILES))
    
    extra_data_cefa = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 2850, 'REF_CLIENTE': "Cefa",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_cefa,"Cefa",0,0)
    coloca['MES ORDEN']=coloca['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    coloca.to_excel("{0}/reportes_cefa_valorizada.xlsx".format(settings.ROUTE_OUTPUT_FILES))
    col=get_form_report_3_nor_depositos(consolidado,extra_data_cefa,0)
    col['MES ORDEN']=col['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    col.to_excel("{0}/reporte 3 cefa.xlsx".format(settings.ROUTE_OUTPUT_FILES))
    
    
if len(sys.argv) >=2:
    get_lacefa(sys.argv[1],sys.argv[2],sys.argv[3])
else:   
    get_lacefa(91,"2019-04-01","0. Cefa.xlsx")