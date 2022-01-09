# Imports
import customtkinter as ctk
import json
from tkinter import filedialog, PhotoImage
from pytube import YouTube, Playlist

### Constants ###

HEIGHT = 480
WIDTH = 600

SONG_URL = []
SONG_ERROR = []

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
  "download box": [],
  "download song": [],
  "download list": [],
}
WIDGETS_DAS = {
  "bar": [],
  "back button": [],
  "frame title": [],
  "download box": [],
  "url label": [],
  "save as label": [],
  "url input": [],
  "found label": [],
  "load button": [],
  "save as button": [],
}
WIDGETS_DAP = {
  "bar": [],
  "back button": [],
  "frame title": [],
  "download box": [],
  "url label": [],
  "save as label": [],
  "url input": [],
  "found label": [],
  "load button": [],
  "save as button": [],
}
WIDGETS_SETTINGS = {
  "bar": [],
  "back button": [],
  "frame title": [],
  "settings box": [],
  "save path label": [],
  "path label": [],
  "unhovered change path button dark": [],
  "unhovered change path button light": [],
  "hovered change path button": [],
  "theme label": [],
  "theme frame button": [],
  "theme button": [],
}
SETTINGS = {
  "theme": "",
  "save path": ""
}

COLORS = {
  "background": ("#D4D5D6", "#3f3f3f"),
  "surface 1": ("#E4D6A7", "#1D1D1D"),
  "surface 2": ("#C7B989", "#333333"),
  "primary": ("#9B2915", "#9B2915"),
  "secondary": ("#50A2A7", "#50A2A7"),
  "text white": ("#E4D6A7", "#E4D6A7"),
  "text red": ("#9B2915", "#9B2915"),
  "text blue": ("#50A2A7", "#50A2A7"),
  "text red blue": ("#9B2915", "#50A2A7"),
  "text blue red": ("#50A2A7", "#9B2915"),
  "highlight blue dark 1": ("#3C797C", "#3C797C"),
  "highlight blue dark 2": ("#10666B", "#10666B"),
}

### Window Settings ###

root = ctk.CTk()
root.iconbitmap('./img/logo.ico')
root.title("youtube-audio-downloader by salot")
root.geometry(str(WIDTH) + "x" + str(HEIGHT))

### Functions ###

# General
def reset_frame():
  for widget in root.winfo_children():
    widget.place_forget()

def back_reset(frame):
  SONG_URL.clear()
  SONG_ERROR.clear()
  if frame == "main menu":
    main_menu_frame()
  elif frame == "download":
    download_frame()

def load_settings():
  f = open("settings.json")
  settings_data = json.load(f)
  f.close()

  SETTINGS["theme"] = settings_data["theme"]
  SETTINGS["save path"] = settings_data["save path"]

  ctk.set_appearance_mode(SETTINGS["theme"])

def save_settings():
  with open("settings.json", "w") as outfile:
    json.dump(SETTINGS, outfile, indent=2)

def toggle_theme():
  if ctk.get_appearance_mode() == "Light":
    WIDGETS_SETTINGS["unhovered change path button light"][-1].place_forget()
    WIDGETS_SETTINGS["unhovered change path button dark"][-1].place(relx=0.908, rely=0.2)
    WIDGETS_SETTINGS["theme button"][-1].configure(fg_color=COLORS["text blue"])
    WIDGETS_SETTINGS["theme button"][-1].place_forget()
    WIDGETS_SETTINGS["theme button"][-1].place(relx=0.92, rely=0.2854)
    SETTINGS["theme"] = "dark"
    ctk.set_appearance_mode("dark")
  else:
    WIDGETS_SETTINGS["unhovered change path button dark"][-1].place_forget()
    WIDGETS_SETTINGS["unhovered change path button light"][-1].place(relx=0.908, rely=0.2)
    WIDGETS_SETTINGS["theme button"][-1].configure(fg_color="gray60")
    WIDGETS_SETTINGS["theme button"][-1].place_forget()
    WIDGETS_SETTINGS["theme button"][-1].place(relx=0.889, rely=0.2854)
    SETTINGS["theme"] = "light"
    ctk.set_appearance_mode("light")

  save_settings()

