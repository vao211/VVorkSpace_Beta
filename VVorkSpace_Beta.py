import customtkinter as ctk
import Messagebox as msb
import os
import sys
from PIL import Image, ImageTk
from tkinter import filedialog
import win32com.client
import shutil
import json

def app_init():
    #create bin folder if deleted
    if not os.path.exists('bin'):
        os.makedirs('./bin')
    if not os.path.exists('bin/resolution.json'):
        with open('bin/resolution.json', 'w') as f:
            json.dump({"width": 1280, "height": 720, "fullscreen": 0}, f, indent=4)
    
    global app, cur, app_window_width, app_window_height, screen_stat
    #load full screen status
    screen_stat = json.load(open('bin/resolution.json'))['fullscreen']
    app_window_width = json.load(open('bin/resolution.json'))['width']
    app_window_height = json.load(open('bin/resolution.json'))['height']
    cur = "@./cursor/cursor.cur"
    app = ctk.CTk()
    app.title("VVorkSpace Beta")
    app.iconbitmap("./icon/VVorkSpace.ico")
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width - app_window_width) // 2
    y = (screen_height - app_window_height) // 2
    app.geometry(f"{app_window_width}x{app_window_height}+{x}+{y-20}")
        
    check_startup_full_screen_status()    
    #full screen mode
    # app.attributes('-fullscreen', True)

    app.bind("<F11>", lambda e: check_full_screen())
    
    app.config(bg="black", cursor=cur)
    app.resizable(True, True)
    
    #grid (5x8)
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=1)
    app.grid_rowconfigure(3, weight=1)
    app.grid_rowconfigure(4, weight=0)
    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=1)
    app.grid_columnconfigure(2, weight=1)
    app.grid_columnconfigure(3, weight=1)
    app.grid_columnconfigure(4, weight=1)
    app.grid_columnconfigure(5, weight=1)
    app.grid_columnconfigure(6, weight=1)
    app.grid_columnconfigure(7, weight=0)
    
    '''
    [0, 0] [0, 1] [0, 2] [0, 3] [0, 4] [0, 5] [0, 6] [0, 7]
    [1, 0] [1, 1] [1, 2] [1, 3] [1, 4] [1, 5] [1, 6] [1, 7]
    [2, 0] [2, 1] [2, 2] [2, 3] [2, 4] [2, 5] [2, 6] [2, 7]
    [3, 0] [3, 1] [3, 2] [3, 3] [3, 4] [3, 5] [3, 6] [3, 7]
    [4, 0] [4, 1] [4, 2] [4, 3] [4, 4] [4, 5] [4, 6] [4, 7]
    '''

    
    #exit grid visualization   
    app.bind("<Control-v>", lambda e: visualize_grid(status=True))
    app.bind("<Control-Shift-V>", lambda e: visualize_grid(status=False))
    global frames
    frames = []
    
def check_startup_full_screen_status():
    if screen_stat == 1:
        app.attributes("-fullscreen", True)
    else:
        app.attributes("-fullscreen", False)
    
#check full screen mode status
def check_full_screen():
    global screen_stat 
    if screen_stat == 1:
        app.attributes("-fullscreen", False)
        #app._set_appearance_mode("win")
        app._windows_set_titlebar_color("dark")
        with open('bin/resolution.json', 'w') as f:
            json.dump({"width": app_window_width, "height": app_window_height,"fullscreen": 0},
                      f, indent=4)
        screen_stat = 0

    else:
        app.attributes("-fullscreen", True)
        with open('bin/resolution.json', 'w') as f:
            json.dump({"width": app_window_width, "height": app_window_height,"fullscreen": 1},
                      f, indent=4)
        screen_stat = 1
        
def set_resolution(width, height):
    global app_window_width, app_window_height
    app_window_width = width
    app_window_height = height
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width - app_window_width) // 2
    y = (screen_height - app_window_height) // 2
    app.geometry(f"{app_window_width}x{app_window_height}+{x}+{y-20}")
    with open('bin/resolution.json', 'w') as f:
        json.dump({"width": app_window_width, "height": app_window_height, "fullscreen": screen_stat},
                  f, indent=4)
    app.update_idletasks()
    
