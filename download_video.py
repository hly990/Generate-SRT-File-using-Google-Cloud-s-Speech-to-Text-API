from pytube import YouTube
import os
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

proxy1="socks5://127.0.0.1:1082"
proxy2="http://127.0.0.1:1092"

os.environ["http_proxy"] = proxy2
os.environ["https_proxy"] = proxy2

# my_dict = {
#   'http_proxy': 'http://127.0.0.1:1092',
#   'https_proxy': 'http://127.0.0.1:1092',
#   'socket_proxy': 'http://127.0.0.1:1082',
# }


def download_video(link):
    try: 
        #object creation using YouTube which was imported in the beginning 
        yt = YouTube(link) 
    except: 
        print("Connection Error") #to handle exception 
    video_path = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path="upload")

    return video_path


path = download_video("https://youtu.be/ho9nKj3lFkU")

print(path)