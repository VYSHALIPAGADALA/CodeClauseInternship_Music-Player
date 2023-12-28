# importing libraries
import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Creating functions to open a file playing the song
def AddMusic():
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)

        for song in songs:
            if song.endswith(".mp3"):
                Playlist.insert(END, song)

def play_song_by_index(index):
    if 0 <= index < Playlist.size():
        Music_Name = Playlist.get(index)
        print(Music_Name[0:-4])
        mixer.music.load(Playlist.get(index))
        mixer.music.play()
current_song_index=0

def PlayMusic():
    play_song_by_index(current_song_index)

# defining a funtion to play the previous song

def play_previous_song():
    global current_song_index
    if Playlist.size() > 0:
        current_song_index = (current_song_index - 1) % Playlist.size()
        PlayMusic

# defining a function to play the next song
def play_next_song():
    global current_song_index
    if Playlist.size() > 0:
        current_song_index = (current_song_index + 1) % Playlist.size()
        PlayMusic


# defining functions to increase and decrease the volume and s
def increase_system_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(current_volume + 0.1, 1.0)
    volume.SetMasterVolumeLevelScalar(new_volume, None)
def change_system_volume(delta):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, min(current_volume + delta, 1.0))
    volume.SetMasterVolumeLevelScalar(new_volume, None)
def set_default_volume(default_volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(default_volume, None)
default_volume = 0.5
set_default_volume(default_volume)

# defining functions to play the previous and next songs

def play_previous_song():
    global current_song_index
    current_song_index = (current_song_index - 1)
    PlayMusic()

def play_next_song():
    global current_song_index
    current_song_index = (current_song_index + 1)
    PlayMusic()

# creating a window and set the geometry, made it resizable

root = Tk()
root.title("Music Player")
root.geometry("485x700+290+10")
root.configure(background='#333333')
root.resizable(False, False)
mixer.init()
# setting the image for the window
photo =PhotoImage(file='img_1.png')
Label(root, image=photo).pack(fill=BOTH, expand=True)
root.image = photo

# creating a frame to place volume, play, pause, previous, next buttons

lower_frame = Frame(root, width=485, height=62,background='light green')
lower_frame.place(x=0, y=487)
# set the window icon
image_icon = PhotoImage(file="img.png")
root.iconphoto(False, image_icon)

# creating a play button

ButtonPlay = PhotoImage(file="play.png")
Button(root, image=ButtonPlay, bg="#FFFFFF", bd=0, height=60, width=60,
       command=PlayMusic).place(x=330, y=487)


mixer.init()

# Creating a button to increase the volume

VolumeUp = PhotoImage(file="volume_up.png")
Button(root,image=VolumeUp, bg="#FFFFFF", bd=0, height=60, width=60,
       command=increase_system_volume).place(x=20,y=487)

# Creating a button to decrease the volume

VolumeDown = PhotoImage(file="volume_down.png")
Button(root, image=VolumeDown, bg="#FFFFFF", bd=0, height=60, width=60,
       command=lambda: change_system_volume(-0.1)).place(x=100, y=487)

# creating a button to pause the music

ButtonPause = PhotoImage(file="pause.png")
Button(root, image=ButtonPause, bg="#FFFFFF", bd=0, height=60, width=60,
       command=mixer.music.pause).place(x=400, y=487)
# creating buttons to play the previous and next songs

prev = PhotoImage(file="img_3.png")
Button(root,image=prev, bg="#FFFFFF", bd=0, height=60, width=60,
       command=play_previous_song).place(x=180,y=487)
next_song = PhotoImage(file="img_4.png")
Button(root,image=next_song, bg="#FFFFFF", bd=0, height=60, width=60,
       command=play_next_song).place(x=260,y=487)

# creating a menu where the list of songs will be displayed
Menu = PhotoImage(file="menu.png")
Label(root, image=Menu).place(x=0, y=580, width=485, height=180)

Frame_Music = Frame(root, bd=2, relief=RIDGE)
Frame_Music.place(x=0, y=585, width=485, height=100)

Button(root, text="Browse Music", width=59, height=1, font=("calibri",
                                                            12, "bold"), fg="red", bg="light blue",
       command=AddMusic).place(x=0, y=550)

Scroll = Scrollbar(Frame_Music)
Playlist = Listbox(Frame_Music, width=100, font=("Times new roman", 10), bg="#333333", fg="grey",
                   selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=Scroll.set)
Scroll.config(command=Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=RIGHT, fill=BOTH)


root.mainloop()