#visualize_grid()
def visualize_grid(status=True):
    if status == True:
        for row in range(5):
            for col in range(8):
                frame = ctk.CTkFrame(app, width=100, height=100, bg_color="black", fg_color="black")
                frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                label = ctk.CTkLabel(frame, text=f"({row}, {col})")
                label.place(relx=0.5, rely=0.5, anchor="center")
                frames.append(frame)
    else:
        for frame in frames:
            frame.destroy()
        frames.clear()
          
def add_button(parent, text, image, command, bg_color, fg_color, width, height, row, column, padx, pady):
    #split file extension
    if text != None:
        text = text.rsplit(".", 1)[0]
    button = ctk.CTkButton(parent, text=text,
                                image=image, command=command, 
                                bg_color=bg_color, fg_color=fg_color, 
                                width=width, height=height)
    button.grid(row=row, column=column, padx=padx, pady=pady)
    button.configure(cursor=cur)


def run_on_startup():
    create_shortcut(sys.executable,
                    os.path.join(os.path.expanduser("~"),
                                 "AppData", "Roaming", "Microsoft", "Windows",
                                 "Start Menu", "Programs", "Startup",
                                 "VVork Space.lnk"), mess=False)
    msb.CTkMessagebox.messagebox(title="Run on startup!", text="VVork Space will run on startup",
                                 sound="on", button_text="OK", 
                                 size="320x150", center=True, top=True)
    
def create_shortcut(target, shortcut_path, mess=True):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.IconLocation = target
    shortcut.save()
    if mess:
        msb.CTkMessagebox.messagebox(title="Shortcut created!", 
                                     text=f"Shortcut created at:\n{shortcut_path}", 
                                     sound="on", button_text="OK", size="320x150", 
                                     center=True, top=True)
def change_resolution():
    global change_resolution_window
    change_resolution_window = ctk.CTkToplevel(setting_window)
    change_resolution_window.title("Change Resolution")
    change_resolution_window.resizable(False, False)
    change_resolution_window.grab_set()
    change_resolution_window.config(cursor=cur, bg="black")
    
    screen_width = setting_window.winfo_screenwidth()
    screen_height = setting_window.winfo_screenheight()
    window_width = 480
    window_height = 320
    
    position_right = int(screen_width/2 - window_width/2)
    position_down = int(screen_height/2 - window_height/2)
    change_resolution_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

    #resolution list
    change_resolution_window.grid_rowconfigure(0, weight=1)
    change_resolution_window.grid_rowconfigure(1, weight=1)
    change_resolution_window.grid_rowconfigure(2, weight=1)
    change_resolution_window.grid_rowconfigure(3, weight=1)
    change_resolution_window.grid_rowconfigure(4, weight=1)
    
    change_resolution_window.grid_columnconfigure(0, weight=1)
    change_resolution_window.grid_columnconfigure(1, weight=0)
    change_resolution_window.grid_columnconfigure(2, weight=1)
    
    add_button(change_resolution_window, "1920x1080", None, 
               lambda: [set_resolution(1920, 1080) ,
                change_resolution_window.destroy(), 
                setting_window.destroy()]
               , "black","#0c2c7b", 100, 80, 0, 1,20,20)
    add_button(change_resolution_window, "1600x900", None, 
               lambda:[set_resolution(1600, 900),
                change_resolution_window.destroy(), 
                setting_window.destroy()],
                "black", "#0c2c7b", 100, 80, 1, 1, 20, 20)
    add_button(change_resolution_window, "1366x768", None, 
               lambda:[set_resolution(1366, 768), 
                       change_resolution_window.destroy(), 
                       setting_window.destroy()],
                "black", "#0c2c7b", 100, 80, 2, 1, 20, 20)
    add_button(change_resolution_window, "1280x720", None, 
               lambda:[set_resolution(1280, 720), 
                       change_resolution_window.destroy(), 
                       setting_window.destroy()],
                "black", "#0c2c7b", 100, 80, 3, 1, 20, 20)
    add_button(change_resolution_window, "900x600", None, 
               lambda:[set_resolution(900, 600), 
                       change_resolution_window.destroy(), 
                       setting_window.destroy()],
                "black", "#0c2c7b", 100, 80, 4, 1, 20, 20)
    
