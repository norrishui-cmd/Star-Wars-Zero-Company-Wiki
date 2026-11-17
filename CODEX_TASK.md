# 接手 Star Wars Zero Company Wiki 的 SEO 开发

GitHub 仓库为 [norrishui-cmd/Star-Wars-Zero-Company-Wiki](https://github.com/norrishui-cmd/Star-Wars-Zero-Company-Wiki)，默认分支为 `main`。

站点域名为 `starwarszerocompany.cc`。项目是静态 HTML，`index.html`、站点地图和 `vercel.json` 都在当前目录。可在此目录运行 `python3 -m http.server 8000` 本地预览。

## 目前的代码基线

本快照已将 2026-11-17 的 SEO 增量合入用户提供的原始源码。原始 ZIP 的归档注释为 `b7e19f6d4f73d5d859c89d687305190963aa56bc`，可用于与 Git 历史核对。该次增量含 494 个 HTML 与 10 个 Python 文件，涉及首页和栏目入口、FAQ、新闻内链、多语言页面和生成脚本。上轮增量包的 SHA-256 为 `1a9244407faa06b7fe53e23a8b8e0d26941d7de9034ab9a5ffd9b4460bd68f33`。本文件仅用于开发交接。

## 首个任务

1. 确认当前工程目录。在已有 Git 工作副本中，先核对分支、工作区改动和上述基线，再逐项合并仓库尚缺的变更；保留基线之后的用户修改。直接打开本快照时，代码已包含上轮改动，可以从审计开始。
2. 从项目根目录依次运行以下只读审计。Python 3.10 或更高版本可运行这组命令。

   ```bash
   python3 -B tools/seo_audit.py
   python3 -B tools/audit_round22_locale_parity.py
   python3 -B tools/audit_round23_cast_parity.py
   python3 -B tools/audit_round26_nav_news_faq.py
   ```

3. 对照交接基线核验结果。全站 1,875 份 HTML，站点地图 1,639 个 URL，152 篇可索引英文 FAQ。结构错误和失效内链均为 0。内容审计另有 166 条质量提示；保留事实准确性，逐页判断短答案是否需要扩充。
4. 用中文说明当前分支或快照、各项检查结果和发现的差异。若基线一致，直接报告复核结果。后续产生实际代码变更时，仅将本轮变化的文件按站点根目录相对路径打成覆盖 ZIP，附变更说明与验收结果，交给用户通过既有 GitHub Desktop 和 Vercel 流程发布。
