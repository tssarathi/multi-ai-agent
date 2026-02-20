import subprocess
import threading
import time

from dotenv import load_dotenv

from utils.custom_exception import CustomException
from utils.logger import get_logger

logger = get_logger(__name__)

load_dotenv()


def run_backend():
    try:
        logger.info("Starting backend server")
        subprocess.run(
            ["uvicorn", "backend.api:app", "--host", "127.0.0.1", "--port", "8000"],
            check=True,
        )
    except CustomException as e:
        logger.error("Problem with backend service")
        raise CustomException(message="Problem with backend service", error_detail=e)


def run_frontend():
    try:
        logger.info("Starting frontend server")
        subprocess.run(["streamlit", "run", "frontend/UI.py"], check=True)
    except CustomException as e:
        logger.error("Problem with frontend service")
        raise CustomException(message="Problem with frontend service", error_detail=e)


def main():
    try:
        logger.info("Starting the application")
        threading.Thread(target=run_backend).start()
        time.sleep(2)
        run_frontend()

    except CustomException as e:
        logger.exception(f"CustomException occured: {str(e)}")


if __name__ == "__main__":
    main()
