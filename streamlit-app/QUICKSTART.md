# 🚀 Quick Reference Guide - DanceSport Assistant

## Setup (5 Minutes)

### 1. Install Dependencies
```bash
pip install streamlit google-generativeai requests
```

### 2. Get API Keys
- **Notion**: https://www.notion.so/my-integrations → Create integration → Copy token
- **Google**: https://aistudio.google.com/app/apikey → Create key → Copy

### 3. Run Application
```bash
streamlit run app.py
```

---

## File Structure

```
📁 Project Root
├── app.py              # Main Streamlit UI
├── agents.py          # AI agent classes
├── notion_client.py   # Notion API wrapper
├── requirements.txt   # Dependencies
├── README.md          # Full documentation
└── EXAMPLES.md        # Tutorials & examples
```

---

## Key Classes & Methods

### NotionClient (`notion_client.py`)

```python
# Initialize
notion = NotionClient(token)

# Basic Operations
notion.search_all(query="DanceSport")
notion.get_page(page_id)
notion.query_database(database_id)
notion.add_comment(page_id, text)
notion.update_page_properties(page_id, properties)
```

### DanceSportAssistant (`agents.py`)

```python
# Initialize
assistant = DanceSportAssistant(notion_client)

# Main Functions
assistant.analyze_progress(dance_data)
assistant.suggest_practice_routine(dance_name, skill_level)
assistant.create_practice_comment(dance_name, observation)
assistant.answer_question(question)
assistant.compare_dances(dance1, dance2)
```

---

## Adding New Features

### 1. Create New Agent

```python
# In agents.py
class YourAgent(BaseAgent):
    def __init__(self, notion_client):
        super().__init__(name="Your Agent Name")
        self.notion = notion_client
    
    def your_method(self, params):
        prompt = "Your AI prompt here"
        return self.generate_response(prompt)
```

### 2. Add UI Tab

```python
# In app.py, in main_interface()
tab_new = st.tabs(["🎯 Your Feature"])

with tab_new:
    st.header("Your Feature")
    # Your UI code here
```

### 3. Customize Prompts

```python
prompt = f"""As a [ROLE], do [TASK].

Consider:
1. Point one
2. Point two

Provide:
- Output format
- Specific details
"""
```

---

## Common Tasks

### Read Notion Page
```python
page = notion.get_page(page_id)
blocks = notion.get_block_children(page_id)
```

### Query Database with Filter
```python
filter_obj = {
    "property": "Status",
    "select": {"equals": "Active"}
}
results = notion.query_database(db_id, filter_obj)
```

### Add AI-Generated Comment
```python
comment = assistant.create_practice_comment(
    dance_name="Cha Cha",
    observation="Good timing today"
)
notion.add_comment(page_id, comment)
```

### Generate Practice Routine
```python
routine = assistant.suggest_practice_routine(
    dance_name="Rumba",
    skill_level="intermediate",
    focus_areas=["Hip Action", "Timing"]
)
```

---

## Streamlit UI Components

### Input Widgets
```python
text = st.text_input("Label", "default")
number = st.number_input("Label", min_value=0)
option = st.selectbox("Label", ["A", "B", "C"])
multi = st.multiselect("Label", ["A", "B", "C"])
slider = st.slider("Label", 0, 100, 50)
checkbox = st.checkbox("Label")
```

### Display Elements
```python
st.header("Header")
st.subheader("Subheader")
st.markdown("**Bold** *italic*")
st.write("Anything")
st.code("code block")
st.json({"key": "value"})
```

### Layout
```python
col1, col2 = st.columns(2)
with col1:
    st.write("Left")
with col2:
    st.write("Right")

with st.expander("Click to expand"):
    st.write("Hidden content")

tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
```

### Interactivity
```python
if st.button("Click me"):
    # Action
    
with st.spinner("Loading..."):
    # Long operation
    
st.success("Success!")
st.error("Error!")
st.warning("Warning!")
st.info("Info!")
```

---

## AI Model Configuration

```python
# In agents.py BaseAgent class
self.model = genai.GenerativeModel(
    "models/gemini-2.0-flash-exp",
    generation_config={
        'temperature': 0.7,     # 0.0-1.0
        'top_p': 0.95,         # 0.0-1.0
        'max_output_tokens': 2048,
    }
)
```

**Temperature Guide:**
- `0.0-0.3`: Factual, consistent (technical analysis)
- `0.4-0.7`: Balanced (general use)
- `0.8-1.0`: Creative, varied (brainstorming)

---

## Debugging Tips

### 1. Check API Connection
```python
try:
    info = notion.get_integration_info()
    print(f"✅ Connected: {info['name']}")
except Exception as e:
    print(f"❌ Error: {e}")
```

### 2. Print Variables
```python
st.write("Debug:", variable_name)
print(f"Value: {variable_name}")
```

### 3. View Session State
```python
st.write(st.session_state)
```

### 4. Error Handling
```python
try:
    # Your code
    result = some_function()
except Exception as e:
    st.error(f"Error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
```

---

## Notion Workspace Structure

```
📄 DanceSport (Main Page)
  ├── 📊 Fundamental Cha Cha (Database)
  │   ├── 📝 Basic Movement (Page)
  │   ├── 📝 New York (Page)
  │   └── 📝 Spot Turn (Page)
  ├── 📊 Fundamental Rumba (Database)
  │   └── 📝 Basic Movement (Page)
  └── 📊 Open Swing (Database)
      └── 📝 Underarm Turn (Page)
```

**Important**: Share pages with integration!

---

## Useful Code Snippets

### Extract Title from Notion Object
```python
def extract_title(obj):
    if obj.get('object') == 'page':
        props = obj.get('properties', {})
        for prop in props.values():
            if prop.get('type') == 'title':
                title = prop.get('title', [])
                if title:
                    return title[0].get('plain_text', 'Untitled')
    return 'Untitled'
```

### Format AI Response
```python
response = assistant.generate_response(prompt)
st.markdown(response)  # Renders markdown formatting
```

### Session State Management
```python
# Initialize
if 'my_var' not in st.session_state:
    st.session_state.my_var = initial_value

# Use
st.session_state.my_var = new_value

# Access
value = st.session_state.my_var
```

---

## Resources

- **Streamlit**: https://docs.streamlit.io
- **Notion API**: https://developers.notion.com
- **Gemini AI**: https://ai.google.dev
- **GitHub Examples**: Search "streamlit notion" or "gemini chatbot"

---

## Common Errors & Solutions

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Invalid API key` | Check key format, regenerate if needed |
| `Page not found` | Share Notion page with integration |
| `Rate limit exceeded` | Add delays: `time.sleep(1)` |
| `Session state error` | Initialize in `init_session_state()` |

---

## Next Steps

1. ✅ Get system running
2. ✅ Test with your Notion workspace
3. 📝 Add a new agent (see EXAMPLES.md)
4. 🎨 Customize UI colors/layout
5. 🚀 Add advanced features

---

**Pro Tip**: Keep this guide open while coding! 📌

For detailed tutorials, see EXAMPLES.md
For full documentation, see README.md
