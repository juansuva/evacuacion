# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 11:53:13 2019

@author: Juan
"""

import pandas as pd
from lib_process import *
from evacuacion.lib_process import *
import sys, os, datetime


def crea_periodo(date):
    '''crea el periodo para que pueda encontrar los datos en las maestras,
    el formato ingresado debe ser el siguiente '2019-04-01'    '''
    periodo = datetime.datetime.strptime(date, '%Y-%m-%d')
    arg1 = "{0} {1}".format(settings.MESES[periodo.strftime('%b')], periodo.strftime('%y'))
    arg2 = "{0}{1}".format(periodo.strftime('%Y'), periodo.strftime('%m'))
    return arg1, arg2


def get_launo(orden,fecha,archivo_cliente,ruta,salida):
    '''
    parametros entrda:
        orden: numero de orden a generar
        fecha: fecha del mes a generar informe
        archivo_cliente: nombre del archivo del cliente
        ruta: ruta donde se encuentran las maestras
        salida:ruta de salida de los reportes generados
    '''    
    #genera las fechas necesarias
    fecha,formatofecha=crea_periodo(fecha)
    ##se obtiene los datos del cliente
    crea_ruta(ruta)
    da_launo=get_data_all(archivo_cliente)
    ##sse organiza codgidos del cliente
    da_launo,nocodes,code=set_tq_codes_str(da_launo,'LA UNO','CADENAS')
    #se limpian las unidades
    da_launo=elimina_unidades(da_launo)
    #se limpia los descontinuados
    da_launo=elimina_descontinuado(da_launo)
    #se obtienen Cod de  puntos de ventas para TQ
    da_launo=set_sellings_point_tq_code_names(da_launo,'UNO ')
    #se obtiene concatenado formato y cod de neg
    da_launo=set_concatenated_and_format(da_launo, "MAESTRA EL SALVADOR")
    #se obtienen precios
    da_launo,no_price=set_price_nor(da_launo,"FARMACIA UNO","Lista de Precios Cadenas","CADENAS")
    #como el cliente blitea se organizan las unidades
    da_launo=calculate_units_s(da_launo,"LA UNO")
    #se genera el consolidado
    consolidado=get_consolidated_report_cadenas(da_launo)
    #se reset el index y se borra cod neg
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_UNO.xlsx"))
    extra_data_launo = { 'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 91,'CANAL': "91 Cadenas de Droguería", 'COD_CLIPADRE': 2851, 'REF_CLIENTE': "FARMACIA UNO",
                          'FLAG_CUA_BAS': ""
             }
    #se genera reporte de valorizacion nor 
    colocacion=get_form_report_NOR(con, extra_data_launo, 'FARMACIA UNO',0,1)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel(os.path.join(salida,"reportes_la_uno_valorizada.xlsx"))
    
    
 launo= get_launo(89,"2019-02-01","0. La Uno.xlsx",settings.ROUTE_INPUT_FILES,settings.ROUTE_OUTPUT_FILES)