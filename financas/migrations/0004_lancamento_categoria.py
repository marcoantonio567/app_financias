from django.db import migrations, models
import django.db.models.deletion


def _preencher_categoria(apps, schema_editor):
    Categoria = apps.get_model("financas", "Categoria")
    Lancamento = apps.get_model("financas", "Lancamento")

    categoria_padrao, _ = Categoria.objects.get_or_create(nome="Sem categoria")
    Lancamento.objects.filter(categoria__isnull=True).update(categoria=categoria_padrao)


class Migration(migrations.Migration):
    dependencies = [
        ("financas", "0003_pessoa"),
    ]

    operations = [
        migrations.AddField(
            model_name="lancamento",
            name="categoria",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="lancamentos",
                to="financas.categoria",
            ),
        ),
        migrations.RunPython(_preencher_categoria, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="lancamento",
            name="categoria",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="lancamentos",
                to="financas.categoria",
            ),
        ),
    ]
