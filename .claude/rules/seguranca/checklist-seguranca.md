---
paths:
  - "meus-produtos/**/entregas/quiz/**"
  - "meus-produtos/**/entregas/apps/**"
  - "meus-produtos/**/entregas/paginas/api/**"
  - "meus-produtos/**/entregas/crm/**"
---

# Checklist de Segurança. Entregas que Gravam Dado

> Aplique este checklist a toda entrega que grava dado, tem login ou chama API de terceiro: prompt do Lovable (quiz, app), função no servidor (`api/*.js` na Vercel), formulário que manda lead para planilha, webhook ou CRM.
> Página HTML estática (vendas, captura sem formulário próprio, obrigado) só precisa do item 1.
> Se qualquer item que se aplica falhar: corrija o prompt ou o código antes de entregar ao aluno.

**Quem carrega este arquivo:** `/lt-quiz`, `/app-saas`, `/pagina-precheckout` e `/pagina-active`, antes de gerar. Toda skill nova que passe a gravar dado, ter login ou chamar API de terceiro também carrega.

**Como usar:** os blocos literais abaixo vão para dentro do prompt do Lovable ou viram o código da função. Depois de gerar, confira item por item da tabela. O aluno não vê este checklist nem ouve falar dele: ele recebe a entrega já segura.

---

## Os 10 itens

| # | Risco | Quando se aplica | Como cumprir |
|---|---|---|---|
| 1 | Chave secreta exposta no navegador | Sempre | Chave só no `.env` (local), nas variáveis de ambiente da Vercel ou nos secrets do Supabase. Em app Vite (todo app do Lovable é Vite), variável com prefixo `VITE_` vai para o navegador: nunca coloque chave secreta nela. Do Supabase, só a chave `anon` pode ir para o navegador; a `service_role` nunca. |
| 2 | Dado lido ou alterado por quem não devia (IDOR) | Banco com dado de usuário ou de lead | Row Level Security (RLS, a regra do banco que diz quem lê cada linha) ligada em todas as tabelas, negando tudo por padrão. Lead de funil: visitante anônimo nunca lê, edita nem apaga. Dado de usuário logado: `user_id = auth.uid()`. |
| 3 | Área de admin aberta | Painel admin, área restrita | Esconder a rota é só visual. A proteção real é a RLS por perfil e a conferência dentro das funções do servidor. Admin entra com login do Supabase Auth, nunca com senha escrita no código. Ninguém vira admin sozinho no cadastro (nem "o primeiro a se cadastrar", nem "quem usar tal e-mail"): o criador cria a própria conta e depois se promove pelo chat do Lovable. Usuário comum nunca altera o próprio perfil de acesso (`role`). Ação que exige privilégio (excluir usuário, exportar leads) roda em função do servidor que confere se quem pediu é admin. |
| 4 | Entrada sem validação | Todo campo que o visitante preenche | Validar no navegador (para a experiência) e de novo no servidor (para a segurança): restrições no banco (`not null`, `check` de tamanho e formato) ou validação na função. O servidor nunca confia em valor vindo do navegador para decidir lista, tag, preço, destino ou perfil de acesso: esses valores ficam fixos no servidor. |
| 5 | Injeção de SQL | Banco | Só consultas pelo cliente do Supabase (`.eq()`, `.insert()`, `.match()`), nunca texto do usuário colado dentro de SQL. Função SQL com consulta montada na hora usa parâmetros. |
| 6 | Injeção de prompt | App que manda texto do usuário para uma IA | Instruções do sistema separadas do texto do usuário. A IA nunca recebe chave nem dados de outros usuários. Resposta da IA não dispara sozinha ação que apaga, envia, cobra ou muda permissão. |
| 7 | XSS (script malicioso rodando na página) | Tela que mostra texto digitado por alguém | Mostrar texto como texto. No React, nunca `dangerouslySetInnerHTML` com conteúdo vindo de usuário ou lead. Em HTML puro, `textContent` no lugar de `innerHTML`. |
| 8 | SSRF (servidor buscando um endereço escolhido pelo usuário) | Função que busca um link colado pelo usuário | Aceitar só domínios de uma lista fechada (ex: `instagram.com`) e recusar endereço interno (`localhost`, `127.0.0.1`, `10.*`, `192.168.*`, `169.254.*`). Se o app não busca link do usuário, não se aplica. |
| 9 | Abuso de envios (robô, spam, derrubar o app) | Formulário público, login, cadastro, função do servidor | Honeypot: campo escondido que só robô preenche; se vier preenchido, responder sucesso sem gravar. Limite de envios por IP na função ou no firewall da hospedagem. No login e no cadastro: o Supabase Auth já limita tentativas; ligar a verificação de senha vazada (Password HIBP check). O Lovable Cloud não tem captcha nativo, então não prometa captcha ao aluno. |
| 10 | Mensagem de erro que vaza informação | Toda tela e função com servidor | O visitante vê mensagem genérica ("Não foi possível enviar agora. Tente de novo em instantes."). Detalhe técnico só no log do servidor. Login responde "E-mail ou senha incorretos" nos dois casos, sem dizer se o e-mail existe: assim ninguém descobre quem é cliente testando e-mails. |

