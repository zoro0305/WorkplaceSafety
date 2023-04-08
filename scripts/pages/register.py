#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   register.py
@Time    :   2023/03/25 11:04:31
@Author  :   Zoro Chang
'''

import streamlit as st
import json
import re

from config import ProjectConfigs
from Home import background

class Register():
    def user_account_register(self):
        with open(ProjectConfigs.USER_INFO_PATH.value, "r", encoding="utf-8") as file:
            user_info = json.load(file)
        with open(ProjectConfigs.USER_INFO_PATH.value, "w", encoding="utf-8") as file:
            user_name_register = st.text_input("欲註冊之使用者名稱 : ", "", max_chars=10)
            if user_name_register:
                st.write("<p style='font-family:Courier; font-size: 15px; color: Tan;'>\
                         <b>已成功輸入</b></p>", unsafe_allow_html=True)
                if user_info.get(user_name_register) != None:
                    st.write("<p style='font-family:Courier; font-size: 15px; color: Tomato;'>\
                             <b>此使用者帳號已被註冊</b></p>", unsafe_allow_html=True)
            user_password_register = st.text_input("欲註冊之使用者密碼 : ", "", max_chars=20,
                                                   type="password")
            if user_password_register:
                st.write("<p style='font-family:Courier; font-size: 15px; color: Tan;'>\
                        <b>已成功輸入</b></p>", unsafe_allow_html=True)
                if user_info.get(user_name_register) == None:
                    if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$",
                                    user_password_register):
                        st.write("<p style='font-family:Courier; font-size: 15px; color: Tomato;'>\
                                 <b>密碼需為英文字母和數字組成(各至少一個)，並且長度介於8-20之間!</b></p>",
                                 unsafe_allow_html=True)
                    else:
                        user_info = {**user_info, user_name_register: user_password_register}
                        st.write("<p style='font-family:Courier; font-size: 15px; color: SaddleBrown;'>\
                                <b>已成功註冊</b></p>", unsafe_allow_html=True)
            json.dump(user_info, file)

    def main(self):
        """the main execution function of the register page.
        """
        background("scripts/background.jpg").set_bg_hack()
        st.markdown("<p style='font-family:Courier; font-size: 35px; color: SaddleBrown;'>\
                    <b>職災ㄨㄚ熊災🐻－職場安全資訊攏底加！</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-family:Courier; font-size: 20px;'>\
                    <b>使用者帳號密碼註冊</b></p>", unsafe_allow_html=True)
        self.user_account_register()

if __name__ == "__main__":
    web = Register()
    web.main()
