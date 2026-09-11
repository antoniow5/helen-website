from django.utils import translation


class LanguageMiddleware:
    SUPPORTED_LANGUAGES = ["ru", "en", "ko"]
    DEFAULT_LANGUAGE = "ru"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith("/static/") or request.path.startswith("/media/"):
            return self.get_response(request)

        lang = request.GET.get("lang")

        if lang not in self.SUPPORTED_LANGUAGES:
            lang = request.COOKIES.get("django_language")

        if lang not in self.SUPPORTED_LANGUAGES:
            lang = self.DEFAULT_LANGUAGE

        translation.activate(lang)

        request.current_language = lang

        response = self.get_response(request)

        if request.GET.get("lang") in self.SUPPORTED_LANGUAGES:
            response.set_cookie(
                "django_language",
                lang,
                max_age=60 * 60 * 24 * 365,
                samesite="Lax"
            )

        return response