def setting_init():
    global setting_window
    setting_window = ctk.CTkToplevel(app)
    setting_window.title("Settings")
    setting_window.resizable(False, False)
    setting_window.grab_set()  #block other windows
    setting_window.config(cursor=cur, bg="black")
    
    screen_width = setting_window.winfo_screenwidth()
    screen_height = setting_window.winfo_screenheight()
    window_width = 720
    window_height = 480
    position_right = int(screen_width/2 - window_width/2)
    position_down = int(screen_height/2 - window_height/2)
    setting_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
    
    #creat_shortcut button
    add_button(setting_window, "Create Shortcut", defaut_img.get("img_create_shortcut"), 
               lambda :  create_shortcut(sys.executable, 
                                        os.path.join(os.path.expanduser("~"), "Desktop", "VVork Space.lnk")),
               "black", "black", 0, 0, 0, 0, 20, 20)
    #run on startup button
    add_button(setting_window, "Run on startup",defaut_img.get("img_run_on_startup") , lambda: run_on_startup(), "black", "black", 0, 0, 1, 0, 20, 20)
    
    add_button(setting_window, "Change resolution", defaut_img.get("img_change_resolution"), lambda: change_resolution() , "black", "black", 0, 0, 2, 0, 20, 20)

#fix open some shortcut (using os.startfile instead of subprocess)
def open_app(file_path):
    print(f"Opening: {file_path}")
    os.startfile(file_path)
    
def open_file_dialog():
    file_path = filedialog.askopenfilename(
        title="Select a file or shortcut",
        filetypes=[("Shortcut files", "*.lnk"), ("All files", "*.*")]
    )
    
    if file_path:
        #check if file is shortcut
        if file_path.lower().endswith('.lnk'):
            print(f"Selected shortcut: {file_path}")
            choose_icon(file_path)
        else:
            print(f"Selected file: {file_path}")
            choose_icon(file_path)
    
def open_folder_dialog():
    folder_path = filedialog.askdirectory()
    if folder_path:
        choose_icon(folder_path)
          
def choose_icon(file_path):
    filetypes = [
        ('Image files', '*.png;*.jpg;*.jpeg;*.ico'),
        ('PNG files', '*.png'),
        ('JPEG files', '*.jpg;*.jpeg'),
        ('ICO files', '*.ico'),
    ]
    
    icon_path = filedialog.askopenfilename(
        title="Choose an icon (or keep blank)",
        filetypes = filetypes
    )
    #note: Thêm tính năg thêm tên app khi icon trống     
    if icon_path:
        try: #copy icon to button_icon folder
            if not os.path.exists('button_icon'):
                os.makedirs('button_icon')
            
            new_filename = os.path.basename(icon_path)
            new_path = os.path.join('button_icon', new_filename) # newpath(icon_path) = ./button_path/name
            
            shutil.copy2(icon_path, new_path)
            
            choose_position(file_path ,icon_path = new_path)  # * new_path
            
            return new_path
     
        except Exception as e:
            msb.CTkMessagebox.messagebox(
                title="Error!",
                text=f"Error copying icon: {e}",
                sound="off",
                button_text="OK",
                size="320x150",
                center=True,
                top=True
            )
    else:
        choose_position(file_path ,icon_path = None)
        return None
    return None

def choose_position(file_path, icon_path): #icon_path = new_path = ./button_path/name
    position_window = ctk.CTkToplevel(app)
    position_window.title("Choose Position")
    position_window.resizable(False, False)
    position_window.grab_set()
    position_window.config(cursor=cur, bg="black")
    
    screen_width = position_window.winfo_screenwidth()
    screen_height = position_window.winfo_screenheight()
    window_width = 420
    window_height = 210
    position_right = int(screen_width/2 - window_width/2)
    position_down = int(screen_height/2 - window_height/2)
    position_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
    
    for row in range(1, 4):
        for column in range(1, 7):
            button = ctk.CTkButton(
                position_window,
                text=f"({row}, {column})",
                command=lambda r=row, c=column: [
                    place_icon(file_path,icon_path, r, c),
                    position_window.destroy() ]
                ,
                width=60,
                height=60
            )
            button.grid(row=row, column=column, padx=5, pady=5)
            button.configure(cursor=cur)


