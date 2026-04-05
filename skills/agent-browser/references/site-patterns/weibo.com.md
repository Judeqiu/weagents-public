---
domain: weibo.com
aliases: ["微博", "新浪微博", "weibo"]
updated: 2026-03-22
---

## 平台特征
- 架构: 服务器端渲染 + 动态加载
- 反爬: 严格，需要登录
- 内容加载: 时间线滚动加载
- 登录要求: 必须登录才能查看完整内容

## 有效模式
- 单条微博: https://weibo.com/{uid}/{mid}
- 用户主页: https://weibo.com/u/{uid}
- 内容选择器: .WB_text
- 图片选择器: .media_box img

## 已知陷阱
- 必须登录才能访问大部分内容
- 内容有过期时间
- 图片使用缩略图，需要替换 URL 获取原图
- 频繁访问会触发验证码
- 移动端 m.weibo.cn 限制较少，可作为备选
