from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from zeep import Client
import pandas as pd
import os
views = Blueprint('views', __name__)

def tipo_cambio_dia():
    cliente = Client('https://www.banguat.gob.gt/variables/ws/TipoCambio.asmx?WSDL')
    tipo_de_cambio_dia = float(cliente.service.TipoCambioDia()['CambioDolar']['VarDolar'][0]['referencia'])
    fecha = cliente.service.TipoCambioDia()['CambioDolar']['VarDolar'][0]['fecha']
    return tipo_de_cambio_dia, fecha

def convertir_usd_a_gtq(usd):
    dolares = float(round(usd,2))
    tc, fecha = tipo_cambio_dia()
    quetzales = round((dolares*tc),2)
    texto = str("{:.2f}".format(usd)) + " USD -> " + str(quetzales) + " GTQ" + " calculado el " + str(fecha)
    return texto

def convertir_gtq_a_usd(gtq):
    quetzales = float(round(gtq,2))
    tc, fecha = tipo_cambio_dia()
    dolares = round((quetzales/tc),2)
    texto = str("{:.2f}".format(gtq)) + " GTQ -> " + str(dolares) + " USD" + " calculado el " + str(fecha)
    return texto

def obtener_tasas_por_rango(fechainicio, fechafin):
    miruta = os.path.dirname(__file__)
    print(miruta)
    cliente = Client('https://www.banguat.gob.gt/variables/ws/TipoCambio.asmx?WSDL')
    tasas = cliente.service.TipoCambioRango(fechainit=fechainicio,fechafin=fechafin)['Vars']['Var']
    ltasas, lfechas = crear_series_datos(tasas)
    registro = pd.Series(ltasas)
    fecha = pd.Series(lfechas)
    df = pd.DataFrame({'Fecha': fecha, 'Tipo de Cambio': registro})
    a = df.plot(x='Fecha', y='Tipo de Cambio', kind='line', figsize=(9, 5), title='Evolución del tipo de cambio de referencia', grid=True, legend=True, ylabel='Quetzales')
    fig = a.get_figure()
    fig.savefig(miruta + "/static/images/output.png")
    if(fig):
        return redirect('/resultadorango')


def crear_series_datos(tasas):
    lista_fechas = []
    lista_tasas = []
    for elemento in tasas:
        lista_fechas.append(elemento['fecha'])
        lista_tasas.append(elemento['venta'])
    return lista_tasas, lista_fechas



