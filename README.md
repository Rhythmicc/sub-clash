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

- 如需自定义规则，你需要编写一个python脚本，在其内部定义一个`format_proxies`函数。

  样例：

  ```python
  def format_proxies(yaml: dict):
      proxies = yaml['proxies']
      singapore = []
      for proxy in proxies:
          if 'Singapore' in proxy['name']:
              singapore.append(proxy)
      yaml['proxy-groups'].append({'name': '🇸🇬 狮城节点', 'proxies': singapore})
      yaml['rules'].append('DOMAIN-SUFFIX,jp,🇯🇵 日本节点')
      yaml['rules'].append('DOMAIN-SUFFIX,github.com,🇺🇲 美国节点')
  ```

