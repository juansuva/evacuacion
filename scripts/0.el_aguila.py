# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:28:11 2019

@author: Juan
"""

import pandas as pd
from lib_process import *

def get_elaguila(orden,fecha,formatofecha):
    ##se obtiene los datos del cliente
    da_aguila=get_data_all("0. El Aguila.xlsx")
    ##sse organiza codgidos del cliente
    da_aguila=organiza_cod_tq_aguila(da_aguila)
    #obtiene el resto de codigo de tq
    data_elaguila=set_tq_codes_of_cli(da_aguila)
    #se limpian las unidades
    data_elaguila=elimina_unidades(data_elaguila)
    #se limpia los descontinuados
    data_elaguila=elimina_descontinuado(data_elaguila)
    #se obtiene formato concatenado y codigo de negocio
    data_elaguila=set_concatenated_and_format(data_elaguila, "MAESTRA EL SALVADOR")
    ##se obtiene precios
    data_elaguila,no_price=set_price_nor(data_elaguila,"El Aguila","Lista de Precios Mayoristas","MAYORISTAS")
    ##se genera el consolidado
    consolidado=get_consolidated_report_mayoristas(data_elaguila)
    #se organiza index y se elimina COD NEG
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True)
    #se genera el excel con el consoldiado
    consolidado.to_excel("../salida/CONSOLIDADO_EL_AGUILA.xlsx")
    #extradata necesaria para la valorizacion y segundo reporte
    extra_data_elaguila = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2839, 'REF_CLIENTE': "El Aguila",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte para mayoristas
    colocacion=get_form_report_mayorista(con, extra_data_elaguila, 'El Aguila',0,0)
    #se exporta el excel
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel("../salida/reportes_elaguila_valorizada.xlsx")

if len(sys.argv) >=2:
    get_elaguila(sys.argv[1],sys.argv[2],sys.argv[3])
else:
    

    get_elaguila(91,"Abr 2019","201904")