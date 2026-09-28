<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <span class="brand-mark">MES</span>
        <div>
          <h1>汽车制造 MES 系统</h1>
          <p>智能制造人机交互模型</p>
        </div>
      </div>

      <nav class="nav-list" aria-label="MES 页面导航">
        <button
          v-for="item in navItems"
          :key="item.key"
          :class="['nav-item', { active: currentPage === item.key }]"
          type="button"
          @click="currentPage = item.key"
        >
          <span>{{ item.group }}</span>
          <strong>{{ item.label }}</strong>
        </button>
      </nav>
    </aside>

    <main class="workspace">
      <header class="topbar">
        <div>
          <p class="eyebrow">实时生产指挥中心</p>
          <h2>{{ pageTitle }}</h2>
        </div>
        <div class="status-strip">
          <span class="dot"></span>
          <span>模拟数据在线</span>
          <span>2026-06-12 17:30</span>
          <button class="cycle-button" type="button" @click="simulateProductionCycle">推进一轮生产</button>
          <button class="cycle-button ingest" type="button" @click="simulateBackendIngestion">采集一批数据</button>
          <label class="role-switch">
            <span>当前角色</span>
            <select v-model="selectedRoleName">
              <option v-for="role in roles" :key="role.name" :value="role.name">{{ role.name }}</option>
            </select>
          </label>
        </div>
      </header>

      <section class="theory-strip" aria-label="当前页面设计依据">
        <div v-for="note in currentDesignNotes" :key="note.title">
          <strong>{{ note.title }}</strong>
          <span>{{ note.text }}</span>
        </div>
      </section>

      <section v-if="currentPage === 'dashboard'" class="page-grid">
        <article v-for="kpi in dashboardKpis" :key="kpi.label" :class="['metric-card', kpi.tone]">
          <span>{{ kpi.label }}</span>
          <strong>{{ kpi.value }}</strong>
          <small>{{ kpi.unit }}</small>
        </article>
        <Panel title="OEE 与产量趋势" wide>
          <div class="dual-charts">
            <MiniChart label="OEE" :values="oeeTrend" suffix="%" />
            <MiniChart label="产量" :values="outputTrend" suffix="件" />
          </div>
        </Panel>
        <Panel title="生产状态总览">
          <div class="status-matrix">
            <StatusPill label="运行设备" :value="runningDeviceCount.toString()" tone="good" />
            <StatusPill label="预警设备" :value="warningDeviceCount.toString()" tone="warn" />
            <StatusPill label="高危设备" :value="dangerDeviceCount.toString()" tone="danger" />
            <StatusPill label="待处理报警" :value="pendingAlerts.length.toString()" tone="danger" />
          </div>
        </Panel>
        <Panel title="告警优先级">
          <AlertList :items="localAlerts" @jump="jumpToAlert" @ack="ackAlert" />
        </Panel>
        <Panel title="行业 MES 能力映射" wide>
          <div class="benchmark-grid">
            <div v-for="item in benchmarkPractices" :key="item.title">
              <span>{{ item.source }}</span>
              <strong>{{ item.title }}</strong>
              <p>{{ item.text }}</p>
            </div>
          </div>
        </Panel>
      </section>

      <section v-else-if="currentPage === 'orders'" class="content-layout">
        <Panel title="工单状态查询" wide>
          <div class="toolbar">
            <button
              v-for="filter in orderFilters"
              :key="filter"
              :class="['chip', { active: orderFilter === filter }]"
              type="button"
              @click="orderFilter = filter"
            >
              {{ filter }}
            </button>
          </div>
          <div class="table-list">
            <button
              v-for="order in filteredOrders"
              :key="order.id"
              :class="['table-row', { selected: selectedOrderId === order.id }]"
              type="button"
              @click="selectOrder(order.id, 'orderDispatch')"
            >
              <span>{{ order.id }}</span>
              <strong>{{ order.model }}</strong>
              <span>{{ order.line }}</span>
              <StatusBadge :label="order.status" />
              <ProgressBar :value="order.progress" />
            </button>
          </div>
        </Panel>
        <Panel title="工单优先级">
          <div class="priority-stack">
            <StatusPill label="高优先级" :value="priorityCount('高').toString()" tone="danger" />
            <StatusPill label="中优先级" :value="priorityCount('中').toString()" tone="warn" />
            <StatusPill label="低优先级" :value="priorityCount('低').toString()" tone="good" />
          </div>
          <div class="schedule-board">
            <h3>APS 排程片段</h3>
            <div v-for="item in schedulePlan" :key="item.line">
              <span>{{ item.line }}</span>
              <strong>{{ item.window }}</strong>
              <small>{{ item.constraint }}</small>
            </div>
          </div>
        </Panel>
      </section>

      <section v-else-if="currentPage === 'orderDispatch'" class="content-layout">
        <Panel title="工单详情与下发" wide>
          <div class="detail-head">
            <div>
              <span class="eyebrow">{{ selectedOrder.id }}</span>
              <h3>{{ selectedOrder.model }}</h3>
            </div>
            <button class="primary-action" type="button" @click="dispatchSelectedOrder">
              {{ selectedOrder.status === "待下发" ? "下发工单" : "查看执行" }}
            </button>
          </div>
          <div class="process-flow">
            <div
              v-for="(step, index) in selectedOrder.steps"
              :key="step"
              :class="['process-step', { done: index * 20 < selectedOrder.progress, active: index * 20 <= selectedOrder.progress && (index + 1) * 20 > selectedOrder.progress }]"
            >
              {{ step }}
            </div>
          </div>
          <ProgressBar :value="selectedOrder.progress" large />
          <div class="esop-panel">
            <h3>电子作业指导 eSOP</h3>
            <div v-for="item in workInstructions" :key="item.step">
              <span>{{ item.step }}</span>
              <strong>{{ item.instruction }}</strong>
              <small>{{ item.check }}</small>
            </div>
          </div>
        </Panel>
        <Panel title="操作反馈">
          <p class="feedback-text">{{ orderFeedback }}</p>
          <StatusPill label="生产节拍" :value="`${factoryStats.takt}s/台`" tone="info" />
          <dl class="fact-list">
            <div><dt>产线</dt><dd>{{ selectedOrder.line }}</dd></div>
            <div><dt>交付节点</dt><dd>{{ selectedOrder.due }}</dd></div>
            <div><dt>优先级</dt><dd>{{ selectedOrder.priority }}</dd></div>
          </dl>
        </Panel>
      </section>

      <section v-else-if="currentPage === 'equipment'" class="content-layout">
        <Panel title="设备运行状态" wide>
          <div class="device-grid">
            <button
              v-for="device in localDevices"
              :key="device.id"
              :class="['device-card', device.status, { selected: selectedDeviceId === device.id }]"
              type="button"
              @click="selectDevice(device.id, 'equipmentDetail')"
            >
              <span>{{ device.id }}</span>
              <strong>{{ device.name }}</strong>
              <small>{{ device.line }}</small>
              <ProgressBar :value="device.utilization" />
            </button>
          </div>
        </Panel>
        <Panel title="停机统计">
          <MiniChart label="停机分钟" :values="[12, 9, 24, 18, 45, 16, 22]" suffix="min" />
        </Panel>
      </section>

      <section v-else-if="currentPage === 'equipmentDetail'" class="content-layout">
        <Panel title="设备详情与报警处理" wide>
          <div class="detail-head">
            <div>
              <span class="eyebrow">{{ selectedDevice.id }}</span>
              <h3>{{ selectedDevice.name }}</h3>
            </div>
            <StatusBadge :label="deviceStatusText" />
          </div>
          <div class="sensor-grid">
            <StatusPill label="温度" :value="`${selectedDevice.temperature}°C`" :tone="selectedDevice.temperature > 80 ? 'danger' : 'good'" />
            <StatusPill label="振动" :value="`${selectedDevice.vibration} mm/s`" :tone="selectedDevice.vibration > 4 ? 'danger' : 'warn'" />
            <StatusPill label="利用率" :value="`${selectedDevice.utilization}%`" tone="info" />
          </div>
        </Panel>
        <Panel title="异常报警">
          <p class="alarm-text">{{ selectedDevice.alarm }}</p>
          <button class="primary-action full" type="button" :disabled="selectedDevice.alarm === '无'" @click="ackEquipmentAlarm">
            确认并生成维护记录
          </button>
          <p class="feedback-text">{{ equipmentFeedback }}</p>
          <div class="maintenance-box">
            <strong>预测性维护建议</strong>
            <span>{{ maintenanceAdvice }}</span>
          </div>
        </Panel>
      </section>

      <section v-else-if="currentPage === 'quality'" class="content-layout">
        <Panel title="质量指标总览" wide>
          <div class="quality-row">
            <StatusPill label="首检合格率" value="98.2%" tone="good" />
            <StatusPill label="最终合格率" value="99.1%" tone="good" />
            <StatusPill label="DPPM" value="148" tone="warn" />
            <StatusPill label="待闭环缺陷" value="3" tone="danger" />
          </div>
          <MiniChart label="不良率趋势" :values="defectTrend" suffix="%" />
        </Panel>
        <Panel title="缺陷分类">
          <div class="defect-bars">
            <ProgressBar label="焊点偏移" :value="42" />
            <ProgressBar label="尺寸偏差" :value="31" />
            <ProgressBar label="压接不良" :value="18" />
          </div>
        </Panel>
      </section>

      <section v-else-if="currentPage === 'spc'" class="content-layout">
        <Panel title="SPC 与过程能力" wide>
          <div class="spc-chart">
            <span v-for="(value, index) in [48, 53, 49, 57, 51, 55, 50, 58, 52]" :key="index" :style="{ height: `${value}%` }"></span>
          </div>
          <div class="quality-row">
            <StatusPill label="CPK" value="1.42" tone="good" />
            <StatusPill label="UCL" value="58.5" tone="info" />
            <StatusPill label="LCL" value="43.2" tone="info" />
          </div>
        </Panel>
        <Panel title="缺陷预警">
          <AlertList :items="localAlerts.filter((item) => item.page === 'spc')" @jump="jumpToAlert" @ack="ackAlert" />
        </Panel>
      </section>

      <section v-else-if="currentPage === 'traceability'" class="content-layout">
        <Panel title="质量追溯" wide>
          <div class="toolbar">
            <button
              v-for="batch in qualityBatches"
              :key="batch.id"
              :class="['chip', { active: selectedBatchId === batch.id }]"
              type="button"
              @click="selectedBatchId = batch.id"
            >
              {{ batch.model }}
            </button>
          </div>
          <div class="trace-chain">
            <div><span>批次</span><strong>{{ selectedBatch.id }}</strong></div>
            <div><span>来源</span><strong>{{ selectedBatch.source }}</strong></div>
            <div><span>工序</span><strong>{{ selectedBatch.process }}</strong></div>
            <div><span>检验员</span><strong>{{ selectedBatch.inspector }}</strong></div>
          </div>
          <div class="genealogy-board">
            <h3>正反向追溯</h3>
            <div><span>反向</span><strong>成品批次 -> 工序 -> 设备 -> 原料批次</strong></div>
            <div><span>正向</span><strong>原料批次 -> 在制品 -> 成品 VIN 范围</strong></div>
          </div>
        </Panel>
        <Panel title="追溯结果">
          <StatusPill label="合格率" :value="`${selectedBatch.passRate}%`" tone="good" />
          <p class="alarm-text">主要缺陷：{{ selectedBatch.defect }}</p>
        </Panel>
      </section>

      <section v-else-if="currentPage === 'materials'" class="content-layout">
        <Panel title="物料库存与缺料预警" wide>
          <div class="table-list">
            <div v-for="material in localMaterials" :key="material.code" :class="['inventory-row', { low: material.stock < material.safety }]">
              <span>{{ material.code }}</span>
              <strong>{{ material.name }}</strong>
              <span>{{ material.location }}</span>
              <ProgressBar :label="`${material.stock}/${material.safety} ${material.unit}`" :value="Math.min(100, Math.round((material.stock / material.safety) * 100))" />
              <button class="row-action" type="button" :disabled="material.stock >= material.safety" @click="replenishMaterial(material.code)">
                {{ material.stock < material.safety ? "生成补货" : "库存正常" }}
              </button>
            </div>
          </div>
        </Panel>
        <Panel title="库存成本">
          <StatusPill label="库存总价值" :value="`${inventoryValue}万`" tone="info" />
          <StatusPill label="周转率" value="4.6次/月" tone="good" />
        </Panel>
      </section>

      <section v-else-if="currentPage === 'agv'" class="content-layout">
        <Panel title="AGV/物流追踪" wide>
          <div class="agv-map">
            <div
              v-for="agv in localAgvs"
              :key="agv.id"
              :class="['agv-node', agv.status === '异常' ? 'danger' : agv.status === '充电' ? 'warn' : 'good', { selected: selectedAgvId === agv.id }]"
              @click="selectedAgvId = agv.id"
            >
              <strong>{{ agv.id }}</strong>
              <span>{{ agv.task }}</span>
              <ProgressBar :value="agv.battery" />
            </div>
          </div>
        </Panel>
        <Panel title="物流状态">
          <StatusPill label="运输中" :value="agvStatusCount('运输中').toString()" tone="good" />
          <StatusPill label="待命" :value="agvStatusCount('待命').toString()" tone="info" />
          <StatusPill label="充电" :value="agvStatusCount('充电').toString()" tone="warn" />
          <button class="primary-action full" type="button" @click="dispatchAgv">调度选中 AGV</button>
          <p class="feedback-text">{{ agvFeedback }}</p>
        </Panel>
      </section>

      <section v-else-if="currentPage === 'integration'" class="content-layout integration-layout">
        <Panel title="数据源连接状态" wide>
          <div class="source-grid">
            <div
              v-for="source in localBackendSources"
              :key="source.id"
              :class="['source-card', source.status === '在线' ? 'online' : source.status === '延迟' ? 'delay' : 'offline']"
            >
              <div>
                <span>{{ source.system }}</span>
                <strong>{{ source.name }}</strong>
              </div>
              <StatusBadge :label="source.status" />
              <dl>
                <div><dt>协议</dt><dd>{{ source.protocol }}</dd></div>
                <div><dt>延迟</dt><dd>{{ source.latency }} ms</dd></div>
                <div><dt>包数</dt><dd>{{ source.packets }}</dd></div>
                <div><dt>最近值</dt><dd>{{ source.lastValue }}</dd></div>
              </dl>
            </div>
          </div>
        </Panel>
        <Panel title="采集与映射流水线">
          <div class="pipeline">
            <div class="pipeline-step active">
              <span>01</span>
              <strong>边缘采集</strong>
              <p>PLC、SCADA、传感器、WMS、ERP 接入网关</p>
            </div>
            <div class="pipeline-step active">
              <span>02</span>
              <strong>清洗校验</strong>
              <p>统一标签、时间戳、单位和异常阈值</p>
            </div>
            <div class="pipeline-step active">
              <span>03</span>
              <strong>业务映射</strong>
              <p>写入工单、设备、质量、库存和物流对象</p>
            </div>
            <div class="pipeline-step warn">
              <span>04</span>
              <strong>告警闭环</strong>
              <p>低库存、设备异常和接口延迟进入日志</p>
            </div>
          </div>
        </Panel>
        <Panel title="最近接入数据" wide>
          <div class="ingestion-list">
            <div v-for="event in localIngestionEvents" :key="`${event.time}-${event.tag}-${event.value}`" class="ingestion-row">
              <span>{{ event.time }}</span>
              <strong>{{ event.source }}</strong>
              <code>{{ event.tag }}</code>
              <span>{{ event.value }}</span>
              <span>{{ event.target }}</span>
              <StatusBadge :label="event.result" />
            </div>
          </div>
        </Panel>
        <Panel title="接入反馈">
          <div class="status-matrix compact">
            <StatusPill label="在线数据源" :value="`${onlineSourceCount}/${localBackendSources.length}`" tone="good" />
            <StatusPill label="本批次数据" :value="`${localIngestionEvents.length}条`" tone="info" />
            <StatusPill label="平均延迟" :value="`${averageLatency}ms`" :tone="averageLatency > 120 ? 'warn' : 'good'" />
            <StatusPill label="接入模式" value="模拟网关" tone="info" />
          </div>
          <p class="feedback-text">{{ ingestionFeedback }}</p>
          <button class="primary-action full" type="button" @click="simulateBackendIngestion">立即采集并写入 MES</button>
        </Panel>
      </section>

      <section v-else-if="currentPage === 'permissions'" class="content-layout">
        <Panel title="用户角色与权限分配" wide>
          <div class="role-grid">
            <button
              v-for="role in roles"
              :key="role.name"
              :class="['role-card', { selected: selectedRoleName === role.name }]"
              type="button"
              @click="selectedRoleName = role.name"
            >
              <strong>{{ role.name }}</strong>
              <span>{{ role.users }} 人</span>
            </button>
          </div>
          <div class="permission-list">
            <span v-for="access in selectedRole.access" :key="access">{{ access }}</span>
          </div>
          <div class="skill-matrix">
            <h3>技能与认证</h3>
            <div v-for="skill in skillMatrix" :key="skill.name">
              <span>{{ skill.name }}</span>
              <ProgressBar :label="skill.label" :value="skill.value" />
            </div>
          </div>
        </Panel>
        <Panel title="权限反馈">
          <p class="feedback-text">当前选中：{{ selectedRole.name }}。关键操作采用角色授权与操作日志双重约束。</p>
        </Panel>
      </section>

      <section v-else class="content-layout">
        <Panel title="操作日志与安全管理" wide>
          <div class="log-list">
            <div v-for="log in localLogs" :key="`${log.time}-${log.action}`" :class="['log-row', log.level === '高危' ? 'danger' : log.level === '警告' ? 'warn' : '']">
              <span>{{ log.time }}</span>
              <strong>{{ log.user }}</strong>
              <p>{{ log.action }}</p>
              <StatusBadge :label="log.level" />
            </div>
          </div>
        </Panel>
        <Panel title="安全策略">
          <StatusPill label="失败登录" value="2" tone="warn" />
          <StatusPill label="高危事件" :value="highRiskLogCount.toString()" tone="danger" />
          <StatusPill label="审计覆盖" value="100%" tone="good" />
        </Panel>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, defineComponent, h, ref, type PropType } from "vue";
