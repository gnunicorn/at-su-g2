from urllib import getproxies
from suds.client import Client
import suds

VIES_URL = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'


client = Client(VIES_URL, proxy=getproxies())

def get_vat_info(vat):
    code = vat[:2]
    number = vat[2:]
    try:
        res = client.service.checkVat(countryCode=code, vatNumber=number)
    except suds.WebFault:
        return (False, {})
    return (bool(res['valid']), res)

if __name__ == "__main__":
    from sure import expect

    # invalid
    valid, info = get_vat_info("MXX1092514")
    valid.should.be.false

    # valid with return info
    valid, info = get_vat_info("MT21092514")

    expect(valid).should.be.true
    expect(info.name).should.look_like("CROWDBET HOLDING LTD")
    expect(info.countryCode).should.be("MT")
    expect(info.vatNumber).should.be("21092514")
    expect(info.address).should.be("COBALT HOUSE, LEVEL 2\n\nTriq\nNotabile\nBKR 3000\nBirkirkara")


