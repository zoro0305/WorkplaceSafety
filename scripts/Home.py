#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Home.py
@Time    :   2023/03/21 10:18:21
@Author  :   Zoro Chang
'''

import streamlit as st
import json
import base64

from config import ProjectConfigs

class background():
    def __init__(self, img_path: str) -> None:
        self.img_path = img_path

    def set_bg_hack(self):
        '''
        A function to unpack an image from root folder and set as bg.

        Returns
        -------
        The background.
        '''
        # set bg name
        main_bg_ext = "jpg"

        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(self.img_path, "rb").read()).decode()});
                background-size: contain
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

class streamlit_web():
    def user_account_login(self,):
        with open(ProjectConfigs.USER_INFO_PATH.value, "r", encoding="utf-8") as file:
            user_info = json.load(file)
        user_name_login = st.text_input("使用者名稱 : ", "", max_chars=10)
        if user_name_login:
            st.write("<p style='font-family:Courier; font-size: 15px; color: Tan;'>\
                     <b>已成功輸入</b></p>", unsafe_allow_html=True)
            if user_name_login not in user_info.keys():
                st.write("<p style='font-family:Courier; font-size: 15px; color: Tomato;'>\
                         <b>使用者帳號尚未註冊</b></p>", unsafe_allow_html=True)
        user_password_login = st.text_input("使用者密碼 : ", "", max_chars=15, type="password")
        if user_password_login:
            st.write("<p style='font-family:Courier; font-size: 15px; color: Tan;'>\
                     <b>已成功輸入</b></p>", unsafe_allow_html=True)
            if user_info.get(user_name_login) != user_password_login:
                st.write("<p style='font-family:Courier; font-size: 15px; color: Tomato;'>\
                         <b>使用者帳號或密碼輸入錯誤或尚未註冊</b></p>", unsafe_allow_html=True)
            else:
                st.write("<p style='font-family:Courier; font-size: 15px; color: SaddleBrown;'>\
                         <b>已成功登入</b></p>", unsafe_allow_html=True)

    def main(self):
        """the main execution function of the web.
        """
        st.set_page_config(page_title="職災ㄨㄚ熊災",
                           page_icon='🔥', layout="centered")
        background("scripts/background.jpg").set_bg_hack()
        st.markdown("<p style='font-family:Courier; font-size: 35px; color: SaddleBrown;'>\
                    <b>職災ㄨㄚ熊災🐻－職場安全資訊攏底加！</b></p>", unsafe_allow_html=True)

        st.markdown("<p style='font-family:Noto Sans TC; font-size: 20px'>\
                    <b>使用者登入</b></p>", unsafe_allow_html=True)
        self.user_account_login()
        st.markdown("<p style='font-family:Noto Sans TC; font-size: 20px'>\
                    <b><br>網頁理念</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-family:Noto Sans TC; font-size: 15'>\
                    &emsp;&emsp;在這科技進步的時代，其實仰賴著許多勞工的默默付出,\
                    但諷刺的是，「工安意外」、「過勞致死」諸類有關職場安全上的問題卻層出不窮。\
                    於是我們想...<br><br>\
                    ➊ <b>成為勞工職場的幫手</b>，提供一個可靠好用的 app，幫助勞工避免職場危險;<br>\
                    ➋ <b>成為勞工背後的靠山</b>，提供一個不幸發生意外時可以保障勞工權益的管道;<br>\
                    ➌ <b>成為勞工信賴的夥伴</b>，提供一個便捷的系統，以即時回覆勞工們的問題。<br></p>",
                    unsafe_allow_html=True)

if __name__ == "__main__":
    web = streamlit_web()
    web.main()
