# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:13:32 2019

@author: Juan
"""
import pandas as pd
from lib_process import *




def get_sanjose(orden,fecha,formatofecha):
    ##se obtiene los datos del cliente
    da_sanjose=get_data_all("0. San Jose.xlsx")
    ##sse organiza codgidos del cliente
    #se organiza datos con cod tq que no estan en la maestra
    data_tq=da_sanjose[da_sanjose['FORMATO']=='TQ']
    data_bonima=da_sanjose[da_sanjose['FORMATO']=='BONIMA']
    data_bonima=set_tq_codes_of_cli(data_bonima)
    data_tq,nocode,c=set_tq_codes2(data_tq,'San Jose','MAYORISTAS')
    #con=valida_codtq(data_tq,'San Jose','MAYORISTAS')
    #da_sanjose=organiza_cod_tq_sanjose(da_sanjose,con)    
    
    da_sanjose=data_tq.append(data_bonima)
     #se limpia los descontinuados    
    da_sanjose=elimina_descontinuado(da_sanjose)
    #se limpian las unidades
    da_sanjose=elimina_unidades(da_sanjose)
    
    #se obtienen los codigos de negocios
    da_sanjose=set_cod_neg(da_sanjose, "MAESTRA EL SALVADOR")
    #se obtiene precios de la base nor 
    da_sanjose,no_price=set_price_nor(da_sanjose,"San Jose","Lista de Precios Mayoristas","MAYORISTAS")
    #se genera el consolidado
    consolidado=get_consolidated_report_mayoristas(da_sanjose)
    #se resetea el index y se eliminan COD NEG
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    consolidado.to_excel("../salida/CONSOLIDADO_SAN_JOSE.xlsx")
    
    extra_data_sanjose = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2837, 'REF_CLIENTE': "San Jose",
                          'FLAG_CUA_BAS': ""
             }
    #se genera el reporte mayoristaa
    colocacion=get_form_report_mayorista(consolidado, extra_data_sanjose, 'San Jose',0,0)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel("../salida/reportes_SAN_JOSE_valorizada.xlsx")
    
if len(sys.argv) >=2:
    get_sanjose(sys.argv[1],sys.argv[2],sys.argv[3])
else: 
    get_sanjose(91,"Abr 2019","201904")