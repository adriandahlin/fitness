import csv

csv_file_path = "workouts.csv"

rows = []

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["date", "run", "bike", "sports", "yoga", "abs"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

menu = "Choose one of the following operations: list, show month, show today"

def command_center():
