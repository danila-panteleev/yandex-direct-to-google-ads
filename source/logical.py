import pandas as pd
import tkinter.filedialog
import re

save_path = ''
open_path = ''


def open_file(file_path):
    """
    Открыть файл экспорта из Директ Коммандера как DataFrame
    :param file_path: путь к файлу
    :return: DataFrame
    """
    return pd.read_csv(file_path,
                       sep='\t',
                       encoding='utf-16',
                       header=1,
                       usecols=['Название кампании',
                                'Название группы',
                                'Ссылка',
                                'Фраза (с минус-словами)',
                                'Заголовок 1',
                                'Заголовок 2',
                                'Текст',
                                'Отображаемая ссылка',
                                'Минус-фразы на кампанию'
                                ])


def rename_columns(df):
    """
    Переименовать колонки DataFrame таблицы в формат Google Ads Editor
    :param df: DataFrame, полученный из функции open_file
    :return: DataFrame
    """
    df = df.rename(columns={'Название группы': 'Adgroup',
                            'Название кампании': 'Campaign',
                            'Фраза (с минус-словами)': 'Keyword',
                            'Заголовок 1': 'Headline 1',
                            'Заголовок 2': 'Headline 2',
                            'Текст': 'Description line 1',
                            'Ссылка': 'Final URL',
                            'Отображаемая ссылка': 'Path 1',
                            'Минус-фразы на кампанию': 'Negative'})
    return df


def add_default_columns(df):
    """
    Добавить минимальный набор столбцов по умолчанию
    :param df: DataFrame
    :return: DataFrame
    """
    df['Labels'] = ''
    df['Budget'] = '100'
    df['Budget type'] = 'Daily'
    df['Campaign Type'] = 'Search'
    df['Networks'] = 'Google search'
    df['Languages'] = 'All'
    df['Bid Strategy Type'] = 'Manual CPC'
    df['Bid Strategy Name'] = ''
    df['Enhanced CPC'] = 'Disabled'
    df['Start Date'] = '[]'
    df['End Date'] = '[]'
    df['Ad Schedule'] = '[]'
    df['Ad rotation'] = 'Optimize for clicks'
    df['Delivery method'] = ''
    df['Targeting method'] = 'Location of presence'
    df['Exclusion method'] = ''
    df['DSA Website'] = ''
    df['DSA Language'] = ''
    df['DSA targeting source'] = 'Google'
    df['DSA page feeds'] = ''
    df['Merchant Identifier'] = ''
    df['Country of Sale'] = ''
    df['Campaign Priority'] = ''
    df['Local Inventory Ads'] = 'Disabled'
    df['Inventory filter'] = '*'
    df['Flexible Reach'] = ''
    df['Tracking template'] = ''
    df['Max CPC'] = '1'
    df['Max CPM'] = '0.01'
    df['Target CPA'] = ''
    df['Max CPV'] = ''
    df['Target CPM'] = '0.01'
    df['Target ROAS'] = ''
    df['Desktop Bid Modifier'] = ''
    df['Mobile Bid Modifier'] = ''
    df['Tablet Bid Modifier'] = ''
    df['TV Screen Bid Modifier'] = ''
    df['Top Content Bid Modifier'] = ''
    df['Display Network Custom Bid Type'] = ''
    df['Targeting expansion'] = ''
    df['Ad Group Type'] = ''
    df['Final URL suffix'] = ''
    df['Custom parameters'] = ''
    df['Age'] = ''
    df['Bid Modifier'] = ''
    df['Final mobile URL'] = ''
    df['ID'] = ''
    df['Location'] = ''
    df['Reach'] = ''
    df['Feed'] = ''
    df['Radius'] = ''
    df['Unit'] = ''
    df['Criterion Type'] = ''
    df['First page bid'] = ''
    df['Top of page bid'] = ''
    df['First position bid'] = ''
    df['Quality score'] = ''
    df['Landing page experience'] = ''
    df['Expected CTR'] = ''
    df['Ad relevance'] = ''
    df['Ad type'] = 'Expanded text ad'
    df['Headline 3'] = ''
    df['Description Line 2'] = ''
    df['Path 2'] = ''
    df['Campaign Status'] = 'Enabled'
    df['Ad Group Status'] = 'Enabled'
    df['Status'] = 'Enabled'
    df['Approval Status'] = 'Enabled'
    df['Comment'] = ''
    return df


def delete_keyword_level_negative_keywords(df):
    """
    Удалить минус-слова на уровне ключевых фраз
    Пример: 'купить пиццу -дешево -быстро' -> 'купить пиццу'
    :param df: DataFrame
    :return: DataFrame
    """
    for i in range(len(df['Keyword'])):

        if type(df['Keyword'][i]) == str:
            keyword = df['Keyword'][i].split(' ')
            keyword = list(filter(lambda word: not word.startswith('-'), keyword))
            df['Keyword'][i] = ' '.join(keyword)

    return df


