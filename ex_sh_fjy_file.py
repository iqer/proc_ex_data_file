import pandas as pd

from file import File
from tools import to_excel_autowidth_and_border


class SHEXFjyFile(File):
    def __init__(self, file_name):
        super().__init__(file_name)

    def _load_data_lines(self):
        with open(self.file_path, encoding='gbk') as f:
            data = f.read()
        self.data_lines = data.split('\n')

    def _check_data_lines(self):
        data_lines = [item.split('|') for item in self.data_lines if item]
        for line in data_lines:
            data_type = line[0]
            assert data_type == 'R0001'
            non_trade_security_code = line[1]
            assert len(non_trade_security_code) == 6
            non_trade_security_name = line[2]
            assert len(non_trade_security_name.encode('gbk')) == 8
            product_security_code = line[3]
            assert len(product_security_code) == 6
            product_security_name = line[4]
            assert len(product_security_name.encode('gbk')) == 8
            non_trade_business_type = line[5]
            assert non_trade_business_type in [
                'IN', 'IS', 'PH', 'KK', 'HK',
                'R1', 'R2', 'R3', 'R4', 'OS',
                'OC', 'OR', 'OD', 'OT', 'OV',
                'FS', 'FC', 'ST', 'SR', 'CI',
                'CO', 'SI', 'SO', 'PA', 'QT',
            ]
            # 非交易订单输入开始日期
            non_trade_order_start_date = line[6]
            assert len(non_trade_order_start_date) == 8
            non_trade_order_end_date = line[7]
            assert len(non_trade_order_end_date) == 8
            # 非交易订单整手数
            non_trade_order_lot = line[8]
            assert len(non_trade_order_lot) == 12
            non_trade_order_min_quantity = line[9]
            assert len(non_trade_order_min_quantity) == 12
            non_trade_order_max_quantity = line[10]
            assert len(non_trade_order_max_quantity) == 12
            # 非交易价格
            non_trade_price = line[11]
            assert len(non_trade_price.split('.')[0]) == 7 and len(non_trade_price.split('.')[1]) == 5
            # IPO总量
            ipo_total_quantity = line[12]
            assert len(ipo_total_quantity) == 16
            # IPO分配方法
            ipo_distribution_method = line[13]
            assert (non_trade_business_type in ['IN', 'IS'] and ipo_distribution_method in ['L', 'A', 'P']) or (
                    len(ipo_distribution_method) == 1)
            # IPO竞价分配或比例配售日期
            ipo_distribution_date = line[14]
            assert len(ipo_distribution_date) == 8
            # IPO验资或配号日期
            ipo_check_date = line[15]
            assert len(ipo_check_date) == 8
            # IPO摇号抽签的日期
            ipo_lottery_date = line[16]
            assert len(ipo_lottery_date) == 8
            # IPO申购价格区间下限
            ipo_price_lower_limit = line[17]
            assert len(ipo_price_lower_limit.split('.')[0]) == 7 and len(ipo_price_lower_limit.split('.')[1]) == 3
            # IPO申购价格区间上限
            ipo_price_upper_limit = line[18]
            assert len(ipo_price_upper_limit.split('.')[0]) == 7 and len(ipo_price_upper_limit.split('.')[1]) == 3
            # IPO比例配售比例
            ipo_distribution_ratio = line[19]
            assert len(ipo_distribution_ratio.split('.')[0]) == 7 and len(ipo_distribution_ratio.split('.')[1]) == 3
            # 配股股权登记日
            allotment_registration_date = line[20]
            assert len(allotment_registration_date) == 8
            # 配股股权除权日
            allotment_ex_rights_date = line[21]
            assert len(allotment_ex_rights_date) == 8
            # 配股比例
            allotment_ratio = line[22]
            assert len(allotment_ratio.split('.')[0]) == 4 and len(allotment_ratio.split('.')[1]) == 6
            # 配股总量
            allotment_total_quantity = line[23]
            assert len(allotment_total_quantity) == 16
            # T-2日基金收益/基金净值
            t_2_fund_income = line[24]
            assert len(t_2_fund_income.split('.')[0]) == 7 and len(t_2_fund_income.split('.')[1]) == 5
            t_1_fund_income = line[25]
            assert len(t_1_fund_income.split('.')[0]) == 7 and len(t_1_fund_income.split('.')[1]) == 5
            # 发行方式
            issue_method = line[26]
            assert (non_trade_business_type in ['IN', 'IS'] and ipo_distribution_method == 'L' and
                    issue_method in ['001', '002', '003']) or (len(issue_method) == 3)
            # 备注
            remark = line[27]
            assert len(remark) == 46

    def _proc_data_lines(self):
        self.data_lines = [item.replace(' ', '').split('|') for item in self.data_lines]

    def to_excel(self):
        writer = pd.ExcelWriter(self.output_file_path, engine='xlsxwriter')
        df = pd.DataFrame(self.data_lines, columns=[
            '参考数据类型',
            '非交易证券代码',
            '非交易证券名称',
            '产品证券代码',
            '产品证券名称',
            '非交易业务类型',
            '非交易订单输入开始日期',
            '非交易订单输入结束日期',
            '非交易订单整手数',
            '非交易订单最小数量',
            '非交易订单最大数量',
            '非交易价格',
            'IPO总量',
            'IPO分配方法',
            'IPO竞价分配或比例配售日期',
            'IPO验资或配号日期',
            'IPO摇号抽签的日期',
            'IPO申购价格区间下限',
            'IPO申购价格区间上限',
            'IPO比例配售比例',
            '配股股权登记日',
            '配股除权日',
            '配股比例',
            '配股总量',
            'T-2日基金收益/基金净值',
            'T-1日基金收益/基金净值',
            '发行方式',
            '备注',
        ])
        to_excel_autowidth_and_border(writer, df, sheetname='产品非交易基础信息', startrow=0, startcol=0)
        writer.close()


if __name__ == '__main__':
    file = SHEXFjyFile('fjy20230708.txt')
    file.to_excel()
