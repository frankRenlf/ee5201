# -*- coding: UTF-8 -*-
"""
    @Author : Frank.Ren
    @Project : code 
    @Product : PyCharm
    @createTime : 2023/9/30 18:01 
    @Email : sc19lr@leeds.ac.uk
    @github : https://github.com/frankRenlf
    @Description : 
"""

import multiprocessing
import time
import random


class Processor(multiprocessing.Process):
    def __init__(self, task_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue

    def run(self):
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                break
            task_name, task_duration = next_task
            print(f"{self.name} is executing {task_name}")
            time.sleep(task_duration)
            print(f"{self.name} has completed {task_name}")


def task_scheduler(task_list, processor_count):
    task_queue = multiprocessing.JoinableQueue()
    processors = [Processor(task_queue) for _ in range(processor_count)]

    for task in task_list:
        task_queue.put(task)

    for p in processors:
        p.start()

    for p in processors:
        task_queue.put(None)

    task_queue.join()
    for p in processors:
        p.join()


if __name__ == '__main__':
    task_list = [('Task1', 2), ('Task2', 3), ('Task3', 1)]
    processor_count = 2
    task_scheduler(task_list, processor_count)
