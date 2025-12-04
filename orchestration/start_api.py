from prefect import flow, task
import subprocess

@task
def start_api():
    subprocess.run(["uvicorn", "api.apimain:app", "--reload"], check=True)

@flow
def api_flow():
    start_api()

if __name__ == "__main__":
    api_flow()
