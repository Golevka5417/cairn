# 有自动续订订阅，商店描述里必须放「使用条款（EULA）」链接，否则送审直接退回

> 2026-11-19 实测 · 适用：带自动续期订阅的 iOS / macOS App

## 现象

提交后几个小时，收到一封自动消息（不是人工审核），审核直接停下：

> The submission offers auto-renewable subscriptions … but does not include a functional link to the Terms of Use (EULA) in the app metadata that appears on the app's App Store product page.

App 里的会员页其实已经有「用户协议」「隐私政策」两个链接、价格、周期和自动续订说明，照样被退。苹果查的是**商店页的元数据**，不是 App 里面。

## 原因

自动续订订阅要求商店页上能点开使用条款。苹果给两种做法：

1. 用苹果标准 EULA：在**每一个语言**的 App 描述里放链接 `https://www.apple.com/legal/internet-services/itunes/dev/stdeula/`
2. 用自己的 EULA：在 App Store Connect →「App 信息」→「许可协议」里填进去

隐私政策网址填在「App 隐私」里，不算这一条。

## 怎么改（不用重新打包）

1. 版本页 → 每个语言的「描述」末尾加：

   ```
   使用条款（EULA）：https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
   用户协议：<你自己的用户协议页>
   隐私政策：<你自己的隐私政策页>
   ```

2. iPhone 和 Mac 是同一条记录的，**两个平台的版本页各改一次**，描述是分开存的
3. 保存 → 「更新审核」重新提交。订阅、订阅群组还在原来那份提交里，不用重新添加

## 一次做对

送审前对一遍：描述里有 EULA 链接；App 内付费页有价格、周期、自动续订说明、「恢复购买」、使用条款和隐私政策链接；用户协议里写清续订和取消规则。

## 相关

- [App Store 首次送审前必填项](../checklists/app-store-first-submission.md)
- [Mac App 带了 network.server 权限被自动退回](mac-network-server-entitlement.md)（同一天、同一次提交的另一封自动消息）
