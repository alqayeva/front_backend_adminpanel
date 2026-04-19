from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler

from utils.response import error_response


def _extract_error_message(detail):
    # DRF error detail-i dict, list, tuple ve ya ErrorDetail kimi gele biler.
    # Frontend ise yalniz tek setirlik error mesaji gozlediyi ucun bu helper
    # gelen strukturu sade string formasina salmaq ucun yazilib.
    if isinstance(detail, dict):
        if not detail:
            return "Something went wrong."

        first_value = next(iter(detail.values()))
        return _extract_error_message(first_value)

    if isinstance(detail, (list, tuple)):
        if not detail:
            return "Something went wrong."

        return _extract_error_message(detail[0])

    if isinstance(detail, ErrorDetail):
        return str(detail)

    return str(detail)


def custom_exception_handler(exc, context):
    # DRF-in oz exception_handler-i evvelce status kodu ve detail qurur.
    # Biz onu istifade edirik, sonra cavabi Task 9-un standart error formatina ceviririk.
    response = exception_handler(exc, context)

    if response is not None:
        return error_response(
            error=_extract_error_message(response.data),
            status=response.status_code,
        )

    # Eger exception DRF terefinden taninmirsa, yenede frontend-e
    # vahid formatda 500 cavabi qaytarilsin.
    return error_response(
        error="Internal server error.",
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
