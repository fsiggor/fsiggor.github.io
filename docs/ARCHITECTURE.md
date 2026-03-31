# Personal Knowledge Engine — Documento de Arquitetura

> Sistema AI-agnostic de automação para coleta, processamento e organização de conteúdo multi-domínio em um vault Obsidian criptografado, com chat IA integrado no navegador, assistência para escrita de artigos e publicação em blog Hugo.

**Versão:** 2.0  
**Data:** 2026-03-30  
**Inspiração:** The M.Akita Chronicles (arquitetura de coleta + IA + organização)  
**Princípios fundamentais:**
- **AI agnostic** — nenhum vendor lock-in; múltiplos modelos para diferentes tarefas
- **Vault criptografado** — dados sensíveis (finanças, flag theory) protegidos at rest
- **Chat IA no navegador** — Obsidian como interface principal de interação com IA, com contexto do vault
- **Pipeline de publicação** — do vault direto para blog Hugo, com IA assistindo a escrita

---

## 1. Visão geral

O sistema funciona como um pipeline de 6 camadas:

```
Fontes → Coletor → Processamento IA → Obsidian Vault (criptografado) → Chat IA + Escrita → Hugo Blog
```

Cada camada é independente e pode ser desenvolvida/testada separadamente. O princípio do Akita se aplica aqui: **sempre prefira a fonte mais simples que funcione** — RSS antes de scraping, API antes de headless browser.

**Princípio AI agnostic:** O sistema usa uma camada de abstração para provedores de IA. Nenhum componente depende de um modelo específico. A escolha do modelo é feita por tarefa:

| Tarefa | Modelo sugerido | Alternativa | Justificativa |
|--------|----------------|-------------|---------------|
| Chat conversacional (vault context) | Claude Sonnet | GPT-4o, Gemini Pro | Melhor para RAG e raciocínio sobre documentos |
| Resumo de artigos (batch) | Claude Haiku / Gemini Flash | DeepSeek, Qwen | Custo baixo para alto volume |
| Tagging e categorização | Modelo local (Ollama) | Qualquer API barata | Tarefa simples, não precisa de modelo caro |
| Escrita de artigos (assistência) | Claude Opus / GPT-4o | Gemini Pro | Qualidade de escrita importa aqui |
| Code generation (scripts) | Claude Code | Codex, Qwen-Coder | Agente com acesso ao filesystem |
| Embeddings (busca semântica) | Modelo local (nomic-embed) | OpenAI ada-002 | Roda local, sem custo recorrente |

A interface de roteamento é feita via **OpenRouter** (API unificada para 100+ modelos) ou via configuração direta por plugin no Obsidian.

---

## 2. Domínios de conhecimento

O vault opera em 5 domínios com características distintas:

### 2.1 Finanças e investimentos (FIN)

- **Perfil:** Investidor solo, decisões de alocação
- **Cadência:** Ingestão diária (alta sensibilidade temporal)
- **Tipo de conteúdo:** Notícias de mercado, análises macro, relatórios de ativos, cotações
- **Fontes sugeridas:**
  - RSS: InfoMoney, Valor Econômico, Bloomberg, Suno Research, Investing.com
  - YouTube: Fernando Ulrich, Investidor Sardinha, canais de macro
  - X/Twitter: analistas e gestores relevantes
  - API: Yahoo Finance (cotações), Google Finance RSS
- **Metadados específicos:** `ticker`, `asset_class` (renda fixa, variável, FII, cripto, commodity), `market` (BR, US, global)
- **Cruzamento:** Conecta com Flag Theory (proteção de ativos) e Hobbies (metais preciosos, terras)

### 2.2 Engenharia de software e ciência da computação (ENG)

- **Perfil:** Base técnica em constante atualização
- **Cadência:** Ingestão diária (conteúdo com meia-vida longa)
- **Tipo de conteúdo:** Artigos técnicos, repositórios, talks, papers, changelogs
- **Fontes sugeridas:**
  - RSS: Hacker News (hnrss.org), Lobsters, Go Blog, Rust Blog, Anthropic Blog
  - YouTube: canais tech (ThePrimeagen, Fireship, Akita, etc.)
  - X/Twitter: devs e pesquisadores
  - GitHub: trending repos, releases de projetos acompanhados
  - Newsletters RSS: TLDR, Golang Weekly, DevOps Weekly
- **Metadados específicos:** `language` (Go, Python, Rust...), `area` (sistemas distribuídos, IA/LLMs, DevOps, arquitetura...), `repo_url`
- **Cruzamento:** Conecta com Finanças (ferramentas de análise) e projetos pessoais

### 2.3 Flag Theory (FLAG)

- **Perfil:** Internacionalização pessoal, soberania financeira
- **Cadência:** Semanal (mudanças regulatórias são lentas mas impactantes)
- **Tipo de conteúdo:** Artigos sobre jurisdições, residência fiscal, offshore banking, cidadania por investimento, proteção de ativos
- **As 7 bandeiras:**
  1. Cidadania e residência
  2. Residência fiscal
  3. Offshore banking
  4. Empresa offshore
  5. Ativos físicos (metais preciosos, terras, imóveis)
  6. Ativos digitais (cripto, tokens)
  7. Segurança digital
- **Fontes sugeridas:**
  - RSS: flagtheory.com/archives, Nomad Capitalist blog, Offshore Citizen
  - YouTube: Nomad Capitalist, Offshore Citizen, Peter Schiff (ouro/macro)
  - X/Twitter: perfis de internacionalização
  - Sites: passports.io, residencies.io, incorporations.io
- **Metadados específicos:** `flag_number` (1-7), `jurisdiction`, `program_type` (CBI, residência, offshore corp, etc.)
- **Cruzamento:** Pesado com Finanças (ativos, tributação) e Hobbies (metais, terras)

### 2.4 Educação clássica (EDU)

