import csv

with open("zoom-present.csv") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    data_read = [row for row in reader]

    email_index = data_read[0].index('Email')
    emails = []

    for i in range(1, len(data_read)):
        emails.append(data_read[i][email_index])

    with open('input.txt', 'a') as f:
        for email in emails:
            f.write("\n{}".format(email))