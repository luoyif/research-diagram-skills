# 原始来源与集成边界

官方来源：jgraph/drawio-mcp，draw.io发布的技能及XML/导出资料。
社区来源：Agents365-ai/drawio-skill、sxy1499894281/drawio-reconstruction-skill、HututuWorks/sci-diagram-pptx。
本项目新增：research-*三入口、Scene引擎、内容/关系合同、几何检查、实际渲染状态及打包工具。

此前绘图参考了Draw.io原生重建/图像拆解方法，不是把每个上游脚本全执行一遍。jgraph官方资料及HututuWorks科研PPT技能是打包阶段补充核验的来源；sources.lock.json中的previous_project_use区分这些状态。

上游原件保留在vendor；集成代码与说明采用MIT，但不改变上游许可。没有复制受限的Anthropic PPTX技能，也没有打包系统内部技能、字体或客户数据。来源引用不是上游对本项目的认证。

开放Skill格式参考：https://agentskills.io/specification 。几何检查、原生编辑对象和实际渲染流程来自不同来源与本项目工程实践，不能将全部实现声称为某一个官方工具的原样输出。
