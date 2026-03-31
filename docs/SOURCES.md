# SOURCES.md — Catálogo de fontes por domínio

> Lista completa de fontes de conteúdo organizadas por domínio, com URLs, tipo, e cadência. Referência para o `collector/sources.yaml`.

## FIN — Finanças e investimentos

### RSS

| Fonte | URL do feed | Tags default | Notas |
|-------|------------|-------------|-------|
| InfoMoney | `https://www.infomoney.com.br/feed/` | mercado, brasil | Principal fonte BR |
| Valor Econômico | `https://valor.globo.com/rss/` | mercado, macro, brasil | Paywall parcial |
| Bloomberg (via Google News) | `https://news.google.com/rss/search?q=when:24h+allinurl:bloomberg.com/markets` | mercado, global | Proxy via Google News RSS |
| Reuters Business (via Google News) | `https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com/business` | mercado, global | Proxy via Google News RSS |
| Suno Research Blog | `https://www.suno.com.br/noticias/feed/` | investimentos, brasil | Análises de ativos BR |
| Investing.com BR | `https://br.investing.com/rss/news.rss` | mercado, cotacoes | Dados e análises |
| Kitco News (Ouro/Prata) | `https://www.kitco.com/feed/rss/news/` | metais, ouro, prata, commodity | Cross-domain com VIT |

### YouTube

| Canal | Channel ID | Tags default |
|-------|-----------|-------------|
| Fernando Ulrich | A verificar | macro, economia-austriaca |
| Investidor Sardinha | A verificar | investimentos, dividendos |
| Peter Schiff (SchiffGold) | A verificar | ouro, macro, internacional |

### X/Twitter

| Perfil | Handle | Tags default | Notas |
|--------|--------|-------------|-------|
| A definir conforme preferência | | | Monitorar analistas/gestores |

**Cadência:** A cada 4 horas

---

## ENG — Engenharia de software e CS

### RSS

| Fonte | URL do feed | Tags default | Notas |
|-------|------------|-------------|-------|
| Hacker News (Best, >100pts) | `https://hnrss.org/best?points=100` | tech | Filtrado por qualidade |
| Lobsters | `https://lobste.rs/rss` | tech | Comunidade curada |
| Go Blog oficial | `https://go.dev/blog/feed.atom` | go, golang | Releases e artigos |
| Rust Blog | `https://blog.rust-lang.org/feed.xml` | rust | Referência |
| Anthropic Blog | `https://www.anthropic.com/research/feed.xml` | ia, llms | Pesquisa de IA |
| Akita On Rails | `https://akitaonrails.com/index.xml` | tech, dev-br | Inspiração do projeto |
| TLDR Newsletter | `https://tldr.tech/api/rss/tech` | tech, resumo | Digest diário |
| Golang Weekly | `https://golangweekly.com/rss/` | go, golang | Newsletter semanal |
| DevOps Weekly | `https://devopsweeklyarchive.com/feed` | devops | Newsletter semanal |
| The Pragmatic Engineer | `https://newsletter.pragmaticengineer.com/feed` | engenharia, carreira | Newsletter |

### YouTube

| Canal | Channel ID | Tags default |
|-------|-----------|-------------|
| ThePrimeagen | A verificar | tech, opiniao |
| Fireship | A verificar | tech, resumo |
| Akitando | A verificar | tech, dev-br |

### GitHub

| Tipo | URL/Config | Tags default | Notas |
|------|-----------|-------------|-------|
| Trending (Go) | GitHub Trending API filtro Go | go, repos | Semanal |
| Trending (Rust) | GitHub Trending API filtro Rust | rust, repos | Semanal |
| Releases acompanhados | Repos específicos via API | releases | Configurar por repo |

**Cadência:** A cada 6 horas

---

## FLAG — Flag Theory

### RSS

