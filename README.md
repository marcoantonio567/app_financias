# Financial App

Personal financial control web application built with Django.

The project allows you to register income and expenses, track paginated history, and view dashboards with metrics for the last 30 days (or by selected month).

## Features

- Registration of financial transactions (income and expenses).

- Automatic calculation of total income, expenses, and balance.

- Listing of the last 20 transactions on the main screen.

- Complete history with pagination.

- Dashboard with graphs (Chart.js) and filter by month.

- Access protection via 6-digit PIN password (session).

## Technologies

- Python 3.12+
- Django 6.0.4
- SQLite (Django's default database)
- HTML + CSS + JavaScript
- Chart.js (via CDN)

## Project Structure

```text.financeiro_app/
|-- core/ # Django project configurations
|-- financas/ # Main app
| |-- migrations/
| |-- templates/financas/
| |-- forms.py
| |-- models.py
| |-- urls.py
| `-- views.py
|-- manage.py
`-- README.md
```

## How to Run

1. Clone or download this repository.

2. Enter the project folder:

```bash
cd financeiro_app
```

1. Create and activate a virtual environment.

Windows (PowerShell):

```powershell
python -m venv .venv .venv\Scripts\Activate.ps1

```

Linux/macOS:

```bash
python3 -m venv .venv .venv source .venv/bin/activate
```

1. Install the dependencies:

```bash
pip install "Django==6.0.4"
```

2. Run the migrations:

```bash
python manage.py migrate
```

3. Start the server:

```bash
python manage.py runserver
```

4. Access in the browser:

```text
http://127.0.0.1:8000/
```

## Main Routes

- `/` or `/lancamentos/` -> registration and summary of transactions
- `/history/` -> paginated history
- `/dashboard/` -> graphs and indicators
- `/password/` -> PIN validation
- `/admin/` -> Django admin panel

## Data Model

The app has the `Transaction` model with the following fields:

- `type` (`E` for Entry, `S` for Exit)
- `description`
- `value`
- `date`
- `created_on`

## Future Improvements (Suggestions)

- Include user authentication (Django login).

- Create automated tests for views and forms.
