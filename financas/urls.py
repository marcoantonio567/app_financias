from django.urls import path

from financas import views

app_name = "financas"

urlpatterns = [
    path("", views.lancamentos_view, name="lancamentos"),
    path("lancamentos/", views.lancamentos_view, name="lancamentos"),
    path("historico/", views.historico_view, name="historico"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("senha/", views.senha_view, name="senha"),
]
