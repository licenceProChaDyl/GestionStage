from django.conf.urls import patterns, url
from entreprises import views

urlpatterns = patterns("",
    url(r'^$', views.accueil, name='accueil'),
    url(r'^(?P<page>\d+)/?$', views.accueil, name='index-page'),
	url(r'^detailEntreprise/(?P<entreprise_id>\d+)/?$', views.detailEntreprise, name="detailEntreprise"),
	url(r'^delete/(?P<entreprise_id>\d+)/?$', views.delete, name="delete"),
    url(r'^ajouterEntreprise/$', views.ajouterEntreprise, name="ajouterEntreprise"),
    url(r'^modifierEntreprise/(?P<entreprise_id>\d+)/?$', views.modifierEntreprise, name="modifierEntreprise"),
    url(r'^detailEntreprise/(?P<entreprise_id>\d+)/?/maps$', views.geoloc, name="geolocal"),
)