| Fonte | URL do feed | Tags default | Notas |
|-------|------------|-------------|-------|
| Flag Theory Blog | `https://flagtheory.com/feed/` | flag-theory, internacionalizacao | Fonte principal |
| Nomad Capitalist Blog | `https://nomadcapitalist.com/feed/` | flag-theory, nomad | Artigos sobre jurisdições |
| Offshore Citizen Blog | A verificar | offshore, cidadania | CBI e residência |
| International Man | `https://internationalman.com/feed/` | internacionalizacao, libertarianismo | Perspectiva macro |

### YouTube

| Canal | Channel ID | Tags default |
|-------|-----------|-------------|
| Nomad Capitalist | `UCgzfj9jqIajBSKSiEF4LC2A` | flag-theory, jurisdicoes |
| Offshore Citizen | A verificar | cidadania, offshore |

### Sites de referência (consulta manual)

| Site | URL | Uso |
|------|-----|-----|
| Passports.io | https://passports.io/ | Comparação de passaportes |
| Residencies.io | https://residencies.io/ | Programas de residência |
| Incorporations.io | https://incorporations.io/ | Abertura de empresas |
| BankAccounts.io | https://bankaccounts.io/ | Banking offshore |

**Cadência:** Semanal (segunda-feira às 8h)

---

## EDU — Educação clássica

### Fontes automáticas (poucas)

| Fonte | URL do feed | Tags default | Notas |
|-------|------------|-------------|-------|
| Livraria Hugo de São Vítor | A verificar | artes-liberais, trivium | Blog eventual |
| É Realizações Editora | A verificar | filosofia, educacao | Novos lançamentos |
| Bunker Editora | A verificar | educacao-classica | Novos lançamentos |

### Obras de referência (ingestão manual)

| Autor | Obra | Arte | Status |
|-------|------|------|--------|
| Miriam Joseph | O Trivium | Gramática, Lógica, Retórica | A ler |
| Otto Maria Carpeaux | História da Literatura Ocidental | Guia geral | A ler |
| Hugo de São Vítor | Didascalicon | Metodologia | A ler |
| Pedro da Fonseca | Instituições Dialéticas | Lógica | A ler |
| Prof. Clístenes H. Fernandes | Coleção 7 Artes Liberais | Todas | A ler |
| Boécio | Consolação da Filosofia | Quadrivium | A ler |
| Cassiodoro | Instituições | Artes liberais | A ler |
| Santo Alcuíno de Iorque | De grammatica | Gramática | A ler |

**Cadência:** Manual (sem automação — baseado em leitura de livros)

---

## VIT — Hobbies e interesses pessoais

### RSS

| Fonte | URL do feed | Tags default | Subdomain | Notas |
|-------|------------|-------------|-----------|-------|
| Kitco News | `https://www.kitco.com/feed/rss/news/` | metais, cotacoes | metais-preciosos | Cross-domain com FIN |
| SilverSeek | A verificar | prata, metais | metais-preciosos | Foco em prata |

### YouTube

| Canal | Channel ID | Tags default | Subdomain |
|-------|-----------|-------------|-----------|
| Canais de churrasco/BBQ | A definir | carnes, tecnicas | carnes |
| Canais de enologia | A definir | vinhos, degustacao | vinhos |

### Fontes manuais

| Tipo | Subdomain | Notas |
|------|-----------|-------|
| Receitas testadas | carnes | Inserção manual após preparo |
| Notas de degustação | vinhos | Inserção manual após degustação |
| Cotações de ouro/prata | metais-preciosos | Kitco + consulta manual |
| Artigos sobre terras | terras-produtivas | Links manuais, sem RSS |

**Cadência:** Diária (12h) para RSS; manual para o resto

---

## Como adicionar uma fonte

1. Verificar se o site tem RSS (procurar `/feed/`, `/rss/`, `/atom.xml`)
2. Se não tem, tentar Google News RSS: `https://news.google.com/rss/search?q=when:24h+allinurl:site.com`
3. Testar o feed: `curl -s "URL" | head -50`
4. Adicionar nesta tabela E em `collector/sources.yaml`
5. Ver CONTRIBUTING.md para detalhes técnicos
