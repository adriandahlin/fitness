import csv

csv_file_path = "workouts_manually_entered.csv"

rows = []

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["date", "run", "bike", "sports", "yoga", "abs", "lift"])
    writer.writeheader()
    writer.writerow({"date": "07/26/17", "run": "0", "bike": "0", "sports": ".5", "yoga": "0", "abs": "0", "lift": ".1"})

with open(csv_file_path, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        rows.append(row)

menu = "Please enter one of the following operation: 'new workout' OR 'show all' "
operations = ["new workout", "show all"]

def command_center():
    inp = input(menu)
    if inp == "new workout":
        new_workout()
    if inp == "show all":
        show_all()
    if inp not in operations:
        print("I'm sorry, I don't recognize that operation. I'll try to figure it out soon!")

def new_workout():
    print("Enter your workout details here:")
    date = input("Date (mm/dd/yy): ")
    run = input("Run (miles): ")
    bike = input("Bike (miles): ")
    sports = input("Sports (hours): ")
    yoga = input("Yoga (hours): ")
    abdoms = input("Abs (minutes): ")
    lift = input("Lift (0 to 1): ")
    new_workout = {
        "date": date,
        "run": run,
        "bike": bike,
        "sports": sports,
        "yoga": yoga,
        "abs": abdoms,
        "lift": lift
    }
    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["date", "run", "bike", "sports", "yoga", "abs", "lift"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        writer.writerow(new_workout)
    print("Here's your new entry:")
    print(new_workout["date"], new_workout["run"], new_workout["bike"], new_workout["sports"], new_workout["yoga"], new_workout["abs"], new_workout["lift"])

def show_all():
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            print(row["date"], row["run"], row["bike"], row["sports"], row["yoga"], row["abs"], row["lift"])

command_center()
