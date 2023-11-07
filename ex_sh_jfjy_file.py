from xml.dom.minidom import parseString

import pandas as pd

from file import File
from tools import to_excel_autowidth_and_border


class SHEXJfjyFile(File):
    def __init__(self, file_name):
        super().__init__(file_name)

    def _load_data_lines(self):
        content = open(self.file_path, encoding='gbk').read()
        dom = parseString(content)
        root = dom.documentElement

        element_list = []
        child_ele = {}
        for child in root.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                if child.tagName == 'Non_Trd_Rec':
                    child_ele = {}
                for subchild in child.childNodes:
                    if subchild.nodeType == subchild.ELEMENT_NODE:
                        child_ele[subchild.tagName] = subchild.firstChild.nodeValue
            if child_ele:
                element_list.append(child_ele)
                child_ele = {}
        self.data_lines = element_list

    def _check_data_lines(self):
        data_lines = self.data_lines
        for line in data_lines:
            inst_id = line['Inst_ID']
            assert len(inst_id) == 6
            inst_name = line['Inst_Nam']
            assert len(inst_name.encode('gbk')) == 8
            busi_typ = line['Busi_Typ']
            assert busi_typ in ['IEC', 'IER', 'GEC', 'GER', 'EEC', 'EER']

            if busi_typ in ['IEC', 'IER', 'GEC', 'GER']:
                continue
            elif busi_typ in ['EEC', 'EER']:
                crea_rtgs_tag = line['Crea_Rtgs_Tag']
                if busi_typ == 'EEC':
                    assert crea_rtgs_tag in ['0', '1']
                else:
                    assert len(crea_rtgs_tag) == 1

    def _proc_data_lines(self):
        etf_goods_gold_list = []
        # ETF现金申赎
        etf_cash_list = []
        data_lines = self.data_lines
        for line in data_lines:
            inst_id = line['Inst_ID']
            inst_name = line['Inst_Nam']
            busi_typ = line['Busi_Typ']
            if busi_typ in ['IEC', 'IER', 'GEC', 'GER']:
                item = [inst_id, inst_name, busi_typ]
                etf_goods_gold_list.append(item)
            elif busi_typ in ['EEC', 'EER']:
                crea_rtgs_tag = line['Crea_Rtgs_Tag']
                item = [inst_id, inst_name, busi_typ, crea_rtgs_tag]
                etf_cash_list.append(item)
        self.etf_goods_gold_list = etf_goods_gold_list
        self.etf_cash_list = etf_cash_list

    def to_excel(self):
        writer = pd.ExcelWriter(self.output_file_path, engine='xlsxwriter')
        df = pd.DataFrame(self.etf_goods_gold_list, columns=[
            '证券代码',
            '证券简称',
            '业务类型',
        ])
        to_excel_autowidth_and_border(writer, df, sheetname='ETF实物黄金申赎', startrow=0, startcol=0)
        df = pd.DataFrame(self.etf_cash_list, columns=[
            '证券代码',
            '证券简称',
            '业务类型',
            'RTGS申购标志',
        ])
        to_excel_autowidth_and_border(writer, df, sheetname='ETF现金申赎', startrow=0, startcol=0)

        writer.close()


if __name__ == '__main__':
    file = SHEXJfjyFile('jfjy20230708.xml')
    file.to_excel()
