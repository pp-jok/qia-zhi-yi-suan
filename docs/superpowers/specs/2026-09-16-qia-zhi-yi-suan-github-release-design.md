# 掐指一算 GitHub 发布设计

## 目标

将 `destiny-personality` 作为独立、可安装的开源 Skill 发布到
`pp-jok/qia-zhi-yi-suan`。公开包装使用玄学与神秘意象，但不削弱现有的
事实边界、审计能力和非诊断声明。

## 公开身份

- 仓库：`qia-zhi-yi-suan`
- 展示名：`掐指一算`
- 英文副标题：`An Auditable Destiny & Personality Oracle`
- GitHub 简介：`以八字为骨，以星盘为镜，将命纹织成一部可审计的人格秘典。`
- 可发现关键词：`agent-skill`、`bazi`、`western-astrology`、
  `personality`、`oracle`、`chinese-metaphysics`

## 发布边界

公开仓库只包含可复用 Skill：`SKILL.md`、`agents/`、`checklists/`、
`configs/`、`examples/`、`references/`、`schemas/`，以及仓库级 README、
LICENSE 和 `.gitignore`。

不发布当前工作区的个人报告、PDF、出生资料、测试输出、项目过程文档、
临时脚本或其他业务文件。Skill 中的真实测试生日替换为明显虚构的格式示例，
同时保留紧凑输入合同的教学作用。

## README 气质

开场使用“星轨、五行、命纹、双重天穹、秘典”等意象。技术说明保持直接，
明确该项目是业务流程与执行校验框架：智能体在运行时调用外部计算能力，
Skill 本身不打包排盘软件。

README 包含：定位、能力、输入示例、56 章报告结构、安装方式、使用方式、
执行边界、目录结构、质量门槛、免责声明和许可证。神秘叙事不能声称科学确定性、
宿命预测、医疗诊断或绝对准确。

## 许可证

使用 MIT License，允许复制、修改与再发布，同时保留版权与免责条款。

## 发布流程

1. 在当前工作区创建隔离的发布目录，不初始化整个业务项目。
2. 复制 Skill 文件并脱敏真实测试输入。
3. 添加 README、MIT License 和 `.gitignore`。
4. 执行敏感信息扫描、Skill 官方校验和包合同测试。
5. 初始化 Git，创建单一初始提交。
6. 使用已登录的 GitHub 账号 `pp-jok` 创建公开仓库并推送 `main`。
7. 设置仓库简介和主题标签，随后读取远端状态确认发布成功。

## 失败处理

- 发现个人数据、绝对路径或密钥时停止发布，先完成脱敏并重新扫描。
- Skill 校验或测试失败时不创建远端仓库。
- 仓库名已占用时停止并报告，不自动改名。
- 远端创建成功但推送失败时保留本地发布目录，修复后继续，不删除远端或强推。

## 验收标准

- 远端地址为 `https://github.com/pp-jok/qia-zhi-yi-suan`。
- 默认分支为 `main`，工作树干净。
- 公开内容不包含本项目用户的出生资料、报告或本地绝对路径。
- `quick_validate.py` 返回 `Skill is valid!`。
- Skill 包合同测试通过。
- GitHub 简介、README 标题和主题标签与本设计一致。
