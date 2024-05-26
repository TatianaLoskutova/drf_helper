from django.urls import include, path

from api.spectacular.urls import urlpatterns as doc_urls
from clubs.urls import urlpatterns as club_urls
from practices.urls import urlpatterns as training_urls
from users.urls import urlpatterns as user_urls

app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
urlpatterns += club_urls
urlpatterns += training_urls
urlpatterns += user_urls
