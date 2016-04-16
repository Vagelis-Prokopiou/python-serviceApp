#!/usr/bin/python3.5

# This program is distributed under the GPLv2 license.

# @Author: Vagelis Prokopiou
# @Email: drz4007@gmail.com
# @Date: 2016-04-08 23:07:57

import csv
import datetime
import random
import re


# Checks the diff in comparison with today.
def validate_date(user_date, today):
    day, month, year = user_date.strip().split('/')
    date = datetime.date(int(year), int(month), int(day))
    if (today > date) and ((today - date) > datetime.timedelta(days=547)):
        return -1
    if today < date:
        return 1
    return 0


# Validates the kms provided by the user.
def validate_kms(kms):
    m = re.search("^\d+?$", kms)
    if m is None:
        return False
    return True


# Turns the user dates to date objects.
def create_date_object(str_date):
    day, month, year = str_date.split('/')
    date = datetime.date(int(year), int(month), int(day))
    return date


# Creates a datetime delta object.
def create_delta_object(date_diff):
    days = int(date_diff) * 30
    target_date = datetime.timedelta(days=days)
    return target_date


# Checks the difference between dates.
def compare_dates(date_changed, date_current, date_interval):
    date = create_date_object(date_changed)
    interval = create_delta_object(date_interval)
    if (date_current - date) >= interval:
        return True
    return False


# Checks the difference between kilometers.
def compare_kms(kms_current, kms_changed, kms_interval):
    kms_changed = int(kms_changed)
    kms_interval = int(kms_interval)
    if (kms_current - kms_changed) >= kms_interval:
        return True
    return False


# Updates the "data.csv" file.
def update_data_file(choice, user_date, user_kms, spare_parts_list):
    for x in range(len(spare_parts_list)):
        if spare_parts_list[x][0] == choice:
            spare_parts_list[x][1] = str(user_date)
            spare_parts_list[x][3] = str(user_kms)
            with open('data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerows(spare_parts_list)
    print('\nThe data was updated successfully. Thank you.\n')


# Prints the messages produced by the inspection.
def inspection_msg(messages):
    if len(messages) == 0:
        print('\nYou rock! Everything looks good!\nRun me again in a few days, will \'ya? :)')
    else:
        for x in range(len(messages)):
            print('\n' + messages[x])


# Prints the various error messages.
def error_msg(errors, errors_advanced, tries):
    if tries < len(errors):
        return errors[tries]
    return errors_advanced[random.randint(0, (len(errors_advanced) - 1))]


# Informs the user for the currently available data entries in the "data.csv" file.
def inform(spare_parts_list):
    print('\nCurrently, the available data entries are the following:\n')
    for x in range(1, len(spare_parts_list)):
        print('{}: Last changed on {}. It must be changed every {} months, or every {} kilometers.\n'.format(
            spare_parts_list[x][0], spare_parts_list[x][1], spare_parts_list[x][2], spare_parts_list[x][4]))


def main():
    # A list with various, custom error messages.
    error_messages = ['Your input is wrong. Please try again.',
                      'Wrong again...',
                      'Wrong again... Really?',
                      'I am losing my patience...',
                      'Wrong again. Are you retarded man?',
                      'This is insane!!!',
                      'Are you kidding me?',
                      ]

    error_messages_advanced = ['Arggggg!!!!!!!!!',
                               'What an @$$!!!',
                               'Are you sure that you are mentally ok man?\nMaybe you should check it out...',
                               'It seems that you should be starring in\n"One Flew Over the Cuckoo\'s Nest".',
                               ]

    # Autobuild the sparepart list.
    spare_parts_list = []

    # Open the file to check the data.
    file = open('data.csv', 'r')

    # Iterate the lines.
    for line in file:
        l = line.strip().split(',')
        spare_parts_list.append(l)
    file.close()

    # Create the global date variable.
    today = datetime.date.today()

    # Create a list to hold all service messages and display them in the end.
    messages = []

    print('\nWhat would you like to do?\n\n'
          'Provide the current mileage of the vehicle, to run an inspection.\n'
          'Press "1" to update_data_file an existing data entry.\n'
          'Press "2" to insert a new data entry.\n'
          'Press "3" to see the existing data entries.\n'
          )
    tries = 0
    while True:
        user_choice = input('\nWaiting for your choice: ')
        # Do something with the user_choice
        if validate_kms(user_choice) and (int(user_choice) > 3):
            user_choice = int(user_choice)
            # Start the checking procedure.

            # Iterate the lines.
            for x in range(1, len(spare_parts_list)):
                date_changed = spare_parts_list[x][1]
                date_interval = spare_parts_list[x][2]
                kms_changhed = spare_parts_list[x][3]
                kms_interval = spare_parts_list[x][4]

                # Check the time that has past since the last change.
                if compare_dates(date_changed, today, date_interval):
                    messages.append(
                        'You have exceeded the allowed {0} months between {1} changes. '
                        'You must change the {1} again now!'.format(
                            (spare_parts_list[x][2].lower()), spare_parts_list[x][0].lower()))

                # Check how many kilometers have past since the last change.
                if compare_kms(user_choice, kms_changhed, kms_interval):
                    messages.append(
                        'You have exceeded the allowed {0} kms between {1} changes. '
                        'You must change the {1} again now!'.format(
                            (spare_parts_list[x][4]).lower(), spare_parts_list[x][0].lower()))
            inspection_msg(messages)
            break
        elif validate_kms(user_choice) and int(user_choice) == 1:
            tries = 0
            while True:
                print('\n')
                for x in range(1, (len(spare_parts_list))):
                    print('For {}, press {}.'.format(spare_parts_list[x][0], x))
                data_update = input('\nChoose the spare part: ')

                if ((int(data_update)) > len(spare_parts_list)) or (int(data_update) <= 0):
                    print('\n')
                    print(error_msg(error_messages, error_messages_advanced, tries))
                    tries += 1
                else:
                    break
            while True:
                user_date = input('Please, provide the date of the ' + spare_parts_list[
                    (int(data_update))][0].lower() + ' change (e.g. 31/12/2015): ')
                m = re.search(
                    "^(((0?[1-9]|[12]\d|3[01])[\.\-\/](0?[13578]|1[02])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|[12]\d|30)[\.\-\/](0?[13456789]|1[012])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|1\d|2[0-8])[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|(29[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))$",
                    user_date)
                if m is None:
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
                print('\nYour choice seems wrong. Please, try again.')

            while True:
                user_kms = input('\nPlease, provide the kilometers of the ' + spare_parts_list[
                    (int(data_update))][0].lower() + ' change: ')
                if validate_kms(user_kms):
                    user_kms = int(user_kms)
                    if user_kms <= current_kms:
                        break
                    else:
                        print(
                            '\nThe kilometers you provided are more than the total kilometers of the vehicle. Something is terribly wrong...\n')

            # If all the above, update_data_file the data.
            update_data_file(spare_parts_list[int(data_update)][0], user_date, user_kms, spare_parts_list)
            # inform(spare_parts_list)
            break
        elif validate_kms(user_choice) and int(user_choice) == 2:
            print('user_choice == int(2)')
            # Do stuff and then
            break
        elif validate_kms(user_choice) and int(user_choice) == 3:
            inform(spare_parts_list)
            break
        else:
            print('\n')
            print(error_msg(error_messages, error_messages_advanced, tries))
            tries += 1


if __name__ == '__main__':
    main()
