---
name: workshop-marketing:configurar-replicate
description: Guia para criar conta no Replicate (via GitHub), gerar o API Token e salvar no .env como REPLICATE_API_TOKEN. Skill reutilizável chamada por qualquer skill que anime criativos via API (sub-fluxo Animar em loop do /criativo-estatico).
allowed-tools: Read, Edit, Bash
model: sonnet
---

# Configurar Replicate

Guia para criar a conta, gerar o token e salvar no `.env`. Só precisa fazer uma vez.

O Replicate é a plataforma que anima os criativos direto pelo chat (image-to-video). Funciona por crédito pré-pago: você adiciona um valor pequeno (a partir de uns dólares) e cada vídeo de loop consome centavos. Sem mensalidade.

**Público não técnico:** conduza cada passo com calma, um por vez. Nunca peça para o aluno editar arquivo nenhum. Quem organiza o `.env` é você.

---

## Passo 1. Conta no GitHub (pré-requisito)

O Replicate só aceita cadastro com conta do GitHub. Pergunte:

```
Você já tem conta no GitHub?

1. Sim, já tenho
2. Não tenho ainda
```

**Se não tiver:** instrua, um passo por vez:

```
Vamos criar sua conta do GitHub (é gratuita):

1. Acesse https://github.com/signup
2. Digite seu email e clique em Continue
3. Crie uma senha e escolha um nome de usuário
4. Confirme o código de verificação que chega no seu email

Quando terminar, me avise que seguimos.
```

**Se já tiver:** avance para o Passo 2.

---

## Passo 2. Criar a conta no Replicate

Instrua:

```
Agora a conta do Replicate:

1. Acesse https://replicate.com/signin
2. Clique em "Sign in with GitHub"
3. Autorize o acesso quando o GitHub pedir

Quando estiver logado, me avise.
```

---

## Passo 3. Gerar o API Token

Instrua:

```
Para gerar sua chave:

1. Clique na sua foto de perfil (canto superior esquerdo)
2. Clique em "API tokens"
3. Digite um nome pra chave (ex: severino) e clique em "Create token"
4. Copie o token gerado (começa com r8_)
```

Peça o token:

```
Cole o token aqui no chat que eu guardo pra você:
```

---

## Passo 4. Testar o token

Rode o teste de conexão com o valor informado:

```bash
curl -s -H "Authorization: Bearer {TOKEN_INFORMADO}" "https://api.replicate.com/v1/account" | head -c 300
```

- Se retornar `{"type":...,"username":...}`: token válido, continua.
- Se retornar `{"detail":"Invalid token..."}` ou erro 401: token inválido ou copiado com espaço. Peça para verificar e colar de novo. Repita o Passo 3.

**Mascaramento obrigatório:** nunca ecoar o token de volta no chat. Ao exibir o comando de teste, mostrar `***TOKEN_MASCARADO***` no lugar do valor.

---

## Passo 5. Salvar no .env

Leia o `.env` da raiz do projeto.

- Se a linha `REPLICATE_API_TOKEN` já existir: atualize o valor com Edit.
- Se não existir: adicione `REPLICATE_API_TOKEN={valor}` ao final do arquivo.

O nome padrão obrigatório da variável é `REPLICATE_API_TOKEN`. Não usar variação diferente desse nome.

Confirme ao aluno (sem mostrar o valor):

```
✅ Chave do Replicate salva e testada com sucesso. Você não precisa fazer mais nada, daqui pra frente eu uso ela automaticamente pra animar seus criativos.
```

---

## Passo 6. Crédito (se a animação falhar por saldo)

Se ao animar aparecer erro de pagamento ou crédito insuficiente, instrua:

```
Falta crédito na sua conta do Replicate. Pra adicionar:

1. Acesse https://replicate.com/account/billing
2. Clique em "Add credit" e escolha um valor (10 dólares já rendem dezenas de vídeos)
```

---

## Após configurar

Retorne ao fluxo que chamou esta skill (ex: sub-fluxo "Animar em loop" do `/criativo-estatico`) e continue de onde parou.
