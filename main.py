import multiprocessing
import time
import os  # 这是新导入的库，用于获取PID


class Task:
    def __init__(self, id, execution_time):
        self.id = id
        self.execution_time = execution_time
        self.portion1_completed = multiprocessing.Value('b', False)


def schedule_first_portion(task, processor_id):
    print(f"Processor {processor_id} (PID: {os.getpid()}) is executing first portion of Task {task.id}")
    time.sleep(task.execution_time / 2)
    task.portion1_completed.value = True
    print(f"Processor {processor_id} (PID: {os.getpid()}) has completed first portion of Task {task.id}")


def schedule_second_portion(task, processor_id):
    print(f"Processor {processor_id} (PID: {os.getpid()}) is waiting to execute second portion of Task {task.id}")
    while not task.portion1_completed.value:
        pass
    print(f"Processor {processor_id} (PID: {os.getpid()}) is executing second portion of Task {task.id}")
    time.sleep(task.execution_time / 2)
    print(f"Processor {processor_id} (PID: {os.getpid()}) has completed second portion of Task {task.id}")


def schedule_non_migratable_task(task, processor_id):
    print(f"Processor {processor_id} (PID: {os.getpid()}) is executing non-migratable Task {task.id}")
    time.sleep(task.execution_time)
    print(f"Processor {processor_id} (PID: {os.getpid()}) has completed non-migratable Task {task.id}")


def main():
    task1 = Task(1, 2)
    task2 = Task(2, 3)

    processor1 = multiprocessing.Process(target=schedule_first_portion, args=(task1, 1,))
    processor2 = multiprocessing.Process(target=schedule_second_portion, args=(task1, 2,))
    processor3 = multiprocessing.Process(target=schedule_non_migratable_task, args=(task2, 3,))

    tasks = [processor1, processor2, processor3]
    for task in sorted(tasks, key=lambda x: x._args[0].execution_time):
        task.start()

    for task in tasks:
        task.join()


if __name__ == "__main__":
    main()
