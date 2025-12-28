# 🏗️ DanceSport Assistant - System Architecture

## Overview

This document provides a detailed technical architecture of the DanceSport Assistant multi-agent system.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                              │
│                       (Streamlit Web App)                            │
│                                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Progress │  │ Practice │  │   Chat   │  │ Comments │           │
│  │ Analysis │  │ Routine  │  │  Coach   │  │  System  │           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
└───────┼─────────────┼─────────────┼─────────────┼──────────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
        ┌─────────────▼──────────────┐
        │   Session State Manager    │
        │  (Streamlit Session State) │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────────────────────────┐
        │         APPLICATION LAYER                       │
        │                                                  │
        │  ┌──────────────────────────────────────┐      │
        │  │   DanceSport Assistant Agent          │      │
        │  │   (Specialized AI Coach)              │      │
        │  │                                        │      │
        │  │  ┌──────────────────────────────┐    │      │
        │  │  │  Progress Analyzer           │    │      │
        │  │  ├──────────────────────────────┤    │      │
        │  │  │  Practice Planner            │    │      │
        │  │  ├──────────────────────────────┤    │      │
        │  │  │  Comment Generator           │    │      │
        │  │  ├──────────────────────────────┤    │      │
        │  │  │  Q&A System                  │    │      │
        │  │  └──────────────────────────────┘    │      │
        │  └──────────────┬───────────────────────┘      │
        │                 │                               │
        │  ┌──────────────▼───────────────────────┐      │
        │  │   Base Agent                          │      │
        │  │   (Foundation Class)                  │      │
        │  │   - Conversation History              │      │
        │  │   - Prompt Management                 │      │
        │  │   - Response Generation               │      │
        │  └──────────────┬───────────────────────┘      │
        └─────────────────┼──────────────────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                    │
┌───────▼────────┐              ┌──────────▼─────────┐
│  Notion API    │              │   Google Gemini    │
│   Client       │              │   AI Model         │
│                │              │                    │
│ - Search       │              │ - Text Generation  │
│ - Get Pages    │              │ - Analysis         │
│ - Query DB     │              │ - Reasoning        │
│ - Add Comments │              │ - Creative Output  │
│ - Update Props │              │                    │
└───────┬────────┘              └──────────┬─────────┘
        │                                   │
┌───────▼────────┐              ┌──────────▼─────────┐
│  Notion API    │              │  Google AI API     │
│  (External)    │              │  (External)        │
└────────────────┘              └────────────────────┘
```

---

## Component Details

### 1. User Interface Layer (Streamlit)

**File**: `app.py`

**Responsibilities**:
- User input/output
- Visual presentation
- Navigation and layout
- Session state management

**Key Components**:
```python
├── API Configuration
│   └── setup_api_keys()
├── Data Loading
│   └── load_workspace_data()
├── Main Interface
│   ├── Tab 1: Progress Analysis
│   ├── Tab 2: Practice Routine
│   ├── Tab 3: Chat Coach
│   └── Tab 4: Comments
└── Session State
    ├── notion_client
    ├── assistant
    ├── workspace_data
    └── chat_history
```

### 2. Application Layer

**File**: `agents.py`

**Agent Hierarchy**:
```
BaseAgent (Abstract)
    │
    ├── DanceSportAssistant
    │   ├── analyze_progress()
    │   ├── suggest_practice_routine()
    │   ├── create_practice_comment()
    │   ├── answer_question()
    │   └── compare_dances()
    │
    └── [Extensible for new agents]
        ├── FitnessCoach
        ├── NutritionAdvisor
        └── CompetitionPrep
```

**Base Agent Features**:
- Conversation history management
- AI model configuration
- Prompt generation
- Response handling
- Error management

### 3. Data Layer

**File**: `notion_client.py`

**Classes**:
```python
NotionClient
    ├── API Connection
    ├── Page Operations
    ├── Database Operations
    ├── Comment Management
    └── Search Functions

WorkspaceAnalyzer
    ├── Hierarchy Building
    ├── Title Extraction
    └── Content Finding

