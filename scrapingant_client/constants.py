from enum import Enum

SCRAPINGANT_API_BASE_URL = 'https://api.scrapingant.com/v1'


class ProxyCountry(str, Enum):
    brasilia = 'br'
    china = 'cn'
    germany = 'de'
    spain = 'es'
    france = 'fr'
    the_united_kingdom = 'gb'
    hong_kong = 'hk'
    india = 'in'
    italy = 'it'
    israel = 'il'
    japan = 'jp'
    the_netherlands = 'nl'
    russia = 'ru'
    saudi_arabia = 'sa'
    the_united_arab_emirates = 'ae'
    usa = 'us'
