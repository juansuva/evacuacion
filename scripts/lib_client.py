#from django.conf import settings
import pandas as pd
from lib_process import *
import re

inputPath = r'C:\Users\Juan\Desktop\Data'
inputFileData = 'Maestra Articulos CAM Reconstruida Ene 2018.xlsx'
inputFileDataCliente='0. Camila.xlsx'
inputPathMaestras = r'C:\Users\Juan\Desktop\Data\Info'
inputMaestraArticulos = 'Codigos Articulos Cliente - TQ.xlsx'
inputMaestraCodigosPDV = 'Codigos PDV Cliente - TQ.xlsx'
inputMaestraPrecios='Lista Precios Salvador Trim I 2019.xlsx'
inputMaestraVentaInventSalvador="Venta e Inventario Salvador Febrero.xlsx"

inputPathMaestras2 = r'C:\Users\Juan\Desktop\Data\EVACUACION_INTERNAL\Entradas'


def get_data_brasil():
    """
    Conversion de los datos provenientes de archivo excel para el cliente Brasil
    de Salvador en DataFrame.

    Parameters:


    Returns:
        DataFrame datos: Datos del cliente Brasil con las columnas: 
                    [
                        'CODIGO', 'DESCRIPCION', 'PDV', 'TIPO', 'VTA_INV', 'UNIDADES'
                    ]
    """
    # cargue de archivos de inventario y ventas.
    venta = pd.read_excel("{}/{}".format(inputPathMaestras, '0. Brasil.xlsx'), sheet_name='VTA')
    inventario = pd.read_excel("{}/{}".format(inputPathMaestras, '0. Brasil.xlsx'),
                                sheet_name='INV', header=[0, 1])

    # Se eliminan las columnas innecesarias y se renombran para normalizar ambas tablas
    inventario.drop(["ID", "LAB", "RUBRO", "TOTAL"], axis=1, level=0, inplace=True)
    inventario.drop("PROMEDIO", axis=1, level=1, inplace=True)
    if 'N' in inventario.columns:
        inventario.drop("N", axis=1, level=0, inplace=True)

    venta.drop(['CODIGO EMPLEADO', 'NOMBRE EMPLEADO', 'TOTAL S/IVA'], axis=1, inplace=True)
    venta.rename(columns={"SALA": "PDV", "CAJAS COMPLETAS": "SALDO", "UNIDADES": "FRACCION"}, inplace=True)

    # Se lleva las columnas a un solo nivel
    inventario.columns = ["%s%s" % (
        a, " %s" % b if "Unnamed" not in b else "") for a, b in inventario.columns]

    # Se pasa los saldos y fraccion de cada punto de ventas, de columnas a filas.
    inventario = inventario.melt(id_vars=['CODIGO', 'DESCRIPCION'], var_name='TIPO')
    inventario[['PDV', 'TIPO']] = inventario['TIPO'].str.split(' ', expand=True)

    venta = venta.melt(id_vars=['CODIGO', 'DESCRIPCION', 'PDV'], var_name='TIPO')

    # Se marcan los datos como inventario y venta
    inventario["VTA_INV"] = "INV"
    venta["VTA_INV"] = "VTA"

    # Se consolidan ambas tablas y se limpian las filas con unidades en cero
    datos = venta.append(inventario)
    datos = datos[datos["value"] != 0]
    datos.rename(columns={"value": "UNIDADES"}, inplace=True)
    print (datos.columns)
    print (datos.head())

    return datos

