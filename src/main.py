import sys
import random


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
            start_edge, end_edge = int(participant), int(participant) + 1
            if (int((previous_ranking.index(remaining_participants[end_edge - 1]))) - (
                    int(previous_ranking.index(remaining_participants[start_edge - 1])))) != 1:
                print("redoing function")
                start_edge, end_edge = get_second_random_edge(random.random(), remaining_participants, previous_ranking)

    return start_edge, end_edge


def get_random_neighbouring_ranking(current_ranking):
    start_edge_A, end_edge_A = get_first_random_edge(random.random(), current_ranking)
    sub_list_A = current_ranking[0:start_edge_A - 1]
    sub_list_B = current_ranking[end_edge_A + 1:len(current_ranking)]
    first_edge = (current_ranking[start_edge_A - 1], current_ranking[end_edge_A - 1])
    print(first_edge)
    # print(f"start edge a, {start_edge_A}")
    # print(f"end edge a, {end_edge_A}")
    # print(f"sublist a, {sub_list_A}")
    # print(f"sublist b, {sub_list_B}")

    remaining_participants = sub_list_A + sub_list_B
    # print(remaining_participants)
    start_edge_B, end_edge_B = get_second_random_edge(random.random(), remaining_participants, current_ranking)
    end_edge_B_value = current_ranking[start_edge_B]
    second_edge = (remaining_participants[start_edge_B - 1], remaining_participants[end_edge_B - 1])
    print(second_edge)
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

    # print(f"sub tour = {sub_tour}")
    sub_tour.reverse()
    # print(f"reversed sub tour = {sub_tour}")
    current_ranking[sub_tour_start:sub_tour_end] = sub_tour
    print(current_ranking)
    new_first_edge = (first_edge[0], second_edge[1])
    new_second_edge = (second_edge[0],)
    print(f"new first edge = {new_first_edge}")

    if ((start_edge_A == 0) and (end_edge_A == 0)) or ((start_edge_B == 0) and (end_edge_B == 0)):
        print("Error, both edges are 0")
    return current_ranking, first_edge, second_edge


def get_cost(tournament_participants, tournament_weighting, ranking):
    cost = 0
    for matchup, weighting in tournament_weighting.items():
        for i in range(len(ranking)):
            for j in range(i + 1, len(ranking)):
                if matchup[0] == ranking[j] and matchup[1] == ranking[i]:
                    # print(f"{ranking[j]} beat {ranking[i]} by {weighting}")
                    cost = cost + int(weighting)
    # print(cost)
    return cost


def get_cost_difference(tournament_participants, tournament_weighting, first_edge, second_edge, cost):
    cost_difference = 0
    for matchup, weighting in tournament_weighting.items():
        if first_edge[1] == matchup[0] and first_edge[0] == matchup[1]:
            print(matchup, weighting)
            print(f"the first cost is reduced by {weighting}")
            first_edge_cost_reduction = int(weighting)
        if second_edge[1] == matchup[0] and second_edge[0] == matchup[1]:
            print(matchup, weighting)
            print(f"the second cost is reduced by {weighting}")
            second_edge_cost_reduction = int(weighting)
    return cost, cost_difference


def simulated_annealing_algorithm():
    tournament_participants, tournament_weighting = get_data()
    # tournament_weighting = {("B", "C"): "1", ("D", "E"): "6", ("G", "F"): "3", ("B", "A"): "2", ("D", "E"): "4",
    #                         ("A", "B"): "9", ("F", "A"): "6"}
    # tournament_participants = {"A": "Alice", "B": "bettie", "C": "Charlie", "D": "Dan", "E": "Ellie", "F": "Fred",
    #                            "G": "Gina", "H": "Harry"}
    # temperature_length = 10
    temperature_length = 1
    cooling_ration = 0.95
    num_non_improve = 8000
    loops_without_optimal_solution = 0
    current_ranking, initial_ranking = [i for i in tournament_participants], [i for i in tournament_participants]
    # get_random_neighbouring_ranking(initial_ranking, previous_ranking)
    cost = get_cost(tournament_participants, tournament_weighting, initial_ranking)
    # cost = get_cost(tournament_participants, tournament_weighting, previous_cost)
    for i in range(int(temperature_length)):
        neighbouring_ranking, first_edge, second_edge = get_random_neighbouring_ranking(current_ranking)
        cost, cost_difference = get_cost_difference(tournament_participants, tournament_weighting, first_edge,
                                                    second_edge, cost)
    print(cost)


simulated_annealing_algorithm()
