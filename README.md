# sub-clash

![demo](https://cos.rhythmlian.cn/ImgBed/02dbde94062c6ec8212f535be9588c42.png)

## Install

```shell
pip3 install git+https://github.com/Rhythmicc/sub-clash.git -U
```

## Usage

```shell
sub-clash
```

在使用前，需要编写一个如下的Python脚本，用于本地的订阅转换。
1. 更改`customize_rulus`字典来添加自己的解析规则；
2. 更改`rules`字典来更改规则的优先级；
3. 修改`get_area`函数中的`regions`字典来更改地区的判断规则，越靠前的规则优先级越高；

编写完成后，执行`sub-clash register <机场名>`，依据流程填写即可。

PS：如果你的机场不支持证书验证，请在157行后添加如下代码：

```python
    for i in proxies: # 为了解决某些节点证书问题，可以选择性添加此句
        i['skip-cert-verify'] = True
```

以下为脚本模板代码（依据奶昔家的配置，但没准其他机场也能用）：

```python
customize_rules = {
    "🇺🇸 美国": "https://raw.githubusercontent.com/Rhythmicc/ACL4SSR/master/Clash/us.list",
    "🚀 节点选择": "https://raw.githubusercontent.com/Rhythmicc/ACL4SSR/master/Clash/no-china.list",
}
rules_root = "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/"
rules = {
    "🎯 全球直连": "LocalAreaNetwork.list",
    "🎯 全球直连": "UnBan.list",
    "🎯 全球直连": "ChinaIp.list",
    "🎯 全球直连": "ChinaDomain.list",
    "🎯 全球直连": "ChinaIpV6.list",
    "🎯 全球直连": "ChinaCompanyIp.list",
    "🛑 全球拦截": "BanAD.list",
    "🍃 应用净化": "BanProgramAD.list",
    "📢 谷歌FCM": "Ruleset/GoogleFCM.list",
    "🎯 全球直连": "GoogleCN.list",
    "Ⓜ️ 微软服务": "Microsoft.list",
    "🍎 苹果服务": "Apple.list",
    "📲 电报信息": "Telegram.list",
    "🌍 国外媒体": "ProxyMedia.list",
    "🚀 节点选择": "ProxyGFWlist.list",
}

def get_area(name: str):
    import re
    
    regions = {
        r"(Hong Kong|HongKong|香港|🇭🇰)": "hk",
        r"(Japan|JP|日本|🇯🇵)": "jp",
        r"(Singapore|新加坡|🇸🇬)": "sg",
        r"(USA|United States|美国|🇺🇸)": "us",
        r"(Taiwan|TW|台湾|🇨🇳)": "tw",
        r"(United Kingdom|英国|🇬🇧)": "uk"
    }
    for k, v in regions.items():
        if re.search(k, name, re.IGNORECASE):
            return v
    return "other"

def config_checker(yaml):
    try:
        proxies = [i["name"] for i in yaml["proxies"]]
        if len(proxies) < 5:
            raise Exception("节点数量少于5个")
        proxy_groups = yaml["proxy-groups"]
        all_proxy_groups = [i['name'] for i in proxy_groups] + ['DIRECT', 'REJECT']
        for proxy_group in proxy_groups:
            for proxy in proxy_group["proxies"]:
                if proxy not in proxies and proxy not in all_proxy_groups:
                    raise Exception(f"节点 {proxy} 不存在")
    except Exception as e:
        raise Exception(f"配置文件错误: {e}")


def format_config(yaml):
    import re
    from QuickStart_Rhy.NetTools.MultiSingleDL import multi_single_dl_content_ls
    
    all_urls = [item[1] for item in customize_rules.items()] + [rules_root + item[1] for item in rules.items()]
    all_ruls = [item[0] for item in customize_rules.items()] + [item[0] for item in rules.items()]
    contents = [i.decode() for i in multi_single_dl_content_ls(all_urls)]

    priority_rules = []
    for _id, content in enumerate(contents):
        rule = all_ruls[_id]
        content = content.split('\n')
        for line in content:
            _line = line.strip()
            if not line or line.startswith("#") or line.startswith("USER-AGENT") or line.startswith("URL-REGEX"):
                continue
            if _line.endswith('no-resolve'):
                _line = _line.split(",")
                _line.insert(-1, rule)
                priority_rules.append(",".join(_line))
            else:
                priority_rules.append(f"{_line},{rule}")
    yaml["rules"] = priority_rules + [
        "GEOIP,CN,🎯 全球直连",
        "MATCH,🐟 漏网之鱼"
    ]
    remove_match = r"(Premium)"
    all_proxy_names = [i['name'] for i in yaml['proxies'] if not re.search(remove_match, i['name'])]
    yaml['proxy-groups'] = [
        {
            "name": "🚀 节点选择",
            "type": "select",
            "proxies": [
                "♻️ 自动选择",
                "🚀 手动切换"
            ]
        },
        {
            "name": "🚀 手动切换",
            "type": "select",
            "proxies": all_proxy_names.copy()
        },
        {
            "name": "♻️ 自动选择",
            "type": "url-test",
            "url": "http://www.gstatic.com/generate_204",
            "interval": 300,
            "tolerance": 50,
            "proxies": all_proxy_names.copy()
        },
        {
            "name": "🌍 国外媒体",
            "type": "select",
            "proxies": []
        },
        {
            "name": "📲 电报信息",
            "type": "select",
            "proxies": ["🚀 节点选择", "🎯 全球直连"] + all_proxy_names.copy()
        },
        {
            "name": "Ⓜ️ 微软服务",
            "type": "select",
            "proxies": ["🚀 节点选择", "🎯 全球直连"] + all_proxy_names.copy()
        },
        {
            "name": "🍎 苹果服务",
            "type": "select",
            "proxies": ["🚀 节点选择", "🎯 全球直连"] + all_proxy_names.copy()
        },
        {
            "name": "📢 谷歌FCM",
            "type": "select",
            "proxies": ["🚀 节点选择", "🎯 全球直连"] + all_proxy_names.copy()
        },
        {
            "name": "🎯 全球直连",
            "type": "select",
            "proxies": ["DIRECT", "🚀 节点选择", "♻️ 自动选择"]
        },
        {
            "name": "🛑 全球拦截",
            "type": "select",
            "proxies": ["DIRECT", "REJECT"]
        },
        {
            "name": "🍃 应用净化",
            "type": "select",
            "proxies": ["DIRECT", "REJECT"]
        },
        {
            "name": "🐟 漏网之鱼",
            "type": "select",
            "proxies": ["🚀 节点选择", "🎯 全球直连", "♻️ 自动选择"] + all_proxy_names.copy()
        },
    ]
    return all_proxy_names

def format_proxies(yaml: dict):
    config_checker(yaml)
    proxies = format_config(yaml)
    proxies = [i for i in yaml["proxies"] if i['name'] in proxies]
    yaml["proxies"] = proxies
    _structure = {
        "hk": {
            "name": "🇭🇰 香港",
            "proxies": []
        },
        "jp": {
            "name": "🇯🇵 日本",
            "proxies": []
        },
        "sg": {
            "name": "🇸🇬 狮城",
            "proxies": []
        },
        "tw": {
            "name": "🇨🇳 台湾",
            "proxies": []
        },
        "uk": {
            "name": "🇬🇧 英国",
            "proxies": []
        },
        "us": {
            "name": "🇺🇸 美国",
            "proxies": []
        },
        "other": {
            "name": "🌏 其他",
            "proxies": []
        }
    }
    for proxy in proxies:
        _structure[get_area(proxy['name'])]['proxies'].append(proxy['name'])
    _structure.pop('other')
    for area in _structure:
        name = _structure[area]['name']
        if _structure[area]['proxies']:
            yaml['proxy-groups'].append({
                "name": name,
                "type": "select",
                "proxies": [f"{name}最佳", f"{name}均衡"]
            })
    
    for area in _structure:
        name = _structure[area]['name']
        if _structure[area]['proxies']:
            yaml['proxy-groups'].append({
                "name": f"{name}最佳",
                "type": "url-test",
                "url": "http://www.gstatic.com/generate_204",
                "interval": 300,
                "tolerance": 50,
                "proxies": _structure[area]['proxies'].copy()
            })
    
    for area in _structure:
        name = _structure[area]['name']
        if _structure[area]['proxies']:
            yaml['proxy-groups'].append({
                "name": f"{name}均衡",
                "type": "load-balance",
                "proxies": _structure[area]['proxies'].copy(),
                "interval": 300,
                "url": "http://www.gstatic.com/generate_204",
                "strategy": "consistent-hashing"
            })
    
    yaml["proxy-groups"][0]["proxies"] = [
        "♻️ 自动选择",
        "🚀 手动切换",
    ]
    for area in _structure:
        if _structure[area]['proxies']:
            yaml["proxy-groups"][0]["proxies"].append(_structure[area]['name'])

    for item in yaml["proxy-groups"]:
        if item["name"] == "🌍 国外媒体":
            item["proxies"] = yaml["proxy-groups"][0]["proxies"].copy()
            item["proxies"].append("🎯 全球直连")
            item["proxies"].append("🚀 节点选择")

```
