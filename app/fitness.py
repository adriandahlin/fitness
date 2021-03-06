import csv
from IPython import embed

csv_file_path = "data/workouts_manually_entered.csv"

rows = []

with open(csv_file_path, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        rows.append(row)

menu = '''Please choose the letter corresponding to the operation you would like to complete:
l - log
a - list all
x - exit
'''

operations = ["c", "l", "a", "m", "t", "x"]

def command_center():
    x = 0
    while x == 0:
        inp = input(menu)
        if inp == "c":
            create_db()
        if inp == "a":
            list_all_workouts()
        if inp == "m":
            show_month()
        if inp == "t":
            show_today()
        if inp == "l":
            log_workout()
        if inp not in operations:
            print("I'm sorry, we're not sure what to do with that operation. Please enter listall, showmonth, or showtoday.")
        if inp == "x":
            x = 1

def list_all_workouts():
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        print("This full list of workouts can also be found at data/workouts_manually_entered.csv.")
        print(reader.fieldnames)
        for row in reader:
            print(row["date"], row["run"], row["bike"], row["sports"], row["yoga"], row["abs"], row["lift"])

def log_workout():
    log_date = input("Enter the date (mm/dd/yy): ")
    log_run = input("Enter miles run: ")
    log_bike = input("Enter miles cycled: ")
    log_sports = input("Enter hours of sports played: ")
    log_yoga = input("Enter hours of yoga completed: ")
    log_abs = input("Enter minutes of abs completed: ")
    log_lift = input("Enter workout (0, 1, or fraction): ")
    new_workout = {
        "date": log_date,
        "run": log_run,
        "bike": log_bike,
        "sports": log_sports,
        "yoga": log_yoga,
        "abs": log_abs,
        "lift": log_lift,
    }
    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["date", "run", "bike", "sports", "yoga", "abs", "lift"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        writer.writerow(new_workout)
    print("--------")
    print("Here's the workout you've just added. You can find the csv at data/workouts_manually_entered.csv.")
    print(new_workout["date"], new_workout["run"], new_workout["bike"], new_workout["sports"], new_workout["yoga"], new_workout["abs"], new_workout["lift"])

def show_month():
    print("I'm sorry, I haven't figured out how to do this yet. Stay tuned.")

def show_today():
    print("I'm sorry, I haven't figured out how to do this yet. Stay tuned.")

command_center()
