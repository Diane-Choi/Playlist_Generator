from moviepy import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips

import pandas as pd
import os

def create_video(audio_path, image_path):
  """
  Creates a video with the given audio and the image and saves it in the 'videos' directory.
  
  Args:
    audio_path (str): A file path for the audio file.
    image_path (str): A file path for the image file that contains the song information.
    
  Returns: 
    str: A path of the mp4 file (output)
  
  """
  image = ImageClip(image_path)
  image = image.with_duration(AudioFileClip(audio_path).duration) # match the audio duration with the image clip duration
  
  audio = AudioFileClip(audio_path)
  
  video = image.with_audio(audio)
  
  dir, image_file_full_name = os.path.split(image_path)
  file_name, ext = os.path.splitext(image_file_full_name)
  
  print(file_name)
  
  output_path = f'./videos/{file_name}.mp4'
  video.write_videofile(output_path, codec='libx264', fps=1)
  
  return output_path

def create_videos_from_csv_playlist(csv_file):
  """
  Creates a video for each of the song in the playlist csv file that has the following columns:
    - 'Audio': The file path of the audio file (e.g. mp3)
    - 'Info_Image': The file path of the image that represents the song info.
  
  Args:
    csv_file (str): A file path of the csv file (separated by ;)
    
  Returns:
    list[str]: A list of successfully created video paths
  """
  df_playlist = pd.read_csv(csv_file, sep=';')
  videos = list()
  
  for i, row in df_playlist.iterrows():
    if row['Audio'] != 'Not Found':
      video = create_video(row['Audio'], row['Info_Image'])
      videos.append(video)
  
  return videos
  
def combine_videos(video_paths, output_path):
  clips = [VideoFileClip(video_path) for video_path in video_paths]
  
  combined_video = concatenate_videoclips(clips)
  combined_video.write_videofile(output_path, codec='libx264')
  
  return output_path
  


if __name__ == '__main__':
  audio_path = '/Users/dianna/Desktop/CST/After/Playlist_Generator/audios/I_Am_the_Best-2NE1.mp3'
  image_path = '/Users/dianna/Desktop/CST/After/Playlist_Generator/images/I_Am_the_Best_2NE1__info.png'
  # result = create_video(audio_path, image_path)
  videos = create_videos_from_csv_playlist('/Users/dianna/Desktop/CST/After/Playlist_Generator/playlist_csv/2010_kpop.csv')
  output_video_path = 'com_vid.mp4'
  combine_videos(videos, output_video_path)
  print("Video combined: ",output_video_path)