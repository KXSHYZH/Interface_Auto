import json
import unittest
import ddt
from Extend.printInfo import print_info
from common.BeautifulReport import BeautifulReport
from common.assertion import Assert
from common.log import *
from common.operationExcel import OperationExcel
from common.readYaml import ReadYaml
from common.request import Request
from common.sendEmail import SendEmail

path = os.path.dirname(os.path.realpath(__file__))
ry = ReadYaml(path + r'\..\Config\config.yaml')
operation_excel = OperationExcel(path + r'\..\CaseData\\' + ry.read_node_data('CASE_CONF', 'FILE_NAME'))
index = ry.read_node_data('CASE_CONF', 'SHEET_1', 'SHEET_INDEX')
# 测试数据，数据所在行
test_data, row_list = operation_excel.get_data(index)
row_result_dic = dict()
row_response_dic = dict()


@ddt.ddt
class TestApi(unittest.TestCase):
    """测试接口类"""

    request = None
    table_header = dict()
    number = 0

    @classmethod
    def setUpClass(cls):
        """必须使用@classmethod 装饰器,所有test运行前运行一次"""
        # 对请求类实例化
        cls.request = Request()
        cls.ass = Assert()

    def setUp(self):
        """每个测试函数运行前运行"""
        # 记录运行次数
        TestApi.number += 1
        data = test_data[TestApi.number-1]
        TestApi.table_header['_caseId'] = data['case_id']  # _caseId: 用例编号
        TestApi.table_header['_testModule'] = data['module']  # _testMethodName: 测试模块
        TestApi.table_header['_testDescribe'] = data['describe']  # _testMethodDoc: 用例描述
        method = test_data[TestApi.number-1]['method']
        # 如果是get请求，将parameter拼接到complete_url后面，并且将parameter设置为None
        self.parameter = data['parameter']
        if method == 'GET':
            data['basic_url'] = data['basic_url'] + data['path'] + data['parameter']
            data['parameter'] = None
        elif method == 'POST':
            data['basic_url'] = data['basic_url'] + data['path']
            data['parameter'] = eval(data['parameter'])

    @ddt.data(*test_data)
    @logger('======******TestApi.testapi.Testapi.test_api******======', 'case数据')
    def test_api(self, case_data):
        """测试接口"""
        print(case_data['basic_url'], '//', case_data['parameter'])
        response_data_str = TestApi.request.request(url=case_data['basic_url'], params=case_data['parameter'],
                                                    method=case_data['method'],
                                                    headers=eval(case_data['headers']))
        res = TestApi.ass.assert_true(json.loads(response_data_str), eval(case_data['expected']))
        if res == eval(case_data['expected']):
            case_data['result'] = 'pass'
            print(self.parameter)
            case_data['parameter'] = self.parameter
            row_result_dic[row_list[TestApi.number-1]] = 'pass'
            LOG.info(">>>>>> 请求结果：pass" )
        else:
            case_data['result'] = 'fail'
            case_data['parameter'] = self.parameter
            row_result_dic[row_list[TestApi.number - 1]] = 'fail'
            LOG.info(">>>>>> 请求结果：fail")
        row_response_dic[row_list[TestApi.number - 1]] = json.dumps(res, indent=2, sort_keys=False, ensure_ascii=False)
        # 断言，打印详细信息
        self.assertEqual(res, eval(case_data['expected']), print_info(case_data, response_data_str, case_data['result']))
        print(print_info(case_data, response_data_str, case_data['result']))

    def tearDown(self):
        """每个测试函数运行完后执行"""
        pass

    @classmethod
    def tearDownClass(cls):
        """必须使用@classmethod装饰器,所有test运行完后运行一次"""
        result_fag = ry.read_node_data('CASE_CONF', 'CASE_FIELD', 'RESULT', 'IS_WRITE')
        response_fag = ry.read_node_data('CASE_CONF', 'CASE_FIELD', 'RESPONSE', 'IS_WRITE')
        result_col = ry.read_node_data('CASE_CONF', 'CASE_FIELD', 'RESULT', 'INDEX')
        response_col = ry.read_node_data('CASE_CONF', 'CASE_FIELD', 'RESPONSE', 'INDEX')
        # 向Execl写入结果
        copy_data, table_data_w = operation_excel.copy_execl(index)
        for row, value in row_result_dic.items():
            if result_fag:
                operation_excel.write_data(table_data_w, row, result_col, value)
            else:
                break
        for row, value in row_response_dic.items():
            if response_fag:
                operation_excel.write_data(table_data_w, row, response_col, value)
            else:
                break
        operation_excel.save(copy_data)


if __name__ == '__main__':
    time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    test_suite = unittest.defaultTestLoader.discover(path + r'\\', pattern='test*.py')
    result = BeautifulReport(test_suite)
    result.report(filename='report_' + time_str + '.html', description='测试报告', report_path=path + r'\..\Report')
    print(result.FIELDS['testAll'], result.FIELDS['testFail'], result.FIELDS['testAll'] - result.FIELDS['testFail'],
          result.FIELDS['beginTime'], type(result.FIELDS['beginTime']), result.FIELDS['end_time'])
    # 发送邮件
    send_email = SendEmail(description=u'测试报告', pass_num=result.FIELDS['testAll'] - result.FIELDS['testFail'],
                           fail_num=result.FIELDS['testAll'], start_time=result.FIELDS['beginTime'],
                           end_time=result.FIELDS['end_time'], continue_time=result.FIELDS['totalTime'])
    send_email.send_email()
