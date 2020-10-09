from pytube import Playlist
from pytube import YouTube
import re
#for gui
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import *
#threading
from threading import *

font = ('verdana', 15)
file_size = 0
myPlaylist=[]

#on complete callback function
def completeDownload(stream=None, file_path=None):
    print("Download Completed")
    showinfo("Message", "File has been downloaded...")
    downloadBtn['text']="Download Now"
    downloadBtn['bg'] = "#3BB8E4"
    downloadBtn['state']='active'
    urlField.delete(0, END)

#on progress callback function
def progressDownload(stream=None, chunk=None, bytes_remaining=None):
    percent = (100*((file_size-bytes_remaining)/file_size))
    downloadBtn['text']="{:00.0f}% downloaded ".format(percent)

#function for downloading single video
def startDownload(url):
    global file_size
    path_to_save=askdirectory()
    if path_to_save is None:
        return

    try:
        yt=YouTube(url)
        st=yt.streams.first()

        yt.register_on_complete_callback(completeDownload)
        yt.register_on_progress_callback(progressDownload)

        file_size=st.filesize
        st.download(output_path=path_to_save)
    except Exception as e:
        print(e)
        label1['text'] = "Paste a valid video url (paste playlist url in below field)"
        label1['bg'] = 'red'
        downloadBtn['text'] = "Download Video"
        downloadBtn['bg'] = "#3BB8E4"
        downloadBtn['state'] = "active"

#function for downloading playlist
def downloadPlaylist(url):
    path_to_save = askdirectory()
    if path_to_save is None:
        return

    try:
        try:
            playlist = Playlist(url)
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

            lengthOfPlaylist = len(playlist.video_urls)
            if (lengthOfPlaylist==0):
                return
            print(lengthOfPlaylist)
            for videoUrl in playlist.video_urls:
                print(videoUrl)
                myPlaylist.append(videoUrl)

            #print(myPlaylist)
        except Exception as e:
            print(e)
            videoName['text']="An exception occured while downloading the playlist. Error: Unable to fetch data from the error or the link is not valid."
            videoName['bg']='red'
        count = 1
        for link in myPlaylist:
            try:
                yt = YouTube(link)
                videos = yt.streams.filter(mime_type="video/mp4")
                video = videos[0]
            except:
                videoName['text']="Exception occured. Either the video has no quality as set by you, or it is not available. Skipping video {number}".format(number=count)
                count += 1
                continue

            video.download(path_to_save)
            percent = (100 * (count / lengthOfPlaylist))
            print(yt.title + " - has been downloaded !!!")
            print("{per}% downloaded".format(per=percent))
            videoName['text']=(yt.title +" - has been downloaded !!!")
            count += 1
            downloadPlaylistBtn['text'] = "{:00.0f}% downloaded ".format(percent)

        print("Download Completed")
        showinfo("Message", "File has been downloaded...")
        videoName['text']=''
        downloadPlaylistBtn['text'] = "Download Playlist"
        downloadPlaylistBtn['bg'] = "#3BB8E4"
        downloadPlaylistBtn['state'] = 'active'
        playlistUrlField.delete(0, END)

    except Exception as e:
        print(e)

def btnClicked():
    try:
        downloadBtn['text'] = "Please wait..."
        downloadBtn['bg'] = "#EEEEEE"
        downloadBtn['state'] = 'disabled'
        url=urlField.get()
        if url=='':
            downloadBtn['text'] = "Download Video"
            downloadBtn['bg'] = "#3BB8E4"
            downloadBtn['state'] = "active"
            return
        print(url)
        thread=Thread(target=startDownload, args=(url,))
        thread.start()
    except Exception as e:
        print(e)

def playlistBtnClicked():
    try:
        downloadPlaylistBtn['text'] = "Please wait..."
        downloadPlaylistBtn['bg'] = "#EEEEEE"
        downloadPlaylistBtn['state'] = 'disabled'
        url=playlistUrlField.get()
        #isPlaylistUrl = re.compile("/[?&]list=([^#\&\?]+)/", url)
        #print(isPlaylistUrl)
        if url=='':
            videoName['text'] = "Please Enter a playlist Url"
            downloadPlaylistBtn['text'] = "Download Playlist"
            downloadPlaylistBtn['bg'] = "#3BB8E4"
            downloadPlaylistBtn['state'] = "active"
            return
        #if isPlaylistUrl==None:
        #   label2['text'] = "Please Enter a valid playlist url here"
        #    label2['bg'] = 'red'
        #    downloadPlaylistBtn['text'] = "Download Playlist"
        #    downloadPlaylistBtn['bg'] = "#3BB8E4"
        #    downloadPlaylistBtn['state'] = "active"
        #    return
        print(url)
        thread = Thread(target=downloadPlaylist, args=(url,))
        thread.start()
    except Exception as e:
        print(e)
        print("here is the error")

#video="https://www.youtube.com/watch?v=V8xHlHhJYxE"
#playlist="https://www.youtube.com/playlist?list=PLsyeobzWxl7poL9JTVyndKe62ieoN-MZ3"

#gui part
root=Tk()
root.title("Vreviewtech YouTube Downloader")
root.iconbitmap("img/logo.ico")
root.geometry("400x500")

#main icon section

file = PhotoImage(file="img/logo.png")
headingIcon=Label(root,image=file)
headingIcon.pack(side=TOP, pady=10)

urlField=Entry(root, font=font, justify=CENTER)
urlField.pack(side=TOP, fill=X, padx=10, pady=10 )
urlField.focus()
label1 = Label( root, text="Paste Youtube video url here")
label1.pack(side=TOP)

#download button
downloadBtn=Button(root, text="Download Video", font=font, relief="ridge", bg='#3BB8E4', command=btnClicked)
downloadBtn.pack(side=TOP, pady=10)

#playlist field
playlistUrlField=Entry(root, font=font, justify=CENTER)
playlistUrlField.pack(side=TOP, fill=X, padx=10, pady=10 )
label2 = Label( root, text="Paste YouTube Playlist url here")
label2.pack(side=TOP)

#playlist download button
downloadPlaylistBtn=Button(root, text="Download Playlist", font=font, bg='#3BB8E4', command=playlistBtnClicked)
downloadPlaylistBtn.pack(side=TOP, pady=10)
videoName = Label( root, textvariable="")
videoName.pack(side=TOP, pady=5, padx=2)

#developer details
developedBy = Label(root, text="Developed By - Kantimahanty Rohit")
developedBy.pack(side=BOTTOM)

root.mainloop()