import {
  agvs as initialAgvs,
  alerts,
  backendSources as initialBackendSources,
  defectTrend,
  devices as initialDevices,
  ingestionEvents as initialIngestionEvents,
  logs as initialLogs,
  materials as initialMaterials,
  navItems,
  oeeTrend,
  outputTrend,
  qualityBatches,
  roles,
  workOrders as initialWorkOrders,
  type Agv,
  type BackendSource,
  type IngestionEvent,
  type Material,
  type PageKey,
  type SystemLog,
  type WorkOrder,
} from "./mockData";

const currentPage = ref<PageKey>("dashboard");
const localOrders = ref<WorkOrder[]>(initialWorkOrders.map((item) => ({ ...item, steps: [...item.steps] })));
const localDevices = ref(initialDevices.map((item) => ({ ...item })));
const localMaterials = ref<Material[]>(initialMaterials.map((item) => ({ ...item })));
const localAgvs = ref<Agv[]>(initialAgvs.map((item) => ({ ...item })));
const localLogs = ref<SystemLog[]>(initialLogs.map((item) => ({ ...item })));
const localBackendSources = ref<BackendSource[]>(initialBackendSources.map((item) => ({ ...item })));
const localIngestionEvents = ref<IngestionEvent[]>(initialIngestionEvents.map((item) => ({ ...item })));
const factoryStats = ref({
  output: 2486,
  oee: 86.4,
  completionRate: 91.8,
  energy: 42.6,
  takt: 58,
});
const selectedOrderId = ref(localOrders.value[0].id);
const selectedDeviceId = ref(localDevices.value[0].id);
const selectedBatchId = ref(qualityBatches[0].id);
const selectedRoleName = ref(roles[0].name);
const selectedAgvId = ref(localAgvs.value[0].id);
const orderFilter = ref("全部");
const orderFeedback = ref("选择工单后可查看流程，也可以对待下发工单执行下发。");
const equipmentFeedback = ref("高危报警需要维护员确认，确认后进入操作日志闭环。");
const agvFeedback = ref("选择 AGV 后可派发紧急物料转运任务。");
const ingestionFeedback = ref("后端接入网关待命：可模拟 PLC/SCADA/ERP/WMS/QMS 数据进入 MES。");
const localAlerts = ref(alerts.map((item) => ({ ...item })));

