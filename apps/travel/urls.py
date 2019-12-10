from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^logInReg$', views.logInReg),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^myTrips$', views.myTrips),
    url(r'^createTravelsLink$', views.link),
    url(r'^createTravels$', views.create_travels),
    url(r'^editTravel/(?P<travel_id>\d+)/edit$', views.editTravels),
    url(r'^updateTravels/(?P<travel_id>\d+)$', views.update_travels),
    url(r'^showTravels/(?P<travel_id>\d+)$', views.travel),
    url(r'^joinTravels/(?P<travel_id>\d+)$', views.joinTravels),
    url(r'^cancelTravels/(?P<travel_id>\d+)$', views.cancelTravels),
    url(r'^deleteTravels/(?P<travel_id>\d+)/destroy$$', views.deleteTravels),
    url(r'^logout$', views.logOut),


]
