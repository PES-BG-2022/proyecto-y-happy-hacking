from zeep import Client


def tipo_cambio_dia():
    cliente = Client('https://www.banguat.gob.gt/variables/ws/TipoCambio.asmx?WSDL')
    tipo_de_cambio_dia = float(cliente.service.TipoCambioDia()['CambioDolar']['VarDolar'][0]['referencia'])
    fecha = cliente.service.TipoCambioDia()['CambioDolar']['VarDolar'][0]['fecha']
    return tipo_de_cambio_dia, fecha

def convertir_usd_a_gtq(usd):
    dolares = float(usd)
    tc, fecha = tipo_cambio_dia()
    quetzales = dolares*tc
    texto = str(usd) + " USD -> " + str(quetzales) + " GTQ" + " calculado el " + str(fecha)
    return texto

def convertir_gtq_a_usd(gtq):
    quetzales = float(gtq)
    tc, fecha = tipo_cambio_dia()
    dolares = quetzales/tc
    texto = str(gtq) + " GTQ -> " + str(dolares) + " USD" + " calculado el " + str(fecha)
    return texto