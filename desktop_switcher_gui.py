from Heema import *
from desktop_switcher import *

def do_nothing():
    pass

x = create_dock()
x.wm_attributes("-topmost", 1)

#apply_theme(x, light_mode)
apply_theme(x,reddish_purple)

screen_width_place = int(x.winfo_screenwidth())
screen_height_place = int(x.winfo_screenheight() * 0.9)

desktops = get_desktops()
print(desktops)

button_widths = []  # List to store button widths
button_heights = []  # List to store button heights


def open_more_settings():
    settings_page=menu_page(text="Settings")
    apply_theme(settings_page,super_dark_mode)

    

    settings_page.mainloop()


for desktop in desktops:
    #print(desktop)
    b1 = button1(x, text=f"{desktop}", command=lambda desktop=desktop: open_desktop_by_name(desktop))
    b1.config(font=('Segoe UI', 10))
    b1.pack(side=LEFT, padx=5)
    
    # Get the required width and height of the button and add them to the lists
    button_widths.append(b1.winfo_reqwidth())
    button_heights.append(b1.winfo_reqheight())
    b1.destroy

b2 = button1(x, text=f"⚙️", command=open_more_settings)
b2.config(font=('Segoe UI', 10))
b2.pack(side=LEFT, padx=8)
button_widths.append(b2.winfo_reqwidth())
button_heights.append(b2.winfo_reqheight())




b3 = button1(x, text=f"Hide/unhide", command=do_nothing)
b3.config(font=('Segoe UI', 10))
b3.pack(side=LEFT,padx=2)
button_widths.append(b3.winfo_reqwidth())
button_heights.append(b3.winfo_reqheight())


# Calculate required width and height based on button widths, heights, and padding
required_width = sum(button_widths) + len(button_widths) * 10  # Adjust padding as needed
required_height = max(button_heights)+2

x.geometry(f"{required_width}x{required_height}+{screen_width_place-required_width}+{screen_height_place}")

lastClickX = 0
lastClickY = 0

def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

window = x
def Dragging(event):
    global window
    x = event.x - lastClickX + window.winfo_x()
    y = event.y - lastClickY + window.winfo_y()
    window.geometry(f"+{x}+{y}")

x.bind('<Button-1>', SaveLastClickPos)
x.bind('<B1-Motion>', Dragging)
x.overrideredirect(True)

x.mainloop()
