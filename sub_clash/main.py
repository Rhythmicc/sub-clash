from QuickProject.Commander import Commander
from . import *

app = Commander()


@app.custom_complete("name")
def update():
    return [
        {"name": i, "icon": "✈️", "description": config.select(i)["show_name"]}
        for i in config.get_all()
    ]


@app.command()
def update(name: str):
    """
    更新Clash订阅

    :param name: 机场名
    """
    import yaml

    if not os.path.exists(".tmp.yaml"):
        requirePackage(
            "QuickStart_Rhy.NetTools.NormalDL", "normal_dl", real_name="QuickStart_Rhy"
        )(config.select(name)["url"], ".tmp.yaml")

    if config.select(name)["custom_format"]:
        with open(".tmp.yaml", "r") as f:
            clash_config = yaml.load(f, Loader=yaml.FullLoader)
        requirePackage(f".airports.{name}", "format_proxies")(clash_config)
        with open(".tmp.yaml", "w") as f:
            yaml.dump(clash_config, f, allow_unicode=True)
    requirePackage(
        "QuickStart_Rhy.API.TencentCloud", "TxCOS", real_name="QuickStart_Rhy"
    )().upload(".tmp.yaml", key=config.select(name)["key"])
    os.remove(".tmp.yaml")


@app.command()
def register(name: str):
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
        "key": _ask({"type": "input", "message": "输入腾讯云对应存储位置"}),
        "show_name": _ask({"type": "input", "message": "输入机场描述信息", "default": name}),
        "custom_format": _ask({"type": "input", "message": "输入自定义格式化文件路径（跳过则不配置）"}),
    }
    if values["custom_format"] and os.path.exists(values["custom_format"]):
        values["custom_format"] = os.path.abspath(values["custom_format"])
        import shutil

        shutil.copy(values["custom_format"], os.path.join(cur_path, name))
        values["custom_format"] = True
    elif values["custom_format"]:
        from QuickProject import QproErrorString

        return QproDefaultConsole.print(QproErrorString, "文件不存在")
    else:
        values["custom_format"] = False
    config.update(name, values)
    QproDefaultConsole.print(QproInfoString, "注册成功")


@app.command()
def unregister(name: str):
    from . import _ask

    cur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "airports")
    if config.select(name) and _ask(
        {"type": "confirm", "message": "是否删除此机场?", "default": False}
    ):
        requirePackage("QuickStart_Rhy", "remove")(os.path.join(cur_path, f"{name}.py"))
        config.update(name, None)
        QproDefaultConsole.print(QproInfoString, "删除成功")


@app.command()
def complete():
    """
    生成补全脚本，并应用fig至.fig/autocomplete/src/
    """
    from . import _ask

    if _ask(
        {"type": "confirm", "message": "此操作会创建complete文件夹, 是否继续?", "default": False}
    ):
        from QuickProject.Qpro import gen_complete

        gen_complete("sub-clash")

        import shutil

        shutil.copyfile(
            "complete/fig/sub-clash.fig",
            os.path.join(user_root, ".fig/autocomplete/src/sub-clash.ts"),
        )
        QproDefaultConsole.print(QproInfoString, "补全脚本生成并应用成功")


def main():
    """
    注册为全局命令时, 默认采用main函数作为命令入口, 请勿将此函数用作它途.
    When registering as a global command, default to main function as the command entry, do not use it as another way.
    """
    app()


if __name__ == "__main__":
    main()
