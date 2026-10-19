# 安装和选择

独立ZIP解压后，把research-drawio、research-pptx或research-diagram-workflow整个文件夹放入宿主配置的skills目录。选择一个即可，统一工作流不要求先安装另两个。宿主目录以各自设置为准；本项目使用公开Agent Skills格式，不宣称一个ZIP可在所有聊天产品自动安装。

仓库入口自动寻找engine/；独立包携带scripts/runtime/。不要只复制SKILL.md。没有Skills自动发现时，直接让具备文件/终端工具的代理读取SKILL.md。

Python 3.10+；PPT依赖python-pptx，PNG操作依赖Pillow，固定版本见requirements.txt。虚拟环境安装，不自动装系统依赖。

Draw.io Desktop从PATH、DRAWIO_PATH及标准macOS/Windows路径发现，可用--drawio显式指定。PPT实际预览需要LibreOffice和pdftoppm；没有就保持未完成，不用另一种格式冒充。

Mac可用Songti SC；Windows可在Scene显式指定SimSun/宋体。Linux需选择实际已安装的字体，例如Noto Serif CJK SC，并披露替代。两级逻辑字号在PPT按pt=逻辑字号×0.75转换；画布按96逻辑像素/英寸。不要重复缩放，不分发字体。

改结构/连接优先Draw.io；办公改字和版式优先PPT。双格式是同一Scene的两个输出，不是双向实时同步。复杂图保留原生Draw.io，不强行经过基础Scene导入器。
