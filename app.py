# Imports
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube

# Constants
HEIGTH = 480
WIDTH = 600
COLORS = {
  "white": "#E4D6A7",
  "red": "#9B2915",
  "blue": "#50A2A7",
  "dark blue": "#3C797C",
}
WIDGETS_MAIN_MENU = {
  "title frame": [],
  "title label": [],
  "main menu frame": [],
  "download button": [],
  "settings button": [],
  "exit button": [],
}
WIDGETS_DOWNLOAD = {
  "bar": [],
  "back button": [],
  "frame title": [],
  "help button": [],
  "download box": [],
  "url label": [],
  "url input": [],
  "found label": [],
  "load button": [],
  "add button": [],
}
WIDGETS_HELP = {
  "bar": [],
  "back button": [],
  "frame title": [],
  "help box": [],
  "help text": [],
}
WIDGETS_SETTINGS = {
  "bar": [],
  "back button": [],
  "frame title": [],
  "settings box": [],
  "dark theme msg": [],
  "save path label": [],
  "path label": [],
  "change path button": [],
}
SONG_URL_LIST = []
SONG_FN_LIST = []
SAVE_PATH = ["./downloads/"]

# Window Settings
root = tk.Tk()
root.iconbitmap('./img/logo.ico')
root.title("Youtube Audio Downloader by salot")
root.geometry(str(WIDTH) + "x" + str(HEIGTH))

# Functions
def reset_frame():
  for widget in root.winfo_children():
    widget.place_forget()

def check_valid_yt_url(url):
  valid_url = "https://www.youtube.com/watch?v="
  
  if url[0:32] == valid_url and len(url) == 43:
    return url
  return False

def check_valid_fn(fn):

  invalid_symbols = ["\\", "/", ":", "*", "?", "<", ">", "|"]
  file_name = list(fn)

  for symb in file_name:
    if symb in invalid_symbols:
      file_name[file_name.index(symb)] = "-"

  return "".join(file_name)

def clear_lists_load_df():
  SONG_URL_LIST.clear()
  SONG_FN_LIST.clear()

  download_frame()

def clear_lists_load_mm():
  SONG_URL_LIST.clear()
  SONG_FN_LIST.clear()

  main_menu_frame()

def change_save_path():
  temp = filedialog.askdirectory(parent=root, title="Save Path", initialdir=SAVE_PATH[0])
  # SAVE_PATH.clear()
  # SAVE_PATH.append(temp)
  SAVE_PATH[0] = temp

  WIDGETS_SETTINGS["path label"][-1].configure(text=SAVE_PATH[0])

# Download Functions
def add_song_to_list(url):
  if check_valid_yt_url(url.get()):
    video = YouTube(url.get())
    WIDGETS_DOWNLOAD["found label"][-1].configure(text="Found: " + video.title)
    url.delete(0, 'end')

    SONG_URL_LIST.append(video)

    WIDGETS_DOWNLOAD["url label"][-1].configure(text="Save as:")
    WIDGETS_DOWNLOAD["add button"][-1].configure(text="Save As", command=lambda: save_as_song(url.get()))
  else:
    WIDGETS_DOWNLOAD["found label"][-1].configure(text="Invalid Url")

def save_as_song(fn):

  WIDGETS_DOWNLOAD["url input"][-1].delete(0, 'end')
  WIDGETS_DOWNLOAD["found label"][-1].configure(text="")

  SONG_FN_LIST.append(check_valid_fn(fn))

  WIDGETS_DOWNLOAD["url label"][-1].configure(text="Enter a url:")
  WIDGETS_DOWNLOAD["add button"][-1].configure(text="Add Song to the List", command=lambda: add_song_to_list(WIDGETS_DOWNLOAD["url input"][-1]))

def download_list():

  if SONG_URL_LIST == [] or SONG_FN_LIST == []:
    return

  for url, fn in zip(SONG_URL_LIST, SONG_FN_LIST):
    url.streams.get_audio_only("mp4").download(output_path=SAVE_PATH[0], filename=fn + ".mp3")

  SONG_URL_LIST.clear()
  SONG_FN_LIST.clear()
  
  WIDGETS_DOWNLOAD["found label"][-1].configure(text="")

