# FinalMate

FinalMate is a Claude Code and Codex-ready plugin for turning course/source material into structured study notes, exam-prep guides, cheatsheets, mock exams, and interactive HTML study pages.

The main Claude Code command is `/finalmate:notes`. The shared skill name is `notes`.

## Features

- Multi-discipline note writing for quantitative, technical, conceptual, case, and essay-style material.
- Markdown/Obsidian output with highlights, source quotes, quiz callouts, Mermaid diagrams, and self-assessment slots.
- Interactive HTML output with clickable quizzes, self-assessment, saved questions, sticky highlighter mode, keyboard highlight shortcuts, code-copy buttons, Mermaid, KaTeX, cheatsheet view, localStorage progress, and AI-ready question prompts.
- Anti-bias quiz rules that balance answer letters and avoid obvious option-length clues.
- Cheatsheets built from worked templates instead of concept-list dumps.

## Install as a Claude Code Plugin

Add this GitHub repository as a marketplace:

```text
/plugin marketplace add fwei0817-vivi/finalmate
```

Install the plugin:

```text
/plugin install finalmate@finalmate
```

Then use:

```text
/finalmate:notes
```

For local development:

```sh
claude --plugin-dir .
```

## Install in Codex

For a direct Codex skill install, copy the shared skill folder:

```sh
cp -R skills/notes ~/.codex/skills/notes
```

This enables `$notes` as a Codex skill.

For Codex plugin distribution, this repository includes `.codex-plugin/plugin.json`. The manifest points to `./skills/`, so the Claude Code plugin and Codex plugin reuse the same canonical skill instead of maintaining two copies.

If your Codex build uses a local plugin marketplace, clone or copy this repository as a plugin folder such as `~/plugins/finalmate`, then register it from your local marketplace configuration.

## Manual Skill Install

If you do not want the plugin wrapper, copy this folder:

```text
skills/notes
```

into:

```text
~/.claude/skills/notes
```

Manual copies and clones do not auto-update. Pull or copy again when this repository changes.

## Updates

Plugin users can update through Claude Code marketplace/plugin update flows. Third-party marketplace auto-update may need to be enabled by the user. Because this plugin declares an explicit `version` in `.claude-plugin/plugin.json`, each release must bump that version or Claude Code may consider the installed plugin already current.

Codex manual skill installs are also copy/clone based: they do not update automatically unless the user pulls the repository or copies the skill again. Codex plugin update behavior depends on the marketplace or plugin source used by that Codex installation.

## HTML Runtime Notes

Interactive HTML uses CDN-loaded libraries:

- `marked`
- `mermaid`
- `KaTeX`

The HTML mode therefore needs network access unless you vendor those assets yourself. Markdown/Obsidian mode works offline.

## Build and Validate the Demo

```sh
node scripts/build-demo.mjs
node scripts/validate-demo.mjs
```

Open `skills/notes/examples/class_demo.html` in a browser to inspect the interactive behavior.

## Sharing Tips

- Include screenshots or a short GIF of the HTML demo.
- Add GitHub topics such as `claude-code`, `claude-plugin`, `study-notes`, `exam-prep`, and `learning-tools`.
- Add Codex-oriented topics such as `codex`, `codex-plugin`, and `ai-study-notes` if you want Codex users to find it too.
- Share all installation paths: Claude Code plugin marketplace, Codex plugin/skill install, and manual skill copy for users who prefer standalone configuration.

## License

MIT
