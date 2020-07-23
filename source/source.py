import pandas as pd
import tkinter.filedialog
import re

save_path = ''
open_path = ''


def open_file(file_path):
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


def add_columns(df):
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


def clean_keyword(keyword):
    if type(keyword) != str:
        return ''
    keyword = keyword.split(' ')
    keyword = list(filter(lambda word: not word.startswith('-'), keyword))
    return ' '.join(keyword)


def delete_negative_keywords(df):
    df['Keyword'] = df['Keyword'].apply(clean_keyword)
    return df


def broad_match_modifier(keyword):
    if type(keyword) != str or keyword == '':
        return ''
    keyword = keyword.split(' ')
    preps = ['в', 'на', 'под', 'из', 'с', 'от', 'у', 'и', 'за']
    for i in range(0, len(keyword)):
        if keyword[i] not in preps:
            keyword[i] = '+' + keyword[i]
    return ' '.join(keyword)


def modify_keyword(df):
    df['Keyword'] = df['Keyword'].apply(broad_match_modifier)
    return df


def save_file_path():
    global save_path
    save_path = tkinter.filedialog.askdirectory()


def write_to_csv(df):
    path = save_path + '/adwords.csv'
    df.to_csv(path, encoding='utf-16')


def open_file_dialog():
    global open_path
    open_path = tkinter.filedialog.askopenfilename()


def utm_cleaner(url):
    if type(url) != str:
        return ''
    return re.sub(r'.utm.*', '', url)


def delete_utm(df):
    df['Final URL'] = df['Final URL'].apply(utm_cleaner)
    return df


def add_keywords(df, cpc):
    keywords = df['Keyword'].tolist()
    df_keywords = pd.DataFrame(keywords, columns=['Keyword'])
    df_keywords['Campaign'] = df['Campaign']
    df_keywords['Adgroup'] = df['Adgroup']
    df_keywords['Max CPC'] = cpc
    df = df.append(df_keywords, ignore_index=True)
    return df


def add_negative_keywords(df):
    campaigns = df['Campaign'].tolist()

    df_negative = pd.DataFrame(campaigns, columns=['Campaign'])
    df_negative['Negative'] = df['Negative']
    df_negative = df_negative.dropna()
    df_negative = df_negative.drop_duplicates()

    negative_dict = df_negative.to_dict(orient='list')

    for i in range(len(negative_dict['Negative'])):
        negative_dict['Negative'][i] = negative_dict['Negative'][i].split(' -')

    negative_done = []
    for i in range(len(negative_dict['Campaign'])):
        for j in range(len(negative_dict['Negative'][i])):
            negative_done.append([negative_dict['Campaign'][i], negative_dict['Negative'][i][j]])

    df_negative_done = pd.DataFrame(negative_done, columns=['Campaign', 'Keyword'])
    df_negative_done['Criterion type'] = 'Campaign Negative Broad'

    df_negative_done['Keyword'] = df_negative_done['Keyword'].apply(delete_marks)

    df = df.append(df_negative_done, ignore_index=True)
    return df


def delete_marks(keyword):
    if type(keyword) != str or keyword == '':
        return ''
    return re.sub(r'[!+\[\]"]', '', keyword)


def delete_marks_keywords(df):
    df['Keyword'] = df['Keyword'].apply(delete_marks)
    return df


def convert_headline_template(headline):
    if type(headline) != str or headline == '':
        return ''

    headline = list(headline)

    if headline.count('#') == 2:
        counter = 0
        for i in range(len(headline)):
            if headline[i] == '#':
                if counter == 0:
                    headline[i] = '{Keyword:'
                    counter += 1
                elif counter == 1:
                    headline[i] = '}'
                    break

    return ''.join(headline)


def modify_headline(df):
    df['Headline 1'] = df['Headline 1'].apply(convert_headline_template)
    return df


def campaign_options_pack(df, geo_method, budget, tracking_template, schedule):

    def convert_schedule_data_to_int(data):
        converted_data = [[] for day in range(7)]
        for day in range(7):
            for hour in range(24):
                converted_data[day].append(data[day][hour].get())
        return converted_data

    def convert_int_schedule_data_to_ads(data):
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


def set_desc_line2(df, desc_line2):
    df['Description Line 2'] = desc_line2
    return df


def path_split(df):
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


def delete_extra_headline3_descline2(df):
    for i in range(len(df['Headline 1'])):
        if type(df['Headline 1'][i]) != str or df['Headline 1'][i] == '':
            df['Headline 3'][i] = ''
            df['Description Line 2'][i] = ''

    return df