ProgressTracker
    ├── Statistics Collection
    └── Data Aggregation
```

---

## Data Flow Diagrams

### Flow 1: Progress Analysis

```
User Clicks "Analyze Progress"
        ↓
[UI] Load dance database ID
        ↓
[NotionClient] Query database
        ↓
[NotionClient] Return pages list
        ↓
[ProgressTracker] Extract statistics
        ↓
[DanceSportAssistant] Prepare context
        ↓
[BaseAgent] Generate AI prompt
        ↓
[Gemini API] Process & analyze
        ↓
[BaseAgent] Return analysis
        ↓
[UI] Display results to user
```

### Flow 2: Practice Routine Generation

```
User Selects: Dance, Level, Focus Areas
        ↓
[UI] Collect parameters
        ↓
[DanceSportAssistant] Load dance knowledge
        ↓
[DanceSportAssistant] Build context
        ↓
[BaseAgent] Create detailed prompt
        ↓
[Gemini API] Generate routine
        ↓
[BaseAgent] Return formatted routine
        ↓
[UI] Display with download option
```

### Flow 3: Comment Posting

```
User Enters Observation
        ↓
[UI] Capture input
        ↓
[DanceSportAssistant] Generate coach comment
        ↓
[Gemini API] Create constructive feedback
        ↓
[UI] Display generated comment
        ↓
User Clicks "Post to Notion"
        ↓
[NotionClient] Format comment
        ↓
[Notion API] Post comment
        ↓
[UI] Confirm success
```

---

## State Management

### Session State Schema

```python
st.session_state = {
    # Authentication
    'api_keys_set': bool,
    
    # Clients
    'notion_client': NotionClient,
    'assistant': DanceSportAssistant,
    
    # Data
    'workspace_data': {
        'total_objects': int,
        'main_pages': List[Dict],
        'databases_by_parent': Dict,
        'pages_by_parent': Dict
    },
    'dancesport_content': {
        'main_page': Dict,
        'dance_categories': List[Dict],
        'all_dances': List[Dict]
    },
    
    # UI State
    'chat_history': List[Dict],
    'generated_comment': str,
    
    # Extensible
    'custom_agents': Dict[str, BaseAgent]
}
```

---

## Security Architecture

### API Key Management

```
User Input (UI)
    ↓
Streamlit Secrets (Development)
    or
Environment Variables (Production)
    ↓
In-Memory Storage (Session State)
    ↓
Never Logged or Persisted
```

### Best Practices:
1. ✅ API keys stored in session state only
2. ✅ Password-type inputs for sensitive data
3. ✅ No keys in code or version control
4. ✅ Clear session on disconnect
5. ✅ HTTPS for production deployment

---

## Extensibility Points

### 1. Adding New Agents

```python
# Location: agents.py

class CustomAgent(BaseAgent):
    def __init__(self, notion_client):
        super().__init__(name="Custom Agent")
        self.notion = notion_client
        # Initialize custom properties
    
    def custom_method(self, params):
        # Implement functionality
        prompt = self._build_prompt(params)
        return self.generate_response(prompt)
```

### 2. Adding UI Tabs

```python
# Location: app.py, in main_interface()

tab_custom = st.tabs(["🎯 Custom Feature"])

with tab_custom:
    # Custom UI code
    custom_agent = CustomAgent(st.session_state.notion_client)
    result = custom_agent.custom_method(params)
    st.markdown(result)
```

### 3. Custom Data Processors

```python
# Location: notion_client.py or new file

class CustomAnalyzer:
    def __init__(self, notion_client):
        self.notion = notion_client
    
    def analyze_custom_data(self, data):
        # Process data
        return results
```

---

## Performance Considerations

### Optimization Strategies

1. **Caching**
```python
@st.cache_data(ttl=3600)
def load_workspace_data():
    # Expensive operation cached for 1 hour
    return data
```

2. **Lazy Loading**
```python
# Load data only when needed
if 'workspace_data' not in st.session_state:
    st.session_state.workspace_data = load_data()
