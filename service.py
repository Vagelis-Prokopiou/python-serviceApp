#!/usr/bin/python3.5

# This program is distributed under the GPLv2 license.

# @Author: Vagelis Prokopiou
# @Email: drz4007@gmail.com
# @Date: 2016-04-08 23:07:57

import datetime
import re
import csv


# import random


def validate_date(user_date, today):
    day, month, year = user_date.strip().split('/')
    date = datetime.date(int(year), int(month), int(day))
    if (today > date) and ((today - date) > datetime.timedelta(days=547)):
        return -1
    if (today < date):
        return 1
    return 0


# This function validates the kms provided by the user.
def validate_kms(kms):
    m = re.search("^\d+?$", kms)
    if m == None:
        return False
    return True


# This function turns the user dates to date objects.
def createDateObject(str_date):
    day, month, year = str_date.split('/')
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


# This function updates the "data.csv" file.
def update(choice, user_date, user_kms):
    r = csv.reader(open('data.csv'))

    # Iterate the lines.
    lines = [l for l in r]
    for x in range(len(lines)):
        if lines[x][0] == choice:
            lines[x][1] = str(user_date)
            lines[x][3] = str(user_kms)
            with open('data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerows(lines)


def main():
    # Autobuild the sparepart list.
    # Create the list to hold the values.
    sparePartsList = []

    # Open the file to check the data.
    file = open('data.csv', 'r')

    # Iterate the lines.
    for line in file:
        l = line.strip().split(',')
        if l[0] != 'element'.lower():
            sparePartsList.append(l)

    file.close()
    print(sparePartsList[0][0])


    # Create the global date variable.
    today = datetime.date.today()

    # Create a list to hold all service messages and display them in the end.
    messages = []

    # The dictionary with all the spare parts.
    sparePartsDict = {'1': 'Spark',
                      '2': 'Oil',
                      '3': 'Oil filter',
                      '4': 'Air filter'}

    # Start interacting with the user. Ask what he wants.
    while True:
        print('What would you like to do?\n'
            'Press "Enter" to run an inspection.\n'
            'Press "1" to update an existing data entry.\n'
            'Press "2" to insert a new data entry.\n'
            'Press "3" to see the existing data entries.\n'
            )
        userChoise = input('Waiting for your choice: ')

        # Do something with the userChoise
        if userChoise == '':
            print('Run inspection.')
            # sparePartsList[0][0]
            # Start the checking procedure.


            # Iterate the lines.
            for x in range(len(sparePartsList)):
                print(sparePartsList[x])


                # dateChanged = l[1]
                # dateInterval = l[2]

                # Check the time that has past.
                if compare_dates(dateChanged, today, dateInterval):
                    messages.append(
                        'You have exceeded the allowed {0} months between {1} changes. You must change the {1} again now!'.format(
                            (l[2].lower()), l[0].lower()))

                # Check how many kilometers have past since the last change.
                if compare_mileage(current_kms, l[3], l[4]):
                    messages.append(
                        'You have exceeded the allowed {0} kms between {1} changes. You must change the {1} again now!'.format(
                            (l[4]).lower(), l[0].lower()))

            file.close()
            break
        elif userChoise == int(1):
            print('Update an existing data entry.')
            break
        elif userChoise == int(2):
            print('Insert a new data entry.')
            break
        elif userChoise == int(3):
            print('See the existing data entries.')
            break
        else:
            print('\nYour choice is wrong. Try again.\n')




    # Create the global mileage of the vehicle variable.
    while True:
        current_kms = input('Please, provide the current kilometers/miles of the vehicle: ')
        if validate_kms(current_kms):
            current_kms = int(current_kms)
            break
        else:
            print('The value you provide is not right. Please, try again.\n')

    # Check if the user wants to update anything.
    while True:
        data_update = input('\nIf you have made any servicing to your vehicle\n'
                            'and you want to update the data, choose the right spare part\n'
                            'according to the following table, otherwise, just press "Enter".\n\n'
                            'For "Spark" press 1.\n'
                            'For "Oil" press 2.\n'
                            'For "Oil filter" press 3.\n'
                            'For "Air filter" press 4.\n'
                            'Enter your choice": ', )
        if data_update == '':
            break
        elif (int(data_update) > len(sparePartsDict)) or (int(data_update) <= 0):
            print('\nYour choice seems wrong. Please, try again.\n\n')
        else:
            break

    if data_update != '':
        while True:
            user_date = input('Please, provide the date of the ' + sparePartsDict[
                data_update].lower() + ' change (e.g. 31/12/2015): ')
            m = re.search(
                "^(((0?[1-9]|[12]\d|3[01])[\.\-\/](0?[13578]|1[02])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|[12]\d|30)[\.\-\/](0?[13456789]|1[012])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|1\d|2[0-8])[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|(29[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))$",
                user_date)
            if m == None:
                print('\nThe date you provided is not valid. Please try again.\n')
            else:
                # Check if the date provided is within a logical time span from today.
                if validate_date(user_date, today) == 1:
                    print(
                        '\nThe date you provided lies ahead in the future.'
                        '\nI cannot accept that, unless you are some king of prophet, or unless you own a time machine.\n')
                elif validate_date(user_date, today) == -1:
                    print('\nThe date you provided seems too old. I just doesn\'t make sense...\n')
                else:
                    break

        while True:
            user_kms = input('\nPlease, provide the kilometers of the ' + sparePartsDict[
                data_update].lower() + ' change: ')
            if validate_kms(user_kms):
                user_kms = int(user_kms)
                if user_kms <= current_kms:
                    break
                else:
                    print(
                        '\nThe kilometers you provided are more than the total kilometers of the vehicle. Something is terribly wrong...\n')

        # If all the above, update the data.
        update(sparePartsDict[data_update], user_date, user_kms)
        # End of function.




    if len(messages) == 0:
        print('\nYou rock! Everything looks good!\nRun me again in a few days, will \'ya? :)')
    else:
        for x in range(len(messages)):
            print('\n' + messages[x])


if __name__ == '__main__':
    main()