const orderFilters = ["全部", "待下发", "生产中", "质检中", "已完成"];
const pageTitle = computed(() => navItems.find((item) => item.key === currentPage.value)?.label ?? "总控看板");
const dashboardKpis = computed(() => [
  { label: "今日产量", value: factoryStats.value.output.toLocaleString("zh-CN"), unit: "辆/套", tone: "good" },
  { label: "OEE", value: factoryStats.value.oee.toFixed(1), unit: "%", tone: "info" },
  { label: "订单完成率", value: factoryStats.value.completionRate.toFixed(1), unit: "%", tone: "good" },
  { label: "能耗", value: factoryStats.value.energy.toFixed(1), unit: "MWh", tone: "warn" },
  { label: "报警", value: pendingAlerts.value.length.toString(), unit: "条", tone: "danger" },
]);
const selectedOrder = computed(() => localOrders.value.find((order) => order.id === selectedOrderId.value) ?? localOrders.value[0]);
const selectedDevice = computed(() => localDevices.value.find((device) => device.id === selectedDeviceId.value) ?? localDevices.value[0]);
const selectedBatch = computed(() => qualityBatches.find((batch) => batch.id === selectedBatchId.value) ?? qualityBatches[0]);
const selectedRole = computed(() => roles.find((role) => role.name === selectedRoleName.value) ?? roles[0]);
const pendingAlerts = computed(() => localAlerts.value.filter((item) => !item.acknowledged));
const runningDeviceCount = computed(() => localDevices.value.filter((device) => device.status === "running").length);
const warningDeviceCount = computed(() => localDevices.value.filter((device) => device.status === "warning").length);
const dangerDeviceCount = computed(() => localDevices.value.filter((device) => device.status === "danger").length);
const inventoryValue = computed(() => Math.round(localMaterials.value.reduce((total, item) => total + item.stock * 0.018, 0)));
const highRiskLogCount = computed(() => localLogs.value.filter((log) => log.level === "高危").length);
const onlineSourceCount = computed(() => localBackendSources.value.filter((source) => source.status === "在线").length);
const averageLatency = computed(() =>
  Math.round(localBackendSources.value.reduce((total, source) => total + source.latency, 0) / localBackendSources.value.length),
);
const deviceStatusText = computed(() => {
  const map = { running: "运行中", warning: "预警", danger: "高危", idle: "待命", done: "完成" };
  return map[selectedDevice.value.status];
});
const filteredOrders = computed(() =>
  orderFilter.value === "全部" ? localOrders.value : localOrders.value.filter((order) => order.status === orderFilter.value),
);
const designNotes: Record<PageKey, { title: string; text: string }[]> = {
  dashboard: [
    { title: "信息层级", text: "KPI 放在首屏最高权重区域，异常与趋势并列展示。" },
    { title: "颜色编码", text: "绿色正常、黄色预警、红色高危，降低报警搜索时间。" },
    { title: "视觉负荷", text: "只显示管理者最需要的实时指标，避免大屏信息过载。" },
  ],
  orders: [
    { title: "任务流", text: "按状态筛选工单，符合生产调度的顺序决策过程。" },
    { title: "可见反馈", text: "进度条与状态标签同时反馈工单执行情况。" },
    { title: "一致性", text: "表格行点击进入详情，保持所有列表页的操作一致。" },
  ],
  orderDispatch: [
    { title: "流程可视化", text: "工序节点从左到右排列，匹配用户的时序认知。" },
    { title: "动作闭环", text: "下发后状态变化并写入日志，形成结束信息。" },
    { title: "角色控制", text: "顶部角色影响日志身份，体现权限管理语义。" },
  ],
  equipment: [
    { title: "注意捕获", text: "设备卡片左侧状态色帮助维护员快速定位异常。" },
    { title: "空间分组", text: "设备状态与停机统计分区展示，减少跨区域记忆。" },
    { title: "视觉搜索", text: "设备编号、名称、产线固定顺序排列，便于扫视。" },
  ],
  equipmentDetail: [
    { title: "异常突出", text: "温度、振动、利用率用阈值色彩直接暴露风险。" },
    { title: "错误预防", text: "无报警设备禁用确认按钮，避免误操作。" },
    { title: "恢复说明", text: "确认报警后生成维护记录编号，给出明确反馈。" },
  ],
  quality: [
    { title: "数据编码", text: "合格率、DPPM、缺陷数用不同颜色区分质量风险。" },
    { title: "趋势认知", text: "不良率趋势帮助用户判断质量是否正在恶化。" },
    { title: "复杂数据简化", text: "质量数据先概览后分类，降低认知负担。" },
  ],
  spc: [
    { title: "控制边界", text: "SPC 柱形图突出接近控制线的数据点。" },
    { title: "告警优先级", text: "缺陷预警单独成区，避免被图表噪声淹没。" },
    { title: "专家视角", text: "CPK、UCL、LCL 面向质量工程师快速判断过程能力。" },
  ],
  traceability: [
    { title: "追溯链路", text: "批次、来源、工序、检验员按因果链展示。" },
    { title: "图文邻近", text: "追溯结果紧邻批次链，减少眼动距离。" },
    { title: "责任定位", text: "把缺陷、设备与人员关联，支持质量闭环。" },
  ],
  materials: [
    { title: "安全库存", text: "低库存行用红色边界提示，优先捕获注意。" },
    { title: "操作约束", text: "库存正常时禁用补货按钮，减少错误操作。" },
    { title: "物流决策", text: "库存、位置、补货动作在同一行完成判断。" },
  ],
  agv: [
    { title: "空间意象", text: "AGV 卡片模拟厂内物流节点，突出任务流向。" },
    { title: "状态反馈", text: "调度后任务、电量、日志同时变化，形成闭环。" },
    { title: "实时性", text: "运输中、待命、充电数量实时汇总。" },
  ],
  integration: [
    { title: "数据来源可见", text: "把 PLC、SCADA、ERP、WMS、QMS 分层展示，说明 MES 数据入口。" },
    { title: "异常前置", text: "延迟和告警数据用颜色编码，便于维护人员快速定位。" },
    { title: "接入闭环", text: "采集批次会驱动 KPI、设备、库存、质量和日志同步变化。" },
  ],
  permissions: [
    { title: "角色模型", text: "按生产、设备、质量、仓储角色组织权限。" },
    { title: "可理解性", text: "权限以短标签展示，避免复杂权限树造成负担。" },
    { title: "安全语义", text: "关键动作与当前角色绑定到日志中。" },
  ],
  logs: [
    { title: "审计追踪", text: "所有关键动作按时间倒序记录，支持答辩演示。" },
    { title: "风险编码", text: "警告与高危日志使用不同视觉强度。" },
    { title: "闭环验证", text: "日志证明工单、设备、物料、AGV 操作均有记录。" },
  ],
};
const currentDesignNotes = computed(() => designNotes[currentPage.value]);
const benchmarkPractices = [
  {
    source: "行业标杆",
    title: "生产执行与资源协同",
    text: "把订单、人员、设备、物料放在同一执行视图中，减少跨系统切换。",
  },
  {
    source: "行业标杆",
    title: "质量内嵌到工序",
    text: "质量不是事后报表，而是在工序节点中设置检查点和追溯链。",
  },
  {
    source: "行业标杆",
    title: "异常闭环",
    text: "报警确认后生成维护或质量记录，并进入日志审计。",
  },
  {
    source: "行业标杆",
    title: "电子作业指导",
    text: "面向操作员显示当前步骤、关键参数、确认项和防错提示。",
  },
];
const schedulePlan = [
  { line: "总装一线", window: "17:30-18:30", constraint: "高优先级 SUV 车门总成插单" },
  { line: "焊装二线", window: "18:30-19:10", constraint: "电池托盘尺寸复检后放行" },
  { line: "机加三线", window: "19:20-21:00", constraint: "等待高强钢板补货完成" },
];
const workInstructions = [
  { step: "01", instruction: "扫描工单与物料条码，校验车型配置。", check: "防错：物料批次必须匹配工单" },
  { step: "02", instruction: "按工艺参数完成装配或焊接。", check: "关键参数：扭矩/温度/节拍" },
  { step: "03", instruction: "完成首件检测并上传结果。", check: "质量门：异常时自动进入质检" },
];
const skillMatrix = computed(() => [
  { name: "设备点检授权", label: selectedRole.value.name, value: selectedRole.value.name === "设备维护员" ? 96 : 58 },
  { name: "质量判定授权", label: selectedRole.value.name, value: selectedRole.value.name === "质量工程师" ? 94 : 62 },
  { name: "物流调度授权", label: selectedRole.value.name, value: selectedRole.value.name === "仓储调度员" ? 91 : 54 },
]);
const maintenanceAdvice = computed(() => {
  if (selectedDevice.value.status === "danger") return "建议立即降速运行，检查扭矩传感器并复核最近 30 分钟质量数据。";
  if (selectedDevice.value.status === "warning") return "建议在下一个换型窗口执行点检，重点关注振动和温度趋势。";
  return "设备状态稳定，按常规点检周期维护。";
});

