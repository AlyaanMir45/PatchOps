
import json
import requests

from system_info import get_system_info

API_URL = "http://127.0.0.1:8000"


def register_device():
    device = get_system_info()

    try:
        response = requests.post(
            f"{API_URL}/devices/register",
            json=device,
            timeout=10
        )

        response.raise_for_status()

        print("Device registration successful!")
        print(json.dumps(response.json(), indent=4))

    except requests.RequestException as error:
        print(f"Device registration failed: {error}")


if __name__ == "__main__":
    register_device()