def get_data_san_benito():
    """
    Conversion de los datos provenientes de archivo excel para el cliente Brasil
    de Salvador en DataFrame.

    Parameters:


    Returns:
        DataFrame datos: Datos del cliente Brasil con las columnas: 
                    [
                        'CODIGO', 'DESCRIPCION', 'PDV', 'TIPO', 'VTA_INV', 'UNIDADES'
                    ]
    """
    # Cargo del archivo del cliente
    venta = pd.read_excel("{}\{}".format(inputPathMaestras, '0. San Benito.xlsx'),
                                sheet_name='VTA', header=1)
    inventario = pd.read_excel("{}\{}".format(inputPathMaestras, '0. San Benito.xlsx'),
                                sheet_name='INV', header = 1)
    print(inventario.columns)
    
    ### Se elimina las columnas que no son necesarios
    inventario.reset_index(level=0, inplace=True)
    print(inventario.columns)
    inventario = inventario[inventario["Unnamed: 1"].notna()]
    inventario = inventario[inventario["Unnamed: 1"] != "REPORTE DE EXISTECIAS "]
    inventario.drop("Total", axis=1, inplace=True)
    inventario.rename(columns={'Unnamed: 1': "DESCRIPCION"}, inplace=True)

    ### Paso los puntos de venta de columnas a filas
    inventario = inventario.melt(id_vars=['DESCRIPCION'], var_name='PDV')
    inventario["VTA_INV"] = "INV"

    ### Limpieza de las columnas que no son necesarias
    venta.index = venta.index.astype(str).str.upper()
    print(venta.columns)
    venta = venta[:"Total"][:-1]
    venta.reset_index(level=0, inplace=True)
    venta.rename(columns={'index': "DESCRIPCION"}, inplace=True)
    venta["DESCRIPCION"] = venta["DESCRIPCION"].fillna(method="ffill")
    venta = venta.groupby("DESCRIPCION").last().reset_index()
    venta.drop("Total", axis=1, inplace=True)
    ### Conversion de filas a columnas
    venta = venta.melt(id_vars=['DESCRIPCION'], var_name='PDV')
    venta["VTA_INV"] = "VTA"

    ## Resultado
    datos = venta.append(inventario)
    datos["DESCRIPCION"] = datos["DESCRIPCION"].str.strip().str.upper()
    ### Se elimina los articulos que no tienen unidades
    datos = datos[datos["value"] != 0]
    datos.rename(columns={"value": "UNIDADES"}, inplace=True)
    datos["CODIGO"] = None
    print (datos.columns)
    print (datos)
    return datos


def get_data_camila(orden,fecha,formatofecha):
    """
    Conversion de los datos provenientes de archivo excel para el cliente Camila
    de Salvador en DataFrame.

    Parameters:


    Returns:
        DataFrame datos: Datos del cliente Brasil con las columnas: 
                    [
                        'CODIGO', 'DESCRIPCION', 'PDV', 'TIPO', 'VTA_INV', 'UNIDADES'
                    ]
    """  
    
    # Cargo del archivo del cliente
    
    venta= pd.read_excel("{}\{}".format(inputPathMaestras,'0. Camila.xlsx'), sheet_name='VTA', header=0)
    inventario=pd.read_excel("{}\{}".format(inputPathMaestras, '0. Camila.xlsx'), sheet_name='INV', header=6)
    venta.drop(['ENVASE', 'LAB', 'BONO','TOTAL BONO','MONTO','DEPENDIENTE','IDVENDEDOR','FECHA'], axis=1, inplace=True)
    venta.rename(columns={"SUCURSAL": "PDV", "IDITEM": "CODIGO", "VENTA": "UNIDADES"}, inplace=True)
    inventario=inventario.drop(columns="TOTAL")
    venta["VTA_INV"]="VTA"
    inventario["VTA_INV"]="INV"
    
    
    inventario.rename(columns = { 'Unnamed: 0': 'DESCRIPCION' }, inplace = True)
    inventario = inventario.melt(id_vars=['DESCRIPCION','VTA_INV'], var_name='PDV')
    venta["TIPO"]="SALDO"
    inventario["TIPO"]="SALDO"
    inventario["CODIGO"]=None
    #inventario=inventario.drop(columns="TOTAL")
    inventario.rename(columns = { 'value': 'UNIDADES' }, inplace = True)
    inventario=inventario[pd.notnull(inventario['UNIDADES'])]
    inventario=inventario[(inventario['UNIDADES'] !=  0)]
    inventario=inventario[(inventario['UNIDADES']  >  0.000001)]
    
    datos = venta.append(inventario)
    
    
    
    return datos




    
def get_americas(orden,fecha,formatofecha):
    las_americas="0. Las Americas.xlsx"
    data_lasamerica=get_data_all(las_americas)
    data_lasamericas,no_code,code=set_tq_codes2(data_lasamerica, "LAS AMERICAS",'CADENAS')
    #data_lasamericas.to_excel("este.xlsx")
    data_lasamericas=set_concatenated_and_format(data_lasamericas, "MAESTRA EL SALVADOR")
    data_lasamericas=set_sellings_point_tq_code(data_lasamericas, "LAS AMERICAS ")
    data_lasamericas,noprice=set_price_hist(data_lasamericas,'FARMACIA LAS AMERICAS','CADENAS')
    
    
    consolidado=get_consolidated_report_cadenas_su(data_lasamericas)
    
    extra_data_america = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                         'COD_CANAL': 92,'CANAL': "91 Cadenas de Dorguería", 'COD_CLIPADRE': 9004, 'REF_CLIENTE': "FARMACIA LAS AMERICAS",
                          'FLAG_CUA_BAS': ""
             }
    
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True)
    consolidado.to_excel("CONSOLIDADO_LAS_AMERICAS.xlsx")
    colocacion,resto=get_form_report(con, extra_data_america, 'FARMACIA LAS AMERICAS')
    colocacion.to_excel("reportes_las_americas_valorizada.xlsx")

