---
domain: zhihu.com
aliases: ["知乎", "知乎回答", "知乎专栏"]
updated: 2026-03-22
---

## 平台特征
- 架构: 混合渲染，首屏 SSR，后续 CSR
- 反爬: 中等，未登录限制浏览量
- 内容加载: 回答内容需要滚动加载更多
- 登录要求: 未登录只能浏览少量内容

## 有效模式
- 问题页: https://www.zhihu.com/question/{question_id}
- 回答页: https://www.zhihu.com/question/{qid}/answer/{aid}
- 专栏文章: https://zhuanlan.zhihu.com/p/{article_id}
- 内容选择器: .RichContent-inner
- 回答列表: .List-item

## 已知陷阱
- 未登录用户只能查看前几个回答 (2026-03)
- 回答内容可能折叠，需要点击"展开"
- 视频内容使用独立播放器
- 评论需要单独加载
- 图片有水印
