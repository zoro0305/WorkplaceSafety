#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   company_search.py
@Time    :   2023/03/26 20:04:15
@Author  :   Zoro Chang
'''

import streamlit as st
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

from Home import background

class company_search():
    def _company_search(self, unit: str):
        ######違反勞動法令紀錄
        url1 = "https://announcement.mol.gov.tw/"

        data1 = {
            "UNITNAME": unit
        }
        response = requests.post(url1, data=data1)
        html = response.text

        # 使用 BeautifulSoup 解析頁面内容
        soup = BeautifulSoup(html, "html.parser")

        for td in soup.find_all('td', class_='column10'):
            td.extract()

        titles=[]
        for title in soup.find_all(class_="col-xs-12 form-group lawTitle"):
            titles.append(title.text.strip())

        cases =[]
        for case in soup.find_all('tbody'):
            case_list = str(case).replace("\n", "").replace("<br/>", "\n").split("</td>")
            case_list = [_.split(">")[1].strip() for _ in case_list]
            while "<tr" in case_list:
                case_list.remove("<tr")
            while '</tbody' in case_list:
                case_list.remove('</tbody')
            while '<tr class="noDataBorder"' in case_list:
                case_list.remove('<tr class="noDataBorder"')
            cases.append(case_list)

        results=[]
        results.append([cases[0][x:x+8] for x in range(0, len(cases[0]), 8)])
        results.append([cases[1][x:x+7] for x in range(0, len(cases[1]), 7)])
        results.append([cases[2][x:x+8] for x in range(0, len(cases[2]), 8)])

        df1_1 = pd.DataFrame(results[0])
        if not df1_1.empty:
            df1_1[0] = [titles[0] for _ in range(len(df1_1[0]))]
            df1_1 = df1_1.drop(columns=[0,1,3])
            df1_1 = df1_1.rename(columns={2: '處分日期', 4: "事業單位名稱(負責人) / 自然人姓名",
                                        5: "違法法規法條 ", 6: "違反法規內容", 7: "罰鍰金額"})
        df1_2 = pd.DataFrame(results[1])
        if not df1_2.empty:
            df1_2[0] = [titles[1] for _ in range(len(df1_2[0]))]
            df1_2 = df1_2.drop(columns=[0,1,3])
            df1_2 = df1_2.rename(columns={2: '處分日期', 4: "事業單位名稱(負責人) / 自然人姓名",
                                        5: "違法法規法條 ", 6: "違反法規內容"})
        df1_3 = pd.DataFrame(results[2])
        if not df1_3.empty:
            df1_3[0] = [titles[2] for _ in range(len(df1_3[0]))]
            df1_3 = df1_3.drop(columns=[0,1,3])
            df1_3 = df1_3.rename(columns={2: '處分日期', 4: "事業單位名稱(負責人) / 自然人姓名",
                                        5: "違法法規法條 ", 6: "違反法規內容", 7: "處分金額／滯納金"})

        ######重大職業災害紀錄
        url2 = "https://pacs.osha.gov.tw/2875/"

        data2 = {
            "q": unit
        }
        response = requests.get(url2, params=data2)
        html = response.text

        # 使用 BeautifulSoup 解析頁面内容
        soup = BeautifulSoup(html, "html.parser")

        events = []
        for event in soup.find_all('div', {'class': 'publiclist'}):
            events.append(event.text.strip())

        times, companies, owners, places, addresses, disasters = [], [], [], [], [], []
        for event in events:
            try:
                time_pattern = r'發生日期：(.*)\n'
                time_match = re.search(time_pattern, event)
                times.append(time_match.group(1))
            except:
                times.append("")
            try:
                company_pattern = r'事業單位：(.*)\n'
                company_match = re.search(company_pattern, event)
                companies.append(company_match.group(1))
            except:
                companies.append("")
            try:
                owner_pattern = r'業主：(.*)\n'
                owner_match = re.search(owner_pattern, event)
                owners.append(owner_match.group(1))
            except:
                owners.append("")
            try:
                place_pattern = r'場所(.*)\n'
                place_match = re.search(place_pattern, event)
                places.append(place_match.group(1)[5:])
            except:
                places.append("")
            try:
                address_pattern = r'地址(.*)\n'
                address_match = re.search(address_pattern, event)
                addresses.append(address_match.group(1))
            except:
                addresses.append("")
            try:
                disaster_pattern = r'災害類型：(.*)\n'
                disaster_match = re.search(disaster_pattern, event)
                disasters.append(disaster_match.group(1))
            except:
                disasters.append("")

        df2 = pd.DataFrame()
        if times:
            df2 = pd.DataFrame({'發生日期': times, '事業單位': companies, '業主': owners,
                                '場所(肇災處)': places, '地址': addresses, '災害類型': disasters})

        ######職業衛生安全紀錄
        url3 = "https://pacs.osha.gov.tw/2872/"

        data3 = {
            "q": unit
        }
        response = requests.get(url3, params=data3)
        html = response.text

        # 使用 BeautifulSoup 解析頁面内容
        soup = BeautifulSoup(html, "html.parser")

        events = []
        for event in soup.find_all('tr'):
            events.append(event.text.strip())

        events = events[1:]
        years, prizes, companies = [], [], []
        for event in events:
            event = event.split("\n")
            event = [_ for _ in event if _ != ""]
            years.append(event[1])
            prizes.append(event[2])
            companies.append(event[3])

        df3 = pd.DataFrame()
        if years:
            df3 = pd.DataFrame({'企業名稱': companies, '獲獎年度': years, '獲獎名稱': prizes})

        return df1_1, df1_2, df1_3, df2, df3

    def customized_df(self, df: pd.DataFrame):
        def background_color(val):
            return f'background-color: PapayaWhip'
        return df.style.set_properties(color='Black').applymap(background_color)

    def main(self):
        background("scripts/background.jpg").set_bg_hack()
        st.markdown("<p style='font-family:Courier; font-size: 35px; color: SaddleBrown;'>\
                    <b>職災ㄨㄚ熊災🐻－職場安全資訊攏底加！</b></p>", unsafe_allow_html=True)
        unit = st.text_input('輸入 自然人姓名/事業單位名稱: ', "")
        if unit:
            df1_1, df1_2, df1_3, df2, df3 = self._company_search(unit)
            st.markdown("<p style='font-family:Courier; font-size: 15px; color: Peru;'>\
                        <b>近期違反勞動基準法／工會法之紀錄</b></p>", unsafe_allow_html=True)
            if not df1_1.empty:
                st.dataframe(self.customized_df(df1_1))
            else:
                st.markdown("<p style='font-family:Courier; font-size: 15px;'>\
                            查無近期相關紀錄</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-family:Courier; font-size: 15px; color: Peru;'>\
                        <b>近期違反性別工作平等法／職業安全衛生法／就業服務法／中高齡者及高齡者就業促進法之紀錄</b></p>",
                        unsafe_allow_html=True)
            if not df1_2.empty:
                st.dataframe(self.customized_df(df1_2))
            else:
                st.markdown("<p style='font-family:Courier; font-size: 15px;'>\
                            查無近期相關紀錄</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-family:Courier; font-size: 15px; color: Peru;'>\
                        <b>近期違反勞工退休金條例／勞工職業災害保險及保護法之紀錄</b></p>", unsafe_allow_html=True)
            if not df1_3.empty:
                st.dataframe(self.customized_df(df1_3))
            else:
                st.markdown("<p style='font-family:Courier; font-size: 15px;'>\
                            查無近期相關紀錄</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-family:Courier; font-size: 15px; color: Peru;'>\
                        <b>近期重大職業災害之紀錄</b></p>", unsafe_allow_html=True)
            if not df2.empty:
                st.dataframe(self.customized_df(df2))
            else:
                st.markdown("<p style='font-family:Courier; font-size: 15px;'>\
                            查無近期相關紀錄</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-family:Courier; font-size: 15px; color: Peru;'>\
                        <b>近期職業安全衛生優良之紀錄</b></p>", unsafe_allow_html=True)
            if not df3.empty:
                st.dataframe(self.customized_df(df3))
            else:
                st.markdown("<p style='font-family:Courier; font-size: 15px;'>\
                            查無近期相關紀錄</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-family:Courier; font-size: 15px;'>\
                        <b>以上表格出自以下網址的關鍵字搜尋結果：</b></p>", unsafe_allow_html=True)
            st.markdown("<p style='font-family:Courier; font-size: 15px;'>\
                        <a href='https://announcement.mol.gov.tw/'>\
                        違反勞動法令事業單位（雇主）查詢系統</a></p>",
                        unsafe_allow_html=True)
            st.markdown("<p style='font-family:Courier; font-size: 15px;'>\
                        <a href='https://pacs.osha.gov.tw/2875/'>\
                        重大職業災害公開網</a></p>",
                        unsafe_allow_html=True)
            st.markdown("<p style='font-family:Courier; font-size: 15px;'>\
                        <a href='https://pacs.osha.gov.tw/2872/'>\
                        職業安全衛生卓越網</a></p>",
                        unsafe_allow_html=True)

if __name__ == "__main__":
    web = company_search()
    web.main()
