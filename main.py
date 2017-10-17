from task import QueManager
from time import sleep

queue = QueManager()

while True:
    print("Checking Tasks")
    task = queue.get_task()
    if task:
        result = task.run()
        queue.send_result(result.getvalue(), task.testid)
    sleep(5)
