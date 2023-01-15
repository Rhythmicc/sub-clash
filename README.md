<h1 style="text-align: center"> sub-clash </h1>

![demo](https://cos.rhythmlian.cn/ImgBed/5aabc7d793a9235387d78f4ad1107391.png)

## Install

```shell
pip3 install git+https://github.com/Rhythmicc/sub-clash.git -U
```

## Usage

```shell
sub-clash --help
```

- 推荐订阅转换：https://nexconvert.com/ （选择多国家版）

- 如需自定义规则，你需要编写一个 python 脚本，在其内部定义一个`format_proxies`函数。

  样例：

  ```python
    def config_checker(yaml):
        try:
            proxies = [i["name"] for i in yaml["proxies"]]
            proxy_groups = yaml["proxy-groups"]
            for proxy_group in proxy_groups:
                for proxy in proxy_group["proxies"]:
                    if proxy not in proxies:
                        raise Exception(f"节点 {proxy} 不存在")
        except Exception as e:
            raise Exception(f"配置文件错误: {e}")

    def format_proxies(yaml: dict):
        proxies = yaml["proxies"]
        singapore = []
        for proxy in proxies:
            if "Singapore" in proxy["name"]:
                singapore.append(proxy["name"])
        yaml["proxy-groups"].append(
            {
                "interval": 300,
                "name": "🇸🇬 狮城节点",
                "proxies": singapore,
                "type": "url-test",
                "url": "http://www.gstatic.com/generate_204",
            }
        )
        yaml["proxy-groups"][0]["proxies"].insert(-2, "🇸🇬 狮城节点")
        for item in yaml["proxy-groups"]:
            if item["name"] != "🌍 国外媒体":
                continue
            item["proxies"] = [
                "🇸🇬 狮城节点",
                "🇺🇲 美国节点",
                "🇭🇰 香港节点",
                "🇯🇵 日本节点",
                "🚀 节点选择",
                "♻️ 自动选择",
                "🎯 全球直连",
                "🚀 手动切换",
            ]
            break
        yaml["rules"].append("DOMAIN-SUFFIX,jp,🇯🇵 日本节点")
        yaml["rules"].append("DOMAIN-SUFFIX,github.com,🇺🇲 美国节点")
  ```
