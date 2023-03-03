# sub-clash

![demo](https://cos.rhythmlian.cn/ImgBed/5aabc7d793a9235387d78f4ad1107391.png)

## Install

```shell
pip3 install git+https://github.com/Rhythmicc/sub-clash.git -U
```

## Usage

```shell
sub-clash --help
```

- 推荐订阅转换：<https://nexconvert.com/> （选择多国家版）

- 如需自定义规则，你需要编写一个 python 脚本，在其内部定义一个`format_proxies`函数。

  样例：

```python
customize_rules = {
    "🇺🇲 美国": "https://raw.githubusercontent.com/Rhythmicc/ACL4SSR/master/Clash/us.list",
    "🚀 节点选择": "https://raw.githubusercontent.com/Rhythmicc/ACL4SSR/master/Clash/no-china.list",
}


def config_checker(yaml):
    try:
        proxies = [i["name"] for i in yaml["proxies"]]
        if len(proxies) < 5:
            raise Exception("节点数量少于5个")
        proxy_groups = yaml["proxy-groups"]
        for proxy_group in proxy_groups:
            for proxy in proxy_group["proxies"]:
                if proxy not in proxies and proxy not in [
                    "🇸🇬 狮城节点",
                    "🇺🇲 美国节点",
                    "🇭🇰 香港节点",
                    "🇯🇵 日本节点",
                    "🚀 节点选择",
                    "♻️ 自动选择",
                    "🎯 全球直连",
                    "🚀 手动切换",
                    "🌍 国外媒体",
                    "🍎 苹果服务",
                    "🎥 奈飞节点",
                    "📺 爱奇艺",
                    "📺 腾讯视频",
                    "📺 哔哩哔哩",
                    "📺 优酷",
                    "📺 芒果TV",
                    "DIRECT",
                    "REJECT",
                ]:
                    raise Exception(f"节点 {proxy} 不存在")
    except Exception as e:
        raise Exception(f"配置文件错误: {e}")


def add_rules(yaml):
    import requests

    priority_rules = []
    for rules in customize_rules:
        url = customize_rules[rules]
        content = requests.get(url).text.strip().splitlines()
        for line in content:
            _line = line.strip()
            if not line or line.startswith("#"):
                continue
            priority_rules.append(f"{_line},{rules}")
    yaml["rules"] = priority_rules + yaml["rules"]


def format_proxies(yaml: dict):
    config_checker(yaml)
    proxies = yaml["proxies"]
    remove_nodes = []
    singapore = []
    for proxy in proxies:
        if "Premium" in proxy["name"]:
            remove_nodes.append(proxy)
            continue
        if "Singapore" in proxy["name"]:
            singapore.append(proxy["name"])
    for proxy in remove_nodes:
        # proxies.remove(proxy)
        for proxy_group in yaml["proxy-groups"]:
            if proxy["name"] in proxy_group["proxies"]:
                proxy_group["proxies"].remove(proxy["name"])
    yaml["proxies"] = [i for i in proxies if i["name"] not in remove_nodes]
    america, hongkong, japan = None, None, None
    for _id, item in enumerate(yaml["proxy-groups"]):
        if item["name"] == "🇺🇲 美国节点":
            america = [i for i in item["proxies"]]
        elif item["name"] == "🇭🇰 香港节点":
            hongkong = [i for i in item["proxies"]]
        elif item["name"] == "🇯🇵 日本节点":
            japan = [i for i in item["proxies"]]
    # remove old proxies
    for delele_item in ["🇺🇲 美国节点", "🇭🇰 香港节点", "🇯🇵 日本节点"]:
        for _id, item in enumerate(yaml["proxy-groups"]):
            if item["name"] == delele_item:
                yaml["proxy-groups"].pop(_id)
                break
    yaml["proxy-groups"].append(
        {
            "name": "🇭🇰 香港",
            "type": "select",
            "proxies": ["🇭🇰 香港最佳", "🇭🇰 香港均衡"],
        }
    )
    yaml["proxy-groups"].append(
        {
            "name": "🇯🇵 日本",
            "type": "select",
            "proxies": ["🇯🇵 日本最佳", "🇯🇵 日本均衡"],
        }
    )
    yaml["proxy-groups"].append(
        {
            "name": "🇺🇲 美国",
            "type": "select",
            "proxies": ["🇺🇲 美国最佳", "🇺🇲 美国均衡"],
        }
    )
    yaml["proxy-groups"].append(
        {
            "name": "🇸🇬 狮城",
            "type": "select",
            "proxies": ["🇸🇬 狮城最佳", "🇸🇬 狮城均衡"],
        }
    )
    yaml["proxy-groups"].append(
        {
            "interval": 300,
            "name": "🇸🇬 狮城最佳",
            "proxies": [i for i in singapore],
            "type": "url-test",
            "url": "http://www.gstatic.com/generate_204",
        },
    )
    yaml["proxy-groups"].append(
        {
            "interval": 300,
            "name": "🇺🇲 美国最佳",
            "proxies": [i for i in america],
            "type": "url-test",
            "url": "http://www.gstatic.com/generate_204",
        },
    )
    yaml["proxy-groups"].append(
        {
            "interval": 300,
            "name": "🇭🇰 香港最佳",
            "proxies": [i for i in hongkong],
            "type": "url-test",
            "url": "http://www.gstatic.com/generate_204",
        },
    )
    yaml["proxy-groups"].append(
        {
            "interval": 300,
            "name": "🇯🇵 日本最佳",
            "proxies": [i for i in japan],
            "type": "url-test",
            "url": "http://www.gstatic.com/generate_204",
        },
    )
    # load-balance
    yaml["proxy-groups"].append(
        {
            "name": "🇸🇬 狮城均衡",
            "proxies": [i for i in singapore],
            "type": "load-balance",
            "strategy": "consistent-hashing",
            "interval": 300,
            "url": "http://www.gstatic.com/generate_204",
        },
    )
    yaml["proxy-groups"].append(
        {
            "name": "🇺🇲 美国均衡",
            "proxies": [i for i in america],
            "type": "load-balance",
            "strategy": "consistent-hashing",
            "interval": 300,
            "url": "http://www.gstatic.com/generate_204",
        },
    )
    yaml["proxy-groups"].append(
        {
            "name": "🇭🇰 香港均衡",
            "proxies": [i for i in hongkong],
            "type": "load-balance",
            "strategy": "consistent-hashing",
            "interval": 300,
            "url": "http://www.gstatic.com/generate_204",
        },
    )
    yaml["proxy-groups"].append(
        {
            "name": "🇯🇵 日本均衡",
            "proxies": [i for i in japan],
            "type": "load-balance",
            "strategy": "consistent-hashing",
            "interval": 300,
            "url": "http://www.gstatic.com/generate_204",
        },
    )
    yaml["proxy-groups"][0]["proxies"] = [
        "♻️ 自动选择",
        "🚀 手动切换",
        "🇭🇰 香港",
        "🇸🇬 狮城",
        "🇺🇲 美国",
        "🇯🇵 日本",
    ]
    if customize_rules:
        add_rules(yaml)

    for item in yaml["proxy-groups"]:
        if item["name"] == "🌍 国外媒体":
            item["proxies"] = [
                "🇸🇬 狮城",
                "🇺🇲 美国",
                "🇭🇰 香港",
                "🇯🇵 日本",
                "🚀 节点选择",
                "♻️ 自动选择",
                "🎯 全球直连",
                "🚀 手动切换",
            ]

```
