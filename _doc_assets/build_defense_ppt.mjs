import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const pptxgen = require("pptxgenjs");

const ROOT = path.resolve(".");
const ASSETS = path.join(ROOT, "_doc_assets");
const SHOTS = path.join(ASSETS, "screenshots");
const OUT_PPT = path.join(ROOT, "Carmessys汽车制造MES系统答辩PPT.pptx");
const OUT_TXT = path.join(ROOT, "Carmessys汽车制造MES系统答辩演讲稿.txt");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Carmessys Team";
pptx.company = "智能制造人机交互课程大作业";
pptx.subject = "汽车制造 MES 系统答辩";
pptx.title = "Carmessys 汽车制造 MES 系统答辩";
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "Microsoft YaHei",
  bodyFontFace: "Microsoft YaHei",
  lang: "zh-CN",
};
pptx.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pptx.layout = "WIDE";

const C = {
  bg: "F8FBFA",
  ink: "264653",
  muted: "6C7A80",
  accent: "66BFB0",
  accent2: "F2D492",
  pale: "EAF6F3",
  pale2: "FFF7E1",
  line: "CFE5DF",
  white: "FFFFFF",
  red: "D66A6A",
};

const slides = [];

function addSlide(kicker, title) {
  const slide = pptx.addSlide();
  slide.background = { color: C.bg };
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: C.bg }, line: { color: C.bg } });
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 0.12, h: 7.5, fill: { color: C.accent }, line: { color: C.accent } });
  if (kicker) {
    slide.addText(kicker, { x: 0.55, y: 0.35, w: 2.4, h: 0.25, fontFace: "Microsoft YaHei", fontSize: 8.5, bold: true, color: C.accent, charSpace: 1.1, margin: 0 });
  }
  if (title) {
    slide.addText(title, { x: 0.55, y: 0.68, w: 9.8, h: 0.55, fontFace: "Microsoft YaHei", fontSize: 25, bold: true, color: C.ink, margin: 0, breakLine: false, fit: "shrink" });
  }
  slide.addText(String(pptx._slides.length).padStart(2, "0"), { x: 12.35, y: 6.95, w: 0.42, h: 0.18, fontSize: 8, color: "9AA7AA", margin: 0, align: "right" });
  return slide;
}

function addPill(slide, text, x, y, w, color = C.pale) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h: 0.38, rectRadius: 0.08, fill: { color }, line: { color } });
  slide.addText(text, { x: x + 0.12, y: y + 0.09, w: w - 0.24, h: 0.16, fontSize: 8.8, color: C.ink, bold: true, margin: 0, align: "center", fit: "shrink" });
}

function addCard(slide, title, body, x, y, w, h, fill = C.white) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: fill, transparency: 0 }, line: { color: C.line, transparency: 0 } });
  slide.addText(title, { x: x + 0.18, y: y + 0.18, w: w - 0.36, h: 0.25, fontSize: 13, bold: true, color: C.ink, margin: 0, fit: "shrink" });
  slide.addText(body, { x: x + 0.18, y: y + 0.58, w: w - 0.36, h: h - 0.76, fontSize: 9.5, color: C.muted, margin: 0.02, breakLine: false, fit: "shrink", valign: "top" });
}

function addImage(slide, file, x, y, w, h) {
  slide.addShape(pptx.ShapeType.roundRect, { x: x - 0.04, y: y - 0.04, w: w + 0.08, h: h + 0.08, rectRadius: 0.08, fill: { color: C.white }, line: { color: C.line } });
  slide.addImage({ path: file, x, y, w, h });
}

function note(num, title, text) {
  slides.push({ num, title, text });
}