def change_save_path():
  temp = filedialog.askdirectory(parent=root, title="save path", initialdir=SETTINGS["save path"])
  if temp:
    SETTINGS["save path"] =  temp
    WIDGETS_SETTINGS["path label"][-1].configure(text=SETTINGS["save path"])
    save_settings()

def check_valid_fn(fn):
  invalid_symbols = ["\\", "/", ":", "*", '"', "?", "<", ">", "|"]
  file_name = list(fn)

  for symb in file_name:
    if symb in invalid_symbols:
      file_name[file_name.index(symb)] = "-"

  return "".join(file_name)

# Change Path Icon Hover Effect
def hover_change_button(self):
  if ctk.get_appearance_mode() == "Dark":
    WIDGETS_SETTINGS["unhovered change path button dark"][-1].place_forget()
  else:
    WIDGETS_SETTINGS["unhovered change path button light"][-1].place_forget()
  WIDGETS_SETTINGS["hovered change path button"][-1].place(relx=0.908, rely=0.2)

def unhover_change_button(self):
  if ctk.get_appearance_mode() == "Dark":
    WIDGETS_SETTINGS["unhovered change path button dark"][-1].place(relx=0.908, rely=0.2)
  else:
    WIDGETS_SETTINGS["unhovered change path button light"][-1].place(relx=0.908, rely=0.2)
  WIDGETS_SETTINGS["hovered change path button"][-1].place_forget()

# Song Functions
def load_song():
  url = WIDGETS_DAS["url input"][-1]
  if check_valid_song_url(url.get()):
    try:
      video = YouTube(url.get())
      url.delete(0, 'end')

      SONG_URL.append(video)
      WIDGETS_DAS["url label"][-1].place_forget()
      WIDGETS_DAS["save as label"][-1].place(relx=0.05, rely=0.14)
      WIDGETS_DAS["found label"][-1].configure(text=video.title, width=540, fg_color=COLORS["surface 2"])

      WIDGETS_DAS["load button"][-1].place_forget()
      WIDGETS_DAS["save as button"][-1].place(relx=0.5, rely=0.7, anchor='center')
    except:
      WIDGETS_DAS["found label"][-1].configure(text="something went wrong\n\ntry again with a different url", fg_color=COLORS["surface 2"])
  else:
    WIDGETS_DAS["found label"][-1].configure(text="invalid url", fg_color=COLORS["surface 2"])

def save_as_song():
  fn = WIDGETS_DAS["url input"][-1].get()
  WIDGETS_DAS["url input"][-1].delete(0, 'end')

  WIDGETS_DAS["found label"][-1].configure(text="", fg_color=COLORS["surface 1"])
  WIDGETS_DAS["url label"][-1].place(relx=0.05, rely=0.14)
  WIDGETS_DAS["save as label"][-1].place_forget()
  WIDGETS_DAS["save as button"][-1].place_forget()
  WIDGETS_DAS["load button"][-1].place(relx=0.5, rely=0.7, anchor='center')
  
  try:
    SONG_URL[0].streams.get_audio_only("mp4").download(output_path=SETTINGS["save path"], filename=check_valid_fn(fn) + ".mp3")
  except:
    WIDGETS_DAS["found label"][-1].configure(text="\"" + SONG_URL[-1].title + "\" could not be downloaded\n\nTry a different url", fg_color=COLORS["surface 2"])

  SONG_URL.clear()

def check_valid_song_url(url):
  valid_url = "https://www.youtube.com/watch?v="
  
  if url[0:32] == valid_url and len(url) == 43:
    return url
  return False