- **Perfil:** Formação intelectual via artes liberais — Trivium (gramática, lógica, retórica) + Quadrivium (aritmética, geometria, música, astronomia)
- **Cadência:** Sob demanda (ingestão predominantemente manual)
- **Tipo de conteúdo:** Notas de leitura, fichamentos, resumos de capítulos, referências cruzadas entre autores
- **Referências centrais:**
  - Otto Maria Carpeaux — História da literatura ocidental como guia de leitura
  - Coleção 7 Artes Liberais (Instituto Hugo de São Vítor / Prof. Clístenes Hafner)
  - Miriam Joseph — O Trivium
  - Hugo de São Vítor — Didascalicon
  - Pedro da Fonseca — Dialética
  - Boécio, Cassiodoro, Santo Alcuíno de Iorque
- **Fontes sugeridas:**
  - Poucos feeds automáticos — este domínio é construído via leitura e anotação
  - RSS (eventual): Livraria Hugo de São Vítor blog, É Realizações, Bunker Editora
  - YouTube: aulas sobre artes liberais, Olavo de Carvalho (referências ao Trivium)
  - Manual: fichamentos de livros, notas de estudo
- **Metadados específicos:** `art` (gramática, lógica, retórica, aritmética, geometria, música, astronomia), `author`, `work`, `chapter`
- **Cruzamento:** Base intelectual que informa todos os outros domínios (lógica → análise de investimentos, retórica → escrita)
- **Diferença arquitetural:** Aqui a IA não coleta — ela organiza, tageia e sugere conexões entre notas que você criou manualmente

### 2.5 Interesses pessoais e hobbies (VIT)

- **Perfil:** Conhecimento prático + ativos tangíveis
- **Cadência:** Variável (mix de diário e sob demanda)
- **Subdomínios:**
  - **Carnes e churrasco:** Técnicas de preparo, cortes, defumação, temperaturas
  - **Vinhos/enologia:** Regiões, uvas, harmonizações, notas de degustação
  - **Metais preciosos:** Ouro, prata — tanto como hobby quanto reserva de valor
  - **Terras produtivas:** Agricultura, pecuária, propriedades rurais como investimento
  - **Outros:** Conforme interesse
- **Fontes sugeridas:**
  - YouTube: canais de churrasco (Pit Master), enologia, agricultura
  - RSS: blogs de culinária, Kitco News (metais)
  - Manual: notas de receitas testadas, degustações, visitas
- **Metadados específicos:** `subdomain` (carnes, vinhos, metais, terras), `type` (receita, análise, cotação, nota pessoal)
- **Cruzamento:** Metais e terras cruzam com Finanças e Flag Theory

---

## 3. Estrutura do vault Obsidian

```
vault/
├── 00-inbox/                    # Tudo cai aqui primeiro
│   ├── FIN/                     # Inbox por domínio (opcional, pode ser flat)
│   ├── ENG/
│   ├── FLAG/
│   ├── EDU/
│   └── VIT/
│
├── 01-financas/
│   ├── macro/                   # Análises macroeconômicas
│   ├── renda-variavel/          # Ações, ETFs
│   ├── renda-fixa/
│   ├── fiis/
│   ├── cripto/
│   ├── commodities/             # Ouro, prata, agro
│   └── _index.md                # MOC do domínio
│
├── 02-engenharia/
│   ├── go/
│   ├── arquitetura/
│   ├── ia-llms/
│   ├── devops/
│   ├── fundamentos-cs/
│   ├── ferramentas/
│   └── _index.md
│
├── 03-flag-theory/
│   ├── 1-cidadania/
│   ├── 2-residencia-fiscal/
│   ├── 3-offshore-banking/
│   ├── 4-empresa-offshore/
│   ├── 5-ativos-fisicos/
│   ├── 6-ativos-digitais/
│   ├── 7-seguranca-digital/
│   ├── jurisdicoes/             # Uma nota por jurisdição relevante
│   └── _index.md
│
├── 04-educacao-classica/
│   ├── trivium/
│   │   ├── gramatica/
│   │   ├── logica/
│   │   └── retorica/
│   ├── quadrivium/
│   │   ├── aritmetica/
│   │   ├── geometria/
│   │   ├── musica/
│   │   └── astronomia/
│   ├── autores/                 # Notas por autor (Carpeaux, Hugo de São Vítor, etc.)
│   ├── obras/                   # Notas por obra/livro
│   └── _index.md
│
├── 05-hobbies/
│   ├── carnes/
│   ├── vinhos/
│   ├── metais-preciosos/
│   ├── terras-produtivas/
│   └── _index.md
│
├── 06-blog/                     # Artigos para publicação no Hugo
│   ├── drafts/                  # Rascunhos em andamento
│   ├── review/                  # Em revisão (IA + pessoal)
│   └── published/               # Prontos para publicar (tag publish: true)
│
├── MOCs/                        # Maps of Content — cross-domain
│   ├── reserva-de-valor.md      # Liga FIN + FLAG + VIT (ouro, terras, cripto)
│   ├── internacionalizacao.md   # Liga FLAG + FIN
│   ├── stack-tecnico-2026.md    # Liga ENG (Go, IA, ferramentas)
│   ├── formacao-intelectual.md  # Liga EDU (progresso no Trivium/Quadrivium)
│   └── ...
│
├── templates/                   # Templates de nota por tipo
│   ├── artigo.md
│   ├── video.md
│   ├── tweet-thread.md
│   ├── nota-de-leitura.md
│   ├── receita.md
│   ├── jurisdicao.md
│   ├── ativo.md
│   └── degustacao.md
│
├── _system/                     # Configs do sistema
│   ├── prompts/                 # Prompts usados pela IA para processamento
│   │   ├── summarize.md
│   │   ├── tagger.md
│   │   ├── linker.md
│   │   └── moc-updater.md
│   ├── sources.yaml             # Cadastro de fontes (RSS URLs, canais, perfis)
│   ├── domains.yaml             # Configuração dos domínios
│   └── cron-config.yaml         # Cadência por domínio
│
└── CLAUDE.md                    # Instruções para Claude Code via MCP
```

---

## 4. Frontmatter YAML padrão

Cada nota gerada pelo sistema segue este schema:

```yaml
---
title: "Título do conteúdo"
source: "InfoMoney"              # De onde veio
source_type: "rss"               # rss | youtube | twitter | manual | book
url: "https://..."               # Link original
date: 2026-03-30                 # Data de publicação original
ingested: 2026-03-30T14:30:00    # Quando foi coletado
domain: "FIN"                    # FIN | ENG | FLAG | EDU | VIT
tags:
  - macro
  - selic
  - renda-fixa
status: "inbox"                  # inbox | reviewed | archived | starred
summary: "Resumo de 2-3 linhas gerado pela IA"
related:                         # Wikilinks sugeridos pela IA
  - "[[Perspectivas Selic 2026]]"
  - "[[MOCs/reserva-de-valor]]"

# Campos específicos por domínio (opcionais)
ticker: "PETR4"                  # FIN
asset_class: "renda-variavel"    # FIN
flag_number: 2                   # FLAG
jurisdiction: "Portugal"         # FLAG
art: "lógica"                    # EDU
author: "Carpeaux"               # EDU
subdomain: "carnes"              # VIT
---
```

---

## 5. Templates de nota

### 5.1 Template: Artigo (genérico)

```markdown
---
title: "{{title}}"
source: "{{source}}"
source_type: "{{source_type}}"
url: "{{url}}"
date: {{date}}
ingested: {{ingested}}
domain: "{{domain}}"
tags: {{tags}}
status: "inbox"
summary: "{{summary}}"
related: {{related}}
---

# {{title}}

> Fonte: [{{source}}]({{url}}) — {{date}}

## Resumo

{{ai_summary}}

## Pontos-chave

{{ai_key_points}}

## Notas pessoais

<!-- Espaço para suas anotações após revisão -->

---

*Processado automaticamente em {{ingested}}*
```

### 5.2 Template: Nota de leitura (Educação clássica)

```markdown
---
title: "{{work}} — {{chapter}}"
source_type: "book"
domain: "EDU"
art: "{{art}}"
author: "{{author}}"
work: "{{work}}"
chapter: "{{chapter}}"
tags: {{tags}}
status: "inbox"
date: {{date}}
---

# {{work}} — {{chapter}}

**Autor:** {{author}}
**Arte liberal:** {{art}}

## Resumo do trecho

<!-- Seu resumo -->

## Citações relevantes

<!-- Trechos que marcou -->

## Conexões

<!-- Como isso se conecta com outras leituras ou domínios -->

## Perguntas abertas

<!-- O que ficou sem resposta, para investigar depois -->
```

### 5.3 Template: Jurisdição (Flag Theory)

```markdown
---
title: "{{country}} — Flag Theory"
source_type: "manual"
domain: "FLAG"
jurisdiction: "{{country}}"
tags: {{tags}}
status: "inbox"
date: {{date}}
---

# {{country}}

## Cidadania / Residência (Flag 1)
<!-- Programas disponíveis, requisitos, custos, timeline -->

## Tributação (Flag 2)
<!-- Regime fiscal, territorial vs. worldwide, tratados -->

## Banking (Flag 3)
<!-- Bancos acessíveis, requisitos de abertura, reputação -->

## Empresas (Flag 4)
<!-- Tipos societários, custos, compliance, substance requirements -->

## Ativos físicos (Flag 5)
<!-- Imóveis, terras, metais — regras de posse por estrangeiros -->

## Ativos digitais (Flag 6)
<!-- Regulamentação cripto, exchanges locais -->

## Notas pessoais

<!-- Suas observações e decisões -->
```

### 5.4 Template: Receita (Hobbies/Carnes)

```markdown
---
title: "{{title}}"
source: "{{source}}"
source_type: "{{source_type}}"
url: "{{url}}"
domain: "VIT"
subdomain: "carnes"
tags: {{tags}}
status: "inbox"
date: {{date}}
---

# {{title}}

## Ingredientes

<!-- Lista -->

## Preparo

<!-- Passo a passo -->

## Temperaturas e tempos

| Etapa | Temperatura | Tempo |
|-------|------------|-------|
|       |            |       |

## Notas pessoais

<!-- Como ficou quando você testou, ajustes -->
```

---

## 6. Pipeline de ingestão (Coletor)

### 6.1 Arquitetura do coletor

```
┌─────────────────────────────────────────────┐
│              sources.yaml                    │
│  (cadastro de todas as fontes por domínio)  │
└──────────────────┬──────────────────────────┘
                   │
          ┌────────▼────────┐
          │   Scheduler     │
          │  (cron/systemd) │
          └────────┬────────┘
                   │
     ┌─────────────┼─────────────┐
     ▼             ▼             ▼
┌─────────┐ ┌──────────┐ ┌──────────┐
│ RSS     │ │ YouTube  │ │ Twitter  │
│ Fetcher │ │ Fetcher  │ │ Fetcher  │
└────┬────┘ └────┬─────┘ └────┬─────┘
     │           │            │
     └─────────┬─┘────────────┘
               ▼
     ┌─────────────────┐
     │  Deduplicador   │
     │  (SQLite/hash)  │
     └────────┬────────┘
              ▼
     ┌─────────────────┐
     │  Fila de        │
     │  processamento  │
     └────────┬────────┘
              ▼
     ┌─────────────────┐
     │  IA Processing  │
     │  (Claude API)   │
     └────────┬────────┘
              ▼
     ┌─────────────────┐
     │  Markdown Writer│
     │  → vault/inbox/ │
     └─────────────────┘
```

### 6.2 Arquivo sources.yaml

