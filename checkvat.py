from urllib import getproxies
from suds.client import Client

VIES_URL = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'


client = Client(VIES_URL, proxy=getproxies())

def get_vat_info(vat):
    code = vat[:2]
    number = vat[2:]
    res = client.service.checkVat(countryCode=code, vatNumber=number)
    return (bool(res['valid']), res)
