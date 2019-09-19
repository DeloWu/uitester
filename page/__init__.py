#!/usr/bin/env python
# encoding: utf-8
import unittest

import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from uitester.common.logger import *
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


class BasePage(object):
    # Page基类，所有其他Page全部继承此类,负责元素和driver方法的封装
    def __init__(self, driver):
        self.driver = driver
        self.read_config()
    def read_config(self):
        pass
    def find_element(self, loc, strict=False):
        """

        :param loc:
        :param strict: type: bool e.g.True:若找不到元素直接抛错 , False:若找不到元素，日志打印报错，不抛错
        :return:
        """
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located(loc))
        except Exception as e:
            # LOG_DEBUG('ERROR: {}'.format(e))
            LOG_DEBUG('页面未找到元素, loc: {}'.format(loc))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except Exception as e:
            LOG_DEBUG('ERROR [find_element]: {}'.format(e))
            LOG_DEBUG('页面未找到元素, loc: {}'.format(loc))
            if strict:
                raise e

    def find_elements(self, loc, strict=False):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located(loc))
        except Exception as e:
            LOG_DEBUG('ERROR [find_element]: {}'.format(e))
            LOG_DEBUG('页面未找到元素: {}'.format(loc))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located(loc))
            return self.driver.find_elements(*loc)
        except Exception as e:
            LOG_DEBUG('ERROR [find_elements]: {}'.format(e))
            LOG_DEBUG('页面未找到元素: {}'.format(loc))
            if strict:
                raise e

    def clear(self, loc=None, ele=None, strict=False):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            ele.clear()
            LOG_DEBUG('元素 loc: {} ,location: {} 清除输入框内容'.format(loc, ele.location))
        except Exception as e:
            LOG_DEBUG('ERROR [clear]: {}'.format(e))

    def text_content(self, content, loc=None, ele=None, strict=False):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            ele.clear()
            ele.send_keys(content)
            LOG_DEBUG('在元素 loc: {} ,location: {} 输入内容: {}'.format(loc, ele.location, content))
        except Exception as e:
            LOG_DEBUG('ERROR [text_content]: {}'.format(e))

    def click(self, loc=None, ele=None, strict=False):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            ele.click()
            LOG_DEBUG('单击元素 loc: {} ,location: {}'.format(loc, ele.location))
        except Exception as e:
            LOG_DEBUG('ERROR [click]: {}'.format(e))

    def double_click(self, loc=None, ele=None, strict=False):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            actions = ActionChains(self.driver)
            actions.double_click(ele)
            actions.perform()
            LOG_DEBUG('双击元素 loc: {} ,location: {}'.format(loc, ele.location))
        except Exception as e:
            LOG_DEBUG('ERROR [double_click]: {}'.format(e))

    def context_click(self, loc=None, ele=None, strict=False):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            actions = ActionChains(self.driver)
            actions.context_click(ele)
            actions.perform()
            LOG_DEBUG('右键单击元素 loc: {} ,location: {}'.format(loc, ele.location))
        except Exception as e:
            LOG_DEBUG('ERROR [context_click]: {}'.format(e))

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

    def is_selected(self, loc=None, ele=None, strict=False):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            selected_flag = ele.is_selected()
            LOG_DEBUG('元素 loc: {} ,location: {} 是否被选中: {}'.format(loc, ele.location, selected_flag))
            return selected_flag
        except Exception as e:
            LOG_DEBUG('ERROR [is_selected]: {}'.format(e))
            return False

    def is_enabled(self, loc=None, ele=None, strict=False):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            enabled_flag = ele.is_enabled()
            LOG_DEBUG('元素 loc: {} ,location: {} 是否可点击: {}'.format(loc, ele.location, enabled_flag))
            return enabled_flag
        except Exception as e:
            LOG_DEBUG('ERROR [is_enabled]: {}'.format(e))
            return False

    def is_displayed(self, loc=None, ele=None, strict=False):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            displayed_flag = ele.is_displayed()
            LOG_DEBUG('元素 loc: {} ,location: {} 是否可见: {}'.format(loc, ele.location, displayed_flag))
            return displayed_flag
        except Exception as e:
            LOG_DEBUG('ERROR [is_displayed]: {}'.format(e))
            return False

    def screenshot(self, filepath):
        success_flag = self.driver.save_screenshot(filepath)
        if success_flag:
            LOG_DEBUG('截图成功, 图片路径: {}'.format(filepath))
        else:
            LOG_DEBUG('截图失败!')
    
    def submit(self, loc=None, ele=None, strict=False):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            ele.submit()
            LOG_DEBUG('元素 loc: {} ,location: {}, 提交表单'.format(loc, ele.location))
        except Exception as e:
            LOG_DEBUG('表单提交失败')
            raise e

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

    def move_by_offset(self, xoffset=0, yoffset=0):
        """
        移动到指定坐标
        :param xoffset:
        :param yoffset:
        :return:
        """
        try:
            LOG_DEBUG('移动到坐标 x:{}, y:{}'.format(xoffset, yoffset))
            actions = ActionChains(self.driver)
            actions.move_by_offset(xoffset, yoffset)
            actions.perform()
        except Exception as e:
            LOG_DEBUG('移动坐标失败: {}'.format(e))

    def move_by_offset_and_click(self, xoffset=0, yoffset=0, action='click'):
        """
        移动到指定坐标
        :param xoffset:
        :param yoffset:
        :return:
        """
        action_select = ['click', 'double_click', 'context_click']
        if action not in action_select:
            LOG_DEBUG('action: {}参数错误, 可选参数为: {}'.format(action, action_select))
        try:
            LOG_DEBUG('移动到坐标 x:{}, y:{}, 点击坐标'.format(xoffset, yoffset))
            actions = ActionChains(self.driver)
            actions.move_by_offset(xoffset, yoffset)
            if action == 'click':
                actions.click()
            elif action == 'double_click':
                actions.double_click()
            elif action == 'context_click':
                actions.context_click()
            else:
                pass
            actions.perform()
        except Exception as e:
            LOG_DEBUG('移动坐标失败: {}'.format(e))

    def move_to_element_with_offset(self, loc=None, ele=None, strict=True, xoffset=0, yoffset=0):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            LOG_DEBUG('移动到坐标 {}'.format(ele.location))
            actions = ActionChains(self.driver)
            LOG_DEBUG('移动当前坐标的相对坐标 x: {}, y: {}'.format(xoffset, yoffset))
            actions.move_to_element_with_offset(ele, xoffset, yoffset)
            actions.perform()
        except Exception as e:
            LOG_DEBUG('移动坐标失败: {}'.format(e))

    def move_to_element_with_offset_and_click(self, loc=None, ele=None, strict=True, xoffset=0, yoffset=0, action='click'):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        action_select = ['click', 'double_click', 'context_click']
        if action not in action_select:
            LOG_DEBUG('action: {}参数错误, 可选参数为: {}'.format(action, action_select))
        try:
            LOG_DEBUG('移动到坐标 {}'.format(ele.location))
            actions = ActionChains(self.driver)
            LOG_DEBUG('移动当前坐标的相对坐标 x: {}, y: {}, 点击坐标'.format(xoffset, yoffset))
            actions.move_to_element_with_offset(ele, xoffset, yoffset)
            if action == 'click':
                actions.click()
            elif action == 'double_click':
                actions.double_click()
            elif action == 'context_click':
                actions.context_click()
            else:
                pass
            actions.perform()
        except Exception as e:
            LOG_DEBUG('移动坐标失败: {}'.format(e))

    def move_to_element(self, loc=None, ele=None, strict=False):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            LOG_DEBUG('移动到 loc: {} ,location: {}'.format(loc, ele.location))
            actions = ActionChains(self.driver)
            actions.move_to_element(ele)
            actions.perform()
        except Exception as e:
            LOG_DEBUG('移动坐标失败: {}'.format(e))

    def move_to_element_and_click(self, loc=None, ele=None, strict=False, action='click'):
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        action_select = ['click', 'double_click', 'context_click']
        if action not in action_select:
            LOG_DEBUG('action: {}参数错误, 可选参数为: {}'.format(action, action_select))
        try:
            LOG_DEBUG('移动到 loc: {} ,location: {}, 点击坐标'.format(loc, ele.location))
            actions = ActionChains(self.driver)
            actions.move_to_element(ele)
            if action == 'click':
                actions.click()
            elif action == 'double_click':
                actions.double_click()
            elif action == 'context_click':
                actions.context_click()
            else:
                pass
            actions.perform()
        except Exception as e:
            LOG_DEBUG('移动坐标失败: {}'.format(e))

    def switch_to_new_window(self):
        # 切换到其他窗口
        window_handles = self.driver.window_handles
        current_window_handle = self.current_window_handle
        LOG_DEBUG('当前窗口句柄为: {}, 所有句柄为: {}'.format(current_window_handle, window_handles))
        try:
            for window_handle in window_handles:
                if window_handle != current_window_handle:
                    self.driver.switch_to.window(window_handle)
                    LOG_DEBUG('切换窗口成功, 当前窗口为: {}'.format(self.get_title()))
        except Exception as e:
            LOG_DEBUG('切换窗口失败: {}'.format(e))

    def execute_script(self, script, *args):
        # 执行js语句
        try:
            LOG_DEBUG('执行js语句: {}'.format(script))
            return self.driver.execute_script(script, *args)
        except Exception as e:
            LOG_DEBUG('执行js语句失败: {}'.format(e))
            return None

    def get(self, url):
        LOG_DEBUG('跳转到url: {}'.format(url))
        self.driver.get(url)

    def get_title(self):
        title_content = self.driver.title
        if isinstance(title_content, unicode):
            title_content = title_content.encode('utf-8', errors='ignore')
        LOG_DEBUG('获取当前页标题: {}'.format(title_content))
        return title_content

    def close(self):
        LOG_DEBUG('关闭窗口')
        self.driver.close()

    def quit(self):
        LOG_DEBUG('关闭窗口')
        self.driver.quit()

    def maximize_window(self):
        LOG_DEBUG('窗口最大化')
        self.driver.maximize_window()

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

    def choice_select(self, by_type, text, loc=None, ele=None, strict=False):
        """
        选择select标签下拉框
        :param by_type: type: str e.g. 'index', 'value', 'visible_text'
        :param text:
        :param loc:
        :param ele:
        :param strict:
        :return:
        """
        by_type_select = ['index', 'value', 'visible_text']
        if by_type not in by_type_select:
            LOG_DEBUG('by_type 参数校验失败: {}'.format(by_type))
            LOG_DEBUG('by_type 可选择参数为: {}'.format(by_type_select))
        else:
            if not (loc or ele):
                LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
            else:
                if not ele:
                    ele = self.find_element(loc, strict=strict)
            try:
                select = Select(ele)
                function_map = {
                    'index': select.select_by_index,
                    'value': select.select_by_value,
                    'visible_text': select.select_by_visible_text
                }
                function_map[by_type](text)
            except Exception as e:
                LOG_DEBUG('选择下拉选项失败: {}'.format(e))

    def switch_to_frame(self, by_type, text, loc=None, ele=None, strict=False):
        """
        切frame
        :param by_type: type: str e.g. 'index', 'value', 'element'
        :param text:
        :param loc:
        :param ele:
        :param strict:
        :return:
        """
        by_type_select = ['index', 'value', 'element']
        if by_type not in by_type_select:
            LOG_DEBUG('by_type 参数校验失败: {}'.format(by_type))
            LOG_DEBUG('by_type 可选择参数为: {}'.format(by_type_select))
        else:
            if by_type == 'element':
                if not (loc or ele):
                    LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
                else:
                    if not ele:
                        ele = self.find_element(loc, strict=strict)
                    try:
                        self.driver.switch_to.frame(ele)
                        LOG_DEBUG('切换frame成功')
                    except Exception as e:
                        LOG_DEBUG('切换frame失败: {}'.format(e))
            else:
                try:
                    self.driver.switch_to.frame(text)
                    LOG_DEBUG('切换frame成功')
                except Exception as e:
                    LOG_DEBUG('切换frame失败: {}'.format(e))

    def switch_to_parent_frame(self):
        LOG_DEBUG('切换到父frame')
        self.driver.switch_to.parent_frame()

    def switch_to_default_content(self):
        LOG_DEBUG('切换到主文档')
        self.driver.switch_to.default_content()

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
            pass
            # actions = ActionChains(self.driver)
            # if action == 'click':
            #     actions.click()
            # elif action == 'double_click':
            #     actions.double_click()
            # elif action == 'context_click':
            #     actions.context_click()
            # else:
            #     pass
            # actions.perform()
        actions = ActionChains(self.driver)
        actions.key_down(key_map[key])
        actions.key_up(key_map[key])
        actions.perform()

    def get_current_url(self):
        current_url = self.driver.current_url
        if isinstance(current_url, unicode):
            current_url = current_url.encode('utf-8', errors='ignore')
        LOG_DEBUG('当前url为: {}'.format(current_url))
        return current_url

    def keyboard_opr(self, key="回车键", loc=None, ele=None, strict=True):
        """
        键盘操作
        :param opr_type: 操作类型 TODO 其他后续用到可再加
        :param loc:
        :param ele:
        :param strict:
        :return:
        """
        key_select = ['回车键', '空格键', '制表键', '回退键', '删除键']
        if key not in key_select:
            LOG_ERROR('参数key: {}输入错误, 可选有效参数为: {}'.format(key, key_select))
        key_map = {
            '回车键': Keys.ENTER,
            '空格键': Keys.SPACE,
            '制表键': Keys.TAB,
            '回退键': Keys.ESCAPE,
            '删除键': Keys.BACKSPACE
        }
        if not (loc or ele):
            LOG_ERROR('loc: {}, ele: {}, 请至少输入一个有效参数!'.format(loc, ele))
        else:
            if not ele:
                ele = self.find_element(loc, strict=strict)
        try:
            LOG_DEBUG('对元素 loc: {},执行{}操作'.format(loc, key))
            ele.send_keys(key_map[key])
        except Exception as e:
            LOG_ERROR("键盘操作:{}失败: {}".format(key_map[key], e))
