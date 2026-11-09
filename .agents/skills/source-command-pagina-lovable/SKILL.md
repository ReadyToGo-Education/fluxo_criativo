---
name: "source-command-pagina-lovable"
description: "Levar uma página HTML do projeto para o Lovable e devolver o link público. Com o conector do Lovable ligado no Claude, cria o projeto, confere e publica sozinho; sem o conector, entrega um prompt pronto para colar no Lovable. Skill de infraestrutura, última etapa do fluxo de página, depois de copy + performance + pixel + checkout."
---

# source-command-pagina-lovable

Use esta skill quando o usuário pedir o comando `/pagina-lovable` do workshop (ou `pagina-lovable`, sem a barra).

<!-- Gerado por scripts/exportar-para-codex.py a partir de .claude/commands/pagina-lovable.md. Não edite aqui: edite o original e rode o script de novo. -->

## Roteiro do comando

# Página Lovable. Publicação pelo conector do Lovable

Leva uma página HTML local para o Lovable e devolve o link público pronto pra usar em anúncios, bio e emails.

## Usage

```
/pagina-lovable
```

## O Que Fazer

Acione a skill `pagina-lovable` do plugin `workshop-marketing` e siga o roteiro:

1. Ler `meus-produtos/.ativo`. Se não houver produto, oriente a usar `/produto-novo`.
2. Se a página chama `fetch('/api/...')` (pre-checkout ou captura com função no servidor), parar e oferecer o `/pagina-vercel`: a função só roda lá.
3. Verificar se o conector do Lovable está ligado no Claude (ferramentas `create_project` e `deploy_project`). Se não estiver, mostrar como conectar (no Claude: + > Conectores > Procurar conectores > Lovable > Conectar) e oferecer as alternativas: prompt pronto para colar no Lovable ou `/pagina-vercel`.
4. Coletar (uma pergunta por vez): qual página, nome no Lovable, nova página ou atualização.
5. Mostrar resumo com conta e saldo de créditos e pedir confirmação. Avisar que o Lovable recria a página com a IA dele e que isso gasta créditos.
6. Com o conector: subir o HTML como anexo, criar o projeto (ou mandar a atualização), conferir pela imagem da tela que o conector devolve e, com a aprovação do aluno, publicar e pegar o endereço `.lovable.app`.
7. Sem o conector: montar o prompt pronto (até 50.000 caracteres), salvar em `entregas/paginas/{nome}-prompt-lovable.md` e guiar o aluno a colar no Lovable e publicar.
8. Salvar histórico em `meus-produtos/{ativo}/entregas/.lovable` e atualizar `meus-produtos/{ativo}/entregas/paginas/.lovable-link.md` com o link público.
9. Mostrar resumo final com URL pública e sugerir próximos passos: conferir no celular e usar o link no `/copy-anuncio` para tráfego pago.

## Regras Resumidas

- O Lovable não publica HTML pronto: ele recria a página com IA. Para cópia idêntica, o caminho é o `/pagina-vercel`.
- Não usar chave de API do Lovable: a API pública só republica projeto existente e exige plano Business ou Enterprise.
- Nunca pedir login/senha do Lovable no chat. O login acontece na tela do Lovable, ao conectar.
- Sempre confirmar antes de criar o projeto (gasta créditos) e antes de publicar.
- Não usar travessão em nenhum texto exibido.
