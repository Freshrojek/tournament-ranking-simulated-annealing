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


def get_random_neighbouring_ranking(tournament_participants, tournament_weighting, initial_ranking):
    random_number = random.random()
    for participant_id in tournament_participants:
        if ((int(participant_id) - 1) / len(tournament_participants) <= random_number) and (
                random_number < (int(participant_id) / len(tournament_participants))):
            start_edge, end_edge = int(participant_id), int(participant_id) + 1
            print(start_edge, random_number, end_edge)


def simulated_annealing_algorithm():
    tournament_participants, tournament_weighting = get_data()
    initial_temperature = 1
    temperature_length = 10
    cooling_ration = 0.95
    num_non_improve = 8000
    loops_without_optimal_solution = 0
    initial_ranking = [i for i in tournament_participants]
    for i in range(int(temperature_length)):
        neighbouring_ranking = get_random_neighbouring_ranking(tournament_participants, tournament_weighting,
                                                               initial_ranking)


simulated_annealing_algorithm()
