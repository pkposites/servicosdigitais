# RDA Serviços Digitais — Documentação para subir as campanhas no Meta com Claude

Use este arquivo em um chat dedicado a campanhas. Cole o **Prompt de abertura** (seção 12) no início do chat e anexe este arquivo e as 4 imagens de `assets/ads/`.

Última atualização: 2026-11-08.

---

## 1. Resumo da operação

- **Objetivo:** gerar pedidos de orçamento todos os dias de quem precisa de serviços digitais e não sabe fazer sozinho.
- **Estrutura:** 1 campanha de Leads, 4 conjuntos de anúncios (um por oferta), 1 anúncio inicial por conjunto.
- **Verba:** mínimo possível por conjunto, teto total de **R$ 29,00/dia**.
- **Destino:** landing page `https://servicos-digitais.netlify.app/`, na âncora da oferta. O formulário (nome, serviço, WhatsApp) dispara o evento **Lead** e abre o WhatsApp.
- **Meta do teste:** "só ver no que dá". Cortar o que não gerar lead e manter o que gerar.

## 2. Contas e IDs

| Item | Valor | Observação |
|---|---|---|
| Conta de anúncios | **ADVANCED TRAFFIC - QVN Ads** — `298240176211615` | BRL, ativa, com forma de pagamento. |
| Business Manager | QVN ADS — `267023785456566` | |
| Pixel / dataset | **Serviços** — `2018578222100683` | Já instalado na LP. Outros datasets na conta: Segredo, Projects, Dados CRM Controlead. **Não usar.** |
| Mínimo diário por conjunto | **R$ 5,49** (`min_daily_budget_cents: 549`) | Vem da API da conta. |
| WhatsApp de destino | `55 11 99191-2707` | Já configurado na LP. |
| Página do Facebook | **A DEFINIR** | Ver seção 3. |

> A conta do Meta do usuário dá acesso a dezenas de contas de outros clientes. **Operar somente na conta `298240176211615`.** Nunca criar, editar ou ativar nada em outra conta.

## 3. Pendências antes de ativar

1. **Página do Facebook.** Nenhuma se chama "RDA Serviços Digitais". As páginas ligadas à conta são: Segredo do nome (`102055919325414`), Mais Seguro (`818083418050920`), MultipliCoisas (`218434654688743`), PkPoeta - MC Piruka (`215731248294926`) e PK Poeta (`1615415575368542`). Sugestão: criar a página "RDA Serviços Digitais" e ligá-la à conta, ou usar a PK Poeta. Anúncio de site (objetivo Leads com conversão no site) não exige aceite dos termos de formulário instantâneo, mas confirme na criação.
2. **Perfil do Instagram** que vai aparecer nos anúncios (opcional, mas melhora a aparência).
3. **Teste real da LP no celular:** enviar o formulário uma vez e conferir se o Lead aparece no Pixel (Gerenciador de Eventos) e na cadeolead.
4. **Netlify Forms está desativado** no site. Não é obrigatório, porque a cadeolead captura os leads, mas ligue em Site configuration → Forms se quiser um backup.
5. **Preço "a partir de R$ 337"** não está na página. Só publicar depois de definir escopo do pacote e quem paga o domínio.

## 4. Estrutura da campanha

**Campanha:** `RDA | Leads | Serviços Digitais | 2026-11`
- Objetivo: **Vendas/Leads → Leads** (`OUTCOME_LEADS`).
- Local de conversão: **site**.
- Evento de otimização: **Lead** do Pixel `2018578222100683`.
- Orçamento no nível do **conjunto** (sem CBO), para cada oferta ter a mesma chance de entregar.
- Status ao criar: **PAUSADA**. Só ativar depois da revisão do usuário.

**Conjuntos de anúncios** (verba mínima de R$ 5,49/dia cada, total R$ 21,96/dia, folga de R$ 7,04 dentro do teto):

| # | Conjunto | Âncora da LP | Imagem do anúncio |
|---|---|---|---|
| 1 | `Página para bio` | `#pagina-bio` | `assets/ads/ad-pagina-bio.webp` |
| 2 | `Landing page` | `#landing-page` | `assets/ads/ad-landing-page.webp` |
| 3 | `Configuração de anúncios` | `#configuracao-anuncios` | `assets/ads/ad-configuracao-anuncios.webp` |
| 4 | `Artes e vídeos` | `#artes-e-videos` | `assets/ads/ad-artes-e-videos.webp` |

**Público (igual nos 4 conjuntos):**
- Brasil, 22 a 55 anos, todos os gêneros, idioma português.
- Sem interesses (segmentação aberta). Comparar ofertas com o mesmo público dá leitura limpa.
- Posicionamentos: **Advantage+ (automáticos)**, ou apenas Feed e Reels se quiser controlar. As artes são **4:5** (1122×1402). O Meta pode cortar no Stories e no Reels. Se aparecer corte ruim na prévia, restringir a Feed.
- Início: imediato, sem data de término.