# List Functions
def load_list():
  url = WIDGETS_DAP["url input"][-1]
  if check_valid_list_url(url.get()):
    try:
      list = Playlist(url.get())
      url.delete(0, 'end')

      SONG_URL.append(list.videos)

      WIDGETS_DAP["url label"][-1].place_forget()
      WIDGETS_DAP["save as label"][-1].place(relx=0.05, rely=0.14)

      WIDGETS_DAP["found label"][-1].configure(text=list.title + " (" + str(len(list)) + " songs)", fg_color=COLORS["surface 2"])
      WIDGETS_DAP["found label"][-1].text_label.place(relx=0.5, rely=0.5, anchor='center')

      WIDGETS_DAP["load button"][-1].place_forget()
      WIDGETS_DAP["save as button"][-1].place(relx=0.5, rely=0.7, anchor='center')
    except:
      WIDGETS_DAP["found label"][-1].configure(text="", fg_color=COLORS["surface 2"])
      WIDGETS_DAP["found label"][-1].configure(text="something went wrong\n\nremember, the playlist must be public or unlisted") 
  else:
    WIDGETS_DAP["found label"][-1].configure(text="", fg_color=COLORS["surface 2"])
    WIDGETS_DAP["found label"][-1].configure(text="invalid url")

def save_as_list():
  fn = WIDGETS_DAP["url input"][-1].get()
  WIDGETS_DAP["url input"][-1].delete(0, 'end')
  WIDGETS_DAP["found label"][-1].configure(text="", fg_color=COLORS["surface 1"])
  WIDGETS_DAP["url label"][-1].place(relx=0.05, rely=0.14)

  WIDGETS_DAP["save as label"][-1].place_forget()
  WIDGETS_DAP["save as button"][-1].place_forget()
  WIDGETS_DAP["load button"][-1].place(relx=0.5, rely=0.7, anchor='center')
    
  for video in SONG_URL[-1]:
    try:
      video.streams.get_audio_only("mp4").download(output_path=SETTINGS["save path"] + "/" + check_valid_fn(fn), filename=check_valid_fn(video.title) + ".mp3")
    except:
      SONG_ERROR.append(video.title)

    if SONG_ERROR != []:
      txt = "these songs could not be downloaded:\n\n"

      for song in SONG_ERROR:
        txt += song + "\n"

      WIDGETS_DAP["found label"][-1].configure(text=txt, fg_color=COLORS["surface 2"])
      WIDGETS_DAP["found label"][-1].text_label.place(relx=0.5, rely=0.0, anchor='n')

  SONG_URL.clear()
  SONG_ERROR.clear()

def check_valid_list_url(url):
  valid_url = "https://www.youtube.com/playlist?list="
  
  if url[0:38] == valid_url and len(url) == 72:
    return url

  return False

# Frames
def main_menu_frame():
  reset_frame()

  # Widgets
  title_frame = ctk.CTkFrame(master=root)

  title_label = ctk.CTkLabel(master=title_frame,
    text="youtube-audio-downloader",
    corner_radius=8,
    fg_color=COLORS["primary"],
    text_font=("centurty gothic", 32, "bold"),
    text_color=COLORS["text white"],
    width=WIDTH*0.98,
    height=HEIGHT*0.2
  )

  main_menu_frame = ctk.CTkFrame(master=root,
    fg_color=COLORS["surface 1"],
    corner_radius=8,
    width=WIDTH*0.98,
    height=HEIGHT*0.7625
  )

  download_button = ctk.CTkButton(master=main_menu_frame,
    text="download",
    command=download_frame,
    corner_radius=5,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 18, "bold"),
    hover=True,
    width=WIDTH*0.5,
    height=HEIGHT*0.1,
    cursor="hand2",
  )

  settings_button = ctk.CTkButton(master=main_menu_frame,
    text="settings",
    command=settings_frame,
    corner_radius=5,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 18, "bold"),
    hover=True,
    width=WIDTH*0.5,
    height=HEIGHT*0.1,
    cursor="hand2"
  )

  exit_button = ctk.CTkButton(master=main_menu_frame,
    text="exit",
    command=root.destroy,
    corner_radius=5,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 18, "bold"),
    hover=True,
    width=WIDTH*0.5,
    height=HEIGHT*0.1,
    cursor="hand2"
  )

  # List
  WIDGETS_MAIN_MENU["title frame"].append(title_frame)
  WIDGETS_MAIN_MENU["title label"].append(title_label)
  WIDGETS_MAIN_MENU["main menu frame"].append(main_menu_frame)
  WIDGETS_MAIN_MENU["download button"].append(download_button)
  WIDGETS_MAIN_MENU["settings button"].append(settings_button)
  WIDGETS_MAIN_MENU["exit button"].append(exit_button)

  # Place
  WIDGETS_MAIN_MENU["title frame"][-1].place(relx=0.01, rely=0.0125)
  WIDGETS_MAIN_MENU["title label"][-1].pack()
  WIDGETS_MAIN_MENU["main menu frame"][-1].place(relx=0.01, rely=0.225)
  WIDGETS_MAIN_MENU["download button"][-1].place(relx=0.5, rely=0.25, anchor="center")
  WIDGETS_MAIN_MENU["settings button"][-1].place(relx=0.5, rely=0.4, anchor="center")
  WIDGETS_MAIN_MENU["exit button"][-1].place(relx=0.5, rely=0.55, anchor="center")

