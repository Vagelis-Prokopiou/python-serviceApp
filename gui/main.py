import datetime as datetime
import kivy

kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import csv
import datetime
import random
import re


# Todo: Create a menu (About)


def validate_date(user_date, today):
    """
    Checks diff of provided date in comparison to today.
    """
    year, month, day = user_date.strip().split('-')
    date = datetime.date(int(year), int(month), int(day))
    if (today > date) and ((today - date) > datetime.timedelta(days=547)):
        return -1
    if today < date:
        return 1
    return 0


def regex_validate_date(date):
    """
    Validate that the input provided is a date.
    """
    # m = re.search(
    #     "^(((0?[1-9]|[12]\d|3[01])[\.\-\/](0?[13578]|1[02])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|[12]\d|30)[\.\-\/](0?[13456789]|1[012])[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|((0?[1-9]|1\d|2[0-8])[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?\d{2}))|(29[\.\-\/]0?2[\.\-\/]((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))$",
    #     date)
    m = re.search("^(\d{4})-(\d{2})-(\d{2})$", date)
    return m


def regex_validate_num(num):
    """
    Validates that the argument is a number.
    """
    m = re.search("^\d+?$", num)
    if m is None:
        return False
    return True


def regex_validate_string(s):
    """
    Validates that the argument is a string.
    """
    m = re.search("^[A-Z|a-z|]+?$", s)
    if m is None:
        return False
    return True


def create_date_object(str_date):
    """
    Turns the user date to a date objects.
    """
    try:
        year, month, day = str_date.split('-')
        date = datetime.date(int(year), int(month), int(day))
        return date
    except Exception as e:
        print(e)
        return False


def create_delta_object(date_diff):
    """
    Creates a datetime delta object.
    """
    days = int(date_diff) * 30
    target_date = datetime.timedelta(days=days)
    return target_date


def compare_dates(date_changed, date_current, date_interval):
    """
    Checks the difference between dates.
    """
    date = create_date_object(date_changed)
    interval = create_delta_object(date_interval)
    if (date_current - date) >= interval:
        return True
    return False


def compare_kms(kms_current, kms_changed, kms_interval):
    """
    Checks the difference between kilometers.
    """
    kms_changed = int(kms_changed)
    kms_interval = int(kms_interval)
    if (kms_current - kms_changed) >= kms_interval:
        return True
    return False


def update_entry(choice, user_date, user_kms, spare_parts_list):
    """
    Updates an existing entry.
    """
    for x in range(len(spare_parts_list)):
        if spare_parts_list[x][0] == choice:
            spare_parts_list[x][1] = str(user_date)
            spare_parts_list[x][3] = str(user_kms)
            write_data(spare_parts_list)


def write_data(spare_parts_list):
    """
    Writes to the "data.csv" file.
    """
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(spare_parts_list)


def inspection_msg(messages):
    """
    Prints the messages produced by the inspection.
    """
    if messages:
        for x in range(len(messages)):
            print('\n' + messages[x])
    else:
        # print('\nYou rock! Everything looks good!\nRun me again in a few days, will \'ya? :)')
        self.ids.text_input_results.text = 'You rock! Everything looks good!\nRun me again in a few days, will \'ya? :)'


def error_msg(errors, errors_advanced, tries):
    """
    Prints the various error messages.
    """
    if tries < len(errors):
        return errors[tries]
    return errors_advanced[random.randint(0, (len(errors_advanced) - 1))]


