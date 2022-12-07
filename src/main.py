import sys
from random import random
from math import exp
from time import time


def get_data():
    file_data, total_participants = read_file()
    tournament_participants = get_participants(file_data, total_participants)
    tournament_weighting = get_weighting(file_data, total_participants)
    return tournament_participants, tournament_weighting


def read_file():
    file = open(sys.argv[1])
    file_data = file.read().splitlines()
    total_participants = file_data[0]
    return file_data, total_participants


def get_participants(file_data, total_participants):
    participants = {}
    for i in range(int(total_participants)):
        id, name = file_data[i + 1].split(",")
        participants[id] = name
    return participants


def get_weighting(file_data, total_participants):
    tournament_weighting = {}
    for i in range(int(total_participants) + 2, len(file_data)):
        weight, participant_A, participant_B = file_data[i].split(",")
        tournament_weighting[(participant_A, participant_B)] = weight
    return tournament_weighting


def get_first_random_edge(random_number, ranking_list):
    start_edge, end_edge = 0, 0
    for participant in range(len(ranking_list)):
        if (int(participant) - 1) / (len(ranking_list) - 1) <= random_number < int(participant) / (
                len(ranking_list) - 1):
            start_edge, end_edge = int(participant), int(participant) + 1
    return start_edge, end_edge


def get_second_random_edge(random_number, remaining_participants, previous_ranking):
    start_edge, end_edge = 0, 0
    for participant in range(len(remaining_participants)):
        if (int(participant) - 1) / (len(remaining_participants) - 1) <= random_number < int(participant) / (
                len(remaining_participants) - 1):
            start_edge, end_edge = int(participant) - 1, int(participant)
            if (int((previous_ranking.index(remaining_participants[end_edge - 1]))) - (
                    int(previous_ranking.index(remaining_participants[start_edge - 1])))) != 1:
                # print("redoing function")
                start_edge, end_edge = get_second_random_edge(random(), remaining_participants, previous_ranking)

    return start_edge, end_edge


def get_random_neighbouring_ranking(current_ranking):
    start_edge_A, end_edge_A = get_first_random_edge(random(), current_ranking)
    sub_list_A = current_ranking[:start_edge_A - 1]
    sub_list_B = current_ranking[end_edge_A + 1:]
    remaining_participants = sub_list_A + sub_list_B
    start_edge_B, end_edge_B = get_second_random_edge(random(), remaining_participants, current_ranking)
    sub_tour = []
    sub_tour_start = 0
    sub_tour_end = len(current_ranking) - 1

    if int(current_ranking.index(current_ranking[start_edge_A])) > int(
            current_ranking.index(remaining_participants[end_edge_B - 1])):
        sub_tour_start = int(current_ranking.index(remaining_participants[end_edge_B - 1]))
        sub_tour_end = int(current_ranking.index(current_ranking[start_edge_A]))
        sub_tour = current_ranking[int(current_ranking.index(remaining_participants[end_edge_B - 1])):int(
            current_ranking.index(current_ranking[start_edge_A]))]
    else:
        sub_tour_start = int(current_ranking.index(current_ranking[end_edge_A - 1]))
        sub_tour_end = int(
            current_ranking.index(remaining_participants[start_edge_B - 1]))
        sub_tour = current_ranking[int(current_ranking.index(current_ranking[end_edge_A - 1])):int(
            current_ranking.index(remaining_participants[start_edge_B - 1]))]

    sub_tour_reversed = sub_tour[:]
    sub_tour_reversed.reverse()
    old_tour = current_ranking[sub_tour_start - 1:sub_tour_end + 1]
    temp_current_ranking = current_ranking[:]
    temp_current_ranking[sub_tour_start:sub_tour_end] = sub_tour_reversed
    new_tour = temp_current_ranking[sub_tour_start - 1:sub_tour_end + 1]
    if ((start_edge_A == 0) and (end_edge_A == 0)) or ((start_edge_B == 0) and (end_edge_B == 0)):
        print("Error, both edges are 0")
    return temp_current_ranking, old_tour, new_tour


def get_cost(tournament_weighting, ranking):
    ranking_cost = 0
    for matchup, weighting in tournament_weighting.items():
        for i in range(len(ranking)):
            for j in range(i + 1, len(ranking)):
                if str(matchup[0]) == str(ranking[j]) and str(matchup[1]) == str(ranking[i]):
                    ranking_cost = ranking_cost + int(weighting)
    return ranking_cost


def get_cost_difference(tournament_participants, tournament_weighting, old_tour, new_tour, cost):
    old_tour_cost = get_cost(tournament_weighting, old_tour)
    new_tour_cost = get_cost(tournament_weighting, new_tour)
    new_cost = (int(cost) - old_tour_cost) + new_tour_cost
    return new_cost, new_cost - cost


def simulated_annealing_algorithm():
    tournament_participants, tournament_weighting = get_data()
    temperature_length = 10
    initial_temperature = 1.0
    current_temperature = initial_temperature
    cooling_ratio = 0.95
    num_non_improve = 1
    loops_without_optimal_solution = 0
    current_ranking, initial_ranking = list(tournament_participants), list(tournament_participants)

    cost = get_cost(tournament_weighting, initial_ranking)
    while loops_without_optimal_solution < num_non_improve:
        for _ in range(temperature_length):
            neighbouring_ranking,old_tour, new_tour = get_random_neighbouring_ranking(
                current_ranking)
            new_cost, cost_difference = get_cost_difference(tournament_participants, tournament_weighting,
                                                            old_tour, new_tour, cost)
            if cost_difference <= 0:
                current_ranking = neighbouring_ranking[:]
                cost = new_cost
            else:
                q = random()
                if q < (exp((-cost) / current_temperature)):
                    current_ranking = neighbouring_ranking[:]
                else:
                    loops_without_optimal_solution += 1

        current_temperature = current_temperature * cooling_ratio
    print(" ")
    print(f"final = {cost}")
    print(time() - start_time)


start_time = time()
simulated_annealing_algorithm()