function currentTime() {
  return new Date().toLocaleTimeString("zh-CN", { hour12: false });
}

function addLog(user: string, action: string, level: SystemLog["level"] = "信息") {
  localLogs.value = [{ time: currentTime(), user, action, level }, ...localLogs.value].slice(0, 10);
}

function priorityCount(priority: WorkOrder["priority"]) {
  return localOrders.value.filter((order) => order.priority === priority).length;
}

function agvStatusCount(status: Agv["status"]) {
  return localAgvs.value.filter((agv) => agv.status === status).length;
}

function selectOrder(id: string, page?: PageKey) {
  selectedOrderId.value = id;
  if (page) currentPage.value = page;
}

function selectDevice(id: string, page?: PageKey) {
  selectedDeviceId.value = id;
  if (page) currentPage.value = page;
}

function dispatchSelectedOrder() {
  if (selectedOrder.value.status === "待下发") {
    localOrders.value = localOrders.value.map((order) =>
      order.id === selectedOrder.value.id ? { ...order, status: "生产中", progress: Math.max(order.progress, 18) } : order,
    );
    orderFeedback.value = `${selectedOrder.value.id} 已下发至 ${selectedOrder.value.line}，状态更新为生产中。`;
    addLog(selectedRole.value.name, `下发 ${selectedOrder.value.id} 至 ${selectedOrder.value.line}`);
    return;
  }

  orderFeedback.value = `${selectedOrder.value.id} 当前处于 ${selectedOrder.value.status}，可继续查看执行过程。`;
  addLog(selectedRole.value.name, `查看 ${selectedOrder.value.id} 执行状态`);
}

