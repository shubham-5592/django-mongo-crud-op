from django.conf.urls import url 
from tutorials import views 
from django.urls import include
from rest_framework import routers

router = routers.SimpleRouter()
router.register('tutorials/published', views.PublishedHandler)
router.register('tutorials', views.TutorialHandler)
urlpatterns = [
    url(r'api/', include(router.urls))
]
