from kivymd.uix.behaviors import RectangularRippleBehavior, RoundedRectangularElevationBehavior
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.vkeyboard import VKeyboard
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.metrics import dp
import json


KV = '''
#: import gch kivy.utils.get_color_from_hex
<CustomDropDownItem>:
    y: self.parent.height - self.height - dp(130)
    on_release:
        root.menu.open()
        select_country_button_icon.icon = "chevron-down-circle" if select_country_button_icon.icon in ["chevron-right-circle"] \
        else "chevron-right-circle"
    id: dropdown_item
    current_item: '+237'
    size_hint_y: None
    height: dp(48)
    md_bg_color: gch("#ffd470")
    radius: [dp(6),]
    padding: [dp(10), dp(9)]

    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            size: self.size[0] - dp(4), self.size[1] - dp(4)
            pos: self.pos[0] + dp(2), self.pos[1] + dp(2)
            radius: [dp(6),]

    FitImage:
        id: select_country_button_flag
        size_hint: None, None
        height: dp(30)
        width: dp(30) + dp(30/4)
        source: "assets/flags/cm.png"

    MDLabel:
        id: select_country_button_text
        text: 'Cameroon +237'
        size_hint_y: None
        height: self.parent.height
        markup: True
        shorten: True
        shorten_from: 'right'
        font_style: "Caption"
        font_size: dp(15)
        valign: "center"
        halign: "center"
        pos_hint: {"center_y": .5}

    MDIcon:
        id: select_country_button_icon
        icon: "chevron-right-circle"
        size_hint_y: None
        height: self.parent.height
        font_style: "Icon"
        font_size: dp(20)
        halign: "right"
        pos_hint: {"center_y": .5}


<CountryCodePicker>:
    name: 'ccp_screen'

    RelativeLayout:

        MDToolbar:
            title: 'Numeric Keyboard Implementation'
            elevation: 10
            y: self.parent.height - self.height

        MDLabel:
            text: 'Number TextField'
            font_size: 15
            y: self.parent.height - self.height - dp(90)
            pos_hint :{'center_x':0.5}
            halign: 'center'
            size_hint_y: None
            height: dp(20)

        MDBoxLayout:
            padding: [dp(20), dp(10), dp(20), dp(10)]

            CustomDropDownItem:
                y: self.parent.height - self.height - dp(130)


            MDTextField
                y: self.parent.height - self.height - dp(170)
                id : reg_tel_number
                hint_text: "Mobile Number"
                mode: "rectangle"
                size_hint_y: None
                height: dp(48)
                input_filter: 'int'
                input_type: 'number'
                multiline: False
                color_mode: "custom"
                current_hint_text_color: gch("#ffd470")
                line_color_focus: gch("#ffd470")
                on_focus: root.set_layout(keyboard_anchor, self)

        RelativeLayout:
            id: keyboard_anchor
            size_hint_y: 0.5


WindowManager:
    CountryCodePicker:
        id: ccp_screen
'''

class WindowManager(ScreenManager):
    pass

class CustomDropDownItem(RoundedRectangularElevationBehavior, RectangularRippleBehavior, ButtonBehavior, MDBoxLayout):
    curent_item = StringProperty()
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        f = open('assets/docs/country_code_flags.json')
        menu_items = json.load(f)
        new_menu = [
            {
                "text1": "{}".format(x['name']),
                "text2": "{}".format(x['dial_code']),
                "viewclass": "DropListItem",
                "icon": "{}".format(x["flag"]),
                "height": dp(40),
                "on_release": lambda x="{} {} {}".format(x['flag'], x['name'], x['dial_code']): self.set_item(x),
            }
            for x in menu_items
        ]
        print(self)
        dropdown_item = self
        self.menu = MDDropdownMenu(
            caller=dropdown_item,
            items=new_menu,
            position="auto",
            width_mult=7,
        )
        self.menu.bind(on_release=self.set_item)

    def set_item(self, value_items):
        self.root.ids.register_screen.ids.select_country_button_flag.icon = "chevron-right-circle"
        value_items = value_items.split(" ")
        flag = value_items[0]
        country_name = value_items[1]
        dial_code = value_items[-1]
        self.ids.select_country_button_flag.source = flag
        self.ids.select_country_button_text.text = country_name + " " + dial_code
        self.ids.dropdown_item.current_item = dial_code
        self.menu.dismiss()

class CountryCodePicker(MDScreen):
    focus_count = 0
    def set_layout(self, keyboard_anchor, target_textfield):
        self.focus_count += 1
        v_keyboard = NumericKeyboard(
            text_field = target_textfield
        )
        keyboard_anchor.clear_widgets()
        keyboard_anchor.add_widget(v_keyboard)

        if self.focus_count == 2:
            keyboard_anchor.clear_widgets()
            self.focus_count = 0

class NumericKeyboard(VKeyboard):
    text_field = ObjectProperty()
    custom_vk_layout = ObjectProperty('numeric.json')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.available_layouts['numpad'] = self.custom_vk_layout
        self.layout = self.custom_vk_layout
        self.pos_hint = {'center_x': 0.5}

    def on_key_down(self, keyboard, keycode, text, *args):
        """ The callback function that catches keyboard events. """

        if isinstance(keycode, tuple):
            keycode = keycode[1]

        if keycode == "bs":
            if len(textfield_data) > 0:
                self.text_field.text = textfield_data[:-1]
        else:
            self.text_field.text += u"{0}".format(keycode)


    def on_key_up(self, keyboard, keycode, *args):
        """ The callback function that catches keyboard events. """
        textfield_data = self.text_field.text

        if isinstance(keycode, tuple):
            keycode = keycode[1]

        if keycode == "bs":
            if len(textfield_data) > 0:
                self.text_field.text = textfield_data[:-1]
        else:
            self.text_field.text += u"{0}".format(keycode)

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    MainApp().run()
