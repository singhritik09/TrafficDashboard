import os
import subprocess
from time import time

def start_containers(container_ids):
    for container_id in container_ids:
        try:
            subprocess.run(['docker', 'start', container_id], check=True)
            print(f"Container {container_id} started successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to start container {container_id}: {e}")
    
def retry_start_containers(container_id, retries=3, delay=5):
    for i in range(retries):
        start_containers(container_id)
        # Here you can add logic to check if the containers are running successfully
        # If they are, break out of the loop
        # If not, wait for the specified delay before retrying
        time.sleep(delay)

if __name__ == "__main__":
    app = start_containers(["e035de4907ae", "b850bcca969e", "43adef22ea25"])
    start_containers("e035de4907ae")