def download_frame():
  reset_frame()

  bar = ctk.CTkFrame(master=root,
    fg_color=COLORS["primary"],
    corner_radius=8,
    width=WIDTH*0.98,
    height=HEIGHT*0.1
  )

  back_button = ctk.CTkButton(master=bar,
    text="",
    image=PhotoImage(file="./img/back-button.png"),
    command=lambda: back_reset("main menu"),
    corner_radius=18,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 10, "bold"),
    hover=True,
    width=36,
    height=36,
    cursor="hand2"
  )

  frame_title = ctk.CTkLabel(master=bar,
    text="download",
    corner_radius=0,
    fg_color=COLORS["primary"],
    text_font=("centurty gothic", 18),
    text_color=COLORS["text white"],
    width=200,
    height=36,
  )

  download_box = ctk.CTkFrame(master=root,
    fg_color=COLORS["surface 1"],
    corner_radius=8,
    width=WIDTH*0.98,
    height=HEIGHT*0.8625
  )

  download_a_song = ctk.CTkButton(master=download_box,
    text="download a song",
    command=download_a_song_frame,
    corner_radius=5,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 18, "bold"),
    hover=True,
    width=WIDTH*0.5,
    height=HEIGHT*0.1,
    cursor="hand2",
  )

  download_a_list = ctk.CTkButton(master=download_box,
    text="download a playlist",
    command=download_a_list_frame,
    corner_radius=5,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 18, "bold"),
    hover=True,
    width=WIDTH*0.5,
    height=HEIGHT*0.1,
    cursor="hand2",
  )
  
  # # List
  WIDGETS_DOWNLOAD["bar"].append(bar)
  WIDGETS_DOWNLOAD["back button"].append(back_button)
  WIDGETS_DOWNLOAD["frame title"].append(frame_title)
  WIDGETS_DOWNLOAD["download box"].append(download_box)
  WIDGETS_DOWNLOAD["download song"].append(download_a_song)
  WIDGETS_DOWNLOAD["download list"].append(download_a_list)

  # # Place
  WIDGETS_DOWNLOAD["bar"][-1].place(relx=0.01, rely=0.0125)
  WIDGETS_DOWNLOAD["back button"][-1].place(relx=0.01, rely=0.125)
  WIDGETS_DOWNLOAD["frame title"][-1].place(relx=0.082, rely=0.125)
  WIDGETS_DOWNLOAD["frame title"][-1].text_label.place(relx=0, anchor="w")
  WIDGETS_DOWNLOAD["download box"][-1].place(relx=0.01, rely=0.125)
  WIDGETS_DOWNLOAD["download song"][-1].place(relx=0.5, rely=0.35, anchor="center")
  WIDGETS_DOWNLOAD["download list"][-1].place(relx=0.5, rely=0.5, anchor="center")

