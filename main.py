from task import QueManager
from time import sleep
import os

checks = 0
queue = QueManager()

while checks < 10:
    print("Checking Tasks")
    task = queue.get_task()
    if task:
        checks = 0
        result = task.run()
        queue.send_result(result, task.testid)
    else:
        checks += 1

    sleep(5)

print("no new tasks for 50 seconds terminating instance...")
os.system("poweroff")