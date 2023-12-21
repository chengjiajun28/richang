import os
# 文件目录
abs_path = os.path.abspath(__file__)
import sys
sys.path.append(abs_path[0:abs_path.find('auction') - 1])


from auction.BaseCrawler import BaseCrawler


class CJJ(BaseCrawler):

    def data_list(self, *args, **kwargs):
        pass

    def data_details(self, *args, **kwargs):
        pass

    def get_total_page(self, *args, **kwargs):
        pass

    def parse_data_list(self, *args, **kwargs):
        pass

    def parse_data_details(self, *args, **kwargs):
        pass

    def action(self, *args, **kwargs):
        a = "售楼处案场置物架"
        datas = self.exist_by_aution_name(a)
        print(datas)


if __name__ == '__main__':
    cjj = CJJ()
    cjj.action()