def download_a_song_frame():
  reset_frame()

  bar = ctk.CTkFrame(master=root,
    fg_color=COLORS["primary"],
    corner_radius=8,
    width=WIDTH*0.98,
    height=HEIGHT*0.1
  )

  back_button = ctk.CTkButton(master=bar,
    text="",
    image=PhotoImage(file="./img/back-button.png"),
    command=lambda: back_reset("download"),
    corner_radius=18,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 10, "bold"),
    hover=True,
    width=36,
    height=36,
    cursor="hand2"
  )

  frame_title = ctk.CTkLabel(master=bar,
    text="download a song",
    corner_radius=0,
    fg_color=COLORS["primary"],
    text_font=("centurty gothic", 18),
    text_color=COLORS["text white"],
    width=200,
    height=36,
  )

  download_box = ctk.CTkFrame(master=root,
    fg_color=COLORS["surface 1"],
    corner_radius=8,
    width=WIDTH*0.98,
    height=HEIGHT*0.8625
  )

  url_label = ctk.CTkLabel(master=download_box,
    text="enter the url of a song:",
    text_font=("centurty gothic", 12, "bold"),
    text_color=COLORS["text blue red"],
    fg_color=COLORS["surface 1"],
    corner_radius=0,
    width=200
  )

  save_as_label = ctk.CTkLabel(master=download_box,
    text="save as:",
    text_font=("centurty gothic", 12, "bold"),
    text_color=COLORS["text blue red"],
    fg_color=COLORS["surface 1"],
    corner_radius=0,
    width=200
  )

  url_input = ctk.CTkEntry(master=download_box,
    fg_color=COLORS["surface 2"],
    corner_radius=5,
    bg_color=COLORS["surface 1"],
    font=("centurty gothic", 14),
    text_color=COLORS["text red blue"],
    width=540,
    height=36,
  )

  found_label = ctk.CTkLabel(master=download_box,
    text="",
    text_font=("centurty gothic", 12),
    text_color=COLORS["text red blue"],
    fg_color=COLORS["surface 1"],
    width=540,
    height=80,
    wraplength=540,
    justify="center",
    corner_radius=5,
  )

  load_button = ctk.CTkButton(master=download_box,
    text="load song",
    command=load_song,
    corner_radius=5,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 18, "bold"),
    hover=True,
    width=WIDTH*0.5,
    height=HEIGHT*0.1,
    cursor="hand2",
  )
  
  save_as_button = ctk.CTkButton(master=download_box,
    text="save song",
    command=save_as_song,
    corner_radius=5,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 18, "bold"),
    hover=True,
    width=WIDTH*0.5,
    height=HEIGHT*0.1,
    cursor="hand2",
  )

  # List
  WIDGETS_DAS["bar"].append(bar)
  WIDGETS_DAS["back button"].append(back_button)
  WIDGETS_DAS["frame title"].append(frame_title)
  WIDGETS_DAS["download box"].append(download_box)
  WIDGETS_DAS["url label"].append(url_label)
  WIDGETS_DAS["save as label"].append(save_as_label)
  WIDGETS_DAS["url input"].append(url_input)
  WIDGETS_DAS["found label"].append(found_label)
  WIDGETS_DAS["load button"].append(load_button)
  WIDGETS_DAS["save as button"].append(save_as_button)

  # Place
  WIDGETS_DAS["bar"][-1].place(relx=0.01, rely=0.0125)
  WIDGETS_DAS["back button"][-1].place(relx=0.01, rely=0.125)
  WIDGETS_DAS["frame title"][-1].place(relx=0.082, rely=0.125)
  WIDGETS_DAS["frame title"][-1].text_label.place(relx=0, anchor="w")
  WIDGETS_DAS["download box"][-1].place(relx=0.01, rely=0.125)
  WIDGETS_DAS["url label"][-1].place(relx=0.05, rely=0.14)
  WIDGETS_DAS["url label"][-1].text_label.place(relx=0, anchor="w")
  WIDGETS_DAS["save as label"][-1].text_label.place(relx=0, anchor="w")
  WIDGETS_DAS["url input"][-1].place(relx=0.5, rely=0.25, anchor='center')
  WIDGETS_DAS["found label"][-1].place(relx=0.5, rely=0.41, anchor='center')
  WIDGETS_DAS["found label"][-1].text_label.place(relx=0.5, rely=0.5, relwidth=1, anchor="center")
  WIDGETS_DAS["load button"][-1].place(relx=0.5, rely=0.7, anchor='center')