# Frames
def main_menu_frame():

  reset_frame()

  # Widgets
  title_frame = tk.Label(master=root,
    bg=COLORS["red"],
  )

  title_label = tk.Label(master=title_frame,
    bg=COLORS["red"],
    bd=5,
    font=("centurty gothic", 32, "bold"),
    fg="white",
    padx=0,
    pady=0,
    text="Youtube Audio Downloader",
  )

  main_menu_frame = tk.Label(master=root,
    bg=COLORS["white"]
  )

  download_button = tk.Button(master=main_menu_frame,
    text="Download",
    activebackground=COLORS["dark blue"],
    activeforeground="white",
    bd=4,
    bg=COLORS["blue"],
    fg="white",
    font=("century gothic", 18),
    padx=0,
    pady=0,
    cursor="hand2",
    command=download_frame
  )

  settings_button = tk.Button(master=main_menu_frame,
    text="Settings",
    activebackground=COLORS["dark blue"],
    activeforeground="white",
    bd=4,
    bg=COLORS["blue"],
    fg="white",
    font=("century gothic", 18),
    padx=0,
    pady=0,
    cursor="hand2",
    command=settings_frame
  )

  exit_button = tk.Button(master=main_menu_frame,
    text="Exit",
    activebackground=COLORS["dark blue"],
    activeforeground="white",
    bd=4,
    bg=COLORS["blue"],
    fg="white",
    font=("century gothic", 18),
    padx=0,
    pady=0,
    cursor="hand2",
    command=root.destroy
  )

  # List
  WIDGETS_MAIN_MENU["title frame"].append(title_frame)
  WIDGETS_MAIN_MENU["title label"].append(title_label)
  WIDGETS_MAIN_MENU["main menu frame"].append(main_menu_frame)
  WIDGETS_MAIN_MENU["download button"].append(download_button)
  WIDGETS_MAIN_MENU["settings button"].append(settings_button)
  WIDGETS_MAIN_MENU["exit button"].append(exit_button)

  # Place
  WIDGETS_MAIN_MENU["title frame"][-1].place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.2)
  WIDGETS_MAIN_MENU["title label"][-1].place(relx=0, rely=0, relwidth=1, relheight=1)
  WIDGETS_MAIN_MENU["main menu frame"][-1].place(relx=0.01, rely=0.22, relwidth=0.98, relheight=0.77)
  WIDGETS_MAIN_MENU["download button"][-1].place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.15)
  WIDGETS_MAIN_MENU["settings button"][-1].place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.15)
  WIDGETS_MAIN_MENU["exit button"][-1].place(relx=0.2, rely=0.5, relwidth=0.6, relheight=0.15)

