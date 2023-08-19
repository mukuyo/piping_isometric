import csv

name = ['bent']
position = [0, 0]
pose = [0, 0, 0]

list = [name, position, pose]
print(list)
with open("data/csv/test.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(list)