def place_icon(file_path,icon_path, row, column): #icon_path = new_path = ./button_path/name
    if icon_path != None:
        try:
            #tạo image
            icon = Image.open(icon_path)
            icon = icon.resize((100, 100), Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon)
            
            add_button(app, None, icon_photo,lambda: open_app(file_path),
                "black","black",
                100,100,row, column,5,5
            )
            
            save_button_info(file_path, icon_path, row, column) #save to json for load on start up
        
               
        except Exception as e:
            msb.CTkMessagebox.messagebox(
                title="Error!",text=f"Error placing icon: {e}",sound="off",button_text="OK",size="320x150",
                center=True,
                top=True
            )
    #add name of app if icon_path == None:
    else:
        try:
            app_name = os.path.basename(file_path)
            app_name, _ = os.path.splitext(app_name)
            defaut_app_icon = defaut_img.get("img_app_default")
            add_button(app, app_name, defaut_app_icon ,lambda: open_app(file_path),
                "black","black",
                100,100,row, column,5,5
            )     
                  
            save_button_info(file_path, icon_path, row, column)
        except Exception as e:
            msb.CTkMessagebox.messagebox(
                title="Error!",text=f"Error placing icon: {e}",sound="off",button_text="OK",size="320x150",
                center=True,
                top=True
            )
            
    #reload icon after placing
    app.update_idletasks()

save_file = r"./bin/saved_buttons.json"

def load_saved_buttons():
    if os.path.exists(save_file):
        try:
            with open(save_file, 'r') as f:
                return json.load(f)
        except:
            return []
    return []


def save_button_info(file_path, icon_path, row, column):   #icon_path = new_path = ./button_path/name
    buttons = load_saved_buttons()
    
    # if os.path.dirname(icon_path) == 'button_icon':
    #     icon_path = os.path.join('button_icon', os.path.basename(icon_path))  #os.path.basename(icon_path) == name of icon file
    
    button_info = {
        'file_path': file_path,
        'icon_path': icon_path,
        'row': row,
        'column': column
    }
    
    buttons = [b for b in buttons if not (b['row'] == row and b['column'] == column)]
    buttons.append(button_info)
    
    with open(save_file, 'w') as f:
        json.dump(buttons, f, indent=4)
        
def restore_button():
    buttons = load_saved_buttons()
    for button in buttons:
        try:
            if button["icon_path"] is not None:
                icon_photo = ImageTk.PhotoImage(Image.open(button['icon_path']).resize((100, 100), Image.Resampling.LANCZOS))
                add_button(app, None, icon_photo,
                        lambda path=button['file_path']: open_app(path),
                        "black", "black",
                        100, 100,
                        button['row'], button['column'],
                        5, 5)
            else: #fix restore None icon app
                icon_photo = defaut_img.get("img_app_default")
                add_button(app, os.path.basename(button['file_path']), icon_photo,
                        lambda path=button['file_path']: open_app(path),
                        "black", "black",
                        100, 100,
                        button['row'], button['column'],
                        5, 5)
        except Exception as e:
            print(f"Error restoring button: {e}")

                    
                     
def add_app():
    add_app_window = ctk.CTkToplevel(app)
    add_app_window.title("Add an app to VVorkSpace")
    add_app_window.resizable(False, False)
    add_app_window.grab_set()
    add_app_window.config(cursor=cur, bg="black")
    
    screen_width = add_app_window.winfo_screenwidth()
    screen_height = add_app_window.winfo_screenheight()
    window_width = 720
    window_height = 480
    position_right = int(screen_width/2 - window_width/2)
    position_down = int(screen_height/2 - window_height/2)
    add_app_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
    
    add_app_window.grid_rowconfigure(0, weight=0)
    add_app_window.grid_rowconfigure(1, weight=1)
    add_app_window.grid_rowconfigure(2, weight=1)
    add_app_window.grid_rowconfigure(3, weight=1)
    add_app_window.grid_rowconfigure(4, weight=1)
    add_app_window.grid_rowconfigure(5, weight=0)
    add_app_window.grid_columnconfigure(0, weight=0)
    add_app_window.grid_columnconfigure(1, weight=1)
    add_app_window.grid_columnconfigure(2, weight=1)
    add_app_window.grid_columnconfigure(3, weight=1)
    add_app_window.grid_columnconfigure(4, weight=0)
    
    add_button(add_app_window, "Choose the app", None, lambda: open_file_dialog(), "blue", "blue", 0, 0, 2, 2, 20, 20)
    add_button(add_app_window, "Choose the folder", None, lambda: open_folder_dialog(), "blue", "blue", 0, 0, 3, 2, 20, 20)