## 5. Links de destino (um por anúncio)

Colocar os parâmetros **antes** do `#`. Assim a âncora e as UTMs funcionam juntas.

```
https://servicos-digitais.netlify.app/?utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}#pagina-bio
https://servicos-digitais.netlify.app/?utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}#landing-page
https://servicos-digitais.netlify.app/?utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}#configuracao-anuncios
https://servicos-digitais.netlify.app/?utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}#artes-e-videos
```

- Se a API recusar as chaves `{{...}}`, usar os nomes fixos, por exemplo `utm_campaign=rda-leads-2026-11&utm_term=pagina-bio`.
- A LP grava `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` e `fbclid` junto com cada lead.
- **Teste obrigatório:** abrir cada link no celular. A página deve chegar ao título da oferta (sem o cabeçalho cobrindo) e o formulário deve vir com o serviço já escolhido.
- Links antigos continuam valendo: `#setup-trafego` abre a configuração de anúncios.

## 6. Textos dos anúncios

Linguagem simples, sem promessa de resultado. Botão: **Solicitar orçamento** (`GET_QUOTE`). Se não estiver disponível, usar **Saiba mais** (`LEARN_MORE`).

### Anúncio 1 — Página para bio
- **Texto principal:** Seu Instagram tem seguidores, mas falta um lugar que mostre tudo o que você faz? Criamos uma página personalizada para a sua bio, com seus serviços, trabalhos e botão de WhatsApp. Peça seu orçamento.
- **Título:** Seu negócio inteiro na bio
- **Descrição:** Página personalizada com acesso ao WhatsApp

### Anúncio 2 — Landing page
- **Texto principal:** Vai anunciar uma oferta e precisa de uma página só para ela? Criamos landing pages que apresentam o seu serviço, respondem as dúvidas e levam o cliente ao WhatsApp. Peça seu orçamento.
- **Título:** Uma página para a sua oferta
- **Descrição:** Apresente seu serviço e receba contatos pelo WhatsApp

### Anúncio 3 — Configuração de anúncios
- **Texto principal:** Quer anunciar e não sabe por onde começar? A gente configura sua conta de anúncios e suas campanhas: estrutura, eventos de conversão e teste. Serviço pontual. Peça seu orçamento.
- **Título:** Configuramos seus anúncios
- **Descrição:** Campanha configurada e rastreamento testado

### Anúncio 4 — Artes e vídeos
- **Texto principal:** Precisa de criativos para anunciar? A gente cria suas artes e vídeos para divulgar a sua oferta. Peça seu orçamento.
- **Título:** Artes e vídeos para anúncios
- **Descrição:** Criativos feitos para divulgar sua oferta

**Regras de conteúdo:** não prometer ganho, prazo, número de leads, desconto nem preço. Não citar "garantido". Não usar antes e depois. As artes estão marcadas como ilustração onde for o caso.

## 7. Criativos (arquivos)

| Arquivo | Oferta | Observação |
|---|---|---|
| `assets/ads/ad-pagina-bio.webp` | Página para bio | Traz a etiqueta "Ilustração". |
| `assets/ads/ad-landing-page.webp` | Landing page | |
| `assets/ads/ad-configuracao-anuncios.webp` | Configuração de anúncios | |
| `assets/ads/ad-artes-e-videos.webp` | Artes e vídeos | |
| `assets/vsl-rda-web.mp4` | Vídeo institucional, 34s, 9:16, sem áudio | Opcional. Pode virar um quinto anúncio para teste em Reels. |

Todas as artes têm 1122×1402 px (4:5). Para subir pela API, o Claude precisa ter acesso ao arquivo local. No chat dedicado, anexe as imagens, ou rode o chat dentro do repositório `pkposites/servicosdigitais`.

## 8. Rastreamento (já instalado na LP)

| Evento | Quando dispara | Dados enviados |
|---|---|---|
| `PageView` | Ao abrir a página | — |
| `OfferView` (personalizado) | Ao chegar por link direto de oferta | `service` |
| `CTAClick` (personalizado) | Clique em botão de oferta | `service` |
| `LinkClick` (personalizado) | Clique em "Ver os serviços" e "Ver página real" | `link` |
| **`Lead`** (padrão) | Envio do formulário | `content_name` (serviço), `content_category` (chave da oferta) |
| `WhatsAppClick` (personalizado) | Clique no link direto de WhatsApp | `service: geral` |

- **Otimizar para `Lead`.** Os demais eventos servem para análise.
- O script da **cadeolead** (`cadeolead.com.br/tracker.js`) está no `<head>` e captura os dados dos leads para planilha, podendo devolver as vendas à Meta pela API de Conversões. O banner de consentimento é dele.
- O Pixel da Meta carrega sem esperar o aceite do banner. Se quiser disparar só após o aceite, é uma alteração na LP.

## 9. Passo a passo para o Claude executar

