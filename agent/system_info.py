import platform
import socket
import uuid
import json


def get_system_info():
    return {
        "device_id": str(uuid.getnode()),
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
    }


if __name__ == "__main__":
    info = get_system_info()
    print(json.dumps(info, indent=4))