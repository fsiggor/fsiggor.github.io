# PUBLISHING.md — Pipeline de publicação: Obsidian → Hugo

> Como escrever artigos no vault, usar IA como assistente, e publicar no blog Hugo com deploy automático.

## Visão geral do fluxo

```
Ideia / pesquisa no vault
    ↓
06-blog/drafts/slug-do-artigo.md     (status: draft)
    ↓  ← IA auxilia: outline, expansão, fact-check
06-blog/review/slug-do-artigo.md     (status: review)
    ↓  ← Revisão pessoal + IA corrige gramática/fluxo
06-blog/published/slug-do-artigo.md  (status: published, publish: true)
    ↓  ← Git hook detecta publish: true
obsidian-to-hugo converte wikilinks
    ↓
hugo-site/content/posts/slug-do-artigo/index.md
    ↓
Hugo build + deploy (Cloudflare Pages / Netlify)
    ↓
Blog publicado na web
```

## Escrevendo um artigo

### 1. Criar o rascunho

No Obsidian, criar nota em `06-blog/drafts/` usando o template:

```yaml
---
title: "Título do artigo"
date: 2026-03-30
draft: true
publish: false
slug: "titulo-do-artigo"
categories:
  - categoria
tags:
  - tag1
  - tag2
summary: "Uma frase descrevendo o artigo"
domain: "FIN"
status: "draft"
hugo_section: "posts"
related:
  - "[[nota-de-referencia-1]]"
  - "[[nota-de-referencia-2]]"
---

# Título do artigo

## Introdução

<!-- Escreva aqui -->

## Desenvolvimento

<!-- Use [[wikilinks]] para referenciar notas do vault -->

## Conclusão

<!-- ... -->

## Referências

<!-- Links para fontes originais -->
```

### 2. Usar IA como assistente de escrita

**Pesquisa prévia (Claude Code via MCP):**
```
"Compile tudo que tenho no vault sobre [tema]. Liste as notas, resumos e conexões."
```

**Gerar outline (Smart Chat):**
```
"Dado estas notas do vault sobre [tema], sugira uma estrutura de artigo com seções e pontos-chave."
```

**Expandir seções (ChatGPT MD / Nova — in-place):**
- Selecione um bullet point ou frase-semente
- Use o comando de expansão do plugin
- A IA expande baseando-se no contexto da nota atual

**Fact-check (Claude Code via MCP):**
```
"Verifique as afirmações deste artigo cruzando com as notas do vault. Liste quais têm fonte e quais não têm."
```

**Revisão gramatical (in-place):**
- Selecione o texto completo
- Aplique correção gramatical via ChatGPT MD ou Nova
- Para bilíngue PT/EN: especifique o idioma no prompt

### 3. Mover para review

Quando o rascunho estiver maduro:
1. Mova de `drafts/` para `review/`
2. Atualize `status: "review"` no frontmatter
3. Releia integralmente fora do modo de edição
4. Peça para a IA fazer uma última revisão de fluxo e coerência

### 4. Publicar

Quando satisfeito:
1. Mova de `review/` para `published/`
2. Atualize o frontmatter:
   ```yaml
   draft: false
   publish: true
   status: "published"
   ```
3. Commit e push — o git hook cuida do resto

## Configuração do Hugo

### Estrutura mínima

```
hugo-site/
├── config.toml
├── content/
│   └── posts/           ← Artigos vêm para cá
├── static/
│   └── images/          ← Imagens dos artigos
├── themes/
│   └── <tema-escolhido>/
└── .github/
    └── workflows/
        └── deploy.yml   ← CI/CD (opcional)
```

### config.toml básico

```toml
baseURL = "https://seublog.com/"
languageCode = "pt-br"
title = "Seu Blog"
theme = "tema-escolhido"

[params]
  description = "Blog pessoal sobre finanças, tecnologia e internacionalização"

[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true    # Permite HTML inline (para <mark>, etc.)

[taxonomies]
  tag = "tags"
  category = "categories"

# Ignorar arquivos do Templater
ignoreFiles = ["_templates\\.md$"]
```

### Temas sugeridos

