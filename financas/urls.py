from django.urls import path

from financas import views

app_name = "financas"

urlpatterns = [
    path("", views.lancamentos_view, name="lancamentos"),
    path("lancamentos/", views.lancamentos_view, name="lancamentos"),
    path("administrativo/", views.administrativo_view, name="administrativo"),
    path(
        "administrativo/categorias/excluir/<int:pk>/",
        views.excluir_categoria_view,
        name="excluir_categoria",
    ),
    path(
        "administrativo/pessoas/excluir/<int:pk>/",
        views.excluir_pessoa_view,
        name="excluir_pessoa",
    ),
    path("historico/", views.historico_view, name="historico"),
    path(
        "historico/excluir/<int:pk>/",
        views.excluir_lancamento_view,
        name="excluir_lancamento",
    ),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("senha/", views.senha_view, name="senha"),
]
