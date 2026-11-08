# Conversions API (CAPI) na Netlify

Evento **Lead** enviado ao Meta pelo servidor, com o mesmo `event_id` do Pixel no navegador (a Meta deduplica).

- **Função:** `netlify/functions/capi.mjs`, rota pública `POST /api/capi`.
- **Disparo:** `index.html`, no envio do formulário. Envia nome, WhatsApp, `_fbp`, `_fbc`, `fbclid`, UTMs e o serviço escolhido.
- **Privacidade:** nome e telefone são normalizados e enviados com hash SHA-256. IP e user agent vêm dos cabeçalhos da requisição.
- **Segurança:** só aceita o evento `Lead`, só da própria origem do site, corpo de até 8 KB.

## Variáveis de ambiente (Netlify → Site configuration → Environment variables)

| Variável | Obrigatória | Valor |
|---|---|---|
| `META_PIXEL_ID` | sim | `2018578222100683` (Pixel "Serviços") |
| `META_CAPI_TOKEN` | sim, **secreta** | Token da Conversions API (Gerenciador de Eventos → Pixel → Configurações) |
| `META_GRAPH_VERSION` | não | Padrão `v23.0` |
| `META_TEST_EVENT_CODE` | não | Código de "Testar eventos". Use só durante o teste e remova depois |
| `CAPI_ALLOWED_ORIGINS` | não | Outras origens permitidas, separadas por vírgula |

Mudou uma variável? É preciso um novo deploy para a função enxergá-la.

## Como testar
1. No Gerenciador de Eventos, aba **Testar eventos**, copie o código e coloque em `META_TEST_EVENT_CODE`. Faça um novo deploy.
2. Envie o formulário da LP. Devem aparecer dois eventos Lead com o mesmo ID: um **Navegador** e um **Servidor**, marcados como desduplicados.
3. Remova `META_TEST_EVENT_CODE` e faça um novo deploy.
