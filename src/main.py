import sys


def get_data():
    file_data, total_participants = read_file()
    tournament_participants = get_participants(file_data, total_participants)
    tournament_weighting = get_weighting(file_data, total_participants)


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


get_data()
