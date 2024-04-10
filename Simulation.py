import os
import csv
import pickle
from num2words import num2words
import random
import time

inflation = 0.03
stockReturn = 0.1 - inflation
bondReturn = 0.05 - inflation
startingYear = 2024
count = 0
death = 0
rsfPot = 0
withdraws = 0
cost = 0
potWithdraws = 0
rsfAccountIncome = 0
rsfPotIncome = 0

age_death_table = {
    1: 21024,
    2: 1440,
    3: 936,
    4: 720,
    5: 612,
    6: 504,
    7: 432,
    8: 396,
    9: 396,
    10: 396,
    11: 468,
    12: 504,
    13: 648,
    14: 792,
    15: 1116,
    16: 1548,
    17: 2160,
    18: 2916,
    19: 3744,
    20: 4428,
    21: 4968,
    22: 5436,
    23: 5688,
    24: 5976,
    25: 6156,
    26: 6408,
    27: 6624,
    28: 6948,
    29: 7236,
    30: 7596,
    31: 7956,
    32: 8244,
    33: 8496,
    34: 8712,
    35: 8964,
    36: 9216,
    37: 9612,
    38: 10008,
    39: 10476,
    40: 10908,
    41: 11340,
    42: 11736,
    43: 12096,
    44: 12564,
    45: 13104,
    46: 13824,
    47: 14796,
    48: 15984,
    49: 17172,
    50: 18324,
    51: 19548,
    52: 21024,
    53: 22788,
    54: 24660,
    55: 26604,
    56: 28620,
    57: 30780,
    58: 32976,
    59: 35280,
    60: 37692,
    61: 40176,
    62: 42876,
    63: 45468,
    64: 47952,
    65: 50184,
    66: 52128,
    67: 54252,
    68: 56484,
    69: 58896,
    70: 61524,
    71: 64512,
    72: 67608,
    73: 71136,
    74: 75312,
    75: 80964,
    76: 85680,
    77: 90468,
    78: 94968,
    79: 99720,
    80: 103680,
    81: 107172,
    82: 110160,
    83: 112896,
    84: 115524,
    85: 116928,
    86: 116964,
    87: 115272,
    88: 112284,
    89: 107892,
    90: 101880,
    91: 94464,
    92: 85752,
    93: 75420,
    94: 64152,
    95: 52704,
    96: 41796,
    97: 31932,
    98: 23472,
    99: 16632,
    100: 11376,
    101: 7560,
    102: 4860,
    103: 3060,
    104: 1836,
    105: 1080,
    106: 612,
    107: 324,
    108: 144,
    109: 72,
    110: 36,
    111: 36,
    112: 0
}

class Person:
    def __init__(self, initBirth, RSF):
        self.alive = True
        self.RSFAccount = RSF
        self.birth = initBirth

    def getAge(self, currentYear):
        return currentYear - self.birth


class Generation:
    def __init__(self, yearInit):
        global rsfPot
        global cost
        self.people = []
        self.year = yearInit
        if rsfPot > (3600000 * 10000):
            rsfPot = rsfPot - (3600000 * 10000)
        else:
            cost += 3600000 * 10000
        for person in range(3600000):  # How many newborns
            self.people.append(Person(yearInit, 10000))  # Add person to generation


generations = []  # List of generation objects in population

def rsfBalance():
    sum = 0
    for generation in generations:
        for person in generation.people:
            sum += person.RSFAccount
    return sum

def getPopulation():
    sum = 0
    for generation in generations:
        sum += len(generation.people)
    return sum

def invest():
    global rsfPot
    global rsfAccountIncome
    global rsfPotIncome
    for generation in generations:
        for person in generation.people:
            if person.getAge(startingYear + count) < 65: #stocks
                person.RSFAccount += (stockReturn * person.RSFAccount)
                rsfAccountIncome += (stockReturn * person.RSFAccount)
                
            else: #bonds
                person.RSFAccount += (bondReturn * person.RSFAccount)
                rsfAccountIncome += (stockReturn * person.RSFAccount)
    rsfPot += (stockReturn * rsfPot)
    rsfPotIncome += (stockReturn * rsfPot)


def simDeath():
    global death
    global rsfPot
    for generation in generations:
        age = (startingYear + count) - generation.year
        if 1 <= age <= 99:
            death_count = lookup_death_count(age)
            for _ in range(death_count):
                if generation.people:
                    rsfPot += generation.people.pop().RSFAccount
                    death += 1

def lookup_death_count(age):
    return age_death_table.get(age, 0)

def withdraw():
    global withdraws
    global potWithdraws
    for generation in generations:
        for person in generation.people:
            if person.getAge(startingYear + count) >= 65:
                if person.RSFAccount >= 30000:
                    person.RSFAccount -= 30000
                    withdraws += 30000
                else:
                    rsfPot = rsfPot - 30000
                    potWithdraws += 30000

# Define a function to save the data to a CSV file
def save_data_to_csv():
    with open('RSF.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if os.path.getsize('RSF.csv') == 0:  # If the file is empty, write column titles
            writer.writerow(['Count', 'Total Population', 'Total Deaths', 'RSF Accounts Total','Total RSF Accounts Investment Income','Total RSF Account Withdraws','Pot Total','Total Pot Investment Income','Total Pot Withdraws','Total Cost'])
        writer.writerow([count, getPopulation(), death, rsfBalance(),rsfAccountIncome,withdraws,rsfPot, rsfPotIncome,potWithdraws,cost])

# Define a function to save the state of the program
def save_state():
    with open('state.pkl', 'wb') as f:
        pickle.dump((count, death, rsfPot, rsfAccountIncome, withdraws, rsfPotIncome, potWithdraws, cost, generations), f)

# Define a function to load the state of the program
def load_state():
    global count, death, rsfPot, rsfAccountIncome, withdraws, rsfPotIncome, potWithdraws, cost, generations
    if os.path.exists('state.pkl'):
        with open('state.pkl', 'rb') as f:
            count, death, rsfPot, rsfAccountIncome, withdraws, rsfPotIncome, potWithdraws, cost, generations = pickle.load(f)
    else:
        count = 0
        death = 0
        rsfPot = 0
        rsfAccountIncome = 0
        withdraws = 0
        rsfPotIncome = 0
        potWithdraws = 0
        cost = 0
        generations = []

# Load state at the beginning
print("Picking up from state.pkl")
load_state()

while True:
    os.system("clear")
    count += 1
    print(f"Loading year {startingYear + count}...")
    print("Simulating Deaths...")
    simDeath()
    print("Done.")
    print("Simulating Investments...")
    invest()
    print("Done.")
    print("Simulating Withdraws...")
    withdraw()
    print("Done.")
    print("Creating Next Generation...")
    generations.append(Generation(startingYear + count))
    print("Done.")
    print("Saving to state.pkl...")
    save_state()
    print("Done.")
    print("Saving data to CSV...")
    save_data_to_csv()
    print("Done.")

