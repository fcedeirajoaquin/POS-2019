#!/usr/bin/env python
#-*- coding: cp850 -*-
import codecs
import openpyxl
import base64
import os
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from .forms import NameForm
import struct
from .forms import UploadFileForm
from funciones import *
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.shortcuts import render_to_response
from django.template import RequestContext
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import sqlite3
def masInformacion(request):
	listaZips=[]
	pucoSumar=""
	contextos={}
	listaTipos=[]
	# try:
	print "ENTROOOOO"
	global documentoUnicoVirtual
	if documentoUnicoVirtual!=False:
		print documentoUnicoVirtual
		listaZips,pucoSumar=masInformacionBots(documentoUnicoVirtual)
		if pucoSumar==True:
			nombreLigadoAlDocumento
			pucoSumar="ESTA INSCRIPTO/A EN EL PLAN SUMAR"
		else:
			pucoSumar="NO ESTA INSCRIPTO/A EN EL PLAN SUMAR"
		if pucoSumar=="ERROR":
			pucoSumar="DATOS NO DISPONIBLES"
		contextos={'sumar_':pucoSumar,
				   'listaPamis_':listaZips,
				   }
		return render(request, 'MasInfo.html',contextos)
	# except Exception as e:
	# 	# print e
	# 	# return HttpResponseRedirect('/pos/')
def wadafuk(request):
    username, response = ntlm_auth(request)
    if response:
        return response
def get_msg_str(msg,start):
    msg_len, _, msg_off = struct.unpack("<HHH", msg[start:start + 6])
    return msg[msg_off:msg_off + msg_len].replace("\0", '')
def ntlm_auth(request):
    username = None
    response = None
    auth = request.META.get('HTTP_AUTHORIZATION')
    if not auth:
        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = "NTLM"
    elif auth[:4] == "NTLM":
        msg = base64.b64decode(auth[4:])
        print repr(msg)
        ntlm_fmt = "<8sb" #string, length 8, 4 - op
        NLTM_SIG = "NTLMSSP\0"
        signature, op = struct.unpack(ntlm_fmt, msg[:9])
        if signature != NLTM_SIG:
            print "error header not recognized"
        else:
            print "recognized"
            print signature, op
            print repr(msg)
            if op == 1:
                out_msg_fmt = ntlm_fmt + "2I4B2Q2H"
                out_msg = struct.pack(out_msg_fmt,
                    NLTM_SIG, #Signature
                    2, #Op
                    0, #target name len
                    0, #target len off
                    1, 2, 0x81, 1, #flags
                    0, #challenge
                    0, #context
                    0, #target info len
                    0x30, #target info offset
                )

                response = HttpResponse(status=401)
                response['WWW-Authenticate'] = "NTLM " + base64.b64encode(out_msg).strip()
            elif op == 3:
                username = get_msg_str(msg, 36)
    print "-----------------------------------------------------------"
    print username
    print "-----------------------------------------------------------"
    return username, response
def handler404(request):
    response = render(request,'paginaNoEncontrada.html')
    return response
def handler500(request):
    response = render(request,'paginaNoEncontrada.html')
    return response
def hola(request):
    return render(request, 'IndexPOS.html')
