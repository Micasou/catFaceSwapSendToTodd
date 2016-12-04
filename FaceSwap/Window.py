from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class Window(GridLayout):

    def send(instance, value):
        print(instance.filePath.text + ' ' +instance.phoneNumber.text)

    def __init__(self, **kwargs):
        super(Window, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='File Path'))
        self.filePath = TextInput(multiline=False)
        self.add_widget(self.filePath)
        self.add_widget(Label(text='phoneNumber'))
        self.phoneNumber = TextInput(multiline=False)
        self.add_widget(self.phoneNumber)
        self.btn_send = Button(text='Send', font_size=14)
        self.add_widget(self.btn_send)
        self.btn_send.bind(on_press=self.send)

class MyApp(App):

    def build(self):
        return Window()


if __name__ == '__main__':
    MyApp().run()