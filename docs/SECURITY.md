# SECURITY.md — Criptografia e segurança do vault

> Modelo de ameaças, configuração de criptografia em camadas, classificação de dados, e procedimentos de backup.

## Modelo de ameaças

O vault contém dados financeiros pessoais, estratégias de internacionalização, e informações sobre ativos. As ameaças relevantes são:

| Ameaça | Vetor | Impacto | Mitigação |
|--------|-------|---------|-----------|
| Acesso físico ao dispositivo | Roubo/perda do laptop | Exposição total | Full-disk encryption (LUKS/FileVault/BitLocker) |
| Acesso ao repositório remoto | Comprometimento do GitHub/GitLab | Exposição de notas | git-crypt (arquivos criptografados at rest no remote) |
| Interceptação em trânsito | Man-in-the-middle | Exposição parcial | SSH para git (não HTTPS), TLS para APIs |
| Vazamento via API de IA cloud | Envio de dados sensíveis para LLM | Exposição de dados financeiros | Ollama local para FIN e FLAG; cloud só para ENG/EDU/VIT |
| Perda da chave de criptografia | Falha de backup | Perda permanente do vault remoto | Backup da chave em 3 locais independentes |
| Comprometimento do Obsidian plugin | Plugin malicioso | Exfiltração de dados | Auditar plugins, mínimo necessário, verificar código-fonte |

## Classificação de dados por domínio

| Domínio | Sensibilidade | Dados sensíveis típicos | IA permitida |
|---------|--------------|------------------------|--------------|
| FIN | **Alta** | Saldos, posições, CPF, contas bancárias, estratégia de alocação | Ollama local APENAS |
| FLAG | **Alta** | Dados de passaporte, números de conta offshore, planos de residência | Ollama local APENAS |
| ENG | Baixa | Código, artigos técnicos, anotações | Cloud via OpenRouter OK |
| EDU | Baixa | Notas de leitura, fichamentos | Cloud via OpenRouter OK |
| VIT | Baixa | Receitas, degustações, cotações públicas de metais | Cloud via OpenRouter OK |

**Exceção para VIT:** Notas sobre metais preciosos que contenham quantidades pessoais possuídas ou locais de armazenamento são reclassificadas como Alta sensibilidade.

## Criptografia em camadas

### Camada 1: Disco (at rest local)

Protege contra acesso físico ao dispositivo.

**Linux:**
```bash
# Verificar se LUKS está ativo
lsblk -f
# A partição deve mostrar "crypto_LUKS"
```

**Mac:**
```bash
# Verificar FileVault
fdesetup status
# Deve retornar "FileVault is On."
```

**Windows:**
```powershell
# Verificar BitLocker
manage-bde -status
```

### Camada 2: Git (at rest no remote)

Protege os arquivos no GitHub/GitLab. Usa git-crypt com GPG.

**Setup inicial (uma vez):**
```bash
cd pke/
git init
git-crypt init

# Opção A: Chave simétrica (mais simples)
git-crypt export-key ~/pke-vault-key.bin
# BACKUP ESSA CHAVE IMEDIATAMENTE

# Opção B: GPG (recomendado — integra com commits assinados)
git-crypt add-gpg-user SEU_EMAIL@example.com
```

**Arquivo .gitattributes:**
```gitattributes
# Criptografar conteúdo do vault
vault/**/*.md filter=git-crypt diff=git-crypt
vault/**/*.canvas filter=git-crypt diff=git-crypt
vault/**/*.png filter=git-crypt diff=git-crypt
vault/**/*.jpg filter=git-crypt diff=git-crypt
vault/**/*.pdf filter=git-crypt diff=git-crypt

# Criptografar configs com dados sensíveis
collector/sources.yaml filter=git-crypt diff=git-crypt
collector/db/*.db filter=git-crypt diff=git-crypt

# NÃO criptografar (precisam ser legíveis no remote)
README.md !filter !diff
CLAUDE.md !filter !diff
GUIDELINES.md !filter !diff
CONTRIBUTING.md !filter !diff
SECURITY.md !filter !diff
SOURCES.md !filter !diff
PUBLISHING.md !filter !diff
ARCHITECTURE.md !filter !diff
.gitattributes !filter !diff
.gitignore !filter !diff
collector/**/*.py !filter !diff
hugo-site/** !filter !diff
scripts/** !filter !diff
```