def get_camila(orden,fecha,formatofecha):
    da_camila=get_data_all("0. Camila.xlsx")
    
    #da_camila.to_excel("CONSOLIDADO_CAMILA12.xlsx")
    data_camia,no_code,base2=set_tq_codes2(da_camila, "CAMILA",'CADENAS')    
    
    data_camila=set_concatenated_and_format(data_camia, "MAESTRA EL SALVADOR")
    data_camila=elimina_unidades(data_camila)
    data_camila=elimina_descontinuado(data_camila)
    data_camila=set_sellings_point_tq_code(data_camila, "CAMILA")
    data_camila_pre,no_price=set_price_nor(data_camila,"FARMACIA CAMILA","Lista de Precios Cadenas","CADENAS")    
    #print(no_price['COD TQ'].unique())
    consolidado=get_consolidated_report_cadenas_su(data_camila_pre)
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True)     
    consolidado.to_excel("CONSOLIDADO_CAMILA.xlsx")
    extra_data_camila = {           'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 91,'CANAL': "91 Cadenas de Dorguería", 'COD_CLIPADRE': 2848, 'REF_CLIENTE': "FARMACIA CAMILA",
                          'FLAG_CUA_BAS': ""
             }
    
    colocacion=get_form_report_NOR(con, extra_data_camila, 'FARMACIA CAMILA',0,0)
    colocacion.to_excel("reportes_camila_valorizada.xlsx")

def get_jheral(orden,fecha,formatofecha):

    da_jheral=get_data_all("0. Jheral Farma.xlsx")
    data_jheral=set_tq_codes_of_cli(da_jheral)
    dar=organiza_cod_tq_jheral(data_jheral)
    dar=set_concatenated_and_format(dar, "MAESTRA EL SALVADOR")
    dar=filter_u_codtq(dar)
    dar,no_price=set_price_nor(dar,"Jheral Farma","Lista de Precios Mayoristas","MAYORISTAS")
    consolidado=get_consolidated_report_mayoristas(dar)
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    
    consolidado.to_excel("CONSOLIDADO_JHERAL.xlsx")
    
    extra_data_jheral = {    'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2838, 'REF_CLIENTE': "Jheral Farma",
                          'FLAG_CUA_BAS': ""
             }
    colocacion=get_form_report_mayorista(consolidado, extra_data_jheral, 'Jheral Farma',0,0)
    colocacion.to_excel("reportes_jheral_valorizada.xlsx")


def get_elpueblo(orden,fecha,formatofecha):
    da_elpueblo=get_data_all("0. El Pueblo.xlsx")
    data_elpubelo,nocodes=set_tq_codes_onlytq(da_elpueblo,'MAYORISTAS')
    data_elpubelo=set_concatenated_and_format(data_elpubelo, "MAESTRA EL SALVADOR")
    data_elpubelo,no_price=set_price_nor(data_elpubelo,"El Pueblo","Lista de Precios Mayoristas","MAYORISTAS")
    consolidado=get_consolidated_report_mayoristas(data_elpubelo)
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    
    consolidado.to_excel("CONSOLIDADO_ELPUEBLO.xlsx")
    
    extra_data_elpueblo = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2834, 'REF_CLIENTE': "El Pueblo",
                          'FLAG_CUA_BAS': ""
             }
    colocacion=get_form_report_mayorista(consolidado, extra_data_elpueblo, 'El Pueblo',0,0)
    colocacion.to_excel("reportes_elpueblo_valorizada.xlsx")


def get_lasalud(orden,fecha,formatofecha):
    da_lasalud=get_data_all("0. La Salud.xlsx")
    data_lasalud,nocodes,code=set_tq_codes2(da_lasalud,'La Salud','MAYORISTAS')
    
    data_lasalud=organiza_cod_tq_salud(data_lasalud)
    data_lasalud=set_concatenated_and_format(data_lasalud, "MAESTRA EL SALVADOR")
    data_lasalud,no_price=set_price_nor(data_lasalud,"La Salud","Lista de Precios Mayoristas","MAYORISTAS")
    consolidado=get_consolidated_report_mayoristas(data_lasalud)
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    consolidado.to_excel("CONSOLIDADO_LA_SALUD.xlsx")
    
    extra_data_salud = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2852, 'REF_CLIENTE': "La Salud",
                          'FLAG_CUA_BAS': ""
             }
    colocacion=get_form_report_mayorista(con, extra_data_salud, 'La Salud',0,0)
    colocacion.to_excel("reportes_la_salud_valorizada.xlsx")



