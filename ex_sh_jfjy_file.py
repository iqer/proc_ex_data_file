import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString


def main():
    content = open('./上交所数据文件/jfjy20230708.xml', encoding='gbk').read()
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
    valid_data_lines(element_list)


def valid_data_lines(data_lines):
    # ETF实物/黄金申赎
    etf_goods_gold_list = []
    # ETF现金申赎
    etf_cash_list = []
    for line in data_lines:
        inst_id = line['Inst_ID']
        assert len(inst_id) == 6
        inst_name = line['Inst_Nam']
        assert len(inst_name.encode('gbk')) == 8
        busi_typ = line['Busi_Typ']
        assert busi_typ in ['IEC', 'IER', 'GEC', 'GER', 'EEC', 'EER']

        if busi_typ in ['IEC', 'IER', 'GEC', 'GER']:
            item = [inst_id, inst_name, busi_typ]
            etf_goods_gold_list.append(item)
        elif busi_typ in ['EEC', 'EER']:
            crea_rtgs_tag = line['Crea_Rtgs_Tag']
            if busi_typ == 'EEC':
                assert crea_rtgs_tag in ['0', '1']
            else:
                assert len(crea_rtgs_tag) == 1

# with open('./上交所数据文件/utf-8-jfjy20230708.xml', encoding='utf-8', mode='w') as f:
#     f.write(content)
# xmlp = ET.XMLParser(encoding="gbk")
# tree = ET.parse('./上交所数据文件/jfjy20230708.xml',parser=xmlp)
# tree = ET.parse('./上交所数据文件/jfjy20230708.xml', parser=ET.XMLParser(encoding='iso-8859-5'))
# tree = ET.parse('')   # 解析 XML 文件
# root = tree.getroot()

#
# # 遍历根元素下的子元素
# for child in root:
#     print(child.items())
#     print(child.tag, child.attrib)

FILE_NAME = 'jfjy20230708.xlsx'


if __name__ == '__main__':
    main()
