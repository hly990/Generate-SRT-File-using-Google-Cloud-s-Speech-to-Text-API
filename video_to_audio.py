import subprocess
from google.cloud import storage
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


video_to_audio("upload/book1.mp4","book1.mp3",2,445032,44100)