# Perplexity-like Real-Time CRM (RT-CRM)

A chat interface that connects to Shopify, Facebook Page, and Website events, plans a multi-channel campaign (Email, SMS, WhatsApp, Ads), and **streams** JSON frames for “right time, right channel, right message, right audience.” Built on **Google AI Studio (Gemini)** and **Vertex AI** MLOps.

## Stack
- UI: Next.js + SSE stream viewer
- API: Fastapi on Cloud Run
- Data: Pub/Sub → BigQuery, Vertex AI Feature Store
- MLOps: Vertex AI Pipelines + Model Registry
- LLM: Google AI Studio (Gemini) with streaming

## Quick Start
```bash
# Server
cd server && npm i
export GOOGLE_API_KEY=***    # AI Studio
npm run dev

# Web
cd web && npm i
export SERVER_URL=http://localhost:8080
npm run dev
```

## File Structure
```bash
perplexity-like-rtcrm/
├─ README.md
├─ infra/
│  ├─ cloudrun.Dockerfile
│  ├─ gke.Dockerfile
│  ├─ terraform/ (optional IaC stubs)
├─ server/
│  ├─ package.json
│  ├─ src/
│  │  ├─ index.ts                 # HTTP + SSE streaming
│  │  ├─ connectors/
│  │  │  ├─ shopify.ts
│  │  │  ├─ facebookPage.ts
│  │  │  └─ website.ts
│  │  ├─ ml/
│  │  │  ├─ audience_scoring.py   # Feature pipeline (Vertex AI Pipelines)
│  │  │  ├─ prompt_templates/
│  │  │  │  └─ campaign_prompt.md
│  │  │  └─ registry.yaml         # model + prompt versioning metadata
│  │  ├─ channels/
│  │  │  ├─ email.ts
│  │  │  ├─ sms.ts
│  │  │  ├─ whatsapp.ts
│  │  │  └─ ads.ts
│  │  ├─ schema/
│  │  │  ├─ campaign.payload.schema.json
│  │  │  └─ audience.schema.json
│  │  └─ utils/
│  │     ├─ googleAiStudio.ts
│  │     ├─ bigquery.ts
│  │     ├─ featureStore.ts
│  │     └─ sse.ts
├─ web/
│  ├─ package.json
│  ├─ next.config.js
│  └─ app/
│     ├─ page.tsx                 # Perplexity-like chat
│     ├─ api/stream/route.ts      # Proxy to server SSE
│     └─ components/
│        ├─ Chat.tsx
│        ├─ SourceChips.tsx
│        └─ ChannelPreview.tsx
└─ mlops/
   ├─ pipeline.yaml               # Vertex AI Pipelines (Kubeflow spec)
   ├─ feature_store_def.yaml      # Vertex AI Feature Store entities
   ├─ mlflow_setup.md             # optional MLflow-on-GCS notes
   └─ notebooks/
      └─ offline_feature_build.ipynb

```