```yaml
domains:
  FIN:
    schedule: "*/4 * * * *"    # A cada 4 horas
    sources:
      - name: "InfoMoney"
        type: rss
        url: "https://www.infomoney.com.br/feed/"
        tags_default: [mercado, brasil]

      - name: "Valor Econômico"
        type: rss
        url: "https://valor.globo.com/rss/"
        tags_default: [mercado, macro]

      - name: "Yahoo Finance BR"
        type: rss
        url: "https://news.google.com/rss/search?q=when:24h+allinurl:finance.yahoo.com&hl=pt-BR"
        tags_default: [mercado, global]

  ENG:
    schedule: "*/6 * * * *"    # A cada 6 horas
    sources:
      - name: "Hacker News - Best"
        type: rss
        url: "https://hnrss.org/best?points=100"
        tags_default: [tech]

      - name: "Lobsters"
        type: rss
        url: "https://lobste.rs/rss"
        tags_default: [tech]

      - name: "Go Blog"
        type: rss
        url: "https://go.dev/blog/feed.atom"
        tags_default: [go, golang]

      - name: "Akita On Rails"
        type: rss
        url: "https://akitaonrails.com/index.xml"
        tags_default: [tech, dev-br]

  FLAG:
    schedule: "0 8 * * 1"      # Segunda-feira às 8h
    sources:
      - name: "Flag Theory Blog"
        type: rss
        url: "https://flagtheory.com/feed/"
        tags_default: [flag-theory, internacionalizacao]

      - name: "Nomad Capitalist"
        type: youtube_channel
        channel_id: "UCgzfj9jqIajBSKSiEF4LC2A"
        tags_default: [flag-theory, internacionalizacao]

  EDU:
    schedule: null               # Sem automação — manual only
    sources: []

  VIT:
    schedule: "0 12 * * *"      # Diário ao meio-dia
    sources:
      - name: "Kitco News"
        type: rss
        url: "https://www.kitco.com/feed/rss/news/"
        tags_default: [metais, ouro, prata]
```

### 6.3 Deduplicação

O sistema usa um SQLite local com hash SHA256 da URL como chave primária:

```sql
CREATE TABLE ingested_items (
    url_hash TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    source TEXT NOT NULL,
    domain TEXT NOT NULL,
    ingested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    vault_path TEXT,
    status TEXT DEFAULT 'processed'
);
```

Antes de processar qualquer item, verifica se `url_hash` já existe. Isso evita duplicatas mesmo se o mesmo artigo aparecer em múltiplos feeds.

### 6.4 Cadência por domínio

| Domínio | Cron | Volume estimado/dia | Justificativa |
|---------|------|-------------------|---------------|
| FIN | A cada 4h | 10-20 itens | Mercado muda rápido, precisa estar atualizado |
| ENG | A cada 6h | 5-15 itens | Conteúdo com meia-vida longa, menos urgência |
| FLAG | Semanal (segunda) | 2-5 itens | Mudanças regulatórias são lentas |
| EDU | Manual | 0 automático | Baseado em leitura de livros |
| VIT | Diário (12h) | 3-8 itens | Mix de cotações (metais) e conteúdo estável |

---

## 7. Processamento IA

### 7.1 Pipeline de processamento

Cada item coletado passa por 4 etapas de IA:

1. **Resumo:** 2-3 parágrafos factuais do conteúdo
2. **Tagger:** Gera tags relevantes + identifica domínio e subdomínio
3. **Linker:** Busca notas existentes no vault que se relacionam e sugere `[[wikilinks]]`
4. **MOC Updater:** Se o item é relevante para um MOC existente, sugere adição

### 7.2 Prompt de resumo (summarize.md)

```markdown
Você é um assistente de curadoria de conhecimento. Dado o conteúdo abaixo,
gere um resumo factual em português de 2-3 parágrafos. Sem opinião, sem
sensacionalismo. Foque nos fatos, dados e conclusões do autor original.

Domínio: {{domain}}
Fonte: {{source}}
Título: {{title}}

Conteúdo:
{{content}}

Responda APENAS com o resumo, sem preâmbulo.
```

### 7.3 Prompt de tagging (tagger.md)

```markdown
Dado o conteúdo abaixo, gere:
1. Uma lista de 3-7 tags relevantes (lowercase, sem acentos, separadas por vírgula)
2. O domínio principal: FIN, ENG, FLAG, EDU ou VIT
3. Campos específicos do domínio quando aplicável

Conteúdo:
{{content}}

Responda em JSON:
{
  "tags": ["tag1", "tag2"],
  "domain": "FIN",
  "specific_fields": {
    "ticker": "PETR4",
    "asset_class": "renda-variavel"
  }
}
```

### 7.4 Prompt de linkagem (linker.md)

```markdown
Dado o resumo abaixo e a lista de notas existentes no vault, sugira
até 5 notas relacionadas que devem ser linkadas via wikilink.

Resumo:
{{summary}}

Notas existentes (título | tags):
{{vault_index}}

Responda em JSON:
{
  "related": ["Nota X", "Nota Y"],
  "reasoning": "Breve justificativa para cada link"
}
```

### 7.5 Custo estimado

Usando Claude Sonnet via API (ou equivalente via OpenRouter para otimizar custo):

| Operação | Tokens estimados | Custo por item (aprox.) |
|----------|-----------------|----------------------|
| Resumo | ~1500 input + 500 output | ~$0.005 |
| Tagger | ~1500 input + 200 output | ~$0.003 |
| Linker | ~2000 input + 300 output | ~$0.004 |
| **Total por item** | | **~$0.012** |
| **30 itens/dia × 30 dias** | | **~$10.80/mês** |

Nota: Esses valores variam conforme o modelo e provedor. Via OpenRouter com modelos mais baratos, pode cair para $3-5/mês.

---

## 8. Chat IA no Obsidian (AI agnostic)

O Obsidian funciona como sua interface principal de chat com IA — no navegador ou desktop — com a vantagem de ter o contexto do vault inteiro disponível para fundamentar respostas.

### 8.1 Stack de plugins recomendado

O ecossistema de plugins é montado em camadas, cada uma AI agnostic:

**Camada 1 — Chat conversacional com contexto do vault:**

Plugin principal: **Smart Connections + Smart Chat**
- Smart Connections faz embeddings locais de todas as notas (zero cloud)
- Smart Chat abre um painel de chat que busca notas relevantes via RAG antes de enviar para o modelo
- Suporta qualquer provedor: OpenAI, Anthropic, Google, Ollama (local), OpenRouter
- As conversas ficam salvas como notas .md dentro do vault — pesquisáveis e linkáveis
- Smart Chat Pro adiciona workspace dedicado com contexto do vault e review do que vai ser enviado ao modelo