def download_frame():

  reset_frame()

  bar = tk.Frame(master=root,
    bg=COLORS["red"]
  )

  back_button = tk.Button(master=bar,
    text="<",
    activebackground=COLORS["dark blue"],
    activeforeground="white",
    bd=2,
    bg=COLORS["blue"],
    fg="white",
    font=("century gothic", 10, "bold"),
    padx=0,
    pady=0,
    cursor="hand2",
    command=clear_lists_load_mm,
  )

  frame_title = tk.Label(master=bar,
    bg=COLORS["red"],
    bd=5,
    font=("centurty gothic", 16),
    fg="#ffffff",
    padx=0,
    pady=0,
    text="Download",
    justify='left'
  )

  help_button = tk.Button(master=bar,
    text="?",
    activebackground=COLORS["dark blue"],
    activeforeground="white",
    bd=2,
    bg=COLORS["blue"],
    fg="white",
    font=("century gothic", 10, "bold"),
    padx=0,
    pady=0,
    cursor="hand2",
    command=help_frame,
  )

  download_box = tk.Frame(master=root,
    bg=COLORS["white"]
  )

  url_label = tk.Label(master=download_box,
    bg=COLORS["white"],
    bd=5,
    font=("centurty gothic", 12),
    fg=COLORS["red"],
    padx=0,
    pady=0,
    text="Enter a url:",
    justify='left',
    anchor='w'
  )

  url_input = tk.Entry(master=download_box,
    bg=COLORS["white"],
    bd=3,
    font=("centurty gothic", 14),
    fg=COLORS["red"],
    relief='groove'
  )

  found_label = tk.Label(master=download_box,
    bg=COLORS["white"],
    bd=5,
    font=("centurty gothic", 14, "bold"),
    fg=COLORS["red"],
    padx=0,
    pady=0,
    justify='left',
    anchor='w'
  )

  load_button = tk.Button(master=download_box,
    text="Download List",
    activebackground=COLORS["dark blue"],
    activeforeground="white",
    bd=4,
    bg=COLORS["blue"],
    fg="white",
    font=("century gothic", 12),
    padx=0,
    pady=0,
    cursor="hand2",
    command=download_list
  )

  add_button = tk.Button(master=download_box,
    text="Add Song to the List",
    activebackground=COLORS["dark blue"],
    activeforeground="white",
    bd=4,
    bg=COLORS["blue"],
    fg="white",
    font=("century gothic", 12),
    padx=0,
    pady=0,
    cursor="hand2",
    command=lambda: add_song_to_list(url_input)
  )

  # List
  WIDGETS_DOWNLOAD["bar"].append(bar)
  WIDGETS_DOWNLOAD["back button"].append(back_button)
  WIDGETS_DOWNLOAD["frame title"].append(frame_title)
  WIDGETS_DOWNLOAD["help button"].append(help_button)
  WIDGETS_DOWNLOAD["download box"].append(download_box)
  WIDGETS_DOWNLOAD["url label"].append(url_label)
  WIDGETS_DOWNLOAD["url input"].append(url_input)
  WIDGETS_DOWNLOAD["found label"].append(found_label)
  WIDGETS_DOWNLOAD["load button"].append(load_button)
  WIDGETS_DOWNLOAD["add button"].append(add_button)

  # Place
  WIDGETS_DOWNLOAD["bar"][-1].place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.08)
  WIDGETS_DOWNLOAD["back button"][-1].place(relx=0.0075, rely=0.1, relwidth=0.05, relheight=0.8)
  WIDGETS_DOWNLOAD["frame title"][-1].place(relx=0.07, rely=0, relheight=1)
  WIDGETS_DOWNLOAD["help button"][-1].place(relx=0.945, rely=0.1, relwidth=0.05, relheight=0.8)
  WIDGETS_DOWNLOAD["download box"][-1].place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.89)
  WIDGETS_DOWNLOAD["url label"][-1].place(relx=0.5, rely=0.17, relwidth=0.75, relheight=0.05, anchor='center')
  WIDGETS_DOWNLOAD["url input"][-1].place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.1, anchor='center')
  WIDGETS_DOWNLOAD["found label"][-1].place(relx=0.5, rely=0.35, relwidth=0.75, relheight=0.08, anchor='center')
  WIDGETS_DOWNLOAD["load button"][-1].place(relx=0.3, rely=0.6, relwidth=0.3, relheight=0.1, anchor='center')
  WIDGETS_DOWNLOAD["add button"][-1].place(relx=0.7, rely=0.6, relwidth=0.3, relheight=0.1, anchor='center')

def help_frame():

  reset_frame()

  bar = tk.Frame(master=root,
    bg=COLORS["red"]
  )

  back_button = tk.Button(master=bar,
    text="<",
    activebackground=COLORS["dark blue"],
    activeforeground="white",
    bd=2,
    bg=COLORS["blue"],
    fg="white",
    font=("century gothic", 10, "bold"),
    padx=0,
    pady=0,
    cursor="hand2",
    command=clear_lists_load_df,
  )

  frame_title = tk.Label(master=bar,
    bg=COLORS["red"],
    bd=5,
    font=("centurty gothic", 16),
    fg="#ffffff",
    padx=0,
    pady=0,
    text="Help",
    justify='left'
  )

  help_box = tk.Frame(master=root,
    bg=COLORS["white"]
  )

  ht = '''
      1. Go to Youtube and copy the url of the song you want to 
          download
      2. Paste the url in the input field
      3. Click the "Add Song to the List" button
      4. Enter a name for the .mp3 file
      5. Click the "Save As" button
      6. Click the "Download List" button to download the song 
          you've just inserted into the list
          (or keep adding songs to the list)
      
      NOTE: If for whatever reason you leave the "Download"
                   window, all the songs you've inserted into the list
                   will be deleted!
    '''
  help_text = tk.Label(master=help_box,
    bg=COLORS["white"],
    bd=5,
    font=("centurty gothic", 12),
    fg=COLORS["red"],
    padx=0,
    pady=0,
    text=ht,
    justify='left'
  )

  # List
  WIDGETS_HELP["bar"].append(bar)
  WIDGETS_HELP["back button"].append(back_button)
  WIDGETS_HELP["frame title"].append(frame_title)
  WIDGETS_HELP["help box"].append(help_box)
  WIDGETS_HELP["help text"].append(help_text)

  # Place
  WIDGETS_HELP["bar"][-1].place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.08)
  WIDGETS_HELP["back button"][-1].place(relx=0.0075, rely=0.1, relwidth=0.05, relheight=0.8)
  WIDGETS_HELP["frame title"][-1].place(relx=0.07, rely=0, relheight=1)
  WIDGETS_HELP["help box"][-1].place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.89)
  WIDGETS_HELP["help text"][-1].place(relx=0.5, rely=0.4, relwidth=1, relheight=1, anchor="center")

