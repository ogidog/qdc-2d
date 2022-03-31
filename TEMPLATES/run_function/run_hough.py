import csv

def run_hough(template):

    with open('/tmp/data.txt', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
    print()
