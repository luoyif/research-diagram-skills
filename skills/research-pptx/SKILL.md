---
name: research-pptx
description: PPT科研原生绘图；从参考图、SVG、手绘草图或文字需求建立原生可编辑图，保留文字与连接语义，采用两级字号、原生分组、逐格式实际渲染与视觉复核；不是生图服务。
license: MIT; upstream sources retain their own licenses
compatibility: Python 3.10+. PPT needs python-pptx; previews need draw.io Desktop or LibreOffice plus pdftoppm. Image interpretation needs a vision-capable agent.
metadata:
  author: "小罗"
  version: "1.0.0"
---

# PPT科研原生绘图

默认后端pptx，用户选择优先。Draw.io维护结构连接，PPT办公编辑，both双格式。三入口可独立安装。不要调用生图工具替代原生绘图，不将整页截图嵌入PPT冒充可编辑。

先读 references/WORKFLOW.md、references/SCENE.md、references/QA.md、references/SOURCES.md。

## 步骤
1. 确认已有参考图/区域、允许的修改、后端、字体/两级字号、印刷宽度、作者和输出目录。默认黑白灰、已安装宋体配置、作者“小罗”；原图好的布局不擅自极简化。
2. 有图先用intake.py归档。视觉逐项记录元素、原文、分区、图标和箭头方向；模糊文字与未决关系不得补造。没有图则依用户文字建立清单。
3. 写Scene，冻结原文与关系合同。复杂元素用上游专项原生流程并明确限制，不静默丢弃。不能靠重新freeze掩盖误删。
4. 父子分组、背景在下、子卡片在上。端点绑定，独立输入分配端口，反馈绕外侧，预留箭头末段。固定两级字号，用调框和换行解决拥挤。
5. validate → build → 每种实际输出分别render。缺少工具时保留PENDING，不上传云服务、不用SVG图代替PPT预览。
6. 真正查看全部实际预览，对照原图逐框/逐箭头核对。修复后新pass重导出。只有自检就如实写自检，不虚构独立审查。
7. review只记录真实检查声明。交付源文件、SVG、PNG、字体说明和限制。用户要Mac时通过Remote写入指定Mac并核验；不要把容器文件说成已到Mac。不得修改无关Word。

## 命令（在本Skill根目录）
```bash
python scripts/diagram.py doctor
python scripts/intake.py /path/reference.png --out /path/intake-01
# 视觉阅读后编写Scene；示例可直接运行
python scripts/diagram.py validate assets/reference-reconstruction.scene.json
python scripts/diagram.py freeze assets/reference-reconstruction.scene.json /path/content.contract.json
python scripts/diagram.py build assets/reference-reconstruction.scene.json --mode pptx --contract /path/content.contract.json --out /path/pass-01
python scripts/diagram.py render /path/pass-01 --mode pptx --width 6400
# 实际查看预览后再记录，不预填虚假PASS
python scripts/diagram.py review /path/pass-01 --reviewer 小罗 --verdict PASS --notes "填写真实检查所看的文件、文字/箭头关系、发现与修复内容。"
```

已有受支持的未压缩Draw.io：
```bash
python scripts/from_drawio.py input.drawio --page 0 --out /path/imported.scene.json
```

目标目录必须新建。仅修改新pass，不覆盖原参考。上游快照原样保留；这些research-*入口是本项目集成，不是厂商认证。高级上游脚本按需审阅，不自动运行全部程序。

## 上游专项路线（不是仅保留链接）

以下为已锁定快照中的真实文件。独立包路径从Skill根目录起；在仓库中开发时，上游在仓库根vendor/。优先读取对应上游SKILL.md及它指向的任务相关参考，不一次塞入所有源码。


- 科研PPT原生重建：`vendor/HututuWorks__sci-diagram-pptx/skills/sci-diagram-pptx/SKILL.md`。优先保留原文、符号、层次和连线，再解决排版；不用于轴/比例本身携带证据的统计图表。
- Draw.io转PPT专项桥接：`vendor/sxy1499894281__drawio-reconstruction-skill/references/drawio-to-pptx.md`。其能力范围以原文及实际工具为准，不能把嵌入PNG的PPT说成形状可编辑。

上游某些路线要求独立Producer/Reviewer或特定宿主。只有实际满足时才能宣称按该上游完整验收；当前宿主没有第二代理时采用具名自检并明确缺少独立复核，不能虚构角色。基础Scene不支持的复杂元素保持原图并切换专项路线，不强迫用户接受简化。任何新增联网、软件安装、客户资料上传均单独遵守用户授权。
