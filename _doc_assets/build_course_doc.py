from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image, ImageDraw, ImageFont


BASE = Path(__file__).resolve().parents[1]
ASSETS = BASE / "_doc_assets"
SCREENSHOTS = ASSETS / "screenshots"
OUT = BASE / "Carmessys汽车制造MES系统课程大作业_优化版.docx"


def font(size=28, bold=False):
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for item in candidates:
        if Path(item).exists():
            return ImageFont.truetype(item, size)
    return ImageFont.load_default()


def draw_center(draw, box, text, fill, fnt):
    x1, y1, x2, y2 = box
    lines = text.split("\n")
    heights = [draw.textbbox((0, 0), line, font=fnt)[3] for line in lines]
    total = sum(heights) + (len(lines) - 1) * 6
    y = y1 + ((y2 - y1) - total) / 2
    for line, h in zip(lines, heights):
        bbox = draw.textbbox((0, 0), line, font=fnt)
        x = x1 + ((x2 - x1) - (bbox[2] - bbox[0])) / 2
        draw.text((x, y), line, fill=fill, font=fnt)
        y += h + 6


def draw_box(draw, box, text, fill="F3F7FA", outline="2E74B5", text_fill="102A43", fnt=None):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=14, fill="#" + fill, outline="#" + outline, width=3)
    draw_center(draw, box, text, "#" + text_fill, fnt or font(28, True))


def draw_arrow(draw, start, end, color="5B6B7A"):
    draw.line([start, end], fill="#" + color, width=4)
    sx, sy = start
    ex, ey = end
    if ex > sx:
        points = [(ex, ey), (ex - 14, ey - 8), (ex - 14, ey + 8)]
    elif ex < sx:
        points = [(ex, ey), (ex + 14, ey - 8), (ex + 14, ey + 8)]
    else:
        points = [(ex, ey), (ex - 8, ey - 14), (ex + 8, ey - 14)]
    draw.polygon(points, fill="#" + color)


