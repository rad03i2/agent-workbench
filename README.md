# Agent Workbench

A small, local-first command-line workbench for keeping agent-assisted development work deliberate and auditable. It tracks tasks, statuses, tags, notes, and a bounded event history in one portable JSON workspace — without executing prompts or commands and without sending data anywhere.

**Author:** Radwan Abdulhadi Ahmed · رضوان عبدالهادي أحمد · GitHub: @rad03i2

## Why it exists

Agent-assisted work often becomes scattered across chat transcripts and temporary notes. Agent Workbench provides a predictable project-side record of *what needs doing, what is in progress, what is blocked, and what was completed*. It is intentionally narrow: it organizes work; it does not pretend to be an autonomous agent runtime.

## Key features

- Local JSON workspace with atomic writes.
- Task lifecycle: `todo`, `doing`, `blocked`, `done`.
- Tags, searchable titles/notes, and append-only task notes.
- Bounded audit event history (latest 1,000 events).
- Summary counts for quick progress checks.
- Explicit `--yes` guard before deletion.
- `--json` machine-readable output for integrations.
- Input validation and corrupt/unsupported workspace rejection.
- Standard-library-only runtime; no accounts, telemetry, API keys, or network calls.
- Cross-platform automated tests for Python 3.10, 3.12, and 3.13.

## Requirements

Python 3.10 or newer.

## Installation

```bash
git clone https://github.com/rad03i2/agent-workbench.git
cd agent-workbench
python -m pip install -e .
```

## Quick start

```bash
agent-workbench init my-project
agent-workbench add "Review API contract" --tag api --tag review
agent-workbench status 1 doing
agent-workbench note 1 "Checked pagination and error responses."
agent-workbench list --status doing
agent-workbench summary
agent-workbench status 1 done
```

The default workspace is `.agent-workbench.json`. Use another path with `--file`:

```bash
agent-workbench --file workspaces/release.json init release-1.0
agent-workbench --file workspaces/release.json add "Run release checklist" --tag release
```

Machine-readable output:

```bash
agent-workbench --json list --tag release
agent-workbench --json summary
```

Search and audit history:

```bash
agent-workbench list --query pagination
agent-workbench events --limit 50
```

Deletion is intentionally explicit:

```bash
agent-workbench delete 3 --yes
```

## Configuration

There is no environment configuration and no `.env` file. `--file` selects the workspace. Workspace data uses schema version `1`. Tags and workspace names use letters, digits, `_`, `-`, and `.`; task titles are limited to 300 characters and notes are bounded to prevent accidental unbounded growth.

## Project structure

```text
src/agent_workbench/
  __init__.py     Public package API
  core.py         Validation, persistence, tasks, events
  cli.py          CLI and exit handling
tests/
  test_core.py    Persistence, filters, validation, lifecycle
  test_cli.py     CLI end-to-end flow
.github/workflows/ci.yml
```