class RootWidget(BoxLayout):
    '''
    The root widget of the application.
    '''

    # This will be true if the user provided a valid kms value.
    # Use it for your first check.
    proceed = False

    # Create the global date variable.
    today = datetime.date.today()

    # Create a list to hold all messages and display them in the end during "Run check".
    messages = []

    # A list with various, custom error messages.
    error_messages = ['Your input is wrong. Please try again.',
                      'Wrong again...',
                      'Wrong again... Really?',
                      'I am losing my patience...',
                      'Wrong again. Are you retarded man?',
                      'This is insane!!!',
                      'Are you kidding me?',
                      ]

    # A list with various, custom, advanced error messages.
    error_messages_advanced = ['Arggggg!!!!!!!!!',
                               'What an @$$!!!',
                               'Are you sure that you are mentally ok man?\nMaybe you should check it out...',
                               'It seems that you should be starring in\n"One Flew Over the Cuckoo\'s Nest".',
                               ]

    # Create the list that will hold the available spare parts.
    spare_parts_list = []

    # This will store the user provided spare part during "Update entry".
    spare_part_update = False

    # This will store the user provided last date of a spare part change, during "Update entry".
    date_changed_update = False

    # This will store the user provided kms of a spare part change during "Update entry".
    kms_changed_update = False

    # This will store the user provided new spare part (spare_part_insert), during "Insert entry".
    spare_part_insert = False

    # This will store the user provided date_interval_insert value, during "Insert entry".
    date_changed_insert = False

    # This will store the user provided kms of a spare part change during "Insert entry".
    kms_changed_insert = False

    # This will store the user provided max number of months for the spare part, during "Insert entry".
    date_interval_insert = False

    # This will store the user provided date_interval_insert value, during "Insert entry".
    kms_interval_insert = False

    # Open the file to read the data into memory.
    with open("data.csv", "r") as f:
        for line in f:
            l = line.strip().split(',')
            # If l in not empty append it to the spare_parts_list.
            if l != ['']:
                print(l)
                spare_parts_list.append(l)

    def kms_provided(self, *args):
        '''
        Checks the value provided for the global_kms
        and creates the variable if all is good.
        '''
        if regex_validate_num(args[0]):
            RootWidget.global_kms = int(args[0])
            # Do not accept a value smaller than 500 kms.
            if RootWidget.global_kms > 500:
                self.ids.text_input_results.text = 'Ok. You can proceed.\n' \
                                                   'The kms you provided equals to {:,} kms.\n' \
                                                   'Press one of the buttons on the right\n' \
                                                   'to run the respective action.'.format(
                    RootWidget.global_kms)
                RootWidget.proceed = True
            else:
                self.ids.text_input_results.text = 'This looks brand new. Are you sure about the value you provided?'
        else:
            # Error message if the value is not a number.
            # Reference the global error_messages.
            # Todo: Make the error message dynamic. Now it is getting a counter from the kv file.
            self.ids.text_input_results.text = 'The value you provided is not valid. Try again.'

    def inform(self):
        """
        Informs the user for the currently available data entries in the "data.csv" file.
        """
        self.ids.text_input_results.text = 'Currently, the available data entries are the following:\n\n'

        for x in range(1, len(RootWidget.spare_parts_list)):
            self.ids.text_input_results.text += '{0}: Last changed on {1}. Must be changed every {2} months, or every {3} kilometers.\n'.format(
                RootWidget.spare_parts_list[x][0], RootWidget.spare_parts_list[x][1], RootWidget.spare_parts_list[x][2],
                RootWidget.spare_parts_list[x][4])

    def check(self):
        '''
        Run this when the check button is pressed.
        '''
        # Clear the messages from previous inspections.
        RootWidget.messages = []
        # If proceed is true, run the check.
        if RootWidget.proceed:
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
                        'Exceeded the allowed {0} months between {1} changes.'.format(
                            date_interval.lower(), spare_part.lower()))

                # Check how many kilometers have past since the last change.
                if compare_kms(RootWidget.global_kms, kms_changed, kms_interval):
                    RootWidget.messages.append(
                        'Exceeded the allowed {0} kms between {1} changes.'.format(
                            kms_interval.lower(), spare_part.lower()))

            # Create an empty message to use in the loop.
            message = ''
            for i in range(len(RootWidget.messages)):
                message += RootWidget.messages[i] + '\n'
            # Print the messages by setting the hint text.
            self.ids.text_input_results.text = message
        # If the global kms variable (proceed) has not been set.
        else:
            # Todo: Make the error message dynamic. Now it is getting a counter from the kv file.
            self.ids.text_input_results.text = 'I cannot proceed. I do not inspect a valid kms value.'

    def insert(self):
        '''
        Creates a new data entry.
        '''
        # Check if the global kms variable (proceed) has been set.
        if RootWidget.proceed:
            # Unset all the variables related to the "Update entry".
            RootWidget.spare_part_update = False
            RootWidget.date_changed_update = False
            RootWidget.kms_changed_update = False
            self.ids.text_input_results.text = ''
            self.ids.text_input_results.hint_text = 'Please provide the name of the spare part, and press "Done".'
        # If the global kms variable (proceed) has not been set.
        else:
            self.ids.text_input_results.text = 'I cannot proceed. I do not inspect a valid kms value.'

    def done(self, *args):
        '''
        Runs when the "Done" button is pressed.
        '''
        # Check if the global kms variable (proceed) has been set.
        if RootWidget.proceed:
            # If all the following are set,
            # spare_part_insert,
            # kms_changed_insert,
            # date_changed_insert,
            # kms_changed_insert,
            # date_interval_insert,
            # kms_interval_insert variables have been set,
            # write the data.
            if RootWidget.spare_part_insert \
                    and RootWidget.date_changed_insert \
                    and RootWidget.date_interval_insert \
                    and RootWidget.kms_changed_insert \
                    and RootWidget.kms_interval_insert:
                row = [RootWidget.spare_part_insert, RootWidget.date_changed_insert, RootWidget.date_interval_insert,
                       RootWidget.kms_changed_insert,
                       RootWidget.kms_interval_insert]
                RootWidget.spare_parts_list.append(row)
                write_data(RootWidget.spare_parts_list)
                self.ids.text_input_results.text = ''
                self.ids.text_input_results.hint_text = 'The new entry has been successfully inserted.'
                # Reset all the variables to start over if the button is pressed again.
                RootWidget.spare_part_insert = False
                RootWidget.date_changed_insert = False
                RootWidget.kms_changed_insert = False
                RootWidget.date_interval_insert = False
                RootWidget.kms_interval_insert = False

            # If the provided value is a number
            # and the spare_part_insert,
            # kms_changed_insert,
            # date_changed_insert,
            # date_interval_insert variables have been set,
            # this sets the kms_changed_insert variable.
            elif regex_validate_num(args[0]) \
                    and RootWidget.spare_part_insert \
                    and RootWidget.date_changed_insert \
                    and RootWidget.date_interval_insert \
                    and RootWidget.kms_changed_insert:
                RootWidget.kms_interval_insert = args[0]
                # Call yourself.
                RootWidget.done(self)

            # If the provided value is a number
            # and the spare_part_insert,
            # kms_changed_insert,
            # date_changed_insert,
            # date_interval_insert variables have been set,
            # this sets the kms_changed_insert variable.
            elif regex_validate_num(args[0]) \
                    and RootWidget.spare_part_insert \
                    and RootWidget.date_changed_insert \
                    and RootWidget.date_interval_insert:
                RootWidget.kms_changed_insert = args[0]
                self.ids.text_input_results.text = ''
                self.ids.text_input_results.hint_text = 'Please provide the max kilometers allowed for the spare part:'

            # If the provided value is a number
            # and the spare_part_insert
            # and kms_changed_insert variables have been set,
            # this sets the date_interval_insert variable.
            elif regex_validate_num(args[0]) \
                    and RootWidget.spare_part_insert \
                    and RootWidget.date_changed_insert:
                RootWidget.date_interval_insert = args[0]
                self.ids.text_input_results.text = ''
                self.ids.text_input_results.hint_text = 'Please, provide the kms of the last change: '

            # If the provided value is a number and nothing else is set
            # we just started the "Update entry" process.
            elif regex_validate_num(args[0]):
                # Check if it is a spare part or the kms of a change based on the value.
                # If it is within the length of the spare part list, it is a spare part.
                if int(args[0]) <= len(RootWidget.spare_parts_list) - 1:
                    RootWidget.spare_part_update = int(args[0])
                    RootWidget.continue_update(self)
                # If it is bigger that 500, it is kms.
                elif int(args[0]) > 500:
                    RootWidget.kms_changed_update = int(args[0])
                    # Check if the provided value is smaller than the global kms variable.
                    if RootWidget.kms_changed_update <= RootWidget.global_kms:
                        # Update the data.
                        update_entry(RootWidget.spare_parts_list[RootWidget.spare_part_update][0],
                                     RootWidget.date_changed_update,
                                     RootWidget.kms_changed_update, RootWidget.spare_parts_list)
                        self.ids.text_input_results.text = ''
                        self.ids.text_input_results.hint_text = 'The data has been successfully updated.' \
                                                                '\nYou can choose another action now.'
                    else:
                        self.ids.text_input_results.text = ''
                        self.ids.text_input_results.hint_text = 'The kilometers you provided are more than the total kilometers of the vehicle.' \
                                                                '\nThis seems wrong. I reckon that you are just stupid and you did not do it on purpose.'
                # If none of the above, the value is wrong.
                else:
                    self.ids.text_input_results.text = ''
                    self.ids.text_input_results.hint_text = 'The value you provided is wrong.' \
                                                            '\nPlease, try again.'

            # If the provided value is a date
            # and the RootWidget.spare_part_insert is set
            # this sets the date_changed_insert variable.
            elif regex_validate_date(args[0]) and RootWidget.spare_part_insert:
                # Create the date object and assign it to the date_changed_update variable.
                RootWidget.date_changed_insert = create_date_object(args[0])
                self.ids.text_input_results.text = ''
                self.ids.text_input_results.hint_text = 'Please, provide the max number of months allowed for the spare part:'

            # If the provided value is a date
            # and the RootWidget.spare_part_update is set
            # this sets the date_changed_update variable.
            elif regex_validate_date(args[0]) and RootWidget.spare_part_update:
                RootWidget.date_changed_update = args[0]
                # Todo: Change the date format to ISO.
                # If the date is in the future.
                if validate_date(RootWidget.date_changed_update, RootWidget.today) == 1:
                    self.ids.text_input_results.text = ''
                    self.ids.text_input_results.hint_text = 'The date you provided lies ahead in the future.' \
                                                            '\nI cannot accept that, unless you are some king of prophet,' \
                                                            '\nor unless you own a time machine.' \
                                                            '\nTry again.'
                # If the date is in the distant past.
                elif validate_date(RootWidget.date_changed_update, RootWidget.today) == -1:
                    self.ids.text_input_results.text = ''
                    self.ids.text_input_results.hint_text = 'The date you provided seems too old.' \
                                                            '\nI just doesn\'t make sense...' \
                                                            '\nTry again.'
                # If the date is right, proceed with the kms.
                else:
                    self.ids.text_input_results.text = ''
                    self.ids.text_input_results.hint_text = 'Please, provide the kilometers of the {0} change:'.format(
                        RootWidget.spare_parts_list[RootWidget.spare_part_update][0].lower())

            # If the value is a string, it is a new spare part.
            elif regex_validate_string(args[0]):
                # Set the new_spare_part variable.
                RootWidget.spare_part_insert = args[0]
                self.ids.text_input_results.text = ''
                self.ids.text_input_results.hint_text = 'Please provide the date of the last change\n' \
                                                        '(in ISO 8601 format [YYYY-MM-DD]. E.g. 2016-05-01):'

            # If the value is neither a number nor a date.
            else:
                self.ids.text_input_results.text = ''
                self.ids.text_input_results.hint_text = 'The value you provided is wrong.' \
                                                        '\nPlease, try again.'
        # If there is no global kms variable set (proceed variable) display error message..
        else:
            self.ids.text_input_results.text = ''
            self.ids.text_input_results.hint_text = 'I cannot proceed. I do not inspect a valid kms value.'

    def continue_update(self):
        if RootWidget.spare_part_update + 1 > len(RootWidget.spare_parts_list) or RootWidget.spare_part_update <= 0:
            # print(error_msg(error_messages, error_messages_advanced, tries))
            self.ids.text_input_results.text = ''
            self.ids.text_input_results.hint_text = 'The value you provided is wrong.' \
                                                    '\nPlease, try again.'
        else:
            # Continue with the function.
            self.ids.text_input_results.text = ''
            self.ids.text_input_results.hint_text = 'Please, provide the date of the {0} change' \
                                                    '\n(in ISO 8601 format [YYYY-MM-DD]. E.g. 2016-05-01): '.format(
                RootWidget.spare_parts_list[RootWidget.spare_part_update][0].lower())

    def update(self):
        if RootWidget.proceed:
            # Reset the variables used in the insert() function.
            RootWidget.spare_part_insert = False
            RootWidget.date_changed_insert = False
            RootWidget.kms_changed_insert = False
            RootWidget.date_interval_insert = False
            RootWidget.kms_interval_insert = False
            message = ''
            # Provide the list with the spare parts.
            for x in range(1, (len(RootWidget.spare_parts_list))):
                # print('For {0}, press {1}.'.format(RootWidget.spare_parts_list[x][0], x))
                message += 'For {0}, press {1}.'.format(RootWidget.spare_parts_list[x][0], x) + '\n'

            message += 'Then, press the "Done" button.'
            # Delete the text and display the message as placeholder text (hint_text).
            # The advantage is that the placeholder text disappears on its own.
            self.ids.text_input_results.text = ''
            self.ids.text_input_results.hint_text = message
        else:
            self.ids.text_input_results.text = ''
            self.ids.text_input_results.hint_text = 'I cannot proceed. I do not inspect a valid kms value.'

    # The pass below belongs to the class definition.
    pass


class ServiceAppApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    ServiceAppApp().run()
