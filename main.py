from task import QueManager
from time import sleep
import os
import json


checks = 0
queue = QueManager()

while checks < 120:
    print("Checking Tasks")
    task = queue.get_task()
    if task:
        checks = 0
        result = task.run()
        queue.send_result(json.dumps(result), task.testid)
    else:
        checks += 1

    sleep(5)

print("no new tasks for 10 minutes terminating instance...")
os.system("poweroff")