function ackEquipmentAlarm() {
  const recordId = `MR-${Date.now().toString().slice(-5)}`;
  equipmentFeedback.value = `${selectedDevice.value.name} 的报警已确认，维护记录编号 ${recordId}。`;
  localDevices.value = localDevices.value.map((device) =>
    device.id === selectedDevice.value.id
      ? { ...device, status: "warning", alarm: "维护处理中", utilization: Math.min(device.utilization, 72) }
      : device,
  );
  localAlerts.value = localAlerts.value.map((alert) =>
    alert.page === "equipmentDetail" ? { ...alert, acknowledged: true } : alert,
  );
  addLog(selectedRole.value.name, `确认 ${selectedDevice.value.name} 报警并生成 ${recordId}`, "警告");
}

function ackAlert(id: string) {
  localAlerts.value = localAlerts.value.map((alert) => (alert.id === id ? { ...alert, acknowledged: true } : alert));
  const alert = localAlerts.value.find((item) => item.id === id);
  addLog(selectedRole.value.name, `确认告警 ${alert?.title ?? id}`, alert?.level === "高" ? "警告" : "信息");
}

function jumpToAlert(page: PageKey) {
  currentPage.value = page;
}

function replenishMaterial(code: string) {
  const material = localMaterials.value.find((item) => item.code === code);
  if (!material) return;
  const targetStock = Math.ceil(material.safety * 1.35);
  localMaterials.value = localMaterials.value.map((item) =>
    item.code === code ? { ...item, stock: targetStock } : item,
  );
  localAlerts.value = localAlerts.value.map((alert) =>
    alert.page === "materials" ? { ...alert, acknowledged: true } : alert,
  );
  addLog(selectedRole.value.name, `为 ${material.name} 生成补货任务，目标库存 ${targetStock}${material.unit}`);
}

