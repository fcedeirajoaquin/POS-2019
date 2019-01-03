#!/usr/bin/env python
#-*- coding: cp850 -*-
import ssl
import os
import urllib
import urllib2
import getpass
import ttk
import sys
import requests
from bs4 import BeautifulSoup
from mechanize import Browser
import tkMessageBox
import openpyxl
import time
from openpyxl.styles import colors
from openpyxl.styles import Font, Color, PatternFill, Border, Side
from openpyxl.workbook import Workbook
import tkFileDialog
import Tkinter
#import py2exe
from tkFileDialog import *
from Tkinter import * 
import Tkinter as tk
from PIL import ImageTk, Image
from openpyxl.styles import colors
from openpyxl.styles import Font, Color, PatternFill, Border, Side
from openpyxl.workbook import Workbook
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.chart import (
    PieChart,
    ProjectedPieChart,
    Reference
)
from openpyxl.chart.series import DataPoint
def chequearSPINespecial(documento):
    global bateria
    global porta
    url = "https://seguro.sssalud.gob.ar/indexss.php?opc=bus650&user=HPGD&cat=consultas"
    browser.open(url,timeout=2)
    form = browser.select_form(nr=0)
    cadenita = "" 
    bateria = ""
    franco = False
    encontro = False 
    browser["nro_doc"]=documento
    response =browser.submit()
    contadorsito2=0
    OSSI2=""
    for elemento in response.read():
        if encontro == True and elemento == "<":
            contadorsito2+=1
            if cadenita.strip(" ") == "No se reportan datos para el NUMERO DE DOCUMENTO "+documento:
                OSSI2="No se encontraron datos"
                return OSSI2
            if contadorsito2 ==3:
                OSSI2=cadenita
            if contadorsito2 == 4:
                bateria=cadenita
            encontro=False
            cadenita=""
        if elemento == "<":
            cadenita=""
        cadenita+=elemento
        if cadenita == '<b>':
            encontro=True
        if elemento==">":
            cadenita=""
    return OSSI2                
def controlSPIN(documento):
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://seguro.sssalud.gob.ar/indexss.php?opc=bus650&user=HPGD&cat=consultas"
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20100101 Firefox/14.0.1', 'Referer': 'http://whateveritis.com'}
        request = urllib2.Request(url, None, header)
        response = browser.open(request,timeout=2)
        form = browser.select_form(nr=0)
        try:
            browser["_user_name_"] =usuarioL
            browser["_pass_word_"] =contraL
            response =browser.submit()
            OSSI2=chequearSPIN(documento,response)
            return OSSI2
        except:
            OSSI2=chequearSPINespecial(documento)
            return OSSI2
    except Exception as e:
        print "----------------------------------------------------------------------------------------"
        print e
        print "----------------------------------------------------------------------------------------"
        return "ERROR"      
def chequearSPIN(documento,response):
    global bateria
    global porta
    global nombreglobal2
    cadenita2 = ""
    cadenita = "" 
    bateria = ""
    franco = False
    encontro = False 
    encontro2 = False
    form = browser.select_form(nr=0)
    browser["nro_doc"]=documento
    response =browser.submit()
    contadorsito2=0
    contadorsitocade2=0
    OSSI2=""
    leer = response.read()
    for elemento in leer:
        if encontro2 == True and elemento == "<":
            if contadorsitocade2 == 6:
                nombreglobal2 = cadenita2
            encontro2=False
            cadenita2=""
            contadorsitocade2+=1
        if encontro == True and elemento == "<":
            contadorsito2+=1
            if cadenita.strip(" ") == "No se reportan datos para el NUMERO DE DOCUMENTO "+documento:
                OSSI2="No se encontraron datos"
                return OSSI2
            if contadorsito2 ==3:
                OSSI2=cadenita
            if contadorsito2 == 4:
                bateria=cadenita
            encontro=False
            cadenita=""
        if elemento == "<":
            cadenita2=""
            cadenita=""
        cadenita2+=elemento
        cadenita+=elemento
        if cadenita2== '<td>':
            encontro2=True
            cadenita2=""
        if cadenita == '<b>':
            encontro=True
        if elemento==">":
            cadenita=""
    return OSSI2
