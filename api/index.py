import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = get_wsgi_application()


def _ensure_tmp_sqlite_ready():
    from django.conf import settings
    from django.core.management import call_command
    from django.db import connections
    from django.db.utils import OperationalError

    default_db = settings.DATABASES.get("default", {})
    if default_db.get("ENGINE") != "django.db.backends.sqlite3":
        return

    if not (
        os.environ.get("VERCEL", "").lower() in {"1", "true", "yes", "on"}
        or os.environ.get("VERCEL_ENV")
    ):
        return

    try:
        with connections["default"].cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='django_migrations' LIMIT 1"
            )
            exists = cursor.fetchone() is not None
        if exists:
            return
    except OperationalError:
        pass

    call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)


_ensure_tmp_sqlite_ready()