def create_diagrams():
    ASSETS.mkdir(exist_ok=True)
    title_font = font(34, True)
    node_font = font(24, True)
    small_font = font(20)

    img = Image.new("RGB", (1500, 850), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw.text((42, 32), "Carmessys MES 页面结构图", fill="#0B2545", font=title_font)
    levels = [
        ("总览层\n总控看板", 80, 150, 310, 270, "E8F4FA"),
        ("业务执行层\n工单 / 设备 / 质量 / 物料 / AGV", 420, 150, 830, 270, "F4F6F9"),
        ("数据集成层\nPLC / SCADA / ERP / WMS / QMS", 940, 150, 1350, 270, "EAF7EF"),
        ("安全审计层\n权限 / 日志 / 安全管理", 515, 500, 980, 620, "FFF7E6"),
    ]
    for text, x1, y1, x2, y2, fill in levels:
        draw_box(draw, (x1, y1, x2, y2), text, fill=fill, fnt=node_font)
    draw_arrow(draw, (310, 210), (420, 210))
    draw_arrow(draw, (830, 210), (940, 210))
    draw_arrow(draw, (625, 270), (625, 500))
    draw_arrow(draw, (1140, 270), (900, 500))
    draw.text((94, 330), "入口判断：生产状态是否正常", fill="#52616B", font=small_font)
    draw.text((454, 330), "业务处置：下发、确认、补货、调度、追溯", fill="#52616B", font=small_font)
    draw.text((964, 330), "后端信息流：采集、清洗、映射、告警", fill="#52616B", font=small_font)
    draw.text((554, 675), "所有关键动作写入日志，支撑责任追溯与安全审计", fill="#52616B", font=small_font)
    img.save(ASSETS / "page_structure.png")

    img = Image.new("RGB", (1500, 850), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw.text((42, 32), "Carmessys MES 功能结构与数据流图", fill="#0B2545", font=title_font)
    draw_box(draw, (70, 160, 300, 280), "ERP\n订单计划", fill="F4F6F9", fnt=node_font)
    draw_box(draw, (70, 340, 300, 460), "设备层\nPLC/SCADA", fill="F4F6F9", fnt=node_font)
    draw_box(draw, (70, 520, 300, 640), "WMS/QMS\n库存与质量", fill="F4F6F9", fnt=node_font)
    draw_box(draw, (520, 270, 920, 530), "MES 执行核心\n工单执行 / 设备监控\n质量追溯 / 物料物流\n数据采集 / 权限日志", fill="E8F4FA", fnt=node_font)
    draw_box(draw, (1150, 160, 1410, 280), "生产管理员\n总览决策", fill="EAF7EF", fnt=node_font)
    draw_box(draw, (1150, 340, 1410, 460), "维护/质量/仓储\n异常处置", fill="FFF7E6", fnt=node_font)
    draw_box(draw, (1150, 520, 1410, 640), "操作日志\n审计追溯", fill="FCEEEF", fnt=node_font)
    for y in [220, 400, 580]:
        draw_arrow(draw, (300, y), (520, 400))
    draw_arrow(draw, (920, 360), (1150, 220))
    draw_arrow(draw, (920, 400), (1150, 400))
    draw_arrow(draw, (920, 470), (1150, 580))
    draw.text((350, 675), "数据进入 MES 后被映射为业务对象，并通过角色化界面反馈给不同用户", fill="#52616B", font=small_font)
    img.save(ASSETS / "function_data_flow.png")


create_diagrams()


def set_run_font(run, east_asia="宋体", ascii_font="Times New Roman", size=10.5, bold=None, color=None):
    run.font.name = ascii_font
    run._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def set_para_format(p, first_line=True, before=0, after=0, line=1.25, align=None):
    fmt = p.paragraph_format
    fmt.first_line_indent = Pt(21) if first_line else None
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = line
    if align is not None:
        p.alignment = align


def add_p(doc, text="", first_line=True, bold=False):
    p = doc.add_paragraph()
    set_para_format(p, first_line=first_line, after=2)
    r = p.add_run(text)
    set_run_font(r, "宋体", size=10.5, bold=bold)
    return p


def add_h1(doc, text):
    p = doc.add_paragraph()
    set_para_format(p, first_line=False, before=10, after=6, line=1.25)
    r = p.add_run(text)
    set_run_font(r, "宋体", size=14, bold=True, color="000000")
    return p


def add_h2(doc, text):
    p = doc.add_paragraph()
    set_para_format(p, first_line=False, before=6, after=4, line=1.25)
    r = p.add_run(text)
    set_run_font(r, "楷体", size=12, bold=False, color="000000")
    return p


def add_caption(doc, text, above=False):
    p = doc.add_paragraph()
    set_para_format(p, first_line=False, before=4 if above else 2, after=4 if above else 8, line=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run(text)
    set_run_font(r, "楷体", size=10.5)
    return p


def set_cell_text(cell, text, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    set_para_format(p, first_line=False, line=1.15)
    r = p.add_run(text)
    set_run_font(r, "宋体", size=10.5, bold=bold)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def table_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for name in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        edge = OxmlElement(f"w:{name}")
        edge.set(qn("w:val"), "single")
        edge.set(qn("w:sz"), "4")
        edge.set(qn("w:space"), "0")
        edge.set(qn("w:color"), "BFBFBF")
        borders.append(edge)
    tbl_pr.append(borders)


def add_table(doc, caption, headers, rows, widths_cm):
    add_caption(doc, caption, above=True)
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table_borders(table)
    for i, h in enumerate(headers):
        table.columns[i].width = Cm(widths_cm[i])
        set_cell_text(table.rows[0].cells[i], h, bold=True)
        shade_cell(table.rows[0].cells[i], "F2F4F7")
    for row in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            set_cell_text(cells[i], str(val), align=WD_ALIGN_PARAGRAPH.LEFT if i > 0 else WD_ALIGN_PARAGRAPH.CENTER)
            cells[i].width = Cm(widths_cm[i])
    doc.add_paragraph()
    return table


def add_figure(doc, image_name, caption):
    image_path = SCREENSHOTS / image_name
    if not image_path.exists():
        image_path = ASSETS / image_name
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run()
    r.add_picture(str(image_path), width=Cm(15.5))
    add_caption(doc, caption)


def add_cover(doc):
    for _ in range(3):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("《智能制造人机交互》")
    set_run_font(r, "隶书", size=22, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("课程大作业")
    set_run_font(r, "隶书", size=22, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("（2025-2026（2）学期）")
    set_run_font(r, "楷体", size=12)
    for _ in range(4):
        doc.add_paragraph()
    for line in [
        "题    目：基于汽车制造场景的 Carmessys MES 系统人机交互界面设计",
        "学    院：工程学院",
        "小组成员：班级：__________ 姓名：__________ 学号：__________",
        "小组成员：班级：__________ 姓名：__________ 学号：__________",
        "小组成员：班级：__________ 姓名：__________ 学号：__________",
        "小组成员：班级：__________ 姓名：__________ 学号：__________",
        "课程教师：陈成明",
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_para_format(p, first_line=False, after=10, line=1.25)
        r = p.add_run(line)
        set_run_font(r, "楷体", size=10.5)
    for _ in range(2):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("2026 年 05 月")
    set_run_font(r, "楷体", size=10.5)
    doc.add_page_break()


doc = Document()
section = doc.sections[0]
section.top_margin = Cm(2.54)
section.bottom_margin = Cm(2.54)
section.left_margin = Cm(2.54)
section.right_margin = Cm(2.54)
section.header_distance = Cm(1.25)
section.footer_distance = Cm(1.25)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Times New Roman"
normal._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
normal.font.size = Pt(10.5)

footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = footer.add_run("2026 春《智能制造人机交互》课程大作业")
set_run_font(fr, "宋体", size=9)

add_cover(doc)

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = title.add_run("基于汽车制造场景的 Carmessys MES 系统人机交互界面设计")
set_run_font(tr, "隶书", size=22, bold=True)
meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
mr = meta.add_run("班级：__________    姓名：__________    学号：__________")
set_run_font(mr, "楷体", size=10.5)

add_h1(doc, "摘要")
add_p(doc, "本课程大作业以汽车制造企业为背景，围绕制造执行系统 MES 在生产现场中的信息采集、工单执行、设备监控、质量追溯、物料物流、权限日志等场景，设计并实现了一个可运行的仿真 MES 前端系统 Carmessys。系统采用 Vue、TypeScript 与 Vite 构建，并参照原有 PCB 项目的打开逻辑补充了 Tauri 桌面壳思路，使其既可以通过浏览器运行，也可以作为后续桌面打包的基础。MES 的定位参考了制造执行系统与企业控制集成相关标准和经典 MES 研究[8][9][10]。")
add_p(doc, "本文不仅展示界面结果，更强调“为什么这样设计”。整体思路是先从汽车制造流程与用户角色出发，分析生产管理员、设备维护员、质量工程师、仓储调度员等角色的信息需求，再将课程第三章的人机交互设计原则和第四章的视觉认知规律转化为界面方案[1]。系统中左侧导航、顶部状态栏、KPI 卡片、颜色编码、告警优先级、交互反馈、操作日志等设计，均服务于降低认知负荷、提高视觉搜索效率和保障工业现场操作安全[2][5][12]。")
add_p(doc, "关键词：智能制造；MES；人机交互；视觉认知；信息编码；汽车制造")

add_h1(doc, "一、整体思考逻辑")
add_p(doc, "本项目的整体思考逻辑可以概括为“场景先行、角色驱动、信息分层、交互闭环、理论点题”。首先，课程要求强调基于真实或虚拟制造企业场景进行设计，因此本组没有继续沿用文件夹名中的 PCB 场景，而是将新系统统一为汽车制造 MES 系统，避免项目主题与界面内容冲突。汽车制造具有工序长、设备多、质量追溯要求高、物流协同复杂等特点，适合体现 MES 对人、机、物、法、环、测等信息的综合组织能力。")
add_p(doc, "其次，MES 不是单纯的数据展示页面，而是面向不同岗位的执行系统。生产管理员关注产量、OEE、工单进度和订单完成率；设备维护员关注设备状态、温度振动、停机统计与报警处置；质量工程师关注 SPC、缺陷分析、批次追溯与质量门；仓储调度员关注库存、安全线、AGV 状态与物流任务；系统管理员关注角色权限、操作日志与安全审计。基于这些角色，本系统设置了总控看板、工单管理、设备监控、质量管理、物料物流、数据接入、权限日志等模块。")
add_p(doc, "再次，界面设计遵循“宏观到微观”的信息路径。总控看板承担第一层信息聚合，帮助管理人员快速判断现场是否正常；各子模块承担第二层业务定位，如工单、设备、质量、物料等；详情页承担第三层处置动作，如工单下发、设备报警确认、物料补货、AGV 调度、数据采集写入等。这种结构对应课程中“信息层级设计”和“工业信息布局原则”，让用户不用在多个界面之间记忆大量信息，而是通过固定导航和任务路径逐步深入。")
add_p(doc, "最后，系统中的交互并非静态展示。点击“推进一轮生产”会模拟产量、OEE、能耗、工单进度和设备利用率变化；点击“采集一批数据”会模拟 PLC、SCADA、ERP、WMS、QMS 后端数据进入 MES，并联动更新看板、设备、库存、质量与日志；工单下发、报警确认、补货、AGV 调度也都会写入操作日志。这种设计体现了课程中“提供信息反馈”“设计结束信息”“预防错误”和“支持内部控制点”的黄金规则[1][2]。")

add_h1(doc, "二、企业背景与生产流程分析")
add_h2(doc, "2.1 企业类型与业务场景")
add_p(doc, "本项目设定的企业为一家中型汽车零部件与整车装配协同制造企业，主要生产车身焊装件、车门总成、电池托盘、内饰装配件以及整车装配相关零部件。企业现场包含冲压、焊装、机加、涂装前处理、总装、质量检测、仓储物流等环节。生产过程具有批量化、多车型、多订单、多设备协同的特点，现场数据来源复杂，包括 PLC、SCADA、设备传感器、ERP 订单、WMS 库存、QMS 检验结果以及 AGV 物流任务。")
add_p(doc, "在传统制造模式下，生产计划、设备状态、质量检测和物料配送往往分散在不同系统中，现场人员需要频繁切换系统或依赖人工沟通，容易出现信息滞后、异常响应慢、责任追溯困难等问题。MES 位于 ERP 与车间控制层之间，其价值在于把计划、执行、设备、质量、物料和人员信息统一到生产现场的执行视图中，使管理人员能够实时掌握生产状态，使一线人员能够按照工单和作业指导完成任务[8][9]。")
add_h2(doc, "2.2 生产流程与 MES 作用")
add_p(doc, "汽车制造场景中的典型流程可描述为：ERP 下达订单计划，MES 根据产线能力和物料状态形成工单；工单下发到对应产线后，操作员按照电子作业指导 eSOP 执行扫描、装配、焊接或检测；设备侧通过 PLC、SCADA 和传感器上传温度、振动、利用率等数据；质量模块记录首件检验、过程检验、SPC 数据和缺陷信息；WMS 与 AGV 系统根据工单需求完成物料配送；所有关键动作进入操作日志，用于后续追溯和审计。")
add_p(doc, "MES 在该流程中的核心作用有四点：第一，执行连接，即把 ERP 的计划转化为可执行的工单和工序；第二，状态透明，即将设备、工单、物料、质量等数据实时展示给不同角色；第三，异常闭环，即把报警、缺料、质量波动等异常转化为可处置任务；第四，追溯审计，即把批次、设备、人员、时间和动作形成可查询的链路。")

add_table(doc, "表1  汽车制造 MES 场景中的用户角色与核心需求", ["角色", "核心关注", "界面需求"], [
    ["生产管理员", "产量、OEE、工单进度、订单完成率", "总控看板、工单筛选、进度追踪、异常总览"],
    ["设备维护员", "设备状态、报警、温度振动、停机统计", "设备卡片、详情页、报警确认、维护建议"],
    ["质量工程师", "SPC、缺陷趋势、批次追溯、检验记录", "质量总览、缺陷分析、正反向追溯"],
    ["仓储调度员", "库存安全线、AGV 任务、物料流向", "库存预警、补货按钮、AGV 状态图"],
    ["系统管理员", "权限、日志、安全审计", "角色切换、权限标签、操作日志、安全状态"],
], [2.6, 4.2, 8.5])

add_h1(doc, "三、用户需求分析")
add_h2(doc, "3.1 操作员与生产管理员需求")
add_p(doc, "操作员与生产管理员的共同特点是任务时间紧、现场干扰多、需要快速判断当前生产状态。生产管理员希望在进入系统后第一眼看到今日产量、OEE、订单完成率、能耗和待处理报警，进而判断生产节奏是否正常。操作员更关注当前工单是否已经下发、工序是否完成、下一步应该做什么，以及操作是否成功。因此系统把总控 KPI 放在首屏顶部，工单列表提供状态筛选和进度条，工单详情页以横向工序流展示工艺步骤，并在下发后给出明确文字反馈。")
add_h2(doc, "3.2 设备维护与质量管理需求")
add_p(doc, "设备维护员面对的是高频实时数据和低频高风险事件。温度、振动、利用率等数据需要长期监控，但真正需要立刻处理的是高危报警。因此设备页面采用卡片左侧状态色和详情页阈值色彩，将正常、预警、高危区分开。质量工程师需要从宏观合格率进入具体缺陷和批次追溯，系统在质量总览中提供合格率、DPPM 和不良率趋势，在 SPC 页面展示过程能力与缺陷预警，在追溯页面展示批次、来源、工序、检验员和缺陷结果。")
add_h2(doc, "3.3 信息交互与安全需求")
add_p(doc, "工业系统的交互需求不仅是“能点”，还要保证“点得对、点后有反馈、出错能恢复”。因此系统对库存正常的物料禁用补货按钮，对无报警设备禁用报警确认按钮，对关键动作写入操作日志，并通过当前角色反映责任主体。数据接入页模拟后端网关，将 PLC、SCADA、ERP、WMS、QMS 的数据映射到 MES 业务对象，说明工业现场的信息流不是孤立页面，而是由多个系统协同形成的实时闭环。")

add_h1(doc, "四、人机交互理论分析与 PPT 知识点点题")
add_h2(doc, "4.1 八条黄金规则在系统中的应用")
add_p(doc, "课程第三章提出人机交互界面设计的八条黄金规则，包括保持一致性、满足普遍可用性、提供信息反馈、设计对话框以产生结束信息、预防错误、允许动作回退、支持内部控制点、减轻记忆负担[1][2][4]。本系统首先在导航、卡片、状态标签、按钮和日志样式上保持一致，用户在不同模块中都能用相似方式完成“查看列表-进入详情-执行动作-获得反馈”的操作。其次，系统在工单下发、报警确认、补货、AGV 调度、数据采集后都提供即时反馈，并写入日志，形成结束信息。")
add_p(doc, "预防错误方面，系统通过禁用按钮、颜色阈值和状态提示减少误操作。例如库存正常时补货按钮显示“库存正常”并禁用；无报警设备无法确认报警；设备温度或振动超过阈值时用预警色提示。减轻记忆负担方面，页面顶部始终显示当前页面名称和课程理论提示，左侧导航保持固定，用户不需要记住每个模块的位置和功能。支持内部控制点方面，用户可以主动切换角色、筛选工单、选择设备、选择批次，并通过按钮触发业务变化，而不是被系统单向展示。")
add_h2(doc, "4.2 工业信息布局原则")
add_p(doc, "PPT 中强调工业信息布局应遵循重要性排序、功能分组、任务时序、空间协调和信息层级可视化[1]。本系统采用左侧导航、右侧内容的左右型布局，适合 MES 这种模块多、层级复杂、需要频繁切换的工业管理系统。总控看板把最重要的 KPI 放在首屏上方，符合“权重决定位置”的原则；工单、设备、质量、物料等模块按业务类别分组，符合格式塔心理学中的接近原则；工单详情页从左到右展示工序流，符合任务时序和用户阅读动线[5]。")
add_p(doc, "在视觉层级上，系统使用大号数字显示 KPI，使用面板标题组织模块，使用进度条表示执行程度，使用状态标签表示对象状态。这样既能支持自上而下的任务驱动搜索，也能利用自下而上的颜色、大小、对比等特征捕获注意。课程中提到 F 型和 Z 型视觉浏览模式，本系统在总控看板中采用上方 KPI、下方趋势与告警的结构，使用户先看到总览，再向下扫描异常和明细。")
add_h2(doc, "4.3 动效、反馈与工业克制性")
add_p(doc, "PPT 中指出工业信息动效应服务于信息，而非炫技，强调克制性、一致性和目的性。本系统没有使用大量装饰性动画，而是用状态变化、按钮反馈、进度变化和日志新增来表现动态。点击“推进一轮生产”后，产量、OEE、能耗、工单进度和设备利用率发生变化；点击“采集一批数据”后，接入记录数量增加，设备、库存和日志同步变化。这种动态反馈让用户感知系统状态变化，同时避免过多动画造成干扰。")
add_h2(doc, "4.4 图符与视觉语义")
add_p(doc, "虽然当前系统主要以文字、状态色和卡片为主，没有大量使用图符，但仍然遵循图符设计中的语义清晰原则。MES 系统面向工业现场，过度复杂或娱乐化图标反而会增加识别成本，因此界面使用 MES 标识、状态圆点、进度条、标签和卡片边界来表达语义。后续若进一步完善，可加入统一的设备图标、AGV 图标、告警图标和权限图标，并保持尺寸、线条和颜色规范一致。")
add_h2(doc, "4.5 数据编码与视觉认知")
add_p(doc, "PPT 中数据编码部分强调颜色、位置、大小、形状、字体等视觉通道应与数据含义匹配。本系统采用交通灯式颜色编码：绿色代表正常，黄色代表预警，红色代表高危或告警，蓝色用于普通信息或在线状态。KPI 数值使用大字号和粗体，单位与说明使用较小字号，体现字体编码。趋势图和柱形图用长度编码表示 OEE、产量、不良率和 SPC 数据，进度条用长度表示工单进度、设备利用率和库存比例。")
add_p(doc, "课程第四章强调视觉搜索、注意捕获、认知负荷和知觉负载[1]。MES 现场信息密度高，如果所有信息都同等呈现，用户只能进行低效的系列搜索。本系统通过颜色、大小、分区和状态标签提高目标显著性，让异常信息能被平行搜索快速发现。例如高危设备卡片左侧红色边界、低库存行红色边界、告警列表单独成区，都是为了让用户在复杂界面中快速定位目标[5][12]。")

add_table(doc, "表2  课程知识点与 Carmessys 系统设计对应关系", ["课程知识点", "系统体现", "设计目的"], [
    ["保持一致性", "统一左侧导航、状态标签、面板样式、按钮反馈", "降低学习成本，形成稳定心理模型"],
    ["信息反馈", "工单下发、采集、补货、报警确认均即时反馈", "让用户明确动作是否成功"],
    ["布局层级", "总控 KPI 置顶，业务模块分区，详情页逐级深入", "减少搜索路径和认知负荷"],
    ["颜色编码", "绿/黄/红表示正常、预警、高危", "提高异常识别效率"],
    ["视觉搜索", "告警、低库存、高危设备突出显示", "支持快速定位关键目标"],
    ["注意捕获", "状态色、进度条、KPI 大字号", "让重要信息优先进入视野"],
    ["动效克制", "用数据变化和日志新增替代装饰动画", "避免工业现场误操作"],
    ["错误预防", "禁用无效按钮，按阈值提示风险", "减少错误操作和安全风险"],
], [3.2, 6.0, 5.9])

add_h1(doc, "五、信息架构设计")
add_p(doc, "Carmessys 的信息架构围绕 MES 的执行逻辑展开，整体分为总览层、业务执行层、数据集成层和安全审计层。总览层是总控看板，展示生产状态、设备状态、OEE、报警、订单完成率、能耗和关键 KPI；业务执行层包含工单、设备、质量、物料和 AGV；数据集成层模拟 PLC、SCADA、ERP、WMS、QMS 数据接入；安全审计层包含人员权限和操作日志。")
add_figure(doc, "page_structure.png", "图1  Carmessys MES 页面结构图")
add_table(doc, "表3  系统页面结构与功能说明", ["层级", "页面", "主要功能"], [
    ["总览层", "总控看板", "展示产量、OEE、订单完成率、能耗、报警和趋势"],
    ["工单层", "工单总览、工单详情/下发", "工单筛选、优先级、工序流、下发反馈"],
    ["设备层", "设备监控、设备详情/报警", "设备状态、参数、报警确认、维护建议"],
    ["质量层", "质量总览、SPC/缺陷分析、质量追溯", "合格率、不良率、SPC、批次链路"],
    ["物流层", "物料库存、AGV/物流追踪", "库存安全线、补货、AGV 任务和电量"],
    ["集成层", "数据采集/接入", "模拟 PLC/SCADA/ERP/WMS/QMS 数据写入 MES"],
    ["安全层", "人员权限、操作日志/安全", "角色权限、操作记录、安全审计"],
], [2.2, 4.4, 8.5])
add_p(doc, "该结构满足课程要求中的“1 个总控大屏、5 个以上子模块页面、页面跳转逻辑、完整交互流程”。目前系统页面数量已经达到 13 个，超过建议不少于 12 页的要求。")
add_figure(doc, "function_data_flow.png", "图2  Carmessys MES 功能结构与数据流图")
add_h1(doc, "六、界面设计展示与说明")
add_h2(doc, "6.1 总控看板")
add_p(doc, "总控看板是生产管理人员进入系统后的第一视图，承担态势感知功能。页面上方以 KPI 卡片展示今日产量、OEE、订单完成率、能耗和报警数量；中部展示 OEE 与产量趋势；右侧和下方展示设备状态、告警优先级和行业 MES 能力映射。该页面的设计逻辑是先让用户判断“是否正常”，再定位“哪里异常”，最后进入具体模块处理。")
add_figure(doc, "01-dashboard.png", "图3  Carmessys MES 总控看板监控截图")
add_h2(doc, "6.2 工单管理")
add_p(doc, "工单总览页面提供按状态筛选、工单进度展示和优先级统计。用户点击工单后进入详情页，可以查看工序流和电子作业指导 eSOP，并对待下发工单执行下发操作。该设计体现任务时序和操作流程逻辑，避免用户在多个页面之间记忆工单状态。")
add_figure(doc, "02-orders.png", "图4  工单总览与工单状态查询截图")
add_h2(doc, "6.3 设备监控与报警处理")
add_p(doc, "设备模块采用卡片式展示设备编号、名称、产线和利用率，用状态色突出运行、预警和高危。设备详情页显示温度、振动、利用率和报警说明，并提供报警确认按钮。报警确认后生成维护记录并写入日志，体现异常闭环。")
add_figure(doc, "03-equipment-detail.png", "图5  设备详情与报警处理截图")
add_h2(doc, "6.4 质量管理与 SPC")
add_p(doc, "质量模块分为质量总览、SPC/缺陷分析和质量追溯。SPC 页面以柱状图表达过程数据，以 CPK、UCL、LCL 指标辅助质量工程师判断过程能力；缺陷预警单独成区，避免被图表信息淹没。追溯页面通过批次、来源、工序、检验员和缺陷结果建立责任链路。")
add_figure(doc, "04-spc.png", "图6  SPC 与缺陷分析监控截图")
add_h2(doc, "6.5 物料库存与物流追踪")
add_p(doc, "物料库存页面展示物料编号、名称、位置、库存与安全线，并对低库存行进行红色边界提示。当库存低于安全线时，用户可以生成补货任务。AGV 页面展示车辆任务、电量和状态，支持调度选中 AGV 执行紧急补货任务。该模块体现工业物流信息的实时交互设计。")
add_figure(doc, "05-materials.png", "图7  物料库存与缺料预警截图")
add_h2(doc, "6.6 后端信息采集与接入")
add_p(doc, "数据采集/接入页面是本项目后续完善的重要部分。页面展示焊装 PLC、总装 SCADA、ERP 订单、WMS 库存、QMS 检验五类数据源，并标注协议、延迟、包数和最近值。采集流程分为边缘采集、清洗校验、业务映射、告警闭环四步。点击采集后，系统会模拟一批后端数据写入 MES，并联动总控、设备、库存、质量和日志。")
add_figure(doc, "06-integration.png", "图8  后端数据源连接状态与采集流水线截图")
add_figure(doc, "07-integration-after-ingest.png", "图9  模拟采集后数据写入 MES 的反馈截图")
add_h2(doc, "6.7 权限与操作日志")
add_p(doc, "权限与日志模块体现工业系统的安全性和可追踪性。用户角色包括生产管理员、设备维护员、质量工程师、仓储调度员等，每个角色拥有不同权限标签。系统所有关键动作都会进入操作日志，例如工单下发、报警确认、补货、AGV 调度和数据采集。日志按时间倒序排列，并用不同状态区分信息、警告和高危事件。")
add_figure(doc, "08-logs.png", "图10  操作日志与安全管理截图")

add_h1(doc, "七、系统实现与仿真数据说明")
add_p(doc, "系统采用 Vue + TypeScript + Vite 实现，集中 mock 数据存放在 mockData.ts 中，包括工单、设备、质量批次、物料、AGV、人员权限、操作日志、后端数据源和采集事件。这样做的好处是便于课程演示和后续文档撰写：所有页面都围绕同一套业务数据变化，避免静态截图之间互相矛盾。")
add_p(doc, "仿真交互主要包括六类：第一，工单筛选和下发；第二，设备报警确认；第三，质量批次追溯；第四，物料补货和库存预警；第五，AGV 调度；第六，后端数据采集写入。每类交互都会改变页面状态，并在日志中留下记录。虽然当前系统未连接真实数据库和真实设备，但数据流逻辑已经模拟了 MES 与设备层、计划层、物流层和质量层之间的信息接入关系。")
add_p(doc, "本项目还保留了与原 PCB 项目类似的打开逻辑：前端通过 Vite 启动，桌面壳可通过 Tauri 思路扩展。由于当前电脑 Rust/Cargo 与 Visual Studio Build Tools 环境不完整，Tauri 打包成 exe 还需要补齐本机环境；但浏览器运行和前端构建已经验证通过。")

add_h1(doc, "八、总结与反思")
add_h2(doc, "8.1 设计亮点")
add_p(doc, "本项目的第一个亮点是场景统一。系统从文件夹名可能带来的 PCB 场景转向汽车制造场景，并在工单、设备、质量、物料和物流中保持汽车制造语义，使项目主题更加清晰。第二个亮点是页面完整。系统包含总控看板、工单、设备、质量、物料、AGV、数据接入、权限日志等 13 个页面，满足课程建议不少于 12 页的要求。第三个亮点是交互闭环。系统不仅展示数据，还模拟业务动作引起的状态变化，并通过日志形成审计记录。")
add_h2(doc, "8.2 存在问题")
add_p(doc, "当前系统仍属于前端仿真模型，尚未连接真实数据库、真实设备接口和真实登录权限。因此数据变化是基于 mock 逻辑生成的，无法代表真实产线运行结果。其次，图符体系还可以进一步完善，例如为设备、AGV、报警、质量缺陷等对象设计统一图标。再次，系统目前主要面向桌面大屏，移动端适配不是重点，后续若面向现场平板使用，需要重新考虑响应式布局和触控尺寸。")
add_h2(doc, "8.3 对智能制造人机交互的理解")
add_p(doc, "通过本次设计可以看出，智能制造人机交互不是把数据堆到屏幕上，也不是把界面做得越炫越好。工业界面的核心是效率、安全、清晰和抗干扰。优秀的 MES 界面需要理解生产流程、用户角色和信息优先级，再利用布局、颜色、字体、图表、反馈和日志等手段，把复杂工业数据转化为可理解、可操作、可追溯的信息。课程第三章提供了界面设计原则，第四章解释了视觉认知背后的原因，两者结合后，才能让系统既满足功能，又符合人的认知规律。")

add_h1(doc, "九、打开与演示教程")
add_h2(doc, "9.1 浏览器方式启动")
add_p(doc, "第一步，确认电脑已经安装 Node.js。第二步，打开 PowerShell，进入项目目录：")
add_p(doc, r"cd <项目目录>", first_line=False)
add_p(doc, "第三步，首次运行时安装依赖：", first_line=False)
add_p(doc, "npm.cmd install", first_line=False)
add_p(doc, "第四步，启动开发服务器：", first_line=False)
add_p(doc, "npm.cmd run dev", first_line=False)
add_p(doc, "第五步，浏览器打开终端显示的地址，默认通常为 http://127.0.0.1:1421。注意：在 PowerShell 环境中建议使用 npm.cmd，而不是 npm run dev，以避免脚本执行策略拦截。")
add_h2(doc, "9.2 双击脚本方式启动")
add_p(doc, r"如果把整个项目文件夹交给其他同学或老师，并且对方电脑已经安装 Node.js，可以直接双击项目根目录中的 start-carmessys.bat。脚本会自动进入项目目录，缺少 node_modules 时先执行 npm.cmd install，然后启动开发服务并打开浏览器。")
add_h2(doc, "9.3 构建检查与桌面打包说明")
add_p(doc, "若只检查项目能否成功打包前端，可运行：", first_line=False)
add_p(doc, r"cd <项目目录>", first_line=False)
add_p(doc, "npm.cmd run build", first_line=False)
add_p(doc, "如果需要像原 PCB 项目一样打包为 Windows 桌面程序，可在本机安装 Rust/Cargo、Visual Studio Build Tools 和 WebView2 后运行 npm.cmd run tauri build。当前系统已经保留 Tauri 配置，但在本机打包 exe 需要先补齐 Cargo 与 MSVC/Windows SDK 环境。")

add_h1(doc, "参考文献")
refs = [
    "陈成明. 智能制造人机交互课程第三、四章教学课件：智能制造系统的人机交互设计原则与视觉认知原理及相关实验范式. 2026.",
    "Ben Shneiderman, Catherine Plaisant, Maxine Cohen, Steven Jacobs, Niklas Elmqvist, Nicholas Diakopoulos. Designing the User Interface: Strategies for Effective Human-Computer Interaction. Pearson, 2016.",
    "Donald A. Norman. The Design of Everyday Things. Basic Books, 2013.",
    "Jakob Nielsen. Usability Engineering. Morgan Kaufmann, 1993.",
    "Colin Ware. Information Visualization: Perception for Design. Morgan Kaufmann, 2019.",
    "ISO 9241-210. Ergonomics of human-system interaction - Human-centred design for interactive systems.",
    "ISO 9241-112. Ergonomics of human-system interaction - Principles for the presentation of information.",
    "ANSI/ISA-95. Enterprise-Control System Integration standard series.",
    "IEC 62264. Enterprise-control system integration standard series.",
    "Michael McClellan. Applying Manufacturing Execution Systems. St. Lucie Press, 1997.",
    "Thomas H. Davenport. Process Innovation: Reengineering Work through Information Technology. Harvard Business School Press, 1993.",
    "Wickens C. D., Lee J. D., Liu Y., Gordon Becker S. An Introduction to Human Factors Engineering. Pearson, 2004.",
]
for i, ref in enumerate(refs, 1):
    p = doc.add_paragraph()
    set_para_format(p, first_line=False, after=3, line=1.15)
    r = p.add_run(f"[{i}] {ref}")
    set_run_font(r, "宋体", size=10.5)

add_h1(doc, "附录：小组分工")
add_table(doc, "表5  小组成员分工记录", ["姓名", "学号", "具体工作内容"], [
    ["__________", "__________", "企业背景分析、需求分析、资料整理"],
    ["__________", "__________", "MES 界面设计、页面交互实现、截图整理"],
    ["__________", "__________", "人机交互理论分析、Word 文档撰写"],
    ["__________", "__________", "PPT 汇报制作、演示测试与答辩准备"],
], [3.2, 3.2, 9.0])

doc.save(OUT)
print(OUT)
