

def extract_data(data, key):
    """
    根据传入的key从字典中提取相应的值
    :param data: 格式为字典
    :return 结果以列表形式返回
    """
    result_dict = dict()
    if isinstance(data, dict) and key in data.keys():
        value = data[key]
        result_dict[key] = value
        return result_dict
    elif isinstance(data, (list, tuple)):
        for item in data:
            value = extract_data(item, key)
            if value == "None" or value is None:
                pass
            elif len(value) == 0:
                pass
            else:
                result_dict = value
        return result_dict
    else:
        if isinstance(data, dict):
            for k in data:
                value = extract_data(data[k], key)
                if value == "None" or value is None:
                    pass
                elif len(value) == 0:
                    pass
                else:
                    result_dict = value
            return result_dict