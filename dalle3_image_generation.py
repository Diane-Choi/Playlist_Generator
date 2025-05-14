import base64
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_dalle_image(prompt, image_file_name, size="512x512"):
  img = client.images.generate(
      model="dall-e-2",
      prompt=prompt,
      n=1,
      size=size,
      response_format='b64_json'
  )

  image_bytes = base64.b64decode(img.data[0].b64_json)
  
  image_file_path = f"./images/{image_file_name}.png"
  
  folder_path = os.path.dirname(image_file_path)
  # create folder_path if not exists
  os.makedirs(folder_path, exist_ok=True)
  
  with open(image_file_path, "wb") as f:
      f.write(image_bytes)
      
  return image_file_path

result = generate_dalle_image("A baby eating subway cookie", "sss")
print(result)