function dispatchAgv() {
  const selectedAgv = localAgvs.value.find((item) => item.id === selectedAgvId.value) ?? localAgvs.value[0];
  const task = "高强钢板补货 -> 冲压车间";
  localAgvs.value = localAgvs.value.map((agv) =>
    agv.id === selectedAgv.id ? { ...agv, task, status: "运输中", battery: Math.max(agv.battery - 8, 10) } : agv,
  );
  agvFeedback.value = `${selectedAgv.id} 已接收任务：${task}。`;
  addLog(selectedRole.value.name, `调度 ${selectedAgv.id} 执行 ${task}`);
}

function simulateBackendIngestion() {
  const now = currentTime();
  const weldingTemperature = Math.min(86, selectedDevice.value.temperature + 2);
  const nextOutput = factoryStats.value.output + 6;
  const steelMaterial = localMaterials.value.find((item) => item.code === "MAT-ST-001") ?? localMaterials.value[0];
  const nextSteelStock = Math.max(0, steelMaterial.stock - 2);
  const stockResult: IngestionEvent["result"] = nextSteelStock < steelMaterial.safety ? "告警" : "已入库";
  const batchEvents: IngestionEvent[] = [
    {
      time: now,
      source: "焊装 PLC",
      tag: "RB-WD-01.temperature",
      value: `${weldingTemperature}°C`,
      target: "设备监控",
      result: weldingTemperature > 80 ? "告警" : "已入库",
    },
    { time: now, source: "总装 SCADA", tag: "Line01.output", value: `${nextOutput}`, target: "总控看板", result: "已入库" },
    { time: now, source: "WMS 库存", tag: `${steelMaterial.code}.stock`, value: `${nextSteelStock}${steelMaterial.unit}`, target: "物料库存", result: stockResult },
    { time: now, source: "QMS 检验", tag: "BATCH-AUTO-260612-A.passRate", value: "98.8%", target: "质量追溯", result: "已入库" },
  ];

  localIngestionEvents.value = [...batchEvents, ...localIngestionEvents.value].slice(0, 12);
  localBackendSources.value = localBackendSources.value.map((source, index) => {
    const latency = Math.max(28, Math.round(source.latency + (index % 2 === 0 ? -6 : 9)));
    const lastValueMap: Record<string, string> = {
      "SRC-PLC-01": `RB-WD-01.temp=${weldingTemperature}`,
      "SRC-SCADA-02": `Line01.output=${nextOutput}`,
      "SRC-ERP-03": "WO-20260612-003.status=待下发",
      "SRC-WMS-04": `${steelMaterial.code}=${nextSteelStock}`,
      "SRC-QMS-05": "BATCH-A.passRate=98.8%",
    };
    return {
      ...source,
      latency,
      packets: source.packets + 4 + index,
      status: latency > 160 ? "延迟" : "在线",
      lastValue: lastValueMap[source.id] ?? source.lastValue,
    };
  });
  factoryStats.value = {
    output: nextOutput,
    oee: Math.min(96.5, factoryStats.value.oee + 0.1),
    completionRate: Math.min(99.9, factoryStats.value.completionRate + 0.1),
    energy: factoryStats.value.energy + 0.2,
    takt: factoryStats.value.takt,
  };
  localDevices.value = localDevices.value.map((device) =>
    device.id === "RB-WD-01"
      ? {
          ...device,
          temperature: weldingTemperature,
          vibration: Number(Math.min(4.8, device.vibration + 0.2).toFixed(1)),
          utilization: Math.min(98, device.utilization + 1),
          status: weldingTemperature > 80 ? "warning" : device.status,
          alarm: weldingTemperature > 80 ? "焊装温度接近预警阈值" : device.alarm,
        }
      : device,
  );
  localMaterials.value = localMaterials.value.map((material) =>
    material.code === steelMaterial.code ? { ...material, stock: nextSteelStock } : material,
  );
  localAlerts.value = localAlerts.value.map((alert) =>
    alert.page === "materials" && stockResult === "告警" ? { ...alert, acknowledged: false } : alert,
  );
  ingestionFeedback.value = `已采集 ${batchEvents.length} 条后端数据：产量、设备温度、库存和质量批次已写入 MES，并生成审计日志。`;
  addLog("数据接入网关", `完成一批后端数据采集，写入 ${batchEvents.length} 条业务数据`, stockResult === "告警" ? "警告" : "信息");
}