def download_a_list_frame():
  reset_frame()

  bar = ctk.CTkFrame(master=root,
    fg_color=COLORS["primary"],
    corner_radius=8,
    width=WIDTH*0.98,
    height=HEIGHT*0.1
  )

  back_button = ctk.CTkButton(master=bar,
    text="",
    image=PhotoImage(file="./img/back-button.png"),
    command=lambda: back_reset("download"),
    corner_radius=18,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 10, "bold"),
    hover=True,
    width=36,
    height=36,
    cursor="hand2"
  )

  frame_title = ctk.CTkLabel(master=bar,
    text="download a playlist",
    corner_radius=0,
    fg_color=COLORS["primary"],
    text_font=("centurty gothic", 18),
    text_color=COLORS["text white"],
    width=220,
    height=36,
  )

  download_box = ctk.CTkFrame(master=root,
    fg_color=COLORS["surface 1"],
    corner_radius=8,
    width=WIDTH*0.98,
    height=HEIGHT*0.8625
  )

  url_label = ctk.CTkLabel(master=download_box,
    text="enter the url of a playlist:",
    text_font=("centurty gothic", 12, "bold"),
    text_color=COLORS["text blue red"],
    fg_color=COLORS["surface 1"],
    corner_radius=0,
    width=200
  )

  save_as_label = ctk.CTkLabel(master=download_box,
    text="save as:",
    text_font=("centurty gothic", 12, "bold"),
    text_color=COLORS["text blue red"],
    fg_color=COLORS["surface 1"],
    corner_radius=0,
    width=200
  )

  url_input = ctk.CTkEntry(master=download_box,
    fg_color=COLORS["surface 2"],
    corner_radius=5,
    bg_color=COLORS["surface 1"],
    font=("centurty gothic", 14),
    text_color=COLORS["text red blue"],
    width=540,
    height=36,
  )

  found_label = ctk.CTkLabel(master=download_box,
    text="",
    text_font=("centurty gothic", 12),
    text_color=COLORS["text red blue"],
    fg_color=COLORS["surface 1"],
    width=540,
    height=80,
    wraplength=540,
    justify="center",
    corner_radius=5,
  )

  load_button = ctk.CTkButton(master=download_box,
    text="load playlist",
    command=load_list,
    corner_radius=5,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 18, "bold"),
    hover=True,
    width=WIDTH*0.5,
    height=HEIGHT*0.1,
    cursor="hand2",
  )
  
  save_as_button = ctk.CTkButton(master=download_box,
    text="save playlist",
    command=save_as_list,
    corner_radius=5,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 18, "bold"),
    hover=True,
    width=WIDTH*0.5,
    height=HEIGHT*0.1,
    cursor="hand2",
  )

  # List
  WIDGETS_DAP["bar"].append(bar)
  WIDGETS_DAP["back button"].append(back_button)
  WIDGETS_DAP["frame title"].append(frame_title)
  WIDGETS_DAP["download box"].append(download_box)
  WIDGETS_DAP["url label"].append(url_label)
  WIDGETS_DAP["save as label"].append(save_as_label)
  WIDGETS_DAP["url input"].append(url_input)
  WIDGETS_DAP["found label"].append(found_label)
  WIDGETS_DAP["load button"].append(load_button)
  WIDGETS_DAP["save as button"].append(save_as_button)

  # Place
  WIDGETS_DAP["bar"][-1].place(relx=0.01, rely=0.0125)
  WIDGETS_DAP["back button"][-1].place(relx=0.01, rely=0.125)
  WIDGETS_DAP["frame title"][-1].place(relx=0.082, rely=0.125)
  WIDGETS_DAP["frame title"][-1].text_label.place(relx=0, anchor="w")
  WIDGETS_DAP["download box"][-1].place(relx=0.01, rely=0.125)
  WIDGETS_DAP["url label"][-1].place(relx=0.05, rely=0.14)
  WIDGETS_DAP["url label"][-1].text_label.place(relx=0, anchor="w")
  WIDGETS_DAP["save as label"][-1].text_label.place(relx=0, anchor="w")
  WIDGETS_DAP["url input"][-1].place(relx=0.5, rely=0.25, anchor='center')
  WIDGETS_DAP["found label"][-1].place(relx=0.5, rely=0.41, anchor='center')
  WIDGETS_DAP["load button"][-1].place(relx=0.5, rely=0.7, anchor='center')

