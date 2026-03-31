# AGENTS.md — Instruções para agentes de IA

> Este arquivo é lido automaticamente pelo Claude Code via symlink CLAUDE.md → AGENTS.md.

## Contexto do projeto

Monorepo com blog pessoal Hugo + Hextra, deploy via GitHub Pages em fsiggor.github.io.

O dono é engenheiro de software que segue princípios XP (Kent Beck): simplicidade, feedback, comunicação, coragem. Documentação em português, conteúdo do blog em inglês.

## Estrutura

```
├── AGENTS.md          # Este arquivo (instruções para IA)
├── CLAUDE.md          # Symlink → AGENTS.md (gitignored)
├── README.md          # Descrição do projeto
├── blog/              # Site Hugo + Hextra
│   ├── hugo.toml
│   ├── content/
│   ├── archetypes/
│   └── static/
├── docs/              # Documentação do projeto
└── .github/workflows/ # CI/CD
```

## Regras

- **CLAUDE.md é symlink para AGENTS.md** — só AGENTS.md vai pro git, CLAUDE.md está no .gitignore
- Simplicidade acima de tudo (YAGNI, KISS)
- Não crie arquivos ou estruturas desnecessárias
- Conteúdo do blog vai em `blog/content/blog/`
- Hugo config em `blog/hugo.toml`
- Frontmatter YAML (`---`) em todos os .md de conteúdo
- Para rodar o Hugo: `cd blog && hugo server -D`

## Tom e estilo

- Respostas diretas, sem enrolação
- O dono é técnico — pode usar jargão de programação e conceitos avançados
- Em português por padrão; inglês para conteúdo técnico e blog