```

3. **Batch Operations**
```python
# Query database once, process multiple times
results = notion.query_database(db_id)
stats = process_stats(results)
analysis = analyze_progress(results)
```

4. **Async Operations** (Future Enhancement)
```python
import asyncio

async def parallel_analysis():
    tasks = [
        analyze_progress(),
        generate_routine(),
        fetch_comments()
    ]
    return await asyncio.gather(*tasks)
```

---

## Error Handling Strategy

### Layered Error Handling

```
┌─────────────────────────────┐
│  UI Layer                   │
│  Try/Except with user msgs  │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│  Application Layer          │
│  Graceful degradation       │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│  Data Layer                 │
│  API error handling         │
└─────────────────────────────┘
```

### Example Implementation

```python
# UI Layer (app.py)
try:
    analysis = assistant.analyze_progress(data)
    st.markdown(analysis)
except Exception as e:
    st.error(f"Analysis failed: {str(e)}")
    st.info("Try refreshing the data")

# Application Layer (agents.py)
def analyze_progress(self, data):
    if not data:
        return "No data available for analysis."
    try:
        return self.generate_response(prompt)
    except Exception as e:
        return f"Unable to complete analysis: {str(e)}"

# Data Layer (notion_client.py)
def get_page(self, page_id):
    response = requests.get(url, headers=self.headers)
    response.raise_for_status()  # Raises exception for 4xx/5xx
    return response.json()
```

---

## Testing Strategy

### Unit Tests
```python
# test_agents.py
def test_dance_knowledge():
    assistant = DanceSportAssistant(mock_notion)
    assert "cha_cha" in assistant.dance_knowledge
    assert "rhythm" in assistant.dance_knowledge["cha_cha"]

def test_routine_generation():
    routine = assistant.suggest_practice_routine("Cha Cha", "beginner")
    assert "warm-up" in routine.lower()
    assert len(routine) > 100
```

### Integration Tests
```python
# test_integration.py
def test_notion_connection():
    notion = NotionClient(TEST_TOKEN)
    info = notion.get_integration_info()
    assert info['type'] == 'bot'

def test_end_to_end_workflow():
    # Setup
    notion = NotionClient(TEST_TOKEN)
    assistant = DanceSportAssistant(notion)
    
    # Test
    results = notion.query_database(TEST_DB_ID)
    analysis = assistant.analyze_progress(results['results'])
    
    # Verify
    assert analysis is not None
    assert len(analysis) > 50
```

---

## Deployment Options

### Option 1: Local Development
```bash
streamlit run app.py
# Access at http://localhost:8501
```

### Option 2: Streamlit Cloud
```bash
# 1. Push to GitHub
# 2. Connect to Streamlit Cloud
# 3. Add secrets in dashboard
# 4. Deploy
```

### Option 3: Docker Container
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## Future Enhancements

### Planned Features
1. **Multi-user Support**: User authentication and personalized data
2. **Video Analysis**: Integration with video upload and AI analysis
3. **Scheduled Reminders**: Automated practice reminders
4. **Mobile App**: React Native or Flutter mobile version
5. **Voice Interface**: Speech-to-text for hands-free interaction
6. **Advanced Analytics**: ML-based progress prediction
7. **Social Features**: Share routines with other dancers
8. **Offline Mode**: Local caching for offline access

### Architecture Scalability
```
Current: Single-server Streamlit
    ↓
Phase 2: Load-balanced Streamlit + Redis
    ↓
Phase 3: Microservices (FastAPI + React + Redis + PostgreSQL)
    ↓
Phase 4: Cloud-native (Kubernetes + Serverless Functions)
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit | Web UI framework |
| Backend | Python 3.9+ | Application logic |
| AI Model | Google Gemini | Natural language processing |
| Data Storage | Notion | Primary data store |
| Session | Streamlit Session State | User session management |
| HTTP Client | Requests | API communication |

---

## Conclusion

This architecture provides:
- ✅ Modular, maintainable code structure
- ✅ Clear separation of concerns
- ✅ Extensibility for new features
- ✅ Robust error handling
- ✅ Scalability for future growth
- ✅ Educational framework for learning

For implementation details, see the source files and EXAMPLES.md.
