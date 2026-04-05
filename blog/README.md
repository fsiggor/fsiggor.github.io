# Blog

Personal blog built with [Hugo](https://gohugo.io/) + [Hextra](https://imfing.github.io/hextra/) theme, deployed via GitHub Pages.

## Setup

### Docker (recommended)

From the repo root:

```bash
docker compose up blog
```

Site available at http://localhost:1313/ with hot reload. No local Hugo installation needed.

### Without Docker

```bash
cd blog
hugo server -D
```

Requires [Hugo](https://gohugo.io/) 0.159.1+ (extended).

## Writing content

Blog posts go in `content/blog/`. Create a new post:

```bash
hugo new blog/my-post.md
```

Each post uses YAML frontmatter (`---`). See `archetypes/default.md` for the template.

## Build for production

```bash
hugo --minify
```

Output goes to `public/`. The CI/CD pipeline (`deploy.yml`) handles this automatically on push to `main`.

## Project structure

```
blog/
├── archetypes/
│   └── default.md        # Frontmatter template for new posts
├── content/
│   ├── _index.md         # Landing page
│   └── blog/
│       ├── _index.md     # Blog listing page
│       └── *.md          # Blog posts
├── layouts/
│   └── partials/         # Custom Hugo partials
├── static/               # Static assets (images, etc.)
├── go.mod                # Hugo module (Hextra theme)
├── go.sum
└── hugo.toml             # Hugo configuration
```
