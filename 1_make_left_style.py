'''
時刻表の左側に表示する駅名一覧のためのHTMLを作成する
'''

import pandas as pd


df_station = pd.read_csv('input/setting_station.txt', header=0, sep='\t', encoding='utf-8', engine='python')

html_path = 'intermediate/left_style.html'  # 出力するファイル名（直接ファイルを読み込める場合はこちらを使用）
txt_path = 'intermediate/left_style.txt'  # 出力するファイル名（出力ファイルにleftの情報を埋め込む場合はこちらを使用）


with open(html_path, 'w', encoding='utf-8') as f:
    # HTMLの最初
    head = '''
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Table of Contents</title>
</head>\n
    '''
    f.write(head)

    #table_beg = '<table border="1" width="90%" style="margin: 0 5%; font-size: 24px;">\n</head>\n'
    #f.write(table_beg)
    body_beg = '<body style="font-family: Arial, sans-serif;">\n<nav>\n'
    f.write(body_beg)
    
    for i, row in df_station.iterrows():
        station_no = row['StationNo']  # str
        station_name = row['駅名']
        file_nk = row['File上下']
        file_n = row['File上り']
        file_k = row['File下り']

        station_link = []  # 駅名のリンクを格納するリスト
        file_list = []
        if pd.notna(file_nk):
            #print('nk', file_nk)
            # 上下が一緒の場合
            station_link.append(f'[{station_no}] {station_name}')
            file_list.append(file_nk)
        else:
            # 上下が別々の場合
            if pd.notna(file_n):
                #print('n', file_n)
                station_link.append(f'[{station_no}] {station_name}（上り）')
                file_list.append(file_n)
            if pd.notna(file_k):
                #print('k', file_k)
                station_link.append(f'[{station_no}] {station_name}（下り）')
                file_list.append(file_k)
            if file_n != 'nan' and file_k == 'nan':
                print(f'Error: {station_no} {station_name}')
        
        f.write('<ul>\n')
        for link, file in zip(station_link, file_list):
            f.write(f'<li><a href="駅時刻表{file}.html">{link}</a></li>\n')
        f.write('</ul>\n')

    tail = '</nav>\n</body>\n</html>'
    f.write(tail)

# 新幹線の路線名を書く駅リスト
line_list = dict()
line_list['明島'] = '北土・山土・東土新幹線'
line_list['米戸'] = '北土・東土新幹線'
line_list['実栗温泉'] = '北土新幹線'
line_list['市見台'] = '山土新幹線'
line_list['葉藪'] = '東土新幹線'


with open(txt_path, 'w') as f:
    f.write('<nav class="left">\n')
    for i, row in df_station.iterrows():
        station_no = row['StationNo']  # str
        station_name = row['駅名']
        file_nk = row['File上下']
        file_n = row['File上り']
        file_k = row['File下り']

        # station_nameがline_listのkeyに含まれる場合
        if station_name in line_list.keys():
            title = line_list[station_name]
            f.write(f'<b style="font-size: 18px">{title}</b>\n')

        station_link = []  # 駅名のリンクを格納するリスト
        file_list = []
        if pd.notna(file_nk):
            #print('nk', file_nk)
            # 上下が一緒の場合
            #station_link.append(f'[{station_no}] {station_name}')
            station_link.append('時刻')
            file_list.append(file_nk)
        else:
            # 上下が別々の場合
            if pd.notna(file_n):
                #print('n', file_n)
                #station_link.append(f'（上り）')
                station_link.append('上り')
                file_list.append(file_n)
            if pd.notna(file_k):
                #print('k', file_k)
                #station_link.append(f'[{station_no}] {station_name}（下り）')
                station_link.append('下り')
                file_list.append(file_k)
            if file_n != 'nan' and file_k == 'nan':
                print(f'Error: {station_no} {station_name}')
        
        f.write('<ul>\n')
        f.write(f'<li>[{station_no}] {station_name}')
        for link, file in zip(station_link, file_list):
            f.write(f' <a href="駅時刻表{file}.html">{link}</a>')
        f.write('</li>\n')
        f.write('</ul>\n')
    f.write('</nav>\n')