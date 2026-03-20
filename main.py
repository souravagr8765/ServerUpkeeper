import urllib.request
import sys
from dotenv import load_dotenv
import os

load_dotenv()

# Replace with your actual Nhost subdomain
NHOST_SUBDOMAINS= str(os.getenv("SUBDOMAINS")).split(",")
NHOST_REGION = "ap-south-1"


def ping(url):
    try:
        req = urllib.request.urlopen(url, timeout=10)
        print(f"OK - Status {req.status} from {url}")
    except Exception as e:
        print(f"FAILED - {e}", file=sys.stderr)

if __name__ == "__main__":
    for NHOST_SUBDOMAIN in NHOST_SUBDOMAINS:
        HEALTH_URL = f"https://{NHOST_SUBDOMAIN}.hasura.{NHOST_REGION}.nhost.run/healthz"
        ping(HEALTH_URL)