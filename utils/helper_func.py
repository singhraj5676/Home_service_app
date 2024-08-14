from typing import List 
from response.currency_response import Currency_Response
from response.language_response import Language_Response
from response.verification_response import VerificationType_Response
from response.location_response import Location_Response


def convert_verification_types(verification_types) -> List[VerificationType_Response]:
    return [VerificationType_Response(type=verification.type) for verification in verification_types]

def convert_blockers(blockers) -> List[str]:
    # Convert a list of Blockers objects to a list of strings
    return [blocker.type for blocker in blockers]

def convert_currencies(currencies) -> List[Currency_Response]:
    return [Currency_Response(code=currency.code, name=currency.name, symbol=currency.symbol) for currency in currencies]

def convert_languages(languages) -> List[Language_Response]:
    return [Language_Response(code=language.code, name=language.name) for language in languages]

def convert_days(days) -> List[str]:
    return [day.day for day in days]

def convert_location(location) -> Location_Response:
    return Location_Response(
        address=location.address,
        latitude=location.latitude,
        longitude=location.longitude,
        city=location.city,
        country=location.country,
        slug=location.slug,
        country_code=location.country_code,
        place_id=location.place_id
    )
