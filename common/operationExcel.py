import xlrd
import os
from common.readYaml import ReadYaml
from xlutils.copy import copy
from common.log import LOG, logger
from common.optimizeData import OptimizeData


class OperationExcel(object):
    """操作Execl表类"""

    def __init__(self, path):
        self.path = path
        self.ry = ReadYaml(os.path.join(os.path.dirname(os.path.realpath(__file__)), r"..\Config\config.yaml"))
        self.response = self.ry.read_node_data('CASE_CONF', 'CASE_FIELD', 'RESPONSE', 'IS_WRITE')

    def open_execl(self):
        """打开Execl"""
        try:
            # formatting_info=True 写入数据时不会改变原有格式
            execl_data = xlrd.open_workbook(self.path, formatting_info=True)
            return execl_data
        except Exception as e:
            LOG.error("""打开%s失败，
                         错误原因%s""" % (self.path, e))
            print('打开%s失败\n\r错误原因%s' % (self.path, e))

    def get_table_data(self, name_or_index):
        """根据sheet索引或者名称获取sheet内容
        sheet索引从0开始
        :type name_or_index: int or str
        """
        sheet_data = None
        if isinstance(name_or_index, int):
            sheet_data = self.open_execl().sheet_by_index(name_or_index)
        elif isinstance(name_or_index, str):
            sheet_data = self.open_execl().sheet_by_name(name_or_index)
        return sheet_data

    def get_sheet_row(self, name_or_index):
        """获取总行数"""
        total_row = self.get_table_data(name_or_index).nrows
        return total_row

    def get_sheet_col(self, name_or_index):
        """获取总列数"""
        total_cols = self.get_table_data(name_or_index).ncols
        return total_cols

    def get_row_data(self, name_or_index, row_int):
        """获取整行的值（数组）
        row_int：行数，索引从0开始
        """
        row_data = self.get_table_data(name_or_index).row_values(row_int)
        return row_data

    def get_col_data(self, name_or_index, col_int):
        """获取整列的值（数组）
        col_int：列数，索引从0开始
        """
        col_data = self.get_table_data(name_or_index).col_values(col_int)
        return col_data

    def get_value(self, name_or_index, row, col):
        """获取单元格内容"""
        value = self.get_table_data(name_or_index).cell(row, col).value.encode('utf-8')
        return value

    def get_index(self, name_or_index, key):
        """表头通过字段获取所在列的索引，注意：索引从0开始"""
        keys = self.get_row_data(name_or_index, 0)
        num = 0
        for k in keys:
            if key == k:
                return num
            num += 1
        else:
            return None

    @logger('common.operationExecl.OperationExecl.get_data', 'case的sheet索引值')
    def get_data(self, name_or_index):
        """获取case数据，返回为列表"""
        optimize_data = OptimizeData(self.get_table_data(name_or_index))
        case_data = optimize_data.optimize()
        if case_data:
            return case_data
        print('case数据获取失败')

    def copy_execl(self, index):
        """写入数据前复制文件"""
        # 先复制一份数据
        copy_data = copy(self.open_execl())
        # 通过下标获取表
        table_data = copy_data.get_sheet(index)
        return copy_data, table_data

    def write_data(self, table_data, row, col, value):
        """写入数据
        row：需要修改的行  --> int
        col： 需要修改的列  --> int
        value: 写入的数据  --> str
        """
        try:
            # 通过行，列写入数据
            table_data.write(row, col, value)
        except Exception as e:
            table_data.write(row, col, 'WRITE_ERROR')
            LOG.error("""写入%s行%s列数据%s失败
                         错误原因为：%s""" % (row, col, value, e))
            print("""写入%s行%s列数据%s失败
                         错误原因为：%s""" % (row, col, value, e))

    def save(self, copy_data):
        """写入完后保存文件"""
        # 保存文件
        copy_data.save(self.path)


if __name__ == '__main__':
    c = OperationExcel(r"..\CaseData\case.xls")
    # d = c.get_data(0)
    # s = c.get_table_data(0)

    # print(s)

    # print(c.get_col_data(0, 2))

    # copy_data, table_data = c.copy_execl(0)
    # c.write_data(table_data, 2, 10, 'passaa')
    # c.save(copy_data)
    d = c.get_data(0)
    print(d)

    # v = c.get_index(0, 'result')
    # print(v)
