import pandas as pd
from youtube_search import YoutubeSearch
from utils.sanitize import sanitize_file_name
import yt_dlp

def is_relevant_video_title(video_title, song_title, song_artist):
  video_title = video_title.lower()
  song_title = song_title.lower()
  song_artist = song_artist.lower()
  
  title_words = song_title.split()
  artist_words = song_artist.split()
  
  title_matches = sum([word in video_title for word in title_words])
  artist_matches = sum([word in video_title for word in artist_words])
  
  return title_matches >= len(title_words) * 0.5 and artist_matches >= len(artist_words) * 0.5
  
def download_song(title, artist):
  query = f"{title} {artist} audio"
  file_name = sanitize_file_name(f"{title}-{artist}")
  
  # search Youtube
  videos_search = YoutubeSearch(query, max_results=5)
  results = videos_search.to_dict()
    
  for searched in results:
    video = searched
    video_title = video['title']
    
    if is_relevant_video_title(video_title, title, artist):
      video_url = f"https://www.youtube.com{searched['url_suffix']}"
        
      # set up yt_dlp
      ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
        }],
        'ffmpeg_location': '/usr/local/bin',
        'outtmpl': f'./audios/{file_name}.%(ext)s'
      }
        
      # download the audio file
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
      print(f"Successfully download the audio file for: {title} by {artist}")
      return f'./audios/{file_name}.mp3'
  else:
    print(f"Cannot find the audio file for: {title} by {artist}")
  return None
      
def download_music_from_youtube(csv_file):
  # Read csv file
  df = pd.read_csv(csv_file, delimiter=';', encoding='UTF-8')
  # df.columns = df.columns.str.strip().str.replace(r'\s+', '', regex=True)
  
  audios = []
  response_str = '\nThe audio file has been downloaded: '
  
  # search Youtube and download the audio file
  for index, row in df.iterrows():
    title = row['Title']
    artist = row['Artist']
    
    audio_file_path = download_song(title, artist)
    audios.append(audio_file_path)
    response_str += f'\n{title} by {artist} : {audio_file_path}'
  
  df['Audio'] = audios
  df = df.fillna('Not Found')
  print(df)
  
  df.to_csv(csv_file, index=False, encoding='UTF-8', sep=';')
  print(response_str)
  return response_str
    

if __name__ == '__main__':
  csv_file = 'playlist_csv/tvxq.csv'
  download_music_from_youtube(csv_file)