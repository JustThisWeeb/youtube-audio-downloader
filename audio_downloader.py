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
        link = url.get()  # getting the video url from the entry box
        youtube_object = YouTube(link)  # creating youtube object
        try:
            video_title = youtube_object.title  # getting the title and because sometimes it just gives me an error when trying to get the title I will be catching such situations here
        except:
            try:
                youtube_object = YouTube(link)  # retrying
                video_title = youtube_object.title
            except:
                video_title = "not available"  # default for when there's no title.

        print(f"downloading {video_title}")  # status updates
        download_status.config(text=f"downloading {video_title}...")
        download_status.update()


        print(youtube_object.watch_url)
        youtube_object1080 = youtube_object.streams.filter(file_extension='mp4', res='1080p',
                                                               only_video=True).first()  # getting 1080p video resolution
        youtube_object_audio = youtube_object.streams.filter(file_extension='mp4',
                                                                 only_audio=True).first()  # getting the audio for said vide

        try:
            directory = read_directory()[0]  # getting the save directory
            if "." in video_title:
                video_title = video_title.replace(".", "")
            youtube_object_audio.download(output_path=directory,
                                            filename=f'{video_title}.{read_extension()[0]}')  # downloading the audio file
            print(f"{video_title} downloaded successfully at 1080p\n")  # status updates
            download_status.config(text=f"downloaded {video_title} successfully at 1080p resolution!")
            download_status.update()

        except:
            print(
                "failed to download highest so trying with the highest possible quality...")  # failed to download 1080p meaning there was some error or the video doesn't have 1080p
            try:
                try:
                    os.remove(f'{directory}\\{video_title}.mp3')
                except:
                    print("no audio file to be deleted")
                youtube_object = youtube_object.streams.get_audio_only()  # getting the highest resolution it can get # resolution for said video
                youtube_object.download(directory)  # downloading it
                # status updates
                print(
                    f"{video_title} downloaded successfully at {res} resolution and {youtube_object.fps}fps {youtube_object.video_codec} codec  {youtube_object.bitrate} bitrate {youtube_object.filesize_mb} mb size\n")
                download_status.config(
                    text=f"downloaded {video_title} successfully at {res} resolution and {youtube_object.fps}fps! ({youtube_object.filesize_mb:.2f} mb size)")
                download_status.update()
            except:
                print("there was an error while downloading the video")  # some other error occured
                download_status.config(text=f"there was an error while downloading {video_title}")  # status updates
                download_status.update()

def playlist_dowload():
    playlist_link = playlist_url.get()
    playlist = Playlist(playlist_link)
    number_of_vids = len(playlist.videos)
    progressbar.start()
    downloaded_videos = 0  # counter for downloaded videos
    total_percentage = 0  # download percentage
    percent_per_vid = (1 / number_of_vids) * 100
    for video in playlist.videos:
        try:  # I found that for some videos it inexplicably gives me an exception stating that it can't get the title of a video so I'm trying to catch it here.
            video_title = video.title
        except:
            try:
                video = YouTube(video.watch_url)
                video_title = video.title
            except:
                print("error while getting the title of the video")
                video_title = "not available"  # the file is still going to be saved as the original title as this is just for the gui and prints

        current_audio.config(text=f'Currently downloading: {video_title}', bg='#0F0F0F',
                             fg='#fafafa')  # displaying currently downloading video
        current_audio.update()  # updating the gui

        print(f"Downloading {video_title}...")

        if f"{video_title}.{read_extension()[0]}" in os.listdir(read_directory()[0]):  # seeing if the video has already been downloaded

            print("file already downloaded\n")
            current_audio.config(text=f"{video_title} already downloaded")
            downloaded_videos += 1
            total_percentage += percent_per_vid
            progress_percent.config(text=f'{total_percentage:.2f}%')
            downloaded.config(text=f'{downloaded_videos}/{number_of_vids} downloaded')
            downloaded.update()  # updating downloaded counter on gui
            progress_percent.update()  # updating progress percent (pp) on the gui
            progressbar.update_idletasks()
            if downloaded_videos == number_of_vids:
                progressbar.stop()  # resetting and stopping the progressbar
            continue


        try:  # huge try except for all of this just in case heart
            vid_link = video.watch_url
            youtube_object = YouTube(vid_link)  # same procedure as the single video downloads except it's for playlists
            youtube_object_audio = youtube_object.streams.filter(file_extension='mp4',
                                                                    only_audio=True).first()  # getting the audio for said vide
            try:
                current_audio.config(text=f"Downloading {video_title}...")
                directory = read_directory()[0]  # getting the save directory
                print("checking if the title is valid...")
                if "." in video_title:  # This can cause issues if the title ends in ... as windows would just ignore and remove them but the title of the video still has it
                    video_title.replace(".", "")
                print("downloading seperate streams...")
                youtube_object_audio.download(output_path=directory, filename=f'{video_title}.{read_extension()[0]}')  # downloading the audio file
                print(f"{video_title} downloaded successfully at 1080p\n")  # status updates
                current_audio.config(text=f"downloaded {video_title} successfully at 1080p resolution!")
                current_audio.update()

            except:  # if it fails to download it we try to download the highest resolution it can download
                print("failed to download 1080p version. trying to download with the highest possible resolution (usually 720p)")
                try:  # trying to download the highest resolution
                    youtube_object = youtube_object.streams.get_audio_only()
                    youtube_object.download(output_path=directory, filename=f'{video_title}.{read_extension()[0]}')  # downloading video
                    print(f"{video_title} downloaded successfully at {youtube_object.resolution} resolution\n")
                    current_audio.config(text=f"{video_title} downloaded successfully", bg='#0F0F0F', fg='#fafafa')
                except:  # there's some other error preventing it from downloading
                    print("there was an error while downloading the video")
                    current_audio.config(text=f"there was an error while downloading the video", bg='#0F0F0F',
                                             fg='#fafafa')

            downloaded_videos += 1  # updating the taskbar
            progressbar.update_idletasks()
            total_percentage += percent_per_vid
            progress_percent.config(text=f'{total_percentage:.2f}%')
            downloaded.config(text=f'{downloaded_videos}/{number_of_vids} downloaded')
            downloaded.update()  # updating downloaded counter on gui
            progress_percent.update()  # updating progress percent (pp) on the gui
            if downloaded_videos == number_of_vids:
                progressbar.stop()  # resetting and stopping the progressbar

        except:  # some other error occured during this entire proccess
            print(f"failed to download video {video_title}")
            current_audio.config(text=f'failed to download video "{video_title}"', bg='#0F0F0F', fg='#fafafa')

        current_audio.update()  # updating the window so it shows the download status

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