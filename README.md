# Carmessys 汽车制造 MES 演示系统

## 项目简介

面向汽车制造场景的 MES 前端交互演示。项目使用 Vue 3、TypeScript 和 Vite 构建 Web 界面，并通过 Tauri 2 提供 Windows 桌面端封装。

## 主要内容

- 总控看板与生产 KPI
- 工单筛选、详情与下发
- 设备监控、报警确认和维护闭环
- SPC、缺陷分析与质量追溯
- 物料库存、补货任务和 AGV 调度
- PLC、SCADA、ERP、WMS、QMS 接入流程模拟
- 人员权限和操作审计日志

当前版本使用集中式模拟数据，不连接真实数据库或工业设备。界面操作会联动更新工单、设备、库存、质量和日志状态，适合演示 MES 信息流及人机交互设计。

## 环境依赖

需要 Node.js 20 或更高版本。

桌面端还需要 Rust、Cargo、WebView2 和带 Windows SDK 的 Visual Studio Build Tools。

## 使用方法

```powershell
npm install
npm run dev
```

浏览器访问 `http://127.0.0.1:1421`。Windows 用户也可双击 `start-carmessys.bat`，脚本会在缺少依赖时先安装依赖。

## 构建

Web 版本：

```powershell
npm run build
npm run preview
```

桌面开发与打包：

```powershell
npm run tauri dev
npm run tauri build
```

## 目录结构

```text
src/                 Vue 界面、样式和模拟数据
src-tauri/           Tauri 桌面端配置与 Rust 入口
_doc_assets/         功能结构图、演示截图和文档生成辅助脚本
package.json         前端依赖与运行命令
start-carmessys.bat  Windows 快速启动脚本
```

## 演示流程

1. 筛选待下发工单并执行下发。
2. 选择异常设备并确认报警。
3. 为低库存物料生成补货任务，再调度 AGV。
4. 在数据接入页面触发一轮模拟采集。
5. 回到总控看板和操作日志查看联动结果。

## 验证状态

整理副本已通过 TypeScript 检查和 Vite 生产构建。桌面端仍需在具备 Rust、Cargo、WebView2 和 Windows SDK 的环境中验证。

## 已知限制

当前版本使用模拟数据，不具备真实生产系统所需的数据库、身份认证、网络隔离、设备协议和故障恢复能力。

## 隐私与公开范围

仓库不包含生产凭据、真实设备地址或真实业务数据。接入模块仅演示 OPC UA、MQTT、REST API 和消息队列等典型工业集成概念。

## 许可证

当前未附加开源许可证。公开仓库可用于作品展示，但第三方复用权限需由仓库所有者另行确定。
