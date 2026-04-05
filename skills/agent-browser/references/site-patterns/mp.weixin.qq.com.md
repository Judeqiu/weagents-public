---
domain: mp.weixin.qq.com
aliases: ["微信公众号", "微信文章", "公众号"]
updated: 2026-03-22
---

## 平台特征
- 架构: 服务器端渲染，但内容有反爬保护
- 反爬: 需要微信环境或特殊 headers
- 内容加载: 文章主体是静态 HTML，但图片懒加载
- JS 验证: 部分页面有简单的 JS 挑战

## 有效模式
- 文章页: https://mp.weixin.qq.com/s/{base64_id}
- 文章页(长链接): https://mp.weixin.qq.com/s?__biz={biz}&mid={mid}&idx={idx}&sn={sn}
- 内容选择器: #js_content
- 标题选择器: #activity_name
- 作者选择器: #js_name

## 已知陷阱
- 链接有过期时间，临时链接会失效
- 图片使用 data-src 懒加载，需要滚动触发
- 部分文章需要验证才能查看完整内容
- 频繁抓取会触发封禁
- 文本内容可能被分段或使用特殊字符
