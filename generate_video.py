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
  """
  Combines multiple video clips into a single video.
  
  Args:
    video_paths (list[str]): A list of file paths to the each video clips.
    output_path (str): The output file path for the combined video.
    
  Returns:
    str: The path to the final combined video file.
  """
  clips = [VideoFileClip(video_path) for video_path in video_paths]
  
  combined_video = concatenate_videoclips(clips)
  combined_video.write_videofile(output_path, codec='libx264')
  
  return output_path
  
def generate_video_using_images(csv_file):
  """
  Generates individual videos from a csv file and combines them into one final video.
  The csv file should contain the following columns:
    
  Args:
    csv_file (str): The path to the playlist csv file that contains the following columns:
      - 'Audio': The file path of the audio file (e.g. mp3)
      - 'Info_Image': The file path of the image that represents the song info.
    
  Returns: 
    str: A message indicating that the final video has been created with the output path. 
  """
  videos = create_videos_from_csv_playlist(csv_file)
  
  dir, csv_file_full_name = os.path.split(csv_file)
  file_name, ext = os.path.splitext(csv_file_full_name)
  
  output_video_path = f'./videos/{file_name}.mp4'
  combine_videos(videos, output_video_path)

  return f"The video for the playlist is successfully created. A file path is as follow: \n {output_video_path}" 
