

def print_info(case_data, response_data_str, res):
    """打印详细数据"""
    result_data = """
                </br>
                请求方式：%s ,请求URL：%s</br>
                请求params：%s</br>
                预期：%s</br>
                用例测试结果：%s</br>
                实际返回结果：</br>
                %s""" % (case_data['method'], case_data['basic_url'], case_data['parameter'], case_data['expected'],
                         res, response_data_str)
    return result_data