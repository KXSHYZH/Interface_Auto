1、使用方式<br>
<br>
import unittest<br>
from common.BeautifulReport import BeautifulReport<br>
<br>
if __name__ == '__main__':<br>
    test_suite = unittest.defaultTestLoader.discover('../tests', pattern='test*.py')<br>
    result = BeautifulReport(test_suite)<br>
    result.report(filename='测试报告', description='测试报告', report_path='report')<br>
    <br>
2、Report API简介<br>
<br>
- BeautifulReport.report<br>
  - report (<br>
    filename -> 测试报告名称, 如果不指定默认文件名为report.html<br>
    description -> 测试报告用例名称展示<br>
    report_path='.' -> log文件写入路径<br>
    )<br>
<br>
<br><br><br>

<h4>Excel怎么批量删除空白行_Excel快速删除空行？<h4>
https://jingyan.baidu.com/article/b907e6276b6c6d46e6891c49.html<br>
1、首先，将鼠标移到开始菜单栏下的“查找和选择”选项上，左键单击一下。<br>
2、在出现的多个选项中，选择并点击一下第四个选项“定位条件”。<br>
3、在出现的定位条件选择窗口中，选择左侧第四个选项“空值”(没有数据的单元格)；然后再点击一下“确定”按钮。<br>
4、操作完上面的步骤，可以看到表格中有数据的区域中的空白单元格已经被选中了。<br>
5、将鼠标移到被选中的区域；单击鼠标右键；然后在出现的选项中点击“删除”。<br>
6、在弹出的删除窗口中，选中“下方单元格上移”选项；然后点击“确定”按钮。<br>
7、执行完上面的删除操作，有数据的区域的所有空行就都被清除掉了。Excel快速删除大量空白行的操作就完成了！<br>
