from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EleitorViewSet, EleicaoViewSet, CandidatoViewSet, 
    AptidaoEleitorViewSet, RegistroVotacaoViewSet, VotoViewSet
)

router = DefaultRouter()
router.register(r'eleitores', EleitorViewSet)
router.register(r'eleicoes', EleicaoViewSet)
router.register(r'candidatos', CandidatoViewSet)
router.register(r'aptidoes', AptidaoEleitorViewSet)
router.register(r'registros-votacao', RegistroVotacaoViewSet)
router.register(r'votos', VotoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]