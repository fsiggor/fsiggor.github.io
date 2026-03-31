# fsiggor.github.io

Blog pessoal e landing page de um engenheiro de software. Construído com Hugo + Hextra, deploy via GitHub Pages.

## Estrutura do repositório

```
├── README.md
├── AGENTS.md                    # Instruções para agentes de IA
├── blog/                        # Site Hugo + Hextra
│   ├── hugo.toml
│   ├── content/
│   ├── archetypes/
│   └── static/
├── docs/                        # Documentação do projeto
│   ├── ARCHITECTURE.md
│   ├── GUIDELINES.md
│   ├── CONTRIBUTING.md
│   ├── SECURITY.md
│   ├── SOURCES.md
│   └── PUBLISHING.md
└── .github/workflows/           # CI/CD
```

## Quick start

```bash
cd blog
hugo server -D
```

O site estará disponível em http://localhost:1313/.

## Documentação

| Documento | Conteúdo |
|-----------|----------|
| [AGENTS.md](AGENTS.md) | Instruções para agentes de IA |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Arquitetura e pipeline |
| [GUIDELINES.md](docs/GUIDELINES.md) | Convenções de conteúdo e frontmatter |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Como contribuir |
| [SECURITY.md](docs/SECURITY.md) | Segurança e dados sensíveis |
| [SOURCES.md](docs/SOURCES.md) | Catálogo de fontes por domínio |
| [PUBLISHING.md](docs/PUBLISHING.md) | Pipeline de publicação |

## Licença

Projeto pessoal — uso privado.
