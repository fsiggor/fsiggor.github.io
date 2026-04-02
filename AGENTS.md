# AGENTS.md — Instructions for AI agents

> This file is automatically read by Claude Code via symlink CLAUDE.md → AGENTS.md.

## Project context

Monorepo with a personal Hugo + Hextra blog, deployed via GitHub Pages at fsiggor.github.io.

The owner is a software engineer who follows XP principles (Kent Beck): simplicity, feedback, communication, courage. All project files, documentation, comments, and content must be in English.

## Structure

```
├── AGENTS.md          # This file (AI instructions)
├── CLAUDE.md          # Symlink → AGENTS.md (gitignored)
├── README.md          # Project description
├── blog/              # Hugo + Hextra site
│   ├── hugo.toml
│   ├── content/
│   ├── archetypes/
│   └── static/
├── docs/              # Project documentation
└── .github/workflows/ # CI/CD
```

## Rules

- **CLAUDE.md is a symlink to AGENTS.md** — only AGENTS.md is tracked in git, CLAUDE.md is in .gitignore
- Simplicity above all (YAGNI, KISS)
- Do not create unnecessary files or structures
- Blog content goes in `blog/content/blog/`
- Hugo config is at `blog/hugo.toml`
- YAML frontmatter (`---`) in all content .md files
- To run Hugo: `cd blog && hugo server -D`

## Tone and style

- Direct responses, no fluff
- The owner is technical — feel free to use programming jargon and advanced concepts
- Everything in English
