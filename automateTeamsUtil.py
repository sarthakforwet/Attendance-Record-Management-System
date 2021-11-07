from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto.findwindows import ElementNotFoundError
import time

def send_attendance_alert(meeting_name: str, ptr: int):
    app = Application(backend='uia').connect(title_re=meeting_name)

    # Open the message bar
    #print(app.window().print_control_identifiers())
    #app.window().print_control_identifiers()
    try:
        showConversation = app.window().child_window(title="Show conversation", auto_id="chat-button", control_type="Button").click()
        time.sleep(2)
    except ElementNotFoundError:
        print("here")
        pass

    finally:
        #print(app.window().print_control_identifiers())
        messageWindow = app.window().child_window(title="Type a new message", found_index=0,control_type="Edit")
        messageWindow.click_input()
        time.sleep(1)
        messageWindow.type_keys(f"Attendance count for {ptr} second is about to Happen!!", with_spaces=True)
        send = app.window().child_window(title="Send", control_type="Button")
        #send.click_input()
        send.click()
        # Close the message Bar
        hideConversation = app.window().child_window(title="Hide conversation", auto_id="chat-button", control_type="Button").click()
        send_keys('%{TAB}')