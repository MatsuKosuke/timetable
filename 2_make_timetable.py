'''
timetable をpandasで読み込む．
ただし，行の名前は0行目から取得し，列の名前は0列目から取得する
何もないところはnan
'''

import pandas as pd
from collections import defaultdict
import time


start = time.time()

# ファイルの読み込み
df_tt_n = pd.read_csv('input/timetable_nobori.txt', header=0, sep='\t', encoding='utf-8', engine='python')
df_tt_k = pd.read_csv('input/timetable_kudari.txt', header=0, sep='\t', encoding='utf-8', engine='python')
df_setting_n = pd.read_csv('input/setting_nobori.txt', header=0, sep='\t', encoding='utf-8', engine='python')
df_setting_k = pd.read_csv('input/setting_kudari.txt', header=0, sep='\t', encoding='utf-8', engine='python')

# 使用する変数（まとめ）
df_tt = [df_tt_n, df_tt_k]  # 上りが0，下りが1
df_setting = [df_setting_n, df_setting_k]  # 上りが0，下りが1
df_station = pd.read_csv('input/setting_station.txt', header=0, sep='\t', encoding='utf-8', engine='python')


for i, row in df_station.iterrows():
    # 駅ごとに時刻表を作成
    station_num_int = row['駅番']
    station_num_str = row['StationNo']
    station_name = row['駅名']
    station_name_arab = row['駅名Eng']
    is_devide = False
    if row['上下'] == '別':
        is_devide = True
    nobori = [row['上り1'], row['上り2']]
    kudari = [row['下り1'], row['下り2']]
    nobori_dest = [row['上り1方面'], row['上り2方面']]
    kudari_dest = [row['下り1方面'], row['下り2方面']]
    # nanである要素を削除してリストにする
    nobori = [n for n in nobori if str(n) != 'nan']
    kudari = [k for k in kudari if str(k) != 'nan']
    nobori_dest = [n for n in nobori_dest if str(n) != 'nan']
    kudari_dest = [k for k in kudari_dest if str(k) != 'nan']
    # 両方向の列車番号を取得
    station_nums = [nobori, kudari]
    station_dest = [nobori_dest, kudari_dest]
    train_info_list = [[], []]  # 方向別の列車情報を格納するリスト (list of "train_info") 上りと下り

    # デバッグ用（特定の駅のみ実行）
    # if station_num_int != 55:
    #    continue



    for nk, df_setting_nk in enumerate(df_setting):  # nk: 0 or 1
        for uniq_station_num in station_nums[nk]:
            # df_settingの「駅番」列を参照し，station_numと一致する行を取得
            df_station_info = df_setting_nk[df_setting_nk['駅番'] == str(uniq_station_num)]

            # headerとvalueの辞書型に変換
            station_info = df_station_info.to_dict(orient='records')[0]  # {'駅番': '1', '駅名': '明島', ...}

            # 参照するキーを取得
            train_types_ref = [station_info['種別1'], station_info['種別2'], station_info['種別3']]
            destinations_ref = [station_info['終着1'], station_info['終着2'], station_info['終着3']]
            departures_ref = [station_info['始発1'], station_info['始発2'], station_info['始発3']]
            car_nums_ref = station_info['両数']
            station_code = station_info['符号発']
            #station_name = station_info['駅名']
            #station_name_arab = station_info['駅名Eng']
            train_num_ref = '号'


            train_info = []  # 列車情報を格納するリスト
            row_description = df_tt[nk]['行の説明']
            # for文でdfを列ごとに見ていく
            for i, (column_index, column) in enumerate(df_tt[nk].iteritems()):
                # row_descriptionとcolumnを結合する
                dep_tt = pd.concat([row_description, column], axis=1)
                station_dep = dep_tt[dep_tt['行の説明'] == station_code].values[0]  # 「行の説明」がstation_nameである行を取得
                if ':' in str(station_dep):
                    # station_depの1つ下の行のcolumnが「=」ならば，continue
                    if dep_tt.iloc[dep_tt[dep_tt['行の説明'] == station_code].index[0] + 1].values[1] == '=':
                        continue

                    # 時分を取得
                    hour, minute = station_dep[1].split(':')
                    # このときの行先，種別，両数を取得（それぞれ，df['行の説明'] が「終着11」「終着12」「終着13」，「種別11」「種別12」「種別13」，「両数10」である行にある）
                    destination = [dep_tt[dep_tt['行の説明'] == dest].values[0][1] for dest in destinations_ref if str(dest) != 'nan']
                    destination = [t for t in destination if str(t) != 'nan']  # 3つの行先のうち，NaNでない要素を結合してリストにする
                    departure = [dep_tt[dep_tt['行の説明'] == dest].values[0][1] for dest in departures_ref if str(dest) != 'nan']
                    departure = [t for t in departure if str(t) != 'nan']  # 3つの出発地のうち，NaNでない要素を結合してリストにする
                    train_type = [dep_tt[dep_tt['行の説明'] == ttype].values[0][1] for ttype in train_types_ref if str(ttype) != 'nan']
                    train_type = [t for t in train_type if str(t) != 'nan']  # 3つの種別のうち，NaNでない要素を結合してリストにする
                    car_num = dep_tt[dep_tt['行の説明'] == car_nums_ref].values[0][1]  # 両数
                    train_num = dep_tt[dep_tt['行の説明'] == train_num_ref].values[0][1]  # 列車番号

                    # 情報を辞書にしてリストに追加
                    train_info_0 = dict()
                    train_info_0['hour'] = int(hour)
                    train_info_0['minute'] = int(minute)
                    train_info_0['departure'] = departure
                    train_info_0['destination'] = destination
                    train_info_0['train_type'] = train_type
                    train_info_0['train_num'] = train_num
                    train_info_0['car_num'] = int(car_num)
                    train_info.append(train_info_0)
                    

            # train_infoをhourのintで昇順にソート（ただし，hourが同じ場合はminuteのintで昇順にソート）
            train_info.sort(key=lambda x: (x['hour'], x['minute']))
            #print(train_info)
            train_info_list[nk].append(train_info)




    # 列車の文字色を指定
    # みや：ピンク，わか：緑，すず：紫，たに：橙，のば：茶，つば：赤，ささ：水色，いぶ：明るい橙，ほた：青，こや：黒色
    train_color = dict()
    train_color['みや'] = 'F0E'  # ピンク
    train_color['わか'] = '090'  # 緑
    train_color['すず'] = 'B0E'  # 紫
    train_color['たに'] = 'D80'  # 橙
    train_color['のば'] = 'B20'  # 茶
    train_color['つば'] = 'F00'  # 赤
    train_color['ささ'] = '09F'  # 水色
    train_color['いぶ'] = 'E60'  # 明るい橙
    train_color['ほた'] = '33F'  # 青
    train_color['こや'] = '333'  # 黒色

    # 列車の正式名称の対応
    train_name = dict()
    train_name['みや'] = 'みやび'
    train_name['わか'] = 'わかば'
    train_name['すず'] = 'すずめ'
    train_name['たに'] = 'たにま'
    train_name['のば'] = 'のばな'
    train_name['つば'] = 'つばき'
    train_name['ささ'] = 'ささめ'
    train_name['いぶ'] = 'いぶき'
    train_name['ほた'] = 'ほたる'
    train_name['こや'] = 'こやり'

    # 列車本数のカウント用（デフォルトで0を代入）
    train_count = [[defaultdict(int), defaultdict(int)], [defaultdict(int), defaultdict(int)]]  # 上りと下り
    # 辞書型の順番を，上記の「みや」から「こや」までの順番にする
    for i in range(2):
        for j in range(2):
            for ttype in ['みや', 'わか', 'すず', 'たに', 'のば', 'つば', 'ささ', 'いぶ', 'ほた', 'こや', '計']:
                train_count[i][j][ttype] = 0

    # 保存するファイル名の例："tt_01_明島_下り.html"
    file_base_path = f'output/Station_{station_num_int:02d}_{station_name}'
    if is_devide:
        # 上下で分ける
        file_path = [file_base_path + '_上り.html', file_base_path + '_下り.html']
    else:
        # 上下を同じページにする
        file_path = [file_base_path + '.html']


    for nk, file in enumerate(file_path):
        # 上下で分けるなら，nk=0が上り，nk=1が下り．上下を同じページにするなら，nk=0のみ
        is_star = False  # 当駅始発がある場合はTrue
        with open(file, 'w') as f:
            add_text = ''
            if is_devide and nk == 0:
                add_text = '_上り'
            elif is_devide and nk == 1:
                add_text = '_下り'
            # HTMLの最初
            head = f'''
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{station_num_int:02d}_{station_name}{add_text}</title>
<link rel="stylesheet" type="text/css" href="../input/style_time_table.css">\n
            '''
            f.write(head)
            # style_time_table.cssを参照する

            body_beg = '<body style="font-family: Arial, sans-serif;">\n<div class="container">\n'
            f.write(body_beg)
            txt_path = 'intermediate/left_style.txt'
            for line in open(txt_path):
               f.write(line)
            f.write('<article class="right">\n')

            station_disp = f'<p style="margin: 0"><b style="font-size: 40px;">[{station_num_str}] {station_name}駅 </b>'+\
                            f'<b style="font-size: 28px;"> {station_name_arab} Station </b>'+\
                            f'<b style="font-size: 18px;"> ({station_num_int})</b></p>\n'
            f.write(station_disp)

            table_beg = '<table border="1" width="97%" style="margin: 0; font-size: 24px;">\n</head>\n'
            f.write(table_beg)

            # 表のヘッダ
            f.write('<tr>\n')
            f.write('<th bgcolor="#EEE" valign="top" width="50px" id="timetable">\n')
            f.write('時\n')
            f.write('</th>\n')
            train_info_dict = dict()
            if is_devide:
                train_info_dict[nk] = train_info_list[nk]
            else:
                train_info_dict[0] = train_info_list[0]
                train_info_dict[1] = train_info_list[1]

            # 辞書型をfor文で回すときは，items()を使う
            for p1, tid in train_info_dict.items():
                for k, _ in enumerate(tid):
                    nk_str = '上り' if p1 == 0 else '下り'
                    f.write('<th bgcolor="#EEE" valign="top" width="auto" id="timetable">\n')
                    dest_str = station_dest[p1][k]
                    f.write(f'{nk_str}: {dest_str}<span style="font-size: 18px;"> 方面</span>\n')
                    f.write('</th>\n')
            f.write('</tr>\n')


            one_train_info_list = []
            if is_devide:
                one_train_info_list = train_info_list[nk]
            else:
                one_train_info_list = train_info_list[0] + train_info_list[1]  # 上りと下りを結合

            # 表の中身
            for hour in range(6, 24):
                # 緑系：#DFD，#EFE
                # 桃系：#FDE，#FEE
                if hour % 2 == 0:
                    color = '#DFD'
                else:
                    color = '#EFE'
                f.write('<tr>\n')
                f.write(f'<td bgcolor="{color}" valign="top" align="center">\n')
                f.write(str(hour) + '\n')
                f.write('</td>\n')
                
                for ti, train_info in enumerate(one_train_info_list):
                    f.write(f'<td bgcolor="{color}" valign="top" style="padding-left: 2%">\n')
                    for train in train_info:
                        if train['hour'] == hour:
                            p2 = ti
                            if is_devide:
                                p1 = nk
                            else:
                                if ti < len(train_info_list[0]):
                                    # 上りなら
                                    p1 = 0
                                else:
                                    # 下りなら
                                    p1 = 1
                                    p2 -= len(train_info_list[0])
                                    
                            d_len = len(train['destination'])
                            t_len = len(train['train_type'])
                            f.write(f'<font color="#{train_color[train["train_type"][0]]}">')
                            ttype = train_name[train['train_type'][0]]
                            tnum = train['train_num']
                            dep_start = ''
                            if station_name in train['departure']:
                                dep_start = '★'
                                is_star = True
                            desti = dep_start + train['destination'][0]
                            train_count[p1][p2][train['train_type'][0]] += 1
                            train_count[p1][p2]['計'] += 1
                            if (d_len > 1 or t_len > 1) and train['train_type'][0] != train['train_type'][1]:
                                ttype += '・' + train_name[train['train_type'][1]]
                                train_count[p1][p2][train['train_type'][1]] += 1
                            if (d_len > 2 or t_len > 2) and train['train_type'][1] != train['train_type'][2]:
                                ttype += '・' + train_name[train['train_type'][2]]
                                train_count[p1][p2][train['train_type'][2]] += 1
                            if d_len > 1:
                                desti += '・' + train['destination'][1]
                            if d_len > 2:
                                desti += '・' + train['destination'][2]
                            desc = ttype + tnum + '号 ' + desti + '行 ' + str(train['car_num']) + '両'
                            # style_time_table.cssを使う
                            f.write(f'<span class="tooltip" data-tooltip="{desc}"><ul><li class="min">{train["minute"]:02d}</li><li class="desti">{desti}</li></ul></a></span> &nbsp; \n')

                    f.write('</td>\n')
                f.write('</tr>\n')
            #print(train_count)

            # 表の備考欄（列車本数を書く）※セルを2つ結合する
            f.write('<tr>\n')
            f.write(f'<td bgcolor="#EEE" valign="top" align="center">\n')
            f.write('</td>\n')


            loop_list = [0, 1]  # 1つめのfor文で回すリスト
            if is_devide:
                loop_list = [nk]
            #print('loop_list: ', loop_list)
            
            for ti in loop_list:
                loop_list2 = [0, 1]  # 2つめのfor文で回すリスト
                if len(station_nums[ti]) == 1:
                    loop_list2 = [0]
                #print('loop_list2: ', loop_list2)

                for p1 in loop_list2:
                    idx = ti if is_devide else p1
                    f.write(f'<td bgcolor="#EEE" valign="top" style="padding-left: 2%; font-size: 16px;">\n')
                    count_text = ''
                    for ttype, count in train_count[ti][p1].items():
                        if ttype == '計' or count == 0:
                            continue
                        count_text += f'<font color="#{train_color[ttype]}">{train_name[ttype]} {count}，'
                    count_text += f'<font color="#000">計{train_count[ti][p1]["計"]}本'
                    f.write(count_text)
                    f.write('</td>\n')


            # HTMLの最後
            table_end = '</table>\n'
            f.write(table_end)

            if is_star:
                star = '★：当駅始発'
                f.write(f'<p style="margin: 0; font-size: 16px;">{star}</p>\n')

            tail = '<article>\n</div>\n</body>\n</html>'
            f.write(tail)

end = time.time()
print(f'time: {(end - start):.2f} [sec]')