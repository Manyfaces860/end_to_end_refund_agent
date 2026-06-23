<div align="center">

# 🤖 AuraGear AI Refund Agent

### A production-oriented customer-support agent for evaluating refund requests with RAG, structured decisioning, guardrails, and observability

<p>
  <img src="https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/OpenAI_Agents_SDK-0.16-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI Agents SDK" />
  <img src="https://img.shields.io/badge/Next.js-16-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/MongoDB-Beanie-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB and Beanie" />
  <img src="https://img.shields.io/badge/Pinecone-Hybrid_Search-000000?style=for-the-badge" alt="Pinecone hybrid search" />
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
</p>

<p>
  <a href="#-overview">Overview</a> •
  <a href="#-key-capabilities">Capabilities</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-getting-started">Getting started</a> •
  <a href="#-deployment">Deployment</a>
</p>

</div>

---

## 🌍 Overview

**AuraGear AI Refund Agent** is a full-stack customer-support system that evaluates refund requests using a combination of:

- large-language-model reasoning
- explicit business rules
- retrieval-augmented generation
- structured output schemas
- input and output guardrails
- persistent conversation state
- observability and tracing

The system is designed around a fictional commerce organisation named **AuraGear**. It demonstrates how an AI agent can support sensitive business workflows without relying on unrestricted free-form generation.

Rather than acting like a general chatbot, the agent gathers missing information, retrieves the relevant policy, checks order and customer data, applies refund constraints, and produces a controlled decision.

---

## ✨ Key capabilities

### 🧠 Agent-based refund evaluation

The backend uses the OpenAI Agents SDK to coordinate reasoning, tools, policy retrieval, and structured decision generation.

### 🔍 Hybrid policy retrieval

Refund policies are retrieved from Pinecone using hybrid search so the system can combine semantic similarity with keyword relevance.

### 🧾 Structured decisions

The agent returns controlled outcomes such as:

- `APPROVED`
- `DENIED`
- `ESCALATE`
- `NEEDS_MORE_INFORMATION`

The response can also include:

- customer-facing explanation
- reasoning summary
- refund amount
- restocking fee
- updated conversation summary

### 🛡️ Guardrails

Input and output guardrails protect the workflow from:

- prompt manipulation
- unsupported actions
- malformed responses
- policy-breaking decisions
- unsafe or irrelevant requests

### 🧰 Programmatic tools

The agent can use application tools to retrieve policy information and work with customer, product, and order data instead of inventing facts.

### 💬 Session-aware conversations

Conversation state is maintained across requests so users can provide missing details over multiple turns.

### 📊 Observability

The backend includes OpenInference, OpenTelemetry, and Langfuse dependencies for tracing:

- agent runs
- tool calls
- latency
- token usage
- execution failures
- decision behaviour

### 🐳 Full-stack containerisation

The frontend and backend run as separate Docker services and can be started together with Docker Compose.

---

## 🏛️ Business rules represented

The system is designed to handle rules such as:

| Rule | Behaviour |
|---|---|
| Standard return window | Refund eligibility is checked against delivery date |
| Black November purchases | Extended window with a possible restocking fee |
| Final-sale products | Refund denied |
| Opened or activated software | Refund denied |
| Customer-caused damage | Refund denied |
| High-value refund | Escalated for manual review |
| Flagged customer | Escalated for manual review |
| Missing order information | Agent asks for more information |

These checks ensure that the model works inside a defined business process instead of making unrestricted financial decisions.

---

## 🧱 Architecture

```text
┌──────────────────────────────┐
│ Next.js customer chat UI     │
└──────────────┬───────────────┘
               │ HTTP
               ▼
┌──────────────────────────────┐
│ FastAPI backend              │
│                              │
│ • Session handling           │
│ • Request validation         │
│ • Agent orchestration        │
│ • Structured responses       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Refund decision agent        │
│                              │
│ • Input guardrail            │
│ • Business-rule reasoning    │
│ • Tool calling               │
│ • Output guardrail           │
└───────┬─────────┬────────────┘
        │         │
        │         ├──────────────────────┐
        ▼         ▼                      ▼
┌────────────┐ ┌──────────────┐ ┌─────────────────┐
│ Pinecone   │ │ MongoDB      │ │ Redis / session │
│ policies   │ │ order data   │ │ state           │
└────────────┘ └──────────────┘ └─────────────────┘
        │
        ▼
┌──────────────────────────────┐
│ Langfuse / OpenTelemetry     │
│ tracing and observability    │
└──────────────────────────────┘
```

---

## 🔄 Request flow

```text
Customer message
      │
      ▼
Input validation and guardrail
      │
      ▼
Load session and conversation context
      │
      ▼
Retrieve relevant refund policy
      │
      ▼
Fetch order, product, and customer data
      │
      ▼
Apply policy and business constraints
      │
      ▼
Generate structured refund decision
      │
      ▼
Output validation and guardrail
      │
      ▼
Return customer-facing response
```

---

## 🛠️ Tech stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, Uvicorn |
| Agent framework | OpenAI Agents SDK |
| Validation | Pydantic |
| Database | MongoDB, Motor, Beanie |
| Session and caching | Redis |
| Vector retrieval | Pinecone |
| LLM integration | OpenAI |
| Frontend | Next.js 16, React 19, TypeScript |
| Styling | Tailwind CSS |
| Observability | Langfuse, OpenInference, OpenTelemetry |
| Containers | Docker, Docker Compose |
| Infrastructure | Terraform, Google Cloud |

