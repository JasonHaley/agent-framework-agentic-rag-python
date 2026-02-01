# Agentic RAG - IT Support Ticket Search

This directory contains the source code for an **Agentic RAG (Retrieval-Augmented Generation) system** that intelligently routes user queries to specialized AI agents for searching and analyzing IT support tickets.

## Overview

The application uses the **Microsoft Agent Framework** with a **Handoff orchestration pattern** to route user questions to specialized search agents based on query type. It leverages Azure OpenAI for language understanding and Azure AI Search for hybrid (keyword + vector) search capabilities.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Query                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Classifier Agent                             │
│         (Routes queries to specialized agents)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Yes/No Agent │    │  Count Agent  │    │ Semantic Agent│
└───────────────┘    └───────────────┘    └───────────────┘
        ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Azure AI Search                             │
│              (Hybrid Search: Keyword + Vector)                  │
└─────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
src/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── agents/                 # Specialized AI agents
│   ├── agent_factory.py    # Factory for creating agents
│   ├── classifier_agent.py # Query routing agent
│   ├── semantic_search_agent.py
│   ├── yes_no_agent.py
│   ├── count_agent.py
│   ├── difference_agent.py
│   ├── intersection_agent.py
│   ├── multi_hop_agent.py
│   ├── comparative_agent.py
│   ├── ordinal_agent.py
│   └── superlative_agent.py
├── config/                 # Configuration management
│   └── azure_config.py     # Azure service configuration
├── services/               # External service integrations
│   └── search_service.py   # Azure AI Search client
├── utils/                  # Utility scripts
│   └── index_loader.py     # Script to load data into Azure AI Search
└── workflows/              # Workflow event handling
    └── workflow_handlers.py
```

## Agents

### Classifier Agent
The central routing agent that analyzes incoming queries and hands them off to the appropriate specialist agent based on query type.

### Specialized Search Agents

| Agent | Purpose | Example Query |
|-------|---------|---------------|
| **Semantic Search** | General questions requiring semantic similarity search | "What problems are there with Surface devices?" |
| **Yes/No** | Boolean questions expecting yes/no answers | "Are there any issues for Dell XPS laptops?" |
| **Count** | Questions asking for counts or totals with filters | "How many Incidents for Human Resources and low priority?" |
| **Difference** | Questions asking for items matching one criterion but excluding another | "Which Dell XPS issue does not mention Windows?" |
| **Intersection** | Questions requiring items matching multiple criteria (AND logic) | "What issues are for Dell XPS laptops and the user tried Win+Ctrl+Shift+B?" |
| **Multi-hop** | Questions requiring multi-step reasoning | "What department had consultants with Login Issues?" |
| **Comparative** | Questions comparing multiple items | "Do we have more issues with MacBook Air or Dell XPS?" |
| **Ordinal** | Questions asking for items by position/order | "What is the last issue for the HR department?" |
| **Superlative** | Questions asking for max/min across groups | "Which department has the most high priority incidents?" |

## Azure AI Search Index Schema

The IT support ticket index contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| Id | string | Unique ticket identifier |
| Create_Date | datetime | Ticket creation date |
| Subject | string | Ticket subject line |
| Body | string | Ticket question/description |
| Answer | string | Ticket response/solution |
| Type | string | Ticket type: Incident, Request, Problem, Change |
| Queue | string | Department: Human Resources, IT, Finance, Operations, Sales, Marketing, Engineering, Support |
| Priority | string | Priority level: high, medium, low |
| Language | string | Ticket language |
| Business_Type | string | Business category |
| Tags | string[] | Categorization tags |

## Configuration

The application requires the following environment variables:

```env
# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AZURE_SEARCH_API_KEY=<your-search-api-key>
AZURE_SEARCH_INDEX_NAME=<your-index-name>

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com
AZURE_OPENAI_API_KEY=<your-openai-api-key>
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=<your-chat-model-deployment>
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=<your-embedding-model-deployment>
```

## Usage

### Demo Mode (Default)
Runs predefined test queries to demonstrate the system:

```bash
cd src
python main.py
```

### Interactive Mode
Start an interactive session to ask questions:

```bash
cd src
python main.py --interactive
# or
python main.py -i
```

Type your questions at the prompt. Type `quit`, `exit`, or `q` to end the session.

## Loading Data

Before running the application, you need to load the IT support ticket data into Azure AI Search:

```bash
python utils/index_loader.py ../data/en-only-tickets.csv
```

This script will:
1. Create an Azure AI Search index with the appropriate schema
2. Generate embeddings for the Body and Answer fields using Azure OpenAI
3. Upload all documents to the search index

## Dependencies

Key dependencies include:
- `agent-framework` - Microsoft Agent Framework for orchestration
- `azure-search-documents` - Azure AI Search SDK
- `azure-identity` - Azure authentication
- `openai` - Azure OpenAI SDK
- `python-dotenv` - Environment variable management

Install all dependencies:
```bash
pip install -r requirements.txt
```

## How It Works

1. **User submits a query** via the command line
2. **Classifier Agent** analyzes the query and determines the best specialist agent
3. **Handoff** occurs to the selected specialist agent
4. **Specialist Agent** uses AI functions to:
   - Generate appropriate search queries/filters
   - Call Azure AI Search with hybrid search (keyword + vector)
   - Process and format results
5. **Response** is returned to the user with relevant tickets and insights

## Search Capabilities

The system uses **hybrid search** combining:
- **Keyword search** - Traditional text matching
- **Vector search** - Semantic similarity using embeddings (BodyEmbeddings, AnswerEmbeddings fields)
- **Filters** - OData filters for precise filtering by Type, Queue, Priority, etc.
