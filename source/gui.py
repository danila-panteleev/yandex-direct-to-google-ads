import logical as src
import tkinter as tk


def wrap():
    df = src.open_file(src.open_path)

    df = src.rename_columns(df)
    df = src.add_default_columns(df)

    df = src.delete_keyword_level_negative_keywords(df)
    df = src.delete_utm(df)
    df = src.convert_headline_templates(df)

    df = src.add_keywords_with_cpc(df, cpc_var.get())
    df = src.delete_marks_keywords(df)
    df = src.modify_keyword(df)

    df = src.add_negative_keywords(df)
    df = src.set_headline3(df, headline3_text_var.get())
    df = src.set_description_line2(df, description_line2_text_var.get())
    if path_split_checkbutton_var.get() == 1:
        df = src.path_split(df)
    df = src.campaign_options_pack(df,
                                   geo_checkbutton_var.get(),
                                   budget_var.get(),
                                   tt_var.get(),
                                   schedule_data,
                                   )
    df = src.delete_extra_headline3_description_line2(df)
    src.save_file_path()
    src.write_to_csv(df)


def ad_schedule():
    global schedule_data
    ad_schedule_window = tk.Toplevel(master=root)
    ad_schedule_window.title('Direct to Adwords | Расписание показов')
    ad_schedule_window.geometry('695x260')

    week = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']

    hours_1st_row = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
                     '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']

    hours_2nd_row = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
                     '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']

    for day in range(7):
        day_label = tk.Label(master=ad_schedule_window, text=week[day])
        day_label.grid(row=day, column=0)

    for hour in range(24):
        hour_label = tk.Label(master=ad_schedule_window, text=hours_1st_row[hour])
        hour_label.grid(row=7, column=hour + 1, sticky='w', padx=2)

    for hour in range(24):
        hour_label = tk.Label(master=ad_schedule_window, text=hours_2nd_row[hour])
        hour_label.grid(row=8, column=hour + 1, sticky='w', padx=2)

    for day in range(7):
        for hour in range(24):
            hour_checkbutton = tk.Checkbutton(master=ad_schedule_window, variable=schedule_data[day][hour])
            hour_checkbutton.grid(row=day, column=hour + 1)

    save_schedule_button = tk.Button(master=ad_schedule_window,
                                     text='Сохранить расписание',
                                     command=ad_schedule_window.destroy)

    save_schedule_button.grid(row=9, columnspan=26)