def settings_frame():
  reset_frame()

  # Widgets 
  bar = ctk.CTkFrame(master=root,
    fg_color=COLORS["primary"],
    corner_radius=8,
    width=WIDTH*0.98,
    height=HEIGHT*0.1
  )

  back_button = ctk.CTkButton(master=bar,
    text="",
    image=PhotoImage(file="./img/back-button.png"),
    command=lambda: back_reset("main menu"),
    corner_radius=18,
    border_width=2,
    border_color=COLORS["highlight blue dark 2"],
    fg_color=COLORS["secondary"],
    hover_color=COLORS["highlight blue dark 1"],
    text_color=COLORS["text white"],
    text_font=("century gothic", 10, "bold"),
    hover=True,
    width=36,
    height=36,
    cursor="hand2"
  )

  frame_title = ctk.CTkLabel(master=bar,
    text="settings",
    corner_radius=0,
    fg_color=COLORS["primary"],
    text_font=("centurty gothic", 18),
    text_color=COLORS["text white"],
    width=200,
    height=36,
  )

  settings_box = ctk.CTkFrame(master=root,
    fg_color=COLORS["surface 1"],
    corner_radius=8,
    width=WIDTH*0.98,
    height=HEIGHT*0.8625
  )

  save_path_label = ctk.CTkLabel(master=settings_box,
    text="save path:",
    corner_radius=0,
    fg_color=COLORS["surface 1"],
    text_font=("centurty gothic", 14),
    text_color=COLORS["text red"],
    width=120,
    height=25,
  )

  path_label = ctk.CTkLabel(master=settings_box,
    text=SETTINGS["save path"],
    corner_radius=0,
    bg_color="blue",
    fg_color=COLORS["surface 1"],
    text_font=("centurty gothic", 14),
    text_color=COLORS["text blue"],
    width=385,
    height=25,
    anchor="w",
    justify="right",
  )

  unhovered_change_path_button_dark = ctk.CTkButton(master=settings_box,
    text="",
    image=PhotoImage(file="./img/edit-button-unhovered-dark.png"),
    command=change_save_path,
    corner_radius=0,
    border_width=0,
    fg_color=COLORS["surface 1"],
    text_font=("century gothic", 10, "bold"),
    width=25,
    height=25,
    cursor="hand2",
    hover=False
  )

  unhovered_change_path_button_light = ctk.CTkButton(master=settings_box,
    text="",
    image=PhotoImage(file="./img/edit-button-unhovered-light.png"),
    command=change_save_path,
    corner_radius=0,
    border_width=0,
    fg_color=COLORS["surface 1"],
    text_font=("century gothic", 10, "bold"),
    width=25,
    height=25,
    cursor="hand2",
    hover=False
  )

  hovered_change_path_button = ctk.CTkButton(master=settings_box,
    text="",
    image=PhotoImage(file="./img/edit-button-hovered.png"),
    command=change_save_path,
    corner_radius=0,
    border_width=0,
    fg_color=COLORS["surface 1"],
    text_font=("century gothic", 10, "bold"),
    hover=False,
    width=25,
    height=25,
    cursor="hand2"
  )

  theme_label = ctk.CTkLabel(master=settings_box,
    text="dark theme:",
    corner_radius=0,
    fg_color=COLORS["surface 1"],
    text_font=("centurty gothic", 14),
    text_color=COLORS["text red"],
    width=120,
    height=25
  )

  theme_frame_button = ctk.CTkFrame(master=settings_box,
    width=38,
    height=20,
    bg_color=COLORS["surface 1"],
    corner_radius=10,
  )

  theme_button = ctk.CTkButton(master=settings_box,
    text="",
    width=16,
    height=16,
    bg_color=COLORS["background"],
    hover_color=COLORS["highlight blue dark 1"],
    command=toggle_theme,
    cursor="hand2"
  )

  # List
  WIDGETS_SETTINGS["bar"].append(bar)
  WIDGETS_SETTINGS["back button"].append(back_button)
  WIDGETS_SETTINGS["frame title"].append(frame_title)
  WIDGETS_SETTINGS["settings box"].append(settings_box)
  WIDGETS_SETTINGS["save path label"].append(save_path_label)
  WIDGETS_SETTINGS["path label"].append(path_label)
  WIDGETS_SETTINGS["unhovered change path button dark"].append(unhovered_change_path_button_dark)
  WIDGETS_SETTINGS["unhovered change path button light"].append(unhovered_change_path_button_light)
  WIDGETS_SETTINGS["hovered change path button"].append(hovered_change_path_button)
  WIDGETS_SETTINGS["theme label"].append(theme_label)
  WIDGETS_SETTINGS["theme frame button"].append(theme_frame_button)
  WIDGETS_SETTINGS["theme button"].append(theme_button)

  # Binds
  WIDGETS_SETTINGS["unhovered change path button light"][-1].bind("<Enter>", hover_change_button)
  WIDGETS_SETTINGS["unhovered change path button dark"][-1].bind("<Enter>", hover_change_button)
  WIDGETS_SETTINGS["hovered change path button"][-1].bind("<Leave>", unhover_change_button)
  
  # Place
  WIDGETS_SETTINGS["bar"][-1].place(relx=0.01, rely=0.0125)
  WIDGETS_SETTINGS["back button"][-1].place(relx=0.01, rely=0.125)
  WIDGETS_SETTINGS["frame title"][-1].place(relx=0.082, rely=0.125)
  WIDGETS_SETTINGS["frame title"][-1].text_label.place(relx=0, anchor="w")
  WIDGETS_SETTINGS["settings box"][-1].place(relx=0.01, rely=0.125)
  WIDGETS_SETTINGS["save path label"][-1].place(relx=0.05, rely=0.2)
  WIDGETS_SETTINGS["save path label"][-1].text_label.place(relx=1, anchor="e")
  WIDGETS_SETTINGS["path label"][-1].place(relx=0.26, rely=0.2)
  WIDGETS_SETTINGS["path label"][-1].text_label.place(relx=0, anchor="w")
  WIDGETS_SETTINGS["theme label"][-1].place(relx=0.05, rely=0.275)
  WIDGETS_SETTINGS["theme label"][-1].text_label.place(relx=1, anchor="e")
  WIDGETS_SETTINGS["theme frame button"][-1].place(relx=0.886, rely=0.28125)
  if SETTINGS["theme"] == "dark":
    WIDGETS_SETTINGS["unhovered change path button dark"][-1].place(relx=0.908, rely=0.2)
    WIDGETS_SETTINGS["theme button"][-1].place(relx=0.92, rely=0.2854)
    WIDGETS_SETTINGS["theme button"][-1].configure(fg_color=COLORS["secondary"])
  else:
    WIDGETS_SETTINGS["unhovered change path button light"][-1].place(relx=0.908, rely=0.2)
    WIDGETS_SETTINGS["theme button"][-1].place(relx=0.889, rely=0.2854)
    WIDGETS_SETTINGS["theme button"][-1].configure(fg_color="gray60")

### Loop ###

load_settings()
main_menu_frame()
root.mainloop()

