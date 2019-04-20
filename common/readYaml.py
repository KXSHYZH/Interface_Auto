import yaml
import os


class ReadYaml(object):

    def __init__(self, conf_path):
        self.conf_path = conf_path

    def read_node_data(self, *args):
        """
        读取配置文件的内容
        args： 输入‘根节点’，‘子节点’，‘子节点’，...
        :return 通过根节点和子节点获取到的信息
        """
        with open(self.conf_path, 'r', encoding='utf-8') as f:
            conf_str = f.read()  # 读出来是字符串
        conf_dict = yaml.load(conf_str)  # 用load方法转字典
        node_data = self.by_key_get_value(conf_dict, args)
        return node_data

    def by_key_get_value(self, data_dict, key_tuple, start=0):
        value = data_dict[key_tuple[start]]
        start += 1
        if start >= len(key_tuple):
            return value
        return self.by_key_get_value(value, key_tuple, start)


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    conf_path = os.path.join(path, r"..\Config\config.yaml")
    ry = ReadYaml(conf_path)
    r = ry.read_node_data('CASE_CONF')
    print(r)