def get_elaguila(orden,fecha,formatofecha):
    da_aguila=get_data_all("0. El Aguila.xlsx")
    da_aguila=organiza_cod_tq_aguila(da_aguila)
    da_aguila=elimina_unidades(da_aguila)
    data_elaguila=set_tq_codes_of_cli(da_aguila)
    data_elaguila=set_concatenated_and_format(data_elaguila, "MAESTRA EL SALVADOR")
    data_elaguila,no_price=set_price_nor(data_elaguila,"El Aguila","Lista de Precios Mayoristas","MAYORISTAS")
    
    consolidado=get_consolidated_report_mayoristas(data_elaguila)
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    consolidado.to_excel("CONSOLIDADO_EL_AGUILA.xlsx")
    
    extra_data_elaguila = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2839, 'REF_CLIENTE': "El Aguila",
                          'FLAG_CUA_BAS': ""
             }
    colocacion=get_form_report_mayorista(consolidado, extra_data_elaguila, 'El Aguila',0,0)
    colocacion.to_excel("reportes_elaguila_valorizada.xlsx")


def get_lavida(orden,fecha,formatofecha):
    da_lavida=get_data_all("0. La Vida.xlsx")
    da_lavida=organiza_tipo_lavida(da_lavida)    
    da_lavida=elimina_unidades(da_lavida)
    data_lavida,nocode=set_tq_code_descripcion(da_lavida,"LA VIDA",'MAYORISTAS')
    data_lavida=elimina_descontinuado(data_lavida)
    data_lavida=set_sellings_point_tq_code_names(data_lavida,"LA VIDA")
    data_lavida=set_concatenated_and_format(data_lavida, "MAESTRA EL SALVADOR")
    data_lavida,no_price=set_price_nor_aliados(data_lavida,"FARMACIA LA VIDA","Lista de Precios Cadenas","CADENAS")
    consolidado=get_consolidated_report_cadenas_su(data_lavida)
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True)     
    consolidado.to_excel("CONSOLIDADO_LAVIDA.xlsx")
    extra_data_lavida = { 'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 91,'CANAL': "91 Cadenas de Dorguería", 'COD_CLIPADRE': 2844, 'REF_CLIENTE': "FARMACIA LA VIDA",
                          'FLAG_CUA_BAS': ""
             }
    colocacion=get_form_report_NOR(con, extra_data_lavida, 'FARMACIA LA VIDA',1,0)
    colocacion.to_excel("reportes_la_vida_valorizada.xlsx")


def get_launo(orden,fecha,formatofecha):
    da_launo=get_data_all("0. La Uno.xlsx")
    da_launo,nocodes,code=set_tq_codes_str(da_launo,'LA UNO','CADENAS')
    da_launo=elimina_unidades(da_launo)
    da_launo=elimina_descontinuado(da_launo)
    da_launo=set_sellings_point_tq_code_names(da_launo,'UNO ')
    da_launo=set_concatenated_and_format(da_launo, "MAESTRA EL SALVADOR")
    da_launo,no_price=set_price_nor(da_launo,"FARMACIA UNO","Lista de Precios Cadenas","CADENAS")
    da_launo=calculate_units_s(da_launo,"LA UNO")
    consolidado=get_consolidated_report_cadenas(da_launo)
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    
    consolidado.to_excel("CONSOLIDADO_UNO.xlsx")
    extra_data_launo = { 'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 91,'CANAL': "91 Cadenas de Dorguería", 'COD_CLIPADRE': 2851, 'REF_CLIENTE': "FARMACIA UNO",
                          'FLAG_CUA_BAS': ""
             }

    colocacion=get_form_report_NOR(con, extra_data_launo, 'FARMACIA UNO',0,1)
    colocacion.to_excel("reportes_la_uno_valorizada.xlsx")



