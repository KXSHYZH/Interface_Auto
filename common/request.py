import json
import requests
from common.log import LOG, logger


class Request(object):
    """接口请求的封装
    注意：当访问HTTPS网站时会出现SSL错误
    解决方法
    第一步：在开始请求前，输入requests.urllib3.disable_warnings()，屏蔽warning信息
    第二步：在请求中将verify设置为False----verify=False

    """

    # 屏蔽warning信息
    requests.urllib3.disable_warnings()

    def request_get(self, url, params, **kwargs):
        """GET请求
        :param url: 请求地址
        :param params: get请求参数，使用？加参数值的格式
        :param kwargs: 可以传入多个值，比如header和cookie，格式为key=value
        :return: 返回相应数据
        """
        response_get = requests.get(url=url, params=params, verify=False, **kwargs).json()
        # sort_keys：根据key排序，设置成True为升序排列；indent：以几个空格缩进，输出阅读友好型；ensure_ascii: 可以序列化非ascii码（中文等）
        return json.dumps(response_get, indent=2, sort_keys=False, ensure_ascii=False)

    def request_post(self, url, data, **kwargs):
        """POST请求
        :param url: 请求地址
        :param data: post请求参数，使用字段的格式
        :param kwargs: 可以传入多个值，比如header和cookie，格式为key=value
        :return: 返回相应数据
        """
        response_post = requests.post(url=url, data=data, **kwargs).json()
        return json.dumps(response_post, indent=2, sort_keys=False, ensure_ascii=False)

    @logger('common.Request.request')
    def request(self, url, params, method, **kwargs):
        """根据传入的请求类型发出请求"""
        if method == 'GET':
            response_data_str = self.request_get(url, params, **kwargs)
            return response_data_str
        elif method == 'POST':
            response_data_str = self.request_post(url, params, **kwargs)
            return response_data_str
        else:
            LOG.error('method参数有误，请检查！')


if __name__ == '__main__':
    request = Request()
    # get
    url_get = 'https://www.imooc.com/lecturer/ajaxrecteacher'
    response_data = request.request(url=url_get, params=None, method='GET')
    print(response_data)
    # post
    url_post = 'https://www.imooc.com/search/hotwords'
    response_data = request.request(url=url_post, params=None, method='POST')
    print(response_data)

    response_get = requests.get(url='https://www.imooc.com/lecturer/ajaxrecteacher1111')
    print(response_get.text == '')