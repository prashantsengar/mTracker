import csv

def write_data(name, email, url):
    with open('data.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, email, url])
