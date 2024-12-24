# -*- coding: utf-8 -*-

name = "sub-clash"

from .__config__ import *

config: sub_clashConfig = None
if enable_config:
    config = sub_clashConfig()

import sys
from QuickProject import (
    user_pip,
    _ask,
    external_exec,
    QproErrorString,
    QproDefaultStatus,
)


def requirePackage(
    pname: str,
    module: str = "",
    real_name: str = "",
    not_exit: bool = True,
    not_ask: bool = False,
    set_pip: str = user_pip,
):
    """
    获取本机上的python第三方库，如没有则询问安装

    :param not_ask: 不询问，无依赖项则报错
    :param set_pip: 设置pip路径
    :param pname: 库名
    :param module: 待引入的模块名，可缺省
    :param real_name: 用于 pip3 install 的名字
    :param not_exit: 安装后不退出
    :return: 库或模块的地址
    """
    local_scope = {}
    try:
        exec((f"from {pname} import {module}" if module else f"import {pname}"), globals(), local_scope)
    except (ModuleNotFoundError, ImportError):
        if not_ask:
            return None
        if _ask(
            {
                "type": "confirm",
                "message": f"""{name} require {pname + (' -> ' + module if module else '')}, confirm to install?
  {name} 依赖 {pname + (' -> ' + module if module else '')}, 是否确认安装?""",
                "default": True,
            }
        ):
            with QproDefaultStatus("Installing..." if user_lang != "zh" else "正在安装..."):
                external_exec(
                    f"{set_pip} install {pname if not real_name else real_name} -U",
                    True,
                )
            if not_exit:
                exec((f"from {pname} import {module}" if module else f"import {pname}"), globals(), local_scope)
            else:
                QproDefaultConsole.print(
                    QproInfoString,
                    f'just run again: "{" ".join(sys.argv)}"'
                    if user_lang != "zh"
                    else f'请重新运行: "{" ".join(sys.argv)}"',
                )
                exit(0)
        else:
            exit(-1)
    finally:
        return local_scope.get(module if module else pname)


def parse_host(content: str) -> dict:
    host = {}
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        if not line.strip():
            continue
        line = line.split()
        host[line[0]] = line[1]
    return host