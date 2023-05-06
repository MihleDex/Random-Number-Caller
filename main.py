from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.label import MDLabel

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.user_country_code = ""

        # Create App layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.add_widget(layout)

        # Add  blank widget
        layout.add_widget(Widget(size_hint=(1, 0.3)))

        # Create the image and center it vertically and horizontally
        image = Image(source='Images/earth.png', size_hint=(1, None), height=200)
        image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        layout.add_widget(image)

        # Add a label between the image and the text input
        welcome_text = MDLabel(text="Enter country code:", halign="center", size_hint=(1, None), height=50, font_style="H5")
        layout.add_widget(welcome_text)

        # Create and center the text input
        text_input = MDTextField(hint_text="Country Code Eg. +27", size_hint=(0.8, None), height=40)
        text_input.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        layout.add_widget(text_input)

        # Add a label widget for displaying error messages
        self.error_label = MDLabel(text="", halign="center", theme_text_color="Error")

        # Create the button and add it to the layout below the text input
        submit_button = MDRoundFlatButton(text='Submit', size_hint=(0.5, None), height=50)
        submit_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        submit_button.bind(on_press=lambda x: self.submit_text(text_input.text))
        layout.add_widget(submit_button)

        # Add the error label below the submit button
        layout.add_widget(self.error_label)
        

    def validate_country_code(self, text):
        if len(text) < 2 or text[0] != '+':
            return False
        for char in text[1:]:
            if not char.isdigit():
                return False
        return True

    def submit_text(self, text):
        if self.validate_country_code(text):
            # The country code is valid, do something with it
            self.user_country_code = text
            print(self.user_country_code)
            self.error_label.text = ""
            self.go_to_DialerScreen()

        else:
            # The country code is not valid, show an error message
            self.error_label.text = "Please enter a valid country code"

    def go_to_DialerScreen(self, *args):
        self.manager.current = 'DialerScreen'



class DialerScreen(Screen):
    def __init__(self, **kwargs):
        super(DialerScreen, self).__init__(**kwargs)

        self.add_widget(MDRectangleFlatButton(text='Go to Screen 3', on_release=self.go_to_PrankScreen))

    def go_to_PrankScreen(self, *args):
        self.manager.current = 'PrankScreen'

class PrankScreen(Screen):
    def __init__(self, **kwargs):
        super(PrankScreen, self).__init__(**kwargs)

        self.add_widget(MDRectangleFlatButton(text='Go to Screen 1', on_release=self.go_to_LoginScreen))

    def go_to_LoginScreen(self, *args):
        self.manager.current = 'LoginScreen'

class MyScreenManager(ScreenManager):
    pass

class MyApp(MDApp):
    def build(self):
        sm = MyScreenManager()
        Window.size = (480, 720)
        sm.add_widget(LoginScreen(name='LoginScreen'))
        sm.add_widget(DialerScreen(name='DialerScreen'))
        sm.add_widget(PrankScreen(name='PrankScreen'))
        return sm
    

if __name__ == '__main__':
    MyApp().run()
