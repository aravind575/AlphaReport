from django.urls import path, include

from api.views.searchView import SearchView

urlpatterns = [
    path('search', SearchView.as_view())
]