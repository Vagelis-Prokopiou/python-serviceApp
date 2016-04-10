#!/usr/bin/python3

# This program is distributed under the GPLv2 licence.

# @Author: Vagelis Prokopiou
# @Email: drz4007@gmail.com
# @Date: 2016-04-08 23:07:57

import time


# This function checks the difference between dates.
def compare_dates(dateChanged, dateCurrent, dateInterval):
    dateInterval = int(dateInterval) * (31 * 24 * 60 * 60)
    dateTuple = (int(dateChanged[2]), int(dateChanged[1]), int(dateChanged[0]), 0, 0, 0, 0, 0, 0)
    dateChanged = time.mktime(dateTuple)
    if (dateCurrent - dateChanged) >= dateInterval:
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
    file = open('data.csv', 'r')
    # header = file.readline().strip().split(',')
    # Iterate the lines.
    for line in file:
        l = line.strip().split(',')
        if l[0] == sparePartsDict[choice]:
            print(l[0], sparePartsDict[choice])
            print(str(user_date), str(user_kms))


def main():
    while True:
        data_update = input('If you have made any servicing to your vehicle\n'
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
            user_date = input('Please, provide the date of the change (in the form of day/month/year): ')
            user_kms = input('Please, provide the kilometres of the change: ')
            update(str(data_update), user_date, int(user_kms))
            break

    # Create the global mileage of the vehicle variable.
    mileageCurrent = input('Please, provide the current mileage of the vehicle: ')
    mileageCurrent = int(str(mileageCurrent).replace('.', ''))

    # Create the global date variable.
    dateCurrent = time.time()

    # Open the file to check the data.
    file = open('data.csv', 'r')
    header = file.readline().strip().split(',')

    # Iterate the lines.
    for line in file:
        l = line.strip().split(',')
        day, month, year = l[1].split('/')
        dateElements = [day, month, year]

        # Check the time that has past.
        if compare_dates(dateElements, dateCurrent, l[2]):
            print(
                'More than {0} months have past since you changed your {1}. You must change the {1} again now!'.format(
                    (l[2].lower()), l[0].lower()))

        # Check how many kilometers have past since the last change.
        if compare_mileage(mileageCurrent, l[3], l[4]):
            print(
                'You have exceeded the allowed {0} kms between {1} changes. You must change the {1} again now!'.format(
                    (l[4]).lower(), l[0].lower()))

    file.close()
    print('If no messages appeared, you rock!')
    print('Otherwise, you better do some servicing man...')


if __name__ == '__main__':
    main()
