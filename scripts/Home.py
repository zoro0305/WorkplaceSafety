#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Home.py
@Time    :   2023/03/21 10:18:21
@Author  :   Zoro Chang
'''

import streamlit as st
import schedule
import time

class streamlit_web():
    def _my_scraper(self):
        pass

    def _run_scheduler(self):
        """A function that executes regularly every day.
        """
        schedule.every().day.at("12:00").do(self._my_scraper)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def main(self):
        """the main execution function of the web.
        """
        st.set_page_config(page_title="職災ㄨㄚ熊災",
                           page_icon='🔥', layout="centered")
        st.markdown("<p style='font-family:Courier; font-size: 37px; color: SaddleBrown;'>\
                    <b>職災ㄨㄚ熊災🐻－職場安全資訊攏底加！</b></p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='font-family:Noto Sans TC; font-size: 18px'>\
                        網頁簡介</p>", unsafe_allow_html=True)

        with col2:
            user_name = st.text_input("使用者名稱 : ", "", max_chars=10)
            if user_name:
                st.write("<p style='font-family:Courier; font-size: 15px; color: LimeGreen;'>\
                         <b>已成功輸入✅</b></p>", unsafe_allow_html=True)
            user_password = st.text_input("使用者密碼 : ", "", max_chars=15, type="password")
            if user_password:
                st.write("<p style='font-family:Courier; font-size: 15px; color: LimeGreen;'>\
                         <b>已成功輸入✅</b></p>", unsafe_allow_html=True)

        # 每天的定時運行
        self._run_scheduler()

if __name__ == "__main__":
    web = streamlit_web()
    web.main()
