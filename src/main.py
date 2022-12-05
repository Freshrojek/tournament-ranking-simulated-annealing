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
    print(f"start edge a, {start_edge_A}")
    print(f"end edge a, {end_edge_A}")
    print(f"sublist a, {sub_list_A}")
    print(f"sublist b, {sub_list_B}")

    remaining_participants = sub_list_A + sub_list_B
    print(remaining_participants)
    start_edge_B, end_edge_B = get_second_random_edge(random.random(), remaining_participants, current_ranking)
    end_edge_B_value = current_ranking[start_edge_B]
    print(f"start edge b, {start_edge_B}")
    print(f"end edge b, {end_edge_B}")
    sub_list_C = remaining_participants[0:start_edge_B - 1]
    sub_list_D = remaining_participants[end_edge_B:len(remaining_participants)]
    print(sub_list_C + sub_list_D)
    sub_tour = []
    print(f"index1test {current_ranking.index(current_ranking[start_edge_A])}")
    print(f"index2test {current_ranking.index(remaining_participants[end_edge_B - 1])}")

    if int(current_ranking.index(current_ranking[start_edge_A])) > int(
            current_ranking.index(remaining_participants[end_edge_B - 1])):
        sub_tour = current_ranking[int(current_ranking.index(remaining_participants[end_edge_B - 1])):int(
            current_ranking.index(current_ranking[start_edge_A]))]
        sub_tour.insert(int(current_ranking.index(current_ranking[end_edge_A-1])), current_ranking[end_edge_A-1])
        sub_tour.insert(int(
            current_ranking.index(remaining_participants[start_edge_B - 1])), remaining_participants[start_edge_B - 1])
    else:
        sub_tour = current_ranking[int(current_ranking.index(current_ranking[end_edge_A - 1])):int(
            current_ranking.index(remaining_participants[start_edge_B - 1]))]
        sub_tour.insert(int(current_ranking.index(remaining_participants[end_edge_B - 1])),
                        remaining_participants[end_edge_B - 1])
        sub_tour.insert(int(current_ranking.index(current_ranking[start_edge_A])),
                        current_ranking.index(current_ranking[start_edge_A]))
    sub_tour.reverse()
    print(f"reversed sub tour = {sub_tour}")

    print(current_ranking)

    if ((start_edge_A == 0) and (end_edge_A == 0)) or ((start_edge_B == 0) and (end_edge_B == 0)):
        print("Error, both edges are 0")


def simulated_annealing_algorithm():
    # tournament_participants, tournament_weighting = get_data()
    tournament_participants = {"A": "Alice", "B": "bettie", "C": "Charlie", "D": "Dan", "E": "Ellie", "F": "Fred",
                               "G": "Gina", "H": "Harry"}
    temperature_length = 10
    cooling_ration = 0.95
    num_non_improve = 8000
    loops_without_optimal_solution = 0
    initial_ranking = [i for i in tournament_participants]
    for i in range(int(temperature_length)):
        neighbouring_ranking = get_random_neighbouring_ranking(initial_ranking)


simulated_annealing_algorithm()
