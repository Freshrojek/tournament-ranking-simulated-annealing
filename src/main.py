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
        if ((int(participant) - 1) / (len(ranking_list) - 1) <= random_number) and (
                random_number < (int(participant) / (len(ranking_list) - 1))):
            start_edge, end_edge = int(participant), int(participant) + 1
    return start_edge, end_edge


def get_second_random_edge(random_number, remaining_participants, previous_ranking):
    start_edge, end_edge = 0, 0
    for participant in range(len(remaining_participants)):
        if ((int(participant) - 1) / (len(remaining_participants) - 1) <= random_number) and (
                random_number < (int(participant) / (len(remaining_participants) - 1))):
            start_edge, end_edge = int(participant) - 1, int(participant)
            if (int((previous_ranking.index(remaining_participants[end_edge - 1]))) - (
                    int(previous_ranking.index(remaining_participants[start_edge - 1])))) != 1:
                # print("redoing function")
                start_edge, end_edge = get_second_random_edge(random(), remaining_participants, previous_ranking)

    return start_edge, end_edge


def get_random_neighbouring_ranking(current_ranking):
    start_edge_A, end_edge_A = get_first_random_edge(random(), current_ranking)
    sub_list_A = current_ranking[0:start_edge_A - 1]
    sub_list_B = current_ranking[end_edge_A + 1:len(current_ranking)]
    first_edge = (current_ranking[start_edge_A - 1], current_ranking[end_edge_A - 1])
    # print(first_edge)
    # print(f"start edge a, {start_edge_A}")
    # print(f"end edge a, {end_edge_A}")
    # print(f"sublist a, {sub_list_A}")
    # print(f"sublist b, {sub_list_B}")

    remaining_participants = sub_list_A + sub_list_B
    # print(remaining_participants)
    start_edge_B, end_edge_B = get_second_random_edge(random(), remaining_participants, current_ranking)
    end_edge_B_value = current_ranking[start_edge_B]
    # print(f"start edge b, {start_edge_B}")
    # print(f"end edge b, {end_edge_B}")
    sub_list_C = remaining_participants[0:start_edge_B - 1]
    sub_list_D = remaining_participants[end_edge_B:len(remaining_participants)]
    # print(sub_list_C + sub_list_D)
    sub_tour = []
    sub_tour_start = 0
    sub_tour_end = len(current_ranking) - 1
    # print(f"index1test {current_ranking.index(current_ranking[start_edge_A])}")
    # print(f"index2test {current_ranking.index(remaining_participants[end_edge_B - 1])}")
    second_edge = ()
    new_first_edge = ()
    new_second_edge = ()

    if int(current_ranking.index(current_ranking[start_edge_A])) > int(
            current_ranking.index(remaining_participants[end_edge_B - 1])):
        sub_tour_start = int(current_ranking.index(remaining_participants[end_edge_B - 1]))
        sub_tour_end = int(current_ranking.index(current_ranking[start_edge_A]))
        sub_tour = current_ranking[int(current_ranking.index(remaining_participants[end_edge_B - 1])):int(
            current_ranking.index(current_ranking[start_edge_A]))]

        second_edge = (current_ranking[start_edge_B - 1], current_ranking[end_edge_B - 1])
        new_first_edge = (second_edge[0], first_edge[0])
        new_second_edge = (second_edge[1], first_edge[1])
    else:
        sub_tour_start = int(current_ranking.index(current_ranking[end_edge_A - 1]))
        sub_tour_end = int(
            current_ranking.index(remaining_participants[start_edge_B - 1]))
        sub_tour = current_ranking[int(current_ranking.index(current_ranking[end_edge_A - 1])):int(
            current_ranking.index(remaining_participants[start_edge_B - 1]))]
        second_edge = (current_ranking[start_edge_B + 1], current_ranking[end_edge_B + 1])
        new_first_edge = (first_edge[0], second_edge[0])
        new_second_edge = (first_edge[1], second_edge[1])

    # print(f"sub tour = {sub_tour}")
    sub_tour_reversed = sub_tour[:]
    sub_tour_reversed.reverse()

    # print(f"reversed sub tour = {sub_tour}")
    old_tour = current_ranking[sub_tour_start - 1:sub_tour_end + 1]
    temp_current_ranking = current_ranking[:]
    temp_current_ranking[sub_tour_start:sub_tour_end] = sub_tour_reversed
    new_tour = temp_current_ranking[sub_tour_start - 1:sub_tour_end + 1]
    # print(f"old_tour {old_tour}")
    # print(f"new_tour {new_tour}")

    if ((start_edge_A == 0) and (end_edge_A == 0)) or ((start_edge_B == 0) and (end_edge_B == 0)):
        print("Error, both edges are 0")
    return temp_current_ranking, first_edge, second_edge, new_first_edge, new_second_edge, old_tour, new_tour


