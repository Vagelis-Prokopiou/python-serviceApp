import kivy

kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class ServiceApp(App):
    def build(self):
        # Define the Layouts
        box_layout_root = BoxLayout(orientation='vertical')
        box_layout_buttons = BoxLayout()
        box_layout_results = BoxLayout(orientation='vertical')

        # Define the Labels
        label_global_kms = Label(text='Please, provide the total kms of the vehicle.')
        label_results = Label(text='Results:')

        # Define the Text Inputs
        text_input_global_kms = TextInput(font_size=50, size_hint_y=None,
                                          height=100)
        text_input_results = TextInput(font_size=50)

        # Define the Buttons
        button_run_check = Button(text='Run a check.')
        button_update_entry = Button(text='Update an existing data entry.')
        button_insert_entry = Button(text='Insert a new data entry.')
        button_available_entries = Button(text='See the available data entries.')

        # Add widgets to the box_layout_buttons
        box_layout_buttons.add_widget(button_run_check)
        box_layout_buttons.add_widget(button_update_entry)
        box_layout_buttons.add_widget(button_insert_entry)
        box_layout_buttons.add_widget(button_available_entries)

        # Add widgets to the textarea_box_layout
        box_layout_results.add_widget(text_input_results)

        # Add widgets to the root_box_layout
        box_layout_root.add_widget(label_global_kms)
        box_layout_root.add_widget(text_input_global_kms)
        box_layout_root.add_widget(box_layout_buttons)
        box_layout_root.add_widget(box_layout_results)
        return box_layout_root


def some_function(*args):
    print('Text changed.')


if __name__ == '__main__':
    ServiceApp().run()
