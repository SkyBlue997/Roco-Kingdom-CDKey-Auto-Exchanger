# 洛克王国资格码自动兑换工具 (Roco Kingdom CDKey Auto-Exchanger)

这是一个用于自动尝试兑换洛克王国世界测试资格码的Python工具。它使用Selenium自动化测试框架，模拟人工操作来尝试不同的资格码组合，直到成功兑换或手动停止。

## 功能特点

- 🔄 **持续自动化兑换**: 按照指定规则生成并尝试兑换资格码，直到成功或手动停止
- 🧠 **智能延迟调整**: 根据网络繁忙情况自动调整操作间隔
- 👤 **模拟人工操作**: 随机化输入延迟与点击时机，降低被检测风险
- 🔍 **自动处理各类弹窗**: 包括网络繁忙、兑换失败等弹窗
- 📊 **详细统计报告**: 实时显示运行时间、尝试次数和成功次数
- 📝 **成功记录保存**: 自动将成功的兑换码保存到文件中

## 安装要求

- Python 3.6+
- Selenium 库
- Chrome 浏览器
- 与Chrome版本匹配的ChromeDriver

### 安装依赖

```bash
pip install selenium
```

## 使用方法

1. **下载ChromeDriver**

   确保下载与您Chrome浏览器版本匹配的ChromeDriver：
   https://googlechromelabs.github.io/chrome-for-testing/

2. **配置ChromeDriver路径**

   默认情况下，脚本会在以下位置查找ChromeDriver:
   - Mac: `~/Downloads/chromedriver-mac-arm64/chromedriver` 或 `~/下载/chromedriver-mac-arm64/chromedriver`
   - 如果找不到，脚本会提示输入正确路径

3. **运行脚本**

   ```bash
   python rocom.py
   ```

4. **手动登录**

   脚本启动后会打开洛克王国资格码兑换页面，需要手动完成登录操作，登录成功后脚本会自动开始尝试兑换。

5. **结束程序**

   按`Ctrl+C`可随时停止程序。

## 资格码生成规则

脚本按照以下规则生成18位资格码：

- 前4位: 固定为 "DJBm"
- 第5位: 数字 (0-9)
- 第6位: 大写字母 (A-Z)
- 第7-8位: 连续两位小写字母 (a-z)
- 第9位: 固定为数字 0
- 第10位: 小写字母 (a-z)
- 第11位: 大写字母 (A-Z)
- 第12位: 数字 (0-9)
- 第13位: 小写字母 (a-z)
- 第14位: 大写字母 (A-Z)
- 第15位: 数字 (0-9)
- 第16位: 大写字母 (A-Z)
- 第17位: 小写字母 (a-z)
- 第18位: 大写字母 (A-Z)

## 代码结构说明

- **generate_key()**: 按照规则生成18位资格码
- **wait_for_login_complete()**: 等待用户完成登录
- **is_exchange_successful()**: 检测兑换是否成功
- **is_network_busy()**: 检测是否出现网络繁忙提示
- **is_exchange_failed()**: 检测是否兑换失败
- **handle_common_modal()**: 处理各类弹窗
- **reset_page_if_needed()**: 检查并重置页面状态
- **main()**: 主程序逻辑

## 注意事项

- 本工具仅供学习和研究自动化测试技术使用
- 过于频繁的请求可能会导致IP被临时限制，请谨慎使用
- 成功兑换的资格码会保存在`successful_keys.txt`文件中
- 根据网络状况，可能需要手动调整初始延迟时间

## 许可证

MIT License

## 免责声明

本项目仅用于学习和研究网页自动化测试技术，请勿用于任何商业或非法用途。使用本工具所产生的任何后果由使用者自行承担。 