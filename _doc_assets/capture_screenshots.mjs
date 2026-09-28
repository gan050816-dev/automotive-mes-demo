import http from "node:http";
import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const root = path.resolve("dist");
const outDir = path.resolve("_doc_assets/screenshots");
await fs.mkdir(outDir, { recursive: true });

const mime = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml",
  ".json": "application/json",
};

const server = http.createServer(async (req, res) => {
  try {
    const urlPath = decodeURIComponent(new URL(req.url || "/", "http://localhost").pathname);
    const rel = urlPath === "/" ? "index.html" : urlPath.slice(1);
    const file = path.join(root, rel);
    const data = await fs.readFile(file);
    res.writeHead(200, { "content-type": mime[path.extname(file)] || "application/octet-stream" });
    res.end(data);
  } catch {
    const data = await fs.readFile(path.join(root, "index.html"));
    res.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    res.end(data);
  }
});

await new Promise((resolve) => server.listen(1432, "127.0.0.1", resolve));

const browser = await chromium.launch({ channel: "msedge", headless: true });
const page = await browser.newPage({ viewport: { width: 1500, height: 960 }, deviceScaleFactor: 1 });
await page.goto("http://127.0.0.1:1432", { waitUntil: "domcontentloaded", timeout: 15000 });
await page.waitForSelector(".nav-item", { timeout: 10000 });

async function capture(text, file) {
  if (text) await page.getByText(text, { exact: true }).click();
  await page.waitForTimeout(250);
  await page.screenshot({ path: path.join(outDir, file), fullPage: false });
}

await capture(null, "01-dashboard.png");
await capture("工单工单总览", "02-orders.png");
await capture("设备设备详情/报警", "03-equipment-detail.png");
await capture("质量SPC/缺陷分析", "04-spc.png");
await capture("物料物料库存", "05-materials.png");
await capture("集成数据采集/接入", "06-integration.png");
await page.getByText("立即采集并写入 MES", { exact: true }).click();
await page.waitForTimeout(250);
await page.screenshot({ path: path.join(outDir, "07-integration-after-ingest.png"), fullPage: false });
await capture("权限操作日志/安全", "08-logs.png");

await browser.close();
await new Promise((resolve) => server.close(resolve));

console.log((await fs.readdir(outDir)).join("\n"));
