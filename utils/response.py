from rest_framework.response import Response


def success_response(data=None, message="", status=200):
    return Response({
        "success": True,
        "data": data,
        "message": message
    }, status=status)


def error_response(error="Something went wrong", status=400):
    return Response({
        "success": False,
        "error": error
    }, status=status)