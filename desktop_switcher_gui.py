import tkextrafont
from Heema import *

from desktop_switcher import *

import toggle_switch_button
# for the config database.
from tinydb import TinyDB, Query
import json

# {"_default": {"1": {"animations": "False", "show_labels": "False"}}}

def start():
    ##################### variables

    dock_positions = []
    position = 'center'

    # default config and user confing

    default_settings = {
        "animations": "False",
        "show_labels": "False",
        "elgato_on_startup": "False",
        "type": "default_settings"
    }

    user_settings = {
        "animations": "False",
        "show_labels": "False",
        "elgato_on_startup": "False",
        "type": "user_settings"
    }

    config_file = "./config.json"

    # connecting to db

    db = TinyDB(config_file)
    query_instance = Query()

    # getting the settings from the database

    default_settings_from_db = db.search(query_instance.type == "default_settings")
    #print(f"default_settings in db is: {default_settings_from_db}")

    user_settings_from_db = db.search(query_instance.type == "user_settings")
    #print(f"user_settings in db is: {user_settings_from_db}")

    # creating settings if they don't exist.

    if (default_settings_from_db == []):
        db.insert(default_settings)
    if (user_settings_from_db == []):
        db.insert(user_settings)


    ##########################3 above functions are the new functions
    def do_nothing():
        pass


    x = create_dock()

    # string vars config comes here:
    global user_choice_to_animate
    global user_choice_to_show_numbers_before_desktops
    user_choice_to_animate = StringVar()
    user_choice_to_show_numbers_before_desktops = StringVar()

    user_choice_to_animate.set(db.search(query_instance.type == "user_settings")[0]["animations"])

    user_choice_to_show_numbers_before_desktops.set(db.search(query_instance.type == "user_settings")[0]["show_labels"])

    #heema_icons = tkextrafont.Font(file="./heema-icons.ttf", family="heema-icons")
    heema_icons = tkextrafont.Font(file="heema-icons.ttf", family="heema-icons")
    x.wm_attributes("-topmost", 1)

    # x.unbind("<Escape>")

    # apply_theme(x, light_mode)
    # apply_theme(x, light_mode)
    apply_theme(x, reddish_purple)

    screen_width_place = int(x.winfo_screenwidth())
    screen_height_place = int(x.winfo_screenheight() * 0.9)

    desktops = get_desktops()
    # print(desktops)

    button_widths = []  # List to store button widths
    button_heights = []  # List to store button heights

    state = "on"  # Initial state of the toggle switch


    def open_more_settings():
        settings_page = menu_page(text="Settings")
        settings_page_option_frame = label_frame(settings_page)
        settings_page_option_frame.pack()

        apply_theme(settings_page, light_mode)
        make_rounded(settings_page)
        allow_mouse_drag(settings_page)

        def turn_animations_on_or_off():
            global user_choice_to_animate
            if animations_toggle_switch.state() == "off":
                user_choice_to_animate.set("False")
                db.update({"animations": "False"}, query_instance.type == "user_settings")
                user_choice_to_animate.set(db.search(query_instance.type == "user_settings")[0]["animations"])
                x.update()
            else:
                db.update({"animations": "True"}, query_instance.type == "user_settings")
                user_choice_to_animate.set(db.search(query_instance.type == "user_settings")[0]["animations"])
                x.update()

        label(settings_page_option_frame, text="Animations ").grid(row=0, column=0, sticky="E")
        animations_toggle_switch = toggle_switch_button.SwitchButton(settings_page_option_frame,
                                                                     toggle_state=(
                                                                         "on" if user_choice_to_animate.get() == "True" else "off"),
                                                                     on_click=turn_animations_on_or_off,
                                                                     font=(heema_icons, 42))
        animations_toggle_switch.grid(row=0, column=1, sticky="E")

        def restart():
            settings_page.destroy()
            x.destroy()
            start()

        def show_labels_on_or_off():
            global user_choice_to_show_numbers_before_desktops
            if show_labels_on_or_off_switch.state() == "off":
                user_choice_to_show_numbers_before_desktops.set("False")
                db.update({"show_labels": "False"}, query_instance.type == "user_settings")
                user_choice_to_show_numbers_before_desktops.set(
                    db.search(query_instance.type == "user_settings")[0]["show_labels"])
                restart()



            else:
                db.update({"show_labels": "True"}, query_instance.type == "user_settings")
                user_choice_to_show_numbers_before_desktops.set(
                    db.search(query_instance.type == "user_settings")[0]["show_labels"])
                restart()

        label(settings_page_option_frame, text="Show numbers before Desktop").grid(row=1, column=0, sticky="E")

        global show_labels_on_or_off_switch
        show_labels_on_or_off_switch = toggle_switch_button.SwitchButton(settings_page_option_frame,
                                                                         toggle_state=(
                                                                             "on" if user_choice_to_show_numbers_before_desktops.get() == "True" else "off"),
                                                                         on_click=show_labels_on_or_off,
                                                                         font=(heema_icons, 42))

        show_labels_on_or_off_switch.grid(row=1, column=1, sticky="E")
        settings_page.mainloop()


    desktop_button_frame = frame(x)
    desktop_button_frame.pack(side=LEFT)

    # button_schemes are: button,button1,white_label_button
    button_scheme = "button1"
    global button
    if (button_scheme == 'button'):
        button = button1
    elif (button_scheme == 'white_label_button'):
        button = white_label_button
    else:
        pass
    for desktop in desktops:
        # print(desktop)

        # if show numbers is enabled. show below
        # b1 = button(desktop_button_frame, text=f"{desktops[desktop]} {desktop}", command=lambda desktop=desktop: open_desktop_by_name(desktop))

        # if show numbers is not enabled, show the following
        if (user_choice_to_show_numbers_before_desktops.get() == "False"):

            b1 = button(desktop_button_frame, text=f"{desktop}",
                        command=lambda desktop=desktop: open_desktop_by_name(desktop))
        else:
            b1 = button(desktop_button_frame, text=f"{desktops[desktop]+1}) {desktop}",
                        command=lambda desktop=desktop: open_desktop_by_name(desktop))
        b1.config(font=('Segoe UI', 10), highlightthickness=0, takefocus=0)
        b1.pack(side=LEFT, padx=5)

        # Get the required width and height of the button and add them to the lists
        button_widths.append(b1.winfo_reqwidth())
        button_heights.append(b1.winfo_reqheight())
        # b1.destroy

    global hidden
    hidden = False


    def hide_unhide(animated=user_choice_to_animate.get()):
        global hidden

        if (animated == "False"):
            if (hidden == False):
                # desktop_button_frame.pack_forget()
                desktop_button_frame.pack_forget()
                # b3.winfo_reqwidth() b0.winfo_reqwidth()

                x.geometry(
                    f"{options_buttons_frame.winfo_reqwidth()}x{required_height}+{options_buttons_frame.winfo_rootx()}+{options_buttons_frame.winfo_rooty()}")
                hidden = True

            else:

                options_buttons_frame.pack_forget()
                desktop_button_frame.pack(side=LEFT)
                options_buttons_frame.pack()
                x.geometry(
                    f"{options_buttons_frame.winfo_reqwidth() + desktop_button_frame.winfo_reqwidth()}x{required_height}+{options_buttons_frame.winfo_rootx() - desktop_button_frame.winfo_reqwidth()}+{options_buttons_frame.winfo_rooty()}")

                global position
                hidden = False
        else:

            def animate():
                global hidden
                if hidden == False:
                    desktop_button_frame.pack_forget()
                    animate_hide(options_buttons_frame)
                    hidden = True
                else:
                    options_buttons_frame.pack_forget()
                    desktop_button_frame.pack(side=LEFT)
                    options_buttons_frame.pack()
                    animate_show(options_buttons_frame)
                    hidden = False

            def animate_hide(frame_to_hide):
                width = frame_to_hide.winfo_reqwidth()
                height = required_height
                x_pos = options_buttons_frame.winfo_rootx()
                y_pos = options_buttons_frame.winfo_rooty()

                for i in range(0, width + 1, 5):
                    x.geometry(f"{i}x{height}+{x_pos}+{y_pos}")
                    x.update()
                    time.sleep(0.01)

            def animate_show(frame_to_show):
                width = options_buttons_frame.winfo_reqwidth() + desktop_button_frame.winfo_reqwidth()
                height = required_height
                x_pos = options_buttons_frame.winfo_rootx() - desktop_button_frame.winfo_reqwidth()
                y_pos = options_buttons_frame.winfo_rooty()

                for i in range(options_buttons_frame.winfo_reqwidth(), width + 10, 10):
                    x.geometry(f"{i}x{height}+{x_pos}+{y_pos}")
                    x.update()
                    # time.sleep(0.1)

            animate()

        #######################################################################################################


    options_buttons_frame = label_frame(x)
    options_buttons_frame.pack()

    b2 = button1(options_buttons_frame, text=f"⚙️", command=open_more_settings)
    b2.config(font=('Segoe UI', 10), highlightthickness=0)
    b2.pack(side=LEFT, padx=8)
    button_widths.append(b2.winfo_reqwidth())
    button_heights.append(b2.winfo_reqheight())

    b3 = button1(options_buttons_frame, text=f">", command=lambda: hide_unhide(animated=user_choice_to_animate.get()))
    b3.config(font=('Segoe UI', 10), highlightthickness=0)
    b3.pack(side=LEFT, padx=2)
    button_widths.append(b3.winfo_reqwidth())
    button_heights.append(b3.winfo_reqheight())

    b0 = button1(options_buttons_frame, text=f" drag 🤚", command=do_nothing)
    b0.config(font=('Segoe UI', 10), highlightthickness=0)
    b0.pack(side=LEFT, padx=2)
    button_widths.append(b0.winfo_reqwidth())
    button_heights.append(b0.winfo_reqheight())

    # Calculate required width and height based on button widths, heights, and padding
    required_width = sum(button_widths) + len(button_widths) * 10  # Adjust padding as needed
    required_height = max(button_heights) + 2


    def place_dock(position):
        if (position == 'center'):
            x.update()
            required_width = options_buttons_frame.winfo_reqwidth() + desktop_button_frame.winfo_reqwidth()
            center_width = int(screen_width_place / 2) - int(required_width / 2)
            # orignal
            # x.geometry(f"{required_width}x{required_height}+{center_width}+{screen_height_place}")

            # test

            x.geometry(f"{required_width}x{required_height}+{center_width}+{screen_height_place}")

        else:
            x.geometry(f"{required_width}x{required_height}+{screen_width_place - required_width}+{screen_height_place}")


    place_dock(position)

    lastClickX = 0
    lastClickY = 0


    def SaveLastClickPos(event):
        global lastClickX, lastClickY
        lastClickX = event.x
        lastClickY = event.y

    global window
    window = x


    def Dragging(event):
        global window
        x = event.x - lastClickX + window.winfo_x()
        y = event.y - lastClickY + window.winfo_y()
        window.geometry(f"+{x}+{y}")


    x.bind('<Button-1>', SaveLastClickPos)
    x.bind('<B1-Motion>', Dragging)
    # x.overrideredirect(True)

    make_rounded(x)

    # x.bind("<Enter>",make_dock_opaque)
    # x.bind("<Leave>",make_dock_transparent)

    x.mainloop()



start()
