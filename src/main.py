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
            start_edge, end_edge = int(participant) - 1, int(participant)
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
        second_edge = (start_edge_B, end_edge_B)
        new_first_edge = (second_edge[0], first_edge[0])
        new_second_edge = (second_edge[1], first_edge[1])
    else:
        sub_tour_start = int(current_ranking.index(current_ranking[end_edge_A - 1]))
        sub_tour_end = int(
            current_ranking.index(remaining_participants[start_edge_B - 1]))
        sub_tour = current_ranking[int(current_ranking.index(current_ranking[end_edge_A - 1])):int(
            current_ranking.index(remaining_participants[start_edge_B - 1]))]
        second_edge = (start_edge_B + 2, end_edge_B + 2)
        new_first_edge = (first_edge[0], second_edge[0])
        new_second_edge = (first_edge[1], second_edge[1])

    # print(f"sub tour = {sub_tour}")
    sub_tour.reverse()

    # print(f"reversed sub tour = {sub_tour}")
    current_ranking[sub_tour_start:sub_tour_end] = sub_tour
    print(current_ranking)

    if ((start_edge_A == 0) and (end_edge_A == 0)) or ((start_edge_B == 0) and (end_edge_B == 0)):
        print("Error, both edges are 0")
    return current_ranking, first_edge, second_edge, new_first_edge, new_second_edge


def get_cost(tournament_participants, tournament_weighting, ranking):
    cost = 0
    i_over_j_wins = 0
    j_over_i_wins = 0
    for matchup, weighting in tournament_weighting.items():
        for i in range(len(ranking)):
            for j in range(i + 1, len(ranking)):
                if matchup[0] == ranking[j] and matchup[1] == ranking[i]:
                    # print(f"{ranking[j]} beat {ranking[i]} by {weighting}")
                    j_over_i_wins = int(weighting)
                if matchup[0] == ranking[i] and matchup[1] == ranking[j]:
                    i_over_j_wins = int(weighting)
                if j_over_i_wins - i_over_j_wins > 0:
                    cost = cost + (j_over_i_wins - i_over_j_wins)
    # print(cost)
    return cost


def calculate_edge_cost(matchup, weighting, edge):
    cost_reduction = 0
    first_weighting = 0
    second_weighting = 0
    if str(edge[1]) == str(matchup[0]) and str(edge[0]) == str(matchup[1]):
        first_weighting = weighting
        print(matchup, weighting)
        print(f"first weighting = {first_weighting} ")
    if edge[0] == matchup[0] and edge[1] == matchup[1]:
        second_weighting = weighting
        print(matchup, weighting)
        print(f"second weighting = {second_weighting} ")
    cost_reduction = int(first_weighting) - int(second_weighting)
    if cost_reduction != 0:
        print(f"cost reduction = {cost_reduction}")
    return cost_reduction


def get_cost_difference(tournament_participants, tournament_weighting, first_edge, second_edge, new_first_edge,
                        new_second_edge, cost):
    cost_difference = 0
    new_cost = int(cost)
    first_edge_cost_reduction = 0
    second_edge_cost_reduction = 0
    new_first_edge_cost_reduction = 0
    new_second_edge_cost_reduction = 0
    print(f"first edge {first_edge}")
    print(f"second edge {second_edge}")
    print(f"new first edge {new_first_edge}")
    print(f"new second edge {new_second_edge}")

    for matchup, weighting in tournament_weighting.items():
        first_edge_cost_reduction = calculate_edge_cost(matchup, weighting, first_edge)
        second_edge_cost_reduction = calculate_edge_cost(matchup, weighting, second_edge)

        new_first_edge_cost_reduction = calculate_edge_cost(matchup, weighting, new_first_edge)

        new_second_edge_cost_reduction = calculate_edge_cost(matchup, weighting, new_second_edge)
        if first_edge_cost_reduction != 0 and second_edge_cost_reduction != 0 and new_first_edge_cost_reduction != 0 and new_second_edge_cost_reduction != 0:
            print(first_edge_cost_reduction, second_edge_cost_reduction, new_first_edge_cost_reduction,
                  new_second_edge_cost_reduction)
        new_cost = new_cost - (int((first_edge_cost_reduction + second_edge_cost_reduction))) + (
                    new_first_edge_cost_reduction + new_second_edge_cost_reduction)

        # if first_edge[1] == matchup[0] and first_edge[0] == matchup[1]:
        #     print(matchup, weighting)
        #     print(f"the first cost is reduced by {weighting}")
        #     first_edge_cost_reduction = int(weighting)
        # if second_edge[1] == matchup[0] and second_edge[0] == matchup[1]:
        #     print(matchup, weighting)
        #     print(f"the second cost is reduced by {weighting}")
        #     second_edge_cost_reduction = int(weighting)
        # if new_first_edge[1] == matchup[0] and new_first_edge[0] == matchup[1]:
        #     print(matchup, weighting)
        #     print(f"first new edges cost is reduced by {weighting}")
        #     new_first_edge_cost_reduction = int(weighting)
        # if new_second_edge[1] == matchup[0] and new_second_edge[0] == matchup[1]:
        #     print(matchup, weighting)
        #     print(f"second new edges cost is reduced by {weighting}")
        #     new_second_edge_cost_reduction = int(weighting)
    print(f"cost = {cost}")
    print(f"new cost = {new_cost}")
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
        neighbouring_ranking, first_edge, second_edge, new_first_edge, new_second_edge = get_random_neighbouring_ranking(
            current_ranking)
        cost, cost_difference = get_cost_difference(tournament_participants, tournament_weighting, first_edge,
                                                    second_edge, new_first_edge, new_second_edge, cost)
    print(cost)


simulated_annealing_algorithm()
