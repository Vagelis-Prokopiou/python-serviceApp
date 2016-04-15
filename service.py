#!/usr/bin/python3.5

# This program is distributed under the GPLv2 license.

# @Author: Vagelis Prokopiou
# @Email: drz4007@gmail.com
# @Date: 2016-04-08 23:07:57

import csv
import datetime
import re


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

def print_messages(messages):
  if len(messages) == 0:
        print('\nYou rock! Everything looks good!\nRun me again in a few days, will \'ya? :)')
  else:
      for x in range(len(messages)):
          print('\n' + messages[x])

def inform(sparePartsList):
  print('Currently, the available data entries are the following:\n')
  for x in range(len(sparePartsList)):
      print('{}: Last changed on {}. It must be changed every {} months, or every {} kilometers.\n'.format(sparePartsList[x][0], sparePartsList[x][1],sparePartsList[x][2],sparePartsList[x][4]))

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

    # Create the global date variable.
    today = datetime.date.today()

    # Create a list to hold all service messages and display them in the end.
    messages = []

    print('\nWhat would you like to do?\n\n'
          'Provide the current mileage of the vehicle, to run an inspection.\n'
          'Press "1" to update an existing data entry.\n'
          'Press "2" to insert a new data entry.\n'
          'Press "3" to see the existing data entries.\n'
          )
    while True:
        user_choice = input('Waiting for your choice: ')
        # Do something with the user_choice
        if validate_kms(user_choice) and (int(user_choice) > 3):
            user_choice = int(user_choice)
            # Start the checking procedure.

            # Iterate the lines.
            for x in range(len(sparePartsList)):
                dateChanged = sparePartsList[x][1]
                dateInterval = sparePartsList[x][2]
                kmsChanghed = sparePartsList[x][3]
                kmsInterval = sparePartsList[x][4]

                # Check the time that has past.
                if compare_dates(dateChanged, today, dateInterval):
                    messages.append(
                        'You have exceeded the allowed {0} months between {1} changes. You must change the {1} again now!'.format(
                            (sparePartsList[x][2].lower()), sparePartsList[x][0].lower()))

                # Check how many kilometers have past since the last change.
                if compare_mileage(user_choice, kmsChanghed, kmsInterval):
                    messages.append(
                        'You have exceeded the allowed {0} kms between {1} changes. You must change the {1} again now!'.format(
                            (sparePartsList[x][4]).lower(), sparePartsList[x][0].lower()))
            print_messages(messages)

            break

        elif validate_kms(user_choice) and int(user_choice) == 1:
            while True:
                print('\n')
                for x in range(len(sparePartsList)):
                    print('For {}, press {}.'.format(sparePartsList[x][0], x+1))
                data_update = input('\nChoose the spare part: ')

                if ((int(data_update)-1) > len(sparePartsList)) or (int(data_update) <= 0):
                    print('\nYour choice seems wrong. Please, try again.\n\n')
                else:
                    break
            while True:
                user_date = input('Please, provide the date of the ' + sparePartsList[
                    (int(data_update)-1)][0].lower() + ' change (e.g. 31/12/2015): ')
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
              current_kms = input('\nPlease, provide the current kilometers of the vehicle: ')
              if validate_kms(current_kms):
                  current_kms = int(current_kms)
                  break

            while True:
              user_kms = input('\nPlease, provide the kilometers of the ' + sparePartsList[
                  (int(data_update)-1)][0].lower() + ' change: ')
              if validate_kms(user_kms):
                  user_kms = int(user_kms)
                  if user_kms <= current_kms:
                      break
                  else:
                      print(
                          '\nThe kilometers you provided are more than the total kilometers of the vehicle. Something is terribly wrong...\n')

            # If all the above, update the data.
            update(sparePartsList[int(data_update)-1][0], user_date, user_kms)
            inform(sparePartsList)
            break
        elif validate_kms(user_choice) and int(user_choice) == 2:
            print('user_choice == int(2)')
            # Do stuff and then
            break
        elif validate_kms(user_choice) and int(user_choice) == 3:
          inform(sparePartsList)
          break
        else:
            print('\nYour choice is wrong. Try again.\n')




if __name__ == '__main__':
    main()
