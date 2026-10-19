# Scene v1

这是本项目的轻量中间格式，不是draw.io官方JSON。每个文件一页，必需字段schema_version=1、width、height、nodes；edges可为空。

```json
{"schema_version":1,"title":"示例","author":"小罗","width":1400,"height":860,"font_family":"Songti SC","font_sizes":[26,21],"monochrome":true,"nodes":[],"edges":[]}
```

实际nodes不能为空。节点类型group/rect/ellipse/text；每个节点有唯一ASCII语义id、x/y/w/h、可选parent(root为画布)。子坐标相对父组，边的waypoints使用画布绝对坐标。group不承载文字，标签另建子text；底板标记role=background，最先绘制。背景/装饰豁免仅限真实底板/装饰，不能用它隐藏文字碰撞。

文本字段text、font_size（仅两级）、bold、align(left/center)、color。换行使用\n，不自动缩字号。图形支持fill、stroke、stroke_width、rounded；透明使用none。黑白模式要求RGB三个通道相同。

边：id、source、target、source_port、target_port、waypoints、arrow、dashed。端口在[0,1]边界上，如[1,0.5]是右侧中心，转折点为绝对坐标。arrow为目标箭头；不明方向需人工确认。可以明确声明allow_crossing，但不能借此绕过穿字检查；声明本身不是科学关系成立的证据。

不保证任意SVG路径、复杂公式、三维、照片、旋转文本或数据驱动图表的无损导入。超出范围走上游专项流程，不静默压平/丢弃。完整通用示例在examples/或独立包assets/。

显式共用总线可给相关边指定相同非空shared_bus；仍记录警告，不等于语义自动正确。未声明的共线叠线阻断；background/decoration角色不得包含文字以绕过碰撞检查。
