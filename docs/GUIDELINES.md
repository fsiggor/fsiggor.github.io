# GUIDELINES.md — Convenções do vault

> Regras para criação, nomenclatura e organização de notas. Tanto humanos quanto agentes IA devem seguir estas convenções.

## Nomenclatura de arquivos

- **Lowercase com hífens:** `analise-selic-marco-2026.md` (nunca camelCase ou espaços)
- **Sem acentos no nome do arquivo:** `educacao-classica` (não `educação-clássica`)
- **Prefixo de data para conteúdo temporal:** `2026-03-30-decisao-copom.md`
- **Sem prefixo de data para conteúdo atemporal:** `o-que-e-flag-theory.md`
- **MOCs usam sufixo descritivo:** `reserva-de-valor.md`, `stack-tecnico-2026.md`
- **Templates usam o tipo como nome:** `artigo.md`, `video.md`, `jurisdicao.md`

## Frontmatter YAML

### Campos obrigatórios (toda nota)

```yaml
---
title: "Título legível em português"
source: "Nome da fonte (InfoMoney, Hacker News, etc.)"
source_type: "rss|youtube|twitter|manual|book"
url: "https://..."
date: 2026-03-30
ingested: 2026-03-30T14:30:00
domain: "FIN|ENG|FLAG|EDU|VIT"
tags:
  - tag1
  - tag2
status: "inbox|reviewed|archived|starred"
summary: "Resumo de 2-3 linhas"
related:
  - "[[Nota relacionada 1]]"
  - "[[Nota relacionada 2]]"
---
```

### Campos específicos por domínio

**FIN (Finanças):**
```yaml
ticker: "PETR4"
asset_class: "renda-variavel|renda-fixa|fii|cripto|commodity|macro"
market: "BR|US|global"
```

**ENG (Engenharia):**
```yaml
language: "go|python|rust|typescript|..."
area: "sistemas-distribuidos|ia-llms|devops|arquitetura|fundamentos|ferramentas"
repo_url: "https://github.com/..."
```

**FLAG (Flag Theory):**
```yaml
flag_number: 1-7
jurisdiction: "Portugal|Paraguai|Dubai|..."
program_type: "cbi|residencia|offshore-corp|banking|..."
```

**EDU (Educação clássica):**
```yaml
art: "gramatica|logica|retorica|aritmetica|geometria|musica|astronomia"
author: "Carpeaux|Hugo de São Vítor|Miriam Joseph|..."
work: "Nome da obra"
chapter: "Capítulo ou seção"
```

**VIT (Hobbies):**
```yaml
subdomain: "carnes|vinhos|metais-preciosos|terras-produtivas"
type: "receita|analise|cotacao|nota-pessoal|degustacao"
```

### Campos para blog (06-blog/)

```yaml
publish: true|false
draft: true|false
slug: "url-amigavel-do-post"
hugo_section: "posts|notes|guides"
categories:
  - categoria1
```

## Tags

### Regras gerais

- Lowercase, sem acentos, hífens como separador: `renda-variavel` (não `Renda Variável`)
- Tags descrevem O QUE é o conteúdo, não ONDE está (a pasta já diz onde)
- Mínimo 2, máximo 7 tags por nota
- Evitar tags genéricas demais: `mercado` é vago, `selic` ou `ibovespa` é útil
- Tags cross-domain são encorajadas: uma nota sobre ouro pode ter `ouro`, `commodity`, `reserva-de-valor`, `hedge`

### Tags reservadas (significado especial)

| Tag | Significado |
|-----|-------------|
| `urgente` | Requer atenção imediata (ex: mudança regulatória) |
| `acao-necessaria` | Precisa de alguma ação concreta do dono |
| `referencia` | Material de referência permanente (não temporal) |
| `series` | Parte de uma série de notas sobre o mesmo tema |
| `contradiz:[[nota]]` | Contradiz ou atualiza informação de outra nota |

## Status das notas

| Status | Significado | Localização |
|--------|-------------|-------------|
| `inbox` | Recém-chegada, não revisada | `00-inbox/` |
| `reviewed` | Revisada e aprovada pelo dono | Pasta do domínio |
| `archived` | Não mais relevante mas preservada | Pasta do domínio |
| `starred` | Importante, destacada | Pasta do domínio |
| `draft` | Artigo em rascunho | `06-blog/drafts/` |
| `review` | Artigo em revisão | `06-blog/review/` |
| `published` | Artigo publicado no blog | `06-blog/published/` |

## Wikilinks

- Use wikilinks do Obsidian: `[[Nome da nota]]`
- Para seções específicas: `[[Nome da nota#Seção]]`
- Para alias: `[[Nome da nota|texto exibido]]`
- Links entre domínios são encorajados e devem ser registrados em `related:` no frontmatter
- MOCs são o ponto de entrada para navegação cross-domain

## Maps of Content (MOCs)

MOCs são notas-índice que agregam e contextualizam notas de um ou mais domínios.

Estrutura de um MOC:
```markdown
---
title: "Reserva de valor"
domain: "CROSS"
tags: [moc, ouro, terras, cripto, hedge]
status: "reviewed"
---

# Reserva de valor

Notas sobre ativos que preservam poder de compra no longo prazo.

## Metais preciosos
- [[analise-ouro-2026]]
- [[prata-como-hedge]]

## Terras produtivas
- [[terras-ms-precificacao]]

## Cripto como reserva
- [[bitcoin-tese-store-of-value]]

## Flag Theory — Ativos físicos
- [[flag-5-ativos-fisicos]]
- [[jurisdicoes-ouro-fisico]]
```

Regras para MOCs:
- Um MOC por tema transversal, não por domínio (os `_index.md` dos domínios já fazem isso)
- Atualizado automaticamente pelo job semanal de curadoria
- O dono pode editar manualmente para adicionar comentários e priorizar itens
- MOCs ficam em `vault/MOCs/`

## Templates

Templates ficam em `vault/templates/` e são usados pelo Templater plugin.

Templates disponíveis:
- `artigo.md` — conteúdo genérico de qualquer fonte
- `video.md` — vídeo do YouTube (inclui campo de transcrição)
- `tweet-thread.md` — thread ou tweet relevante
- `nota-de-leitura.md` — fichamento de livro (domínio EDU)
- `receita.md` — receita com ingredientes, preparo, temperaturas
- `jurisdicao.md` — análise de jurisdição (domínio FLAG)
- `ativo.md` — análise de ativo financeiro (domínio FIN)
- `degustacao.md` — nota de degustação de vinho

## Imagens e anexos

- Imagens ficam na mesma pasta da nota que as referencia (Hugo page bundles)
- Formato preferido: PNG para diagramas, JPG para fotos
- Nomenclatura: `nome-da-nota-descricao.png`
- Referência no markdown: `![descrição](nome-da-nota-descricao.png)`
- Imagens são criptografadas junto com as notas via git-crypt
