# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 09:26:49 2019

@author: Juan
"""

import pandas as pd
from lib_process import *
#from evacuacion.lib_process import *
import sys, os, datetime



def crea_periodo(date):
    '''crea el periodo para que pueda encontrar los datos en las maestras,
    el formato ingresado debe ser el siguiente '2019-04-01'    '''
    periodo = datetime.datetime.strptime(date, '%Y-%m-%d')
    arg1 = "{0} {1}".format(settings.MESES[periodo.strftime('%b')], periodo.strftime('%y'))
    arg2 = "{0}{1}".format(periodo.strftime('%Y'), periodo.strftime('%m'))
    return arg1, arg2


def get_Carosa(orden,fecha,archivo_cliente,ruta,salida):
    '''obtiene reportes cliente carosa,
    parametros entrda:
        orden: numero de orden a generar
        fecha: fecha del mes a generar informe
        archivo_cliente: nombre del archivo del cliente
        ruta: ruta donde se encuentran las maestras
        salida:ruta de salida de los reportes generados
    '''    
    #genera las fechas necesarias
    fecha,formatofecha=crea_periodo(fecha)
    
    crea_ruta(ruta)
    #cargamos los datos del cliente
    da_carosa=get_data_all(archivo_cliente)
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
    

    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_Grupo Carosa.xlsx"))
    #consolidado.to_excel("{0}/CONSOLIDADO_Grupo Carosa.xlsx".format(salida))
    
    extra_data_cefa = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 9712, 'REF_CLIENTE': "Grupo Carosa",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_cefa,"Grupo Carosa",0,0)
    coloca['MES ORDEN']=coloca['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    coloca.to_excel(os.path.join(salida,"reportes_Grupo Carosa_valorizada.xlsx"))
    col=get_form_report_3_nor_depositos(consolidado,extra_data_cefa,0)
    col['MES ORDEN']=col['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    col.to_excel(os.path.join(salida,"reporte_3_Grupo_Carosa.xlsx"))
 
    
    
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
    
    
def get_elaguila(orden,fecha,archivo_cliente,ruta,salida):   
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
    ##se obtiene los datos del cliente
    da_aguila=get_data_all(archivo_cliente)
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
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_EL_AGUILA.xlsx"))
    #extradata necesaria para la valorizacion y segundo reporte
    extra_data_elaguila = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2839, 'REF_CLIENTE': "El Aguila",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte para mayoristas
    colocacion=get_form_report_mayorista(con, extra_data_elaguila, 'El Aguila',0,0)
    #se exporta el excel
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel(os.path.join(salida,"reportes_elaguila_valorizada.xlsx"))
    
def get_sanjose(orden,fecha,archivo_cliente,ruta,salida):
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
    ##se obtiene los datos del cliente
    da_sanjose=get_data_all(archivo_cliente)
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
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_SAN_JOSE.xlsx"))
    
    extra_data_sanjose = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2837, 'REF_CLIENTE': "San Jose",
                          'FLAG_CUA_BAS': ""
             }
    #se genera el reporte mayoristaa
    colocacion=get_form_report_mayorista(consolidado, extra_data_sanjose, 'San Jose',0,0)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel(os.path.join(salida,"reportes_SAN_JOSE_valorizada.xlsx"))


def get_lacefa(orden,fecha,archivo_cliente,ruta,salida):
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
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_CEFA.xlsx"))
    
    extra_data_cefa = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 2850, 'REF_CLIENTE': "Cefa",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_cefa,"Cefa",0,0)
    coloca['MES ORDEN']=coloca['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    coloca.to_excel(os.path.join(salida,"reportes_cefa_valorizada.xlsx"))
    col=get_form_report_3_nor_depositos(consolidado,extra_data_cefa,0)
    col['MES ORDEN']=col['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    col.to_excel(os.path.join(salida,"reporte 3 cefa.xlsx"))
    
    
def get_elpueblo(orden,fecha,archivo_cliente,ruta,salida):
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
    
    da_elpueblo=get_data_all(archivo_cliente)
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
    
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_ELPUEBLO.xlsx"))
    
    extra_data_elpueblo = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2834, 'REF_CLIENTE': "El Pueblo",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte para mayoristas
    colocacion=get_form_report_mayorista(consolidado, extra_data_elpueblo, 'El Pueblo',0,0)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel(os.path.join(salida,"reportes_elpueblo_valorizada.xlsx"))
    
    
def get_integral(orden,archivo_cliente,ruta,salida):
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
    #cargamos los datos del cliente
    da_integral=get_data_all(archivo_cliente)
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
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_Integral.xlsx"))
    
    extra_data_cefa = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 9715, 'REF_CLIENTE': "Integral",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_cefa,"Integral",0,0)
    coloca['MES ORDEN']=coloca['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    coloca.to_excel(os.path.join(salida,"reportes_Integral_valorizada.xlsx"))
    col=get_form_report_3_nor_depositos(consolidado,extra_data_cefa,0)
    col['MES ORDEN']=col['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    col.to_excel(os.path.join(salida,"reporte 3 Integral.xlsx"))
    
def get_jheral(orden,fecha,archivo_cliente,ruta,salida):
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
    ##se obtiene los datos del cliente
    da_jheral=get_data_all(archivo_cliente)
    ##sse organiza codgidos del cliente
    data_jheral=set_tq_codes_of_cli(da_jheral)
        #se limpia los descontinuados
    da_jheral=elimina_descontinuado(da_jheral)
    #se limpian las unidades
    da_jheral=elimina_unidades(da_jheral)
    dar=organiza_cod_tq_jheral(data_jheral)
    dar=set_concatenated_and_format(dar, "MAESTRA EL SALVADOR")
    dar=filter_u_codtq(dar)
    #se obtienen precios 
    dar,no_price=set_price_nor(dar,"Jheral Farma","Lista de Precios Mayoristas","MAYORISTAS")
    #se genera consolidado
    consolidado=get_consolidated_report_mayoristas(dar)
    #se organiza index y se elimina COD NEG
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_JHERAL.xlsx"))
    
    extra_data_jheral = {    'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2838, 'REF_CLIENTE': "Jheral Farma",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte
    colocacion=get_form_report_mayorista(con, extra_data_jheral, 'Jheral Farma',0,0)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel(os.path.join(salida,"reportes_jheral_valorizada.xlsx"))
    
    
def get_nuevosiglo(orden,archivo_cliente,ruta,salida):
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
    #cargamos los datos del cliente
    da_nuevosiglo=get_data_all(archivo_cliente)
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
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_Nuevo Siglo.xlsx"))
    
    extra_data_cefa = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 9715, 'REF_CLIENTE': "Nuevo Siglo",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_cefa,"Nuevo Siglo",0,0)
    coloca['MES ORDEN']=coloca['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    coloca.to_excel(os.path.join(salida,"reportes_Nuevo Siglo_valorizada.xlsx"))
    col=get_form_report_3_nor_depositos(consolidado,extra_data_cefa,0)
    col['MES ORDEN']=col['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    col.to_excel(os.path.join(salida,"reporte 3 Nuevo Siglo.xlsx"))


def get_lasalud(orden,fecha,archivo_cliente,ruta,salida):
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
    ##se obtiene los datos del cliente
    da_lasalud=get_data_all(archivo_cliente)
    ##sse organiza codgidos del cliente
    data_lasalud,nocodes,code=set_tq_codes2(da_lasalud,'La Salud','MAYORISTAS')
    #elimina los datos con descontinuado 
    data_lasalud=elimina_descontinuado(data_lasalud)
    #se limpian las unidades
    data_lasalud=elimina_unidades(data_lasalud)
    #organiza codigos TQ
    data_lasalud=organiza_cod_tq_salud(data_lasalud)
    #obtiene concatenado y formato
    data_lasalud=set_concatenated_and_format(data_lasalud, "MAESTRA EL SALVADOR")
    #obtiene precios nor 
    data_lasalud,no_price=set_price_nor(data_lasalud,"La Salud","Lista de Precios Mayoristas","MAYORISTAS")
    #obtiene el consoldidado
    consolidado=get_consolidated_report_mayoristas(data_lasalud)
    #elimina la columna cod nego y reorganiza el index
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    #se genera el excel del reporte
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_LA_SALUD.xlsx"))
    
    extra_data_lasalud = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2852, 'REF_CLIENTE': "La Salud",
                          'FLAG_CUA_BAS': ""
             }
    colocacion=get_form_report_mayorista(con, extra_data_lasalud, 'La Salud',0,0)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel(os.path.join(salida,"reportes_la_salud_valorizada.xlsx"))
    
def get_americana(orden,fecha,archivo_cliente,ruta,salida):
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
    #cargamos los datos del cliente
    da_americana=get_data_all(archivo_cliente)
    #limpiamos unidades en (0)
    da_americana=elimina_unidades(da_americana)
    #obtenemos codigos tq
    
    da_americana,nocode=set_tq_code(da_americana,'Americana','DEPOSITOS')
    #se eliminan los descontinuados 
    
    da_americana=elimina_descontinuado(da_americana)
    
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
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_AMERICANA.xlsx"))
    
    extra_data_cefa = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 2816, 'REF_CLIENTE': "Americana",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_cefa,"Americana",0,0)
    coloca['MES ORDEN']=coloca['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    coloca.to_excel(os.path.join(salida,"reportes_americana_valorizada.xlsx"))
    col=get_form_report_3_nor_depositos(consolidado,extra_data_cefa,0)
    col['MES ORDEN']=col['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    col.to_excel(os.path.join(salida,"reporte 3 americanas.xlsx"))
    
def get_laSantaLucia(orden,fecha,archivo_cliente,ruta,salida):
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
    #cargamos los datos del cliente
    da_santalucia=get_data_all(archivo_cliente)
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
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_Santa Lucia.xlsx"))
    
    extra_data_SantaLucia = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 2815, 'REF_CLIENTE': "Santa Lucia",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_SantaLucia,"Santa Lucia",0,1)
    coloca['MES ORDEN']=coloca['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    coloca.to_excel(os.path.join(salida,"reportes_Santa Lucia_valorizada.xlsx"))
    col=get_form_report_3_nor_depositos(consolidado,extra_data_SantaLucia,1)
    col['MES ORDEN']=col['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    col.to_excel(os.path.join(salida,"reporte 3 Santa Lucia.xlsx"))
    
def get_camila(orden,fecha,archivo_cliente,ruta,salida):
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
    ##se obtiene los datos del cliente
    da_camila=get_data_all(archivo_cliente)
    
    #da_camila.to_excel("salida/CONSOLIDADO_CAMILA12.xlsx")
    ##sse organiza codgidos del cliente
    data_camia,no_code,base2=set_tq_codes2(da_camila, "CAMILA",'CADENAS')    
    #se obtiene formato concatenado y codigo de negocio
    data_camila=set_concatenated_and_format(data_camia, "MAESTRA EL SALVADOR")
    #se limpian las unidades
    data_camila=elimina_unidades(data_camila)
    data_camila=elimina_descontinuado(data_camila)
    #se obtienen puntos de cod de puntos de venta
    data_camila=set_sellings_point_tq_code(data_camila, "CAMILA")
    #se obtienen precios 
    data_camila_pre,no_price=set_price_nor(data_camila,"FARMACIA CAMILA","Lista de Precios Cadenas","CADENAS")    
    #print(no_price['COD TQ'].unique())
    #se genera consolidado
    consolidado=get_consolidated_report_cadenas_su(data_camila_pre)
    #se organiza index y se elimina COD NEG
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True)     
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_CAMILA.xlsx"))
    extra_data_camila = {           'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 91,'CANAL': "91 Cadenas de Droguería", 'COD_CLIPADRE': 2848, 'REF_CLIENTE': "FARMACIA CAMILA",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte
    colocacion=get_form_report_NOR(con, extra_data_camila, 'FARMACIA CAMILA',0,0)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel(os.path.join(salida,"reportes_camila_valorizada.xlsx"))
    
    
def get_labuena(orden,archivo_cliente,ruta,salida):
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
    ##se obtiene los datos del cliente
    da_labuena=get_data_all(archivo_cliente)
    #se limpian las unidades
    da_labuena=elimina_unidades(da_labuena)
    ##sse organiza codgidos del cliente
    da_labuena,nocodes,code=set_tq_codes_str(da_labuena,'LA BUENA','CADENAS')
    #se limpian los descontinuados
    da_labuena=elimina_descontinuado(da_labuena)
    #se obtienen puntos de ventan para TQ
    da_labuena=set_sellings_point_tq_code(da_labuena,'LA BUENA')
    #se obtiene formato concatenado y codigo de negocio
    da_labuena=set_concatenated_and_format(da_labuena, "MAESTRA EL SALVADOR")
    #se obteniene los precios
    da_labuena,no_price=set_price_nor_aliados(da_labuena,"FARMACIA LA BUENA","Lista de Precios Cadenas","CADENAS")
    ##se generaa el consolidado
    consolidado=get_consolidated_report_cadenas_su(da_labuena)
    #Se resetea el index y se borra cod neg
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_LABUENA.xlsx"))
    extra_data_labuena = {      'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha,'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 91,'CANAL': "91 Cadenas de Dorguería", 'COD_CLIPADRE': 2843, 'REF_CLIENTE': "FARMACIA LA BUENA",
                              'FLAG_CUA_BAS': ""
                 }
    #se genera reporte de valorizacion nor
    colocacion=get_form_report_NOR(con, extra_data_labuena, 'FARMACIA LA BUENA',1,0)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel(os.path.join(salida,"reportes_la_buena_valorizada.xlsx"))
    
def get_lavida(orden,fecha,archivo_cliente,ruta,salida):
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
    ##se obtiene los datos del cliente
    da_lavida=get_data_all(archivo_cliente)
    #organiza tipod e datos la vida
    
    da_lavida=organiza_tipo_lavida(da_lavida)    
    
    #se limpian las unidades
    da_lavida=elimina_unidades(da_lavida)
    
    ##sse organiza codgidos del cliente
   
    data_lavida,nocode=set_tq_code_descripcion(da_lavida,"LA VIDA",'CADENAS')
    
    #se limpian descontinuados
    
    data_lavida=elimina_descontinuado(data_lavida)
    
    #se obtienen puntos de cod de puntos de venta
    data_lavida=set_sellings_point_tq_code_names(data_lavida,"LA VIDA")
    #se obtiene formato concatenado y codigo de negocio
    data_lavida=set_concatenated_and_format(data_lavida, "MAESTRA EL SALVADOR")
    #se obtienen precios 
    data_lavida,no_price=set_price_nor_aliados(data_lavida,"FARMACIA LA VIDA","Lista de Precios Cadenas","CADENAS")
    #se genera consolidado
    
    consolidado=get_consolidated_report_cadenas_su(data_lavida)
    #se organiza index y se elimina COD NEG
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True)     
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_LAVIDA.xlsx"))
    extra_data_lavida = { 'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 91,'CANAL': "91 Cadenas de Droguería", 'COD_CLIPADRE': 2844, 'REF_CLIENTE': "FARMACIA LA VIDA",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte
    
    colocacion=get_form_report_NOR(con, extra_data_lavida, 'FARMACIA LA VIDA',1,0)
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel(os.path.join(salida,"reportes_la_vida_valorizada.xlsx"))

def get_americas(orden,fecha,archivo_cliente,ruta,salida):
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
    ##se obtiene los datos del cliente
    las_americas=archivo_cliente
    data_lasamerica=get_data_all(las_americas)
    ##sse organiza codgidos del cliente
    data_lasamericas,no_code,code=set_tq_codes2(data_lasamerica, "LAS AMERICAS",'CADENAS')
    #se limpian descontinuados
    data_lasamericas=elimina_descontinuado(data_lasamericas)
    #se limpian unidades
    data_lasamericas=elimina_unidades(data_lasamericas)    
    #se obtiene formato concatenado y codigo de negocio
    data_lasamericas=set_concatenated_and_format(data_lasamericas, "MAESTRA EL SALVADOR")
    #se obtienen puntos de cod de puntos de venta
    data_lasamericas=set_sellings_point_tq_code(data_lasamericas, "LAS AMERICAS ")
    #se obtienen precios 
    data_lasamericas,noprice=set_price_hist(data_lasamericas,'FARMACIA LAS AMERICAS','CADENAS')
    
    #se genera consolidado
    consolidado=get_consolidated_report_cadenas_su(data_lasamericas)   
    
    #se organiza index y se elimina COD NEG
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True)
    consolidado.to_excel(os.path.join(salida,"CONSOLIDADO_LAS_AMERICAS.xlsx"))
    
    extra_data_america = { 'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                         'COD_CANAL': 92,'CANAL': "91 Cadenas de Droguería", 'COD_CLIPADRE': 9004, 'REF_CLIENTE': "FARMACIA LAS AMERICAS",
                          'FLAG_CUA_BAS': ""
             }
    #se obtiene reporte
    colocacion,resto=get_form_report(con, extra_data_america, 'FARMACIA LAS AMERICAS')
    colocacion['COD CANAL']=91
    colocacion['MES ORDEN']=colocacion['MES ORDEN'].str.strip().str.replace(' 20', '. ')
    colocacion.to_excel(os.path.join(salida,"reportes_las_americas_valorizada.xlsx"))