---

## 📂 Repository structure

```text
.
├── backend/
│   ├── agents/              Agent definitions and orchestration
│   ├── guardrails/          Input and output validation
│   ├── models/              Database and response models
│   ├── routes/              FastAPI endpoints
│   ├── services/            Business and persistence services
│   ├── tools/               Agent-callable programmatic tools
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app/                 Next.js application routes
│   ├── components/          Chat and interface components
│   ├── Dockerfile
│   └── package.json
│
├── terraform/               Cloud infrastructure definitions
├── docker-compose.yml
└── README.md
```

> The exact internal folder names may evolve as the project is developed, but the repository is organised around separate backend, frontend, and infrastructure layers.

---

## 🔌 API contract

The primary chat endpoint follows this general request shape:

```json
{
  "query": "I want a refund for order AG-1024",
  "session_key": "optional-existing-session-key"
}
```

Example response:

```json
{
  "message": "Your request requires manual review because the order value exceeds the automatic refund limit.",
  "refund": {
    "decision": "ESCALATE",
    "refund_amount": null,
    "restocking_fee": null
  },
  "session_key": "generated-or-existing-session-key"
}
```

The exact schema may include additional structured decision and conversation fields.

---

## 🚀 Getting started

### Prerequisites

Install:

- Docker
- Docker Compose
- Git

You will also need credentials for the services enabled in your environment, such as:

- OpenAI
- MongoDB
- Pinecone
- Redis
- Langfuse
- Google Cloud

### Clone the repository

```bash
git clone https://github.com/Manyfaces860/end_to_end_refund_agent.git
cd end_to_end_refund_agent
```

### Configure environment variables

Create the required environment files for the backend and frontend.

Example backend configuration:

```env
OPENAI_API_KEY=your_openai_api_key

MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=refund_agent

REDIS_URL=your_redis_connection_string

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_policy_index

LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=your_langfuse_host
```

Example frontend configuration:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Do not commit real credentials or cloud service-account files.

### Run with Docker Compose

```bash
docker compose up --build
```

Services are exposed locally at:

| Service | Address |
|---|---|
| Frontend | `http://localhost:3000` |
| Backend | `http://localhost:8000` |
| API documentation | `http://localhost:8000/docs` |

### Stop the application

```bash
docker compose down
```

---

## 💻 Run services separately

### Backend

```bash
cd backend

python -m venv .venv
```

Activate the environment.

macOS or Linux:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies and start the API:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Testing

Run backend tests with:

```bash
cd backend
pytest
```

Useful test areas include:

- eligible standard refunds
- expired return windows
- final-sale products
- customer-caused damage
- Black November restocking fees
- high-value escalation
- flagged-customer escalation
- missing order information
- prompt-injection attempts
- malformed model output

---

## 📈 Observability

The project is designed to trace agent execution using Langfuse and OpenTelemetry-compatible instrumentation.

Typical signals include:

- total request latency
- model call duration
- retrieval latency
- tool-call success rate
- token consumption
- policy documents retrieved
- guardrail failures
- final decision distribution
- escalation rate

Observability is especially important in financial workflows because an apparently correct customer response may still be based on the wrong policy, tool result, or intermediate reasoning step.

---

## ☁️ Deployment

The repository separates deployment-relevant code into:

```text
backend/
frontend/
terraform/
```

Its GitHub Actions deployment workflow is configured to run on pushes to `main` only when files inside one of those paths change.

A README-only update does not trigger the automated deployment workflow.

Infrastructure definitions under `terraform/` are intended to make cloud resources reproducible and version controlled.

---

## 🔐 Security considerations

This project demonstrates a safer pattern for agentic financial workflows:

- sensitive values are loaded from environment variables
- financial decisions use structured schemas
- high-risk cases are escalated
- retrieved policy is used as grounding
- model input and output are checked by guardrails
- tool access is explicit
- execution is observable

For a real production deployment, additional controls would be required, including authentication, authorisation, audit logging, rate limiting, secret rotation, encrypted data storage, and human approval for sensitive transactions.

---

## 🗺️ Roadmap

- [x] Full-stack chat workflow
- [x] Structured refund decisions
- [x] Policy retrieval
- [x] Session-aware conversations
- [x] Input and output guardrails
- [x] Docker Compose setup
- [x] Agent observability foundation
- [x] Infrastructure-as-code structure
- [ ] Expanded automated evaluation suite
- [ ] Policy-version tracking
- [ ] Load and failure testing
- [ ] Production security hardening

---

## 👤 Author

**Abhishek Gupta**

<p>
  <a href="https://github.com/Manyfaces860">
    <img src="https://img.shields.io/badge/GitHub-Manyfaces860-181717?style=flat-square&logo=github" alt="GitHub" />
  </a>
  <a href="https://www.linkedin.com/in/abhishek-gupta-ab377b305/">
    <img src="https://img.shields.io/badge/LinkedIn-Abhishek_Gupta-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
</p>

---

<div align="center">

### Built to explore safe, observable, and policy-grounded AI decision workflows.

</div>
