from pytube import YouTube
from pytube import Playlist
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os

def extension_change():
    new_extension = new_dir.get()
    with open("extension.txt", 'w') as extension_file:
        extension_file.write(new_extension)
    extension_file.close()
    messagebox.showinfo(title="Extension changed!", message=f"Changed the extension to {new_extension}!")
def read_extension():
    files = os.listdir()
    present = False
    for file in files: #Checking if the save directory file exists in the same directory as the script file.
        if file.startswith("extension"):
            present = True
    if present:
        with open("extension.txt", "r") as directory_file:
            directory = directory_file.readlines()
            directory_file.close()
            return directory
    else:
        messagebox.showerror(title="Error", message="Save file not found!\nPlease add an extension with change dir option") #showing an error
        win = Tk() #not really tested but it's supposed to be just a directory changer window.
        win.frame()
        win.geometry('325x125')
        Label(win, text="The file is missing!").place(x=100, y=10)
        Label(win, text="Change or add directory", font='italic 10').place(x=90, y=25)
        new_dir = Entry(win, width=48)
        new_dir.place(x=10, y=50)
        Button(win, text="Change dir", command=extension_change).place(x=120, y=75)
        win.mainloop()

def directory_change(): #directory change method
    new_directory = new_dir.get()
    with open('save_directory.txt', "w") as directory_file:
        directory_file.write(new_directory)
    directory_file.close()
    messagebox.showinfo(title = "directory changed!", message=f"changed the save directory to:\n{new_directory}") #showing message
    return f"directory changed to {new_directory}"

def read_directory(): #reading the contents of the save_directory file
    files = os.listdir()
    present = False
    for file in files: #Checking if the save directory file exists in the same directory as the script file.
        if file.startswith("save_directory"):
            present = True
    if present:
        with open("save_directory.txt", "r") as directory_file:
            directory = directory_file.readlines()
            directory_file.close()
            return directory
    else:
        messagebox.showerror(title="Error", message="Save file not found!\nPlease add a direcotry with change dir option") #showing an error
        win = Tk() #not really tested but it's supposed to be just a directory changer window.
        win.frame()
        win.geometry('325x125')
        Label(win, text="The file is missing!").place(x=100, y=10)
        Label(win, text="Change or add directory", font='italic 10').place(x=90, y=25)
        new_dir = Entry(win, width=48)
        new_dir.place(x=10, y=50)
        Button(win, text="Change dir", command=directory_change).place(x=120, y=75)
        win.mainloop()



def single_audio_download(): #single audio download method
    link = url.get() #getting the audio url from the entry box
    youtube_object = YouTube(link) #creating youtube object
    audio_title = youtube_object.title
    print(f"downloading {audio_title}")
    download_status.config(text=f"downloading {audio_title}...")
    download_status.update()
    youtube_object1080 = youtube_object.streams.get_by_itag(141) #getting highest resolution
    try:
        directory = read_directory()[0]
        youtube_object1080.download(output_path= directory, filename= f"{audio_title}.{read_extension()[0]}")
        print(f"{audio_title} downloaded successfully\n")
        download_status.config(text=f"downloaded {audio_title} successfully!")
        download_status.update()
    except:
        try:
            youtube_object = youtube_object.streams.get_audio_only()
            youtube_object.download(output_path=directory, filename=f"{audio_title}.{read_extension()[0]}")  # downloading audio
            print(f"{audio_title} downloaded successfully\n")
            download_status.config(text=f"downloaded {audio_title} successfully!")
            download_status.update()
        except:
            print("there was an error while downloading the audio")
            download_status.config(text=f"there was an error while downloading {audio_title}")
            download_status.update()

