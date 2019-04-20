

def split_list(data_list):
    """将大列表拆分为小列表"""
    n = 1  # 大列表中几个数据组成一个小列表
    data = [data_list[i:i + n] for i in range(0, len(data_list), n)]
    return data
