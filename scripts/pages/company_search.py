#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   company_search.py
@Time    :   2023/03/26 20:04:15
@Author  :   Zoro Chang
'''

import streamlit as st
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

from Home import background

class company_search():
    def _company_search(self, unit: str):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        ######違反勞動法令紀錄
        chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        chrome.get("https://announcement.mol.gov.tw/")

        unitname = chrome.find_element("id", "unitname")

        unitname.send_keys(unit)
        unitname.submit()

        html1 = chrome.page_source

        time.sleep(0.5)
        chrome.quit()

        ######重大職業災害紀錄
        chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        chrome.get("https://pacs.osha.gov.tw/2875/")

        unitname = chrome.find_element("id", "info_q")

        unitname.send_keys(unit)
        unitname.submit()

        html2 = chrome.page_source

        time.sleep(0.5)
        chrome.quit()

        ######職業衛生安全紀錄
        chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        chrome.get("https://pacs.osha.gov.tw/2872/")

        unitname = chrome.find_element("id", "info_q")

        unitname.send_keys(unit)
        unitname.submit()

        html3 = chrome.page_source

        time.sleep(0.5)
        chrome.quit()

        ######找關鍵字

        #1-"https://announcement.mol.gov.tw/"
        soup = BeautifulSoup(html1, 'html.parser')

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

        #2-"https://pacs.osha.gov.tw/2875/"
        soup = BeautifulSoup(html2, 'html.parser')

        times=[]
        for tim in soup.find_all('td', {'data-title': '發生日期'}):
            times.append(tim.text.strip())

        companies=[]
        for company in soup.find_all('td', {'data-title': '事業單位'}):
            companies.append(company.text.strip())

        owners=[]
        for owner in soup.find_all('td', {'data-title': '業主'}):
            owners.append(owner.text.strip())

        places=[]
        for place in soup.find_all('td', {'data-title': '場所(肇災處)'}):
            places.append(place.text.strip())

        addresses=[]
        for address in soup.find_all('td', {'data-title': '地址'}):
            addresses.append(address.text.strip())

        disasters=[]
        for disaster in soup.find_all('td', {'data-title': '災害類型'}):
            disasters.append(disaster.text.strip())

        df2 = pd.DataFrame()
        if times:
            df2 = pd.DataFrame({'發生日期': times, '事業單位': companies, '業主': owners,
                                '場所(肇災處)': places, '地址': addresses, '災害類型': disasters})

        #3-"https://pacs.osha.gov.tw/2872/"
        soup = BeautifulSoup(html3, 'html.parser')

        years=[]
        for year in soup.find_all('td', {'data-title': '獲獎年度'}):
            years.append(year.text.strip())

        prizes=[]
        for prize in soup.find_all('td', {'data-title': '獲獎名稱'}):
            prizes.append(prize.text.strip())

        companies=[]
        for company in soup.find_all('td', {'data-title': '企業名稱'}):
            companies.append(company.text.strip())

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