| Tema | Estilo | Link |
|------|--------|------|
| PaperMod | Minimalista, rápido | https://github.com/adityatelange/hugo-PaperMod |
| Stack | Blog + documentação | https://github.com/CaiJimmy/hugo-theme-stack |
| Blowfish | Moderno, Tailwind | https://github.com/nunocoracao/blowfish |
| Congo | Clean, multi-idioma | https://github.com/jpanther/congo |

## Script de sincronização

### obsidian-to-hugo (Python)

```bash
pip install obsidian-to-hugo

python -m obsidian_to_hugo \
  --obsidian-vault-dir=vault/06-blog/published \
  --hugo-content-dir=hugo-site/content/posts
```

O que ele faz:
- `[[wikilinks]]` → `[text]({{< ref "path" >}})`
- `==highlight==` → `<mark>highlight</mark>`
- Copia imagens referenciadas
- Ignora frontmatter que Hugo não entende (campos do vault)

### Git hook (automático)

Arquivo: `scripts/obsidian-to-hugo.sh`

```bash
#!/bin/bash
set -e

VAULT_DIR="$(dirname "$0")/../vault"
HUGO_DIR="$(dirname "$0")/../hugo-site"

# Verificar se há notas para publicar
PUBLISH_COUNT=$(grep -rl "publish: true" "$VAULT_DIR/06-blog/published/" --include="*.md" 2>/dev/null | wc -l)

if [ "$PUBLISH_COUNT" -eq 0 ]; then
    echo "Nenhuma nota para publicar."
    exit 0
fi

echo "Publicando $PUBLISH_COUNT artigo(s)..."

# Converter e copiar
python -m obsidian_to_hugo \
    --obsidian-vault-dir="$VAULT_DIR/06-blog/published" \
    --hugo-content-dir="$HUGO_DIR/content/posts"

# Copiar imagens
find "$VAULT_DIR/06-blog/published" -name "*.png" -o -name "*.jpg" | while read img; do
    cp "$img" "$HUGO_DIR/static/images/"
done

# Build local para verificar
cd "$HUGO_DIR"
hugo --minify

echo "Build OK. Commitando..."
git add -A
git commit -m "publish: $(date +%Y-%m-%d) update"
git push

echo "Deploy triggered."
```

Registrar como git hook:
```bash
# Em .git/hooks/post-commit (do vault repo)
#!/bin/bash
bash scripts/obsidian-to-hugo.sh
```

## Deploy

### Cloudflare Pages (recomendado)

1. Conectar repo GitHub ao Cloudflare Pages
2. Build command: `cd hugo-site && hugo --minify`
3. Build output directory: `hugo-site/public`
4. Branch: `main`
5. Cloudflare faz build e deploy a cada push

### Netlify

1. Conectar repo GitHub ao Netlify
2. Build command: `cd hugo-site && hugo --minify`
3. Publish directory: `hugo-site/public`
4. Deploy automático a cada push

### Preview local

```bash
cd hugo-site
hugo server -D    # -D inclui drafts
# Abrir http://localhost:1313
```

## Conversão de wikilinks

O Obsidian usa `[[wikilinks]]` mas o Hugo espera links markdown padrão ou shortcodes.

| Obsidian | Hugo (após conversão) |
|----------|----------------------|
| `[[outra-nota]]` | `[outra-nota]({{< ref "outra-nota" >}})` |
| `[[nota\|texto]]` | `[texto]({{< ref "nota" >}})` |
| `![[imagem.png]]` | `![](imagem.png)` |
| `==destaque==` | `<mark>destaque</mark>` |

Se preferir não converter wikilinks (manter como referência interna), configure no filtro do obsidian-to-hugo para remover em vez de converter.

## Checklist de publicação

- [ ] Artigo está em `06-blog/published/`
- [ ] Frontmatter tem `publish: true` e `draft: false`
- [ ] Slug está definido e é URL-friendly
- [ ] Summary está preenchido (aparece em listagens)
- [ ] Tags e categories estão corretos
- [ ] Imagens estão referenciadas corretamente
- [ ] Wikilinks internos foram resolvidos ou removidos
- [ ] Preview local via `hugo server` está OK
- [ ] Nenhum dado sensível (FIN/FLAG pessoal) no artigo
