from app import webserver
from flask import request, jsonify
from threading import Lock
import app.utils as utils
import app.jobs as jobs
from datetime import datetime

jobs_lock = Lock()

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    if request.method == 'GET':
        # TODO
        # Check if job_id is valid
        job_id = int(job_id.split('_')[-1])
        if not 0 < int(job_id) < utils.job_counter:
            webserver.logger.error(f"[{datetime.now}] Job ID {job_id} not found")
            return jsonify({
                "status": "error",
                "reason": "Invalid job_id"
            })

        # Check if job_id is done and return the result
        if utils.all_jobs_results.get(f'job_id_{job_id}'):
            return jsonify({
                "status": "done",
                "data": utils.all_jobs_results[f'job_id_{job_id}']
            })
        else:
            return jsonify({
                "status": "running",
            })

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Get request data
    data = request.json

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method == 'POST':
        # Wait for the data to be loaded
        utils.initialized_csv_and_threadpool.wait()

        # Safely increment job counter
        with jobs_lock:
            job_id = utils.job_counter
            # Submit the task to the thread pool
            response = webserver.tasks_runner.submit_task((jobs.compute_states_mean, job_id, data['question'], None))
            utils.job_counter += 1

    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    if request.method == 'POST':
        # Wait for the data to be loaded
        utils.initialized_csv_and_threadpool.wait()

        # Get request data
        data = request.json

        # Safely increment job counter
        with jobs_lock:
            job_id = utils.job_counter
            # Submit the task to the thread pool
            response = webserver.tasks_runner.submit_task((jobs.compute_state_mean, job_id, data['question'], data['state']))
            utils.job_counter += 1

        return jsonify({"job_id": "job_id_" + str(job_id)})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    if request.method == 'POST':
        # Wait for the data to be loaded
        utils.initialized_csv_and_threadpool.wait()

        # Get request data
        data = request.json

        # Safely increment job counter
        with jobs_lock:
            job_id = utils.job_counter
            # Submit the task to the thread pool
            response = webserver.tasks_runner.submit_task((jobs.compute_best5, job_id, data['question'], None))
            utils.job_counter += 1

        return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    if request.method == 'POST':
        # Wait for the data to be loaded
        utils.initialized_csv_and_threadpool.wait()

        # Get request data
        data = request.json

        # Safely increment job counter
        with jobs_lock:
            job_id = utils.job_counter
            # Submit the task to the thread pool
            response = webserver.tasks_runner.submit_task((jobs.compute_worst5, job_id, data['question'], None))
            utils.job_counter += 1

        return jsonify({"job_id": "job_id_" + str(job_id)})


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
   if request.method == 'POST':
        # Wait for the data to be loaded
        utils.initialized_csv_and_threadpool.wait()

        # Get request data
        data = request.json

        # Safely increment job counter
        with jobs_lock:
            job_id = utils.job_counter
            # Submit the task to the thread pool
            response = webserver.tasks_runner.submit_task((jobs.compute_global_mean, job_id, data['question'], None))
            utils.job_counter += 1

        return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
   if request.method == 'POST':
        # Wait for the data to be loaded
        utils.initialized_csv_and_threadpool.wait()

        # Get request data
        data = request.json

        # Safely increment job counter
        with jobs_lock:
            job_id = utils.job_counter
            # Submit the task to the thread pool
            response = webserver.tasks_runner.submit_task((jobs.compute_diff_from_mean, job_id, data['question'], None))
            utils.job_counter += 1

        return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    if request.method == 'POST':
        # Wait for the data to be loaded
        utils.initialized_csv_and_threadpool.wait()

        # Get request data
        data = request.json

        # Safely increment job counter
        with jobs_lock:
            job_id = utils.job_counter
            # Submit the task to the thread pool
            response = webserver.tasks_runner.submit_task((jobs.compute_state_diff_from_mean, job_id, data['question'], data['state']))
            utils.job_counter += 1

        return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})


@webserver.route('/api/jobs', methods=['GET'])
def api_jobs():
    if request.method == 'GET':
        # Return all jobs
        return jsonify({
            "status": "done",
            "data": utils.all_jobs_status
        })

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