def chequearIOMA(documento):
    global nombreglobal3
    nombreglobal3=""
    sexo=["1","2"]
    counterIOMA=0
    itworks=False
    suma=0
    try:    
        for indele in sexo:
            cadenita = ""
            ultima = ""
            url = "http://www.ioma.gba.gov.ar/sistemas/consulta_padron_afiliados/consulta_afiliados.php" ##Son necesarias las comillas
            franco = False
            encontro = False
            browser.open(url)
            form = browser.select_form("numdoc")
            browser[" T3"] = documento
            browser.form.set_value([indele],name='sexo')
            response = browser.submit()
            leer = response.read()
            for elemento in leer:
                if encontro == True and elemento == "<":
                    counterIOMA+=1
                    if counterIOMA == 2:
                        nombreglobal3 = cadenita
                    ultima=cadenita
                    encontro=False
                    cadenita=""
                if elemento == "<":
                    cadenita=""
                cadenita+=elemento
                if cadenita == '<span class="texto-azul">' or cadenita =='<span class="texto-azul-bold">' :
                    encontro=True
                    itworks = True
                if elemento==">":
                    cadenita=""
            if len(ultima) > 2:
                suma+=1
            else:
                suma+=0
        if suma>0:
            return True
        else:
            return False
    except Exception as e:
            print "-----------------------------------------------------------------"
            print str(e)
            return "ERROR"
def botPUCO2(documento):
    global nombreglobal
    nombreglobal = ""
    data = urllib.urlencode({'documento':documento})
    try:
        url = "http://200.69.210.1/nacer/personas_puco_con_documentos.php"
        request = urllib2.Request(url,data)
        respuesta = urllib2.urlopen(request).read()
        respLimpia,nombreglobal=limpiandingSTR(respuesta)
        if respuesta == "null":
            return "No se reportan datos"
        else:
            return respLimpia
    except: 
        listaEr=["PAGINA NO DISPONIBLE"]
        return listaEr
def limpiandingSTR(cadena):
    nombresito=""
    c=""
    nombre=""
    listreturn=[]
    conta=1
    conta2=0
    eselnombre=False
    encontro = False
    termino= False
    nueva=0
    for elemento in cadena:
        if eselnombre == True:
            if elemento == '"':
                nombresito=nombre
                eselnombre=False
        nombre+=elemento
        if elemento == ",":
            nombre=""
        if elemento != '"' and elemento != "}" and encontro == True: 
            c+=elemento
        if elemento == ":":
            c=""
            encontro =True
        if elemento == "}":
            if c not in listreturn and len(c)>3:
                listreturn.append(c)
            conta2=0
        if nombre == '"NombreYApellido":"':
            eselnombre=True
            nombre=""
    return listreturn,nombresito
def limpiandingSTR2(cadena):
    global estaactivosumar
    clausula = False
    clausula2 = False
    clausula3= False
    apellido=""
    nombreactivo=""
    eselapellido=False
    nombresito=""
    nombresito2=""
    c=""
    nombre=""
    listreturn=[]
    conta=1
    conta2=0
    eselnombre=False
    encontro = False
    termino= False
    nueva=0
    for elemento in cadena:
        if eselnombre == True:
            if elemento == '"' and clausula == False:
                nombresito=nombre
                eselnombre=False
        if eselapellido == True:
            if elemento == '"' and clausula2 == False:
                nombresito2=apellido
                eselapellido=False
        apellido+=elemento
        nombre+=elemento
        nombreactivo+=elemento
        if elemento == "," and encontro == True:
            nombre=""
        if elemento != '"' and elemento != "}" and encontro == True: 
            c+=elemento
        if elemento == ":":
            c=""
            encontro =True
        if elemento == "}":
            listreturn.append(c)
            conta2=0
        if nombre == '"afiNombre":"':
            eselnombre=True
            nombre=""
        if nombre == '"afiApellido":"':
            eselapellido=True
            apellido=""
        # if nombre == '"Activo":"N"' and clausula3 == False:
        #   clausula3= True
        #   estaactivosumar=False
        if nombre == '"Activo":"S"' and clausula3 == False:
            estaactivosumar = True
            return nombresito+" "+nombresito2
    estaactivosumar = False
    return ""
