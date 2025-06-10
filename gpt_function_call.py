import json
import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import tkinter.filedialog as filedialog
from youtube_audio_download import download_music_from_youtube
from generate_image import generate_images_for_songs
from generate_video import generate_video_using_images

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def save_to_csv(df):
    file_path = filedialog.asksaveasfile(defaultextension='.csv')
    if file_path:
        df.to_csv(file_path.name, sep=';', index=False, lineterminator='\n')
        return f'Successfully saved the file. The file path is: \n{file_path.name} \nWould you like to download the audio files for this playlist?', file_path.name
    return f'Canceled to save the file.', None

def save_playlist_as_csv(playlist_csv):
    if ';' in playlist_csv:
        response_lines = playlist_csv.strip().split('\n')
        csv_data = []
      
        for line in response_lines:
            if ';' in line:
                csv_data.append(line.split(';'))
          
        if len(csv_data) > 0:
            df = pd.DataFrame(csv_data[1:], columns=csv_data[0])
            return save_to_csv(df)
    return f'Failed to save the file. \n: {playlist_csv}', None
        
def ask_to_gpt_35_turbo(messages, functions, model='gpt-3.5-turbo', temperature=0.1):
    # GPT-3.5 Turbo 모델에 메시지를 보내 응답을 받는 함수
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    response_message = response.choices[0].message
    
    if response_message.function_call:
                # Step 3: call the function
        available_functions = {
            "save_playlist_as_csv": save_playlist_as_csv,
            "download_music_from_youtube": download_music_from_youtube,
            "generate_images_for_songs": generate_images_for_songs,
            "generate_video_using_images": generate_video_using_images,
        }
        function_name = response_message.function_call.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message.function_call.arguments)
        function_response = function_to_call(**function_args)
        
        if function_name == 'save_playlist_as_csv':
            function_response, csv_file_path = function_response
        
        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": f'{function_response,}',
            }
        )  # extend conversation with function response
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )  # get a new response from GPT where it can see the function response
    return response.choices[0].message.content

def main():
    def on_send():
        user_input = user_entry.get()  # 입력 필드에서 사용자 입력을  가져옴

        if user_input.lower() == 'quit':
            window.destroy()
            return

        messages.append(
            {'role': 'user', 'content': user_input},  # 사용자 메시지를 메시지 목록에 추가
        )

        chat_history.config(state=tk.NORMAL)  # 채팅 히스토리 텍스트 상태를 편집 가능한 상태로 변경
        chat_history.insert(tk.END, 'You: ' + user_input + '\n', 'user')  # 사용자 입력을 채팅 히스토리에 추가
        window.update_idletasks()

        thinking_popup = show_popup_message(window, 'Thinking...')
        
        response = ask_to_gpt_35_turbo(messages, functions)  # 메시지 목록을 GPT-3.5 Turbo 모델에 전달하여 응답 받음
        
        thinking_popup.destroy()

        messages.append(
            {'role': 'assistant', 'content': response},  # 응답을 메시지 목록에 추가
        )

        chat_history.insert(tk.END, 'Assistant: ' + response + '\n', 'assistant')  # 응답을 채팅 히스토리에 추가
        chat_history.config(state=tk.DISABLED)  # 채팅 히스토리 텍스트 상태를 읽기 전용 상태로 변경
        chat_history.see(tk.END)  # 채팅 히스토리 스크롤을 맨 아래로 이동

        user_entry.delete(0, tk.END)  # 입력 필드를 비움

    def show_popup_message(window, message):
        popup = tk.Toplevel(window)
        popup.title('GPT-3.5')

        label = tk.Label(popup, text=message)
        label.pack(expand=True, fill=tk.BOTH)

        popup_width = 400
        popup_height = 100

        popup.geometry(f'{popup_width}x{popup_height}')

        # 팝업 창 중앙 위치
        window_x = window.winfo_x()
        window_y = window.winfo_y()
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        popup_x = window_x + window_width // 2 - popup_width // 2
        popup_y = window_y + window_height // 2 - popup_height // 2
        popup.geometry(f'+{popup_x}+{popup_y}')

        popup.transient(window)
        popup.attributes('-topmost', True)
        popup.update()

        return popup

    window = tk.Tk()
    window.title("GPT Powered DJ")
    font = ('맑은 고딕', 10)

    chat_history = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED) 
    # chat_history = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, font=font)  # 채팅 히스토리를 보여주기 위한 텍스트 위젯 생성
    chat_history.configure(spacing1=3, spacing3=3)
    chat_history.tag_configure('user', background='#c9daf8')
    chat_history.tag_configure('assistant', background='#e4e4e4')
    chat_history.pack(fill=tk.BOTH, expand=True,  padx=10, pady=10)  # 텍스트 위젯을 윈도우에 배치

    input_frame = tk.Frame(window)  # 입력 필드와 전송 버튼을 담기 위한 프레임 생성
    input_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)  # 프레임을 윈도우에 배치

    user_entry = tk.Entry(input_frame)  # 사용자 입력을 받기 위한 입력 필드 생성
    user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)  # 입력 필드를 프레임에 배치

    send_button = tk.Button(input_frame, text="Send", command=on_send)  # 전송 버튼 생성
    send_button.pack(side=tk.RIGHT)  # 전송 버튼을 프레임에 배치

    window.bind('<Return>', lambda event: on_send())

    messages = [
        {'role': 'system', 'content': """
         You are a DJ assistant who creates playlists. 
         - At first, suggest songs to make a playlist based on users' request. The playlist must contain the title, artist, and release year of each song in a list format. You must ask the user if they want to save the playlist as follow: "Would you like to save this playlist as a CSV file?".
         - After saving the playlist as a CSV file, you must ask the users if they would like to download the MP3 files of the songs in the playlist.
         - After downloading the mp3 files for songs in the playlist, you must ask the users if they would like to generate album cover images for the each song.
         - After downloading the mp3 files in the playlist, you can generate a playlisst video using created album cover images. You should ask the users if they want to create the video.
         - After generating the video, you can say goodbye to the users or if they want another recommendation.
         """}, 
    ]
    
    functions = [
        {
            "name": "save_playlist_as_csv",
            "description": "This function can be called only when a user request to save a playlist into a CSV file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "playlist_csv": {
                        "type": "string",
                        "description": "A playlist in CSV format, separated by ';'. It must contain a header and the release year format should be 'YYYY'. The CSV format must start with a new line. The header of the CSV file must be in English and it should be formatted as follows: 'Title;Artist;Released'.",
                    },
                },
                "required": ["playlist_csv"],
            },
        },
        {
            "name": "download_music_from_youtube",
            "description": "Download mp3 of songs in the recent CSV file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "csv_file": {
                        "type": "string",
                        "description": "A file path of the recent CSV file.",
                    },
                },
                "required": ["csv_file"],
            },
        },
        {
            "name": "generate_images_for_songs",
            "description": "Generate images for the songs in the recent CSV file. This function can be used only after downloading audio files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "csv_file": {
                        "type": "string",
                        "description": "A file path of the recent CSV file.",
                    },
                },
                "required": ["csv_file"],
            },
        },
        {
            "name": "generate_video_using_images",
            "description": "Generate a playlist video using the created images. This function can be used only after images are created.",
            "parameters": {
                "type": "object",
                "properties": {
                    "csv_file": {
                        "type": "string",
                        "description": "A file path of the recent CSV file.",
                    },
                },
                "required": ["csv_file"],
            },
        }  
    ]


    window.mainloop()


if __name__ == '__main__':
    global csv_file_path
    main()