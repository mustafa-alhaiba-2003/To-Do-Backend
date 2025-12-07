from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


class JWTService:
    def set_jwt_cookies(response : Response, access_token: str, refresh_token : RefreshToken):
        response.set_cookie(
            key="access",
            value=access_token,
            httponly=True,
            samesite="Lax",
            max_age=60 * 30,  
        )
        response.set_cookie(
            key="refresh",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 60 * 24 * 7,
        )
        return response

    def clear_jwt_cookies(response):
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response