from zeep import Client


def tipo_cambio_dia():
    cliente = Client('https://www.banguat.gob.gt/variables/ws/TipoCambio.asmx?WSDL')
    tipo_de_cambio_dia = float(cliente.service.TipoCambioDia()['CambioDolar']['VarDolar'][0]['referencia'])
    fecha = cliente.service.TipoCambioDia()['CambioDolar']['VarDolar'][0]['fecha']
    return tipo_de_cambio_dia, fecha