def chosse_delete_app():
    delete_window = ctk.CTkToplevel(app)
    delete_window.title("Delete an App")
    delete_window.resizable(False, False)
    delete_window.grab_set()
    delete_window.config(bg="black")

    screen_width = delete_window.winfo_screenwidth()
    screen_height = delete_window.winfo_screenheight()
    window_width = 420
    window_height = 210
    position_right = int(screen_width / 2 - window_width / 2)
    position_down = int(screen_height / 2 - window_height / 2)
    delete_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
    
    for row in range(1, 4):
        for column in range(1, 7):
            button = ctk.CTkButton(
                delete_window,
                text=f"({row}, {column})",
                command=lambda r=row, c=column: [delete_app(r, c),
                delete_window.destroy()],
                width=60,
                height=60
            )
            button.grid(row=row, column=column, padx=5, pady=5)
            button.configure(cursor=cur)
    
def delete_app(row, column):
    buttons = load_saved_buttons()
    for button in buttons:
        if button['row'] == row and button['column'] == column:
            buttons.remove(button)
            save_button_info(file_path=None, icon_path=None, row=row, column=column)

            for widget in app.grid_slaves(): #get all widget
                if widget.grid_info()["row"] == row and widget.grid_info()["column"] == column:
                    widget.destroy()
            break

if __name__ == "__main__":
    try:
        app_init()
        
        #default images
        defaut_img = {
            "img_setting": ImageTk.PhotoImage(Image.open(r"./button_icon/setting.png").resize((100, 100))),
            "img_visualize": ImageTk.PhotoImage(Image.open(r"./button_icon/visualize.png").resize((100, 100))),
            "img_create_shortcut": ImageTk.PhotoImage(Image.open(r"./button_icon/shortcut.png").resize((100, 100))),
            "img_add": ImageTk.PhotoImage(Image.open(r"./button_icon/add.png").resize((100, 100))),
            "img_exit": ImageTk.PhotoImage(Image.open(r"./button_icon/exit.png").resize((100, 100))),
            "img_run_on_startup": ImageTk.PhotoImage(Image.open(r"./button_icon/run_on_startup.png").resize((100, 100))),
            "img_app_default" : ImageTk.PhotoImage(Image.open(r"./button_icon/default_app.png").resize((50,50))),
            "img_delete_app": ImageTk.PhotoImage(Image.open(r"./button_icon/delete_app.png").resize((100, 100))),
            "img_change_resolution": ImageTk.PhotoImage(Image.open(r"./button_icon/change_resolution.png").resize((100, 100)))
        }
        
        #add some default buttons
        #setting button
        add_button(app, None, defaut_img.get("img_setting") , lambda: setting_init(), "black", "black", 0, 0, 0, 7, 20, 20)
        
        #view visualize grid button
        #add_button(app, None ,defaut_img.get("img_visualize") , lambda: visualize_grid(), "black", "black", 0, 0, 0, 0, 20, 20)
        
        #delete app button
        add_button(app, None, defaut_img.get("img_delete_app"),lambda: chosse_delete_app(), "black", "black", 0, 0, 0, 0, 20, 20)
        
        #add button
        add_button(app, None, defaut_img.get("img_add"), lambda: add_app(), "black", "black", 0, 0, 4, 0, 20, 20)
        #exit button
        add_button(app, None, defaut_img.get("img_exit"), app.destroy, "black", "black", 0, 0, 4, 7, 20, 20)

        restore_button()

        app.mainloop()
    except KeyError: #resolution.json file lost
        with open('bin/resolution.json', 'w') as f:
            json.dump({"width": 1280, "height": 720, "fullscreen": 0}, f, indent=4)
        msb.CTkMessagebox.messagebox(title="Error!", text="Json file error. \nRestart the app to fix", 
                                     sound="on", button_text="OK", size="320x150",
                                     center=True, top=True)
        
    except(json.JSONDecodeError, FileNotFoundError):  #json file error
        with open('bin/resolution.json', 'w') as f:
            json.dump({"width": 1280, "height": 720, "fullscreen": 0}, f, indent=4)
        msb.CTkMessagebox.messagebox(title="Error!", text="Json file error. \nRestart the app to fix", 
                                     sound="on", button_text="OK", size="320x150",
                                     center=True, top=True)