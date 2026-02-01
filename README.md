# Agentic RAG - IT Support Ticket Search

This is an **example of implementing an Agentic RAG (Retrieval-Augmented Generation) system** in python and using [agent-framework](https://github.com/microsoft/agent-framework).

The sample uses a Kaggle dataset from Tobias Bueck. (2025). [Customer IT Support - Ticket Dataset](https://www.kaggle.com/datasets/tobiasbueck/multilingual-customer-support-tickets). I have filtered out the non-english tickets and added a random create date in order to perform additional search types.

> NOTE: This is based on the lab3 solution I created for [agent-framework-dev-day](https://github.com/AgentFrameworkDev/agent-framework-dev-day)

## Prerequisites
- [Azure subscription](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=azurefreeaccount)
- [Python 3.11, 3.12, 3.13 or 3.14 and PIP](https://www.python.org/downloads/) with `pip` and `venv`
    - **Important**: Python and the pip package manager must be in the path in Windows for the setup scripts to work.
    - **Important**: Ensure you can run `python --version` from console. On Ubuntu, you might need to run `sudo apt install python-is-python3` to link `python` to `python3`.
- [Powershell 7+ (pwsh)](https://github.com/powershell/powershell) - for Windows users only
    - **Important**: Ensure you can run pwsh.exe from a PowerShell terminal. If this fails, you likely need to upgrade PowerShell.
- [Git](https://git-scm.com/downloads)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows) (Optional)
- [Visual Studio Code](https://code.visualstudio.com/download) (Optional)

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

## Getting Setup
There are two options:
- Use azd to do the setup for you
- Manually create the Azure Resources and populate the search index

### Using `azd` to create the Azure Resources

The following steps will provizion Azure resources and populate the search index with the sample dataset, using azd (Azure Developer CLI). If you already have the Azure AI Search and Azure Open AI resources created in Azure, you can continue on to the next section. 

1. Create a folder you want to put the project files in
2. Open VS Code or a PowerShell terminal in that path
3. Run the following to clone to code:
```bash
git clone https://github.com/JasonHaley/agent-framework-agentic-rag-python.git
```
4. Change to the directory that was just created
```bash
cd agent-framework-agentic-rag-python
```
4. Run the following and login you Azure subscription using azd
```bash
azd auth login
```
5. Next run the provision command, select your environment name and locations to provision the resources:
```bash
azd provision
```
The above will create output that looks something like this:
```text
  (✓) Done: Resource group: rg-beta (925ms)
  (✓) Done: Search service: afarag-lggbzors3dpmk (4.15s)
  (✓) Done: Azure OpenAI: cog-lggbzors3dpmk (17.928s)
  (✓) Done: Azure AI Services Model Deployment: cog-lggbzors3dpmk/text-embedding-ada-002 (2.602s)
  (✓) Done: Azure AI Services Model Deployment: cog-lggbzors3dpmk/gpt-4.1 (1.368s)
```
Once the resources are created, the postprovision hook **should** also run:

This command will:
1. Create a virtual environment
2. Install the dependencies
3. Create an Azure AI Search index with the appropriate schema
4. Generate embeddings for the Body and Answer fields using Azure OpenAI
5. Upload rows of the dataset to the search index

**If the postprovision hook does not run** you can run it manually with the following command:
```bash
azd hooks run postprovision
```

### Manual Configuration

1. Create a folder you want to put the project files in
2. Open VS Code or a PowerShell terminal in that path
3. Run the following to clone to code:
```bash
git clone https://github.com/JasonHaley/agent-framework-agentic-rag-python.git
```
4. Change to the directory that was just created
```bash
cd agent-framework-agentic-rag-python
```

5. You will need to create the following in Azure:
    - Azure AI Search resource
    - Azure OpenAI resource
    - Deploy a Chat model - like GPT 4.1
    - Deploy an Embedding model - like text-embedding-ada-002

6. Once you have your resources created, create a `.env` file in the root directory of the project
7. Add the following to that file:
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

8. Create a Python `venv` virtual environment with the following command:
```bash
python -m venv .venv
```
9. Activate the virtual environment with the following:

#### Windows (PowerShell)
```bash
.venv\Scripts\Activate.ps1
```

#### Mac, Linux
```bash
source .venv/bin/activate
```

10. Install the dependencies
```bash
pip install -r requirements-dev.txt
```

11. Populate the search index with the sample dataset:

```bash
python src/utils/index_loader.py data/en-only-tickets.csv
```
This script will:
1. Create an Azure AI Search index with the appropriate schema
2. Generate embeddings for the Body and Answer fields using Azure OpenAI
3. Upload rows of the dataset to the search index


## Dependencies

Key dependencies include:
- `agent-framework` - Microsoft Agent Framework for orchestration
- `azure-search-documents` - Azure AI Search SDK
- `azure-identity` - Azure authentication
- `openai` - Azure OpenAI SDK
- `python-dotenv` - Environment variable management


## Usage

First make sure you have activated the venv before running.

#### Windows (PowerShell)
```bash
.venv\Scripts\Activate.ps1
```

#### Mac, Linux
```bash
source .venv/bin/activate
```

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