def playlist_dowload():
    playlist_link = playlist_url.get()
    playlist = Playlist(playlist_link)
    number_of_filess = len(playlist.audios)
    progressbar.start()
    downloaded_audios = 0
    total_percentage = 0
    percent_per_files = (1/number_of_filess) * 100
    for audio in playlist.audios:
        try: #I found that for some audios it inexplicably gives me an exception stating that it can't get the title of a audio so I'm trying to catch it here.
            audio_title = audio.title
        except:
            print("error while getting the title of the audio")
            audio_title = "n/a" #the file is still going to be saved as the original title as this is just for the gui and prints

        current_audio.config(text=f'Currently downloading: {audio_title}', bg='#0F0F0F', fg='#fafafa') #displaying currently downloading audio
        current_audio.update() #updating the gui

        print(f"Downloading {audio_title}...") #a print for debugging

        if f"{audio_title}.mp4" in os.listdir(read_directory()[0]): #seeing if the audio has already been downloaded
            print("file already downloaded")
            continue
        else:
            print(f"apparently not found {audio_title}")

        try: #huge try except for all of this just in case heart
            files_link = audio.watch_url
            youtube_object = YouTube(files_link)
            youtube_object1080 = youtube_object.streams.get_by_itag(141) #itag 141 = 256k audio - getting the stream and downloading it

            try: #trying to download it at 1080p
                directory = read_directory()[0] #getting the save directory
                youtube_object.download(output_path=directory, filename=f"{audio_title}.{read_extension()[0]}")  # downloading audio
                print(f"{audio_title} downloaded successfully\n")
                current_audio.config(text=f"{audio_title} downloaded successfully", bg='#0F0F0F', fg='#fafafa')
            except: #if it fails to download it we try to download the highest resolution it can download
                try: #trying to download the highest resolution
                    youtube_object = youtube_object.streams.get_audio_only()
                    youtube_object.download(output_path= directory, filename=f"{audio_title}.{read_extension()[0]}") #downloading audio
                    print(f"{audio_title} downloaded successfully\n")
                    current_audio.config(text=f"{audio_title} downloaded successfully", bg='#0F0F0F', fg='#fafafa')
                except: #there's some other error preventing it from downloading
                    print("there was an error while downloading the audio")
                    current_audio.config(text=f"there was an error while downloading the audio", bg='#0F0F0F', fg='#fafafa')

            downloaded_audios += 1 #updating the taskbar
            progressbar.update_idletasks()
            total_percentage += percent_per_files
            progress_percent.config(text=f'{total_percentage:.2f}%')
            downloaded.config(text=f'{downloaded_audios}/{number_of_filess} downloaded')
            downloaded.update() #updating downloaded counter on gui
            progress_percent.update() #updating progress percent (pp) on the gui
            if downloaded_audios == number_of_filess:
                progressbar.stop() # resetting and stopping the progressbar
        except: #some other error occured during this entire proccess
            print(f"failed to download audio {audio_title}")
            current_audio.config(text=f'failed to download audio "{audio_title}"',bg='#0F0F0F', fg='#fafafa')

        current_audio.update() #updating the window so it shows the download status


root = Tk() #creating tkinter object
root.frame() #creating the frame so it could be fullscreened
root.geometry('1053x450')#decided this is an optimal resolution
root.config(bg='#0F0F0F') #setting the background color to the youtube dark mode one
root.title("YouTube Audio Downloader by jtw") #window title
root.iconphoto(False, PhotoImage(file= f"{os.getcwd()}\\yt_icon.ico")) #changing the icon of the window to that of youtube
Label(root, text="YouTube Audio Downloader",bg='#0F0F0F',fg='#fafafa' , font='italic 15 bold').pack(pady=10) #first title label

#Downloadng a single audio
Label(root, text = "Download a single audio: ",bg='#0F0F0F',fg='#fafafa', font="italic 10").place(x=37, y=72) #label
url = Entry(root, width=60) #creating entry box
url.place(x=185, y=72) #fixed position (would look worse the higher the resolution of the monitor gets)
Button(root, text="Download",bg='#267cc7', command=single_audio_download).place(x=555, y=67) #creating the button using random color as background color
download_status = Label(root, text="", bg='#0f0f0f', fg="#fafafa", font='italic 10')
download_status.place(x=185, y=92) #decided to also add download status for single audio downloads


#Downloading a playlist
Label(root, text = "Download a playlist: ",bg='#0F0F0F',fg='#fafafa', font="italic 10").place(x=37, y=150)
playlist_url = Entry(root, width=60)
playlist_url.place(x=185, y=150)
Button(root, text="Download", bg='#267cc7', command=playlist_dowload).place(x = 555, y = 145)
current_audio = Label(root, text='',bg='#0F0F0F') # not quite sure if I should delete that
current_audio.place(x=185, y=170)

#creating a progressbar and everything related to it
progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=600, mode= 'determinate')
progressbar.place(x=150, y=500)
progressbar.pack(expand=True)
progress_percent = Label(root, text='', bg='#0f0f0f', fg='#fafafa', font='italic 10') #progress percent. pretty self explanatory
progress_percent.place(x=840, y=100)
downloaded = Label(root, text='', bg='#0f0f0f', fg='#fafafa', font='italic 10') #count for downloaded audios
downloaded.place(x=840, y=180)

#adding the option to change a directory
Label(root, text="Change or add directory",bg='#0F0F0F', fg='#fafafa' ,font='italic 10').place(x=475, y= 300)
new_dir = Entry(root, width=48)
new_dir.place(x=400, y=325)
Button(root, text="Change dir",bg='#267cc7', command=directory_change).place(x=500, y= 350)
Button(root, text="Change extension", bg='#267cc7', command=extension_change).place(x=700, y=322)

Button(root, text = "QUIT", width=10, height=1, bg='RED', fg='#fafafa', command=root.destroy).place(relx= .9, rely=.9, anchor=CENTER)
root.mainloop() #executing tkinter object