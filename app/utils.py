import threading


# Checking state of csv loading
initialized_csv_and_threadpool = threading.Event()

# Initialize job counter
job_counter = 1