**Verificar:**
```bash
git-crypt status
# Todos os *.md do vault devem mostrar "encrypted"
# Docs do root devem mostrar "not encrypted"
```

**Clonar em outro dispositivo:**
```bash
git clone <repo-url> pke
cd pke

# Com chave simétrica:
git-crypt unlock /path/to/pke-vault-key.bin

# Com GPG (se a chave GPG está no keyring):
git-crypt unlock
```

### Camada 3: Notas individuais (seções sensíveis)

Para dados extremamente sensíveis DENTRO de uma nota (números de conta, senhas, CPF).

Plugin: **Obsidian Encrypt** (meld-cp)
- Criptografa seções específicas com AES-256
- Seções criptografadas ficam como blocos `%%ENCRYPTED%%...%%`
- IA NÃO consegue ler — isso é intencional
- Útil para: dados bancários em notas FIN, dados de passaporte em notas FLAG

Plugin: **Cryptsidian** (vault inteiro)
- Criptografa TODAS as notas com senha
- Usar ao "trancar" o vault quando sair do computador
- Decriptar ao voltar
- NÃO usar durante sessões de trabalho (impede IA e sync)

## Backup da chave de criptografia

A chave do git-crypt é o ponto único de falha. Procedimento de backup:

| Local | Método | Acesso |
|-------|--------|--------|
| Pendrive criptografado | Arquivo `.bin` em pendrive com VeraCrypt | Físico, guardado em local seguro |
| Password manager | Upload da chave como "secure note" no Bitwarden/1Password | Cloud, protegido por master password + 2FA |
| Cópia offline | Impresso como QR code ou base64 em papel, guardado em cofre | Físico, disaster recovery |

**Teste de recovery (fazer periodicamente):**
```bash
# Em uma máquina limpa ou VM:
git clone <repo-url> pke-test
cd pke-test
git-crypt unlock /path/to/backup-key.bin
# Verificar que os .md estão legíveis
cat vault/01-financas/_index.md
```

## Segurança dos plugins Obsidian

Regras para instalação de plugins:
- Somente plugins do Community Plugins oficial do Obsidian
- Verificar código-fonte no GitHub antes de instalar (especialmente plugins de IA)
- Preferir plugins com mais de 1000 downloads e manutenção ativa
- NUNCA instalar plugins de fontes não verificadas via BRAT sem auditar
- Plugins com acesso a rede devem ser justificados (IA, sync, git)

## .gitignore recomendado

```gitignore
# Obsidian internos (não precisam de sync)
vault/.obsidian/workspace.json
vault/.obsidian/workspace-mobile.json
vault/.obsidian/cache/

# Sistema
.DS_Store
Thumbs.db
*.swp
*.swo

# Chaves (NUNCA commitar)
*.bin
*.key
*.pem

# SQLite WAL (transiente)
collector/db/*.db-wal
collector/db/*.db-shm

# Hugo build output
hugo-site/public/
hugo-site/resources/

# Python
__pycache__/
*.pyc
.venv/
```

## Checklist de segurança (revisar mensalmente)

- [ ] Full-disk encryption ativa no dispositivo principal
- [ ] git-crypt status mostra arquivos do vault como encrypted
- [ ] Backup da chave em pelo menos 2 locais independentes
- [ ] Teste de recovery feito nos últimos 3 meses
- [ ] Plugins do Obsidian atualizados
- [ ] Nenhum plugin novo instalado sem verificação
- [ ] Dados FIN e FLAG não foram enviados para APIs cloud
- [ ] GPG key não expirou
- [ ] 2FA ativo no GitHub/GitLab
- [ ] Repositório remoto é PRIVADO