if __name__ == '__main__':

    root = tk.Tk()

    root.title('Direct to Adwords')
    root.geometry('800x490')

    frame_open_about_button = tk.Frame(master=root, width=700, height=70)

    about_button = tk.Button(master=frame_open_about_button, text='About')
    about_button.place(relx=0.95, rely=0.5, anchor='center')

    open_button = tk.Button(master=frame_open_about_button, text='Select file', command=src.open_file_dialog)
    open_button.place(rely=0.5, relx=0.5, anchor='center')

    frame_open_about_button.pack(fill=tk.BOTH, expand=True)

    frame_budget_cpc_geo_schedule = tk.Frame(master=root, width=700, height=70)

    frame_budget = tk.Frame(master=frame_budget_cpc_geo_schedule, width=200, height=70)
    budget_label = tk.Label(master=frame_budget, text='Ежедневный бюджет')
    budget_label.place(relx=0.5, rely=0.33, anchor='center')
    budget_var = tk.StringVar()
    budget_var.set('100')
    budget_input = tk.Entry(master=frame_budget, textvariable=budget_var)
    budget_input.place(relx=0.5, rely=0.66, anchor='center')
    frame_budget.place(relx=0.25, rely=0.5, anchor='e')

    frame_cpc = tk.Frame(master=frame_budget_cpc_geo_schedule, width=200, height=70)
    cpc_label = tk.Label(master=frame_cpc, text='Max CPC')
    cpc_label.place(relx=0.5, rely=0.33, anchor='center')
    cpc_var = tk.StringVar()
    cpc_var.set('1')
    cpc_input = tk.Entry(master=frame_cpc, textvariable=cpc_var)
    cpc_input.place(relx=0.5, rely=0.66, anchor='center')
    frame_cpc.place(relx=0.5, rely=0.5, anchor='e')

    frame_geo = tk.Frame(master=frame_budget_cpc_geo_schedule, width=200, height=70)
    geo_label = tk.Label(master=frame_geo, text='Расширенный геотаргетинг')
    geo_label.place(relx=0.5, rely=0.33, anchor='center')
    geo_checkbutton_var = tk.IntVar()
    geo_checkbutton_var.set(0)
    geo_checkbutton = tk.Checkbutton(master=frame_geo, variable=geo_checkbutton_var)
    geo_checkbutton.place(relx=0.5, rely=0.66, anchor='center')
    frame_geo.place(relx=0.75, rely=0.5, anchor='e')

    frame_schedule = tk.Frame(master=frame_budget_cpc_geo_schedule, width=200, height=70)
    schedule_data = [[tk.IntVar() for hour in range(24)] for day in range(7)]
    for day in range(7):
        for hour in range(24):
            schedule_data[day][hour].set(0)
    schedule_button = tk.Button(master=frame_schedule, text='Расписание показов', command=ad_schedule)
    schedule_button.place(relx=0.5, rely=0.5, anchor='center')
    frame_schedule.place(relx=1, rely=0.5, anchor='e')

    frame_budget_cpc_geo_schedule.pack(fill=tk.BOTH, expand=True)

    frame_tracking_template = tk.Frame(master=root, width=700, height=70)

    tt_label_frame = tk.Frame(master=frame_tracking_template, width=200, height=70)
    tt_label = tk.Label(master=tt_label_frame, text='Шаблон отслеживания')
    tt_label.place(relx=0.5, rely=0.5, anchor='center')
    tt_label_frame.place(relx=0.25, rely=0.5, anchor='e')

    tt_input_frame = tk.Frame(master=frame_tracking_template, width=600, height=70)
    tt_var = tk.StringVar()
    tt_var.set(
        "{lpurl}?utm_source=google&utm_medium=cpc&utm_campaign=cid|{campaignid}|{ifsearch:search}{ifcontent:context}"
        "&utm_content=gid|{adgroupid}|aid|{creative}|placement|{placement}&utm_term={keyword}")
    tt_input = tk.Entry(master=tt_input_frame, width=85, textvariable=tt_var)
    tt_input.place(relx=0.5, rely=0.5, anchor='center')
    tt_input_frame.place(relx=1, rely=0.5, anchor='e')

    frame_tracking_template.pack(fill=tk.BOTH, expand=True)

    frame_headline3 = tk.Frame(master=root, width=700, height=70)

    headline3_label_frame = tk.Frame(master=frame_headline3, width=200, height=70)
    headline3_label = tk.Label(master=headline3_label_frame, text='Заголовок 3')
    headline3_label.place(relx=0.5, rely=0.5, anchor='center')
    headline3_label_frame.place(relx=0.25, rely=0.5, anchor='e')

    headline3_input_frame = tk.Frame(master=frame_headline3, width=600, height=70)

    headline3_text_var = tk.StringVar()
    headline3_text_var.set('')
    headline3_input = tk.Entry(master=headline3_input_frame, width=85, textvariable=headline3_text_var)
    headline3_input.place(relx=0.5, rely=0.5, anchor='center')

    headline3_counter_var = tk.StringVar()
    headline3_counter_var.set('00')
    headline3_counter = tk.Label(master=headline3_input_frame, textvariable=headline3_counter_var)
    headline3_counter.place(relx=0.95, rely=0.5, anchor='center')

    headline3_input_frame.place(relx=1, rely=0.5, anchor='e')

    frame_headline3.pack(fill=tk.BOTH, expand=True)

    frame_description_line2 = tk.Frame(master=root, width=700, height=70)

    description_line2_label_frame = tk.Frame(master=frame_description_line2, width=200, height=70)
    description_line2_label = tk.Label(master=description_line2_label_frame, text='Строка описания 2')
    description_line2_label.place(relx=0.5, rely=0.5, anchor='center')
    description_line2_label_frame.place(relx=0.25, rely=0.5, anchor='e')

    description_line2_input_frame = tk.Frame(master=frame_description_line2, width=600, height=70)
    description_line2_text_var = tk.StringVar()
    description_line2_text_var.set('')
    description_line2_input = tk.Entry(master=description_line2_input_frame, width=85, textvariable=description_line2_text_var)
    description_line2_input.place(relx=0.5, rely=0.5, anchor='center')

    description_line2_counter_var = tk.StringVar()
    description_line2_counter_var.set('00')
    description_line2_counter = tk.Label(master=description_line2_input_frame, textvariable=description_line2_counter_var)
    description_line2_counter.place(relx=0.95, rely=0.5, anchor='center')

    description_line2_input_frame.place(relx=1, rely=0.5, anchor='e')

    frame_description_line2.pack(fill=tk.BOTH, expand=True)

    frame_path_split = tk.Frame(master=root, width=700, height=70)

    path_split_label = tk.Label(master=frame_path_split, text='Разбить отображаемую ссылку')
    path_split_label.place(relx=0.5, rely=0.33, anchor='center')
    path_split_checkbutton_var = tk.IntVar()
    path_split_checkbutton_var.set(0)
    path_split_checkbutton = tk.Checkbutton(master=frame_path_split, variable=path_split_checkbutton_var)
    path_split_checkbutton.place(relx=0.5, rely=0.66, anchor='center')

    frame_path_split.pack(fill=tk.BOTH, expand=True)

    frame_do_button = tk.Frame(master=root, width=700, height=70)
    do_button = tk.Button(frame_do_button, text='To adwords', command=wrap)
    do_button.place(rely=0.5, relx=0.5, anchor='center')
    frame_do_button.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
