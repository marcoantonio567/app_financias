from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("financas", "0002_categoria"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pessoa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=120, unique=True)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["nome"],
            },
        ),
    ]

