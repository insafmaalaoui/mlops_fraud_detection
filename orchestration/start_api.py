from prefect import flow, task
import subprocess
from prefect import flow, task
from prefect.blocks.notifications import SendgridEmail

from prefect.blocks.notifications import SendgridEmail
from prefect import flow, task

@task
def send_email():
    # Charge ton bloc SendGrid
    sendgrid_block = SendgridEmail.load("email-1")
    
    # Envoie l'email
    sendgrid_block.notify("Test email from Prefect!")

@flow
def api_flow():
    send_email()

if __name__ == "__main__":
    api_flow()

@task
def start_api():
    subprocess.run(["uvicorn", "api.apimain:app", "--reload"], check=True)

@flow
def api_flow():
    start_api()

if __name__ == "__main__":
    api_flow()
