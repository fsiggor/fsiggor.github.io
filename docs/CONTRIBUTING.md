# CONTRIBUTING.md — Como estender o sistema

> Guia para adicionar fontes, domínios, templates, processadores e integrações ao PKE.

## Adicionar uma nova fonte

1. Edite `collector/sources.yaml` e adicione a fonte no domínio correto:

```yaml
- name: "Nome da Fonte"
  type: rss|youtube_channel|twitter_user|manual
  url: "https://..."
  tags_default: [tag1, tag2]
```

2. Teste a coleta isolada:

```bash
cd collector
python main.py --source "Nome da Fonte" --dry-run
```

3. Verifique se o conteúdo coletado faz sentido (título, resumo, tags)
4. Commit com mensagem: `feat(sources): add Nome da Fonte to DOMAIN`

### Hierarquia de fontes (do Akita)

Sempre prefira, nesta ordem:
1. RSS/Atom feed nativo do site
2. Google News RSS como proxy (`https://news.google.com/rss/search?q=when:24h+allinurl:site.com`)
3. API pública do serviço (YouTube Data API, Twitter API)
4. Scraping com requests HTTP simples (sem JS)
5. Headless browser (Playwright/Puppeteer) — ÚLTIMO RECURSO

## Adicionar um novo domínio

1. Crie a pasta no vault: `vault/NN-nome-dominio/`
2. Crie o `_index.md` na pasta (MOC do domínio)
3. Adicione o domínio em:
   - `CLAUDE.md` → tabela de domínios
   - `GUIDELINES.md` → campos específicos do frontmatter
   - `collector/sources.yaml` → seção do domínio com schedule e fontes
   - `SECURITY.md` → classificação de sensibilidade
4. Crie templates específicos se necessário em `vault/templates/`
5. Atualize o `_system/domains.yaml`

## Adicionar um novo template

1. Crie o arquivo em `vault/templates/nome-do-template.md`
2. Use a sintaxe do Templater para campos dinâmicos: `{{title}}`, `{{date}}`, etc.
3. Inclua o frontmatter YAML completo com todos os campos obrigatórios
4. Documente o template em GUIDELINES.md seção Templates
5. Teste criando uma nota manualmente com o template

## Adicionar um processador IA

Processadores ficam em `collector/processors/` e são chamados em sequência para cada item coletado.

Interface de um processador:

```python
class Processor:
    """Base class for AI processors."""

    def __init__(self, config: dict):
        self.config = config

    def process(self, item: dict) -> dict:
        """
        Recebe um item coletado e retorna o item enriquecido.

        item = {
            "title": "...",
            "url": "...",
            "content": "...",   # texto extraído
            "source": "...",
            "domain": "...",
            "tags": [...],      # tags default da fonte
            "metadata": {...}   # metadados específicos
        }

        Retorna o mesmo dict com campos adicionais.
        """
        raise NotImplementedError
```

Processadores existentes:
- `summarizer.py` — gera resumo via LLM
- `tagger.py` — gera tags e detecta domínio
- `linker.py` — encontra notas relacionadas no vault
- `moc_updater.py` — sugere adição a MOCs existentes

Para adicionar um novo:
1. Crie o arquivo em `collector/processors/`
2. Implemente a interface `Processor`
3. Registre no pipeline em `collector/pipeline.yaml`
4. Adicione o prompt correspondente em `vault/_system/prompts/`

## Modificar o pipeline de processamento

O pipeline é configurado em `collector/pipeline.yaml`:

```yaml
pipeline:
  - processor: summarizer
    model: openrouter/google/gemini-2.5-flash
    enabled: true

  - processor: tagger
    model: ollama/llama3.2
    enabled: true

  - processor: linker
    model: openrouter/anthropic/claude-sonnet-4
    enabled: true
    requires: [summarizer, tagger]

  - processor: moc_updater
    model: ollama/llama3.2
    enabled: true
    requires: [linker]
    schedule: weekly  # não roda em cada item, só no job semanal
```

Cada processador pode especificar qual modelo usar (AI agnostic).

## Adicionar um novo tema ao Hugo

1. Escolha um tema em https://themes.gohugo.io/
2. Adicione como submódulo git: `git submodule add <url> hugo-site/themes/<nome>`
3. Atualize `hugo-site/config.toml`
4. Teste: `cd hugo-site && hugo server -D`
5. Verifique se o frontmatter das notas publicadas é compatível com o tema

## Convenções de commit

```
feat(domain): descrição     → nova funcionalidade
fix(domain): descrição      → correção
docs: descrição             → documentação
refactor(domain): descrição → refatoração sem mudar comportamento
chore: descrição            → manutenção (deps, configs)
content(domain): descrição  → conteúdo novo no vault (notas, MOCs)
publish: título do artigo   → publicação de artigo no blog
```

Exemplos:
```
feat(sources): add Kitco News RSS to VIT
fix(collector): handle timeout on Yahoo Finance fetch
content(FIN): add analysis of Selic decision March 2026
publish: Como estruturar investimentos usando Flag Theory
```

## Testes

O coletor deve ter testes para:
- Parsing de cada tipo de fonte (RSS, YouTube, Twitter)
- Deduplicação (mesmo URL não gera duas notas)
- Geração de frontmatter válido
- Pipeline de processamento (mocks para LLM)

```bash
cd collector
python -m pytest tests/ -v
```

## Estrutura do coletor

```
collector/
├── main.py                 # Entry point
├── config.py               # Carrega sources.yaml e pipeline.yaml
├── sources.yaml            # Cadastro de fontes
├── pipeline.yaml           # Configuração do pipeline de processamento
├── fetchers/
│   ├── base.py             # Interface base
│   ├── rss.py              # RSS/Atom fetcher
│   ├── youtube.py          # YouTube API + transcrição
│   └── twitter.py          # Twitter/X API
├── processors/
│   ├── base.py             # Interface base
│   ├── summarizer.py       # Resumo via LLM
│   ├── tagger.py           # Tags e categorização
│   ├── linker.py           # Linkagem com vault
│   └── moc_updater.py      # Atualização de MOCs
├── writers/
│   ├── markdown.py         # Gera .md com frontmatter
│   └── templates.py        # Aplica templates
├── db/
│   ├── dedup.py            # SQLite para deduplicação
│   └── pke.db              # Banco SQLite
└── tests/
    ├── test_fetchers.py
    ├── test_processors.py
    └── test_writers.py
```