def get_labuena(orden,fecha,formatofecha):
    da_labuena=get_data_all("0. La Buena.xlsx")
    da_labuena=elimina_unidades(da_labuena)
    da_labuena,nocodes,code=set_tq_codes_str(da_labuena,'LA BUENA','CADENAS')
    da_labuena=elimina_descontinuado(da_labuena)
    da_labuena=set_sellings_point_tq_code(da_labuena,'LA BUENA')
    da_labuena=set_concatenated_and_format(da_labuena, "MAESTRA EL SALVADOR")
    da_labuena,no_price=set_price_nor_aliados(da_labuena,"FARMACIA LA BUENA","Lista de Precios Cadenas","CADENAS")
    consolidado=get_consolidated_report_cadenas_su(da_labuena)
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    
    consolidado.to_excel("CONSOLIDADO_LABUENA.xlsx")
    extra_data_labuena = {      'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha,'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 91,'CANAL': "91 Cadenas de Dorguería", 'COD_CLIPADRE': 2843, 'REF_CLIENTE': "FARMACIA LA BUENA",
                              'FLAG_CUA_BAS': ""
                 }
    
    colocacion=get_form_report_NOR(con, extra_data_labuena, 'FARMACIA LA BUENA',1,0)
    colocacion.to_excel("reportes_la_buena_valorizada.xlsx")




def get_sanjose(orden,fecha,formatofecha):

    da_sanjose=get_data_all("0. San Jose.xlsx")
    da_sanjose=set_tq_codes_of_cli(da_sanjose)
    da_sanjose=elimina_descontinuado(da_sanjose)
    da_sanjose=elimina_unidades(da_sanjose)
    da_sanjose=set_cod_neg(da_sanjose, "MAESTRA EL SALVADOR")
    da_sanjose,no_price=set_price_nor(da_sanjose,"San Jose","Lista de Precios Mayoristas","MAYORISTAS")
    consolidado=get_consolidated_report_mayoristas(da_sanjose)
    consolidado.reset_index(inplace=True)
    consolidado.drop("index", axis=1, inplace=True)
    con=consolidado
    consolidado.drop("COD NEG", axis=1, inplace=True) 
    consolidado.to_excel("CONSOLIDADO_SAN_JOSE.xlsx")
    
    extra_data_sanjose = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                          'COD_CANAL': 97,'CANAL': "97 Mayoristas", 'COD_CLIPADRE': 2837, 'REF_CLIENTE': "San Jose",
                          'FLAG_CUA_BAS': ""
             }
    colocacion=get_form_report_mayorista(consolidado, extra_data_sanjose, 'El Aguila',0,0)
    colocacion.to_excel("reportes_SAN_JOSE_valorizada.xlsx")


def get_lacefa(orden,fecha,formatofecha):
    da_cefa=get_data_all("0. Cefa.xlsx")
    da_cefa=elimina_unidades(da_cefa)
    da_cefa,nocode,c=set_tq_codes2(da_cefa,'Cefa','DEPOSITOS')
    da_cefa=elimina_descontinuado(da_cefa)
    da_cefa=set_concatenated_and_format(da_cefa, "MAESTRA EL SALVADOR")
    da_cefa=set_concatenado_municipio(da_cefa)
    da_cefa,gr=set_grupo(da_cefa)
    da_cefa,no_price=set_price_nor(da_cefa,"Cefa","Lista de Precios Depósitos","DEPOSITOS")
    consolidado=get_consolidated_report_depositos_su(da_cefa)
    consolidado.reset_index(level=0, inplace=True)
    consolidado.to_excel("CONSOLIDADO_CEFA.xlsx")
    
    extra_data_cefa = {            'ORDEN': orden, 'MES_ORDEN': fecha, 'FORMATO_FECHA': formatofecha, 'COD_PAIS': 41, 'PAIS': "41 SALVADOR",
                              'COD_CANAL': 92,'CANAL': "92 Depositos", 'COD_CLIPADRE': 2850, 'REF_CLIENTE': "Cefa",
                              'FLAG_CUA_BAS': ""
                 }
    coloca=get_form_report_NOR_depositos(consolidado,extra_data_cefa,"Cefa",0,0)
    coloca.to_excel("reportes_cefa_valorizada.xlsx")
    col=get_form_report_3_nor_depositos(consolidado,extra_data_cefa,0)
    col.to_excel("reporte 3 cefa.xlsx")
    
'''
get_lacefa(91,"Abr 2019","201904")
get_jheral(91,"Abr 2019","201904")
#get_americas(89,"Feb 2019","201902")
get_elaguila(91,"Abr 2019","201904")
get_lasalud(91,"Abr 2019","201904")
get_elpueblo(91,"Abr 2019","201904")
#get_camila(89,"Feb 2019","201902")
#get_lavida(89,"Feb 2019","201902")
#get_launo(89,"Feb 2019","201902")
#get_labuena(89,"Feb 2019","201902")
get_sanjose(91,"Abr 2019","201904")
    
'''

#BUSQUEDA CON EXPRECIONES REGULARES
#co=colocacion[colocacion['ARTÍCULO'].str.contains('TAB$', regex=True)]
#co['ARTÍCULO']=co['ARTÍCULO'].str[:-3]




    
   

