from django.urls import path
from .views import ManageAppsViews, RunContainerView

urlpatterns = [
    path("manage_apps/", ManageAppsViews.as_view(
            {"get":"list", "post":"create"}
        ), name='manage-apps-list'),
    path("manage_apps/detail/<int:pk>/", ManageAppsViews.as_view(
            {"get":"retrieve", "put":"update", "delete":"destroy"}
        ), name='manage-apps-detail'),
    path("run_container/<int:pk>/", RunContainerView.as_view(), name="run-container"),
]
