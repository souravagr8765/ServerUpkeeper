import subprocess
import urllib.request
import atexit
import sys
from dotenv import load_dotenv
import os
import loki_logger as logger

LOG_FILE = "./Upkeeper.log"
# Setup logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s [%(levelname)s] %(message)s',
#     handlers=[
#         logging.FileHandler(LOG_FILE, encoding='utf-8'),
#         logging.StreamHandler(sys.stdout)
#    ] 
# )
# logger = logging.getLogger(__name__)

load_dotenv()

# Replace with your actual Nhost subdomain
NHOST_SUBDOMAINS= str(os.getenv("SUBDOMAINS")).split(",")
NHOST_REGION = "ap-south-1"
APP_NAMES = str(os.getenv("NAMES")).split(",")

def ping(url):
    try:
        req = urllib.request.urlopen(url, timeout=10)
        logger.info(f"{APP_NAMES[NHOST_SUBDOMAINS.index(NHOST_SUBDOMAIN)]}: OK - Status {req.status}")
    except Exception as e:
        logger.error(f"{APP_NAMES[NHOST_SUBDOMAINS.index(NHOST_SUBDOMAIN)]} FAILED - {e}")


def cleanup():
    """Terminate background processes on exit."""
    global _loki_process
    if _loki_process is not None:
        logger.info("Terminating background Loki logger...")
        try:
             # Send termination signal via log file
             logger.info("LOKI_LOGGER_TERMINATE")
             _loki_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _loki_process.kill()
        except Exception as e:
            logger.error(f"Error terminating Loki logger: {e}")
        logger.info("Loki logger terminated.")

# Register the cleanup function to run automatically when the script exits
atexit.register(cleanup)

if __name__ == "__main__":
    
    # # Global reference to the background loki logger process
    # _loki_process = None

    # def init_loki_logger(log_file):
    #     global _loki_process
        
    #     # Calculate where to start reading the log file (so we don't resend old logs)
    #     start_pos = 0
    #     if os.path.exists(log_file):
    #         start_pos = os.path.getsize(log_file)
        
    #     loki_url = os.environ.get("LOKI_URL")
    #     if loki_url:
    #         # Assumes loki_logger.py is in the same directory as this script
    #         base_dir = os.path.dirname(os.path.abspath(__file__))
    #         loki_script_path = os.path.join(base_dir, "loki_logger.py")
        
    #         if os.path.exists(loki_script_path):
    #             logger.info(f"Starting background Loki logger streaming to {loki_url}")
    #             try:
    #                 _loki_process = subprocess.Popen(
    #                     [sys.executable, loki_script_path, log_file, str(start_pos)],
    #                     stdout=subprocess.DEVNULL,
    #                     stderr=subprocess.DEVNULL,
    #                     start_new_session=True # Runs independently
    #                 )
    #             except Exception as e:
    #                 logger.error(f"Failed to start Loki logger subprocess: {e}")
    #         else:
    #             logger.warning("loki_logger.py not found. Loki logging will not be available.")

    # init_loki_logger(LOG_FILE)

    logger.info("="*50)
    for NHOST_SUBDOMAIN in NHOST_SUBDOMAINS:
        HEALTH_URL = f"https://{NHOST_SUBDOMAIN}.hasura.{NHOST_REGION}.nhost.run/healthz"
        ping(HEALTH_URL)
    logger.info("="*50)