def modify_keyword(df, preps=['в', 'на', 'под', 'из', 'с', 'от', 'у', 'и', 'за']):
    """
    Добавить '+' к каждому слову в ключевых фразах, кроме предлогов, определенных в переменной preps
    Пример: 'купить пиццу с сыром' -> '+купить +пиццу с +сыром'
    :param preps: список предлогов
    :param df: DataFrame
    :return: DataFrame
    """
    for i in range(len(df['Keyword'])):

        if type(df['Keyword'][i]) == str:
            keyword = df['Keyword'][i].split(' ')

            for j in range(len(keyword)):
                if keyword[j] not in preps:
                    keyword[j] = '+' + keyword[j]

            df['Keyword'][i] = ' '.join(keyword)

    return df


def save_file_path():
    """
    Вызвать окно Tkinter для запроса пути сохранения файла
    Сохранить пути в глобальную переменную save_path
    :return: None
    """
    global save_path
    save_path = tkinter.filedialog.askdirectory()


def write_to_csv(df, file_name='adwords'):
    """
    Созранить DataFrame в csv utf-16
    Путь для файла берется из глобальной переменной save_path
    :param file_name: имя файла
    :param df: DataFrame
    :return: None
    """
    path = save_path + f'/{file_name}.csv'
    df.to_csv(path, encoding='utf-16')


def open_file_dialog():
    """
    Вызвать окно Tkinter для запроса пути открытия файла экспорта Директ Коммандера
    :return: None
    """
    global open_path
    open_path = tkinter.filedialog.askopenfilename()


def delete_utm(df):
    """
    Удалить UTM-метки из ссылок в объявлениях
    Пример: 'example.com?utm_medium=cpc&utm_source=yandex' -> 'example.com'
    :param df: DataFrame
    :return: DataFrame
    """
    for i in range(len(df['Final URL'])):
        if type(df['Final URL'][i]) == str:
            df['Final URL'][i] = re.sub(r'.utm.*', '', df['Final URL'][i])

    return df


def add_keywords_with_cpc(df, cpc='1'):
    """
    Добавить ключевые фразы в низ таблицы DataFrame со значением Max CPC для каждого (Макс. цена клика)
    :param df: DataFrame
    :param cpc: Max CPC (макс. цена клика)
    :return: DataFrame
    """
    df_keywords = pd.DataFrame(df, columns=['Keyword', 'Campaign', 'Adgroup'])
    df_keywords = df_keywords.dropna()
    df_keywords = df_keywords.drop_duplicates()
    df_keywords['Max CPC'] = cpc

    df = df.append(df_keywords, ignore_index=True)

    return df


def add_negative_keywords(df):
    """
    Конвертировать минус-слова на уровне кампании в формат Google Ads Editor
    :param df: DataFrame
    :return: DataFrame
    """
    df_negative = pd.DataFrame(df, columns=['Campaign', 'Negative'])

    df_negative = df_negative.dropna()
    df_negative = df_negative.drop_duplicates()
    df_negative = df_negative.reset_index()

    negative_done = []

    for campaign_index in range(len(df_negative['Campaign'])):
        negative_words = df_negative['Negative'][campaign_index].split(' -')

        for negative_words_index in range(len(negative_words)):
            negative_done.append([df_negative['Campaign'][campaign_index], negative_words[negative_words_index]])

    df_negative_done = pd.DataFrame(negative_done, columns=['Campaign', 'Keyword'])
    df_negative_done['Criterion type'] = 'Campaign Negative Broad'
    df_negative_done['Keyword'] = df_negative_done['Keyword'].apply(delete_marks)

    df = df.append(df_negative_done, ignore_index=True)
    return df


def delete_marks(keyword):
    """ 
    Удаляить оператор из ключевой фразы
    :param keyword: str
    :return: str without marks
    """
    if type(keyword) != str or keyword == '':
        return ''

    return re.sub(r'[!+\[\]"]', '', keyword)


def delete_marks_keywords(df):
    """
    Применить функцию delete_marks к значениям в столбце Keyword
    :param df: DataFrame
    :return: DataFrame
    """
    df['Keyword'] = df['Keyword'].apply(delete_marks)
    return df


def convert_headline_templates(df):
    """
    Привести шаблоны в заголовках к формату Google Ads
    Example: '#Купить пиццу#!' -> '{Keyword:Купить пиццу}!'
    :param df: DataFrame
    :return: DataFrame
    """
    for i in range(len(df['Headline 1'])):
        if type(df['Headline 1'][i]) == str or df['Headline 1'][i] != '':
            headline = list(df['Headline 1'][i])
            if headline.count('#') == 2:
                counter = 0
                for j in range(len(headline)):
                    if headline[j] == '#':
                        if counter == 0:
                            headline[j] = '{Keyword:'
                            counter += 1
                        elif counter == 1:
                            headline[j] = '}'
                            break
            df['Headline 1'][i] = ''.join(headline)

    return df


