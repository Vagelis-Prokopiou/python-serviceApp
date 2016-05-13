import datetime as datetime
import kivy

kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import csv
import datetime
import random
import re


def validate_date(user_date, today):
    """ Checks diff of provided date in comparison to today. """
    day, month, year = user_date.strip().split('/')
    date = datetime.date(int(year), int(month), int(day))
    if (today > date) and ((today - date) > datetime.timedelta(days=547)):
        return -1
    if today < date:
        return 1
    return 0


def regex_validate_date(date):
    """ Validate that the input provided is a date. """
    m = re.search(
        "^(((0?[1-9]|[12]\d|3[01])[\.\-\/](0?[13578]|1[02])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|[12]\d|30)[\.\-\/](0?[13456789]|1[012])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|1\d|2[0-8])[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|(29[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))$",
        date)
    return m


def regex_validate_num(num):
    """ Validates that the argument is a number. """
    m = re.search("^\d+?$", num)
    if m is None:
        return False
    return True


def regex_validate_string(s):
    """ Validates that the argument is a string. """
    m = re.search("^[A-Z|a-z]+?$", s)
    if m is None:
        return False
    return True


def create_date_object(str_date):
    """  Turns the user dates to date objects. """
    try:
        day, month, year = str_date.split('/')
        date = datetime.date(int(year), int(month), int(day))
        return date
    except Exception as e:
        print(e)
        return False


def create_delta_object(date_diff):
    """ Creates a datetime delta object. """
    days = int(date_diff) * 30
    target_date = datetime.timedelta(days=days)
    return target_date


def compare_dates(date_changed, date_current, date_interval):
    """ Checks the difference between dates. """
    date = create_date_object(date_changed)
    interval = create_delta_object(date_interval)
    if (date_current - date) >= interval:
        return True
    return False


def compare_kms(kms_current, kms_changed, kms_interval):
    """ Checks the difference between kilometers. """
    kms_changed = int(kms_changed)
    kms_interval = int(kms_interval)
    if (kms_current - kms_changed) >= kms_interval:
        return True
    return False


def update_entry(choice, user_date, user_kms, spare_parts_list):
    """ Updates an existing entry. """
    for x in range(len(spare_parts_list)):
        if spare_parts_list[x][0] == choice:
            spare_parts_list[x][1] = str(user_date)
            spare_parts_list[x][3] = str(user_kms)
            write_data(spare_parts_list)


def write_data(spare_parts_list):
    """ Writes to the "data.csv" file. """
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(spare_parts_list)
    print('\nThe data was updated successfully. Thank you.\n')


def inspection_msg(messages):
    """ Prints the messages produced by the inspection. """
    if messages:
        for x in range(len(messages)):
            print('\n' + messages[x])
    else:
        print('\nYou rock! Everything looks good!\nRun me again in a few days, will \'ya? :)')


def error_msg(errors, errors_advanced, tries):
    """ Prints the various error messages. """
    if tries < len(errors):
        return errors[tries]
    return errors_advanced[random.randint(0, (len(errors_advanced) - 1))]


def inform(spare_parts_list):
    """ Informs the user for the currently available data entries in the "data.csv" file. """
    print('\nCurrently, the available data entries are the following:\n')
    for x in range(1, len(spare_parts_list)):
        print('{0}: Last changed on {1}. Must be changed every {2} months, or every {3} kilometers.\n'.format(
            spare_parts_list[x][0], spare_parts_list[x][1], spare_parts_list[x][2], spare_parts_list[x][4]))


class RootWidget(BoxLayout):
    ''' The root widget of the application. '''
    # Use proceed to run your checks.
    proceed = False

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

    # Autobuild the spare part list.
    spare_parts_list = []

    # Open the file to check the data.
    with open("data.csv", "r") as f:
        # Iterate the lines.
        for line in f:
            l = line.strip().split(',')
            spare_parts_list.append(l)

    # Create the global date variable.
    today = datetime.date.today()

    # Create a list to hold all service messages and display them in the end.
    messages = []

    def kms_provided(self, *args):
        # Check if the provided value is all numbers.
        if regex_validate_num(args[0]):
            # Set the global kms variable.
            RootWidget.global_kms = int(args[0])
            if RootWidget.global_kms > 500:
                self.ids.results_label.text = 'Ok. You can proceed.\nThe kms you provided equals to {:,} kms.'.format(RootWidget.global_kms)
                RootWidget.proceed = True
            else:
                self.ids.results_label.text = 'This looks brand new. Are you sure about the value you provided?'
        else:
            # Reference the global error_messages.
            # Todo: Make the error message dynamic. Now it is getting a counter from the kv file.
            self.ids.results_label.text = 'The value you provided is not valid. Try again.'

    def check(self):
        ''' Run this when the check button is pressed. '''
        # If proceed is true, run the check.
        if RootWidget.proceed:
            if RootWidget.global_kms > 500:
                # Iterate the lines.
                for x in range(1, len(RootWidget.spare_parts_list)):
                    spare_part = RootWidget.spare_parts_list[x][0]
                    date_changed = RootWidget.spare_parts_list[x][1]
                    date_interval = RootWidget.spare_parts_list[x][2]
                    kms_changed = RootWidget.spare_parts_list[x][3]
                    kms_interval = RootWidget.spare_parts_list[x][4]

                    # Check the time that has past since the last change.
                    if compare_dates(date_changed, RootWidget.today, date_interval):
                        RootWidget.messages.append(
                            'You have exceeded the allowed {0} months between {1} changes. ' 'You must change the {1} again now!'.format(
                                date_interval.lower(), spare_part.lower()))

                    # Check how many kilometers have past since the last change.
                    if compare_kms(RootWidget.global_kms, kms_changed, kms_interval):
                        RootWidget.messages.append(
                            'You have exceeded the allowed {0} kms between {1} changes. ''You must change the {1} again now!'.format(
                                kms_interval.lower(), spare_part.lower()))
                inspection_msg(RootWidget.messages)
            else:
                # Todo: Make the error message dynamic. Now it is getting a counter from the kv file.
                self.ids.results_label.text = 'Are you sure that these are the total kms of the vehicle?'
        else:
            # Todo: Make the error message dynamic. Now it is getting a counter from the kv file.
            self.ids.results_label.text = 'I cannot proceed. I do not inspect a valid kms value.'

    pass


class ServiceApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    ServiceApp().run()
