import pandas as pd
import time
from dalle3_image_generation import generate_dalle_image
from album_art_text_overlay import create_album_art

def generate_images_for_songs(csv_file):
  df_playlist = pd.read_csv(csv_file, sep=';')
  
  image_file_path = list()
  info_image_file_path = list()
  
  response_str = 'Generated images for the upcoming song. '
  
  for i, row in df_playlist.iterrows():
    if row['Audio'] == 'Not Found':
      image_file_path.append(None)
      info_image_file_path.append(None)
      response_str += f"\n{row['Title']} by {row['Artist']}: Cannot find the audio, Failed to generate Image"
      print(f"Failed to find the audio file for '{row['Title']}'...")
    else:
      image_file = generate_dalle_image(row['Title'], row['Artist'])
      image_file_path.append(image_file)
      
      info_image_file = create_album_art(image_file, row['Title'], row['Artist'])
      info_image_file_path.append(info_image_file)
      
      response_str += f"\n{row['Title']} by {row['Artist']}: Successfully generated the image {image_file}"
    time.sleep(1)
  
  df_playlist['Image'] = image_file_path
  df_playlist['Info_Image'] = info_image_file_path
  df_playlist.to_csv(csv_file, sep=';', index=False, lineterminator='\n')
  return response_str

if __name__ == '__main__':
  csv_file = '/Users/dianna/Desktop/CST/After/Playlist_Generator/playlist_csv/2010_kpop.csv'
  result = generate_images_for_songs(csv_file)
  print(result)