import os
import re
from common.readYaml import ReadYaml


class OptimizeData(object):
    """用于对数据的优化处理"""

    def __init__(self, table_data, filter_rule=None, format_require=None):
        """
        :param table_data: 需要处理的sheet页的数据
        :param filter_rule: 字典，如{'run'： 'N',...}
        :param format_require: 检查字段需要符合的格式要求
        :return:
        """
        self.table_data = table_data
        self.filter_rule = filter_rule
        self.format_require = format_require
        # original_data: 读取的所有case数据，格式为[{},{},...]
        self.original_data = list()
        # filter_data: 过滤不需要执行的case后的数据，格式为[{},{},...]
        self.filter_after_data = list()
        # conf_table_header：配置文件表头的信息
        self.conf_table_header = list()
        # table_head_keys：case表格的表头的信息
        self.table_head_keys = list()
        # row_list：过滤后的case所在表格行
        self.row_list = list()
        self.ry = ReadYaml(os.path.join(os.path.dirname(os.path.realpath(__file__)), r"..\Config\config.yaml"))
        self.get_filter_rule()
        self.get_format_require()
        self.combine_to_dict()

    def get_filter_rule(self):
        """获取过滤规则"""
        if self.filter_rule is None:
            self.filter_rule = self.ry.read_node_data('CASE_CONF', 'RULE_DICT')

    def get_format_require(self):
        """获取字段格式
        {0: {'IS_NONE': 'N', 'VALUE': 'no_check', 'TYPE': 'no_check', 'RE': 'no_check'},
        3: {'IS_NONE': 'N', 'VALUE': ['URL_1'], 'TYPE': 'no_check', 'RE': 'no_check'},'':{},...}
        """
        if self.format_require is None:
            format_require_dic = dict()
            fr = self.ry.read_node_data('CASE_CONF', 'CASE_FIELD')
            fr.pop('RESULT')
            fr.pop('RESPONSE')
            f_list = list(fr.values())
            for f in f_list:
                self.conf_table_header.append(f['NAME'])
                if f['FORMAT'] != {'IS_NONE': 'Y', 'VALUE': 'no_check', 'TYPE': 'no_check', 'RE': 'no_check'}:
                    format_require_dic[f['INDEX']] = f['FORMAT']
            self.conf_table_header += [self.ry.read_node_data('CASE_CONF', 'CASE_FIELD', 'RESULT', 'NAME'),
                                       self.ry.read_node_data('CASE_CONF', 'CASE_FIELD', 'RESPONSE', 'NAME')]
            self.format_require = format_require_dic

    def combine_to_dict(self):
        """key，value一一对应来组合转换为字典,，返回一个元素为字典的列表"""
        # 获取总行数
        total_row = self.table_data.nrows
        if total_row > 1:
            # 获取第一行的内容，列表格式
            keys = self.table_data.row_values(0)
            # 获取每一行的内容，列表格式
            for row in range(1, total_row):
                row_value = self.table_data.row_values(row)
                row_value_n = list()
                # 去掉字符两端空格
                for value in row_value:
                    row_value_n.append(value.strip())
                case_dict = dict(zip(keys, row_value_n))
                self.original_data.append(case_dict)
                self.table_head_keys = list(key.lower() for key in self.original_data[0].keys())
        else:
            print("表格未填写数据")

    def filter(self):
        """过滤不需要执行的case"""
        num = 0
        r_keys = list(key.lower() for key in self.filter_rule.keys())
        # 判断c_keys是否是d_keys的子集，如果是则进行过滤操作
        if set(r_keys).issubset(set(self.table_head_keys)):
            for case_data in self.original_data:
                num += 1
                temp = True
                for key in r_keys:
                    if case_data[key] == self.filter_rule[key.upper()]:
                        temp = False
                        break
                if temp:
                    # 加入之前，将数据中的basic_url进行替换成实际需要的url
                    url_ = case_data[self.ry.read_node_data('CASE_CONF', 'CASE_FIELD', 'BASIC_URL', 'NAME')]
                    case_data[self.ry.read_node_data('CASE_CONF', 'CASE_FIELD', 'BASIC_URL', 'NAME')] = \
                        self.ry.read_node_data('CASE_CONF', 'CASE_FIELD', 'BASIC_URL', url_)
                    self.row_list.append(num)
                    self.filter_after_data.append(case_data)
        else:
            print('“rule_dic”中key关键字含有不在表头之内的字段')

    def check_format(self):
        """对数据进行格式检查"""
        res = dict()
        fr_keys = list(self.format_require.keys())
        for col in fr_keys:
            num = 0
            table_col_data = self.table_data.col_values(col)
            for value in table_col_data[1:]:
                num += 1
                if self.format_require[col]['IS_NONE'] == 'N':
                    if value.strip() == '':
                        try:
                            res[self.table_data.row_values(num)[0]].append(table_col_data[0])
                        except:
                            res[self.table_data.row_values(num)[0]] = list()
                            res[self.table_data.row_values(num)[0]].append(table_col_data[0])
                        continue
                else:
                    if value.strip() == 'None':
                        continue
                fag = True
                # 检验VALUE
                if self.format_require[col]['VALUE'] == 'no_check':
                    pass
                else:
                    if OptimizeData.check_value(value.strip(), self.format_require[col]['VALUE']):
                        continue
                    else:
                        fag = False
                # 检验TYPE
                if self.format_require[col]['TYPE'] == 'no_check':
                    pass
                else:
                    if OptimizeData.check_type(value.strip(), eval(self.format_require[col]['TYPE'])):
                        continue
                    else:
                        fag = False
                # 检验RE
                if self.format_require[col]['RE'] == 'no_check':
                    pass
                else:
                    if OptimizeData.check_re(value.strip(), self.format_require[col]['RE']):
                        continue
                    else:
                        fag = False
                if fag is False:
                    try:
                        res[self.table_data.row_values(num)[0]].append(table_col_data[0])
                    except:
                        res[self.table_data.row_values(num)[0]] = list()
                        res[self.table_data.row_values(num)[0]].append(table_col_data[0])
        return res

    @staticmethod
    def check_value(value, limit):
        """检查字段的值是否符合限定的条件
        :param value: 需要检查的数据
        :param limit: 限定的条件，类型为列表
        :return 返回结果，类型为bool
        """
        if value in limit:
            return True
        else:
            return False

    @staticmethod
    def check_type(ch_data, ch_type):
        """检查字段的数据类型
        :param ch_data: 需要检查的数据
        :param ch_type: 类型
        :return 返回结果，类型为bool
        """
        if OptimizeData.check_re(ch_data, '{.*}'):
            try:
                ch_data = eval(ch_data)
            except:
                return False
        if isinstance(ch_data, ch_type):
            return True
        else:
            return False

    @staticmethod
    def check_re(re_data, r):
        """检查字段的数据类型
        :param re_data: 需要匹配的数据
        :param r: 正则表达式
        :return 返回结果，类型为bool
        """
        if re.match(r, re_data):
            return True
        else:
            return False

    def optimize(self):
        """数据优化执行主程序"""
        # 检查表头信息是否与配置文件的一致
        if self.conf_table_header == self.table_head_keys:
            check_res = self.check_format()
            if check_res == dict():
                if self.original_data:
                    self.filter()
                    return self.filter_after_data, self.row_list
                else:
                    print('original_data为空列表')
            else:
                print('case数据有误，错误地方%s' % check_res)
        else:
            print('case表头信息是与配置文件的不一致')


if __name__ == '__main__':
    from common.operationExcel import OperationExcel

    c = OperationExcel(r"..\CaseData\case.xls")
    table_data = c.get_table_data(0)
    op = OptimizeData(table_data)

    print(op.optimize())

    # print(op.format_require)
