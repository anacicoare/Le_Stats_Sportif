from app import webserver
from datetime import datetime
from collections import OrderedDict
import math


def compute_states_mean(question):
    # Order result by mean value (ascending)
    result = {}

    all_states = set(list(map(lambda x: x.LocationDesc, webserver.data_ingestor.data_entries)))
    for state in all_states:
        state_data_entry = list(filter(lambda x: x.LocationDesc == state and x.Question == question, webserver.data_ingestor.data_entries))
        data_value_list = list(map(lambda x: x.Data_Value, state_data_entry))
        if len(data_value_list) != 0:
            mean = sum(data_value_list) / len(data_value_list)
            result[state] = mean


    result = dict(sorted(result.items(), key=lambda x: x[1]))
    if question in webserver.data_ingestor.questions_best_is_max:
        result = dict(reversed(result.items()))

    return result


def compute_state_mean(state, question):
    # Order result by mean value (ascending)
    result = {}

    state_data_entry = list(filter(lambda x: x.LocationDesc == state and x.Question == question, webserver.data_ingestor.data_entries))
    data_value_list = list(map(lambda x: x.Data_Value, state_data_entry))
    if len(data_value_list) != 0:
        mean = sum(data_value_list) / len(data_value_list)
        result[state] = mean

    return result
