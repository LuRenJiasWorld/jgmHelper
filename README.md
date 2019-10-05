# jgmHelper
![<https://img.shields.io/badge/License-Apache2.0-green>](https://img.shields.io/badge/License-Apache2.0-green) ![<https://img.shields.io/badge/python-3.7-blue>](<https://img.shields.io/badge/python-3.7-blue>)  

> 腾讯游戏《家国梦》自动收集金币+运货辅助工具

Author: LuRenJiasWorld \<loli@lurenjia.in\>

Initial Release Date: 20191005

Last Update Date: 20191005

Current Version: v0.0.1

## 依赖：
- ADB驱动&命令行工具(Build版已内置)
- Pillow(用于截图的缩放)


## 技术细节
- 设备控制使用adb工具实现(Android Debugging Bridge)
- GUI使用Tkinter实现
- 暴力遍历用户打下的每个关键点，模拟点击与滑动

## 使用截图

![](https://github.com/LuRenJiasWorld/jgmHelper/raw/master/snapshots/1.jpg)

![](https://github.com/LuRenJiasWorld/jgmHelper/raw/master/snapshots/2.jpg)

## TODO

- [ ] 去掉对Pillow的依赖
- [ ] 优化遍历规则，提升效率
- [ ] 增加自动升级建筑物、自动抽卡功能
- [ ] 增加暂停功能，避免对正常手机使用造成困扰
- [ ] 支持存储用户的打点历史，避免重启软件后重新打点

## 贡献
项目作者不需要任何经济资助，但欢迎大家传播该软件，提交有建设性的[Issue](https://github.com/LuRenJiasWorld/jgmHelper/issues)与[Pull Request](https://github.com/LuRenJiasWorld/jgmHelper/pulls)，帮助这个项目变得更好，更完善。