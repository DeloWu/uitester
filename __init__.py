#!/usr/bin/env python
# encoding: utf-8
import unittest
import pytest
import json
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import platform
from common.logger import *


class UIFrame(unittest.TestCase):
    # UI自动化用例基类

    @classmethod
    def setUpClass(cls, headless_flag=False):
        if platform.system() != 'Windows':
            pytest.skip('ui自动化用例仅在windows环境执行', allow_module_level=True)
        LOG_DEBUG('初始化环境')
        cls.read_config()
        chrome_options = Options()
        if headless_flag:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('-start-maximized')
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            LOG_DEBUG(e)
            LOG_DEBUG('Chrome启动失败，此环境不可进行UI自动化，自动跳过所有UI自动化用例')
            pytest.skip('此环境异常，无法进行UI自动化', allow_module_level=True)
        cls.driver.implicitly_wait(10)
        cls.index_url = r'https://something'
        cls.driver.get(cls.index_url)

    @classmethod
    def tearDownClass(cls):
        LOG_DEBUG('清除环境')
        try:
            cls.driver.quit()
            os.system('taskkill /F /im chrome.exe')
            os.system('taskkill /F /im chromedriver.exe')
        except Exception as e:
            LOG_ERROR(e)

    def setUp(self, auto_login=True, username='', pwd=''):
        if auto_login:
            if self.index_page.check_login_success():
                LOG_DEBUG('当前已处于登录状态')
            else:
                LOG_DEBUG('当前未登录,开始自动登录')
                self.user_login(username=username, pwd=pwd)

    def tearDown(self):
        pass

    @classmethod
    def read_config(cls):
        pass

    def get(self, url):
        if not (url.startswith(r'http://') or url.startswith(r'https://')):
            if not url.startswith(r'/'):
                url = '/' + url
            launch_url = self.mgr_ip + url
        else:
            launch_url = url
        # UIFrame.driver.get(launch_url)
        self.driver.get(launch_url)
        LOG_DEBUG('页面跳转到: {}'.format(launch_url))

    def close_window(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def switch_to_new_window(self):
        # 切换到其他窗口
        try:
            window_handles = self.driver.window_handles
            if len(window_handles) == 1:
                self.driver.switch_to.window(window_handles[0])
                LOG_DEBUG('切换窗口成功, 当前窗口为: {}'.format(self.get_title()))
                return True
            current_window_handle = self.driver.current_window_handle
            LOG_DEBUG('当前窗口句柄为: {}, 所有句柄为: {}'.format(current_window_handle, window_handles))
            for window_handle in window_handles:
                if window_handle != current_window_handle:
                    self.driver.switch_to.window(window_handle)
                    LOG_DEBUG('切换窗口成功, 当前窗口为: {}'.format(self.get_title()))
        except Exception as e:
            LOG_DEBUG('切换窗口失败: {}'.format(e))

    def back(self):
        LOG_DEBUG('页面回退')
        self.driver.back()

    def forward(self):
        LOG_DEBUG('页面前进')
        self.driver.forward()

    def refresh(self):
        LOG_DEBUG('页面刷新')
        self.driver.refresh()

    def get_cookies(self):
        cookies_content = self.driver.get_cookies()
        if isinstance(cookies_content, unicode):
            cookies_content = cookies_content.encode('utf-8', errors='ignore')
        LOG_DEBUG('获取所有cookies: {}'.format(cookies_content))
        return cookies_content

    def get_cookie(self, name):
        try:
            value = self.get_cookie(name)
            if isinstance(value, unicode):
                value = value.encode('utf-8', errors='ignore')
            LOG_DEBUG('获取指定cookie: 名称: {}, 值: {}'.format(name, value))
            return value
        except Exception as e:
            LOG_DEBUG('获取指定cookie失败')
            return ''

    def add_cookie(self, cookie_dict):
        LOG_DEBUG('添加cookies: {}'.format(cookie_dict))
        self.driver.add_cookie(cookie_dict)

    def get_alert_text(self):
        # 获取弹窗内容
        text = self.driver.switch_to.alert.text
        if isinstance(text, unicode):
            text = text.encode('utf-8', errors='ignore')
        LOG_DEBUG('弹窗内容为: {}'.format(text))

    def accept_alert(self):
        # 弹窗点确定
        try:
            self.driver.switch_to.alert.accept()
            LOG_DEBUG('弹窗确定')
        except Exception as e:
            LOG_DEBUG('弹窗确定失败: {}'.format(e))

    def dismiss_alert(self):
        # 弹窗点拒绝
        try:
            self.driver.switch_to.alert.dismiss()
            LOG_DEBUG('弹窗拒绝')
        except Exception as e:
            LOG_DEBUG('弹窗拒绝失败: {}'.format(e))

    def send_keys_to_alert(self, text):
        # 向弹窗输入内容
        try:
            self.driver.switch_to.alert.send_keys(text)
            LOG_DEBUG('向弹窗输入内容: {}'.format(text))
        except Exception as e:
            LOG_DEBUG('向弹窗输入内容失败: {}'.format(e))

    def execute_script(self, script, *args):
        # 执行js语句
        try:
            LOG_DEBUG('执行js语句: {}'.format(script))
            return self.driver.execute_script(script, *args)
        except Exception as e:
            LOG_DEBUG('执行js语句失败: {}'.format(e))
            return None

    def scroll(self, key='end', loc=None, ele=None, strict=False, position=None, action='click'):
        key_select = ['end', 'home', 'page_up', 'page_down']
        if key not in key_select:
            LOG_ERROR('参数key: {}输入错误, 可选有效参数为: {}'.format(key, key_select))
        key_map = {
            'end': Keys.END,
            'home': Keys.HOME,
            'page_up': Keys.PAGE_UP,
            'page_down': Keys.PAGE_DOWN
        }
        if loc or ele:
            self.move_to_element_and_click(loc=loc, ele=ele, strict=strict, action=action)
        elif position:
            self.move_by_offset_and_click(xoffset=position[0], yoffset=position[1], action=action)
        else:
            actions = ActionChains(self.driver)
            if action == 'click':
                actions.click()
            elif action == 'double_click':
                actions.double_click()
            elif action == 'context_click':
                actions.context_click()
            else:
                pass
            actions.perform()
        actions = ActionChains(self.driver)
        actions.key_down(key_map[key])
        actions.key_up(key_map[key])
        actions.perform()

    def screenshot(self, filepath):
        success_flag = self.driver.save_screenshot(filepath)
        if success_flag:
            LOG_DEBUG('截图成功, 图片路径: {}'.format(filepath))
        else:
            LOG_DEBUG('截图失败!')

    def get_cur_url(self):
        cur_url = self.driver.current_url
        LOG_DEBUG('当前url为: {}'.format(cur_url))
        return cur_url

    def get_page_source(self):
        try:
            page_content = self.driver.page_source
            LOG_DEBUG('获取当前页面源码成功')
            if isinstance(page_content, unicode):
                page_content = page_content.encode('utf-8', errors='ignore')
            return page_content
        except Exception as e:
            LOG_DEBUG('获取当前页面源码失败')
            return ''

    def get_attribute(self, name, loc=None, ele=None, strict=False):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            value = ele.get_attribute(name)
            if isinstance(value, unicode):
                value = value.encode('utf-8', errors='ignore')
            LOG_DEBUG('获取元素 loc: {} ,location: {} ,属性名: {},属性值: {}'.format(loc, ele.location, name, value))
            return value
        except Exception as e:
            LOG_DEBUG('ERROR [get_attribute]: {}'.format(e))
            return ''

    def get_text(self, loc=None, ele=None, strict=False):
        """
        获取两个标签之间的文本信息
        :param loc:
        :param ele:
        :return: text
        """
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            text = ele.text
            if isinstance(text, unicode):
                text = text.encode('utf-8', errors='ignore')
            LOG_DEBUG('元素 loc: {} ,location: {}, 获取文本信息为: {}'.format(loc, ele.location, text))
            return text
        except Exception as e:
            LOG_DEBUG('获取文本信息失败: {}'.format(e))
            return ''

    def get_title(self):
        title_content = self.driver.title
        if isinstance(title_content, unicode):
            title_content = title_content.encode('utf-8', errors='ignore')
        LOG_DEBUG('获取当前页标题: {}'.format(title_content))
        return title_content

    def get_current_url(self):
        current_url = self.driver.current_url
        if isinstance(current_url, unicode):
            current_url = current_url.encode('utf-8', errors='ignore')
        LOG_DEBUG('当前url为: {}'.format(current_url))
        return current_url
