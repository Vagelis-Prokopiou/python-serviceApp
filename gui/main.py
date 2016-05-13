import kivy

kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import re


def regex_validate_num(num):
    """ Validates that the argument is a number. """
    m = re.search("^\d+?$", num)
    if m is None:
        print('False')
        return False
    print('True')
    return True


class RootWidget(BoxLayout):
    ''' The root widget of the application. '''

    global_kms = 0

    def alert(self, *args):
        if regex_validate_num(*args):
            # Also set the global kms variable.
            global_kms = int(args[0])
            self.ids.results_label.text = "Ok. You can proceed.\nThe kms you provided equal to " + str(global_kms) + ' kms.'
        else:
            self.ids.results_label.text = "The value you provided is wrong."

    pass


class ServiceApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    ServiceApp().run()
