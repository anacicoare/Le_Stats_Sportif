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


def compute_best5(question):
    all_means = compute_states_mean(question)
    return {k: all_means[k] for k in list(all_means)[:5]}


def compute_worst5(question):
    all_means = compute_states_mean(question)
    return {k: all_means[k] for k in list(all_means)[-5:]}


def compute_global_mean(question):
    result = {}
    all_sum = 0
    all_len = 0

    all_states = set(list(map(lambda x: x.LocationDesc, webserver.data_ingestor.data_entries)))
    for state in all_states:
        state_data_entry = list(
            filter(lambda x: x.LocationDesc == state and x.Question == question, webserver.data_ingestor.data_entries))
        data_value_list = list(map(lambda x: x.Data_Value, state_data_entry))
        if len(data_value_list) != 0:
            all_sum += sum(data_value_list)
            all_len += len(data_value_list)

    return {"global_mean": all_sum / all_len}


def compute_diff_from_mean(question):
    result = {}
    global_mean = compute_global_mean(question)["global_mean"]
    all_states_mean = compute_states_mean(question)

    for state, mean in all_states_mean.items():
        result[state] = global_mean - mean

    return result


def compute_state_diff_from_mean(state, question):
    result = {}
    global_mean = compute_global_mean(question)["global_mean"]
    state_mean = compute_state_mean(state, question)

    for state, mean in state_mean.items():
        result[state] = global_mean - mean

    return result


def compute_mean_by_category(question):
    result = {}
    all_states = set(list(map(lambda x: x.LocationDesc, webserver.data_ingestor.data_entries)))
    for state in all_states:
        state_data_entries = list(filter(lambda x: x.LocationDesc == state and x.Question == question, webserver.data_ingestor.data_entries))
        all_stratification1_for_state = set(list(map(lambda x: x.Stratification1, state_data_entries)))
        for stratification1 in all_stratification1_for_state:
            stratification1_data_entries = list(filter(lambda x: x.Stratification1 == stratification1, state_data_entries))
            all_stratificationcategory1_for_state = set(list(map(lambda x: x.StratificationCategory1, stratification1_data_entries)))
            for stratificationcategory1 in all_stratificationcategory1_for_state:
                stratificationcategory1_data_entries = list(filter(lambda x: x.StratificationCategory1 == stratificationcategory1, stratification1_data_entries))
                data_value_list = list(map(lambda x: x.Data_Value, stratificationcategory1_data_entries))
                if len(data_value_list) != 0:
                    mean = sum(data_value_list) / len(data_value_list)
                    result[f"('{state}', '{stratificationcategory1}', '{stratification1}')"] = mean

    result = dict(sorted(result.items(), key=lambda x: x[1]))
    if question in webserver.data_ingestor.questions_best_is_max:
        result = dict(reversed(result.items()))

    return result


def compute_state_mean_by_category(state, question):
    result = {state: {}}
    state_data_entries = list(
        filter(lambda x: x.LocationDesc == state and x.Question == question, webserver.data_ingestor.data_entries))
    all_stratification1_for_state = set(list(map(lambda x: x.Stratification1, state_data_entries)))
    for stratification1 in all_stratification1_for_state:
        stratification1_data_entries = list(filter(lambda x: x.Stratification1 == stratification1, state_data_entries))
        all_stratificationcategory1_for_state = set(
            list(map(lambda x: x.StratificationCategory1, stratification1_data_entries)))
        for stratificationcategory1 in all_stratificationcategory1_for_state:
            stratificationcategory1_data_entries = list(
                filter(lambda x: x.StratificationCategory1 == stratificationcategory1, stratification1_data_entries))
            data_value_list = list(map(lambda x: x.Data_Value, stratificationcategory1_data_entries))
            if len(data_value_list) != 0:
                mean = sum(data_value_list) / len(data_value_list)
                result[state][f"('{stratificationcategory1}', '{stratification1}')"] = mean

    # result = dict(sorted(result.items(), key=lambda x: x[1]))
    # if question in webserver.data_ingestor.questions_best_is_max:
    #     result = dict(reversed(result.items()))

    return result