// 1 Cover
{
  const s = pptx.addSlide();
  s.background = { color: C.bg };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: C.bg }, line: { color: C.bg } });
  s.addShape(pptx.ShapeType.arc, { x: 9.2, y: -0.45, w: 4.8, h: 4.8, line: { color: C.pale, transparency: 20, width: 2 }, adjustPoint: 0.35 });
  addPill(s, "智能制造人机交互 · 课程大作业答辩", 0.8, 0.72, 3.1);
  s.addText("Carmessys", { x: 0.78, y: 1.52, w: 5.2, h: 0.65, fontSize: 39, bold: true, color: C.ink, margin: 0 });
  s.addText("汽车制造 MES 系统\n人机交互界面设计", { x: 0.82, y: 2.28, w: 5.8, h: 1.2, fontSize: 25, bold: true, color: C.ink, margin: 0, breakLine: false, fit: "shrink" });
  s.addText("围绕汽车制造流程，构建生产、设备、质量、物料、数据接入与安全审计的一体化 MES 仿真系统。", { x: 0.84, y: 3.72, w: 5.35, h: 0.62, fontSize: 13.2, color: C.muted, margin: 0.02, fit: "shrink" });
  addImage(s, path.join(SHOTS, "01-dashboard.png"), 6.45, 1.15, 5.85, 3.75);
  s.addText("小组成员：__________  __________  __________  __________\n课程教师：陈成明    日期：2026 年 05 月", { x: 0.85, y: 6.48, w: 6.3, h: 0.42, fontSize: 10, color: C.muted, margin: 0 });
  note(1, "封面", "各位老师好，我们小组汇报的题目是 Carmessys 汽车制造 MES 系统人机交互界面设计。本项目围绕汽车制造现场的生产执行、设备监控、质量追溯、物料物流和数据接入，完成了一个可运行的 MES 仿真系统。");
}

// 2 Design logic
{
  const s = addSlide("DESIGN LOGIC", "整体思路：从制造场景到交互闭环");
  const items = [
    ["场景先行", "统一为汽车制造 MES，避免 PCB 名称与汽车主题冲突"],
    ["角色驱动", "生产管理员、维护员、质量工程师、仓储调度员分别有不同任务"],
    ["信息分层", "总控看板看态势，子模块定位问题，详情页完成处置"],
    ["交互闭环", "下发、确认、补货、采集等动作都会反馈并写入日志"],
  ];
  items.forEach((it, i) => addCard(s, it[0], it[1], 0.85 + i * 3.05, 2.0, 2.55, 2.05, i % 2 ? C.pale2 : C.pale));
  s.addText("核心判断：MES 不是静态看板，而是连接人、机、物、质量和数据流的现场执行系统。", { x: 1.0, y: 5.15, w: 10.8, h: 0.42, fontSize: 17, bold: true, color: C.ink, margin: 0, align: "center" });
  note(2, "整体思路", "我们的设计逻辑分为四步：第一是场景先行，把系统统一为汽车制造 MES；第二是角色驱动，不同岗位的信息需求不同；第三是信息分层，从总控到模块再到详情；第四是交互闭环，每个关键动作都要有反馈和日志。");
}

// 3 Scenario needs
{
  const s = addSlide("SCENARIO", "汽车制造现场需要一张统一的执行视图");
  addCard(s, "生产管理员", "关注今日产量、OEE、订单完成率、报警数量和生产节拍。", 0.82, 1.65, 2.85, 1.28);
  addCard(s, "设备维护员", "关注设备状态、温度振动、停机统计和报警处置。", 3.9, 1.65, 2.85, 1.28);
  addCard(s, "质量工程师", "关注 SPC、DPPM、不良率、缺陷分类和批次追溯。", 6.98, 1.65, 2.85, 1.28);
  addCard(s, "仓储调度员", "关注库存安全线、补货任务、AGV 状态和物流路径。", 10.06, 1.65, 2.85, 1.28);
  s.addShape(pptx.ShapeType.line, { x: 1.1, y: 4.1, w: 10.95, h: 0, line: { color: C.line, width: 2 } });
  ["ERP 订单", "PLC/SCADA", "WMS 库存", "QMS 检验", "MES 执行"].forEach((t, i) => addPill(s, t, 1.05 + i * 2.18, 4.55, 1.45, i === 4 ? C.accent2 : C.pale));
  s.addText("设计目标：让关键状态能被快速看见，让异常能被快速定位，让操作能被追溯。", { x: 1.05, y: 5.85, w: 10.7, h: 0.36, fontSize: 17, bold: true, color: C.ink, align: "center", margin: 0 });
  note(3, "场景与需求", "汽车制造现场的数据来源很多，角色也很多。生产管理员看全局，维护员看设备，质量工程师看质量，仓储调度员看库存和物流。所以我们希望用一张统一的执行视图，把 ERP、设备层、WMS、QMS 和 MES 执行过程连接起来。");
}

// 4 Architecture
{
  const s = addSlide("ARCHITECTURE", "页面结构采用“总览 - 执行 - 集成 - 审计”四层");
  addImage(s, path.join(ASSETS, "page_structure.png"), 0.88, 1.55, 11.55, 5.05);
  note(4, "页面结构", "这是系统页面结构图。最上层是总控看板，用于快速判断生产现场是否正常；中间是工单、设备、质量、物料和 AGV 等执行模块；右侧是数据采集接入，模拟后端系统进入 MES；底部是权限和日志，用于安全审计。");
}