def settings_frame():

  reset_frame()

  # Widgets 
  bar = tk.Frame(master=root,
    bg=COLORS["red"]
  )

  back_button = tk.Button(master=bar,
    text="<",
    activebackground=COLORS["dark blue"],
    activeforeground="white",
    bd=2,
    bg=COLORS["blue"],
    fg="white",
    font=("century gothic", 10, "bold"),
    padx=0,
    pady=0,
    cursor="hand2",
    command=main_menu_frame,
  )

  frame_title = tk.Label(master=bar,
    bg=COLORS["red"],
    bd=5,
    font=("centurty gothic", 16),
    fg="#ffffff",
    padx=0,
    pady=0,
    text="Settings",
    justify='left'
  )

  settings_box = tk.Frame(master=root,
    bg=COLORS["white"]
  )

  dark_theme_msg = tk.Label(settings_box, 
    text="Dark Theme Coming Soon...",
    bg=COLORS["white"],
    font=("century gothic", 22)
  )

  save_path_label = tk.Label(master=settings_box,
    bg=COLORS["white"],
    bd=5,
    font=("centurty gothic", 14),
    fg=COLORS["red"],
    padx=0,
    pady=0,
    text="Save Folder:",
    justify='left'
  )

  path_input = tk.Label(master=settings_box,
    bg=COLORS["white"],
    bd=5,
    font=("centurty gothic", 14),
    fg=COLORS["blue"],
    padx=0,
    pady=0,
    text=SAVE_PATH,
    anchor='w'
  )

  change_path_button = tk.Button(master=settings_box,
    text="Change",
    activebackground=COLORS["dark blue"],
    activeforeground="white",
    bd=2,
    bg=COLORS["blue"],
    fg="white",
    font=("century gothic", 10, "bold"),
    padx=0,
    pady=0,
    cursor="hand2",
    command=change_save_path,
  )

  # List
  WIDGETS_SETTINGS["bar"].append(bar)
  WIDGETS_SETTINGS["back button"].append(back_button)
  WIDGETS_SETTINGS["frame title"].append(frame_title)
  WIDGETS_SETTINGS["settings box"].append(settings_box)
  WIDGETS_SETTINGS["dark theme msg"].append(dark_theme_msg)
  WIDGETS_SETTINGS["save path label"].append(save_path_label)
  WIDGETS_SETTINGS["path label"].append(path_input)
  WIDGETS_SETTINGS["change path button"].append(change_path_button)

  # Place
  WIDGETS_SETTINGS["bar"][-1].place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.08)
  WIDGETS_SETTINGS["back button"][-1].place(relx=0.0075, rely=0.1, relwidth=0.05, relheight=0.8)
  WIDGETS_SETTINGS["frame title"][-1].place(relx=0.07, rely=0, relheight=1)
  WIDGETS_SETTINGS["settings box"][-1].place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.89)
  WIDGETS_SETTINGS["save path label"][-1].place(relx=0.05, rely=0.2, relwidth=0.2)
  WIDGETS_SETTINGS["path label"][-1].place(relx=0.25, rely=0.2, relwidth=0.6)
  WIDGETS_SETTINGS["change path button"][-1].place(relx=0.85, rely=0.2, relheight=0.075)
  WIDGETS_SETTINGS["dark theme msg"][-1].place(anchor='center', relx=0.5, rely=0.8)



# Loop
main_menu_frame()
root.mainloop()