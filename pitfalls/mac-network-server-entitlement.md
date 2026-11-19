# Mac App 带了 network.server 权限，自动审核说「看不出对应功能」被退回

> 2026-11-19 实测 · 适用：开了 App Sandbox 的 macOS App

## 现象

Mac 版提交后收到自动消息，审核停下：

> An automated analysis of the submission indicates the app includes the com.apple.security.network.server entitlement but does not appear to have matching functionality.

同一次提交里，iPhone 版没有这一条（iOS 没有这个权限）。

## 原因

`com.apple.security.network.server` 是「监听端口、接受别人连进来」的权限。只往外连服务器的 App 只需要 `network.client`。苹果的自动分析看不出你在哪里监听，就先退回。

## 怎么改

**先判断是不是真的要。** 代码里有 `NWListener`、`bind`/`listen`、本机 HTTP 服务、本机 MCP 接口这类东西，才需要。

- **不需要**：从 entitlements 里删掉，重新打包上传，换新构建再提交
- **需要**（我们的情况：Mac 版只在本机回环地址（localhost）上开了一个接口，给同一台电脑上的 AI 工具读数据）：不用改包，做两件事
  1. 在「App 审核」那条消息下**回复**：用英文写清楚监听什么地址和端口、给谁用、外网能不能连进来、审核员怎么验证（给一条 curl 命令最直接）
  2. 版本页「App 审核信息 → 备注」里写同样的说明，**直接点名这个权限**，比如小标题写「LOCAL INTERFACE (needs com.apple.security.network.server)」。我们原来备注里写了本机接口的用途，但没点权限名，自动分析照样退回

审核备注上限 4000 字，写满了要先删别的。

## 一次做对

Mac 版第一次送审前查一遍 entitlements：每一个权限都要能说出「App 里哪个功能用它」，用不上的删掉，要用的在审核备注里点名写清楚。

## 相关

- [有自动续订订阅，商店描述里必须放 EULA 链接](subscription-needs-eula-link.md)
- [App Store 首次送审前必填项](../checklists/app-store-first-submission.md)