// 5 Function flow
{
  const s = addSlide("DATA FLOW", "功能结构体现 MES 的信息流与业务闭环");
  addImage(s, path.join(ASSETS, "function_data_flow.png"), 0.88, 1.55, 11.55, 5.05);
  note(5, "功能与数据流", "这张图说明系统的数据流。ERP 提供订单计划，PLC 和 SCADA 提供设备数据，WMS 和 QMS 提供库存与质量数据。数据进入 MES 后，映射为工单、设备、质量、物料等业务对象，再反馈给不同角色，并写入日志形成追溯。");
}

// 6 Dashboard + orders
{
  const s = addSlide("PRODUCTION", "总控看板负责态势感知，工单模块负责执行推进");
  addImage(s, path.join(SHOTS, "01-dashboard.png"), 0.75, 1.45, 5.75, 3.68);
  addImage(s, path.join(SHOTS, "02-orders.png"), 6.83, 1.45, 5.75, 3.68);
  addPill(s, "KPI 置顶：产量 / OEE / 完成率 / 能耗 / 报警", 1.05, 5.75, 4.4);
  addPill(s, "工单闭环：筛选 -> 查看 -> 下发 -> 进度反馈", 7.1, 5.75, 4.15, C.pale2);
  note(6, "总控与工单", "总控看板解决的是态势感知问题，所以把产量、OEE、完成率、能耗和报警放在首屏。工单模块解决的是执行推进问题，支持按状态筛选、查看进度，并进入详情页完成下发。");
}

// 7 Equipment + quality
{
  const s = addSlide("CONTROL", "设备与质量模块把异常前置，减少视觉搜索成本");
  addImage(s, path.join(SHOTS, "03-equipment-detail.png"), 0.75, 1.45, 5.75, 3.68);
  addImage(s, path.join(SHOTS, "04-spc.png"), 6.83, 1.45, 5.75, 3.68);
  addPill(s, "设备：温度、振动、利用率用阈值色提示", 1.05, 5.75, 4.25);
  addPill(s, "质量：SPC、CPK、UCL/LCL 支持过程判断", 7.1, 5.75, 4.45, C.pale2);
  note(7, "设备与质量", "设备模块把温度、振动和利用率用阈值色表达，高危报警可以确认并生成维护记录。质量模块通过 SPC、CPK、UCL 和 LCL 帮助质量工程师判断过程是否稳定。这两部分都体现了异常信息突出原则。");
}

// 8 Materials + integration
{
  const s = addSlide("INTEGRATION", "物料物流与后端接入让系统从“看板”变为“执行系统”");
  addImage(s, path.join(SHOTS, "05-materials.png"), 0.75, 1.45, 5.75, 3.68);
  addImage(s, path.join(SHOTS, "06-integration.png"), 6.83, 1.45, 5.75, 3.68);
  addPill(s, "低库存：安全线 + 补货动作 + 告警状态", 1.05, 5.75, 4.05);
  addPill(s, "数据源：PLC / SCADA / ERP / WMS / QMS", 7.1, 5.75, 4.25, C.pale2);
  note(8, "物料与数据接入", "物料页面体现安全库存和缺料预警，低库存时可以生成补货任务。数据采集页面模拟 PLC、SCADA、ERP、WMS、QMS 接入 MES，点击采集后会联动总控、设备、库存、质量和日志。");
}

// 9 Theory mapping
{
  const s = addSlide("THEORY", "PPT 知识点不是附加说明，而是进入了界面设计");
  const rows = [
    ["黄金规则", "一致性、反馈、结束信息、错误预防"],
    ["布局原则", "左侧导航 + 分区面板 + 层级化总控"],
    ["数据编码", "绿/黄/红状态色，大号 KPI，进度条长度编码"],
    ["视觉认知", "异常前置，降低系列搜索和认知负荷"],
    ["动效原则", "克制地用数据变化和日志新增表达状态"],
  ];
  rows.forEach((r, i) => {
    const y = 1.55 + i * 0.92;
    addPill(s, r[0], 1.05, y, 1.45, i % 2 ? C.pale2 : C.pale);
    s.addText(r[1], { x: 2.8, y: y + 0.07, w: 8.6, h: 0.24, fontSize: 15, color: C.ink, bold: true, margin: 0 });
  });
  s.addText("一句话：工业界面要服务效率、安全、清晰和抗干扰。", { x: 1.25, y: 6.35, w: 10.5, h: 0.36, fontSize: 18, bold: true, color: C.accent, align: "center", margin: 0 });
  note(9, "理论映射", "本项目不是单纯做界面，而是把课程知识点落到界面上。黄金规则体现在一致性和反馈，布局原则体现在左侧导航和分区面板，数据编码体现在交通灯状态色和进度条，视觉认知体现在异常前置，动效原则则体现在克制的状态变化。");
}

