# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 08:28:16 2019

@author: Juan
"""

import pandas as pd
from lib_process import *

def get_elpueblo(orden,fecha,formatofecha):
    da_elpueblo=get_data_all("0. El Pueblo.xlsx")
    data_elpubelo,nocodes=set_tq_codes_onlytq(da_elpueblo,'MAYORISTAS')
        #se limpia los descontinuados
    data_elpubelo=elimina_descontinuado(data_elpubelo)
    #se limpian las unidades
    data_elpubelo=elimina_unidades(data_elpubelo)
    #se obtiene formato concatenado y codigo de negocio
    data_elpubelo=set_concatenated_and_format(data_elpubelo, "MAESTRA EL SALVADOR")
    #se obtienen precios 
    data_elpubelo,no_price=set_price_nor(data_elpubelo,"El Pueblo","Lista de Precios Mayoristas","MAYORISTAS")
    #se genera consolidado
    consolidado=get_consolidated_report_mayoristas(data_elpubelo)
    #se organiza index y se elimina COD NEG
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    
    consolidado.to_excel("../salida/CONSOLIDADO_ELPUEBLO.xlsx")
    
    extra_data_elpueblo = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2834, 'REF_CLIENTE': "El Pueblo",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte para mayoristas
    colocacion=get_form_report_mayorista(consolidado, extra_data_elpueblo, 'El Pueblo',0,0)
    colocacion.to_excel("../salida/reportes_elpueblo_valorizada.xlsx")
    
get_elpueblo(91,"Abr 2019","201904")