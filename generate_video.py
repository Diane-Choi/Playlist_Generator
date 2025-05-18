from moviepy import ImageClip, AudioFileClip

import pandas as pd
import os

def create_video(audio_path, image_path):
  """
  Creates a video with the given audio and the image.
  
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
  
  
if __name__ == '__main__':
  audio_path = '/Users/dianna/Desktop/CST/After/Playlist_Generator/audios/I_Am_the_Best-2NE1.mp3'
  image_path = '/Users/dianna/Desktop/CST/After/Playlist_Generator/images/I_Am_the_Best_2NE1__info.png'
  result = create_video(audio_path, image_path)
  print(result)