function simulateProductionCycle() {
  factoryStats.value = {
    output: factoryStats.value.output + 18,
    oee: Math.min(96.5, factoryStats.value.oee + 0.3),
    completionRate: Math.min(99.9, factoryStats.value.completionRate + 0.2),
    energy: factoryStats.value.energy + 0.4,
    takt: Math.max(52, factoryStats.value.takt - 1),
  };
  localOrders.value = localOrders.value.map((order) => {
    if (order.status !== "生产中" && order.status !== "质检中") return order;
    const nextProgress = Math.min(100, order.progress + 8);
    return {
      ...order,
      progress: nextProgress,
      status: nextProgress >= 100 ? "已完成" : order.status,
    };
  });
  localDevices.value = localDevices.value.map((device) =>
    device.status === "running"
      ? { ...device, utilization: Math.min(98, device.utilization + 1), temperature: Math.min(72, device.temperature + 1) }
      : device,
  );
  addLog("系统", `完成一轮生产推进，今日产量更新为 ${factoryStats.value.output.toLocaleString("zh-CN")} 辆/套`);
}

const Panel = defineComponent({
  props: {
    title: { type: String, required: true },
    wide: { type: Boolean, default: false },
  },
  setup(props, { slots }) {
    return () =>
      h("article", { class: ["panel", props.wide ? "wide" : ""] }, [
        h("header", { class: "panel-title" }, props.title),
        h("div", { class: "panel-body" }, slots.default?.()),
      ]);
  },
});

