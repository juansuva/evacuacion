# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 08:20:07 2019

@author: Juan
"""

from .utils.scripts import *
import os 


ruta=os.getcwd()
if 'ROUTE_INPUT_FILES' not in locals():
    ROUTE_INPUT_FILES = ruta
if 'ROUTE_OUTPUT_FILES' not in locals():
    ROUTE_OUTPUT_FILES = ruta

cliente_carosa = 'carosa'
cliente_launo = 'launo'
cliente_elaguila = "elaguila"
cliente_sanjose = "sanjose"
cliente_lacefa = "lacefa"
cliente_elpueblo = "elpueblo"
cliente_integral = "integral"
cliente_jheral = "jheral"
cliente_nuevosiglo = "nuevosiglo"
cliente_lasalud = "lasalud"
cliente_americana = "ameriana"
cliente_santalucia = "santalucia"
cliente_camila = "camila"
cliente_labuena = "labuena"
cliente_lavida = "lavida"
cliente_americas = "americas"



if 'CLIENTE' not in locals():
    CLIENTE = cliente_carosa

if CLIENTE == cliente_carosa:
    corosa = get_Carosa(91,"2019-04-01","0. Grupo Carosa.xlsx", ROUTE_INPUT_FILES, ROUTE_OUTPUT_FILES)
elif CLIENTE == cliente_launo:
    launo = get_launo(89,"2019-02-01","0. La Uno.xlsx", ROUTE_INPUT_FILES, ROUTE_OUTPUT_FILES)    
  
elif CLIENTE == cliente_elaguila:
    aguila = get_elaguila(91,"2019-04-01","0. El Aguila.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)

elif CLIENTE == cliente_sanjose:
    sanjose = get_sanjose(91,"2019-04-01","0. San Jose.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)

elif CLIENTE == cliente_lacefa:
    lacefa = get_lacefa(91,"2019-04-01","0. Cefa.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)

elif CLIENTE == cliente_elpueblo:
    elpueblo = get_elpueblo(91,"2019-04-01","0. El Pueblo.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)

elif CLIENTE == cliente_integral:
    integral = get_integral(91,"2019-04-01","0. Integral.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)

elif CLIENTE == cliente_jheral:
    jheral = get_jheral(91,"2019-04-01","0. Jheral Farma.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)

elif CLIENTE == cliente_nuevosiglo:
    nuevosiglo = get_nuevosiglo(91,"2019-04-01","0. Nuevo Siglo.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)
    
elif CLIENTE == cliente_lasalud:
    lasalud = get_lasalud(91,"2019-04-01","0. La Salud.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)

elif CLIENTE == cliente_americana:
    americana = get_americana(91,"2019-04-01","0. Americana.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)
    
elif CLIENTE == cliente_santalucia:
    santalucia = get_laSantaLucia(91,"2019-04-01","0. Santa Lucia.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)

elif CLIENTE == cliente_camila:
    camila= get_camila(89,"2019-02-01","0. Camila.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)
    
elif CLIENTE == cliente_labuena:
    labuena= get_labuena(89,"2019-02-01","0. La Buena.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)
    
elif CLIENTE == cliente_lavida:
    lavida= get_lavida(89,"2019-02-01","0. La Vida.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)
    
elif CLIENTE == cliente_americas:
    americas= get_americas(89,"2019-02-01","0. Las Americas.xlsx",ROUTE_INPUT_FILES,ROUTE_OUTPUT_FILES)
