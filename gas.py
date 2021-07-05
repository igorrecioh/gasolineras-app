import requests

BASE_URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes"


def get_comunidades():
    try:
        comunidades = {}
        response_ccaa = requests.get(BASE_URL + "/Listados/ComunidadesAutonomas/")
        data_ccaa = response_ccaa.json()
        for comunidad in data_ccaa:
            print(comunidad['IDCCAA'] + " --> " + comunidad['CCAA'])
            comunidades[comunidad['CCAA']] = comunidad['IDCCAA']
        return comunidades
    except requests.exceptions.ConnectionError:
        return comunidades

def get_provincias(ccaa_id):
    response_prov = requests.get(BASE_URL + "/Listados/ProvinciasPorComunidad/" + ccaa_id)
    data_prov = response_prov.json()
    provincias = {}
    for provincia in data_prov:
        print(provincia['IDPovincia'] + " --> " + provincia['Provincia'])
        provincias[provincia['Provincia']] = provincia['IDPovincia']
    return provincias


def get_municipios(province_id):
    response_municipios = requests.get(BASE_URL + "/Listados/MunicipiosPorProvincia/" + province_id)
    data_municipios = response_municipios.json()
    municipios = {}
    for city in data_municipios:
        print(city['IDMunicipio'] + " --> " + city['Municipio'])
        municipios[city['Municipio']] = city['IDMunicipio']
    return municipios


def get_estaciones_por_ciudad(ciudad_id):
    response_estaciones = \
        requests.get(BASE_URL + "/EstacionesTerrestres/FiltroMunicipio/" + ciudad_id)
    data_estaciones = response_estaciones.json()
    estaciones = []
    for estacion in data_estaciones['ListaEESSPrecio']:
        estaciones.append(estacion)
    return estaciones
