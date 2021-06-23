from datetime import datetime

from fabric import task


@task
def develop(context):
    context.run("[ -d env ] || python3 -m venv env", replace_env=False)
    context.run("./env/bin/pip install -e .[dev]", replace_env=False)
    context.run("pre-commit install", replace_env=False)


@task
def fetch_data(context):
    today = datetime.now().date().year
    context.run(
        f"./env/bin/fetch_pollen_csv 1996 {today} data.csv", replace_env=False
    )


@task
def run_web(context):
    context.run(
        "./env/bin/flask run --reload",
        env={"FLASK_APP": "pollux.api:make_app"},
        replace_env=False,
    )
