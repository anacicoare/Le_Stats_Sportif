import os
from queue import Queue
from threading import Thread
from app.utils import all_jobs_status, all_jobs_results


class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        self.task_queue = Queue()
        self.workers = []
        self.num_threads = 0

        if os.environ.get("TP_NUM_OF_THREADS"):
            self.num_threads = int(os.environ.get("TP_NUM_OF_THREADS"))
        else:
            self.num_threads = os.cpu_count()

        self.create_task_runners()

    def create_task_runners(self):
        for _ in range(self.num_threads):
            worker = TaskRunner(self.task_queue)
            self.workers.append(worker)
            worker.start()

    def submit_task(self, task):
        self.task_queue.put(task)

    def terminate(self):
        for worker in self.workers:
            worker.graceful_shutdown = True
        for worker in self.workers:
            worker.join()


class TaskRunner(Thread):
    def __init__(self, task_queue: Queue):
        # TODO: init necessary data structures
        super().__init__()
        self.graceful_shutdown = False
        self.task_queue = task_queue

    def run(self):
        while True:
            # TODO
            # Get pending job
            (pending_job, job_id, question, state) = self.task_queue.get()
            # Execute the job and save the result to disk
            all_jobs_status.append({f'job_id_{job_id}': 'running'})
            job_result = pending_job(question)
            all_jobs_results[f'job_id_{job_id}'] = job_result
            for job in all_jobs_status:
                if job.get(f'job_id_{job_id}') == 'running':
                    job[f'job_id_{job_id}'] = 'done'

            # Repeat until graceful_shutdown
            if self.graceful_shutdown:
                break
