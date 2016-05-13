import kivy

kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class RootWidget(BoxLayout):
    pass


class ServiceApp(App):
    def build(self):
        return RootWidget()


def some_function(*args):
    print('Text changed.')


if __name__ == '__main__':
    ServiceApp().run()
