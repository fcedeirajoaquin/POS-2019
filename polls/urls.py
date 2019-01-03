from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$',views.hola, name='home'),
    # url(r'^POS/$',views.hola, name='home'),
    url(r'^consultaLista/$',views.simple_upload, name='consultaLista'),
    url(r'^consultaUnica/$',views.get_name, name='consultaUnica'),
    url(r'^masInformacion/$',views.masInformacion, name='masInformacion'),
    url(r'^descarga/$',views.descargaExcel, name='descarga'),
    # url(r'^hola/$',views.hola,name='hola'),
    # url(r'^elMejorBoton/',views.elMejorBoton),
]