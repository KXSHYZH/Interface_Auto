import os
import datetime
import time
import smtplib                           # 发送邮件模块
from email.mime.text import MIMEText    # 定义邮件内容
from email.header import Header         # 定义邮件标题
from email.mime.multipart import MIMEMultipart  # 用于传送附件
from common.readYaml import ReadYaml


dir_path = os.path.dirname(os.path.realpath(__file__))
conf_path = os.path.join(dir_path, r"..\Config\config.yaml")
ry = ReadYaml(conf_path)
report_dir = dir_path + r'\..\Report'
case_path = dir_path + r'\..\CaseData\case.xls'
smtp_server = ry.read_node_data('EMAIL_CONF', 'SMTP_SERVER')
user = ry.read_node_data('EMAIL_CONF', 'USER')
password = ry.read_node_data('EMAIL_CONF', 'PASSWORD')
sender = ry.read_node_data('EMAIL_CONF', 'SENDER')
receives = ry.read_node_data('EMAIL_CONF', 'RECEIVES')
subject = ry.read_node_data('EMAIL_CONF', 'SUBJECT')
content = ry.read_node_data('EMAIL_CONF', 'CONTENT')


class SendEmail:

    def __init__(self, description, pass_num, fail_num, start_time, end_time, continue_time, **kwargs):
        """初始化邮件的配置"""
        self.report_dir = report_dir
        self.case_path = case_path
        self.smtp_server = smtp_server
        self.user = user
        self.password = password
        self.sender = sender
        self.receives = receives
        self.subject = subject
        self.key_value(kwargs)
        # 邮件正文内容
        self.text_content = eval(content % (description, pass_num+fail_num, pass_num, fail_num, start_time,
                                            end_time, continue_time))
        # 报告的内容
        self.report_content = self.read_file(self.latest_report_path())
        # 邮件附件内容
        self.att_content = self.read_file(self.case_path)

    def key_value(self, kwargs):
        """通过传入的字典，进行设定变量值"""
        for key, value in kwargs.items():
            if key == 'report_dir':
                self.report_dir = value
            elif key == 'case_path':
                self.case_path = value
            elif key == 'report_dir':
                self.report_dir = value
            elif key == 'smtp_server':
                self.smtp_server = value
            elif key == 'user':
                self.user = value
            elif key == 'password':
                self.password = value
            elif key == 'sender':
                self.sender = value
            elif key == 'receives':
                self.receives = value
            elif key == 'subject':
                self.subject = value

    # 获取最近测试报告的路径
    def latest_report_path(self):
        # 或目录下的文件目录
        lists = os.listdir(self.report_dir)
        # 按时间顺序对该目录文件夹下面的文件进行排序
        lists.sort(key=lambda fn: os.path.getatime(self.report_dir + '/' + fn))
        return os.path.join(self.report_dir, lists[-1])

    # 获取文件名
    def filename(self, fileParh):
        # 判断路径中是否有‘\\’，有则换成‘/’
        if '/' in  fileParh:
            fileParh = "/".join(fileParh.split('\\'))
        file_name = fileParh.split('\\')[-1]
        return file_name

    # 读取文件
    def read_file(self, filePath):
        with open(filePath, 'rb') as f:
            mail_content = f.read()
        return mail_content

    # 构造附件内容
    def attachment(self, file, filename):
        att = MIMEText(file, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment;filename=%s' % filename
        return att

    # 发送邮件
    def send_email(self):
        # 创建一个带附件的实例
        msg = MIMEMultipart()
        # 构建HTML邮件正文,附件
        msg.attach(MIMEText(self.text_content, 'html', 'utf-8'))
        # 主题
        msg['Subject'] = Header(self.subject, 'utf-8')
        # 构建发送邮件信息
        msg['From'] = self.sender
        # 构建收件邮件信息
        msg['To'] = ','.join(self.receives)
        # 构建附件--测试报告
        msg.attach(self.attachment(self.report_content, self.filename(self.latest_report_path())))
        # 构建附件--case文件
        msg.attach(self.attachment(self.att_content, self.filename(self.case_path)))
        # 链接服务器
        smtp = smtplib.SMTP_SSL(self.smtp_server, 465)
        # 向服务器标识用户身份
        smtp.helo(self.smtp_server)
        # 服务器返回结果确认
        smtp.ehlo(self.smtp_server)
        # 登录邮箱服务器用户名和密码
        smtp.login(self.user, self.password)
        print("Start send Email...")
        smtp.sendmail(self.sender, self.receives, msg.as_string())
        smtp.quit()
        print("Send Email end!")


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    time.sleep(2)
    end_time = datetime.datetime.now()
    s = SendEmail(description=u'测试报告', pass_num=1, fail_num=1, start_time=start_time,
                  end_time=end_time, continue_time=end_time-start_time)
    s.send_email()
    s.latest_report_path()
    s.filename(s.latest_report_path())