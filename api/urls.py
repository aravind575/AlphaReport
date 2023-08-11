from django.urls import path, include

from api.views.searchView import SearchView
from api.views.reportView import ReportInitiateView, ReportStatusView

urlpatterns = [
    path('search', SearchView.as_view()),

    path('report/initiate', ReportInitiateView.as_view()),
    path('report/status', ReportStatusView.as_view())
]