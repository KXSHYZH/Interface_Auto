import os
import unittest
import datetime
from common.BeautifulReport import BeautifulReport
from common.sendEmail import SendEmail


path = os.path.dirname(os.path.realpath(__file__))
time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
test_suite = unittest.defaultTestLoader.discover(path + r'\TestApi\\', pattern='test*.py')
result = BeautifulReport(test_suite)
result.report(filename='report_' + time_str + '.html', description='测试报告', report_path=path + r'\Report')
# 发送邮件
send_email = SendEmail(description=u'测试报告', pass_num=result.FIELDS['testAll'] - result.FIELDS['testFail'],
                       fail_num=result.FIELDS['testFail'], start_time=result.FIELDS['beginTime'],
                       end_time=result.FIELDS['end_time'], continue_time=result.FIELDS['totalTime'])
send_email.send_email()
