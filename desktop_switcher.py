import os
import ctypes
import time

#loding teh dll adn creating the desktop accessor



#os.path won't work here as it takes the path of the terminal instead of the file's directory, helpbro will work, as it needs it's working directory.
path_of_dll = os.path.dirname(os.path.abspath(__file__))+"//VirtualDesktopAccessor.dll"
virtual_desktop_accessor = ctypes.WinDLL(path_of_dll)

# defining the function prototype
GetDesktopName = virtual_desktop_accessor.GetDesktopName
GetDesktopName.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char), ctypes.c_size_t]
GetDesktopName.restype = ctypes.c_int






# function to get number of desktops/ returns an int
def get_number_of_desktops():
    # Get the number of desktops
    desktop_count = virtual_desktop_accessor.GetDesktopCount()
    #print(f"Number of desktops: {desktop_count}")
    return desktop_count


#function to return the desktops with their names, and index,/ returns a dict{'name':index}
def get_desktops():
    # Get the name of each desktop
    desktops={}
    desktop_count=get_number_of_desktops()
    for desktop_number in range(desktop_count):
        name_buffer = ctypes.create_string_buffer(256)  # Assuming max name length is 255 characters
        result = GetDesktopName(desktop_number, name_buffer, ctypes.sizeof(name_buffer))
        if result != 0:
            #print(f"Desktop {desktop_number} name: {name_buffer.value.decode('utf-8')}")
            desktops[f"{name_buffer.value.decode('utf-8')}"]= desktop_number
            
        else:
            #print(f"Desktop {desktop_number} name: {name_buffer.value.decode('utf-8')}")
            print("something went wrong.")

    #print(desktops)
    return desktops



#function to show the desktops, also refresh the desktops on creation. prints the menu.
def show_desktop_menu():

    all_desktops=get_desktops()

    print('All Desktops: ',end='\t\t\t')
    for desktop in all_desktops:
        print(str(all_desktops[desktop])+':'+desktop, end='\t \t')
    print()
    #open_desktop(desktop_name='output')





def open_desktop_by_name(desktop_name):
    desktops=get_desktops()
    try:
        virtual_desktop_accessor.GoToDesktopNumber(desktops[desktop_name])
        time.sleep(0.01) #this sleep is helping in making sure handle is not lost.
    except:
        print("No such desktop found.")


def open_desktop_by_number(desktop_number):
    desktops=get_desktops()

    try:
        virtual_desktop_accessor.GoToDesktopNumber(desktop_number)
        time.sleep(0.01) #this sleep is helping in making sure handle is not lost.
    except:
        print("No such desktop found.")


