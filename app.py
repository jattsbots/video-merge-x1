from pyrogram import Client, filters
from moviepy.editor import VideoFileClip, clips_array
import os

# Replace with your string session
string_session = "YOUR_STRING_SESSION"

app = Client("video_merger_bot", string_session=string_session)

@app.on_message(filters.command('start'))
def start(client, message):
    message.reply_text("Send me two video files to merge.")

@app.on_message(filters.video & filters.private)
def receive_video(client, message):
    chat_id = message.chat.id
    if 'video1' not in client.data:
        client.data['video1'] = message.video.file_id
        client.send_message(chat_id, "Video 1 received. Send the second video.")
    elif 'video2' not in client.data:
        client.data['video2'] = message.video.file_id
        client.send_message(chat_id, "Video 2 received. Merging...")
        merge_videos(client, chat_id)
    else:
        message.reply_text("Already received two videos. Please start over by sending /start.")

def merge_videos(client, chat_id):
    video1_id = client.data.get('video1')
    video2_id = client.data.get('video2')
    
    # Download videos
    video1_path = download_video(client, video1_id, 'video1.mp4')
    video2_path = download_video(client, video2_id, 'video2.mp4')
    
    # Merge videos
    output_path = 'merged_video.mp4'
    merge_video_files(video1_path, video2_path, output_path)
    
    # Send the merged video
    client.send_video(chat_id, output_path)
    
    # Clean up
    os.remove(video1_path)
    os.remove(video2_path)
    os.remove(output_path)
    
    # Reset data
    client.data = {}

def download_video(client, file_id, filename):
    file_path = client.download_media(file_id, file_name=filename)
    return file_path

def merge_video_files(video1_path, video2_path, output_path):
    clip1 = VideoFileClip(video1_path)
    clip2 = VideoFileClip(video2_path)
    
    # Resize if necessary
    clip1 = clip1.resize(height=360)
    clip2 = clip2.resize(height=360)
    
    # Merge clips side by side
    final_clip = clips_array([[clip1, clip2]])
    final_clip.write_videofile(output_path, codec='libx264')

if __name__ == "__main__":
    app.data = {}
    app.run()
