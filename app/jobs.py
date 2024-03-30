from app import webserver
from datetime import datetime
from collections import OrderedDict


def compute_states_mean(question):
    webserver.logger.info(f"[{datetime.now()}] Computing mean for states ...")

    # Order result by mean value (ascending)
    result = OrderedDict({}, key=lambda x: x[1])

    all_states = set(list(map(lambda x: x.LocationDesc, webserver.data_ingestor.data_entries)))
    for state in all_states:
        state_data_entry = list(filter(lambda x: x.LocationDesc == state and x.Question == question, webserver.data_ingestor.data_entries))
        data_value_list = list(map(lambda x: x.Data_Value, state_data_entry))
        mean = sum(data_value_list) / len(data_value_list)
        result[state] = mean

    return result
