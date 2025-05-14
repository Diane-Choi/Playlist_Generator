import pandas as pd

strings = """
요청하신 플레이리스트입니다.

Title;Artist;Released
Dynamite;BTS;2020
Gangnam Style;PSY;2010
Good Day;IU;2023

어떤가요?
"""

def extract_csv_to_dataframe(response):
    if ';' in response:
      response_lines = response.strip().split('\n')
      csv_data = []
      
      for line in response_lines:
        if ';' in line:
          csv_data.append(line.split(';'))
          
      if len(csv_data) > 0:
        df = pd.DataFrame(csv_data[1:], columns=csv_data[0])
        return df
    else:
      return None
    
# df = extract_csv_to_dataframe(strings)
# print(df)