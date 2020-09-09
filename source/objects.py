from abc import ABC

import pandas as pd
import re


class ExportFile:

    def __init__(self, path):
        self = pd.read_csv(filepath_or_buffer=path,
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

    def rename_columns(self):
        """
        rename columns: Yandex -> Google
        """
        self = self.rename(columns={'Название группы': 'Adgroup',
                                    'Название кампании': 'Campaign',
                                    'Фраза (с минус-словами)': 'Keyword',
                                    'Заголовок 1': 'Headline 1',
                                    'Заголовок 2': 'Headline 2',
                                    'Текст': 'Description line 1',
                                    'Ссылка': 'Final URL',
                                    'Отображаемая ссылка': 'Path 1',
                                    'Минус-фразы на кампанию': 'Negative'})

    def delete_negative_keywords(self):
        """
        delete keyword-level negative keywords
        example: 'купить пиццу -дешево -быстро' -> 'купить пиццу'
        """
        for i in range(len(self['Keyword'])):
            if type(self['Keyword'][i]) != str:
                pass
            else:
                keyword = self['Keyword'][i].split(' ')
                keyword = list(filter(lambda word: not word.startswith('-'), keyword))
                self['Keyword'][i] = ' '.join(keyword)

    def delete_utm(self):
        """
        delete utm from urls
        """
        for i in range(len(self['Final URL'])):
            if type(self['Final URL'][i]) != str:
                pass
            else:
                self['Final URL'][i] = re.sub(r'utm.*', '', self['Final URL'][i])

        # add keywords with cpc
        df_keywords = pd.DataFrame
        df_keywords['Keywords'] = self['Keywords']
        df_keywords['Campaign'] = self['Campaign']
        df_keywords['Adgroup'] = self['Adgroup']
        df_keywords['Max CPC'] = cpc
        self = self.append(df_keywords, ignore_index=True)

        # delete utm from urls
        for i in range(len(self['Final URL'])):
            if type(self['Final URL'][i]) != str:
                pass
            else:
                self['Final URL'][i] = re.sub(r'utm.*', '', self['Final URL'][i])

        # convert headline templates
        # example: #Купить пиццу#! -> {Keyword:Купить пиццу}!
        for i in range(len(self['Headline 1'])):
            if type(self['Headline 1'][i]) != str:
                pass
            else:
                headline = self['Headline 1'][i]
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
        self['Headline 1'][i] = ''.join(headline)
