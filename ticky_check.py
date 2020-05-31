import csv
import operator
import os
import re
import sys

# global variables
err_list = []
err_dict = {}
filename = "syslog.log"

# iterates over the error list and increases for each time it appears
# returns sorted dictionary
def errdict(err_list, err_dict):
    err_dict.update([
        ("Timeout while retrieving information", 0),
        ("The ticket was modified while updating", 0),
        ("Connection to DB failed", 0),
        ("Tried to add information to closed ticket", 0),
        ("Permission denied while closing ticket", 0),
        ("Ticket doesn't exist", 0)
    ])
    for line in err_list:
        for k in err_dict.keys():
            if k in line:
                err_dict[k] += 1
    return sorted(err_dict.items(), key=operator.itemgetter(1), reverse=True)

def printer(errdict):
    prepareme = errdict(err_list, err_dict)
    header = ["Error", "Count"]
    try:
        with open("error_message.csv", "r+", newline='') as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(prepareme)
            
    except:
        print("creating error_message.csv")
        with open("error_message.csv", "w", newline='') as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(prepareme)

with open(filename, "r+", encoding="utf-8") as ef:
    x = ef.readlines()
    tmplist = [line for line in x]
    ef.close()

err_list += [line for line in tmplist if "ERROR" in line]

printer(errdict)

# global variables
user_list = []
user_dict = {}
filename = "syslog.log"

# Writes to CSV
def printer(user_dict):
    header = ["Username", "INFO", "ERROR"]
    with open("user_statistics.csv", "w", newline='') as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writerows(user_dict)
    f.close()

# Reads file and creates a temporary list of all items
with open(filename, "r+", encoding="utf-8") as ef:
    x = ef.readlines()
    tmplist = [line for line in x]
    ef.close()

for line in tmplist:
    usernames = re.findall(r"(?<=\().*(?=\))", line)
    for username in usernames:
        err = 0
        inf = 0
        for line in tmplist:
            if "ERROR" in line and "("+username+")" in line:
                err += 1   
            elif "INFO" in line and "("+username+")" in line:
                inf += 1
        user_dict.setdefault(username,[inf, err])

f = open("user_statistics.csv", "w")
f.write("%s, %s, %s\n" % ("Username", "INFO", "ERROR"))
for key in sorted(user_dict.keys()):
    f.write("%s, %s, %s\n" % (key, user_dict[key][0], user_dict[key][1]))
f.close()