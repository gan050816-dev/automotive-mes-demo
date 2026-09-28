export type PageKey =
  | "dashboard"
  | "orders"
  | "orderDispatch"
  | "equipment"
  | "equipmentDetail"
  | "quality"
  | "spc"
  | "traceability"
  | "materials"
  | "agv"
  | "integration"
  | "permissions"
  | "logs";

export type Status = "running" | "warning" | "danger" | "idle" | "done";

export interface NavItem {
  key: PageKey;
  label: string;
  group: string;
}

export interface WorkOrder {
  id: string;
  model: string;
  line: string;
  priority: "高" | "中" | "低";
  status: "待下发" | "生产中" | "质检中" | "已完成";
  progress: number;
  due: string;
  steps: string[];
}

export interface Device {
  id: string;
  name: string;
  line: string;
  status: Status;
  temperature: number;
  vibration: number;
  utilization: number;
  alarm: string;
}

export interface QualityBatch {
  id: string;
  model: string;
  passRate: number;
  defect: string;
  source: string;
  process: string;
  inspector: string;
}

export interface Material {
  code: string;
  name: string;
  stock: number;
  safety: number;
  unit: string;
  location: string;
}

export interface Agv {
  id: string;
  task: string;
  battery: number;
  status: "运输中" | "待命" | "充电" | "异常";
}

export interface Role {
  name: string;
  users: number;
  access: string[];
}

export interface SystemLog {
  time: string;
  user: string;
  action: string;
  level: "信息" | "警告" | "高危";
}

export interface BackendSource {
  id: string;
  name: string;
  protocol: string;
  system: string;
  status: "在线" | "延迟" | "离线";
  latency: number;
  packets: number;
  lastValue: string;
}

export interface IngestionEvent {
  time: string;
  source: string;
  tag: string;
  value: string;
  target: string;
  result: "已入库" | "待校验" | "告警";
}

export const navItems: NavItem[] = [
  { key: "dashboard", label: "总控看板", group: "总览" },
  { key: "orders", label: "工单总览", group: "工单" },
  { key: "orderDispatch", label: "工单详情/下发", group: "工单" },
  { key: "equipment", label: "设备监控总览", group: "设备" },
  { key: "equipmentDetail", label: "设备详情/报警", group: "设备" },
  { key: "quality", label: "质量总览", group: "质量" },
  { key: "spc", label: "SPC/缺陷分析", group: "质量" },
  { key: "traceability", label: "质量追溯", group: "质量" },
  { key: "materials", label: "物料库存", group: "物料" },
  { key: "agv", label: "AGV/物流追踪", group: "物料" },
  { key: "integration", label: "数据采集/接入", group: "集成" },
  { key: "permissions", label: "人员权限", group: "权限" },
  { key: "logs", label: "操作日志/安全", group: "权限" },
];

export const kpis = [
  { label: "今日产量", value: "2,486", unit: "辆/套", tone: "good" },
  { label: "OEE", value: "86.4", unit: "%", tone: "info" },
  { label: "订单完成率", value: "91.8", unit: "%", tone: "good" },
  { label: "能耗", value: "42.6", unit: "MWh", tone: "warn" },
  { label: "报警", value: "4", unit: "条", tone: "danger" },
];

export const oeeTrend = [78, 81, 82, 86, 84, 88, 86];
export const outputTrend = [320, 352, 341, 386, 402, 391, 424];
export const defectTrend = [1.8, 1.5, 1.6, 1.3, 1.2, 1.4, 1.1];
export const energyTrend = [36, 38, 41, 40, 43, 42, 44];

export const workOrders: WorkOrder[] = [
  {
    id: "WO-20260612-001",
    model: "纯电 SUV 车门总成",
    line: "总装一线",
    priority: "高",
    status: "生产中",
    progress: 74,
    due: "18:30",
    steps: ["下发", "焊装", "涂装", "总装", "终检"],
  },
  {
    id: "WO-20260612-002",
    model: "混动轿车电池托盘",
    line: "焊装二线",
    priority: "中",
    status: "质检中",
    progress: 88,
    due: "19:10",
    steps: ["下发", "冲压", "焊装", "尺寸检测", "入库"],
  },
  {
    id: "WO-20260612-003",
    model: "底盘副车架",
    line: "机加三线",
    priority: "低",
    status: "待下发",
    progress: 12,
    due: "21:00",
    steps: ["排产", "备料", "加工", "检验", "转运"],
  },
  {
    id: "WO-20260612-004",
    model: "智能座舱线束",
    line: "电子装配线",
    priority: "高",
    status: "已完成",
    progress: 100,
    due: "16:20",
    steps: ["下发", "裁线", "压接", "导通测试", "包装"],
  },
];

export const devices: Device[] = [
  {
    id: "RB-WD-01",
    name: "焊接机器人 A01",
    line: "焊装一线",
    status: "running",
    temperature: 61,
    vibration: 1.8,
    utilization: 94,
    alarm: "无",
  },
  {
    id: "PR-ST-02",
    name: "冲压机 P02",
    line: "冲压车间",
    status: "warning",
    temperature: 78,
    vibration: 3.6,
    utilization: 82,
    alarm: "振动偏高",
  },
  {
    id: "AG-QC-03",
    name: "视觉检测站 Q03",
    line: "终检区",
    status: "running",
    temperature: 42,
    vibration: 0.8,
    utilization: 89,
    alarm: "无",
  },
  {
    id: "CN-AS-04",
    name: "拧紧工作站 N04",
    line: "总装二线",
    status: "danger",
    temperature: 84,
    vibration: 4.9,
    utilization: 63,
    alarm: "扭矩传感器异常",
  },
];

