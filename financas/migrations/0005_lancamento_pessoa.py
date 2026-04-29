from django.db import migrations, models
import django.db.models.deletion


def _preencher_pessoa(apps, schema_editor):
    Pessoa = apps.get_model("financas", "Pessoa")
    Lancamento = apps.get_model("financas", "Lancamento")

    pessoa_padrao, _ = Pessoa.objects.get_or_create(nome="Sem pessoa")
    Lancamento.objects.filter(pessoa__isnull=True).update(pessoa=pessoa_padrao)


class Migration(migrations.Migration):
    dependencies = [
        ("financas", "0004_lancamento_categoria"),
    ]

    operations = [
        migrations.AddField(
            model_name="lancamento",
            name="pessoa",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="lancamentos",
                to="financas.pessoa",
            ),
        ),
        migrations.RunPython(_preencher_pessoa, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="lancamento",
            name="pessoa",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="lancamentos",
                to="financas.pessoa",
            ),
        ),
    ]