const ProgressBar = defineComponent({
  props: {
    value: { type: Number, required: true },
    label: { type: String, default: "" },
    large: { type: Boolean, default: false },
  },
  setup(props) {
    return () =>
      h("div", { class: ["progress-wrap", props.large ? "large" : ""] }, [
        props.label ? h("span", { class: "progress-label" }, props.label) : null,
        h("div", { class: "progress-track" }, [
          h("span", { style: { width: `${Math.max(0, Math.min(100, props.value))}%` } }),
        ]),
      ]);
  },
});

const StatusBadge = defineComponent({
  props: { label: { type: String, required: true } },
  setup(props) {
    const tone = computed(() =>
      /高危|异常|待下发/.test(props.label)
        ? "danger"
        : /预警|警告|质检|生产中/.test(props.label)
          ? "warn"
          : "good",
    );
    return () => h("span", { class: ["status-badge", tone.value] }, props.label);
  },
});

const StatusPill = defineComponent({
  props: {
    label: { type: String, required: true },
    value: { type: String, required: true },
    tone: { type: String, default: "info" },
  },
  setup(props) {
    return () =>
      h("div", { class: ["status-pill", props.tone] }, [h("span", props.label), h("strong", props.value)]);
  },
});

const MiniChart = defineComponent({
  props: {
    label: { type: String, required: true },
    values: { type: Array as PropType<number[]>, required: true },
    suffix: { type: String, default: "" },
  },
  setup(props) {
    const max = computed(() => Math.max(...props.values));
    return () =>
      h("div", { class: "mini-chart" }, [
        h("div", { class: "chart-head" }, [
          h("strong", props.label),
          h("span", `${props.values[props.values.length - 1]}${props.suffix}`),
        ]),
        h(
          "div",
          { class: "bars" },
          props.values.map((value) => h("span", { style: { height: `${(value / max.value) * 100}%` } })),
        ),
      ]);
  },
});

const AlertList = defineComponent({
  props: {
    items: {
      type: Array as PropType<{ id: string; title: string; page: PageKey; level: string; acknowledged: boolean }[]>,
      required: true,
    },
  },
  emits: ["jump", "ack"],
  setup(props, { emit }) {
    return () =>
      h(
        "div",
        { class: "alert-list" },
        props.items.map((alert) =>
          h("div", { class: ["alert-row", alert.acknowledged ? "ack" : ""] }, [
            h("button", { type: "button", onClick: () => emit("jump", alert.page) }, alert.title),
            h("span", `等级 ${alert.level}`),
            h(
              "button",
              { type: "button", disabled: alert.acknowledged, onClick: () => emit("ack", alert.id) },
              alert.acknowledged ? "已确认" : "确认",
            ),
          ]),
        ),
      );
  },
});
</script>
