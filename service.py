#!/usr/bin/python3.5

# This program is distributed under the GPLv2 licence.

# @Author: Vagelis Prokopiou
# @Email: drz4007@gmail.com
# @Date: 2016-04-08 23:07:57

import time
import datetime
import re


# This function turns the user dates to date objects.


def createDateObject(str_date):
    day, month, year = str_date.split('/')
    print(day, month, year)
    date = datetime.date(int(year), int(month), int(day))
    return date


def createDeltaObject(date_diff):
    days = int(date_diff) * 30
    target_date = datetime.timedelta(days=days)
    return target_date


# This function checks the difference between dates.
def compare_dates(dateChanged, dateCurrent, dateInterval):
    date = createDateObject(dateChanged)
    interval = createDeltaObject(dateInterval)
    if (dateCurrent - date) >= interval:
        return True
    return False


# This functions checks the difference between dates.
def compare_mileage(mileageCurrent, kmsChanghed, kmsInterval):
    kmsChanghed = int(kmsChanghed)
    kmsInterval = int(kmsInterval)
    if (mileageCurrent - kmsChanghed) >= kmsInterval:
        return True
    return False


def update(choice, user_date, user_kms):
    sparePartsDict = {'1': 'Spark',
                      '2': 'Oil',
                      '3': 'Oil filter',
                      '4': 'Air filter'}
    file = open('data.csv', 'r+')

    # Iterate the lines.
    lines = [l for l in file]
    for x in range(len(lines)):
        print(lines[x])
        l = lines[x].strip().split(',')
        if l[0] == sparePartsDict[choice]:
            l[0] += l[0]
            print(l[0])
            # print(l[0], sparePartsDict[choice])
            # print(str(user_date), str(user_kms))
    # See the csv module. https://docs.python.org/3/library/csv.html


    file.writerows(lines)
    #     See http://stackoverflow.com/questions/11033590/change-specific-value-in-csv-file-via-python

    file.close()


def main():
    # Create a list to hold all service messages and display them in the end.
    messages = []

    while True:
        # Create the global mileage of the vehicle variable.
        current_kms = input('Please, provide the current mileage of the vehicle: ')
        m = re.search("^\d+?$", current_kms)
        if m == None:
            print('What you typed doesn\'t seem valid. Please, try again.')
        if m:
            current_kms = int(current_kms)
            break

    # Create the global date variable.
    today = datetime.date.today()

    while True:
        data_update = input('\nIf you have made any servicing to your vehicle\n'
                            'and you want to update the data, choose the right spare part\n'
                            'according to the following table, otherwise, just press "Enter".\n'
                            'For the "Spark" press 1.\n'
                            'For the "Oil" press 2.\n'
                            'For the "Oil filter" press 3.\n'
                            'For the "Air filter" press 4.\n'
                            'Enter your choice": ', )
        if data_update == '':
            break
        elif int(data_update) > 4 or (int(data_update) <= 0):
            print('\nYour choice seems wrong. Please, try again.\n\n')
        else:
            while True:
                user_date = input('Please, provide the date of the change (in the form of day/month/year): ')
                m = re.search(
                    "^(((0?[1-9]|[12]\d|3[01])[\.\-\/](0?[13578]|1[02])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|[12]\d|30)[\.\-\/](0?[13456789]|1[012])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|1\d|2[0-8])[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|(29[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))$",
                    user_date)
                if m == None:
                    print('The date you provided is not valid. Please try again.')
                else:
                    while True:
                        user_kms = input('Please, provide the kilometres of the change: ')
                        if user_kms <= current_kms:
                            break
                            # update(str(data_update), user_date, int(user_kms))
                break

    # Open the file to check the data.
    file = open('data.csv', 'r')
    header = file.readline().strip().split(',')

    # Iterate the lines.
    for line in file:
        l = line.strip().split(',')
        # day, month, year = l[1].split('/')
        dateChanged = l[1]
        dateInterval = l[2]

        # Check the time that has past.
        if compare_dates(dateChanged, today, dateInterval):
            print(
                'More than {0} months have past since you changed your {1}. You must change the {1} again now!'.format(
                    (l[2].lower()), l[0].lower()))
            messages.append(
                'More than {0} months have past since you changed your {1}. You must change the {1} again now!'.format(
                    (l[2].lower()), l[0].lower()))

        # Check how many kilometers have past since the last change.
        if compare_mileage(current_kms, l[3], l[4]):
            print(
                'You have exceeded the allowed {0} kms between {1} changes. You must change the {1} again now!'.format(
                    (l[4]).lower(), l[0].lower()))
            messages.append('You have exceeded the allowed {0} kms between {1} changes. You must change the {1} again now!'.format(
                    (l[4]).lower(), l[0].lower()))

    file.close()

    if len(messages) == 0:
        print('You rock! Everything looks good!')
    else:
        for x in range(len(messages)):
            print(messages[x])


if __name__ == '__main__':
    main()