Ferramentas do Meta MCP previstas (as três primeiras foram testadas nesta conta; as demais existem no MCP e devem ser validadas ao usar): `ads_get_ad_accounts`, `ads_get_datasets`, `ads_get_ad_account_pages`, `ads_get_field_context`, `ads_create_campaign`, `ads_create_ad_set`, `ads_creative_upload_local_image` ou `ads_creative_upload_media`, `ads_create_creative`, `ads_create_ad`, `ads_get_ad_preview`, `ads_get_ad_entities`, `ads_update_entity`, `ads_activate_entity`. Toda chamada exige `client_conversation_id` (20 caracteres alfanuméricos, o mesmo durante o chat) e `client_model`.

1. **Conferir o ambiente:** `ads_get_ad_accounts` → confirmar que `298240176211615` está ACTIVE, `is_queryable: true`. `ads_get_datasets` → confirmar o Pixel `2018578222100683` ativo. `ads_get_ad_account_pages` → confirmar a página escolhida pelo usuário.
2. **Conferir o Lead:** consultar estatísticas do dataset (`ads_get_dataset_stats`) e ver se o evento Lead já chegou. Se não, pedir ao usuário o teste do formulário antes de seguir.
3. **Mostrar o plano e pedir confirmação** (nomes, verbas, público, links, textos).
4. **Criar a campanha pausada.**
5. **Criar os 4 conjuntos pausados**, com R$ 5,49/dia cada, mesmo público, otimização por Lead no Pixel. Usar `ads_get_field_context` para validar campos e valores antes de enviar.
6. **Subir as 4 imagens** e criar os criativos com os textos da seção 6 e os links da seção 5.
7. **Criar os 4 anúncios pausados** e gerar as prévias (`ads_get_ad_preview`) para o usuário revisar.
8. **Revisão do usuário.** Só depois da confirmação explícita, ativar (`ads_activate_entity`), começando pela campanha e depois pelos conjuntos.
9. **Após ativar:** conferir o status de entrega, possíveis reprovações (`ads_get_errors`) e a verba total no painel (≤ R$ 29,00/dia).

## 10. Como ler os resultados e decidir

Com R$ 5,49/dia por conjunto, o volume é baixo. O Meta provavelmente mostrará "fase de aprendizado limitada", porque ela pede cerca de 50 conversões por semana por conjunto. Isso é esperado neste teste. Por isso, decidir por sinais simples:

- **Janela mínima:** 7 dias, sem mexer em público, verba ou criativo nesse período.
- **Métricas por conjunto:** gasto, impressões, cliques no link, custo por clique, leads (evento `Lead`), custo por lead e, na planilha da cadeolead, leads reais vs. curiosos.
- **Corte:** conjunto com gasto acima de R$ 40 (cerca de 7 dias) e zero leads → pausar.
- **Manter/escalar:** conjunto com lead mais barato e conversa qualificada no WhatsApp → subir a verba aos poucos (até 20% por vez) usando a folga do teto.
- **Criativo:** CTR baixo (menos de 0,7%) com custo por clique alto → trocar a arte ou o texto, um por vez.
- **Qualidade:** o que vale é a venda. Registrar no WhatsApp quem virou cliente e devolver à cadeolead para otimizar por venda no futuro.

## 11. Segurança e limites

- Nunca ativar nada sem a confirmação do usuário na conversa.
- Nunca exceder **R$ 29,00/dia** no total.
- Nunca mexer em outra conta, página ou Pixel.
- Não alterar a LP nem o Pixel dentro do chat de campanhas.
- Se a API recusar algo, mostrar o erro do Meta ao usuário em vez de tentar contornar.
- Não prometer resultado financeiro ao usuário.

## 12. Prompt de abertura (colar no chat dedicado)

```
Você vai subir e operar campanhas de Meta Ads para a RDA Serviços Digitais, usando o Meta MCP.
Leia o arquivo anexo "campanhas-meta-com-claude.md" e siga exatamente.

Resumo:
- Conta de anúncios: ADVANCED TRAFFIC - QVN Ads (298240176211615). Não mexa em nenhuma outra conta.
- Pixel: Serviços (2018578222100683). Otimizar para o evento Lead.
- Página do Facebook: [PREENCHER — nome e ID].
- 1 campanha de Leads, 4 conjuntos (Página para bio, Landing page, Configuração de anúncios, Artes e vídeos), R$ 5,49/dia cada, teto total R$ 29,00/dia.
- Cada anúncio usa a imagem correspondente de assets/ads/ e o link com UTMs e âncora da seção 5.
- Crie tudo PAUSADO, gere as prévias, mostre o plano e espere minha confirmação antes de ativar.
- Comece conferindo conta, Pixel, página e se o evento Lead está chegando.
```

## 13. Referências

- Landing page: https://servicos-digitais.netlify.app/
- Repositório: https://github.com/pkposites/servicosdigitais
- Exemplo real usado na LP: https://ludmillaimoveis.netlify.app/