**Camada 2 — Chat agêntico (lê/escreve no vault):**

Plugin: **Claudian** (sidebar com Claude Code) ou **BMO Chatbot** (multi-provider)
- Claudian: embeds Claude Code como sidebar — pode ler, escrever, editar notas, executar bash, usar MCP
- BMO Chatbot: suporta Ollama, LM Studio, OpenAI, Anthropic, Google, Mistral, OpenRouter — chat com nota atual ou vault inteiro
- Para uso AI agnostic, BMO é mais flexível; Claudian é mais poderoso mas tied ao Claude

**Camada 3 — Edição in-place (sem chat):**

Plugin: **Nova** ou **ChatGPT MD**
- Seleciona texto → aplica transformação (reescrever, expandir, traduzir, corrigir) → resultado streama no lugar
- ChatGPT MD suporta múltiplos provedores e modelos locais via Ollama
- O frontmatter da nota pode especificar qual modelo usar: `model: "ollama/llama3.2"` ou `model: "claude-sonnet-4-20250514"`

**Camada 4 — Roteamento de provedores (hub central):**

Plugin: **AI Providers**
- Configura todos os provedores de IA em um só lugar (API keys, endpoints, modelos default)
- Outros plugins consomem dele — evita configurar a mesma API key em 5 plugins diferentes
- Suporta OpenAI-compatible endpoints, Ollama, e provedores específicos

### 8.2 Configuração AI agnostic via OpenRouter

OpenRouter funciona como proxy unificado para 100+ modelos. Todos os plugins que aceitam "OpenAI-compatible endpoint" funcionam com OpenRouter:

```
Endpoint: https://openrouter.ai/api/v1
API Key: sk-or-...
Model: anthropic/claude-sonnet-4   (ou qualquer outro)
```

Isso significa que você pode trocar de modelo a qualquer momento sem mudar plugin. Na prática:

- Chat rápido do dia a dia → `google/gemini-2.5-flash` (barato e rápido)
- Análise profunda de documentos → `anthropic/claude-sonnet-4` (melhor RAG)
- Escrita de artigos → `anthropic/claude-opus-4` (melhor qualidade)
- Tagging batch → `deepseek/deepseek-chat` (custo mínimo)
- Privacidade total → `ollama/llama3.2` (local, zero cloud)

### 8.3 Modelos locais via Ollama

Para dados sensíveis (finanças, flag theory), rodar modelos localmente é ideal:

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Baixar modelos
ollama pull llama3.2          # Chat geral (3B, roda em qualquer máquina)
ollama pull nomic-embed-text  # Embeddings para Smart Connections
ollama pull qwen2.5-coder     # Assistência de código

# O servidor roda em http://localhost:11434
# Todos os plugins de Obsidian que suportam Ollama apontam para esse endpoint
```

Fluxo recomendado: dados sensíveis → Ollama local. Dados públicos/tech → API cloud via OpenRouter.

### 8.4 Fluxo de chat no dia a dia

```
Você abre o Obsidian no navegador (Obsidian Web ou desktop app)
    │
    ├── Quer perguntar algo rápido sobre o vault?
    │   └── Smart Chat → busca notas via RAG → envia contexto + pergunta para o modelo
    │
    ├── Quer que a IA crie/edite notas no vault?
    │   └── Claudian/BMO → agente com acesso ao filesystem → cria, edita, organiza
    │
    ├── Está escrevendo um artigo e quer assistência?
    │   └── ChatGPT MD / Nova → edição in-place → reescrever, expandir, traduzir
    │
    └── Quer deep research cruzando vault + web?
        └── Claude Code via MCP → busca vault primeiro → web search como fallback
```

---

## 9. Pipeline de publicação: Obsidian → Hugo

### 9.1 Visão geral do fluxo

```
Nota no vault (status: draft)
    │
    ├── IA assiste na escrita (Smart Chat, Nova, ChatGPT MD)
    │
    ├── Nota recebe tag #publish no frontmatter
    │
    ├── Git hook ou script detecta a tag
    │
    ├── obsidian-to-hugo converte wikilinks → Hugo refs
    │
    ├── Copia para hugo/content/posts/
    │
    ├── Hugo build (local preview ou CI/CD)
    │
    └── Deploy (Netlify, Cloudflare Pages, Vercel, ou self-hosted)
```

### 9.2 Estrutura no vault para publicação

```
vault/
├── 06-blog/                     # Artigos em andamento
│   ├── drafts/                  # Rascunhos (status: draft)
│   ├── review/                  # Em revisão (status: review)
│   └── published/               # Publicados (status: published)
│
└── ...
```

### 9.3 Frontmatter para artigos publicáveis

```yaml
---
title: "Como estruturar investimentos usando Flag Theory"
date: 2026-03-30
draft: false
publish: true                    # Flag que triggers o pipeline
slug: "flag-theory-investimentos"
categories:
  - finanças
  - flag-theory
tags:
  - internacionalizacao
  - investimentos
  - offshore
summary: "Um guia prático sobre como aplicar os 7 flags..."
domain: "FLAG"
status: "published"
hugo_section: "posts"            # Onde vai no Hugo (posts, notes, guides...)
---
```

### 9.4 Script de sincronização Obsidian → Hugo

Usando `obsidian-to-hugo` (Python, zero dependências):

```bash
# Instalar
pip install obsidian-to-hugo

# Executar (pode ser via git hook, cron, ou manualmente)
python -m obsidian_to_hugo \
  --obsidian-vault-dir=/path/to/vault/06-blog/published \
  --hugo-content-dir=/path/to/hugo/content/posts
```

O que ele faz automaticamente:
- Converte `[[wikilinks]]` para Hugo `[text]({{< ref "path" >}})`
- Converte `==highlights==` para `<mark>highlights</mark>`
- Copia imagens referenciadas para `hugo/static/images/`
- Aceita filtros e processadores customizados

### 9.5 Automação via Git hook

```bash
#!/bin/bash
# .git/hooks/post-commit (no repo do vault)