## Testing

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
agent-workbench --version
```

GitHub Actions runs the same test suite on Ubuntu, Windows, and macOS. A green workflow is the authoritative CI result.

## Preview / screenshots

This is a terminal application, so a screenshot is optional. For a repository preview, capture the quick-start flow showing `list` and `summary`; do not publish real workspace notes or private agent transcripts.

## Security and privacy

All application operations are local. Agent Workbench does **not** execute task text, prompts, notes, or shell commands. The default workspace is in `.gitignore` to reduce accidental publication. Workspace files are plain JSON and are not encrypted, so do not store passwords, tokens, secrets, or sensitive transcripts in them. See [SECURITY.md](SECURITY.md).

## Limitations

- No GUI or web dashboard.
- No cloud sync, multi-user locking, or encryption.
- No autonomous agent execution or model/provider integration.
- Concurrent writers to the same workspace are not coordinated.
- Event history is intentionally capped at 1,000 entries.

These constraints keep the tool transparent and dependency-free.

## Optional roadmap

Potential future additions include safe workspace export/merge, configurable status sets, and an optional read-only HTML report. They are not required for the current workflow.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please add tests for behavior changes and keep documentation in English and Arabic aligned.

## License

MIT License. See [LICENSE](LICENSE).

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# Agent Workbench — العربية

أداة سطر أوامر صغيرة ومحلية لتنظيم العمل بمساعدة وكلاء الذكاء الاصطناعي بصورة واضحة وقابلة للمراجعة. تحفظ المهام وحالاتها والوسوم والملاحظات وسجل الأحداث في ملف JSON محلي واحد، من دون تنفيذ الأوامر أو إرسال البيانات إلى أي خدمة خارجية.

**المؤلف:** Radwan Abdulhadi Ahmed · رضوان عبدالهادي أحمد · GitHub: @rad03i2

## لماذا هذا المشروع؟

قد يتوزع العمل المعتمد على الوكلاء بين المحادثات والملاحظات المؤقتة. يوفر Agent Workbench سجلاً بسيطًا بجانب المشروع يوضح ما المطلوب، وما يجري العمل عليه، وما هو متوقف، وما اكتمل. الأداة تنظّم العمل فقط ولا تدّعي أنها منصة تشغيل وكيل ذاتي.

## الميزات الرئيسية

- مساحة عمل JSON محلية مع كتابة ذرية تقلل خطر تلف الملف.
- حالات المهام: `todo` و`doing` و`blocked` و`done`.
- وسوم وبحث في العناوين والملاحظات وإضافة ملاحظات متتابعة.
- سجل تدقيق يحتفظ بآخر 1,000 حدث.
- ملخص سريع لأعداد المهام حسب الحالة.
- اشتراط `--yes` قبل الحذف.
- مخرجات `--json` للاستخدام مع الأدوات الأخرى.
- التحقق من المدخلات ورفض ملفات مساحة العمل التالفة أو غير المدعومة.
- لا توجد تبعيات تشغيل خارج مكتبة Python القياسية، ولا حسابات أو تتبع أو مفاتيح API أو اتصال بالشبكة.
- اختبارات آلية متعددة الأنظمة لـ Python 3.10 و3.12 و3.13.

## المتطلبات والتثبيت

يتطلب Python 3.10 أو أحدث.

```bash
git clone https://github.com/rad03i2/agent-workbench.git
cd agent-workbench
python -m pip install -e .
```

## الاستخدام

```bash
agent-workbench init my-project
agent-workbench add "Review API contract" --tag api --tag review
agent-workbench status 1 doing
agent-workbench note 1 "Checked pagination and error responses."
agent-workbench list --status doing
agent-workbench summary
agent-workbench status 1 done
```

اسم الملف الافتراضي `.agent-workbench.json`. لتحديد ملف مختلف:

```bash
agent-workbench --file workspaces/release.json init release-1.0
```

للمخرجات البرمجية والبحث وسجل الأحداث:

```bash
agent-workbench --json summary
agent-workbench list --query pagination
agent-workbench events --limit 50
```

الحذف يحتاج تأكيدًا صريحًا:

```bash
agent-workbench delete 3 --yes
```

## الإعداد

لا يحتاج المشروع متغيرات بيئة أو ملف `.env`. الخيار `--file` يحدد مساحة العمل. صيغة البيانات الحالية هي schema رقم `1`. أسماء المساحات والوسوم محدودة بمحارف آمنة، كما توجد حدود لأطوال العناوين والملاحظات.

## بنية المشروع

`src/agent_workbench` يحتوي المحرك والـCLI، و`tests` يحتوي اختبارات المنطق والتدفق الكامل، بينما `.github/workflows/ci.yml` يشغّل الاختبارات على الأنظمة المدعومة.

## الاختبارات

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
agent-workbench --version
```

نتيجة GitHub Actions الخضراء هي المرجع النهائي لحالة CI.

## المعاينة

لأن المشروع أداة طرفية، لا يحتاج صورة شاشة كي يعمل. عند إضافة صورة تعريفية للمستودع يمكن تصوير أوامر `list` و`summary` ببيانات تجريبية فقط، وعدم نشر ملاحظات أو محادثات حقيقية.

## الخصوصية والأمان

كل العمليات محلية. الأداة لا تنفذ نصوص المهام أو الملاحظات أو الأوامر. ملف مساحة العمل الافتراضي موجود في `.gitignore` لتقليل احتمال نشره بالخطأ. البيانات JSON غير مشفرة، لذلك يجب عدم تخزين كلمات المرور أو الرموز أو الأسرار أو المحادثات الحساسة فيها. راجع [SECURITY.md](SECURITY.md).

## القيود

لا توجد واجهة رسومية أو مزامنة سحابية أو تشفير أو قفل متعدد المستخدمين، ولا يوجد تشغيل ذاتي للوكلاء أو تكامل مع مزودي النماذج. كذلك لا تتم مزامنة عمليات كتابة متزامنة على الملف نفسه، وسجل الأحداث محدود بآخر 1,000 حدث.

## تطوير اختياري

يمكن مستقبلًا إضافة دمج/تصدير آمن لمساحات العمل، وحالات قابلة للتخصيص، وتقرير HTML للقراءة فقط. هذه إضافات اختيارية وليست ميزات مزعومة في النسخة الحالية.

## المساهمة والترخيص

راجع [CONTRIBUTING.md](CONTRIBUTING.md) للمساهمة. المشروع مرخص برخصة MIT؛ راجع [LICENSE](LICENSE).

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
