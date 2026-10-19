# 三套 Skill 的选择与调用

这是可编辑科研绘图工作流，不是数据库 SQL，也不是生图模型。三个入口按公开 Agent Skills 目录结构组织，均可独立安装；完整工作流已经携带两种后端，不要求再装另外两个。

## 推荐选择

- **research-drawio**：优先用于参考图重建、复杂层级、需要反复移动节点或修改连线的技术图。`.drawio` 是连接关系的主文件。
- **research-pptx**：用于必须在 PowerPoint 中交付、需要办公改字和汇报排版的技术图。文字、框、分组和线段为原生对象；移动节点后须复查分段折线。
- **research-diagram-workflow**：推荐作为团队默认入口；根据用户选择输出 Draw.io、PPT 或两者，共用同一 Scene 与内容/连接清单。

两种输出不是双向实时同步。一个格式被人工修改后，应先确定哪个版本是当前主稿，再同步其结构，不应覆盖人工改动。

## 直接给支持技能的代理的提示词

### 参考图重建，Draw.io优先

> 使用 research-drawio。以我上传的参考图为依据，保留主要层级、次级卡片、原文和箭头方向，不改成极简大框。先清点元素和关系，标出模糊处，再建立可编辑源图。黑白灰、已安装宋体、两级字号，图文作者使用我指定的名字。每张图实际导出并检查文字、端点、穿框和裁切后，交付 .drawio、文字可编辑SVG、高清PNG及检查记录。仅写入我指定的新目录，不修改原文稿。

### 科研PPT原生绘图

> 使用 research-pptx。根据参考图重建技术机制图，要求文字、节点、图标和连线可分别编辑，不接受整页图片铺在PPT里。优先保留参考内容与拓扑，调整框宽和换行而不是随意增加字号种类。实际渲染PPT并逐页检查，再交付原生PPTX、SVG和预览；缺少渲染工具时明确未验证，不用SVG预览冒充PPT预览。

### 从文字或草图到双格式

> 使用 research-diagram-workflow。输入为我的文字需求或草图。先确定图型、输入、输出、模块层级和反馈关系；不确定关系先标记，不补造。主编辑格式选择Draw.io，同时生成原生PPT。共用内容和关系清单，每种格式分别导出检查，交付源文件、预览、版本和说明。复杂图不支持的元素走包内上游专项路线，不静默丢弃。

## 没有自动发现 Skill 的宿主

让具有文件读取、终端和视觉能力的代理先读取解压目录中的 `SKILL.md`。不是每个普通聊天网页都能直接安装ZIP或调用本地程序；宿主权限和本地工具以实际环境为准。

## 在新环境中测试

独立包内执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/diagram.py doctor
python tools/verify_sources.py
python scripts/diagram.py validate assets/reference-reconstruction.scene.json
python scripts/diagram.py build assets/reference-reconstruction.scene.json --out /path/new-pass-01
```

Windows使用虚拟环境的对应激活命令。输出目录必须尚不存在。Draw.io实际预览需要draw.io Desktop；PPT实际预览需要LibreOffice与pdftoppm。依赖缺失时保留PENDING，不自动安装、不悄悄上传客户图到云端。

## 如何迭代现有图

保留原始参考与已审版本。只修改用户指定节点、文字或连接；内容不变的版式调整沿用原文/连接合同。需要改业务关系或正式指标时先明确授权，不能通过重新冻结清单掩盖差异。每次修订写入新的pass目录，源文件改变后原视觉复核失效。

涉及真实曲线、坐标、比例和实验数据的科研统计图，应使用原始数据及专门绘图库；本项目重点是架构、流程和机制图，不用示意图伪造实验结果。
