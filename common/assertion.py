from Extend.extractData import extract_data
from common.log import LOG, logger


class Assert(object):
    """断言类"""

    @logger('common.Assert.assert_true', '请求返回数据', '预期')
    def assert_true(self, response_data, expected):
        """
        断言True or False
        :param response_data: 相应数据，格式字典
        :param expected: 预期，格式字典
        :return: 返回字典类型
        """
        try:
            result_d = dict()
            for key in expected.keys():
                data_dict = extract_data(response_data, key)
                for k, v in data_dict.items():
                    result_d[k] = v
            return result_d
        except Exception as e:
            LOG.error(""""传入的数据有误，错误原因%s
                       请求数据为：%s
                       预期数据为：%s""" % (e, response_data, expected))
            return {'ERROR': '传入的数据有误'}


if __name__ == '__main__':
    response_data_dict = {"result": 0,
                          "data": ["React", {'parameter': None}, "算法", "Vue.js", "Python", "人工智能", "GO语言", "小程序"],
                          "msg": "成功", "case": {"run": {'parameter': None}, "result": 1}}
    expected_dict = 'parameter'
    ass = Assert()
    result = ass.assert_true(response_data_dict, expected_dict)
    print(result)