BLOG_DIR="/path/to/hugo"
VAULT_DIR="/path/to/vault"

# Encontra notas com publish: true
PUBLISH_FILES=$(grep -rl "publish: true" "$VAULT_DIR/06-blog/" --include="*.md")

if [ -n "$PUBLISH_FILES" ]; then
    python -m obsidian_to_hugo \
        --obsidian-vault-dir="$VAULT_DIR/06-blog/published" \
        --hugo-content-dir="$BLOG_DIR/content/posts"

    cd "$BLOG_DIR"
    git add -A
    git commit -m "Auto-publish from vault"
    git push  # Triggers Netlify/Cloudflare build
fi
```

### 9.6 IA como assistente de escrita

O diferencial do seu blog: você não escreve do zero nem posta conteúdo genérico de IA. O fluxo é:

1. **Pesquisa:** Claude Code busca no vault notas relevantes sobre o tema (via MCP)
2. **Outline:** IA sugere estrutura do artigo baseada nas suas notas coletadas
3. **Primeiro rascunho:** Você escreve o core, IA expande e refina (via Nova/ChatGPT MD in-place)
4. **Fact-check:** IA cruza claims do artigo com notas do vault e fontes originais
5. **Revisão:** IA corrige gramática, melhora fluxo, sugere cortes (especialmente útil para português/inglês)
6. **Publicação:** Tag `publish: true` → git hook → Hugo → deploy

O conteúdo sai fundamentado na sua base de conhecimento, não genérico.

### 9.7 Deploy sugerido

| Opção | Custo | Setup | Nota |
|-------|-------|-------|------|
| Cloudflare Pages | Grátis | Conecta GitHub, build command: `hugo` | Mais rápido, CDN global |
| Netlify | Grátis (tier básico) | Conecta GitHub, auto-build | Mais popular, boa DX |
| Self-hosted (VPS) | ~$5/mês | Hugo build local + rsync/scp | Controle total |
| GitHub Pages | Grátis | GitHub Actions + Hugo | Simples mas menos flexível |

---

## 10. Criptografia do vault

### 10.1 Estratégia de criptografia em camadas

O vault contém dados com sensibilidades diferentes. A estratégia é criptografia em camadas:

**Camada 1 — Disco (at rest):**
- **Linux/Mac:** LUKS (Linux) ou FileVault (Mac) — criptografia full-disk nativa do OS
- **Windows:** BitLocker
- Protege contra roubo físico do dispositivo
- Zero overhead no uso diário do Obsidian

**Camada 2 — Git (sync/backup):**
- **git-crypt** com chaves GPG — criptografia transparente no push/pull
- Arquivos ficam criptografados no GitHub/GitLab, decriptados localmente
- Configuração via `.gitattributes`:

```gitattributes
# Criptografar tudo exceto configs do git
*.md filter=git-crypt diff=git-crypt
*.canvas filter=git-crypt diff=git-crypt
*.png filter=git-crypt diff=git-crypt
*.jpg filter=git-crypt diff=git-crypt
*.pdf filter=git-crypt diff=git-crypt

# NÃO criptografar
.gitattributes !filter !diff
.gitignore !filter !diff
```

Setup:
```bash
# Inicializar
cd /path/to/vault
git init
git-crypt init

# Exportar chave simétrica (BACKUP ESSA CHAVE!)
git-crypt export-key ~/vault-key.bin

# Ou usar GPG (recomendado — já usa para commits assinados)
git-crypt add-gpg-user SEU_EMAIL@example.com

# Verificar status
git-crypt status
```

**Camada 3 — Notas individuais (sensíveis):**
- Plugin **Obsidian Encrypt** (meld-cp) — criptografa seções específicas dentro de uma nota
- Plugin **Cryptsidian** — criptografa vault inteiro com AES-256 (útil para "trancar" ao sair)
- Para notas de finanças e flag theory com dados pessoais específicos (números de conta, CPF, etc.)

### 10.2 Configuração recomendada por domínio

| Domínio | Sensibilidade | Camada 1 (disco) | Camada 2 (git) | Camada 3 (nota) |
|---------|--------------|-------------------|----------------|-----------------|
| FIN | Alta | Sim | git-crypt | Seções com dados bancários |
| FLAG | Alta | Sim | git-crypt | Dados de passaporte/contas |
| ENG | Baixa | Sim | git-crypt (pode relaxar) | Não necessário |
| EDU | Baixa | Sim | git-crypt | Não necessário |
| VIT | Baixa | Sim | git-crypt | Não necessário |

### 10.3 Compatibilidade com IA

Ponto crítico: a criptografia do vault não pode impedir o funcionamento dos plugins de IA.

- **git-crypt** é transparente — arquivos ficam decriptados localmente, criptografados só no remote. Os plugins de IA leem arquivos locais normalmente.
- **Cryptsidian** (vault inteiro criptografado) bloqueia tudo — usar apenas quando sair do computador, não durante uso.
- **Obsidian Encrypt** (seções) — a IA não vê o conteúdo criptografado dentro da nota, o que é o comportamento desejado para dados sensíveis.
- **Modelos locais (Ollama)** — para notas financeiras e flag theory, preferir IA local para não enviar dados sensíveis para APIs cloud.

### 10.4 Backup da chave de criptografia

A chave do git-crypt é o ponto único de falha. Perder = perder acesso ao vault no remote.

Estratégia de backup:
- Exportar chave simétrica: `git-crypt export-key ~/vault-key.bin`
- Armazenar em: pendrive criptografado (separado) + password manager (Bitwarden/1Password) + cópia offline em local seguro
- Se usar GPG: backup da chave privada GPG com as mesmas precauções
- Testar recovery periodicamente: clonar repo em máquina nova, decriptar com a chave

---

## 11. Consulta via Claude Code + MCP

### 8.1 Setup

1. **Plugin Obsidian:** Instalar `obsidian-claude-code-mcp` (iansinnott)
   - Habilita servidor MCP via WebSocket (porta 22360)
   - Claude Code auto-descobre o vault via lock file

2. **Claude Code:** Configurar para conectar ao Obsidian
   - Ao rodar `claude` no terminal, executar `/ide` e selecionar Obsidian
   - Ou configurar manualmente no `claude_desktop_config.json`

3. **CLAUDE.md:** Arquivo na raiz do vault com instruções de comportamento

### 8.2 CLAUDE.md (instruções para Claude Code)

```markdown
# Personal Knowledge Engine — Instruções

