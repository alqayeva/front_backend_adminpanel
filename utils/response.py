from rest_framework.response import Response


def success_response(data=None, message="", status=200):
    # Task 9-un esas success formati burada merkezlesdirilib.
    # Ferqli endpoint-ler ayri-ayri JSON qurmasin deye her yerde eyni envelope qaytarilir.
    return Response(
        {
            "success": True,
            "data": data,
            "message": message,
        },
        status=status,
    )


def paginated_success_response(
    *,
    count,
    next_link,
    previous_link,
    results,
    message="Data fetched successfully.",
    status=200,
):
    # Pagination olan endpoint-lerde count/next/previous/results saxlanilir,
    # amma bunlar da umumI success envelope-un icine yerlestirilir.
    return success_response(
        data={
            "count": count,
            "next": next_link,
            "previous": previous_link,
            "results": results,
        },
        message=message,
        status=status,
    )


def error_response(error="Something went wrong", status=400):
    # Task 9-a gore error cavablarin hamisi eyni sade formatda qayidmalidir.
    return Response(
        {
            "success": False,
            "error": error,
        },
        status=status,
    )
