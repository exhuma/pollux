from fabric import task
from datetime import datetime


@task
def develop(context):
    context.run("poetry install")


@task
def fetch_data(context):
    today = datetime.now().date().year
    context.run(
        f"poetry run fetch_pollen_csv 1996 {today} data.csv", replace_env=False
    )
