import pandas as pd
import numpy as np

import os 
ruta=os.getcwd()
#from django.conf import settings

##ruta dinamica para django 
#inputPathMaestras = settings.ROUTE_INPUT_FILES
ruta=ruta+'\..\Entradas'

##ruta de las entradas en esta carpeta se encuentra tanto como datos del cliente, como las maestras necesarias para la ejecucion
inputPathMaestras = ruta



##sele
lp_hist=0
tipo_suc=0 ##tipo de sucursal se esta manejando 1 CADENAS 2 MAYORISTAS 3 DEPOSITO
def load_price_hist(tipo, lp_hist=lp_hist,):
    '''funcion que carga la lista de precios historica'''
    global load_hist,tipo_suc
    
    if  load_hist==0:
        if tipo == 1:            
            lp_hist = pd.read_excel("{}/{}".format(inputPathMaestras, "Lista de Precios historico - Salvador.xlsx"),sheet_name="CADENAS", header=0)
            load_hist=1
            tipo_suc=1
        elif tipo == 2:
            lp_hist = pd.read_excel("{}/{}".format(inputPathMaestras, "Lista de Precios historico - Salvador.xlsx"),sheet_name="MAYORISTAS", header=0)
            load_hist=1
            tipo_suc=2
        elif tipo == 3:
            lp_hist = pd.read_excel("{}/{}".format(inputPathMaestras, "Lista de Precios historico - Salvador.xlsx"),sheet_name="DEPOSITO", header=0)
            load_hist=1
            tipo_suc=3
    elif tipo != tipo_suc:
        load_hist=0
        load_price_hist(tipo)
        
        
def get_data_all(cliente):
    """Conversion de los datos provenientes de archivo excel para cualquier cliente

    Parameters:
        COD PRODUCTO, DESCRIPCIÓN, PRESENTACIÓN, COD PDV,NOMBRE PDV, MUNICIPIO,COD ESTABLECIMIENTO,	ESTABLECIMIENTO,	CAJAS,	UNIDADES,	TIPO


    Returns:
        DataFrame datos: Datos del cliente Brasil con las columnas: 
                    [
                        COD PRODUCTO	DESCRIPCIÓN	PRESENTACIÓN	COD PDV	NOMBRE PDV	MUNICIPIO	COD ESTABLECIMIENTO	ESTABLECIMIENTO	CAJAS	UNIDADES	TIPO	FORMATO

                    ]
    """  
    data= pd.read_excel("{}\{}".format(inputPathMaestras, cliente), sheet_name='Hoja1', header=0)
    
    return data     


def set_tq_codes_of_cli(data): 
    '''copia los codigos de producto a codigos TQ'''
    data['COD TQ']=data['COD PRODUCTO']
    
    return data


def organiza_tq_nuevosiglo(data):
    #se organiza cod tq para nuevo siglo se separa los que terminan en -2 y los que terminan en numeros 
    dacon=data[data['COD PRODUCTO'].str.contains('-2$', regex=True)]
    dasin=data[data['COD PRODUCTO'].str.contains('[0-9]{2}$', regex=True)]
    #se elimina el -2 y se concatena
    dacon['COD PRODUCTO']=dacon['COD PRODUCTO'].str[:-2]
    print("dataocc",dacon['COD PRODUCTO'])
    print(len(dacon['COD PRODUCTO']))
    print(len(dasin['COD PRODUCTO']))
    data=dasin.append(dacon)
    print(len(data['COD PRODUCTO']))
    
    return data 


def set_concatenado_municipio(data):
    '''concatena el municipio y el establecimiento en un columna'''
    data.MUNICIPIO.fillna("", inplace=True)
    data.ESTABLECIMIENTO.fillna("", inplace=True)
    
    data['CONCATENADO GRUPO']=data.MUNICIPIO.astype(str).str.cat(data.ESTABLECIMIENTO.astype(str), sep=' - ')
    
    return data

def set_grupo(data):
    
    grupos=pd.read_excel("{}/{}".format(inputPathMaestras, "Grupo Depositos - CAM.xlsx"),
                                        sheet_name="Depositos- Salvador", header=0)
    print("fefa",grupos.columns)
    print("dad",data.columns)
    grupos['CONCATENADO GRUPO']=grupos['CONCATENADO GRUPO'].str.upper()
    grupos=grupos.groupby('CONCATENADO GRUPO').first()
    grupos.reset_index(level=0, inplace=True)
    data=data.merge(grupos[['CONCATENADO GRUPO','Grupo establecimiento']],how="left", on="CONCATENADO GRUPO")
    return data, grupos


def organiza_cod_tq_aguila(data):
    data.ix[data.DESCRIPCIÓN== 'ACETAMINOFEN MK 500 MG. X 100 TABLETAS', 'COD PRODUCTO'] = 3006128
    data['COD PRODUCTO']=data['COD PRODUCTO'].astype(np.int64)
    data.ix[data['COD PRODUCTO']== 3001428 , 'COD PRODUCTO']=3001420
    
    
    return data 
def organiza_tq_integral(data):
    data=data[data['COD PRODUCTO'] != 57602]
    data=data[data['DESCRIPCIÓN'] != "LORAZEPAM MK 1 MG X 1 TAB (DNM)"]
    
    return data

def organiza_tq_santalucia2(data):
    
    data['COD TQ']=data['COD TQ'].astype(str)
    '''
    data.ix[data['COD TQ']== 'NE', 'COD TQ'] = -1
    data['COD TQ']=data['COD TQ'].astype(np.int64)
    '''
    data=data[data['COD TQ'] !="NE"]
    data['COD TQ']=data['COD TQ'].astype(np.int64)
    return data

def organiza_cod_tq_jheral(data):
    data.ix[data.PRESENTACIÓN== '1x5', 'COD TQ'] = 365354
    data.ix[data.PRESENTACIÓN== '2x5', 'COD TQ'] = 355292
    data.ix[data.PRESENTACIÓN== '½x5', 'COD TQ'] = 367114
    
    return data 


def elimina_unidades(data):
    data=data[pd.notnull(data.UNIDADES)]
    data.UNIDADES=data.UNIDADES.astype(np.float64)
    data=data[data.UNIDADES != 0]
    
    return data

def elimina_descontinuado(data):
    data=data[data["COD TQ"] != "Descontinuado"]
    data=data[data['COD TQ'] != 'descontinuado']
    data=data[data['COD TQ'] != 'DESCONTINUADO']
    return data

def organiza_tipo_lavida(data):
    data.ix[data.TIPO== 'EXISTENCIA', 'TIPO'] = "INV"
    data.ix[data.TIPO== 'VENTAS 30', 'TIPO'] = "VTA"
    return data 
    
def organiza_cod_tq_salud(data):
    data.ix[data.DESCRIPCIÓN== 'Vita C Naranja', 'COD TQ'] = 2120571
    return data 

def organiza_cod_tq_sanjose(data,cod):
    
    for indice_fila, fila in cod.iterrows():
       
        
        data.ix[data['COD TQ'].astype(str)== str(fila._values)[1 : -1], 'COD TQ'] = 0
    return data 
       

    
 
def valida_codtq(data,client,hoja):
    articulos_tq_cliente = pd.read_excel("{}/{}".format(inputPathMaestras, "Codigos Articulos Cliente TQ - Salvador.xlsx"),
                                        sheet_name=hoja, header=0)
    articulos_tq_cliente=articulos_tq_cliente[articulos_tq_cliente[hoja[:-1]] == client]
    
    articulos_tq_cliente.rename(columns={'DESCRIPCION':'DESCRIPCIÓN'}, inplace=True)
    dat=data[['COD TQ','DESCRIPCIÓN']].merge(articulos_tq_cliente[['COD TQ','DESCRIPCIÓN']],on="COD TQ", how='left')
    
    
    dat=dat[dat.DESCRIPCIÓN_y.isnull()][['COD TQ']]
    
    return dat
    