def get_cost(tournament_weighting, ranking):
    ranking_cost = 0
    for matchup, weighting in tournament_weighting.items():
        for i in range(len(ranking)):
            for j in range(i + 1, len(ranking)):
                if str(matchup[0]) == str(ranking[j]) and str(matchup[1]) == str(ranking[i]):
                    ranking_cost = ranking_cost + int(weighting)
    # print(ranking_cost)
    return ranking_cost


def get_cost_difference(tournament_participants, tournament_weighting, first_edge, second_edge, new_first_edge,
                        new_second_edge, old_tour, new_tour, cost):
    # print(f"first edge {first_edge}")
    # print(f"second edge {second_edge}")
    # print(f"new first edge {new_first_edge}")
    # print(f"new second edge {new_second_edge}")

    # first_edge_cost = get_cost(tournament_weighting, first_edge)
    # print(f"first_edge_cost = {first_edge_cost}")
    #
    # second_edge_cost = get_cost(tournament_weighting, second_edge)
    # print(f"second_edge_cost = {second_edge_cost}")
    #
    # new_first_edge_cost = get_cost(tournament_weighting, new_first_edge)
    # print(f"new_first_edge_cost = {new_first_edge_cost}")
    #
    # new_second_edge_cost = get_cost(tournament_weighting, new_second_edge)
    # print(f"new_second_edge_cost = {new_second_edge_cost}")

    old_tour_cost = get_cost(tournament_weighting, old_tour)
    new_tour_cost = get_cost(tournament_weighting, new_tour)

    # print(f"old_tour_cost = {old_tour_cost}")
    # print(f"new_tour_cost = {new_tour_cost}")

    # new_cost = cost - ((first_edge_cost + second_edge_cost) + (new_first_edge_cost + new_second_edge_cost))
    new_cost = (int(cost) - old_tour_cost) + new_tour_cost
    # print(f"cost = {cost}")
    # print(f"new cost = {new_cost}")
    # print(f"new cost - cost = {new_cost - cost}")

    return new_cost, new_cost - cost


def simulated_annealing_algorithm():
    tournament_participants, tournament_weighting = get_data()
    # tournament_weighting = {("B", "C"): "1", ("G", "F"): "3", ("D", "E"): "4",
    #                         ("A", "B"): "9", ("F", "A"): "6"}
    # tournament_participants = {"A": "Alice", "B": "bettie", "C": "Charlie", "D": "Dan", "E": "Ellie", "F": "Fred",
    #                            "G": "Gina", "H": "Harry"}
    # temperature_length = 10
    temperature_length = 1
    initial_temperature = 1.0
    current_temperature = float(initial_temperature)
    cooling_ratio = 0.95
    num_non_improve = 1
    loops_without_optimal_solution = 0
    current_ranking, initial_ranking = [i for i in tournament_participants], [i for i in tournament_participants]
    # get_random_neighbouring_ranking(initial_ranking, previous_ranking)
    cost = get_cost(tournament_weighting, initial_ranking)
    while loops_without_optimal_solution < num_non_improve:
        for i in range(int(temperature_length)):
            neighbouring_ranking, first_edge, second_edge, new_first_edge, new_second_edge, old_tour, new_tour = get_random_neighbouring_ranking(
                current_ranking)
            new_cost, cost_difference = get_cost_difference(tournament_participants, tournament_weighting, first_edge,
                                                            second_edge, new_first_edge, new_second_edge,
                                                            old_tour, new_tour, cost)
            if cost_difference <= 0:
                # print("found better ranking")
                current_ranking = neighbouring_ranking[:]
                cost = new_cost
                # check = get_cost(tournament_weighting, current_ranking)
                # # print(f"getting cost for  {current_ranking}")
                #
                # print(f"verifying the kemeny score is {check}")
                # if check != new_cost:
                #     print("error")
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