def campaign_options_pack(df, geo_method, budget, tracking_template, schedule):
    """
    Обработать настройки кампаний, добавить их в верх DataFrame
    :param df: DataFrame
    :param geo_method: int, расширенный геотаргетинг, 0 (выкл) или 1 (вкл)
    :param budget: numeric, ежедневный бюджет кампании
    :param tracking_template: str, шаблон отслеживания
    :param schedule: 2D list with tk.IntVar() values, почасовое расписание показов на неделю
    :return: df
    """

    def convert_schedule_data_to_int(data):
        """
        Конвертировать 2D лист со значениями tk.IntVar() в формать 0 или 1
        :param data: значения tk.IntVar() данных в 2D списке
        :return: 2D список со значениями 0 или 1
        """
        converted_data = [[] for day in range(7)]
        
        for day in range(7):
            for hour in range(24):
                converted_data[day].append(data[day][hour].get())
                
        return converted_data

    def convert_int_schedule_data_to_ads(data):
        """
        Конвертировать 2D список со значениями 0 или 1 в формат расписания показов Google Ads Editor
        :param data: 2D список со значениями 0 или 1
        :return: str, расписание показов формата Google Ads Editor
        """
        week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday', 'Sunday']
        schedule_done = []
        schedule_hours = [[[]]]
        
        for day in range(7):
            for hour in range(24):
                if data[day][hour] == 1:
                    data[day][hour] = hour
            data[day] = list(filter(lambda x: x != 0, data[day]))

        for day in range(len(data)):
            schedule_hours.append([[]])
            
            for i in range(len(data[day])):
                if i == 0:
                    schedule_hours[day][i].append(data[day][i])
                    
                elif data[day][i] - data[day][i - 1] == 1:
                    schedule_hours[day][len(schedule_hours[day]) - 1].append(data[day][i])
                    
                elif data[day][i] - data[day][i - 1] != 1:
                    schedule_hours[day].append([])
                    schedule_hours[day][len(schedule_hours[day]) - 1].append(data[day][i])

        for day in range(len(schedule_hours) - 1):
            if data[day]:
                for i in range(len(schedule_hours[day])):
                    schedule_done.append(
                        f'({week[day]}[{min(schedule_hours[day][i])}:00-{max(schedule_hours[day][i]) + 1}:00])')

        schedule_done = ';'.join(schedule_done)

        return schedule_done

    int_schedule_data = convert_schedule_data_to_int(schedule)
    schedule_data_done = convert_int_schedule_data_to_ads(int_schedule_data)

    df_campaigns = pd.DataFrame(df['Campaign'])
    df_campaigns = df_campaigns.dropna()
    df_campaigns = df_campaigns.drop_duplicates()
    df_campaigns['Budget'] = budget
    df_campaigns['Budget type'] = 'Daily'
    df_campaigns['Campaign Type'] = 'Search'
    df_campaigns['Networks'] = 'Google search'
    df_campaigns['Languages'] = 'All'
    df_campaigns['Bid Strategy Type'] = 'Manual CPC'
    df_campaigns['Enhanced CPC'] = 'Disabled'
    df_campaigns['Start Date'] = '[]'
    df_campaigns['End Date'] = '[]'
    df_campaigns['Ad Schedule'] = schedule_data_done
    df_campaigns['Ad rotation'] = 'Optimize for clicks'
    df_campaigns['Delivery method'] = ''
    if geo_method == 1:
        df_campaigns['Targeting method'] = 'Location of presence or Area of interest'
    elif geo_method == 0:
        df_campaigns['Targeting method'] = 'Location of presence'
    df_campaigns['Exclusion method'] = ''
    df_campaigns['DSA targeting source'] = 'Google'
    df_campaigns['Campaign Priority'] = 'Low'
    df_campaigns['Local Inventory Ads'] = 'Disabled'
    df_campaigns['Inventory filter'] = '*'
    df_campaigns['Tracking template'] = tracking_template

    df = pd.concat([df_campaigns, df], ignore_index=True)
    
    return df


def set_headline3(df, headline3):
    df['Headline 3'] = headline3
    return df


def set_description_line2(df, description_line2):
    df['Description Line 2'] = description_line2
    return df


def path_split(df):
    """
    Разбить отображаемую ссылку если она длинее, чем 15 знаков и если она разделена '-' или '_'
    на 'Путь 1' и 'Путь 2'
    :param df: DataFrame
    :return: DataFrame
    """
    for i in range(len(df['Path 1'])):
        if type(df['Path 1'][i]) == str:
            if len(df['Path 1'][i]) > 15:
                
                if '-' in df['Path 1'][i] and df['Path 1'][i].count('-') < 2:
                    splitted = df['Path 1'][i].split('-')
                    df['Path 1'][i] = splitted[0]
                    df['Path 2'][i] = splitted[1]
                    
                elif '_' in df['Path 1'][i] and df['Path 1'][i].count('_') < 2:
                    splitted = df['Path 1'][i].split('_')
                    df['Path 1'][i] = splitted[0]
                    df['Path 2'][i] = splitted[1]

    return df


def delete_extra_headline3_description_line2(df):
    """
    Удалить лишние строки, в которых есть только значения "Заголовок 3" и "Строка описания 2"
    :param df: DataFrame
    :return: DataFrame
    """
    for i in range(len(df['Headline 1'])):
        if type(df['Headline 1'][i]) != str or df['Headline 1'][i] == '':
            df['Headline 3'][i] = ''
            df['Description Line 2'][i] = ''

    return df