def set_tq_code_descripcion(data,client,hoja):
    '''obtienen los codigos de TQ a partir de la descripcion
        Parameters:
        data (DataFrame): Conjunto de artículos. Deben tener las columnas:
                        [
                             COD PRODUCTO, DESCRIPCIÓN, PRESENTACIÓN, COD PDV,NOMBRE PDV, MUNICIPIO,COD ESTABLECIMIENTO,	ESTABLECIMIENTO,	CAJAS,	UNIDADES,	TIPO
                        ]
        client(str): Nombre del cliente.
        hoja: la hoja que usa la maestra

        Returns:
            resultado (Dataframe): Conjunto de artículos con su respectivo código TQ.
                                
            no_codigos (List): Articulos que no tiene código TQ
    
    '''
    c = data.columns
    no_codigos=None
    articulos_tq_cliente = pd.read_excel("{}/{}".format(inputPathMaestras, "Codigos Articulos Cliente TQ - Salvador.xlsx"),
                                        sheet_name=hoja, header=0)
    articulos_tq_cliente=articulos_tq_cliente[articulos_tq_cliente[hoja[:-1]] == client]
    
    
    data.DESCRIPCIÓN=data.DESCRIPCIÓN.str.strip().str.upper().str.replace('  ', ' ').str.replace('   ', ' ').str.replace('    ', ' ')
    articulos_tq_cliente.DESCRIPCION=articulos_tq_cliente.DESCRIPCION.str.strip().str.upper().str.replace('  ', ' ').str.replace('   ', ' ').str.replace('    ', ' ')
    datacod=data.merge(articulos_tq_cliente[['DESCRIPCION','COD TQ']], how='left', left_on="DESCRIPCIÓN", right_on="DESCRIPCION")
    no_codigos = datacod[pd.isnull(datacod['COD TQ'])]
    concodigos = datacod[pd.notnull(datacod['COD TQ'])]
    no_codigos = datacod[pd.isnull(datacod["COD TQ"])]
    if len(no_codigos) > 0:
        print("No se logró obtener los factores de conversion para: " + no_codigos.loc[:,["DESCRIPCIÓN"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los codigos TQ",
            "result": no_codigos.loc[:, ["DESCRIPCIÓN',"]].drop_duplicates().to_json(orient="split")
        })
    """
    return concodigos, no_codigos



def set_tq_code(data, client,hoja):
    """
    Obtener el código TQ respectivo de cada artículo, usando el código
    que maneja el cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos. Deben tener las columnas:
                        [
                             COD PRODUCTO, DESCRIPCIÓN, PRESENTACIÓN, COD PDV,NOMBRE PDV, MUNICIPIO,COD ESTABLECIMIENTO,	ESTABLECIMIENTO,	CAJAS,	UNIDADES,	TIPO
                        ]
        client(str): Nombre del cliente.

    Returns:
        resultado (Dataframe): Conjunto de artículos con su respectivo código TQ.
                            [
                                'CODIGO', 'DESCRIPCION', 'PDV', 'TIPO', 'VTA_INV', 
                                'UNIDADES', 'COD CLIENTE', 'COD TQ', 'NOMB TQ'
                            ]
        no_codigos (List): Articulos que no tiene código TQ
    """
    c = data.columns
    no_codigos=None
    articulos_tq_cliente = pd.read_excel("{}/{}".format(inputPathMaestras, "Codigos Articulos Cliente TQ - Salvador.xlsx"),
                                        sheet_name=hoja, header=0)
       
    articulos_tq_cliente=articulos_tq_cliente[articulos_tq_cliente[hoja[:-1]] == client]
    
    
   
            
    
    articulos_tq_cliente["COD PRODUCTO"] = articulos_tq_cliente["COD PRODUCTO"].astype(str)
    data["COD PRODUCTO"].fillna(0, inplace=True)
    data["COD PRODUCTO"] = data["COD PRODUCTO"].astype(str)
    data = pd.merge(data, articulos_tq_cliente[['COD PRODUCTO', 'COD TQ']], how="left",
                        left_on="COD PRODUCTO", right_on="COD PRODUCTO")
    #data.drop([cod_prod], axis=1, inplace=True)
    # Si faltan articulos por codigo, debe hacerse la búsqueda por descripción.
    
    
        

    # Obtener los articulos que definitivamente no tienen codigo
    
    
    data=data[data["COD TQ"] != "Descontinuado"]
    # data=data[pd.notnull(data['COD TQ'])]
    data=data[(data['UNIDADES'] !=  0)]
    #data=data[(data['UNIDADES']  >  0.000001)]
    #no_codigos = data[pd.isna(data[cod_prod_tq])]
    
    no_codigos = data[pd.isnull(data["COD TQ"])]
    if len(no_codigos) > 0:
        print("No se logró obtener los factores de conversion para: " + no_codigos.loc[:,["DESCRIPCIÓN"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los codigos TQ",
            "result": no_codigos.loc[:, ["DESCRIPCIÓN',"]].drop_duplicates().to_json(orient="split")
        })
    """
    
    return data, no_codigos


def set_tq_codes_str(data, client,hoja):
    """
    Obtener el código TQ respectivo de cada artículo, usando el código
    usando descripcion despuesde buscar por codigos

    Parameters:
        data (DataFrame): Conjunto de artículos. Deben tener las columnas:
                        [
                             COD PRODUCTO, DESCRIPCIÓN, PRESENTACIÓN, COD PDV,NOMBRE PDV, MUNICIPIO,COD ESTABLECIMIENTO,	ESTABLECIMIENTO,	CAJAS,	UNIDADES,	TIPO
                        ]
        client(str): Nombre del cliente.

    Returns:
        resultado (Dataframe): Conjunto de artículos con su respectivo código TQ.
                            
        no_codigos (List): Articulos que no tiene código TQ
    """
    
    c = data.columns
    no_codigos=None
    articulos_tq_cliente = pd.read_excel("{}/{}".format(inputPathMaestras, "Codigos Articulos Cliente TQ - Salvador.xlsx"),
                                        sheet_name=hoja, header=0)
       
    articulos_tq_cliente=articulos_tq_cliente[articulos_tq_cliente[hoja[:-1]] == client]
      
        #quitamos descontinuados de cod productos y de codigos tq
    articulos_tq_clientes=articulos_tq_cliente[articulos_tq_cliente["COD PRODUCTO"] != "Descontinuado"]
    #articulos_tq_clientes=articulos_tq_cliente[articulos_tq_cliente["COD TQ"] != "Descontinuado"]
   
    
    articulos_tq_clientes['COD PRODUCTO'].fillna(0, inplace=True)
    articulos_tq_clientes['COD PRODUCTO']=articulos_tq_clientes['COD PRODUCTO'].astype(str)
    data['COD PRODUCTO']=data['COD PRODUCTO'].astype(str)
    #obtenemos los que no tiene cod producto y agrupamos por descripcion
    data_sincod=articulos_tq_clientes[articulos_tq_clientes['COD PRODUCTO']==0]
    #data_sincod=data_sincod.groupby('DESCRIPCION').first().reset_index(0)
    #agrupamos por codigo de producto
    data_articulos2 = articulos_tq_clientes.groupby('COD PRODUCTO').first()
    data_articulos2.reset_index(level=0, inplace=True)
    #buscamos entre los datos
    base=pd.merge(data,data_articulos2[['COD PRODUCTO', 'COD TQ']], how="left", left_on="COD PRODUCTO", right_on="COD PRODUCTO")
    base_sincod=base[base['COD TQ'].isnull()]
    base_sincod=base_sincod.drop(columns="COD TQ")
   
    ##buscamos los que no obtuieron codigo atravez de la descripcion
    base_sincod['DESCRIPCIÓN']=base_sincod['DESCRIPCIÓN'].str.strip().str.upper().str.replace('  ', ' ').str.replace('   ', ' ').str.replace('    ', ' ')
    data_sincod['DESCRIPCION']=data_sincod['DESCRIPCION'].str.strip().str.upper().str.replace('  ', ' ').str.replace('   ', ' ').str.replace('    ', ' ')
    articulos_tq_clientes['DESCRIPCION']=articulos_tq_clientes['DESCRIPCION'].str.strip().str.upper().str.replace('  ', ' ').str.replace('   ', ' ').str.replace('    ', ' ')
    base_sincod=pd.merge(base_sincod,articulos_tq_clientes[['DESCRIPCION', 'COD TQ']], how="left", left_on="DESCRIPCIÓN", right_on="DESCRIPCION")
    base=base[pd.notnull(base['COD TQ'])]
    #unimos bases
    bases=base.append(base_sincod)
    
    unid=bases[bases['TIPO']=='VTA']   
    
    #bases=bases[bases["COD TQ"] != "Descontinuado"]
    bases=bases[(bases['UNIDADES'] !=  0)]
    no_codigos = bases[pd.isnull(bases["COD TQ"])]
    
    #volvemos a buscar los que no obtuvieron codigo TQ a travez de la descripcion
    
    
    no_codigos=no_codigos.drop(columns="COD TQ")    
    no_codigos['DESCRIPCIÓN']=no_codigos['DESCRIPCIÓN'].str.strip().str.upper().str.replace('  ', '').str.replace('   ', '').str.replace('    ', '')
    data_sincod['DESCRIPCION']=data_sincod['DESCRIPCION'].str.strip().str.upper().str.replace('  ', '').str.replace('   ', '').str.replace('    ', '')    
    no_codig=no_codigos.merge(data_sincod[['DESCRIPCION', 'COD TQ']],how="left", left_on="DESCRIPCIÓN", right_on="DESCRIPCION")
    #unimos bases
    base2=bases[pd.notnull(bases["COD TQ"])].append(no_codig)    
    no_codigos = no_codig   
    no_codigos = bases[pd.isnull(bases["COD TQ"])]
    if len(no_codigos) > 0:
        print("No se logró obtener los factores de conversion para: " + no_codigos.loc[:,["DESCRIPCIÓN"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los codigos TQ",
            "result": no_codigos.loc[:, ["DESCRIPCIÓN',"]].drop_duplicates().to_json(orient="split")
        })
    """
    
    return bases,no_codigos,base2
    

def set_tq_codes2(data, client,hoja):
    """
    Obtener el código TQ respectivo de cada artículo, usando el código
    que maneja el cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos. Deben tener las columnas:
                        [
                             COD PRODUCTO, DESCRIPCIÓN, PRESENTACIÓN, COD PDV,NOMBRE PDV, MUNICIPIO,COD ESTABLECIMIENTO,	ESTABLECIMIENTO,	CAJAS,	UNIDADES,	TIPO
                        ]
        client(str): Nombre del cliente.

    Returns:
        resultado (Dataframe): Conjunto de artículos con su respectivo código TQ.
                            
        no_codigos (List): Articulos que no tiene código TQ
    """
    ##cargamos muestras y buscamos las del cliente en especifico
    c = data.columns
    no_codigos=None
    articulos_tq_cliente = pd.read_excel("{}/{}".format(inputPathMaestras, "Codigos Articulos Cliente TQ - Salvador.xlsx"),
                                        sheet_name=hoja, header=0)   
    
    articulos_tq_cliente=articulos_tq_cliente[articulos_tq_cliente[hoja[:-1]] == client]    
    #quitamos descontinuados de cod productos y de codigos tq y volvemos tipo entero
    articulos_tq_clientes=articulos_tq_cliente[articulos_tq_cliente["COD PRODUCTO"] != "Descontinuado"]    
    articulos_tq_clientes['COD PRODUCTO'].fillna(0, inplace=True)
    
    articulos_tq_clientes['COD PRODUCTO']=articulos_tq_clientes['COD PRODUCTO'].astype(np.int64)
    #obtenemos los que no tiene cod producto y agrupamos por descripcion
    data_sincod=articulos_tq_clientes[articulos_tq_clientes['COD PRODUCTO']==0]
    #agrupamos por codigo de producto
    data_articulos2 = articulos_tq_clientes.groupby('COD PRODUCTO').first()
    data_articulos2.reset_index(level=0, inplace=True)
    #buscamos entre los datos
    base=pd.merge(data,data_articulos2[['COD PRODUCTO', 'COD TQ']], how="left", left_on="COD PRODUCTO", right_on="COD PRODUCTO")
    base_sincod=base[base['COD TQ'].isnull()]
    base_sincod=base_sincod.drop(columns="COD TQ")
    ##buscamos los que no tenian codigo de producto 
    base_sincod['DESCRIPCIÓN']=base_sincod['DESCRIPCIÓN'].str.strip().str.upper().str.replace('  ', ' ').str.replace('   ', ' ').str.replace('    ', ' ')
    data_sincod['DESCRIPCION']=data_sincod['DESCRIPCION'].str.strip().str.upper().str.replace('  ', ' ').str.replace('   ', ' ').str.replace('    ', ' ')
    articulos_tq_clientes['DESCRIPCION']=articulos_tq_clientes['DESCRIPCION'].str.strip().str.upper().str.replace('  ', ' ').str.replace('   ', ' ').str.replace('    ', ' ')
    base_sincod=pd.merge(base_sincod,articulos_tq_clientes[['DESCRIPCION', 'COD TQ']], how="left", left_on="DESCRIPCIÓN", right_on="DESCRIPCION")
    base=base[pd.notnull(base['COD TQ'])]
    bases=base.append(base_sincod)
    
    unid=bases[bases['TIPO']=='VTA']   
    
    bases=bases[bases["COD TQ"] != "Descontinuado"]
    bases=bases[(bases['UNIDADES'] !=  0)]
    no_codigos = bases[pd.isnull(bases["COD TQ"])]
    
    
    ##buscamos los que no obtuvimos codigo apartir de la descripcion 
    
    no_codigos=no_codigos.drop(columns="COD TQ")    
    no_codigos['DESCRIPCIÓN']=no_codigos['DESCRIPCIÓN'].str.strip().str.upper().str.replace('  ', '').str.replace('   ', '').str.replace('    ', '')
    data_sincod['DESCRIPCION']=data_sincod['DESCRIPCION'].str.strip().str.upper().str.replace('  ', '').str.replace('   ', '').str.replace('    ', '')
    no_codig=no_codigos.merge(data_sincod[['DESCRIPCION', 'COD TQ']],how="left", left_on="DESCRIPCIÓN", right_on="DESCRIPCION")
    ##unimos bases
    base2=bases[pd.notnull(bases["COD TQ"])].append(no_codig)    
    no_codigos = no_codig
    
    ##elimina descontinuados y convierte en entero     
    
    bases=bases[bases["COD TQ"] != "Descontinuado"]
    bases=bases[bases["COD TQ"] != "DESCONTINUADO"]
    bases['COD TQ']=bases['COD TQ'].astype(np.int64)
    no_codigos = bases[pd.isnull(bases["COD TQ"])]
    if len(no_codigos) > 0:
        print("No se logró obtener los factores de conversion para: " + no_codigos.loc[:,["DESCRIPCIÓN"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los codigos TQ",
            "result": no_codigos.loc[:, ["DESCRIPCIÓN',"]].drop_duplicates().to_json(orient="split")
        })
    """
    
    return bases,no_codigos,base2
    
    
def set_tq_codes_onlytq(data, client):
    """
    Obtener el código TQ respectivo de cada artículo, usando el código
    que maneja el cliente. pero solo los articulos de tq 

    Parameters:
        data (DataFrame): Conjunto de artículos. Deben tener las columnas:
                        [
                             COD PRODUCTO, DESCRIPCIÓN, PRESENTACIÓN, COD PDV,NOMBRE PDV, MUNICIPIO,COD ESTABLECIMIENTO,	ESTABLECIMIENTO,	CAJAS,	UNIDADES,	TIPO
                        ]
        client(str): Nombre del cliente.

    Returns:
        resultado (Dataframe): Conjunto de artículos con su respectivo código TQ.
                            
        no_codigos (List): Articulos que no tiene código TQ
    """
    data['COD PRODUCTO'] = data['COD PRODUCTO'].astype(np.int64)
    
    data_bonima=data[data['FORMATO'] !='TQ']
    data=data[data['FORMATO']=='TQ']
    
    
    
    data_bonima=set_tq_codes_of_cli(data_bonima)
    ##abrimos articulos del cleinte y convertirmos en entero
    c = data.columns
    no_codigos=None
    articulos_tq_cliente = pd.read_excel("{}/{}".format(inputPathMaestras, "Codigos Articulos Cliente TQ - Salvador.xlsx"),
                                        sheet_name=client, header=0)
           
    articulos_tq_cliente['COD TQ'] = articulos_tq_cliente['COD TQ'].fillna(0).astype(np.int64)
    ##buscamos los articulos que no tienen codigo y agrupamos por codigo TQ y codigo de producto
    data_sincod=articulos_tq_cliente[pd.isnull(articulos_tq_cliente["COD PRODUCTO"])]
    data_sincod =data_sincod.groupby(["COD TQ"]).first().reset_index(level=0)
    articulos_tq2=articulos_tq_cliente.groupby('COD PRODUCTO').first().reset_index(level=0)
    ##buscamos los codigos TQ
    base=pd.merge(data,articulos_tq2[['COD PRODUCTO', 'COD TQ']].drop_duplicates(), how="left", left_on="COD PRODUCTO", right_on="COD PRODUCTO")
    ##obtenemos los que quedaron sin codigo y limpiamos columna de TQ
    base_sincod=base[base['COD TQ'].isnull()]
    base_sincod=base_sincod.drop(columns="COD TQ")
    ##obtenemos codigo TQ atravez de la descripcion de los que no obtuvieron codigo 
    base_sincod=pd.merge(base_sincod,data_sincod[['DESCRIPCION', 'COD TQ']], how="left", left_on="DESCRIPCIÓN", right_on="DESCRIPCION")
    base_sincod=base_sincod.drop(columns="DESCRIPCION")
    base_sincod=base_sincod.drop(columns="COD PRODUCTO")
    base=base[pd.notnull(base['COD TQ'])]
    ##unimos bases de datos
    data=base.append(base_sincod)
        
    
    data_sincod_tq=data[pd.isnull(data["COD TQ"])]
    
    
    # Si faltan articulos por codigo, debe hacerse la búsqueda por descripción.
    
    if len(data[pd.isnull(data["COD TQ"])]) > 0:
        
        ##buscamos datos a partir de la descripcion
        data['DESCRIPCIÓN'] = data['DESCRIPCIÓN'].str.strip().str.upper().str.replace('  ', ' ')
        articulos_tq_cliente["DESCRIPCION"] = articulos_tq_cliente["DESCRIPCION"].str.strip().str.upper().str.replace('  ', ' ')
        data['DESCRIPCIÓN'] = data['DESCRIPCIÓN'].str.strip().str.upper().str.replace(' ', ' ')
        articulos_tq_cliente["DESCRIPCION"] = articulos_tq_cliente["DESCRIPCION"].str.strip().str.upper().str.replace(' ', ' ')
        #agrupamos articulos ciente por descipcion 
        articulos_tq_cliente =articulos_tq_cliente.groupby("DESCRIPCION").first()
        articulos_tq_cliente.reset_index(level=0, inplace=True)
        ##obtenems datos sin codigo
        data_sincod=data[pd.isnull(data["COD TQ"])]
        ##asiganamos las mismas columnas
        data_sincod=data_sincod[c]
        base_inv=pd.merge(data_sincod,articulos_tq_cliente[["DESCRIPCION", "COD TQ"]], how="left", left_on="DESCRIPCIÓN", right_on="DESCRIPCION")
        #obtenemos los que no obtuvimos coo TQ y volvermos abuscar por descripcion
        data = data[pd.notnull(data["COD TQ"])].append(base_inv)       
        no_codigos = data[pd.isnull(data["COD TQ"])]
        
           
        data.drop("DESCRIPCION", axis=1, inplace=True)
        
        if len(data[pd.isnull(data["COD TQ"])]) > 0:                       
            articulos_tq_sincod["DESCRIPCION"] = articulos_tq_sincod["DESCRIPCION"].str.strip().str.upper().str.replace('  ', ' ')           
            articulos_tq_sincod["DESCRIPCION"] = articulos_tq_sincod["DESCRIPCION"].str.strip().str.upper().str.replace(' ', ' ')
            no_codigos = no_codigos.merge(articulos_tq_sincod[["DESCRIPCION", "COD TQ"]],how="left", left_on="DESCRIPCIÓN", right_on="DESCRIPCION") 
            
    # Obtener los articulos que definitivamente no tienen codigo
    
    
    data=data[data["COD TQ"] != "Descontinuado"]
    # data=data[pd.notnull(data['COD TQ'])]
    data=data[(data['UNIDADES'] !=  0)]
    #data=data[(data['UNIDADES']  >  0.000001)]
    
    data=data.append(data_bonima)
    
    no_codigos = data[pd.isnull(data["COD TQ"])]
    if len(no_codigos) > 0:
        print("No se logró obtener los factores de conversion para: " + no_codigos.loc[:,["DESCRIPCIÓN"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los codigos TQ",
            "result": no_codigos.loc[:, ["DESCRIPCIÓN',"]].drop_duplicates().to_json(orient="split")
        })
    """
    return data,no_codigos


def calculate_units_s(data,client):
    '''calcula unidades apartir del factor de conversion pero solo toma los articulos que empiezen con S'''
    ##obtenemos articulos que solo empiezan por S
    co=data[data['COD PRODUCTO'].str.contains('^S', regex=True)]
    ##abrimos el archivo con los factores de conversion  y agrupamos por codigo de producto
    factor_conversion = pd.read_excel("{}/{}".format(inputPathMaestras, 'Factor de conversion - Salvador.xlsx'),
                                    sheet_name=client)
    factor_conversion = factor_conversion.groupby("COD PRODUCTO").first().reset_index(level=0)
    ##eliminamos descripions y obtenemo el factore de conversion para la data
    factor_conversion.drop("DESCRIPCION", axis=1, inplace=True)    
    data=data.merge(factor_conversion[['COD PRODUCTO','FACTOR DE CONVERSION']],how="left", left_on="COD PRODUCTO", right_on="COD PRODUCTO")
    
    no_codigos=data[data['FACTOR DE CONVERSION'].isnull()]
    if len(no_codigos) > 0:
        print("No se logró obtener los factores de conversion para: " + no_codigos.loc[:,["DESCRIPCIÓN"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los codigos TQ",
            "result": no_codigos.loc[:, ["DESCRIPCIÓN',"]].drop_duplicates().to_json(orient="split")
        })
    """
    
    #data=data.merge(data_co[['COD PRODUCTO','FACTOR DE CONVERSION']],how="left", left_on="COD PRODUCTO", right_on="COD PRODUCTO")
    
    #ponemos 1 a las que no obtuvieron factor de conversion y multiplicamos 
    data['FACTOR DE CONVERSION'].fillna(1, inplace=True)
    data['UNIDADES DEF']=data['FACTOR DE CONVERSION']*data['UNIDADES']
    
    return data
        

def calculate_units_santalucia(data):
    data['COD PRODUCTO']=data['COD PRODUCTO'].astype(np.int64)
    datablis=data[(data['COD PRODUCTO'] == 154249) | (data['COD PRODUCTO'] == 154248)]
    datasinblis=data[(data['COD PRODUCTO'] != 154249) | (data['COD PRODUCTO'] != 154248)]
    datablis['UNIDADES DEF']=datablis['UNIDADES'] / 12
    datasinblis['UNIDADES DEF']=datasinblis['UNIDADES']
    
    data=datasinblis.append(datablis)
    return data


def calculate_units(data, client):
    """
    Funcion que calcula las unidades, en base a las completas mas las fraccionadas.
    Unidades = Completas + Fraccion * Factor.

    Parameters:
        data (DataFrame): Conjunto de artículos. Deben tener las columnas:
                        [
                            'CODIGO', 'DESCRIPCION', 'PDV', 'TIPO', 'VTA_INV', 
                            'UNIDADES', 'COD CLIENTE', 'COD TQ', 'NOMB TQ'
                        ]
        client (str): Nombre del cliente

    Returns:
        resultado (DataFrame): Conjunto de artículos con las unidades completas:
                            
        no_factor (DataFrame): Conjunto de artículos a los que no se les halló un factor
    """
    # Lectura del archivo de factor de conversion
    factor_conversion = pd.read_excel("{}/{}".format(inputPathMaestras, 'Factor de conversion El Salvador.xlsx'),
                                    sheet_name=client)
    factor_conversion = factor_conversion.groupby("CODIGO").first().reset_index(level=0)
    factor_conversion.drop("DESCRIPCION", axis=1, inplace=True)

    # Se clasifican las unidades en completas y por fraccion
    completa = data[data["TIPO"] == "SALDO"]
    completa["COMPLETAS"] = completa["UNIDADES"]
    fraccion = data[data["TIPO"] == "FRACCION"]
    # Se obtiene el factor de conversion de cada articulo
    fraccion = fraccion.merge(factor_conversion, how="left", on="CODIGO")

    # Se identifican las fracciones que no tienen factor de conversion
    no_factor = fraccion[pd.isnull(fraccion['FACTOR CONVERSION'])]

    # Se hace el calculo de las unidades: Unidades = Completas + (Fracciones * Factor)
    fraccion["UNIDADES"] = fraccion.apply(
    lambda x: x["UNIDADES"] / x["FACTOR CONVERSION"] if x["FACTOR CONVERSION"] > 1 else x["UNIDADES"] * x["FACTOR CONVERSION"],
    axis=1)

    data = pd.concat([completa, fraccion])
    data = data[['VTA_INV', 'COD CLIENTE', 'COD TQ', 'NOMB TQ', 'PDV', 'UNIDADES', 'COMPLETAS']]
    data = data.groupby(['VTA_INV', 'COD CLIENTE', 'COD TQ', 'NOMB TQ','PDV']).agg({"UNIDADES": "sum", "COMPLETAS": "sum"}).reset_index()

    # Se le agrega la columna de factor de conversion
    data = data.merge(fraccion[["COD TQ", "FACTOR CONVERSION"]].drop_duplicates(), how="left", on="COD TQ").fillna(0)
    
    return data, no_factor

def set_sellings_point_tq_code(data, client):
    """
    Obtener los codigos de los puntos de ventas registrados en TQ

    Parameters:
        data (DataFrame): Conjunto de artículos. Debe tener las columnas:
                        [
                            'VTA_INV', 'COD CLIENTE', 'COD TQ', 'NOMB TQ', 'PDV', 'UNIDADES',
                            'FACTOR CONVERSION'
                        ]
        client (str): Nombre del cliente.

    Returns:
        resultado (DataFrame): Conjunto de artículos con su respectivo punto de venta TQ
                           
    """
    
    data.drop("NOMBRE PDV", axis=1, inplace=True)
    # Lectura de la maestra de codigos de ventas
    puntos_venta = pd.read_excel("{}/{}".format(inputPathMaestras, 'Codigos PDV Cliente TQ - Salvador.xlsx'),
                                sheet_name=client)
    #puntos_venta.rename(columns = { 'COD TQ': 'PDV TQ', 'NOMBRE QUE REPORTA EL CLIENTE': 'PDV' }, inplace = True)
    #puntos_venta.drop("FORMATO", axis=1, inplace=True)    
    #data['COD PDV'] = data['COD PDV'].str.strip().astype(str).str.upper()
    #puntos_venta['COD PDV'] = puntos_venta['COD PDV'].astype(str).str.strip().str.upper()
    puntos_venta=puntos_venta.drop_duplicates()
    puntos_venta=puntos_venta.groupby('COD PDV').first()
    puntos_venta.reset_index(level=0, inplace=True)    
    puntos_venta.rename(columns = { 'COD PDV':'COD PDV CLI' }, inplace = True)
    # Se consulta los codigos de ventas para cada articulo, si no existe se coloca cero (0).    
    
    data = data.merge(puntos_venta[['COD PDV CLI','COD PDV TQ']], how="left", left_on="COD PDV", right_on="COD PDV CLI")
    no_codigos = data[pd.isnull(data["COD PDV TQ"])]
    #data.drop("COD PDV CLI", axis=1, inplace=True)
    data['COD PDV TQ'].fillna(0, inplace=True)
    
    
    if len(no_codigos) > 0:
        print("No se logró obtener codigos de PDV TQ para: " + no_codigos.loc[:,["DESCRIPCIÓN"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los codigos de PDV TQ",
            "result": no_codigos.loc[:, ["DESCRIPCIÓN',"]].drop_duplicates().to_json(orient="split")
        })
    """
        
    return data


def set_sellings_point_tq_code_names(data, client):
    """
    Obtener los codigos de los puntos de ventas registrados en TQ a partir de los nombres de estos

    Parameters:
        data (DataFrame): Conjunto de artículos. Debe tener las columnas:
                        [
                            'VTA_INV', 'COD CLIENTE', 'COD TQ', 'NOMB TQ', 'PDV', 'UNIDADES',
                            'FACTOR CONVERSION'
                        ]
        client (str): Nombre del cliente.

    Returns:
        resultado (DataFrame): Conjunto de artículos con su respectivo punto de venta TQ
                            
    """
    
    #data.drop("NOMBRE PDV", axis=1, inplace=True)
    # Lectura de la maestra de codigos de ventas
    puntos_venta = pd.read_excel("{}/{}".format(inputPathMaestras, 'Codigos PDV Cliente TQ - Salvador.xlsx'),
                                sheet_name=client)
    #puntos_venta.rename(columns = { 'COD TQ': 'PDV TQ', 'NOMBRE QUE REPORTA EL CLIENTE': 'PDV' }, inplace = True)
    #puntos_venta.drop("FORMATO", axis=1, inplace=True)    
    #data['COD PDV'] = data['COD PDV'].str.strip().astype(str).str.upper()
    #puntos_venta['COD PDV'] = puntos_venta['COD PDV'].astype(str).str.strip().str.upper()
    puntos_venta=puntos_venta.drop_duplicates()
    puntos_venta=puntos_venta.groupby('NOMBRE PDV').first()
    puntos_venta.reset_index(level=0, inplace=True)
    data['NOMBRE PDV']= data['NOMBRE PDV'].str.strip()
    puntos_venta.rename(columns = { 'NOMBRE PDV':'NOMBRE PDV CLI' }, inplace = True)
    # Se consulta los codigos de ventas para cada articulo, si no existe se coloca cero (0).    
    data = data.merge(puntos_venta[['NOMBRE PDV CLI','COD PDV TQ']], how="left", left_on="NOMBRE PDV", right_on="NOMBRE PDV CLI")
    data.drop("NOMBRE PDV CLI", axis=1, inplace=True)
    no_codigos = data[pd.isnull(data["COD PDV TQ"])]
    data['COD PDV TQ'].fillna(0, inplace=True)
    
    if len(no_codigos) > 0:
        print("No se logró obtener codigos de PDV TQ para: " + no_codigos.loc[:,["DESCRIPCIÓN"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los codigos de PDV TQ",
            "result": no_codigos.loc[:, ["DESCRIPCIÓN',"]].drop_duplicates().to_json(orient="split")
        })
    """
    
    return data



def set_cod_neg(data, region):
    """
    Obtiene el Codigo de negocio del cliente

    Parameters:
        data (DataFrame): Conjunto de artículos:
                        [
                            'VTA_INV', 'COD CLIENTE', 'COD TQ', 'NOMB TQ', 'PDV', 
                            'UNIDADES', 'PDV TQ'
                        ]
        region (str): Nombre de la region con la que se va a trabajar

    Returns:
        resultado (DataFrame): Conjunto de articulos con su respectiva concatenacion y formato
                        
    """
    if  'COD NEG' in data.columns:
        data.drop("COD NEG", axis=1, inplace=True)
    # Cargue de la maestra de artículos y selección de columnas.
    maestra_cam_articulos = pd.read_excel("{}/{}".format(inputPathMaestras, 'Maestra Articulos CAM.xlsx'),
                                            sheet_name=region, skiprows=2)
    maestra_cam_articulos = maestra_cam_articulos.loc[:, ['COD TQ', 'COD NEG']]    
    # Se cerciora que los tipo de datos sean correctos
    maestra_cam_articulos['COD TQ'] = maestra_cam_articulos['COD TQ'].astype(str)
    data['COD TQ'] = data['COD TQ'].astype(str)    
    # Retirar los articulos repetidos
    maestra_cam_articulos_unique = maestra_cam_articulos.groupby(['COD TQ']).first()
    # Se agrega el codigo de negocio 
    data = pd.merge(data, maestra_cam_articulos_unique, how="left", on="COD TQ")
    data['COD NEG']=data['COD NEG'].fillna(0)
    return data

def set_concatenated_and_format(data, region):
    """
    Obtiene el concatenado (Nombre + Presentación) y el formato ["TQ", "BONIMA"] y codigo de negocio.

    Parameters:
        data (DataFrame): Conjunto de artículos:
                        [
                            'VTA_INV', 'COD CLIENTE', 'COD TQ', 'NOMB TQ', 'PDV', 
                            'UNIDADES', 'PDV TQ'
                        ]
        region (str): Nombre de la region con la que se va a trabajar

    Returns:
        resultado (DataFrame): Conjunto de articulos con su respectiva concatenacion y formato
                       
    """
    if  'FORMATO' in data.columns:
        data.drop("FORMATO", axis=1, inplace=True)
    # Cargue de la maestra de artículos y selección de columnas.
    maestra_cam_articulos = pd.read_excel("{}/{}".format(inputPathMaestras, 'Maestra Articulos CAM.xlsx'),
                                            sheet_name=region, skiprows=2)
    maestra_cam_articulos = maestra_cam_articulos.loc[:, ['COD TQ', 'CONCATENADO','COD NEG', 'FORMATO']]    
    # Se cerciora que los tipo de datos sean correctos
    maestra_cam_articulos['COD TQ'] = maestra_cam_articulos['COD TQ'].astype(str)
    data['COD TQ'] = data['COD TQ'].astype(str)    
    # Retirar los articulos repetidos
    maestra_cam_articulos_unique = maestra_cam_articulos.groupby(['COD TQ']).first()
    # Se agrega la concatenacion y el formato por artículo
    data = pd.merge(data, maestra_cam_articulos_unique, how="left", on="COD TQ")
    
    return data

def set_format(data, region):
    """
    Obtiene el formato ["TQ", "BONIMA"].

    Parameters:
        data (DataFrame): Conjunto de artículos:
                        [
                            'VTA_INV', 'COD CLIENTE', 'COD TQ', 'NOMB TQ', 'PDV', 
                            'UNIDADES', 'PDV TQ'
                        ]
        region (str): Nombre de la region con la que se va a trabajar

    Returns:
        resultado (DataFrame): Conjunto de articulos con su respectiva concatenacion y formato
                      
    """
    if  'FORMATO' in data.columns:
        data.drop("FORMATO", axis=1, inplace=True)
    # Cargue de la maestra de artículos y selección de columnas.
    maestra_cam_articulos = pd.read_excel("{}/{}".format(inputPathMaestras, 'Maestra Articulos CAM.xlsx'),
                                            sheet_name=region, skiprows=2)
    maestra_cam_articulos = maestra_cam_articulos.loc[:, ['COD TQ', 'FORMATO']]    
    # Se cerciora que los tipo de datos sean correctos
    maestra_cam_articulos['COD TQ'] = maestra_cam_articulos['COD TQ'].astype(str)
    data['COD TQ'] = data['COD TQ'].astype(str)
    
    # Retirar los articulos repetidos
    maestra_cam_articulos_unique = maestra_cam_articulos.groupby(['COD TQ']).first()
    # Se agrega  el formato por artículo
    data = pd.merge(data, maestra_cam_articulos_unique, how="left", on="COD TQ")
    
    return data


def filter_u_codtq(data):
    '''elimina unidades en 0 y descontinuados'''
    data=data[data['UNIDADES'] != 0]
    data=data[data['COD TQ'] != 'Descontinuado']
    
    return data
    


def set_price_hist(data,client,hoja):
    ##abrimos el archivo apartir del la hoja, y renombramos columns organizamos el mes y filtramos los datos del cliente 
    lp_hist = pd.read_excel("{}/{}".format(inputPathMaestras, "Lista de Precios historico - Salvador.xlsx"),sheet_name=hoja, header=0)   
    lp_hist.rename(columns = { 'CIF NETO': 'PRECIO' }, inplace = True)
    lp_hist.MES=lp_hist.MES.str.strip().str.upper().str.replace('. ', '')
    lp_hist2=lp_hist[lp_hist['NOMBRE CLIENTE'] == client]
    ##organizamos los meses de forma ascendente  para obtener el ultimo  y agrupamos por codigo TQ
    lp_hist2.MES=lp_hist2.MES.astype(str)
    lp_hist2.sort_values("MES",ascending=True)
    lp_hist22=lp_hist2.groupby("COD TQ").first().reset_index()[["COD TQ", "PRECIO",'NOMBRE CLIENTE','MES']]
    #lp_hist = lp_hist[lp_hist["NOMBRE CLIENTE"].str.contains(client, case=False)].sort_values("MES", ascending=False).groupby("COD TQ").first().reset_index()[["COD TQ", "CIF NETO"]]    
    #lp_hist2=pd.DataFrame(np.sort(lp_hist2.values,axis=0),index=lp_hist2.index,columns=lp_hist2.columns)
    ##convertimos a tipo entero
    lp_hist22['COD TQ'] = lp_hist22['COD TQ'].astype(np.int64)
    #data['COD TQ']=data[data['COD TQ']!='DESCONTINUADO']    
    data['COD TQ'] = data['COD TQ'].astype(np.int64)
    #miramos que no exista la columna precio 
    if  'PRECIO' in data.columns:
        data.drop(['PRECIO'], axis=1, inplace=True)
        
    #traemos el precio    
    data=data.merge(lp_hist22, how="left", on="COD TQ")    
    sin_precio = data[data["PRECIO"].isna()]
    
    no_codigos = data[pd.isnull(data["PRECIO"])]
    if len(no_codigos) > 0:
        print("No se logró obtener los precios para: " + no_codigos.loc[:,["COD TQ"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los precios",
            "result": no_codigos.loc[:, ["COD TQ',"]].drop_duplicates().to_json(orient="split")
        })
    """
    
    return data, sin_precio
    

def set_price_nor(data,ref_cliente,pertenencia_nor,pertenencia):
    """
        Hallar el precio neto de cada artículo buscando primero en la lista nor despues en
        la list precios a la que pertenece el cliente y luego por el historial de precios.
    
        Parameters:
            data (DataFrame): Conjunto de artículos. Debe tener las columnas:
                            [
                                'VTA_INV', 'COD CLIENTE', 'COD TQ', 'NOMB TQ', 'PDV', 
                                'UNIDADES', 'PDV TQ', 'CONCATENADO', 'FORMATO'
                            ]
            pertenencia_nor (str): Nombre de la pagina del cliente en la maestra
            ref client (str): Nombre del cliente.
            pertenencia(str): Es la clase a la que pertenece el cliente
    
        Returns:
            resultado (DataFrame): Conjunto de artículos con su respectivo punto de venta TQ
                               
            sin_precio (DataFrame): Conjunto de artículos a los que no se le logro hallar 
                                el precio.
    """
    
    if pertenencia=="MAYORISTAS":
        ruta_maestra="Lista de Precios historico - Salvador.xlsx"
        hoja="MAYORISTAS"
    elif pertenencia=="CADENAS":
        ruta_maestra="Lista de Precios historico - Salvador.xlsx"
        hoja="CADENAS"
    elif pertenencia=="DEPOSITOS":
        ruta_maestra="Lista de Precios historico - Salvador.xlsx"
        hoja="DEPOSITOS"
    bases_nor=data[(data["COD NEG"] == 7) | (data["COD NEG"] == 82) ]
    data_precios_nor=pd.read_excel("{}\{}".format(inputPathMaestras, "Lista de Precios MK-NOR - Salvador.xlsx"), sheet_name=pertenencia_nor, header=0)
    data_precios=pd.read_excel("{}\{}".format(inputPathMaestras, "Lista Precios - Salvador.xlsx"), sheet_name=pertenencia, header=0)
    #lp_hist = pd.read_excel("{}/{}".format(inputPathMaestras, ruta_maestra),sheet_name=hoja, header=0)
    
    
    data_precios2=data_precios_nor.loc[:,['COD TQ','PRECIO']]
    data_precios2["COD TQ"]=data_precios2["COD TQ"].astype(np.int64)
    bases_nor = bases_nor[bases_nor["COD TQ"] != "Descontinuado"]
    bases_nor["COD TQ"]=bases_nor["COD TQ"].astype(np.int64)
    data["COD TQ"]=data["COD TQ"].astype(np.int64)
    #consolidamos precios
    consolidado=data.merge(data_precios2[['COD TQ','PRECIO']], how="left", on="COD TQ")
    data_precios3=data_precios2
    consolidado_conprecio=consolidado[consolidado['PRECIO'].notnull()]
    consolidado2=consolidado[consolidado['PRECIO'].isnull()]
    consolidado2.drop(['PRECIO'], axis=1, inplace=True)
    
    data_precios2=data_precios.loc[:,['COD TQ','PRECIO']]
    data_precios2["COD TQ"]=data_precios2["COD TQ"].astype(np.int64)
    bases_nor["COD TQ"]=data["COD TQ"].astype(np.int64)
    data_precios3=data_precios3.append(data_precios2)
    #consolidamos precios
    consolidado=consolidado2.merge(data_precios2[['COD TQ','PRECIO']], how="left", on="COD TQ")
    consolidados=consolidado_conprecio.append(consolidado)
    
    
    #buscamos en el historial de precios
    consolidado_conprecio=consolidados[consolidados['PRECIO'].notnull()]
    consolidado2=consolidados[consolidados['PRECIO'].isnull()]    
    consolidado_sinprecio,sinprecio=set_price_hist(consolidado2,ref_cliente,hoja)
    consolidados2=consolidado_conprecio.append(consolidado_sinprecio)
    consolidadosinprecio=consolidados2[consolidados2['PRECIO']==0]
    
    no_codigos = consolidados2[pd.isnull(consolidados2["PRECIO"])]
    if len(no_codigos) > 0:
        print("No se logró obtener los precios para: " + no_codigos.loc[:,["COD TQ"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los precios",
            "result": no_codigos.loc[:, ["COD TQ',"]].drop_duplicates().to_json(orient="split")
        })
    """
    
    return consolidados2,consolidadosinprecio



def set_price_nor_aliados(data,ref_cliente,pertenencia_nor,pertenencia):
    """
    Hallar el precio neto de cada artículo buscando primero en la lista del cliente aliados,
    luego en la lista nor despues en la list precios a la que pertenece el cliente y luego por
    el historial de precios.

    Parameters:
        data (DataFrame): Conjunto de artículos. Debe tener las columnas:
                        [
                            'VTA_INV', 'COD CLIENTE', 'COD TQ', 'NOMB TQ', 'PDV', 
                            'UNIDADES', 'PDV TQ', 'CONCATENADO', 'FORMATO'
                        ]
        pertenencia_nor (str): Nombre de la pagina del cliente en la maestra
        ref client (str): Nombre del cliente.
        pertenencia(str): Es la clase a la que pertenece el cliente

    Returns:
        resultado (DataFrame): Conjunto de artículos con su respectivo punto de venta TQ
                           
        sin_precio (DataFrame): Conjunto de artículos a los que no se le logro hallar 
                            el precio.
    """
    if pertenencia=="MAYORISTAS":
        ruta_maestra="Lista de Precios historico - Salvador.xlsx"
        hoja="MAYORISTAS"
    elif pertenencia=="CADENAS":
        ruta_maestra="Lista de Precios historico - Salvador.xlsx"
        hoja="CADENAS"
    bases_nor=data[(data["COD NEG"] == 7) | (data["COD NEG"] == 82) ]
    data_precios_nor=pd.read_excel("{}\{}".format(inputPathMaestras, "Lista de Precios MK-NOR - Salvador.xlsx"), sheet_name=pertenencia_nor, header=0)
    data_precios_aliados=pd.read_excel("{}\{}".format(inputPathMaestras, "Lista Precios - Salvador.xlsx"), sheet_name="CADENAS ALIADAS", header=0)
    data_precios=pd.read_excel("{}\{}".format(inputPathMaestras, "Lista Precios - Salvador.xlsx"), sheet_name=pertenencia, header=0)
    #lp_hist = pd.read_excel("{}/{}".format(inputPathMaestras, ruta_maestra),sheet_name=hoja, header=0)
    
    
    ##buscamos precios en lista de aliados
    data_precios_aliados=data_precios_aliados.loc[:,['COD TQ','PRECIO']]
    data_precios_aliados["COD TQ"]=data_precios_aliados["COD TQ"].astype(np.int64)
    data_precios2=data_precios_nor.loc[:,['COD TQ','PRECIO']]
    data_precios2["COD TQ"]=data_precios2["COD TQ"].astype(np.int64)
    bases_nor = bases_nor[bases_nor["COD TQ"] != "Descontinuado"]
    bases_nor["COD TQ"]=bases_nor["COD TQ"].astype(np.int64)
    data["COD TQ"]=data["COD TQ"].astype(np.int64)
    #consolidamos precios
    
    conso=data.merge(data_precios_aliados[['COD TQ','PRECIO']], how="left", on="COD TQ")
    conso_conpre=conso[conso['PRECIO'].notnull()]
    conso_sinpre=conso[conso['PRECIO'].isnull()]
    conso_sinpre.drop(['PRECIO'], axis=1, inplace=True)
    
    ##buscamos en la lista nor 
    
    consolidado=conso_sinpre.merge(data_precios2[['COD TQ','PRECIO']], how="left", on="COD TQ")
    data_precios3=data_precios2
    consolidado_conprecio=consolidado[consolidado['PRECIO'].notnull()]
    consolidado2=consolidado[consolidado['PRECIO'].isnull()]
    consolidado2.drop(['PRECIO'], axis=1, inplace=True)
    ##buscamos en la lista de precios normal
    data_precios2=data_precios.loc[:,['COD TQ','PRECIO']]
    data_precios2["COD TQ"]=data_precios2["COD TQ"].astype(np.int64)
    bases_nor["COD TQ"]=bases_nor["COD TQ"].astype(np.int64)
    data_precios3=data_precios3.append(data_precios2)
    #consolidamos precios
    consolidado=consolidado2.merge(data_precios2[['COD TQ','PRECIO']], how="left", on="COD TQ")    
    consolidados=consolidado_conprecio.append(consolidado)
    consolidados=consolidados.append(conso_conpre)    
    #buscamos en el historial de precios
    consolidado_conprecio=consolidados[consolidados['PRECIO'].notnull()]
    consolidado2=consolidados[consolidados['PRECIO'].isnull()]     
    ##buscamos en el historial de precios
    consolidado_sinprecio,sinprecio=set_price_hist(consolidado2,ref_cliente,hoja)
    consolidados2=consolidado_conprecio.append(consolidado_sinprecio)
    consolidadosinprecio=consolidados2[consolidados2['PRECIO']==0]
    
    no_codigos = consolidados2[pd.isnull(consolidados2["PRECIO"])]
    if len(no_codigos) > 0:
        print("No se logró obtener los precios para: " + no_codigos.loc[:,["DESCRIPCIÓN"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los precios",
            "result": no_codigos.loc[:, ["DESCRIPCIÓN',"]].drop_duplicates().to_json(orient="split")
        })
    """
       
    return consolidados2,consolidadosinprecio
    
def set_price(data, page_client, class_client, client,hoja):
    """
    Hallar el precio neto de cada artículo buscando primero en la lista del cliente,
    luego en la lista de la clase a la que pertenece el cliente y luego por
    el historial de precios.

    Parameters:
        data (DataFrame): Conjunto de artículos. Debe tener las columnas:
                        [
                            'VTA_INV', 'COD CLIENTE', 'COD TQ', 'NOMB TQ', 'PDV', 
                            'UNIDADES', 'PDV TQ', 'CONCATENADO', 'FORMATO'
                        ]
        page_client (str): Nombre de la pagina del cliente en la maestra
        client (str): Nombre del cliente.
        class_client(str): Es la clase a la que pertenece el cliente

    Returns:
        resultado (DataFrame): Conjunto de artículos con su respectivo punto de venta TQ
                            [
                                'VTA_INV', 'COD CLIENTE', 'COD TQ', 'NOMB TQ', 'PDV', 
                                'UNIDADES', 'PDV TQ', 'PRECIO NETO'
                            ]
        sin_precio (DataFrame): Conjunto de artículos a los que no se le logro hallar 
                            el precio.
    """

    # Listado de precios del cliente
    lp_cliente = pd.read_excel("{}/{}".format(inputPathMaestras, "Lista Precios Salvador Triim IV-2018.xlsx"),
                            sheet_name=page_client, header=4)
    lp_cliente.drop("Unnamed: 0", axis=1, inplace=True)

    # Listado de precios de la clase a la que pertenece el cliente
    lp_clase = pd.read_excel("{}/{}".format(inputPathMaestras, "Lista Precios Salvador Triim IV-2018.xlsx"),
                            sheet_name=class_client, header=3)

    # Listado historico
    lp_hist = pd.read_excel("{}/{}".format(inputPathMaestras, "Lista de Precios MK-NOR - Salvador.xlsx"),
                            sheet_name=hoja, header=1)
    # Se elimina los duplicados dejando los mas recientes del cliente
    lp_hist = lp_hist[lp_hist["NOMBRE CLIENTE"].str.contains(client, case=False)].sort_values(
        "Formato Fecha", ascending=False).groupby("COD TQ").first().reset_index()[["COD TQ", "CIF NETO"]]
    lp_hist['COD TQ'] = lp_hist['COD TQ'].astype(str)
    
    # Se unen la lista de precios del cliente con la de su clase
    list_precios = pd.concat([lp_cliente, lp_clase]).groupby("Código Tq").first().reset_index()
    list_precios['Código Tq'] = list_precios['Código Tq'].astype(str)
    
    ## Se busca en la lista de precio los precios de los articulos
    data = data.merge(list_precios[["Código Tq", "Precio Neto"]], how="left", left_on="COD TQ", right_on="Código Tq")
    ## Se obtiene los que no se logro obtener el precio
    sin_precio = data[data["Precio Neto"].isna()].merge(lp_hist, how="left", on="COD TQ")
    sin_precio.drop(["Precio Neto"], axis=1, inplace=True)
    sin_precio.rename(columns={"CIF NETO": "Precio Neto"}, inplace=True)
    ## Se juntan los precios de lista de precio con histórico
    data = data[data["Precio Neto"].notna()].append(sin_precio)
    data.drop("Código Tq", axis=1, inplace=True)
    
    if ('UNIDADES' in data.columns):
        data["TOTAL"] = data["UNIDADES"] * data["Precio Neto"]

    sin_precio = data[data["Precio Neto"].isna()]
    
    no_codigos = sin_precio
    if len(no_codigos) > 0:
        print("No se logró obtener los precios para: " + no_codigos.loc[:,["DESCRIPCIÓN"]].drop_duplicates().to_json(orient="split"))
    """    
        raise Exception({
            "status": "ERROR",
            "message": "No se logró obtener los precios",
            "result": no_codigos.loc[:, ["DESCRIPCIÓN',"]].drop_duplicates().to_json(orient="split")
        })
    """

    return data, sin_precio

def get_consolidated_report_deposito(data):
    """
    Se contruye el reporte CONSOLIDADO a partir de un conjunto de articulos del cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos del cliente
    
    Returns
        consolidado (Dataframe): Reporte consolidado
        COD TQ	COD NEGOCIO	MUNICIPIO	COD ESTABLECIMIENTO	ESTABLECIMIENTO	CONCATENADO GRUPO	GRUPO	COD PRODUCTO	DESCRIPCIÓN	UNIDADES	PRECIO	TIPO	FORMATO


    """
    consolidado = data.rename(columns={"PDV TQ": "COD PDV", "COD CLIENTE": "COD PRODUCTO", "NOMB TQ": "DESCRIPCIÓN", "VTA_INV": "TIPO", "CONCATENADO": "CONCATE", "Precio Neto": "PRECIO"})   
    consolidado = consolidado[["COD TQ","MUNICIPIO", "COD ESTABLECIMIENTO"	"ESTABLECIMIENTO", "GRUPO",	"COD PRODUCTO",	"DESCRIPCIÓN","UNIDADES","PRECIO","TIPO","FORMATO"]]
    return consolidado

def get_consolidated_report_mayoristas(data):
    """
    Se contruye el reporte CONSOLIDADO a partir de un conjunto de articulos del cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos del cliente
    
    Returns
        consolidado (Dataframe): Reporte consolidado
        COD TQ,	COD PRODUCTO,	DESCRIPCIÓN,	PRESENTACIÓN,		UNIDADES,	PRECIO,	TIPO,	FORMATO

    """
    consolidado = data.rename(columns={"PDV TQ": "COD PDV", "COD CLIENTE": "CODIGO", "NOMB TQ": "DESCRIPCION", "VTA_INV": "TIPO", "CONCATENADO": "CONCATE", "Precio Neto": "PRECIO"})    
    consolidado = consolidado[["COD TQ",  "COD PRODUCTO", "DESCRIPCIÓN", "PRESENTACIÓN", "UNIDADES", "PRECIO", "TIPO","COD NEG", "FORMATO"]]
    return consolidado


def get_consolidated_report_depositos_su(data):
    """
    Se contruye el reporte CONSOLIDADO a partir de un conjunto de articulos del cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos del cliente
    
    Returns
    COD TQ	MUNICIPIO	COD ESTABLECIMIENTO	ESTABLECIMIENTO	CLIENTES DETALLADOS		GRUPO	COD PRODUCTO	DESCRIPCIÓN	UNIDADES	PRECIO	TIPO	FORMATO


        consolidado (Dataframe): Reporte consolidado
    """
    if "CLIENTES DETALLADOS" not in data.columns:
        data["CLIENTES DETALLADOS"]=""
        
    data.rename(columns={ "Grupo establecimiento": "GRUPO"}, inplace=True)
    consolidado = data[["COD TQ", "MUNICIPIO","COD ESTABLECIMIENTO" ,"ESTABLECIMIENTO","CLIENTES DETALLADOS","GRUPO" ,"COD PRODUCTO", "DESCRIPCIÓN", "UNIDADES","PRECIO","TIPO","FORMATO"]]
    return consolidado

def get_consolidated_report_depositos(data):
    """
    Se contruye el reporte CONSOLIDADO a partir de un conjunto de articulos del cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos del cliente
    
    Returns
    COD TQ	MUNICIPIO	COD ESTABLECIMIENTO	ESTABLECIMIENTO	CLIENTES DETALLADOS		GRUPO	COD PRODUCTO	DESCRIPCIÓN	UNIDADES	PRECIO	TIPO	FORMATO


        consolidado (Dataframe): Reporte consolidado
    """
    if "CLIENTES DETALLADOS" not in data.columns:
        data["CLIENTES DETALLADOS"]=""
        
    data.rename(columns={ "Grupo establecimiento": "GRUPO"}, inplace=True)
    consolidado = data[["COD TQ", "MUNICIPIO","COD ESTABLECIMIENTO" ,"ESTABLECIMIENTO","CLIENTES DETALLADOS","GRUPO" ,"COD PRODUCTO", "DESCRIPCIÓN", "UNIDADES","UNIDADES DEF","PRECIO","TIPO","FORMATO"]]
    return consolidado

def get_consolidated_report_cadenas_su(data):
    """
    Se contruye el reporte CONSOLIDADO a partir de un conjunto de articulos del cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos del cliente
    
    Returns
  
        consolidado (Dataframe): Reporte consolidado
    """
    ##consolidado para cadenas cuando no reportan blisteamiento, solo unidades 
    if "NOMBRE PDV" not in data.columns:
        data['NOMBRE PDV']=""
    consolidado = data[["COD TQ", "CONCATENADO" ,"COD PRODUCTO",'COD NEG', "DESCRIPCIÓN", "COD PDV TQ","COD PDV","NOMBRE PDV",'COD NEG', "UNIDADES","PRECIO","TIPO","FORMATO"]]
    return consolidado
    


def get_form_report(data, extra_data, page_client):
    """
    Se construye el reporte de FORMA a partir del conjunto de articulos del cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos. Debe tener las siguientes columnas:
                        [
                            COD TQ", "CONCATENADO" ,"COD PRODUCTO", "DESCRIPCIÓN", "COD PDV TQ","COD PDV","UNIDADES","PRECIO","TIPO","FORMATO"
                        ]
        extra_data(dict): Diccionario con datos extra para el reportes:
                        ['ORDEN', 'MES_ORDEN', 'FORMATO_FECHA', 'COD_PAIS', 'PAIS', 
                        'COD_CANAL','CANAL', 'COD_CLIPADRE', 'REF_CLIPADRE', 'FLAG_CUA_BAS']
        page_client (str): Nombre de la pagina del cliente en la maestra
        client (str): Nombre del cliente.
        class_client(str): Es la clase a la que pertenece el cliente
    
    Returns:
        result (DataFrame): Reporte de articulos del cliente. Orden	Mes Orden	Formato Fecha	Cod Pais	País	Cod Canal	Canal	Cod Clipadre	Ref Cliente	COD TQ	Artículo	Presentación	Cod Negocio	Negocio	Cod Linea	Linea	Cod Marca	Marca	CIF NETO	Art Vigentes	Flag Cuadro Basico	Flag Seg Marca	Flag Prod Foco TG NOR	Flag Incentivos	plan recambio	estrategia de apoyo 	Cod Est Apoyo	Est Apoyo	Cod Agrupación	Agrupación	Evacuación	Inventario	Colocación 	 Evacuación Valores 	 Inventario Valores 	 Colocación Valores 	 Colocación V36 	Compañía

    """
    
    
    if "COD PDV TQ" not in data.columns:
        data['COD PDV TQ']=""
        
    if "COD NEG" not in data.columns:
        data['COD NEG']=""    
    ## Segregacion de las unidades en ventas e inventarios
    
    
    data = data.pivot_table("UNIDADES", ["COD TQ", "FORMATO", "COD NEG", "PRECIO"], "TIPO", aggfunc={
                            "UNIDADES": "sum"}).fillna(0).reset_index()    
    data.rename(columns={"INV": "INVENTARIO", "VTA": "EVACUACION"}, inplace=True)
    data = data.groupby("COD TQ").agg({"PRECIO": "first", "INVENTARIO": "sum", "EVACUACION": "sum", "FORMATO": "first"}).reset_index()

    # Se calcula los precios de la evacuacion y del inventario
    data["EVACUACION VALORES"] = data["PRECIO"] * data["EVACUACION"]
    data["INVENTARIO VALORES"] = data["PRECIO"] * data["INVENTARIO"]
    
    # Lectura del archivo de ventas e inventario
    venta_inv = pd.read_excel("{}/{}".format(inputPathMaestras, "Venta e Inventario Salvador.xlsx"),
                            sheet_name="Venta e Inventario Salvador", skiprows=2)
    venta_inventario = venta_inv.loc[:, ['Articulo', 'Mes', 'Canal', 'Cliente Padre', 'Cliente', 'Unidades vta comer' ,'Valor des com']]
    # Se modifica los tipos de datos en los campos a tratar
    venta_inventario["Articulo"] = venta_inventario["Articulo"].astype(np.int64)
    venta_inventario["Cliente"] = venta_inventario["Cliente"].astype(np.int64)
    data["COD TQ"] = data["COD TQ"].astype(np.int64)
    
    # se obtiene la venta e inventario del cliente
    venta_inventario = venta_inventario[(venta_inventario['Mes'] == extra_data["MES_ORDEN"]) & (
        venta_inventario['Cliente Padre'] == extra_data["COD_CLIPADRE"]) & (venta_inventario['Canal'] == extra_data["COD_CANAL"])]
    
    venta_inventario =venta_inventario[venta_inventario["Unidades vta comer"] != 0]
    
    data = data.merge(venta_inventario[['Articulo', 'Unidades vta comer', 'Valor des com']], how="left", left_on=["COD TQ"], right_on=["Articulo"])
    data.drop("Articulo", axis=1, inplace=True)
    data.rename(columns={"Unidades vta comer": "COLOCACION", "Valor des com": "COLOCACION V36"}, inplace=True)
    data = data.groupby(['COD TQ', 'PRECIO', 'INVENTARIO', 'EVACUACION', 'EVACUACION VALORES',
                         'INVENTARIO VALORES', "FORMATO"]).agg({"COLOCACION": "sum", "COLOCACION V36": "sum"}).reset_index()

    # Se obtiene los articulos que no registró el cliente
    resto = data.merge(venta_inventario, how="right", left_on="COD TQ", right_on="Articulo")
    resto = resto[resto["COD TQ"].isna()]
    resto = resto[['Articulo', 'Unidades vta comer', 'Valor des com']]
    resto.rename(columns={"Articulo": "COD TQ", "Unidades vta comer": "COLOCACION", "Valor des com": "COLOCACION V36"}, inplace=True)
    ## Se calcula los precios de los sobrantes
    if extra_data["COD_CANAL"]== 97:
        hoja="MAYORISTAS"
    elif extra_data["COD_CANAL"]== 91:
        hoja="CADENAS"
    elif extra_data["COD_CANAL"]== 92:
        if extra_data["REF_CLIENTE"]=="FARMACIA LAS AMERICAS":
            hoja="CADENAS"
        else:
            hoja="DEPOSITOS"    
    resto, sin_precio_resto = set_price_hist(resto, page_client,hoja)
    #resto =set_concatenated_and_format
   
    resto=set_format(resto,"MAESTRA EL SALVADOR")
    ## Se clasifica en bonima o tq
    resto['COD TQ']=resto['COD TQ'].astype(np.int64)
    #resto["FORMATO"] = resto.apply(lambda x: "BONIMA" if x["COD TQ"].startswith("300") else "TQ", axis=1)
    ## Se juntan los sobrantes al resto de artículos
    data = data.append(resto)
    maestra_cam_articulos = pd.read_excel("{}/{}".format(inputPathMaestras, 'Maestra Articulos CAM.xlsx'),
                                        sheet_name='MAESTRA EL SALVADOR', skiprows=2)
    maestra_cam_articulos = maestra_cam_articulos[['COD TQ', 'NOMBRE TQ', 'PRESENTACIÓN', 'COD NEG', 'NOMBRE NEG', 'COD LIN', 'NOMBRE LIN', 'COD MARCA',
                                                   'NOMBRE MARCA', 'Art Vigentes', 'Flag Seg Marca', 'Flag Prod Foco TG NOR', 'Flag Incentivos',
                                                   'plan recambio', 'Estrategia de apoyo ', 'Est Apoyo','Cod Est Apoyo','Cod Agrupación', 'Agrupación']]
    maestra_cam_articulos = maestra_cam_articulos.groupby('COD TQ').first().reset_index()
    maestra_cam_articulos["COD TQ"] = maestra_cam_articulos["COD TQ"].astype(np.int64)
    data = data.merge(maestra_cam_articulos, how="left", on="COD TQ").fillna(0)
    data["Orden"] = extra_data["ORDEN"]
    data["Mes Orden"] = extra_data["MES_ORDEN"]
    data["Formato Fecha"] = extra_data["FORMATO_FECHA"]
    data["Cod Pais"] = extra_data["COD_PAIS"]
    data["País"] = extra_data["PAIS"]
    data["Cod Canal"] = extra_data["COD_CANAL"]
    data["Canal"] = extra_data["CANAL"]
    data["Cod Clipadre"] = extra_data["COD_CLIPADRE"]
    data["Ref Cliente"] = extra_data["REF_CLIENTE"]
    # brasil_2["Colocación Depósitos"] = "NO"
    data["flag cuadro basico"] = extra_data["FLAG_CUA_BAS"]
    data["Colocación valores"] = data["PRECIO"] * data["COLOCACION"]

    data.rename(columns={"NOMBRE TQ": "ARTÍCULO", "COD NEG": "Cod Negocio", "NOMBRE NEG": "Negocio", "COD LIN": "Cod linea", "NOMBRE LIN": "Linea",
                         "NOMBRE MARCA": "Marca", "PRECIO": "CIF Neto", "FORMATO": "Compañía", "EVACUACION": "Evacuación",
                         "EVACUACION VALORES": "Evacuación valores", "COLOCACION": "Colocación", "COLOCACION VALORES": "Colocación valores" , "Cod Agrupación":"COD AGRUPACION","Cod Est Apoyo":"COD EST APOYO"}, inplace=True)

    data.columns = data.columns.str.strip().str.upper()
    data = data[["ORDEN", "MES ORDEN", "FORMATO FECHA", "COD PAIS", "PAÍS", "COD CANAL", "CANAL", "COD CLIPADRE", "REF CLIENTE", "COD TQ", "ARTÍCULO",
                 "PRESENTACIÓN", "COD NEGOCIO", "NEGOCIO", "COD LINEA", "LINEA", "COD MARCA", "MARCA", "CIF NETO", "ART VIGENTES", "FLAG CUADRO BASICO",
                 "FLAG SEG MARCA", "FLAG PROD FOCO TG NOR", "FLAG INCENTIVOS", "PLAN RECAMBIO", "ESTRATEGIA DE APOYO","COD EST APOYO", "EST APOYO", "COD AGRUPACION","AGRUPACIÓN",
                 "EVACUACIÓN", "INVENTARIO", "COLOCACIÓN", "EVACUACIÓN VALORES", "INVENTARIO VALORES", "COLOCACIÓN VALORES", "COLOCACION V36", "COMPAÑÍA"]]

    return data,resto



def get_form_report_NOR(data, extra_data, page_client,aliado,blistea):
    """
    Se construye el reporte de FORMA a partir del conjunto de articulos del cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos. Debe tener las siguientes columnas:
                        [
                            COD TQ", "CONCATENADO" ,"COD PRODUCTO", "DESCRIPCIÓN", "COD PDV TQ","COD PDV","UNIDADES","PRECIO","TIPO","FORMATO"
                        ]
        extra_data(dict): Diccionario con datos extra para el reportes:
                        ['ORDEN', 'MES_ORDEN', 'FORMATO_FECHA', 'COD_PAIS', 'PAIS', 
                        'COD_CANAL','CANAL', 'COD_CLIPADRE', 'REF_CLIPADRE', 'FLAG_CUA_BAS']
        page_client (str): Nombre de la pagina del cliente en la maestra
        client (str): Nombre del cliente.
        class_client(str): Es la clase a la que pertenece el cliente
    
    Returns:
        result (DataFrame): Reporte de articulos del cliente. Orden	Mes Orden	Formato Fecha	Cod Pais	País	Cod Canal	Canal	Cod Clipadre	Ref Cliente	COD TQ	Artículo	Presentación	Cod Negocio	Negocio	Cod Linea	Linea	Cod Marca	Marca	CIF NETO	Art Vigentes	Flag Cuadro Basico	Flag Seg Marca	Flag Prod Foco TG NOR	Flag Incentivos	plan recambio	estrategia de apoyo 	Cod Est Apoyo	Est Apoyo	Cod Agrupación	Agrupación	Evacuación	Inventario	Colocación 	 Evacuación Valores 	 Inventario Valores 	 Colocación Valores 	 Colocación V36 	Compañía

    """
  
    
    if "COD PDV TQ" not in data.columns:
        data['COD PDV TQ']=""
        
    if "COD NEG" not in data.columns:
        data['COD NEG']=""    
    ## Segregacion de las unidades en ventas e inventarios
    if blistea==0:
        
        data = data.pivot_table("UNIDADES", ["COD TQ", "FORMATO", "COD NEG", "PRECIO"], "TIPO", aggfunc={
                                "UNIDADES": "sum"}).fillna(0).reset_index()       
        
        data.rename(columns={"INV": "INVENTARIO", "VTA": "EVACUACION"}, inplace=True)
        data = data.groupby("COD TQ").agg({"PRECIO": "first", "INVENTARIO": "sum", "EVACUACION": "sum", "FORMATO": "first"}).reset_index()
    
        # Se calcula los precios de la evacuacion y del inventario
        data["EVACUACION VALORES"] = data["PRECIO"] * data["EVACUACION"]
        data["INVENTARIO VALORES"] = data["PRECIO"] * data["INVENTARIO"]
    elif blistea==1:
        data = data.pivot_table("UNIDADES DEF", ["COD TQ", "FORMATO", "COD NEG", "PRECIO"], "TIPO", aggfunc={
                                "UNIDADES DEF": "sum"}).fillna(0).reset_index()
        
        
        data.rename(columns={"INV": "INVENTARIO", "VTA": "EVACUACION"}, inplace=True)
        data = data.groupby("COD TQ").agg({"PRECIO": "first", "INVENTARIO": "sum", "EVACUACION": "sum", "FORMATO": "first"}).reset_index()
    
        # Se calcula los precios de la evacuacion y del inventario
        data["EVACUACION VALORES"] = data["PRECIO"] * data["EVACUACION"]
        data["INVENTARIO VALORES"] = data["PRECIO"] * data["INVENTARIO"]
        
    
    # Lectura del archivo de ventas e inventario
    venta_inv = pd.read_excel("{}/{}".format(inputPathMaestras, "Venta e Inventario Salvador.xlsx"),
                            sheet_name="Venta e Inventario Salvador", skiprows=2)
    venta_inventario = venta_inv.loc[:, ['Articulo', 'Mes', 'Canal', 'Cliente Padre', 'Cliente', 'Unidades vta comer' ,'Valor des com']]
    # Se modifica los tipos de datos en los campos a tratar
    venta_inventario["Articulo"] = venta_inventario["Articulo"].astype(np.int64)
    venta_inventario["Cliente"] = venta_inventario["Cliente"].astype(np.int64)
    data["COD TQ"] = data["COD TQ"].astype(np.int64)
    
    # se obtiene la venta e inventario del cliente
    venta_inventario = venta_inventario[(venta_inventario['Mes'] == extra_data["MES_ORDEN"]) & (venta_inventario['Cliente Padre'] == extra_data["COD_CLIPADRE"]) & (venta_inventario['Canal'] == extra_data["COD_CANAL"])]
    
    venta_inventario =venta_inventario[(venta_inventario["Unidades vta comer"] != 0) | (venta_inventario["Valor des com"] != 0)]
    
    data = data.merge(venta_inventario[['Articulo', 'Unidades vta comer', 'Valor des com']], how="left", left_on=["COD TQ"], right_on=["Articulo"])
    data.drop("Articulo", axis=1, inplace=True)
    data.rename(columns={"Unidades vta comer": "COLOCACION", "Valor des com": "COLOCACION V36"}, inplace=True)
    data = data.groupby(['COD TQ', 'PRECIO', 'INVENTARIO', 'EVACUACION', 'EVACUACION VALORES',
                         'INVENTARIO VALORES', "FORMATO"]).agg({"COLOCACION": "sum", "COLOCACION V36": "sum"}).reset_index()

    # Se obtiene los articulos que no registró el cliente
    resto = data.merge(venta_inventario, how="right", left_on="COD TQ", right_on="Articulo")
    resto = resto[resto["COD TQ"].isna()]
    resto = resto[['Articulo', 'Unidades vta comer', 'Valor des com']]
    resto.rename(columns={"Articulo": "COD TQ", "Unidades vta comer": "COLOCACION", "Valor des com": "COLOCACION V36"}, inplace=True)
    ## Se calcula los precios de los sobrantes
    if extra_data["COD_CANAL"]== 97:
        hoja="MAYORISTAS"
        sheet="Lista de Precios Mayoristas"
    elif extra_data["COD_CANAL"]== 91:
        hoja="CADENAS"
        sheet="Lista de Precios Cadenas"
    elif extra_data["COD_CANAL"]== 92:
        hoja="DEPOSITOS"         
        sheet="Lista de Precios Depósitos"
        
    
    if "COD NEG" in resto.columns:
        
        resto.drop("COD NEG", axis=1, inplace=True)
    resto=set_concatenated_and_format(resto,"MAESTRA EL SALVADOR")
    if aliado==0:        
        resto, sin_precio_resto = set_price_nor(resto, page_client,sheet,hoja)
    elif aliado==1:
         resto, sin_precio_resto = set_price_nor_aliados(resto, page_client,sheet,hoja)
    ## Se clasifica en bonima o tq
    resto['COD TQ']=resto['COD TQ'].astype(np.int64)
    #resto["FORMATO"] = resto.apply(lambda x: "BONIMA" if x["COD TQ"].startswith("300") else "TQ", axis=1)
    ## Se juntan los sobrantes al resto de artículos
    data = data.append(resto).fillna(0)
    
    data.drop("COD NEG", axis=1, inplace=True)
    maestra_cam_articulos = pd.read_excel("{}/{}".format(inputPathMaestras, 'Maestra Articulos CAM.xlsx'),
                                        sheet_name='MAESTRA EL SALVADOR', skiprows=2)
    maestra_cam_articulos = maestra_cam_articulos[['COD TQ', 'NOMBRE TQ', 'PRESENTACIÓN', 'COD NEG', 'NOMBRE NEG', 'COD LIN', 'NOMBRE LIN', 'COD MARCA',
                                                   'NOMBRE MARCA', 'Art Vigentes', 'Flag Seg Marca', 'Flag Prod Foco TG NOR', 'Flag Incentivos',
                                                   'plan recambio', 'Estrategia de apoyo ', 'Est Apoyo','Cod Est Apoyo','Cod Agrupación', 'Agrupación']]
    maestra_cam_articulos = maestra_cam_articulos.groupby('COD TQ').first().reset_index()
    maestra_cam_articulos["COD TQ"] = maestra_cam_articulos["COD TQ"].astype(np.int64)

    data = data.merge(maestra_cam_articulos, how="left", on="COD TQ").fillna(0)

    data["Orden"] = extra_data["ORDEN"]
    data["Mes Orden"] = extra_data["MES_ORDEN"]
    data["Formato Fecha"] = extra_data["FORMATO_FECHA"]
    data["Cod Pais"] = extra_data["COD_PAIS"]
    data["País"] = extra_data["PAIS"]
    data["Cod Canal"] = extra_data["COD_CANAL"]
    data["Canal"] = extra_data["CANAL"]
    data["Cod Clipadre"] = extra_data["COD_CLIPADRE"]
    data["Ref Cliente"] = extra_data["REF_CLIENTE"]
    # brasil_2["Colocación Depósitos"] = "NO"
    data["flag cuadro basico"] = extra_data["FLAG_CUA_BAS"]
    data["Colocación valores"] = data["PRECIO"] * data["COLOCACION"]
    
    data.rename(columns={"NOMBRE TQ": "ARTÍCULO", "COD NEG": "Cod Negocio", "NOMBRE NEG": "Negocio", "COD LIN": "Cod linea", "NOMBRE LIN": "Linea",
                         "NOMBRE MARCA": "Marca", "PRECIO": "CIF Neto", "FORMATO": "Compañía", "EVACUACION": "Evacuación",
                         "EVACUACION VALORES": "Evacuación valores", "COLOCACION": "Colocación", "COLOCACION VALORES": "Colocación valores" , "Cod Agrupación":"COD AGRUPACION","Cod Est Apoyo":"COD EST APOYO"}, inplace=True)

    data.columns = data.columns.str.strip().str.upper()
    data = data[["ORDEN", "MES ORDEN", "FORMATO FECHA", "COD PAIS", "PAÍS", "COD CANAL", "CANAL", "COD CLIPADRE", "REF CLIENTE", "COD TQ", "ARTÍCULO",
                 "PRESENTACIÓN", "COD NEGOCIO", "NEGOCIO", "COD LINEA", "LINEA", "COD MARCA", "MARCA", "CIF NETO", "ART VIGENTES", "FLAG CUADRO BASICO",
                 "FLAG SEG MARCA", "FLAG PROD FOCO TG NOR", "FLAG INCENTIVOS", "PLAN RECAMBIO", "ESTRATEGIA DE APOYO","COD EST APOYO", "EST APOYO", "COD AGRUPACION","AGRUPACIÓN",
                 "EVACUACIÓN", "INVENTARIO", "COLOCACIÓN", "EVACUACIÓN VALORES", "INVENTARIO VALORES", "COLOCACIÓN VALORES", "COLOCACION V36", "COMPAÑÍA"]]

    return data
def get_form_report_NOR_depositos(data, extra_data, page_client,aliado,blistea):
    """
    Se construye el reporte de FORMA a partir del conjunto de articulos del cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos. Debe tener las siguientes columnas:
                        [
                            COD TQ", "CONCATENADO" ,"COD PRODUCTO", "DESCRIPCIÓN", "COD PDV TQ","COD PDV","UNIDADES","PRECIO","TIPO","FORMATO"
                        ]
        extra_data(dict): Diccionario con datos extra para el reportes:
                        ['ORDEN', 'MES_ORDEN', 'FORMATO_FECHA', 'COD_PAIS', 'PAIS', 
                        'COD_CANAL','CANAL', 'COD_CLIPADRE', 'REF_CLIPADRE', 'FLAG_CUA_BAS']
        page_client (str): Nombre de la pagina del cliente en la maestra
        client (str): Nombre del cliente.
        class_client(str): Es la clase a la que pertenece el cliente
    
    Returns:
        result (DataFrame): Reporte de articulos del cliente. Orden	Mes Orden	Formato Fecha	Cod Pais	País	Cod Canal	Canal	Cod Clipadre	Ref Cliente	COD TQ	Artículo	Presentación	Cod Negocio	Negocio	Cod Linea	Linea	Cod Marca	Marca	CIF NETO	Art Vigentes	Flag Cuadro Basico	Flag Seg Marca	Flag Prod Foco TG NOR	Flag Incentivos	plan recambio	estrategia de apoyo 	Cod Est Apoyo	Est Apoyo	Cod Agrupación	Agrupación	Evacuación	Inventario	Colocación 	 Evacuación Valores 	 Inventario Valores 	 Colocación Valores 	 Colocación V36 	Compañía

    """
  
    
    if "COD PDV TQ" not in data.columns:
        data['COD PDV TQ']=""
        
    if "COD NEG" not in data.columns:
        data['COD NEG']=""    
    ## Segregacion de las unidades en ventas e inventarios
    if blistea==0:
        
        data = data.pivot_table("UNIDADES", ["COD TQ", "FORMATO", "COD NEG", "PRECIO"], "TIPO", aggfunc={
                                "UNIDADES": "sum"}).fillna(0).reset_index()       
        
        data.rename(columns={"INV": "INVENTARIO", "VTA": "EVACUACION"}, inplace=True)
        data = data.groupby("COD TQ").agg({"PRECIO": "first", "INVENTARIO": "sum", "EVACUACION": "sum", "FORMATO": "first"}).reset_index()
    
        # Se calcula los precios de la evacuacion y del inventario
        data["EVACUACION VALORES"] = data["PRECIO"] * data["EVACUACION"]
        data["INVENTARIO VALORES"] = data["PRECIO"] * data["INVENTARIO"]
    elif blistea==1:
        data = data.pivot_table("UNIDADES DEF", ["COD TQ", "FORMATO", "COD NEG", "PRECIO"], "TIPO", aggfunc={
                                "UNIDADES DEF": "sum"}).fillna(0).reset_index()
        
        
        data.rename(columns={"INV": "INVENTARIO", "VTA": "EVACUACION"}, inplace=True)
        data = data.groupby("COD TQ").agg({"PRECIO": "first", "INVENTARIO": "sum", "EVACUACION": "sum", "FORMATO": "first"}).reset_index()
    
        # Se calcula los precios de la evacuacion y del inventario
        data["EVACUACION VALORES"] = data["PRECIO"] * data["EVACUACION"]
        data["INVENTARIO VALORES"] = data["PRECIO"] * data["INVENTARIO"]
        
    
    # Lectura del archivo de ventas e inventario
    venta_inv = pd.read_excel("{}/{}".format(inputPathMaestras, "Venta e Inventario Salvador.xlsx"),
                            sheet_name="Venta e Inventario Salvador", skiprows=2)
    venta_inventario = venta_inv.loc[:, ['Articulo', 'Mes', 'Canal', 'Cliente Padre', 'Cliente', 'Unidades vta comer' ,'Valor des com']]
    # Se modifica los tipos de datos en los campos a tratar
    venta_inventario["Articulo"] = venta_inventario["Articulo"].astype(np.int64)
    venta_inventario["Cliente"] = venta_inventario["Cliente"].astype(np.int64)
    data["COD TQ"] = data["COD TQ"].astype(np.int64)
    
    # se obtiene la venta e inventario del cliente
    venta_inventario = venta_inventario[(venta_inventario['Mes'] == extra_data["MES_ORDEN"]) & (venta_inventario['Cliente Padre'] == extra_data["COD_CLIPADRE"]) & (venta_inventario['Canal'] == extra_data["COD_CANAL"])]
    
    venta_inventario =venta_inventario[(venta_inventario["Unidades vta comer"] != 0) | (venta_inventario["Valor des com"] != 0)]
    
    data = data.merge(venta_inventario[['Articulo', 'Unidades vta comer', 'Valor des com']], how="left", left_on=["COD TQ"], right_on=["Articulo"])
    data.drop("Articulo", axis=1, inplace=True)
    data.rename(columns={"Unidades vta comer": "COLOCACION", "Valor des com": "COLOCACION V36"}, inplace=True)
    data = data.groupby(['COD TQ', 'PRECIO', 'INVENTARIO', 'EVACUACION', 'EVACUACION VALORES',
                         'INVENTARIO VALORES', "FORMATO"]).agg({"COLOCACION": "sum", "COLOCACION V36": "sum"}).reset_index()

    # Se obtiene los articulos que no registró el cliente
    resto = data.merge(venta_inventario, how="right", left_on="COD TQ", right_on="Articulo")
    resto = resto[resto["COD TQ"].isna()]
    resto = resto[['Articulo', 'Unidades vta comer', 'Valor des com']]
    resto.rename(columns={"Articulo": "COD TQ", "Unidades vta comer": "COLOCACION", "Valor des com": "COLOCACION V36"}, inplace=True)
    ## Se calcula los precios de los sobrantes
    if extra_data["COD_CANAL"]== 97:
        hoja="MAYORISTAS"
        sheet="Lista de Precios Mayoristas"
    elif extra_data["COD_CANAL"]== 91:
        hoja="CADENAS"
        sheet="Lista de Precios Cadenas"
    elif extra_data["COD_CANAL"]== 92:
        hoja="DEPOSITOS"         
        sheet="Lista de Precios Depósitos"
        
    
    if "COD NEG" in resto.columns:
        
        resto.drop("COD NEG", axis=1, inplace=True)
    resto=set_concatenated_and_format(resto,"MAESTRA EL SALVADOR")
    if aliado==0:        
        resto, sin_precio_resto = set_price_nor(resto, page_client,sheet,hoja)
    elif aliado==1:
         resto, sin_precio_resto = set_price_nor_aliados(resto, page_client,sheet,hoja)
    ## Se clasifica en bonima o tq
    resto['COD TQ']=resto['COD TQ'].astype(np.int64)
    #resto["FORMATO"] = resto.apply(lambda x: "BONIMA" if x["COD TQ"].startswith("300") else "TQ", axis=1)
    ## Se juntan los sobrantes al resto de artículos
    data = data.append(resto).fillna(0)
    
    data.drop("COD NEG", axis=1, inplace=True)
    maestra_cam_articulos = pd.read_excel("{}/{}".format(inputPathMaestras, 'Maestra Articulos CAM.xlsx'),
                                        sheet_name='MAESTRA EL SALVADOR', skiprows=2)
    maestra_cam_articulos = maestra_cam_articulos[['COD TQ', 'NOMBRE TQ', 'PRESENTACIÓN', 'COD NEG', 'NOMBRE NEG', 'COD LIN', 'NOMBRE LIN', 'COD MARCA',
                                                   'NOMBRE MARCA', 'Art Vigentes', 'Flag Seg Marca', 'Flag Prod Foco TG NOR', 'Flag Incentivos',
                                                   'plan recambio', 'Estrategia de apoyo ', 'Est Apoyo','Cod Est Apoyo','Cod Agrupación', 'Agrupación']]
    maestra_cam_articulos = maestra_cam_articulos.groupby('COD TQ').first().reset_index()
    maestra_cam_articulos["COD TQ"] = maestra_cam_articulos["COD TQ"].astype(np.int64)

    data = data.merge(maestra_cam_articulos, how="left", on="COD TQ").fillna(0)

    data["Orden"] = extra_data["ORDEN"]
    data["Mes Orden"] = extra_data["MES_ORDEN"]
    data["Formato Fecha"] = extra_data["FORMATO_FECHA"]
    data["Cod Pais"] = extra_data["COD_PAIS"]
    data["País"] = extra_data["PAIS"]
    data["Cod Canal"] = extra_data["COD_CANAL"]
    data["Canal"] = extra_data["CANAL"]
    data["Cod Clipadre"] = extra_data["COD_CLIPADRE"]
    data["Ref Cliente"] = extra_data["REF_CLIENTE"]
    # brasil_2["Colocación Depósitos"] = "NO"
    data["flag cuadro basico"] = extra_data["FLAG_CUA_BAS"]
    data["Colocación valores"] = data["PRECIO"] * data["COLOCACION"]
    
    data.rename(columns={"NOMBRE TQ": "ARTÍCULO", "COD NEG": "Cod Negocio", "NOMBRE NEG": "Negocio", "COD LIN": "Cod linea", "NOMBRE LIN": "Linea",
                         "NOMBRE MARCA": "Marca", "PRECIO": "CIF Neto", "FORMATO": "Compañía", "EVACUACION": "Evacuación",
                         "EVACUACION VALORES": "Evacuación valores", "COLOCACION": "Colocación", "COLOCACION VALORES": "Colocación valores" , "Cod Agrupación":"COD AGRUPACION","Cod Est Apoyo":"COD EST APOYO"}, inplace=True)
    
    ##Orden	Mes Orden	Formato Fecha	Cod Pais	País	Cod Canal	Canal	Cod Clipadre	Ref Cliente	COD TQ	Artículo	
    #Presentación	Cod Negocio	Negocio	Cod Linea	Linea	Cod Marca	Marca	CIF NETO	Art Vigentes	
    #Flag Seg Marca	Flag Prod Foco TG NOR	Flag Incentivos	plan recambio	estrategia de apoyo 	Cod Est Apoyo	Est Apoyo	Cod Agrupación	Agrupación	
    #Evacuación	Inventario	Colocación 	Evacuación Valores	Inventario Valores	Colocación Valores	Colocación V36	Compañía

    
    
    data.columns = data.columns.str.strip().str.upper()
    data = data[["ORDEN", "MES ORDEN", "FORMATO FECHA", "COD PAIS", "PAÍS", "COD CANAL", "CANAL", "COD CLIPADRE", "REF CLIENTE", "COD TQ", "ARTÍCULO",
                 "PRESENTACIÓN", "COD NEGOCIO", "NEGOCIO", "COD LINEA", "LINEA", "COD MARCA", "MARCA", "CIF NETO", "ART VIGENTES",
                 "FLAG SEG MARCA", "FLAG PROD FOCO TG NOR", "FLAG INCENTIVOS", "PLAN RECAMBIO", "ESTRATEGIA DE APOYO","COD EST APOYO", "EST APOYO", "COD AGRUPACION","AGRUPACIÓN",
                 "EVACUACIÓN", "INVENTARIO", "COLOCACIÓN", "EVACUACIÓN VALORES", "INVENTARIO VALORES", "COLOCACIÓN VALORES", "COLOCACION V36", "COMPAÑÍA"]]

    return data

def get_form_report_3_nor_depositos(data, extra_data,blistea):
    """
    Se construye el reporte de FORMA a partir del conjunto de articulos del cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos. Debe tener las siguientes columnas:
                        [
                            COD TQ", "CONCATENADO" ,"COD PRODUCTO", "DESCRIPCIÓN", "COD PDV TQ","COD PDV","UNIDADES","PRECIO","TIPO","FORMATO"
                        ]
        extra_data(dict): Diccionario con datos extra para el reportes:
                        ['ORDEN', 'MES_ORDEN', 'FORMATO_FECHA', 'COD_PAIS', 'PAIS', 
                        'COD_CANAL','CANAL', 'COD_CLIPADRE', 'REF_CLIPADRE', 'FLAG_CUA_BAS']
        page_client (str): Nombre de la pagina del cliente en la maestra
        client (str): Nombre del cliente.
        class_client(str): Es la clase a la que pertenece el cliente
    
    Returns:
        result (DataFrame): Reporte de articulos del cliente. Orden	Mes Orden	Formato Fecha	Cod Pais	País	Cod Canal	Canal	Cod Clipadre	Ref Cliente	COD TQ	Artículo	Presentación	Cod Negocio	Negocio	Cod Linea	Linea	Cod Marca	Marca	CIF NETO	Art Vigentes	Flag Cuadro Basico	Flag Seg Marca	Flag Prod Foco TG NOR	Flag Incentivos	plan recambio	estrategia de apoyo 	Cod Est Apoyo	Est Apoyo	Cod Agrupación	Agrupación	Evacuación	Inventario	Colocación 	 Evacuación Valores 	 Inventario Valores 	 Colocación Valores 	 Colocación V36 	Compañía

    """
    data["COD ESTABLECIMIENTO"].fillna(0, inplace=True)
    data["MUNICIPIO"].fillna("", inplace=True)
    data["CLIENTES DETALLADOS"].fillna("", inplace=True)
    data["ESTABLECIMIENTO"].fillna("", inplace=True)
    data["GRUPO"].fillna("", inplace=True)
    
    if "COD PDV TQ" not in data.columns:
        data['COD PDV TQ']=""
        
    if "COD NEG" not in data.columns:
        data['COD NEG']=""    
    ## Segregacion de las unidades en ventas e inventarios
    if blistea==0:
        
        data = data.pivot_table("UNIDADES", ["COD TQ", "FORMATO", "COD NEG", "PRECIO","GRUPO","ESTABLECIMIENTO","CLIENTES DETALLADOS","COD ESTABLECIMIENTO","MUNICIPIO"], "TIPO", aggfunc={
                                "UNIDADES": "sum"}).fillna(0).reset_index()       
        print("esto",data.columns)
        data.rename(columns={"INV": "INVENTARIO", "VTA": "EVACUACION"}, inplace=True)
        if "INVENTARIO" in data.columns:
            data.drop("INVENTARIO", axis=1, inplace=True)
        data=data[data.EVACUACION != 0]
        
        #data = data.groupby(["COD TQ","MUNICIPIO"]).agg({"PRECIO": "first", "EVACUACION": "sum", "FORMATO": "first",  "ESTABLECIMIENTO": "first", "CLIENTES DETALLADOS": "first", "COD ESTABLECIMIENTO": "first", "GRUPO": "first"}).reset_index()
    
        # Se calcula los precios de la evacuacion y del inventario
        data["EVACUACION VALORES"] = data["PRECIO"] * data["EVACUACION"]
        
    elif blistea==1:
        data = data.pivot_table("UNIDADES DEF", ["COD TQ", "FORMATO", "COD NEG", "PRECIO","GRUPO","ESTABLECIMIENTO","CLIENTES DETALLADOS","COD ESTABLECIMIENTO","MUNICIPIO"], "TIPO", aggfunc={
                                "UNIDADES DEF": "sum"}).fillna(0).reset_index()
        
        
        data.rename(columns={"INV": "INVENTARIO", "VTA": "EVACUACION"}, inplace=True)
        data.drop("INVENTARIO", axis=1, inplace=True)
        data=data[data.EVACUACION != 0]
        #data = data.groupby("COD TQ").agg({"PRECIO": "first",  "EVACUACION": "sum", "FORMATO": "first"}).reset_index()
    
        # Se calcula los precios de la evacuacion y del inventario
        data["EVACUACION VALORES"] = data["PRECIO"] * data["EVACUACION"]
        
   
    if "COD NEG" in data.columns:
        data.drop("COD NEG", axis=1, inplace=True)
    maestra_cam_articulos = pd.read_excel("{}/{}".format(inputPathMaestras, 'Maestra Articulos CAM.xlsx'),
                                        sheet_name='MAESTRA EL SALVADOR', skiprows=2)
    maestra_cam_articulos = maestra_cam_articulos[['COD TQ', 'NOMBRE TQ', 'PRESENTACIÓN', 'COD NEG', 'NOMBRE NEG', 'COD LIN', 'NOMBRE LIN', 'COD MARCA',
                                                   'NOMBRE MARCA', 'Art Vigentes', 'Flag Seg Marca', 'Flag Prod Foco TG NOR', 'Flag Incentivos',
                                                   'plan recambio', 'Estrategia de apoyo ', 'Est Apoyo','Cod Est Apoyo','Cod Agrupación', 'Agrupación']]
    maestra_cam_articulos = maestra_cam_articulos.groupby('COD TQ').first().reset_index()
    maestra_cam_articulos["COD TQ"] = maestra_cam_articulos["COD TQ"].astype(np.int64)

    data = data.merge(maestra_cam_articulos, how="left", on="COD TQ").fillna(0)

    data["Orden"] = extra_data["ORDEN"]
    data["Mes Orden"] = extra_data["MES_ORDEN"]
    data["Formato Fecha"] = extra_data["FORMATO_FECHA"]
    data["Cod Pais"] = extra_data["COD_PAIS"]
    data["País"] = extra_data["PAIS"]
    data["Cod Canal"] = extra_data["COD_CANAL"]
    data["Canal"] = extra_data["CANAL"]
    data["Cod Clipadre"] = extra_data["COD_CLIPADRE"]
    data["Ref Cliente"] = extra_data["REF_CLIENTE"]
    # brasil_2["Colocación Depósitos"] = "NO"
    data["flag cuadro basico"] = extra_data["FLAG_CUA_BAS"]
    
    
    data.rename(columns={"NOMBRE TQ": "ARTÍCULO", "COD NEG": "Cod Negocio", "NOMBRE NEG": "Negocio", "COD LIN": "Cod linea", "NOMBRE LIN": "Linea",
                         "NOMBRE MARCA": "Marca", "PRECIO": "CIF Neto", "FORMATO": "Compañía", "EVACUACION": "Evacuación",
                         "EVACUACION VALORES": "Evacuación valores", "COLOCACION": "Colocación", "COLOCACION VALORES": "Colocación valores" , "Cod Agrupación":"COD AGRUPACION","Cod Est Apoyo":"COD EST APOYO","GRUPO":"GRUPO ESTABLECIMIENTO"}, inplace=True)
    
    ##ORDEN	MES ORDEN	FORMATO FECHA	COD PAIS	PAÍS	COD CANAL	CANAL	AGRUPACIÓN CANAL	COD CLIPADRE	REF CLIENTE	MUNICIPIO	COD ESTABLECIMIENTO	ESTABLECIMIENTO	CLIENTES DETALLADOS	GRUPO ESTABLECIMIENTO	COD TQ	ARTÍCULO	
    #PRESENTACIÓN	COD NEGOCIO	NEGOCIO	COD LINEA	LINEA	COD MARCA	MARCA	CIF NETO	ART VIGENTES
#	FLAG SEG MARCA	FLAG PROD FOCO TG NOR	FLAG INCENTIVOS	PLAN RECAMBIO	ESTRATEGIA DE APOYO 	COD EST APOYO	EST APOYO	COD AGRUPACIÓN	AGRUPACIÓN	
#EVACUACIÓN	EVACUACIÓN VALORES	COMPAÑÍA


    if "AGRUPACIÓN CANAL" not in data.columns:
        data['AGRUPACIÓN CANAL']=""
    print (data.columns)
    data.columns = data.columns.str.strip().str.upper()
    data = data[["ORDEN", "MES ORDEN", "FORMATO FECHA", "COD PAIS", "PAÍS", "COD CANAL", "CANAL", "AGRUPACIÓN CANAL","COD CLIPADRE", "REF CLIENTE", "MUNICIPIO", "COD ESTABLECIMIENTO", "ESTABLECIMIENTO", "CLIENTES DETALLADOS", "GRUPO ESTABLECIMIENTO", "COD TQ", "ARTÍCULO",
                 "PRESENTACIÓN", "COD NEGOCIO", "NEGOCIO", "COD LINEA", "LINEA", "COD MARCA", "MARCA", "CIF NETO", "ART VIGENTES",
                 "FLAG SEG MARCA", "FLAG PROD FOCO TG NOR", "FLAG INCENTIVOS", "PLAN RECAMBIO", "ESTRATEGIA DE APOYO","COD EST APOYO", "EST APOYO", "COD AGRUPACION","AGRUPACIÓN",
                 "EVACUACIÓN",  "EVACUACIÓN VALORES", "COMPAÑÍA"]]

    return data

def get_form_report_mayorista(data, extra_data, page_client,aliado,blistea):
    """
    Se construye el reporte de FORMA a partir del conjunto de articulos del cliente.

    Parameters:
        data (DataFrame): Conjunto de artículos. Debe tener las siguientes columnas:
                        [
                            COD TQ", "CONCATENADO" ,"COD PRODUCTO", "DESCRIPCIÓN", "COD PDV TQ","COD PDV","UNIDADES","PRECIO","TIPO","FORMATO"
                        ]
        extra_data(dict): Diccionario con datos extra para el reportes:
                        ['ORDEN', 'MES_ORDEN', 'FORMATO_FECHA', 'COD_PAIS', 'PAIS', 
                        'COD_CANAL','CANAL', 'COD_CLIPADRE', 'REF_CLIPADRE', 'FLAG_CUA_BAS']
        page_client (str): Nombre de la pagina del cliente en la maestra
        client (str): Nombre del cliente.
        class_client(str): Es la clase a la que pertenece el cliente
    
    Returns:
        result (DataFrame): Reporte de articulos del cliente.
    """
    if "COD PDV TQ" not in data.columns:
        data['COD PDV TQ']=""
    if "COD NEG" not in data.columns:
        data['COD NEG']=""
    ## Segregacion de las unidades en ventas e inventarios
    data = data.pivot_table("UNIDADES", ["COD TQ", "FORMATO", "COD NEG", "PRECIO"], "TIPO", aggfunc={
                            "UNIDADES": "sum"}).fillna(0).reset_index()
    
    data.rename(columns={"INV": "INVENTARIO", "VTA": "EVACUACION"}, inplace=True)
    data = data.groupby("COD TQ").agg({"PRECIO": "first", "INVENTARIO": "sum", "EVACUACION": "sum", "FORMATO": "first","COD NEG": "first"}).reset_index()

    # Se calcula los precios de la evacuacion y del inventario
    data["EVACUACION VALORES"] = data["PRECIO"] * data["EVACUACION"]
    data["INVENTARIO VALORES"] = data["PRECIO"] * data["INVENTARIO"]
    
    # Lectura del archivo de ventas e inventario
    venta_inv = pd.read_excel("{}/{}".format(inputPathMaestras, "Venta e Inventario Salvador.xlsx"),
                            sheet_name="Venta e Inventario Salvador", skiprows=2)
    venta_inventario = venta_inv.loc[:, ['Articulo', 'Mes', 'Canal', 'Cliente Padre', 'Cliente', 'Unidades vta comer' ,'Valor des com']]
    # Se modifica los tipos de datos en los campos a tratar
    venta_inventario["Articulo"] = venta_inventario["Articulo"].astype(np.int64)
    venta_inventario["Cliente"] = venta_inventario["Cliente"].astype(np.int64)
    data["COD TQ"] = data["COD TQ"].astype(np.int64)
    
    # se obtiene la venta e inventario del cliente
    venta_inventario = venta_inventario[(venta_inventario['Mes'] == extra_data["MES_ORDEN"]) & (
        venta_inventario['Cliente Padre'] == extra_data["COD_CLIPADRE"]) & (venta_inventario['Canal'] == extra_data["COD_CANAL"])]
    
    venta_inventario =venta_inventario[venta_inventario["Unidades vta comer"] != 0]
    
    data = data.merge(venta_inventario[['Articulo', 'Unidades vta comer', 'Valor des com']], how="left", left_on=["COD TQ"], right_on=["Articulo"])
    data.drop("Articulo", axis=1, inplace=True)
    data.rename(columns={"Unidades vta comer": "COLOCACION", "Valor des com": "COLOCACION V36"}, inplace=True)
    data = data.groupby(['COD TQ', 'PRECIO', 'INVENTARIO', 'EVACUACION', 'EVACUACION VALORES',
                         'INVENTARIO VALORES','COD NEG',"FORMATO"]).agg({"COLOCACION": "sum", "COLOCACION V36": "sum"}).reset_index()
    
    # Se obtiene los articulos que no registró el cliente
    resto = data.merge(venta_inventario, how="right", left_on="COD TQ", right_on="Articulo")
    resto = resto[resto["COD TQ"].isna()]
    
    resto = resto[['Articulo', 'Unidades vta comer', 'Valor des com','COD NEG']]
    resto.rename(columns={"Articulo": "COD TQ", "Unidades vta comer": "COLOCACION", "Valor des com": "COLOCACION V36"}, inplace=True)
    ## Se calcula los precios de los sobrantes
    if extra_data["COD_CANAL"]== 97:
        hoja="MAYORISTAS"
        sheet="Lista de Precios Mayoristas"
    elif extra_data["COD_CANAL"]== 91:
        hoja="CADENAS"
        sheet="Lista de Precios Cadenas"
    elif extra_data["COD_CANAL"]== 92:
        hoja="DEPOSITOS"         
        sheet="Lista de Precios Depósitos"
        
    
    if "COD NEG" in resto.columns:        
        resto.drop("COD NEG", axis=1, inplace=True)
        
        
    resto=set_concatenated_and_format(resto,"MAESTRA EL SALVADOR")
    
    resto['COD TQ']=resto['COD TQ'].astype(np.int64)
    
    if aliado==0: 
        
        resto, sin_precio_resto = set_price_nor(resto, page_client,sheet,hoja)
        
    elif aliado==1:
        
        resto, sin_precio_resto = set_price_nor_aliados(resto, page_client,sheet,hoja)
 
    
    #resto["FORMATO"] = resto.apply(lambda x: "BONIMA" if x["COD TQ"].startswith("300") else "TQ", axis=1)
    ## Se juntan los sobrantes al resto de artículos
    
    data = data.append(resto)
    
    maestra_cam_articulos = pd.read_excel("{}/{}".format(inputPathMaestras, 'Maestra Articulos CAM.xlsx'),
                                        sheet_name='MAESTRA EL SALVADOR', skiprows=2)
    maestra_cam_articulos = maestra_cam_articulos[['COD TQ', 'NOMBRE TQ', 'PRESENTACIÓN', 'NOMBRE NEG', 'COD LIN', 'NOMBRE LIN', 'COD MARCA',
                                                   'NOMBRE MARCA', 'Art Vigentes', 'Flag Seg Marca', 'Flag Prod Foco TG NOR', 'Flag Incentivos',
                                                   'plan recambio', 'Estrategia de apoyo ', 'Est Apoyo', 'Agrupación']]
    maestra_cam_articulos = maestra_cam_articulos.groupby('COD TQ').first().reset_index()
    maestra_cam_articulos["COD TQ"] = maestra_cam_articulos["COD TQ"].astype(np.int64)

    data = data.merge(maestra_cam_articulos, how="left", on="COD TQ").fillna(0)

    data.drop("COD NEG", axis=1, inplace=True)
    data=set_cod_neg(data,"MAESTRA EL SALVADOR")
    
    data["Orden"] = extra_data["ORDEN"]
    data["Mes Orden"] = extra_data["MES_ORDEN"]
    data["Formato Fecha"] = extra_data["FORMATO_FECHA"]
    data["Cod Pais"] = extra_data["COD_PAIS"]
    data["País"] = extra_data["PAIS"]
    data["Cod Canal"] = extra_data["COD_CANAL"]
    data["Canal"] = extra_data["CANAL"]
    data["Cod Clipadre"] = extra_data["COD_CLIPADRE"]
    data["Ref Cliente"] = extra_data["REF_CLIENTE"]
    # brasil_2["Colocación Depósitos"] = "NO"
    data["flag cuadro basico"] = extra_data["FLAG_CUA_BAS"]
    data["Colocación valores"] = data["PRECIO"] * data["COLOCACION"]

    data.rename(columns={"NOMBRE TQ": "ARTÍCULO", "COD NEG": "Cod Negocio", "NOMBRE NEG": "Negocio", "COD LIN": "Cod linea", "NOMBRE LIN": "Linea",
                         "NOMBRE MARCA": "Marca", "PRECIO": "CIF Neto", "FORMATO": "Compañía", "EVACUACION": "Evacuación",
                         "EVACUACION VALORES": "Evacuación valores", "COLOCACION": "Colocación", "COLOCACION VALORES": "Colocación valores"}, inplace=True)
    
  

    
    
    data.columns = data.columns.str.strip().str.upper()
    data = data[["ORDEN", "MES ORDEN", "FORMATO FECHA", "COD PAIS", "PAÍS", "COD CANAL", "CANAL", "COD CLIPADRE", "REF CLIENTE", "COD TQ", "ARTÍCULO",
                 "PRESENTACIÓN", "COD NEGOCIO", "NEGOCIO","COD LINEA", "LINEA", "COD MARCA", "MARCA", "CIF NETO", "ART VIGENTES", 
                 "FLAG SEG MARCA", "FLAG PROD FOCO TG NOR", "FLAG INCENTIVOS", "PLAN RECAMBIO", "ESTRATEGIA DE APOYO", "EST APOYO", "AGRUPACIÓN",
                 "EVACUACIÓN", "INVENTARIO", "COLOCACIÓN", "EVACUACIÓN VALORES", "INVENTARIO VALORES", "COLOCACIÓN VALORES", "COLOCACION V36", "COMPAÑÍA"]]

    return data


def writeFile(list_data, filename):
    """
    Funcion que escribe un archivo en excel

    Parameters:
        list_data (List<DataFrame>): Lista de Dataframe para registrar en archivo
        filename (str): Nombre del archivo

    Returns:
        ruta (str): Donde se guardo el archivo
        error (str): Mensaje de error
    """
    ruta = None
    error = None
    try:
        ruta = "{}\{}.xlsx".format(inputPathMaestras, filename)
        with pd.ExcelWriter(ruta) as writer:
            for idx, df in enumerate(list_data):
                df.to_excel(writer, sheet_name="reporte_{}".format(idx))

    except Exception as e:
        error = str(e)

    return ruta, error

class EvacuacionError(Exception):
    pass