from fabric import task
from datetime import datetime


@task
def develop(context):
    context.run("[ -d env ] || python3 -m venv env", replace_env=False)
    context.run("./env/bin/pip install -e .[dev]", replace_env=False)


@task
def fetch_data(context):
    today = datetime.now().date().year
    context.run(
        f"poetry run fetch_pollen_csv 1996 {today} data.csv", replace_env=False
    )
