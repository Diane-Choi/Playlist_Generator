from PIL import Image, ImageDraw, ImageFont
import os

def add_info_to_file_path(file_path, info_string):
    """Creates a new file path by appending info str to the original file path.

    Args:
        file_path (str): The original image file path.
        info_string (str): String to append to the file name.
        
    Returns:
        str: New file path with info str appended.
    """
    
    base_name, file_extension = os.path.splitext(file_path)
    new_file_path = f"{base_name}{info_string}{file_extension}"

    return new_file_path

def add_text_border(draw, text, position, font, fill, border_width, border_color):
    """Draws text with a border effect on the image.
    
    Args:
        draw (ImageDraw.Draw): The drawing context.
        text (str): The text to draw.
        position (tuple): x, y coordinates for the text position.
        font (ImageFont.FreeTypeFont): Font to use for the text.
        fill (tuple): Text color in RGB.
        border_width (int): Width of the text border.
        border_color (tuple): border color in RGB.
    """
    x, y = position
    for x_offset in range(-border_width, border_width + 1):
        for y_offset in range(-border_width, border_width + 1):
            draw.text((x + x_offset, y + y_offset), text, font=font, fill=border_color)
    
    draw.text((x, y), text, font=font, fill=fill)

def create_album_art(image_path, title, artist, output_path='__info'):
    """Adds song title and artist name to an image of album art and saves it as a new file.
    
    Args:
        image_path (str): A path to the original image of album art.
        title (str): Song title to overlay.
        artist (str): Artist name to overlay.
        output_path (str): Str to append to the saved image file name.
        
    Returns:
        str: Output path.
    """
    album_art = Image.open(image_path)
    width, height = album_art.size

    font_size_title = int(min(width, height) * 0.08)
    font_size_artist = int(min(width, height) * 0.05)

    # using font for mac
    title_font = ImageFont.truetype("/Library/Fonts/Supplemetal/AppleGothic.ttf", font_size_title)
    artist_font = ImageFont.truetype("/Library/Fonts/Supplemetal/AppleGothic.ttf", font_size_artist)

    draw = ImageDraw.Draw(album_art)

    outline_color = (0, 0, 0)
    outline_width = int(width * 0.01)

    max_text_width = width * 0.9
    
    while title_font.getlength(title) > max_text_width:
        font_size_title -= 1
        title_font = ImageFont.truetype("/Library/Fonts/Supplemetal/AppleGothic.ttf", font_size_title)
        
    while artist_font.getlength(artist) > max_text_width:
        font_size_artist -= 1
        artist_font = ImageFont.truetype("/Library/Fonts/Supplemetal/AppleGothic.ttf", font_size_artist)

    title_width = title_font.getlength(title)
    title_x = width * 0.5 - title_width * 0.5
    title_y = height * 0.7
    title_color = (255, 255, 255)  # white

    artist_width = artist_font.getlength(artist)
    artist_x = width * 0.5 - artist_width * 0.5
    artist_y = title_y + font_size_title + height * 0.015
    artist_color = (255, 255, 255)  # white

    add_text_border(draw, title, (title_x, title_y), title_font, title_color, outline_width, outline_color)
    add_text_border(draw, artist, (artist_x, artist_y), artist_font, artist_color, outline_width, outline_color)

    output_path = add_info_to_file_path(image_path, '__info')

    album_art.save(output_path)
    
    return output_path


# if __name__ == '__main__':
#     create_album_art(
#         "/Users/dianna/Desktop/CST/After/Playlist_Generator/images/Lucifer_SHINee.png", 
#         "Lucifer", 
#         "Shinee", 
#     )