// 10 Highlights and reflection
{
  const s = addSlide("REFLECTION", "项目亮点清晰，但仍有可继续扩展的空间");
  addCard(s, "设计亮点", "场景统一为汽车制造；页面数量达到 13 页；核心交互能形成日志闭环；新增后端采集与接入模拟。", 0.9, 1.65, 5.55, 2.1, C.pale);
  addCard(s, "现阶段不足", "仍是前端仿真，未接真实数据库和设备；图符体系可以继续完善；移动端和平板适配还可以加强。", 6.9, 1.65, 5.55, 2.1, C.pale2);
  addCard(s, "后续方向", "连接真实接口、补充 AI 辅助决策、数字孪生或 AR 运维，并形成更完整的工业数据闭环。", 3.05, 4.45, 7.25, 1.25, C.white);
  note(10, "亮点与反思", "项目的亮点是场景统一、页面完整、交互闭环，并且增加了后端数据采集模拟。不足是目前仍是前端仿真，没有真实数据库和设备接口，图符体系和多终端适配也可以继续完善。后续可以加入 AI 决策、数字孪生或 AR 运维。");
}

// 11 Demo tutorial
{
  const s = addSlide("DEMO", "演示启动方式：优先使用 npm.cmd，避免 PowerShell 策略拦截");
  const steps = [
    ["1", "进入项目目录", "cd E:\\OneDrive\\桌面\\MES\\carmessys"],
    ["2", "首次安装依赖", "npm.cmd install"],
    ["3", "启动开发服务", "npm.cmd run dev"],
    ["4", "打开浏览器地址", "通常为 http://127.0.0.1:1421"],
  ];
  steps.forEach((st, i) => {
    const y = 1.55 + i * 1.08;
    addPill(s, st[0], 1.05, y, 0.48, C.accent2);
    s.addText(st[1], { x: 1.78, y: y + 0.02, w: 2.1, h: 0.25, fontSize: 14, bold: true, color: C.ink, margin: 0 });
    s.addText(st[2], { x: 4.05, y: y + 0.02, w: 6.9, h: 0.25, fontSize: 13, color: C.muted, fontFace: "Consolas", margin: 0, fit: "shrink" });
  });
  s.addText("也可以双击 start-carmessys.bat 自动启动。若打包桌面程序，需要补齐 Rust/Cargo 与 Visual Studio Build Tools。", { x: 1.05, y: 6.25, w: 10.8, h: 0.42, fontSize: 13, color: C.ink, margin: 0, align: "center" });
  note(11, "启动教程", "演示时可以用四步启动：进入 carmessys 目录，首次安装依赖，运行 npm.cmd run dev，然后打开浏览器地址。这里特别说明使用 npm.cmd，是为了避免 PowerShell 的脚本执行策略拦截。也可以双击 start-carmessys.bat。");
}

// 12 End
{
  const s = addSlide("THANK YOU", "汇报结束，欢迎老师批评指正");
  s.addText("Carmessys 汽车制造 MES 系统", { x: 1.15, y: 2.45, w: 10.8, h: 0.55, fontSize: 33, bold: true, color: C.ink, align: "center", margin: 0 });
  s.addText("用人机交互理论，把复杂工业数据组织成可理解、可操作、可追溯的现场执行界面。", { x: 2.0, y: 3.35, w: 9.25, h: 0.42, fontSize: 15, color: C.muted, align: "center", margin: 0 });
  note(12, "结束页", "以上就是我们的汇报。总体来说，本项目希望用人机交互理论，把复杂的工业数据组织成可理解、可操作、可追溯的现场执行界面。感谢老师聆听，欢迎批评指正。");
}

await pptx.writeFile({ fileName: OUT_PPT });

const script = slides.map((s) => `第${s.num}页：${s.title}\n${s.text}\n`).join("\n");
fs.writeFileSync(OUT_TXT, script, "utf8");

console.log(OUT_PPT);
console.log(OUT_TXT);
