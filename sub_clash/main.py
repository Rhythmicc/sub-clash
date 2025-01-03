from QuickProject.Commander import Commander
from . import *

app = Commander(name)


@app.custom_complete("name")
def update():
    return [
        {"name": i, "icon": "✈️", "description": config.select(i)["show_name"]}
        for i in config.get_all()
    ]

@app.custom_complete("name")
def justify():
    return [
        {"name": i, "icon": "✈️", "description": config.select(i)["show_name"]}
        for i in config.get_all()
    ]

@app.custom_complete("name")
def unregister():
    return [
        {"name": i, "icon": "✈️", "description": config.select(i)["show_name"]}
        for i in config.get_all()
    ]


@app.command()
def update(name: str, force: bool = False, no_delete: bool = False, disable_txcos: bool = False):
    """
    更新Clash订阅

    :param name: 机场名
    :param force: 强制更新
    :param no_delete: 不删除临时文件
    :param disable_txcos: 禁用腾讯云COS
    """
    yaml = requirePackage("yaml", real_name="PyYAML")

    if os.path.exists(".tmp.yaml") and force:
        os.remove(".tmp.yaml")
    if not (_info := config.select(name)):
        from QuickProject import QproErrorString

        return QproDefaultConsole.print(QproErrorString, "机场不存在")

    url = _info['url']
    res = requirePackage(
        "QuickStart_Rhy.NetTools.NormalDL", "normal_dl", real_name="QuickStart_Rhy"
    )(url, ".tmp.yaml", ignore_404=True)

    if not res and not os.path.exists(".tmp.yaml"):
        from QuickProject import QproErrorString

        return QproDefaultConsole.print(QproErrorString, "下载失败")

    with open(".tmp.yaml", "r", encoding='utf-8') as f:
        content = f.read()
    with open(".tmp.yaml", "w", encoding='utf-8') as f:
        f.write(content.replace("!<str> ", ""))

    if _info["custom_format"]:
        with open(".tmp.yaml", "r", encoding='utf-8') as f:
            clash_config = yaml.load(f, Loader=yaml.FullLoader)
        QproDefaultConsole.print(f".airports.{name}")
        requirePackage(f".airports.{name}", "format_proxies")(clash_config)
        # 注入 hosts
        clash_config['host'] = parse_host(
            requirePackage(
                "QuickStart_Rhy.NetTools.NormalDL",
                "normal_dl",
                real_name="QuickStart_Rhy",
            )(
                "https://raw.githubusercontent.com/maxiaof/github-hosts/refs/heads/master/hosts",
                write_to_memory=True,
            ).decode('utf-8')
        )
        with open(".tmp.yaml", "w", encoding='utf-8') as f:
            yaml.dump(
                clash_config,
                f,
                allow_unicode=True,
                indent=4,
                default_flow_style=False,
                sort_keys=False,
            )
    if not disable_txcos and _info["key"]:
        with QproDefaultStatus("Uploading..." if user_lang != "zh" else "正在上传..."):
            requirePackage(
                "QuickStart_Rhy.API.TencentCloud", "TxCOS", real_name="QuickStart_Rhy"
            )().upload(".tmp.yaml", key=_info["key"])
            QproDefaultConsole.print(
                QproInfoString, "更新成功，已上传至腾讯云COS:", config.select(name)["key"]
            )
            if no_delete:
                return
            os.remove(".tmp.yaml")
    else:
        os.rename('.tmp.yaml', f'{name}.yaml')
        QproDefaultConsole.print(
            QproInfoString, "更新成功，已保存至", f'{name}.yaml'
        )


@app.command()
def register(name: str):
    """
    添加机场

    :param name: 机场名
    """
    from . import _ask

    cur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "airports")
    if not os.path.exists(cur_path):
        os.mkdir(cur_path)
    airports = os.listdir(cur_path)

    if (name in airports or config.select(name)) and _ask(
        {"type": "confirm", "message": "此机场已注册, 是否覆盖?", "default": False}
    ):
        remove = requirePackage("QuickStart_Rhy", "remove")
        remove(os.path.join(airports, f"{name}.py"))
        config.update(name, None)

    values = {
        "url": _ask({"type": "input", "message": "输入机场订阅链接"}),
        "key": _ask({"type": "input", "message": "输入腾讯云对应存储位置（没有则留空）"}),
        "show_name": _ask({"type": "input", "message": "输入机场描述信息", "default": name}),
        "custom_format": _ask({"type": "input", "message": "输入自定义格式化文件路径"}),
    }
    if values["custom_format"]:
        if not os.path.exists(values["custom_format"]):
            from QuickProject import QproErrorString

            return QproDefaultConsole.print(QproErrorString, "脚本文件不存在")
        values["custom_format"] = os.path.abspath(values["custom_format"])
        import shutil

        shutil.copy(values["custom_format"], os.path.join(cur_path, f"{name}.py"))
        values["custom_format"] = True
    elif values["custom_format"]:
        from QuickProject import QproErrorString

        return QproDefaultConsole.print(QproErrorString, "文件不存在")
    else:
        values["custom_format"] = False
    config.update(name, values)
    QproDefaultConsole.print(QproInfoString, "注册成功")


@app.command()
def justify(
    name: str,
    url: bool = False,
    key: bool = False,
    show_name: bool = False,
    custom_format: bool = False,
):
    """
    修改机场配置

    :param name: 机场名
    :param url: 修改订阅链接
    :param key: 修改腾讯云存储位置
    :param show_name: 修改机场描述信息
    :param custom_format: 修改自定义格式化文件路径
    """
    from . import _ask

    if not (item := config.select(name)):
        from QuickProject import QproErrorString

        return QproDefaultConsole.print(QproErrorString, "机场不存在")
    if url:
        item["url"] = _ask(
            {"type": "input", "message": "输入机场订阅链接", "default": item["url"]}
        )
    if key:
        item["key"] = _ask(
            {"type": "input", "message": "输入腾讯云对应存储位置", "default": item["key"]}
        )
    if show_name:
        item["show_name"] = _ask(
            {"type": "input", "message": "输入机场描述信息", "default": item["show_name"]}
        )
    if custom_format:
        item["custom_format"] = _ask(
            {
                "type": "input",
                "message": "输入自定义格式化文件路径（跳过则不配置）",
                "default": item["custom_format"],
            }
        )
        import shutil

        cur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "airports")
        shutil.copy(item["custom_format"], os.path.join(cur_path, f"{name}.py"))
        item["custom_format"] = True
    config.update(name, item)


@app.command()
def unregister(name: str):
    """
    删除机场

    :param name: 机场名
    """
    from . import _ask

    cur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "airports")
    if config.select(name) and _ask(
        {"type": "confirm", "message": "是否删除此机场?", "default": False}
    ):
        requirePackage("QuickStart_Rhy", "remove")(os.path.join(cur_path, f"{name}.py"))
        config.update(name, None)
        QproDefaultConsole.print(QproInfoString, "删除成功")


def main():
    """
    注册为全局命令时, 默认采用main函数作为命令入口, 请勿将此函数用作它途.
    When registering as a global command, default to main function as the command entry, do not use it as another way.
    """
    app()


if __name__ == "__main__":
    main()
