import re
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
RES_PATH = os.path.sep.join([PROJECT_PATH, 'res'])  # 资源文件夹路径
RUN_RECORD_FILE_PATH = os.path.sep.join([PROJECT_PATH, 'run_record.json'])  # 运行记录文件路径

EX_SH_MKT_RE_EXP = r'^mktdt00_\d{8}.txt$'  # 上交所行情文件名正则

EX_SH_FJY_RE_EXP = r'^fjy\d{8}.txt$'  # 上交所产品非交易基础信息文件名正则

EX_SH_JFJY_RE_EXP = r'^jfjy\d{8}.xml$'  # 上交所基金非交易基础信息文件名正则

EX_SH_MKT_RE = re.compile(EX_SH_MKT_RE_EXP)
EX_SH_FJY_RE_EXP = re.compile(EX_SH_FJY_RE_EXP)
EX_SH_JFJY_RE_EXP = re.compile(EX_SH_JFJY_RE_EXP)
