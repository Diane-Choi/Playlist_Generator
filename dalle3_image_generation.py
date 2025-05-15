import base64
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from utils.sanitize import sanitize_file_name
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def text_to_image_prompt_generator(song_title, artist):
  response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    temperature=0.5,
    messages=[
      {
        'role': 'system', 
        'content': """
          You are an AI assistant designed to create dalle-2 prompts.

          - When the user provides information about a song, imagine the song's lyrics and the representative image of its mood.
          - Based on the imagined image, generate a text prompt for the text-to-image model, dalle-2.
          - Be cautious not to mention the names of famous individuals or artists of the songs.
          - Avoid using words like 'gangster' or 'drug' or 'sensual'.
          - Avoid making racially discriminatory remarks.
          - Modify any violent or sexual content that is not suitable for children under the age of 15 to be expressed in a milder manner.
          """
      },
      {'role': 'user', 'content': 'Stronger - Kelly Clarkson'}, # Give an example 
      {'role': 'assistant', 'content': 'Create an image of a person standing on top of a mountain, surrounded by vibrant rays of sunlight, radiating confidence and strength.'}, # Give an example response
      {'role': 'user', 'content': f'{song_title} by {artist}'},
    ],
  )
  return response.choices[0].message.content

def generate_dalle_image(song_title, artist, size="512x512"):
  prompt = f'Create a Photo. {text_to_image_prompt_generator(song_title, artist)}'
  print(f"Prompt for {song_title} by {artist}: {prompt}")
  
  try:
    img = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size=size,
        response_format='b64_json'
    )
    
  except openai.error.RateLimitError as e:
    print(f"Rate limit error: {e}")
    return None
  except openai.error.APIError as e:
    print(f"OpenAI API error: {e}")
    return None
  except openai.error.APIConnectionError as e:
    print(f"Connection error: {e}")
    return None
  except openai.error.InvalidRequestError as e:
    print(f"Invalid request: {e}")
    return None
  except Exception as e:
    print(f"Unexpected error during image generation: {e}")
    return None
    
  image_bytes = base64.b64decode(img.data[0].b64_json)
  
  image_file_name = sanitize_file_name(f'{song_title}_{artist}')
  image_file_path = f"./images/{image_file_name}.png"
  
  folder_path = os.path.dirname(image_file_path)
  # create folder_path if not exists
  os.makedirs(folder_path, exist_ok=True)
  
  with open(image_file_path, "wb") as f:
      f.write(image_bytes)
      
  return image_file_path


if __name__ == '__main__':
  song_title = "One More Kiss"
  artist = "Dua Lipa"

  result = generate_dalle_image(song_title, artist)

  print(result)