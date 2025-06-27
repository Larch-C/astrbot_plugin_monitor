
<div align="center">

![:name](https://count.getloli.com/@astrbot_plugin_monitor?name=astrbot_plugin_monitor&theme=minecraft&padding=6&offset=0&align=top&scale=1&pixelated=1&darkmode=auto)

# astrbot_plugin_monitor

_✨ [astrbot](https://github.com/AstrBotDevs/AstrBot) 视奸插件 ✨_  

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![AstrBot](https://img.shields.io/badge/AstrBot-3.4%2B-orange.svg)](https://github.com/Soulter/AstrBot)
[![GitHub](https://img.shields.io/badge/作者-Zhalslar-blue)](https://github.com/Zhalslar)

</div>

## 💡 介绍

~~视奸~~互通消息插件，通过bot查看其他群聊的聊天记录, 同时能通过bot向其他群聊发消息

## 📦 安装

- 可以直接在astrbot的插件市场搜索astrbot_plugin_monitor，点击安装即可  

- 或者可以直接克隆源码到插件文件夹：

```bash
# 克隆仓库到插件目录
cd /AstrBot/data/plugins
git clone https://github.com/Zhalslar/astrbot_plugin_monitor

# 控制台重启AstrBot
```

## ⚙️ 配置

请在astrbot面板配置，插件管理 -> astrbot_plugin_monitor -> 操作 -> 插件配置

## ⌨️ 使用说明

## ⌨️ 指令表

|     指令      |                   说明                    |
|:-------------:|:------------------------------------------:|
| 抽查 [群号] [数量] | 抽查目标群中最近若干条消息，并转发至当前群    |
| 监听 [群号]    | 开始监听指定的群聊，若已监听其他群则覆盖原有监听 |
| 取消监听       | 取消当前群对被监听群的监听关系              |
| 回复 [内容]    | 将内容转发到所监听的目标群中                |

注意：为了方便使用，每个指令都支持通过引用消息来获取群号

## 示例图

![download](https://github.com/user-attachments/assets/656ee439-a215-4aae-8ddd-96fad9067e6a)

## 🤝 TODO

- [x] 实现抽查群消息
- [x] 实现发送群消息
- [x] 可实时监听群消息
- [ ] 支持私聊消息
- [ ] 支持更多消息类型（图片、语音、视频...）

## 👥 贡献指南

- 🌟 Star 这个项目！（点右上角的星星，感谢支持！）
- 🐛 提交 Issue 报告问题
- 💡 提出新功能建议
- 🔧 提交 Pull Request 改进代码monitor

## 📌 注意事项

- 想第一时间得到反馈的可以来作者的插件反馈群（QQ群）：460973561（不点star不给进）
