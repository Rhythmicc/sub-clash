<h1 style="text-align: center"> sub-clash </h1>

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
      yaml["proxy-groups"][0]["proxies"].append("🇸🇬 狮城节点")
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