## Contexto
Este vault é uma base de conhecimento pessoal com 5 domínios:
- FIN: Finanças e investimentos (investidor solo)
- ENG: Engenharia de software e CS
- FLAG: Flag Theory (internacionalização, soberania financeira)
- EDU: Educação clássica (Trivium + Quadrivium, Carpeaux)
- VIT: Interesses pessoais (carnes, vinhos, metais, terras)

## Regra de ouro para consultas
1. SEMPRE busque primeiro no vault local antes de ir para a web
2. Use as tags e o frontmatter YAML para filtrar resultados
3. Cite as notas do vault com [[wikilinks]] na resposta
4. Se o vault não tem a informação, faça web search como fallback
5. Ao usar web search, pergunte se o usuário quer salvar o resultado como nova nota

## Estrutura do vault
- 00-inbox/: itens não revisados (status: inbox)
- 01-financas/ a 05-hobbies/: conteúdo organizado por domínio
- MOCs/: Maps of Content que cruzam domínios
- templates/: templates de nota por tipo
- _system/: configs e prompts

## Frontmatter
Todas as notas têm frontmatter YAML com: title, source, domain, tags, status, summary, related.
Use esses campos para filtrar buscas.

## Ao criar novas notas
- Use o template apropriado de templates/
- Coloque em 00-inbox/{DOMAIN}/
- Preencha o frontmatter completo
- Sugira wikilinks para notas existentes

## Tom
Respostas diretas, sem enrolação. O usuário é técnico e quer dados, não disclaimers.
Para finanças: apresente fatos e dados, não recomendações de compra/venda.
Para educação clássica: respeite a tradição intelectual, referencie autores originais.
```

### 8.3 Fluxos de consulta

**Consulta simples (vault-first):**
```
Você: "O que eu tenho sobre Selic?"
Claude Code → MCP → busca no vault por tag "selic"
→ Encontra 8 notas → sintetiza com citações [[wikilink]]
```

**Consulta com fallback web:**
```
Você: "Qual a última decisão do Copom?"
Claude Code → MCP → busca "copom" no vault
→ Nota mais recente é de 2 semanas atrás
→ Faz web search para dados atuais
→ Pergunta: "Quer que eu salve isso como nova nota?"
```

**Deep research (cross-domain):**
```
Você: "Compile tudo que tenho sobre proteção de patrimônio"
Claude Code → MCP → busca tags: ouro, metais, flag-theory, ativos-fisicos, terras
→ Encontra notas em FIN, FLAG e VIT
→ Gera relatório cruzando os domínios
→ Atualiza MOCs/reserva-de-valor.md
```

**Assistência em leitura (EDU):**
```
Você: "Acabei de ler o capítulo 3 do Trivium da Miriam Joseph sobre lógica proposicional.
       Crie uma nota de leitura e conecte com o que já tenho."