def chequearPuco(documento):
    try:
        listaOS=[]
        noTiene=False
        url = "http://www.saludnqn.gob.ar/PadronConsultasWeb/"
        browser.open(url,timeout=2)
        form = browser.select_form(nr=0)
        browser["ctl00$ContentPlaceHolder1$txtNumero"]=documento
        response =browser.submit()
        respuesta=response.read()
        counter=0
        notieneOS=False
        oeses=[5,11,17,23,29,35]
        cadenita = ""
        ultima = ""
        franco = False
        encontro = False
        for elemento in respuesta:
                if encontro == True and elemento == "<":
                    counter+=1
                    ultima=cadenita
                    if ultima.strip(" ") == "No se encontraron datos":
                        notieneOS=True
                        return noTiene
                    encontro=False
                    cadenita=""
                if elemento == "<":
                    cadenita=""
                cadenita+=elemento
                if cadenita == '<td colspan="6">':
                    encontro=True
                if elemento==">":
                    cadenita=""
        cadenita=""
        counter=0
        ultima=""
        encontro=False
        if notieneOS==False:
            for elemento in respuesta:
                if encontro == True and elemento == "<":
                    counter+=1
                    ultima=cadenita
                    if counter in oeses:
                        listaOS.append(ultima.strip(" "))
                    encontro=False
                    cadenita=""
                if elemento == "<":
                    cadenita=""
                cadenita+=elemento
                if cadenita == '<td style="font-size:Smaller;">' or cadenita == '<div class="text">':
                    encontro=True
                if elemento==">":
                    cadenita=""
        return listaOS
    except Exception as e:
            print str(e)
            return "ERROR"
def conseguirInput(cadena):
    inputLimpio=""
    corchetes=0
    encontroInput=False
    pasoLos2Car=False
    conta=0
    for elemento in cadena:
        if encontroInput==True and conta == 2 and elemento=="'":
            return inputLimpio
        if elemento == "[" and encontroInput==False:
            corchetes+=1
        if encontroInput==True and conta<2:
            conta+=1
        if corchetes==2:
            encontroInput=True
        if conta==2:
            if elemento!="'":
                inputLimpio+=elemento
def printAlgo():
    print"*********************************************************************************************"
    print "holaaaaaaaaaaaaaaaaaaaa"
    print"*********************************************************************************************"
def siLaPalabraEstaEnLaLista(lista,palabra):
    for elemento in lista:
        if palabra in elemento:
            return True
    return False
def tienePAMI(laStr, elemento1, elemento2):
    if laStr in elemento1 or siLaPalabraEstaEnLaLista(elemento2,laStr):
        return True
    return False
def chequearPAMI(documento):
    browser.open('http://institucional.pami.org.ar/result.php?c=6-2')
    form=browser.select_form(nr=3)
    browser.set_handle_robots( False )
    browser["nroDocumento"]=documento
    response =browser.submit()
    respuesta=response.read()
    filtrarVomito(respuesta)
    return listaDmodulo,listaRed,listaPrestador
def filtrarVomito(vomito):
    url=""
    acum=""
    acumLink=""
    encontroLink=False
    loproximo=False
    lodeahora=False
    for elemento in vomito:
        if lodeahora==True: 
            if elemento !='"':
                acumLink+=elemento
            else:
                if "beneficio" in acumLink and "parent" in acumLink and encontroLink == False:
                    encontroLink=True
                    url=acumLink
                lodeahora=False
                acumLink=""
        if elemento == "<":
            if loproximo==True:
                loproximo=False
        acum+=elemento
        if elemento == ">":
            if acum == '<p class="whitetxt">':
                loproximo=True
            acum=""
        if acum=='<a href="':
            lodeahora=True
    url="http://institucional.pami.org.ar/"+url
    chequearArbolPami(url)
def chequearArbolPami(url):
    global listaDmodulo
    global listaRed
    global listaPrestador
    r  = requests.get(url)
    listaDmodulo=[]
    listaRed=[]
    listaPrestador=[]
    contador=0
    contaTabla=1
    data = r.text
    soup = BeautifulSoup(data,"html5lib")
    for link in soup.find_all('p'):
        # print(link.get('class'))
        if "<p>PRESTADOR:</p>" in str(link): 
            contador+=1
        if contador==2 and "<p>PRESTADOR:</p>" not in str(link):
            linkLimpio=str(link).strip("<p>").strip("</p>")
            if "APELLIDOS Y NOMBRES" in str(link):
                break
            if contaTabla==4:
                contaTabla=1
            if contaTabla==1:
                # print "D.MODULO: "+linkLimpio
                listaDmodulo.append(str(linkLimpio))
            if contaTabla==2:
                # print "RED: "+linkLimpio
                listaRed.append(str(linkLimpio))
            if contaTabla==3:
                # print "PRESTADOR: "+linkLimpio
                listaPrestador.append(str(linkLimpio))
            contaTabla+=1

global listaDmodulo
global listaRed
global listaPrestador
global browser
global usuarioL
global contraL
usuarioL="sss1754"
contraL="1w4un8"
browser=Browser()
browser.set_handle_robots(False)
print botPUCO2("40743779")