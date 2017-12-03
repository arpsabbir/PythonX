"""
联网相关
"""

import os
import urllib.parse
import urllib.request


def get(url, params=None, headers=None, cookie=None, encode='utf-8', need_print=True):
    """
    获取数据
    :param url: 地址
    :param params: 参数
    :param headers： 头
    :param cookie: cookie
    :param encode: 编码
    :param need_print: 是否需要打印
    :return:
    """
    # 伪装头
    # Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36
    ua = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    if headers is None or headers is not dict:
        headers = {
            'User-Agent': ua
        }
    else:
        if not 'User-Agent' in headers.keys():
            headers['User-Agent'] = ua

    # 拼接参数
    if params is not None:
        extra = urllib.parse.urlencode(params)
        if '?' in url:
            url += '&' + extra
        else:
            url += '?' + extra

    # 构建请求
    request = urllib.request.Request(
        url=url,
        headers=headers)

    # 打开请求
    if need_print:
        print("open " + url)
    if cookie is None:
        request_data = urllib.request.urlopen(request)
    else:
        opener = urllib.request.build_opener()
        opener.addheaders.append(('Cookie', cookie))
        request_data = opener.open(request)

    # 读取并解析结果
    result = request_data.read().decode(encode)
    if need_print:
        print('result is ' + result)
    return result


def get_file(url, file_path, need_print=True):
    """下载文件"""
    if need_print:
        print('下载文件 %s ，从 %s' % (file_path, url))
    dir_name = os.path.dirname(file_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        if need_print:
            print('创建目录 %s' % dir_name)
    urllib.request.urlretrieve(url, file_path)
    if need_print:
        print('下载完成')


def parse_cookies(cookies=''):
    """从字符串中解析出 cookies"""
    result = dict()
    if not cookies:
        return result

    key_value_list = cookies.split(';')
    for key_value in key_value_list:
        key_value_pair = key_value.split('=', maxsplit=1)
        if len(key_value_pair) == 2:
            key, value = key_value_pair
            result[key.strip()] = value.strip()
    return result


def handle_result(requests, success_callback=None, fail_callback=None, print_result=True):
    """处理结果"""
    result = requests.json()
    if print_result:
        print(result)
    if result:
        code = result['code']
        if code == 200:
            # 成功
            data = result['data']
            if success_callback:
                success_callback(data)
            return data
        else:
            # 失败
            msg = result['msg']
            print(msg)
            if fail_callback:
                fail_callback(code, msg)
    else:
        # 结果为空
        if fail_callback:
            fail_callback(0, None)
    return None