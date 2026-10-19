# Research Diagram Skills · 科研可编辑绘图

**三个独立 Skill：Draw.io 绘图、PPT 绘图、统一工作流。** 输入可以是参考图、手绘草图、已有 SVG、受支持的 Draw.io 页面，或文字需求。默认保留参考图的信息层级与箭头语义，不把细节图擅自改成极简大框。

| 入口 | 适用任务 | 输出 |
|---|---|---|
| research-drawio | 经常改节点、连接和复杂层级 | 原生 .drawio、文本SVG、实际导出PNG |
| research-pptx | PowerPoint改字、排版和汇报 | 原生形状/文字/连线PPTX、SVG、实际PPT预览 |
| research-diagram-workflow | 用户选后端，或两种格式都要 | 共用Scene、冻结内容、两种输出、逐格式复核与打包 |

优先用Draw.io维护图的连接关系；PPT用于办公编辑。两者是同一源的输出，不是双向实时同步。默认黑白灰、已安装宋体配置、两级字号，作者“小罗”；不提供字体文件。

## 内容与来源

`skills/` 是三个本项目集成入口；`engine/` 是本项目编写的执行与检查代码；`vendor/` 原样保留四个开源项目的相关技能、脚本、参考资料和许可证。它不是把三个官方Skill重命名，也不受draw.io或Microsoft官方认证。

来源详见 [SOURCES](docs/SOURCES.md)、[PROVENANCE](docs/PROVENANCE.md) 和 sources.lock.json。锁文件包含仓库、固定commit、收录范围、排除清单和逐文件SHA256。“保留上游源码”不等于“已执行过所有上游脚本”。

## 快速运行

```bash
python3 -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python engine/diagram.py doctor
python engine/diagram.py validate examples/reference-reconstruction.scene.json
python engine/diagram.py freeze examples/reference-reconstruction.scene.json /tmp/reference.contract.json
python engine/diagram.py build examples/reference-reconstruction.scene.json --mode both --contract /tmp/reference.contract.json --out /tmp/research-demo-pass-01
python engine/diagram.py render /tmp/research-demo-pass-01 --mode drawio --width 6400
python engine/diagram.py render /tmp/research-demo-pass-01 --mode pptx --width 6400
```

路径换成自己的目录；输出目录及合同文件必须尚不存在。Draw.io预览需要draw.io Desktop；PPT实际预览需要LibreOffice及pdftoppm。没有工具就明确标为PENDING，不自动上传云端转换，也不拿SVG预览冒充PPT预览。

实际打开每张预览检查后，才记录具名声明：

```bash
python engine/diagram.py review /tmp/research-demo-pass-01 --reviewer 小罗 --verdict PASS --notes "已查看本次两个实际预览：双路输入分别汇聚；逐框文字、箭头方向、末端、边界和裁切均已复核。"
```

这条命令是记录声明，不代替真实视觉检查。生成时默认PENDING；源文件或预览变化，旧复核不能沿用。单代理检查不能写成独立双人审阅。

## 从自己的参考图开始

```bash
python engine/intake.py /path/reference.png --out /path/intake-01
```

支持视觉的代理或人员查看存档参考图，填写元素、原文、层级、箭头和不确定项，再编写Scene。SVG可提取原生文字，但CSS/变换和连接含义仍需核对。**这不是任意PNG一键无误转为PPT的图像识别服务。**

已有受支持的Draw.io：

```bash
python engine/from_drawio.py input.drawio --page 0 --out /path/imported.scene.json
```

基础导入器只支持未压缩XML、矩形/椭圆/文字/分组及明确路径；遇到复杂HTML、图标模板或自动路由等未支持元素会停止并报告，不丢掉后继续。复杂图沿用上游专项原生流程。

## 独立安装与打包

```bash
python tools/package_skills.py --out /path/new-release
```

三个独立ZIP各含SKILL.md、运行代码、示例、说明及所需上游快照。解压后的整个文件夹放入宿主配置的skills目录；没有自动发现能力时，让具备文件和终端工具的代理读取SKILL.md执行。不要只复制SKILL.md丢掉依赖。统一工作流可单独安装，不要求先装另两个入口。

## 测试

```bash
python -m unittest discover -s tests -v
python tools/verify_sources.py
```

详见 docs/WORKFLOW.md、docs/SCENE.md、docs/QA.md。几何PASS、单元测试PASS和实际视觉复核PASS不同；三者都不证明科研结论正确。仓库仅包含通用合成示例，不包含标书原文、客户图、凭证、生产数据或字体。
