import pandas as pd

from file import File
from tools import to_excel_autowidth_and_border


class SHEXMKTFile(File):
    def __init__(self, file_name):
        super().__init__(file_name)

    def _load_data_lines(self):
        with open(self.file_path, encoding='gbk') as f:
            data = f.read()
        self.data_lines = data.split('\n')

    def _check_data_lines(self):
        self.data_lines = [item for item in self.data_lines if item]
        first_line = self.data_lines[0].split('|')
        last_line = self.data_lines[-1].split('|')
        assert first_line[0] == 'HEADER' and last_line[0] == 'TRAILER'
        tot_num = self._valid_first_line(first_line)
        self.data_lines = self.data_lines[1:-1]
        assert len(self.data_lines) == tot_num

        for line in self.data_lines:
            line_list = line.split('|')
            if line_list[0] == 'MD001':
                self._valid_index_data_line(line_list)
            elif line_list[0] == 'MD002':
                self._valid_market_data_line(line_list)
            elif line_list[0] == 'MD003':
                self._valid_market_data_line(line_list)
            elif line_list[0] == 'MD004':
                self._valid_market_data_line(line_list)

    def _proc_data_lines(self):
        self.index_data_list = []
        self.stock_data_list = []
        self.bond_data_list = []
        self.fund_data_list = []
        self.data_lines = [item.replace(' ', '').split('|') for item in self.data_lines]
        for line_list in self.data_lines:
            if line_list[0] == 'MD001':
                self._merge_index_data(line_list)
            elif line_list[0] == 'MD002':
                self._merge_stock_data(line_list)
            elif line_list[0] == 'MD003':
                self._merge_bond_data(line_list)
            elif line_list[0] == 'MD004':
                self._merge_fund_data(line_list)

    def to_excel(self):
        index_df = pd.DataFrame(self.index_data_list, columns=[
            '行情数据类型',
            '产品代码',
            '产品名称',
            '成交数量',
            '成交金额',
            '昨日收盘价',
            '今日开盘价',
            '最高价',
            '最低价',
            '最新价',
            '今收盘价',
            '指数实时阶段及标志',
            '时间戳'
        ])

        stock_df = pd.DataFrame(self.stock_data_list, columns=[
            '行情数据类型',
            '产品代码',
            '产品名称',
            '成交数量',
            '成交金额',
            '昨日收盘价',
            '今日开盘价',
            '最高价',
            '最低价',
            '最新价',
            '今收盘价',
            '申买价一',
            '申买量一',
            '申卖价一',
            '申卖量一',
            '申买价二',
            '申买量二',
            '申卖价二',
            '申卖量二',
            '申买价三',
            '申买量三',
            '申卖价三',
            '申卖量三',
            '申买价四',
            '申买量四',
            '申卖价四',
            '申卖量四',
            '申买价五',
            '申买量五',
            '申卖价五',
            '申卖量五',
            '产品实现阶段及标志',
            '时间戳',
        ])

        bond_df = pd.DataFrame(self.bond_data_list, columns=[
            '行情数据类型',
            '产品代码',
            '产品名称',
            '成交数量',
            '成交金额',
            '昨日收盘价',
            '今日开盘价',
            '最高价',
            '最低价',
            '最新价',
            '今收盘价',
            '申买价一',
            '申买量一',
            '申卖价一',
            '申卖量一',
            '申买价二',
            '申买量二',
            '申卖价二',
            '申卖量二',
            '申买价三',
            '申买量三',
            '申卖价三',
            '申卖量三',
            '申买价四',
            '申买量四',
            '申卖价四',
            '申卖量四',
            '申买价五',
            '申买量五',
            '申卖价五',
            '申卖量五',
            '产品实现阶段及标志',
            '时间戳',
        ])

        fund_df = pd.DataFrame(self.fund_data_list, columns=[
            '行情数据类型',
            '产品代码',
            '产品名称',
            '成交数量',
            '成交金额',
            '昨日收盘价',
            '今日开盘价',
            '最高价',
            '最低价',
            '最新价',
            '今收盘价',
            '申买价一',
            '申买量一',
            '申卖价一',
            '申卖量一',
            '申买价二',
            '申买量二',
            '申卖价二',
            '申卖量二',
            '申买价三',
            '申买量三',
            '申卖价三',
            '申卖量三',
            '申买价四',
            '申买量四',
            '申卖价四',
            '申卖量四',
            '申买价五',
            '申买量五',
            '申卖价五',
            '申卖量五',
            '基金T-1日收盘时刻IOPV',
            '基金IOPV',
            '产品实现阶段及标志',
            '时间戳',
        ])

        writer = pd.ExcelWriter(self.output_file_path, engine='xlsxwriter')

        to_excel_autowidth_and_border(writer, index_df, sheetname='指数行情', startrow=0, startcol=0)
        to_excel_autowidth_and_border(writer, stock_df, sheetname='股票（A、B 股）行情', startrow=0, startcol=0)
        to_excel_autowidth_and_border(writer, bond_df, sheetname='债券分销行情', startrow=0, startcol=0)
        to_excel_autowidth_and_border(writer, fund_df, sheetname='基金行情', startrow=0, startcol=0)

        writer.close()

    @staticmethod
    def _valid_first_line(line_list):
        version = line_list[1]
        assert len(version) == 8
        body_length = line_list[2]
        assert len(body_length) == 10
        tot_num_trade_reports = line_list[3]
        assert len(tot_num_trade_reports) == 5
        md_report_id = line_list[4]
        assert len(md_report_id) == 8
        sender_comp_id = line_list[5]
        assert len(sender_comp_id) == 6
        md_time = line_list[6]
        assert len(md_time) == 21
        md_update_type = line_list[7]
        assert len(md_update_type) == 1
        md_ses_status = line_list[8]
        assert len(md_ses_status) == 8

        return int(tot_num_trade_reports)

    @staticmethod
    def _valid_index_data_line(line_list):
        security_id = line_list[1]
        assert len(security_id) == 6
        symbol = line_list[2]
        assert len(symbol.encode('gbk')) == 8
        trade_volume = line_list[3]
        assert len(trade_volume) == 16
        total_value_traded = line_list[4]
        assert len(total_value_traded.split('.')[0]) == 13 and len(total_value_traded.split('.')[1]) == 2
        pre_close_px = line_list[5]
        assert len(pre_close_px.split('.')[0]) == 6 and len(pre_close_px.split('.')[1]) == 4
        open_price = line_list[6]
        assert len(open_price.split('.')[0]) == 6 and len(open_price.split('.')[1]) == 4
        high_price = line_list[7]
        assert len(high_price.split('.')[0]) == 6 and len(high_price.split('.')[1]) == 4
        low_price = line_list[8]
        assert len(low_price.split('.')[0]) == 6 and len(low_price.split('.')[1]) == 4
        trade_price = line_list[9]
        assert len(trade_price.split('.')[0]) == 6 and len(trade_price.split('.')[1]) == 4
        close_px = line_list[10]
        assert len(close_px.split('.')[0]) == 6 and len(close_px.split('.')[1]) == 4
        trading_phase_code = line_list[11]
        assert len(trading_phase_code) == 8
        timestamp = line_list[12]
        assert len(timestamp) == 12

    @staticmethod
    def _valid_market_data_line(line_list):
        md_stream_id = line_list[0]
        security_id = line_list[1]
        assert len(security_id) == 6
        symbol = line_list[2]
        assert len(symbol.encode('gbk')) == 8
        trade_volume = line_list[3]
        assert len(trade_volume) == 16
        total_value_traded = line_list[4]
        assert len(total_value_traded.split('.')[0]) == 13 and len(total_value_traded.split('.')[1]) == 2
        pre_close_px = line_list[5]
        assert len(pre_close_px.split('.')[0]) == 7 and len(pre_close_px.split('.')[1]) == 3
        open_price = line_list[6]
        assert len(open_price.split('.')[0]) == 7 and len(open_price.split('.')[1]) == 3
        high_price = line_list[7]
        assert len(high_price.split('.')[0]) == 7 and len(high_price.split('.')[1]) == 3
        low_price = line_list[8]
        assert len(low_price.split('.')[0]) == 7 and len(low_price.split('.')[1]) == 3
        trade_price = line_list[9]
        assert len(trade_price.split('.')[0]) == 7 and len(trade_price.split('.')[1]) == 3
        close_px = line_list[10]
        assert len(close_px.split('.')[0]) == 7 and len(close_px.split('.')[1]) == 3
        buy_price_one = line_list[11]
        assert len(buy_price_one.split('.')[0]) == 7 and len(buy_price_one.split('.')[1]) == 3
        buy_volume_one = line_list[12]
        assert len(buy_volume_one) == 12
        sell_price_one = line_list[13]
        assert len(sell_price_one.split('.')[0]) == 7 and len(sell_price_one.split('.')[1]) == 3
        sell_volume_one = line_list[14]
        assert len(sell_volume_one) == 12
        buy_price_two = line_list[15]
        assert len(buy_price_two.split('.')[0]) == 7 and len(buy_price_two.split('.')[1]) == 3
        buy_volume_two = line_list[16]
        assert len(buy_volume_two) == 12
        sell_price_two = line_list[17]
        assert len(sell_price_two.split('.')[0]) == 7 and len(sell_price_two.split('.')[1]) == 3
        sell_volume_two = line_list[18]
        assert len(sell_volume_two) == 12
        buy_price_three = line_list[19]
        assert len(buy_price_three.split('.')[0]) == 7 and len(buy_price_three.split('.')[1]) == 3
        buy_volume_three = line_list[20]
        assert len(buy_volume_three) == 12
        sell_price_three = line_list[21]
        assert len(sell_price_three.split('.')[0]) == 7 and len(sell_price_three.split('.')[1]) == 3
        sell_volume_three = line_list[22]
        assert len(sell_volume_three) == 12
        buy_price_four = line_list[23]
        assert len(buy_price_four.split('.')[0]) == 7 and len(buy_price_four.split('.')[1]) == 3
        buy_volume_four = line_list[24]
        assert len(buy_volume_four) == 12
        sell_price_four = line_list[25]
        assert len(sell_price_four.split('.')[0]) == 7 and len(sell_price_four.split('.')[1]) == 3
        sell_volume_four = line_list[26]
        assert len(sell_volume_four) == 12
        buy_price_five = line_list[27]
        assert len(buy_price_five.split('.')[0]) == 7 and len(buy_price_five.split('.')[1]) == 3
        buy_volume_five = line_list[28]
        assert len(buy_volume_five) == 12
        sell_price_five = line_list[29]
        assert len(sell_price_five.split('.')[0]) == 7 and len(sell_price_five.split('.')[1]) == 3
        sell_volume_five = line_list[30]
        assert len(sell_volume_five) == 12

        if md_stream_id == 'MD004':
            prev_close_iopv = line_list[31]
            assert len(prev_close_iopv.split('.')[0]) == 7 and len(prev_close_iopv.split('.')[1]) == 3
            iopv = line_list[32]
            assert len(iopv.split('.')[0]) == 7 and len(iopv.split('.')[1]) == 3
            trading_phase_code = line_list[33]
            assert len(trading_phase_code) == 8
            timestamp = line_list[34]
            assert len(timestamp) == 12
        else:
            trading_phase_code = line_list[31]
            assert len(trading_phase_code) == 8
            timestamp = line_list[32]
            assert len(timestamp) == 12

    def _merge_index_data(self, line_list):
        md_stream_id = line_list[0]
        security_id = line_list[1]
        symbol = line_list[2]
        trade_volume = line_list[3]
        total_value_traded = line_list[4]
        pre_close_px = line_list[5]
        open_price = line_list[6]
        high_price = line_list[7]
        low_price = line_list[8]
        trade_price = line_list[9]
        close_px = line_list[10]
        trading_phase_code = line_list[11]
        timestamp = line_list[12]
        self.index_data_list.append([
            md_stream_id,
            security_id,
            symbol,
            trade_volume,
            total_value_traded,
            pre_close_px,
            open_price,
            high_price,
            low_price,
            trade_price,
            close_px,
            trading_phase_code,
            timestamp,
        ])

    def _merge_stock_data(self, line_list):
        md_stream_id = line_list[0]
        security_id = line_list[1]
        symbol = line_list[2]
        trade_volume = line_list[3]
        total_value_traded = line_list[4]
        pre_close_px = line_list[5]
        open_price = line_list[6]
        high_price = line_list[7]
        low_price = line_list[8]
        trade_price = line_list[9]
        close_px = line_list[10]
        buy_price_one = line_list[11]
        buy_volume_one = line_list[12]
        sell_price_one = line_list[13]
        sell_volume_one = line_list[14]
        buy_price_two = line_list[15]
        buy_volume_two = line_list[16]
        sell_price_two = line_list[17]
        sell_volume_two = line_list[18]
        buy_price_three = line_list[19]
        buy_volume_three = line_list[20]
        sell_price_three = line_list[21]
        sell_volume_three = line_list[22]
        buy_price_four = line_list[23]
        buy_volume_four = line_list[24]
        sell_price_four = line_list[25]
        sell_volume_four = line_list[26]
        buy_price_five = line_list[27]
        buy_volume_five = line_list[28]
        sell_price_five = line_list[29]
        sell_volume_five = line_list[30]
        trading_phase_code = line_list[31]
        timestamp = line_list[32]

        self.stock_data_list.append([
            md_stream_id,
            security_id,
            symbol,
            trade_volume,
            total_value_traded,
            pre_close_px,
            open_price,
            high_price,
            low_price,
            trade_price,
            close_px,
            buy_price_one,
            buy_volume_one,
            sell_price_one,
            sell_volume_one,
            buy_price_two,
            buy_volume_two,
            sell_price_two,
            sell_volume_two,
            buy_price_three,
            buy_volume_three,
            sell_price_three,
            sell_volume_three,
            buy_price_four,
            buy_volume_four,
            sell_price_four,
            sell_volume_four,
            buy_price_five,
            buy_volume_five,
            sell_price_five,
            sell_volume_five,
            trading_phase_code,
            timestamp,
        ])

    def _merge_bond_data(self, line_list):
        md_stream_id = line_list[0]
        security_id = line_list[1]
        symbol = line_list[2]
        trade_volume = line_list[3]
        total_value_traded = line_list[4]
        pre_close_px = line_list[5]
        open_price = line_list[6]
        high_price = line_list[7]
        low_price = line_list[8]
        trade_price = line_list[9]
        close_px = line_list[10]
        buy_price_one = line_list[11]
        buy_volume_one = line_list[12]
        sell_price_one = line_list[13]
        sell_volume_one = line_list[14]
        buy_price_two = line_list[15]
        buy_volume_two = line_list[16]
        sell_price_two = line_list[17]
        sell_volume_two = line_list[18]
        buy_price_three = line_list[19]
        buy_volume_three = line_list[20]
        sell_price_three = line_list[21]
        sell_volume_three = line_list[22]
        buy_price_four = line_list[23]
        buy_volume_four = line_list[24]
        sell_price_four = line_list[25]
        sell_volume_four = line_list[26]
        buy_price_five = line_list[27]
        buy_volume_five = line_list[28]
        sell_price_five = line_list[29]
        sell_volume_five = line_list[30]
        trading_phase_code = line_list[31]
        timestamp = line_list[32]

        self.bond_data_list.append([
            md_stream_id,
            security_id,
            symbol,
            trade_volume,
            total_value_traded,
            pre_close_px,
            open_price,
            high_price,
            low_price,
            trade_price,
            close_px,
            buy_price_one,
            buy_volume_one,
            sell_price_one,
            sell_volume_one,
            buy_price_two,
            buy_volume_two,
            sell_price_two,
            sell_volume_two,
            buy_price_three,
            buy_volume_three,
            sell_price_three,
            sell_volume_three,
            buy_price_four,
            buy_volume_four,
            sell_price_four,
            sell_volume_four,
            buy_price_five,
            buy_volume_five,
            sell_price_five,
            sell_volume_five,
            trading_phase_code,
            timestamp,
        ])

    def _merge_fund_data(self, line_list):
        md_stream_id = line_list[0]
        security_id = line_list[1]
        symbol = line_list[2]
        trade_volume = line_list[3]
        total_value_traded = line_list[4]
        pre_close_px = line_list[5]
        open_price = line_list[6]
        high_price = line_list[7]
        low_price = line_list[8]
        trade_price = line_list[9]
        close_px = line_list[10]
        buy_price_one = line_list[11]
        buy_volume_one = line_list[12]
        sell_price_one = line_list[13]
        sell_volume_one = line_list[14]
        buy_price_two = line_list[15]
        buy_volume_two = line_list[16]
        sell_price_two = line_list[17]
        sell_volume_two = line_list[18]
        buy_price_three = line_list[19]
        buy_volume_three = line_list[20]
        sell_price_three = line_list[21]
        sell_volume_three = line_list[22]
        buy_price_four = line_list[23]
        buy_volume_four = line_list[24]
        sell_price_four = line_list[25]
        sell_volume_four = line_list[26]
        buy_price_five = line_list[27]
        buy_volume_five = line_list[28]
        sell_price_five = line_list[29]
        sell_volume_five = line_list[30]
        prev_close_iopv = line_list[31]
        iopv = line_list[32]
        trading_phase_code = line_list[33]
        timestamp = line_list[34]

        self.fund_data_list.append([
            md_stream_id,
            security_id,
            symbol,
            trade_volume,
            total_value_traded,
            pre_close_px,
            open_price,
            high_price,
            low_price,
            trade_price,
            close_px,
            buy_price_one,
            buy_volume_one,
            sell_price_one,
            sell_volume_one,
            buy_price_two,
            buy_volume_two,
            sell_price_two,
            sell_volume_two,
            buy_price_three,
            buy_volume_three,
            sell_price_three,
            sell_volume_three,
            buy_price_four,
            buy_volume_four,
            sell_price_four,
            sell_volume_four,
            buy_price_five,
            buy_volume_five,
            sell_price_five,
            sell_volume_five,
            prev_close_iopv,
            iopv,
            trading_phase_code,
            timestamp,
        ])


if __name__ == '__main__':
    file = SHEXMKTFile('mktdt00_20230708.txt')
    print(file)
    file.to_excel()
