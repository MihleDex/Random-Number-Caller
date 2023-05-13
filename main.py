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
from kivymd.uix.button import MDIconButton, MDFlatButton,MDRaisedButton
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.toolbar import MDTopAppBar
import random
from kivy.properties import StringProperty
from android.permissions import check_permission, request_permissions
from android.activity import AndroidActivity




class LoginScreen(Screen):
    input_text = StringProperty()
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

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
            app = MDApp.get_running_app()
            app.area_code = text
            self.error_label.text = ""
            self.go_to_DialerScreen()

        else:
            # The country code is not valid, show an error message
            self.error_label.text = "Please enter a valid country code"

    
    def go_to_DialerScreen(self, *args):
        self.manager.current = 'DialerScreen'

class DialerScreen(Screen):
    user_area_code = StringProperty()
    def __init__(self, **kwargs):
        super(DialerScreen, self).__init__(**kwargs)
        phone_number =""

        # Create the toolbar and set its properties
        toolbar = MDTopAppBar(title="Random Caller",anchor_title="left")
        toolbar.pos_hint = {'top': 1}
        toolbar.size_hint = (1, None)
        toolbar.height = '48dp'

        # Create the BoxLayout for the text input and add the phone dialer GridLayout to it
        bottom_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        # Add blank widget
        bottom_layout.add_widget(toolbar)
        bottom_layout.add_widget(Widget(size_hint=(1, 0.3)))
        # Add MDTextField
        self.phone_number_input = MDTextField(hint_text='Phone number', size_hint=(0.8, None), height=40,pos_hint={'center_x': .5})
        bottom_layout.add_widget(self.phone_number_input)
        # Add MDButtons
        button_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        # Add blank widget
        button_layout.add_widget(Widget(size_hint=(.2, .2)))
        button_layout.add_widget(MDRaisedButton(text='Generate', on_release=lambda x: self.generate_button_pressed(self.user_area_code), pos_hint={'center_y': .95,'center_x': 0},md_bg_color="green",rounded_button="True",elevation=2))
        button_layout.add_widget(MDRaisedButton(text='Call', on_release=lambda x: self.make_call(phone_number), pos_hint={'center_y': .95,'center_x': .5},md_bg_color="blue",rounded_button="True",elevation=2))
        button_layout.add_widget(Widget(size_hint=(.2, .2)))
        bottom_layout.add_widget(button_layout)
        # Add blank widget
        bottom_layout.add_widget(Widget(size_hint=(1, 1)))
        
        self.add_widget(bottom_layout)

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        self.user_area_code = app.area_code
    import random

    def generate_button_pressed(self, country_code):
        country_code = int(country_code[1:])
        print(country_code)
        if len(str(country_code)) >2:
            self.phone_number_input.text = "Invalid country code"
            return
        else:
            # Replace the following with the correct rules for the country you are generating phone numbers for
            if country_code == 1:
                area_code = str(random.randint(201, 999))
                prefix = random.randint(200, 999)
                line_number = random.randint(1000, 9999)
                self.phone_number_input.text = f"({area_code}) {prefix}-{line_number}"
            elif country_code == 27:
                mobile_network_operators = ["60", "61", "62", "63", "64", "65", "66", "67", "68", "69","60", "71", "72", "73", "74", "75", "76", "77", "78", "79", "81", "82", "83", "84", "85", "86", "87", "88", "89"]
                prefix = random.choice(mobile_network_operators)
                line_number = random.randint(1000000, 9999999)
                ln_a = str(line_number)[:3]
                ln_b = str(line_number)[3:7]
                self.phone_number_input.text = f"+27 {prefix} {int(ln_a)}-{int(ln_b)}"
                phone_number = self.phone_number_input.text

            else:
                # Add more elif statements for other countries here
                self.phone_number_input.text = "Invalid country code"


    def make_call(self,number):
        phone_number = number
        if check_permission('android.permission.CALL_PHONE'):
            AndroidActivity().send_intent('android.intent.action.CALL', 'tel:'+phone_number)
        else:
            request_permissions(['android.permission.CALL_PHONE'])

    def go_to_About_Screen(self, *args):
        self.manager.current = 'About_Screen'



class About_Screen(Screen):
    def __init__(self, **kwargs):
        super(About_Screen, self).__init__(**kwargs)

        self.add_widget(MDRectangleFlatButton(text='Go to Screen 1', on_release=self.go_to_LoginScreen))

    def go_to_LoginScreen(self, *args):
        self.manager.current = 'LoginScreen'

class MyScreenManager(ScreenManager):
    pass

class MyApp(MDApp):
    area_code = StringProperty("")
    def build(self):
        sm = MyScreenManager()
        Window.size = (480, 720)
        sm.add_widget(LoginScreen(name='LoginScreen'))
        sm.add_widget(DialerScreen(name='DialerScreen'))
        sm.add_widget(About_Screen(name='About_Screen'))
        self.root = sm
        return sm
    

if __name__ == '__main__':
    MyApp().run()
