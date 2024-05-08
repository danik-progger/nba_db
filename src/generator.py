import csv
import random
from faker import Faker

fake = Faker()

# Generate 100 random names
names = ["'" + fake.first_name() + "'" for _ in range(100)]
last_names = ["'" + fake.last_name() + "'" for _ in range(100)]


def fan():
    return random.randint(1, 100)


def seat():
    letters = 'ABCDEFG'
    s = random.randint(1, 30)
    let = random.randint(1, 6)
    return "'" + letters[let] + str(s) + "'"


def phone():
    ph = "'+1"
    for i in range(9):
        ph += str(random.randint(0, 9))

    return ph + "'"


def generate_tickets():
    counter = 1
    tickets = []
    for game_id in range(1, 85):
        for i in range(1, 31):
            tickets.append([f'{counter}', f'{fan()}', f'{game_id}', f'{seat()}'])
            counter += 1

    with open('../data/tickets.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ticket_id', 'fan_id', 'game_id', 'place'])
        writer.writerows(tickets)

    print("Tickets generated and saved to tickets.csv")


generate_tickets()


def generate_fans():
    fans = []
    for i in range(1, 101):
        fans.append([f'{i}', f'{names[i-1]}', f'{last_names[i-1]}', f'{phone()}'])

    with open('../data/fans.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['fan_id', 'first_name', 'last_name', 'phone'])
        writer.writerows(fans)

    print("Fans generated and saved to fans.csv")


generate_fans()
