from zeep import Client


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