export const qualityBatches: QualityBatch[] = [
  {
    id: "BATCH-AUTO-260612-A",
    model: "车门总成",
    passRate: 98.7,
    defect: "焊点偏移",
    source: "焊装一线 / RB-WD-01",
    process: "机器人焊接",
    inspector: "李工",
  },
  {
    id: "BATCH-AUTO-260612-B",
    model: "电池托盘",
    passRate: 97.9,
    defect: "尺寸偏差",
    source: "焊装二线 / PR-ST-02",
    process: "冲压成型",
    inspector: "王工",
  },
  {
    id: "BATCH-AUTO-260612-C",
    model: "智能座舱线束",
    passRate: 99.4,
    defect: "端子压接不良",
    source: "电子装配线",
    process: "导通测试",
    inspector: "赵工",
  },
];

export const materials: Material[] = [
  { code: "MAT-ST-001", name: "高强钢板", stock: 46, safety: 60, unit: "吨", location: "原料库 A2" },
  { code: "MAT-BT-002", name: "电池托盘铝型材", stock: 128, safety: 80, unit: "件", location: "立体库 B1" },
  { code: "MAT-EL-003", name: "线束端子", stock: 18000, safety: 12000, unit: "个", location: "电子料仓 C3" },
  { code: "MAT-PA-004", name: "内饰卡扣", stock: 8200, safety: 9000, unit: "个", location: "辅料区 D4" },
];

export const agvs: Agv[] = [
  { id: "AGV-01", task: "原料库 A2 -> 冲压车间", battery: 76, status: "运输中" },
  { id: "AGV-02", task: "焊装一线 -> 总装一线", battery: 58, status: "运输中" },
  { id: "AGV-03", task: "待命区", battery: 92, status: "待命" },
  { id: "AGV-04", task: "充电桩 2", battery: 24, status: "充电" },
];

export const roles: Role[] = [
  { name: "生产管理员", users: 4, access: ["工单下发", "看板配置", "异常升级"] },
  { name: "设备维护员", users: 8, access: ["设备详情", "报警确认", "维护记录"] },
  { name: "质量工程师", users: 6, access: ["SPC 分析", "质量追溯", "缺陷闭环"] },
  { name: "仓储调度员", users: 5, access: ["库存预警", "AGV 调度", "出入库"] },
];

export const logs: SystemLog[] = [
  { time: "17:02:10", user: "生产管理员", action: "下发 WO-20260612-003 至机加三线", level: "信息" },
  { time: "17:08:44", user: "设备维护员", action: "确认拧紧工作站 N04 扭矩报警", level: "警告" },
  { time: "17:15:31", user: "质量工程师", action: "追溯 BATCH-AUTO-260612-B 缺陷来源", level: "信息" },
  { time: "17:21:02", user: "系统", action: "检测到非授权配置访问尝试", level: "高危" },
];

export const alerts = [
  { id: "ALM-001", title: "拧紧工作站扭矩传感器异常", page: "equipmentDetail" as PageKey, level: "高", acknowledged: false },
  { id: "ALM-002", title: "高强钢板库存低于安全线", page: "materials" as PageKey, level: "中", acknowledged: false },
  { id: "ALM-003", title: "电池托盘尺寸偏差轻微上升", page: "spc" as PageKey, level: "中", acknowledged: true },
];

export const backendSources: BackendSource[] = [
  {
    id: "SRC-PLC-01",
    name: "焊装 PLC",
    protocol: "OPC UA",
    system: "设备层",
    status: "在线",
    latency: 42,
    packets: 1286,
    lastValue: "RB-WD-01.temp=61",
  },
  {
    id: "SRC-SCADA-02",
    name: "总装 SCADA",
    protocol: "MQTT",
    system: "监控层",
    status: "在线",
    latency: 58,
    packets: 964,
    lastValue: "Line01.output=2486",
  },
  {
    id: "SRC-ERP-03",
    name: "ERP 订单",
    protocol: "REST API",
    system: "计划层",
    status: "延迟",
    latency: 180,
    packets: 318,
    lastValue: "WO-20260612-003",
  },
  {
    id: "SRC-WMS-04",
    name: "WMS 库存",
    protocol: "REST API",
    system: "物流层",
    status: "在线",
    latency: 75,
    packets: 642,
    lastValue: "MAT-ST-001=46",
  },
  {
    id: "SRC-QMS-05",
    name: "QMS 检验",
    protocol: "Message Queue",
    system: "质量层",
    status: "在线",
    latency: 92,
    packets: 511,
    lastValue: "CPK=1.42",
  },
];

export const ingestionEvents: IngestionEvent[] = [
  { time: "17:28:12", source: "焊装 PLC", tag: "RB-WD-01.temperature", value: "61°C", target: "设备监控", result: "已入库" },
  { time: "17:28:15", source: "WMS 库存", tag: "MAT-ST-001.stock", value: "46吨", target: "物料库存", result: "告警" },
  { time: "17:28:19", source: "QMS 检验", tag: "BATCH-A.passRate", value: "98.7%", target: "质量追溯", result: "已入库" },
  { time: "17:28:22", source: "ERP 订单", tag: "WO-20260612-003.status", value: "待下发", target: "工单管理", result: "待校验" },
];