Claude Code → cria nota usando template nota-de-leitura.md
→ Busca notas existentes em 04-educacao-classica/trivium/logica/
→ Sugere conexões com notas anteriores
```

---

## 12. Jobs periódicos

Além da ingestão contínua, o sistema roda jobs semanais:

### 9.1 Curadoria semanal (domingo à noite)

- Analisa todas as notas em `00-inbox/` com status "inbox"
- Move notas para a pasta do domínio correto
- Atualiza MOCs com novos itens relevantes
- Gera relatório: quantas notas entraram, por domínio, quais não foram revisadas

### 9.2 Digest semanal (segunda de manhã)

- Gera uma nota-resumo em `MOCs/digest-semanal-YYYY-WW.md`
- Highlights por domínio: o que entrou, tendências, conexões novas
- Lista notas "starred" da semana
- Não é newsletter — é briefing pessoal

### 9.3 Limpeza mensal

- Identifica notas com status "inbox" há mais de 30 dias
- Sugere: revisar, arquivar ou deletar
- Detecta links quebrados e fontes que pararam de publicar

---

## 13. Fases de implementação

### Fase 1 — Fundação (Semana 1-2)

- [ ] Criar vault Obsidian com estrutura de pastas (incluindo `06-blog/`)
- [ ] Configurar criptografia: full-disk + git-crypt no repo
- [ ] Criar todos os templates de nota
- [ ] Escrever CLAUDE.md
- [ ] Instalar plugins de IA: Smart Connections, Smart Chat, BMO/Claudian
- [ ] Configurar OpenRouter como hub de provedores
- [ ] Instalar Ollama + modelos locais básicos
- [ ] Instalar plugin obsidian-claude-code-mcp
- [ ] Testar chat com contexto do vault
- [ ] Criar sources.yaml com 3-5 fontes por domínio

**Entregável:** Vault criptografado, chat IA funcionando com contexto do vault.

### Fase 2 — Coletor automático (Semana 3-4)

- [ ] Implementar RSS fetcher (Python com feedparser ou Go)
- [ ] Implementar deduplicação via SQLite
- [ ] Configurar cron/systemd para FIN e ENG (alto volume)
- [ ] Implementar markdown writer (gera notas no vault)
- [ ] Testar ciclo completo: fonte → nota no inbox

**Entregável:** Notas aparecendo automaticamente no vault a cada poucas horas.

### Fase 3 — Processamento IA (Semana 5-6)

- [ ] Implementar pipeline de resumo via Claude API
- [ ] Implementar tagger automático
- [ ] Implementar linker (busca notas relacionadas)
- [ ] Implementar MOC updater
- [ ] Configurar custos e rate limits

**Entregável:** Notas chegam no vault já resumidas, tageadas e linkadas.

### Fase 4 — Pipeline Hugo + Expansão (Semana 7+)

- [ ] Configurar site Hugo com tema escolhido
- [ ] Implementar script obsidian-to-hugo
- [ ] Configurar git hook para auto-publish
- [ ] Setup deploy (Cloudflare Pages ou Netlify)
- [ ] Adicionar YouTube fetcher (transcrição + resumo)
- [ ] Adicionar Twitter/X monitor
- [ ] Expandir fontes para FLAG e VIT
- [ ] Implementar digest semanal
- [ ] Implementar curadoria automática (mover do inbox)
- [ ] Refinar prompts com base nos primeiros resultados
- [ ] Considerar busca semântica via embeddings locais (Ollama + nomic-embed)

**Entregável:** Sistema completo: coleta → IA → vault criptografado → chat → escrita → blog Hugo.

---

## 14. Stack técnico sugerido

| Componente | Opção A (pragmática) | Opção B (se quiser aprender Go) |
|------------|---------------------|-------------------------------|
| Coletor/fetcher | Python (feedparser, yt-dlp, tweepy) | Go (gofeed, youtube API client) |
| Deduplicação | SQLite (nativo em ambos) | SQLite |
| Processamento IA | OpenRouter (multi-modelo) | OpenRouter |
| Chat no Obsidian | Smart Chat + BMO Chatbot | Smart Chat + Claudian |
| Modelos locais | Ollama (llama3.2, nomic-embed) | Ollama |
| Escrita assistida | ChatGPT MD / Nova (in-place) | ChatGPT MD / Nova |
| Scheduler | cron + systemd | cron + systemd |
| Markdown writer | Python (gera .md direto) | Go (template/text) |
| Vault | Obsidian | Obsidian |
| Criptografia (git) | git-crypt + GPG | git-crypt + GPG |
| Criptografia (disco) | LUKS / FileVault / BitLocker | LUKS / FileVault / BitLocker |
| Consulta agêntica | Claude Code + MCP plugin | Claude Code + MCP plugin |
| Blog | Hugo | Hugo |
| Deploy blog | Cloudflare Pages / Netlify | Cloudflare Pages / Netlify |
| Obsidian→Hugo | obsidian-to-hugo (Python) | Script custom (Go) |
| Versionamento | Git + git-crypt | Git + git-crypt |

---

## 15. Riscos e mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Inbox infinito (acumula sem revisar) | Vault vira cemitério | Digest semanal + alerta de notas >30 dias sem revisão |
| Custo de IA escala com volume | Gasto mensal cresce | Rate limit por domínio + OpenRouter com modelos baratos para batch |
| Fontes RSS quebram/mudam | Ingestão para | Healthcheck semanal de fontes + alertas |
| Vault fica grande demais | Obsidian fica lento | Arquivar notas antigas (>6 meses sem acesso) em pasta separada |
| Over-engineering prematuro | Nunca termina | Fase 1 sem código — só vault + chat IA manual |
| Duplicatas cross-domain | Mesma nota em FIN e FLAG | Tag multi-domain no frontmatter, nota física em um só lugar |
| Perda da chave de criptografia | Perda total do vault remoto | Backup em 3 locais: pendrive, password manager, cópia offline |
| Vendor lock-in em IA | Dependência de um provedor | OpenRouter como abstração + Ollama local como fallback |
| Dados sensíveis enviados para cloud | Vazamento de dados financeiros | Ollama para domínios FIN e FLAG; cloud só para ENG e EDU |
| Blog publica nota errada | Conteúdo inacabado vai ao ar | Flag `publish: true` explícita + preview local antes do deploy |

---

## 16. Referências

- [The M.Akita Chronicles — Arquitetura](https://akitaonrails.com/2026/02/16/vibe-code-do-zero-a-producao-em-6-dias-the-m-akita-chronicles/)
- [Web Scraping em 2026 — Bastidores](https://akitaonrails.com/2026/02/18/web-scrapping-em-2026-bastidores-do-the-m-akita-chronicles/)
- [Obsidian Claude Code MCP Plugin](https://github.com/iansinnott/obsidian-claude-code-mcp)
- [Flag Theory — The Foundation](https://flagtheory.com/the-foundation/)
- [Coleção 7 Artes Liberais — Hugo de São Vítor](https://livraria.hugodesaovitor.org.br/instituto-hugo-de-sao-vitor/7-artes-liberais-12-obras-completo)
- [Prompt do M.Akita (1o prompt)](https://gist.github.com/akitaonrails/d2a7983fc4c839b8071f5d0babaadf94)
- [Smart Connections — Plugin Obsidian](https://github.com/brianpetro/obsidian-smart-connections)
- [Smart Chat — Plugin Obsidian](https://smartconnections.app/smart-chat/)
- [Claudian — Claude Code no Obsidian](https://www.vibesparking.com/en/blog/ai/claude-code/2026-01-04-claudian-obsidian-plugin-embeds-claude-code-sidebar/)
- [BMO Chatbot — Multi-provider chat](https://github.com/longy2k/obsidian-bmo-chatbot)
- [ChatGPT MD — Chat nativo no Obsidian](https://www.blog.brightcoding.dev/2026/03/25/chatgpt-md-the-ai-assistant-your-obsidian-vault-needs)
- [obsidian-to-hugo — Conversor](https://github.com/devidw/obsidian-to-hugo)
- [Obsidian→Hugo Workflow (pedrotchang)](https://pedrotchang.dev/posts/automated-obsidian-to-hugo-publishing/)
- [Obsidian como Hugo CMS (nickgracilla)](https://www.nickgracilla.com/posts/obsidian-is-my-hugo-cms/)
- [git-crypt com Obsidian (Medium)](https://medium.com/@mathieu.veron_70170/secure-hosting-of-your-obsidian-vault-on-github-with-encryption-c5c9995ac843)
- [Obsidian + git-crypt (snazzybytes)](https://github.com/snazzybytes/obsidian-scripts)
- [Cryptsidian — Vault encryption](https://github.com/triumphantomato/cryptsidian)
- [OpenRouter — Multi-model API](https://openrouter.ai/)
- [Ollama — Modelos locais](https://ollama.com/)
