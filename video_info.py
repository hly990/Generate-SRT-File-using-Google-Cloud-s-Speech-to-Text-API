from pydub.utils import mediainfo
def video_info(video_filepath):
    """ this function returns number of channels, bit rate, and sample rate of the video"""

    video_data = mediainfo(video_filepath)
    channels = video_data["channels"]
    bit_rate = video_data["bit_rate"]
    sample_rate = video_data["sample_rate"]

    return channels, bit_rate, sample_rate

x,y,z = video_info("book1.mp4")
print(x,y,z)