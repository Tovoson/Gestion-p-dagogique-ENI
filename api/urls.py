from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('materiel', MaterielViewset, basename = 'materiel')
router.register('admins', AdminViewset, basename = 'admins')
router.register('utilisation', UtilisationViewset, basename = 'utilisation')

urlpatterns = router.urls

