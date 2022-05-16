from google.cloud import speech_v1
from google.cloud.speech import enums
# from google.cloud import speech_v1p1beta1 as speech_v1
# from google.cloud.speech_v1p1beta1 import enums
# from google.cloud.speech_v1p1beta1 import types
import os
import srt
import datetime
import subprocess
from google.cloud import storage
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

def video_to_audio(video_filepath, audio_filename, video_channels, video_bit_rate, video_sample_rate):
    command = f"ffmpeg -i {video_filepath} -b:a {video_bit_rate} -ac {video_channels} -ar {video_sample_rate} -vn {audio_filename}"
    subprocess.call(command, shell=True)
    blob_name = f"audios/{audio_filename}"
    #upload_blob(BUCKET_NAME, audio_filename, blob_name)
    upload_blob("media990", audio_filename, blob_name)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def long_running_recognize(storage_uri, channels, sample_rate):
    
    client = speech_v1.SpeechClient()

    config = {
        "language_code": "en_US", #zh   en_US
        "sample_rate_hertz": int(sample_rate),
        "encoding": enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        "audio_channel_count": int(channels),
        "enable_word_time_offsets": True,
         "model": "video",  #  default  video
        "enable_automatic_punctuation":True
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)
    # operation = client.recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    return response

def subtitle_generation(speech_to_text_response, bin_size=3):
    """We define a bin of time period to display the words in sync with audio. 
    Here, bin_size = 3 means each bin is of 3 secs. 
    All the words in the interval of 3 secs in result will be grouped togather."""
    transcriptions = []
    index = 0
 
    for result in speech_to_text_response.results:
        try:
            if result.alternatives[0].words[0].start_time.seconds:
                # bin start -> for first word of result
                start_sec = result.alternatives[0].words[0].start_time.seconds 
                start_microsec = result.alternatives[0].words[0].start_time.nanos * 0.001
            else:
                # bin start -> For First word of response
                start_sec = 0
                start_microsec = 0 
            end_sec = start_sec + bin_size # bin end sec
            
            # for last word of result
            last_word_end_sec = result.alternatives[0].words[-1].end_time.seconds
            last_word_end_microsec = result.alternatives[0].words[-1].end_time.nanos * 0.001
            
            # bin transcript
            transcript = result.alternatives[0].words[0].word
            
            index += 1 # subtitle index

            for i in range(len(result.alternatives[0].words) - 1):
                try:
                    word = result.alternatives[0].words[i + 1].word
                    word_start_sec = result.alternatives[0].words[i + 1].start_time.seconds
                    word_start_microsec = result.alternatives[0].words[i + 1].start_time.nanos * 0.001 # 0.001 to convert nana -> micro
                    word_end_sec = result.alternatives[0].words[i + 1].end_time.seconds
                    word_end_microsec = result.alternatives[0].words[i + 1].end_time.nanos * 0.001

                    if word_end_sec < end_sec:
                        transcript = transcript + " " + word
                    else:
                        previous_word_end_sec = result.alternatives[0].words[i].end_time.seconds
                        previous_word_end_microsec = result.alternatives[0].words[i].end_time.nanos * 0.001
                        
                        # append bin transcript
                        transcriptions.append(srt.Subtitle(index, datetime.timedelta(0, start_sec, start_microsec), datetime.timedelta(0, previous_word_end_sec, previous_word_end_microsec), transcript))
                        
                        # reset bin parameters
                        start_sec = word_start_sec
                        start_microsec = word_start_microsec
                        end_sec = start_sec + bin_size
                        transcript = result.alternatives[0].words[i + 1].word
                        
                        index += 1
                except IndexError:
                    pass
            # append transcript of last transcript in bin
            transcriptions.append(srt.Subtitle(index, datetime.timedelta(0, start_sec, start_microsec), datetime.timedelta(0, last_word_end_sec, last_word_end_microsec), transcript))
            index += 1
        except IndexError:
            pass
    
    print(u"Waiting for subtitles to complete...")
    # turn transcription list into subtitles
    subtitles = srt.compose(transcriptions)
    return subtitles


os.environ["http_proxy"] = "http://127.0.0.1:1092"
os.environ["https_proxy"] = "http://127.0.0.1:1092"

#upload
video_to_audio("upload/Backend-Application-is-stateless.mp4","Backend-Application-is-stateless.mp3",2,445032,44100)

res = long_running_recognize("gs://media990/audios/Backend-Application-is-stateless.mp3",8,16000)
sub = subtitle_generation(res)
print(sub)

with open("subtitles.srt", "w") as f:
    f.write(sub)