def get_name(request):
	global documentoUnicoVirtual
	listaPamisNormal=[]
	documentoUnicoVirtual=False
	buscarMas=False
	tieneSUMAR=False
	tieneIoma=""
	elNombre=""
	pamiDice=False
	tieneOS2=False
	elNombreOK=False
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			limpiarNombres()
			documento=conseguirInput(str(request.POST))
			capitaOno=""
			capitaOnoTF=False
			IOMA=chequearIOMA2018(documento)
			documentoUnicoVirtual=documento
			listaPuco=botPUCO2019(documento)
			if listaPuco=="No se reportan datos":
				listaPuco=["No se reportan datos"]
			if int(documento) > 10000:
				OSSI2=controlSPIN(documento)
			else:
				OSSI2="NUMERO NO VALIDO"
			tienePami=tienePAMI("JUBILADOS Y PENSIONADOS", OSSI2, listaPuco)
			if IOMA==True:
				tieneIoma="TIENE IOMA"
			else:
				tieneIoma="NO TIENE IOMA"
			tieneOS2=tieneOS(IOMA,listaPuco,OSSI2)
			print tieneOS2
			if tieneOS2:
				elNombre=nombreLigadoAlDocumento()
				if elNombre != False and len(elNombre) >4 :
					elNombreOK=True
					elNombre="- "+elNombre
				if elNombre==False:
					elNombre=""
				if tienePami:
					listaPamisNormal=chequearPAMI(documento)
					print "------------------------------------------------------"
					print len(listaPamisNormal)
					print "------------------------------------------------------"
					if len(listaPamisNormal) > 1:
						pamiDice=False
						if len(listaPamisNormal) == 2:
							if siLaPalabraEstaEnLaLista(listaPamisNormal[1][2],"LARCADE") == False:
								capitaOno="NO CAPITA EN ESTE HOSPITAL"
							else:
								capitaOnoTF=True
								capitaOno="CAPITA EN ESTE HOSPITAL"
						else:
							capitaOnoTF=False
							capitaOno=" DOS PERSONAS CON EL MISMO DNI "
						# arbolPami=zip(listaPuco1,listaPuco2,listaPuco3)
						contextos={'documento_':documento,
						'ioma_': tieneIoma,
						'spin_':OSSI2,
						'tienePAMI_':tienePami,
						'tieneOS2_':tieneOS2,
						'listaPuco_': listaPuco,
						'capitaOno_':capitaOno,
						'capitaOnoTF_':capitaOnoTF,
						'listaPamisNormal_':listaPamisNormal,
						}
						if elNombreOK:
							contextos={'documento_':documento,
							'ioma_': tieneIoma,
							'spin_':OSSI2,
							'tienePAMI_':tienePami,
							'tieneOS2_':tieneOS2,
							'listaPuco_': listaPuco,
							'listaPamisNormal_':listaPamisNormal,
							'capitaOno_':capitaOno,
							'capitaOnoTF_':capitaOnoTF,
							'elNombre_':limpiarNombre(elNombre),
							}
					else:
						tienePami=False
						pamiDice=True
				if tienePami==False:
					contextos={'documento_':documento,
					'listaPuco_': listaPuco,
					'ioma_': tieneIoma,
					'tieneOS2_':tieneOS2,
					'spin_':OSSI2,
					'tienePAMI_':tienePami,
					'pamiDice_':pamiDice,
					}
					if elNombreOK:
						contextos={'documento_':documento,
						'listaPuco_': listaPuco,
						'ioma_': tieneIoma,
						'tieneOS2_':tieneOS2,
						'spin_':OSSI2,
						'tienePAMI_':tienePami,
						'pamiDice_':pamiDice,
						'elNombre_':limpiarNombre(elNombre),
						}
			else:
				print botPUCOSUMAR(documento)				
				tieneSUMAR=botPUCOSUMAR(documento)
				if tieneSUMAR==True:
					contextos={
					'documento_':documento,
					'tieneOS2_':tieneOS2,
					'tieneSUMAR_':tieneSUMAR,
					'elNombre_':limpiarNombre(nombreSumar())
					}
				else:
					contextos={
					'documento_':documento,
					'tieneOS2_':tieneOS2,
					'tieneSUMAR_':tieneSUMAR,
					}
			try:
				escribirEnLaBD(documento,limpiarNombre(elNombre),listaPuco,tieneIoma,OSSI2)
			except Exception as e:
				print e
				print "error en la base de datos"
			return render(request, 'ResultadosConsultaUnica.html', contextos)

	else:
		form = NameForm()
	return render(request, 'ConsultaUnica.html', {'form': form})
def prueba(request):
	return render(request, 'ConsultaLista.html')
def waddup(request, pk):
    print "asddddddddddddddddddddddddd"
    YOUR_OBJECT.objects.filter(pk=pk).update(views=F('views')+1)
    return HttpResponseRedirect(request.GET.get('next'))
def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			file_in_memory = request.FILES['file'].read()
			wb = openpyxl.load_workbook(filename=BytesIO(file_in_memory))
			print type(wb)
	else:
		form = UploadFileForm()
	return render(request, 'ConsultaLista.html', {'form': form})
def descargaExcel(request):
	global rutaExcel
	global nombreExcel
	#return HttpResponse(rutaExcel)
	try:
		response = HttpResponse(open(rutaExcel,"rb").read())
	except:
		print rutaExcel
		response = HttpResponse(open('/srv/http/pos/static/mediaPOS/'+nombreExcel, "rb").read())
	response['Content-Type'] = 'mimetype/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
	response['Content-Disposition'] = 'attachment; filename='+nombreExcel
	return response
def simple_upload(request):
	global rutaExcel
	global nombreExcel
	archivo=True
	try:
		if request.method == 'POST' and request.FILES['myfile']:
			myfile = request.FILES['myfile']
			fs = FileSystemStorage()
			file_in_memory = request.FILES['myfile'].read()
			wb = openpyxl.load_workbook(filename=BytesIO(file_in_memory))
			wbPROCESADO=listaDocus2018(wb)
			wbPROCESADO.save(os.path.join( os.path.dirname( __file__ ), '..' )+"/static/mediaPOS/POS_"+myfile.name)
			nombreExcel="POS_"+myfile.name
			rutaExcel=os.path.join( os.path.dirname( __file__ ), '..' )+"/static/mediaPOS/"+nombreExcel
			file_path = os.path.join(os.path.dirname(os.path.realpath(__name__)), nombreExcel)
			rutaExcel=os.path.join(os.path.dirname(os.path.realpath(__name__)))+"/static/mediaPOS/"+nombreExcel
			# response = HttpResponse(open(rutaExcel, "rb").read())
			# response['Content-Type'] = 'mimetype/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
			# response['Content-Disposition'] = 'attachment; filename='+nombreExcel
			# response['Refresh'] = "1; /home/"
			# return response
			return render(request, 'ConsultaListaDescargaCompleta.html', {"nombreArchivo_":nombreExcel})
	except Exception as e:
		print e
		archivo=False
		return render(request, 'ConsultaLista.html',{'archivo_':archivo})
	return render(request, 'ConsultaLista.html',{'archivo_':archivo})
global buscarMas
global browser
global usuarioL
global contraL
global rutaExcel
global nombreExcel
usuarioL="sss1754"
contraL="1w4un8"
buscarMas=False
browser=Browser()
browser.set_handle_robots(False)
