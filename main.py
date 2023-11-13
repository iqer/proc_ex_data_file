import json
import os
from hashlib import md5

from const import RES_PATH, RUN_RECORD_FILE_PATH, EX_SH_MKT_RE, EX_SH_FJY_RE_EXP, EX_SH_JFJY_RE_EXP
from ex_sh_fjy_file import SHEXFjyFile
from ex_sh_jfjy_file import SHEXJfjyFile
from ex_sh_mkt_file import SHEXMKTFile
from log import logger


def proc_ex_data_file():
    need_run_file_names = _find_need_run_file_names()
    _proc_ex_data_file_impl(need_run_file_names)


def _proc_ex_data_file_impl(file_names):
    run_record = _get_run_record()
    for file_name in file_names:
        if EX_SH_MKT_RE.match(file_name):
            file = SHEXMKTFile(file_name)
            file.to_excel()

        elif EX_SH_FJY_RE_EXP.match(file_name):
            file = SHEXFjyFile(file_name)
            file.to_excel()
        elif EX_SH_JFJY_RE_EXP.match(file_name):
            file = SHEXJfjyFile(file_name)
            file.to_excel()

        digest = _get_file_digest(file_name)
        run_record[file_name] = digest

    _save_run_record(run_record)

def _find_need_run_file_names():
    file_names = os.listdir(RES_PATH)
    file_names = [file_name for file_name in file_names if file_name[-4:] in ['.txt', '.xml']]

    need_run_file_names = []

    for file_name in file_names:
        output_file_name = file_name.replace(file_name[-4:], '.xlsx')
        output_file_path = os.path.sep.join([RES_PATH, output_file_name])
        if not os.path.exists(output_file_path):
            need_run_file_names.append(file_name)
        else:
            need_to_run_flag = check_file_digest(file_name)
            if need_to_run_flag:
                need_run_file_names.append(file_name)

    return need_run_file_names


def check_file_digest(file_name):
    run_record = _get_run_record()
    record_digest = run_record.get(file_name)
    if not record_digest:
        return True
    return _check_file_digest_impl(file_name, record_digest)


def _check_file_digest_impl(file_name, record_digest):
    cur_file_path = os.path.sep.join([RES_PATH, file_name])
    with open(cur_file_path, 'rb') as f:
        cur_file_content = f.read()
        md = md5()
        md.update(cur_file_content)
        cur_digest = md.hexdigest()
        if cur_digest != record_digest:
            return True


def _get_file_digest(file_name):
    cur_file_path = os.path.sep.join([RES_PATH, file_name])
    with open(cur_file_path, 'rb') as f:
        cur_file_content = f.read()
        md = md5()
        md.update(cur_file_content)
        cur_digest = md.hexdigest()
        return cur_digest


def _get_run_record():
    if not os.path.exists(RUN_RECORD_FILE_PATH):
        return {}
    with open(RUN_RECORD_FILE_PATH, 'r') as f:
        run_record = json.load(f)
    return run_record


def _save_run_record(run_record):
    with open(RUN_RECORD_FILE_PATH, 'w') as f:
        json.dump(run_record, f)


if __name__ == '__main__':
    try:
        proc_ex_data_file()
    except Exception:
        import traceback
        logger.warning(traceback.format_exc())