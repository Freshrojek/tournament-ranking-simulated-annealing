import sys

def read_file():
    file = open(sys.argv[1])
    file_data = file.read().splitlines()
    return file_data

def get_participants(file_data):
    total_participants = file_data[0]
    participants = {}
    for i in range(int(total_participants)):
        id, name = file_data[i+1].split(",")
        participants[id] = name

def get_weighting():
    tournament_weighting = {}
    for i in range(int(total_participants) + 2, len(file_data)):
        weight, participant_A, participant_B = file_data[i].split(",")
        tournament_weighting[(participant_A,participant_B)] = weight




read_file()