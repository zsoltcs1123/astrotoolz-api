from astrotoolz_api.utils.camel_model import CamelModel


class DasaRequest(CamelModel):
    birth_date: str
    dasa_level: str
