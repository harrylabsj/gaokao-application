# WorkBuddy 候选资产：高考志愿填报顾问 1.0.0

本目录是从 2026-10-31 保全的 WorkBuddy 静态插件缓存整理出的源码候选，供检查和重新构建使用。它保留缓存中的插件描述、Agent、Skill、引用资料、脚本和头像。缓存目录没有 Git 元数据，也没有对应 source commit 或原始上传包。

## 版本与来源

- 插件 manifest 和 Skill 元数据均声明 `1.0.0`。
- 仓库根目录的通用 `gaokao-application` Skill 当前是 `1.1.1`。本集成目录是独立的历史候选，不覆盖或替代根目录源码，也不应误认为从 `1.1.1` 回推出来的原始 `1.0.0` Git 版本。
- 保全副本中的 `gaokao-advisor-1.0.0-cache-repack-candidate.zip` 是由缓存重打包的候选 ZIP。该 ZIP 的 SHA-256 只标识那次归档构建，无法证明它与 WorkBuddy 平台上传字节相同。本目录不包含该 ZIP。
- 缓存原 README 是带 TODO 的模板；这里的 README 是为本源码候选补写的说明，不是原始上传包内容的证据。
- `plugin.json` 的 MIT 字段来自缓存 manifest。仓库根 `LICENSE` 目前为 MIT；本目录没有独立复制一份许可证文件。

## 构建临时候选

在仓库根目录执行：

```bash
python3 integrations/workbuddy/build_candidate.py
```

脚本只打包本目录内的明确允许文件，产出 ZIP 和 SHA-256 sidecar 到系统临时目录。它不把 ZIP 写入仓库，也不会读取或打包其他目录、用户数据、缓存或凭证。该 ZIP 是可供平台解析验证的**候选包**，不是原上传包。

## 后续迁移

若要让此集成追随根目录版本，应先取得可验证的 WorkBuddy 原始源码/上传包证据，明确插件与 Skill 的版本映射，并审核行为、权限和 manifest 兼容性；再从目标版本的受控源码更新本目录。不要通过覆盖根目录 `SKILL.md` 或将本目录 ZIP 加入主仓来完成迁移。
