from django.urls import path
from .. import apis

urlpatterns = [
    # /api/members/auth-token/
    # DRF Tutorial에서 했던 AuthTokenAPIView에 연결되도록 함
    # view:     members/apis.py
    # url:      members/urls_apis.py ->congig.urls.urlpatterns_apis
    # serializer: members/serializers.py (UserSerializer)

    # INSTALLED_APPS
    # poetry add djangorestframework
    # rest_framework
    # rest_framework.authtoken
    # -> migrate

    # Postman Colletion만들고 (Instagram)
    # members폴더 내에 AuthTokenAPIView로 요청 추가
    path('auth-token/', apis.AuthTokenAPIView.as_view()),
]