**Senha:** quem guarda é o Supabase Auth, que já grava com hash. Nunca criar tabela própria de senha nem guardar senha em texto.

---

## Bloco literal. Prompt do Lovable para funil sem login que grava lead (quiz)

Colar no prompt técnico, na seção de segurança:

> "Regras de segurança obrigatórias. O quiz é público, o visitante não faz login e o funil grava dados pessoais de leads (nome, e-mail, telefone). Siga todas:
>
> 1. Ativar Row Level Security (RLS) em todas as tabelas. Nenhuma política pode permitir que o visitante anônimo leia, edite ou apague linhas de `leads` ou `funnel_events`.
>
> 2. Cada resposta e cada avanço de etapa do visitante é gravado em `funnel_events` (`session_id`, `etapa`, `resposta`, `created_at`), somente com INSERT. A política de INSERT para anônimo existe só nessa tabela e confere os limites no próprio `WITH CHECK` (nunca `WITH CHECK (true)`): `etapa` dentro da lista fechada de etapas do funil, `session_id` com até 64 caracteres, `resposta` com até 200 caracteres. As mesmas regras também ficam como restrições da tabela. Nenhum dado pessoal nessa tabela.
>
> 3. A linha em `leads` nasce uma única vez, no envio do modal de pré-checkout, por uma Supabase Edge Function chamada `registrar-lead`. O navegador nunca grava direto em `leads`, e a tabela não tem política de INSERT para anônimo. A função:
>    a. valida cada campo no servidor: nome com até 100 caracteres, e-mail em formato válido com até 254 caracteres, telefone só com números e 10 ou 11 dígitos;
>    b. se o campo escondido `website` vier preenchido, responde sucesso e não grava nada (é robô);
>    c. aceita no máximo 5 envios do mesmo IP a cada 10 minutos, guardando só o hash do IP, nunca o IP puro;
>    d. usa a service_role key apenas dentro da função, lida das variáveis de ambiente do Supabase;
>    e. em qualquer erro, devolve só a mensagem 'Não foi possível enviar agora. Tente de novo em instantes.' e registra o detalhe no log da função.
>
> 4. O modal de pré-checkout tem um campo `website` escondido (fora da tela por CSS, `tabindex=-1`, `autocomplete=off`, `aria-hidden=true`). Pessoas não veem nem preenchem esse campo.
>
> 5. Painel administrativo em `/admin`, protegido por Supabase Auth com e-mail e senha, com tela de login e de criação de conta. Criar a tabela `admins` (`user_id` uuid, chave primária, referencia `auth.users(id)` com `on delete cascade`), com RLS ativada e nenhuma política: ninguém lê nem grava nela pelo app. Criar a função `public.is_admin()` em SQL, com `security definer`, `stable` e `set search_path = public`, que devolve verdadeiro só quando `auth.uid()` está em `admins`. Ninguém vira admin automaticamente: quem cria conta em `/admin` sem estar em `admins` vê a mensagem 'Sua conta ainda não tem acesso ao painel.' e nenhum dado. As políticas de SELECT de `leads` e `funnel_events` usam `public.is_admin()`. Esconder o menu é só visual; a proteção real é essa política. Nenhuma senha escrita no código.
>
> 6. Exportação de leads (CSV) só aparece e só funciona para quem passa em `public.is_admin()`.
>
> 7. Nenhuma chave secreta no código do frontend nem em variável com prefixo `VITE_`. No frontend vai apenas a anon key pública do Supabase.
>
> 8. Textos digitados pelo visitante aparecem no painel como texto puro. Nunca usar `dangerouslySetInnerHTML`.
>
> 9. Toda mensagem de erro mostrada ao visitante ou ao admin é genérica. Nunca exibir a mensagem crua do banco, da função ou do Supabase."

---

## Bloco literal. Prompt do Lovable para app com login

Colar no prompt técnico, no bloco de segurança:

> "Regras de segurança obrigatórias:
>
> 1. Nenhuma chave secreta, token de API de terceiros ou credencial pode aparecer no código do frontend nem em variável com prefixo `VITE_`, porque tudo que começa com `VITE_` vai para o navegador. Chamadas que exigem chave ficam em Supabase Edge Functions, e o frontend chama via `supabase.functions.invoke()`.
>
> 2. Nunca expor a `service_role` key do Supabase no frontend. Usar apenas a `anon` key pública. Operações com privilégio elevado ficam em Edge Functions, com a `service_role` key lida das variáveis de ambiente do Supabase, e cada uma confere se quem pediu é admin antes de agir.
>
> 3. Ativar Row Level Security (RLS) em TODAS as tabelas. Nenhuma tabela fica com RLS desativado. Cada tabela tem políticas explícitas para SELECT, INSERT, UPDATE e DELETE: negar tudo por padrão e liberar só o necessário. Dados de um usuário nunca são acessados por outro: as políticas usam `auth.uid()`, por exemplo `USING (user_id = auth.uid())`.
>
> 4. Validar os dados no servidor, além do formulário: restrições no banco (`not null`, `check` de tamanho e formato) em todo campo que o usuário preenche. Nunca confiar em valor vindo do navegador para decidir permissão, preço ou dono do registro.
>
> 5. Inputs do usuário nunca são concatenados em queries. Usar sempre os métodos do Supabase client (`.eq()`, `.filter()`, `.match()`), nunca interpolação de texto em SQL.
>
> 6. Textos digitados pelo usuário aparecem na tela como texto puro. Nunca usar `dangerouslySetInnerHTML` com conteúdo vindo de usuário.
>
> 7. Mensagens de erro: o usuário vê sempre mensagem genérica, nunca a mensagem crua do banco ou do Supabase. No login, responder 'E-mail ou senha incorretos' tanto para e-mail inexistente quanto para senha errada. No cadastro, não revelar se o e-mail já tem conta.
>
> 8. Não guardar tokens, chaves ou dados sensíveis em `localStorage` ou `sessionStorage`, além da sessão que o próprio Supabase Auth já gerencia.
>
> 9. Se o app mandar texto do usuário para uma IA: manter as instruções do sistema separadas do texto do usuário, nunca enviar chave nem dados de outros usuários para a IA e nunca deixar a resposta da IA executar sozinha ação que apaga, envia ou muda permissão.
>
> 10. Se alguma Edge Function buscar um link informado pelo usuário: aceitar só domínios de uma lista fechada e recusar endereços internos (localhost, 127.0.0.1, 10.*, 192.168.*, 169.254.*)."

---

## Função no servidor (Vercel, `api/*.js`). Requisitos mínimos

Toda função que o Severino gera para receber formulário (`api/lead.js`, `api/active-sync.js` e futuras) segue estes pontos:

0. **Onde ela funciona.** A função só existe se for publicada pelo `/pagina-vercel`, no mesmo projeto e no mesmo deploy da página que a chama. Página publicada em outro lugar (Lovable, WordPress, página da Hotmart) não tem `/api/` e o formulário não envia. Confirme com o aluno onde a página vai ficar antes de escolher o modo com função.
   - Formato: arquivo `.js` com `export default async function handler(req, res)`. Esse formato roda na Vercel sem `package.json` e sem configuração extra. Sem dependências de npm: use o `fetch` que já vem no Node.
   - Leia `req.body` dentro de `try/catch`: corpo malformado gera erro na leitura.
   - IP do visitante: header `x-forwarded-for` (a Vercel sobrescreve esse header, então ele é confiável).

1. Aceita só `POST`. Outro método responde `405`.
2. Valida cada campo do corpo: tipo, tamanho e formato. Campo inválido responde `400` com mensagem genérica.
3. Honeypot: se o campo `website` vier preenchido, responde `200` e não grava nada.
4. Valores que decidem destino (lista, tag, planilha, webhook, preço) vêm de `process.env`, nunca do corpo do pedido.
5. Chaves e URLs privadas (webhook, Apps Script, API de CRM) só em `process.env`. A página chama a função; a função chama o destino. A URL do destino nunca aparece no HTML.
6. Tudo dentro de `try/catch`. No erro: `console.error` com o detalhe e resposta `500` com `{ "ok": false, "mensagem": "Não foi possível enviar agora. Tente de novo em instantes." }`.
7. Variáveis de ambiente: o `/pagina-vercel` cadastra no projeto da Vercel, com a confirmação do aluno, e publica de novo. A Vercel só entrega a variável à função depois de um novo deploy.
8. Limite de envios: regra no firewall do projeto na Vercel (o `/pagina-vercel` orienta), por IP, para Request Path começando com `/api/`, 5 envios por minuto. O plano grátis da Vercel permite uma regra de limite por projeto, por isso a regra cobre todas as funções de uma vez. A regra vale na hora, sem novo deploy.
9. Destino Google Sheets: o Apps Script precisa estar publicado como app da web com acesso "Qualquer pessoa". Sem isso, a chamada cai numa tela de login e o lead não é gravado, mesmo parecendo que deu certo.

No HTML que chama a função: mostrar ao visitante só a mensagem genérica, nunca o texto do erro devolvido.
