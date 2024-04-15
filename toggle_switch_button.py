
from Heema import label_bd,Button
import tkextrafont
class SwitchButton(Button):
    def __init__(self, *args, on_click=None,toggle_state="off", **kwargs):
        super().__init__(*args, **kwargs)

        self._state = toggle_state
        self.configure(bd=label_bd, activebackground=self.master.cget("background"),
                       activeforeground=self.master.cget("background"),
                       background=self.master.cget("background"))  # Set button background to root's background
        self.update_text()  # Update button text based on initial state

        if on_click:
            self.bind("<Button-1>", lambda event: self.execute_functions(on_click))

    def state(self, new_state=None):
        if new_state is not None:
            self._state = new_state
            self.update_text()  # Update button text when state changes
        return self._state

    def toggle(self):
        if self._state == "on":
            self._state = "off"
        else:
            self._state = "on"
        self.update_text()  # Update button text based on new state

    def update_text(self):
        toggle_on_symbol = u"\ued0a"  # Symbol for the "on" state
        toggle_off_symbol = u"\ued09"  # Symbol for the "off" state
        toggle_text = toggle_off_symbol if self._state == "off" else toggle_on_symbol
        self.config(text=toggle_text, fg="#565656" if self._state == "off" else "#ffffff")

    def execute_functions(self, on_click):
        self.toggle()  # Toggle button state
        on_click()  # Execute the function passed as argument

