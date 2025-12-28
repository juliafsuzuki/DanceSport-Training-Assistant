# 🎓 DanceSport Assistant - Examples & Tutorials

This file contains practical examples and tutorials to help you learn and extend the system.

## Table of Contents
1. [Basic Usage Examples](#basic-usage-examples)
2. [Adding New Agents](#adding-new-agents)
3. [Customizing Prompts](#customizing-prompts)
4. [Working with Notion API](#working-with-notion-api)
5. [UI Customization](#ui-customization)

---

## Basic Usage Examples

### Example 1: Testing the Notion Client

Create a test script to verify your Notion connection:

```python
# test_notion.py
from notion_client import NotionClient

# Initialize client
notion = NotionClient("your_token_here")

# Test connection
try:
    info = notion.get_integration_info()
    print(f"✅ Connected as: {info['name']}")
    
    # Search for pages
    results = notion.search_all(query="DanceSport")
    print(f"Found {len(results['results'])} results")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

### Example 2: Testing the AI Agent

Test the DanceSport Assistant independently:

```python
# test_agent.py
import google.generativeai as genai
from agents import DanceSportAssistant
from notion_client import NotionClient

# Setup
genai.configure(api_key="your_google_api_key")
notion = NotionClient("your_notion_token")
assistant = DanceSportAssistant(notion)

# Test practice routine generation
routine = assistant.suggest_practice_routine(
    dance_name="Cha Cha",
    skill_level="beginner",
    focus_areas=["Timing", "Footwork"]
)

print("Generated Routine:")
print(routine)

# Test question answering
answer = assistant.answer_question(
    "What's the difference between Cha Cha and Rumba timing?"
)

print("\nAnswer:")
print(answer)
```

---

## Adding New Agents

### Example 1: Fitness Coach Agent

```python
# In agents.py, add this class:

class FitnessCoach(BaseAgent):
    """Specialized agent for dance fitness and conditioning"""
    
    def __init__(self, notion_client):
        super().__init__(name="Fitness Coach", model_name="models/gemini-2.0-flash-exp")
        self.notion = notion_client
    
    def create_warmup_routine(self, dance_style: str, duration: int = 10) -> str:
        """Generate a dance-specific warm-up routine"""
        
        prompt = f"""Create a {duration}-minute warm-up routine specifically for {dance_style} dancers.

Include:
1. Dynamic stretches (3 minutes)
2. Dance-specific movements (4 minutes)
3. Cardio activation (3 minutes)

For each section:
- List specific exercises with rep counts or duration
- Explain how it prepares the body for {dance_style}
- Include any safety tips

Format the routine as a clear, step-by-step guide."""

        return self.generate_response(prompt)
    
    def analyze_injury_risk(self, movement_pattern: str) -> str:
        """Analyze potential injury risks in dance movements"""
        
        context = f"Movement being analyzed: {movement_pattern}"
        
        prompt = """As a dance fitness specialist, analyze this movement for potential injury risks.

Provide:
1. **Risk Assessment**: Identify high-risk areas (knees, ankles, back, etc.)
2. **Common Issues**: What problems dancers often face with this movement
3. **Prevention Strategies**: Specific exercises and techniques to reduce risk
4. **When to Stop**: Warning signs that indicate rest is needed

Be professional but accessible in your language."""

        return self.generate_response(prompt, context)
    
    def suggest_conditioning_exercises(self, weak_area: str, skill_level: str) -> str:
        """Suggest exercises to strengthen specific areas"""
        
        prompt = f"""Create a conditioning program for a {skill_level} dancer who needs to strengthen their {weak_area}.

Provide:
1. **Assessment**: Why this area is important for dancing
2. **Exercise Routine**: 5-7 specific exercises with sets/reps
3. **Progression Plan**: How to increase difficulty over 4 weeks
4. **Dance Integration**: How to apply this strength to dancing

Include modifications for different fitness levels."""

        return self.generate_response(prompt)


# Add to app.py in the main_interface() function:

tab5 = st.tabs(["🏋️ Fitness Coach"])

with tab5:
    st.header("🏋️ Fitness & Conditioning")
    
    if 'fitness_coach' not in st.session_state:
        st.session_state.fitness_coach = FitnessCoach(st.session_state.notion_client)
    
    feature = st.selectbox(
        "What would you like help with?",
        ["Warm-up Routine", "Injury Prevention", "Conditioning Exercises"]
    )
    
    if feature == "Warm-up Routine":
        col1, col2 = st.columns(2)
        with col1:
            dance = st.selectbox("Dance Style", ["Cha Cha", "Rumba", "Swing", "Bolero", "Mambo"])
        with col2:
            duration = st.slider("Duration (minutes)", 5, 20, 10)
        
        if st.button("Generate Warm-up"):
            with st.spinner("Creating warm-up routine..."):
                warmup = st.session_state.fitness_coach.create_warmup_routine(dance, duration)
                st.markdown(warmup)
    
    elif feature == "Injury Prevention":
        movement = st.text_input("Movement to analyze", "Cuban hip action in Cha Cha")
        if st.button("Analyze Risk"):
            with st.spinner("Analyzing..."):
                analysis = st.session_state.fitness_coach.analyze_injury_risk(movement)
                st.markdown(analysis)
    
    elif feature == "Conditioning Exercises":
        col1, col2 = st.columns(2)
        with col1:
            area = st.selectbox("Target Area", ["Core", "Legs", "Balance", "Flexibility", "Stamina"])
        with col2:
            level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
        
        if st.button("Get Exercises"):
            with st.spinner("Creating program..."):
                program = st.session_state.fitness_coach.suggest_conditioning_exercises(area, level)
                st.markdown(program)
```

### Example 2: Competition Prep Agent

```python
class CompetitionPrep(BaseAgent):
    """Specialized agent for competition preparation"""
    
    def __init__(self, notion_client):
        super().__init__(name="Competition Coach")
        self.notion = notion_client
    
    def create_prep_timeline(self, competition_date: str, weeks_out: int, 
                            current_level: str, dances: list) -> str:
        """Create a competition preparation timeline"""
        
        context = f"""Competition Date: {competition_date}
Weeks Until Competition: {weeks_out}
Dancer Level: {current_level}
Dances to Prepare: {', '.join(dances)}"""

        prompt = """Create a week-by-week preparation timeline for this dancer.

For each week, provide:
1. **Training Focus**: What to prioritize this week
2. **Practice Schedule**: Recommended hours and structure
3. **Technical Goals**: Specific improvements to target
4. **Mental Preparation**: Mindset work and visualization
5. **Milestones**: What should be achieved by end of week

Structure: Give clear weekly breakdown leading up to competition day."""

        return self.generate_response(prompt, context)
    
    def prepare_mental_game(self, competition_type: str, anxiety_level: str) -> str:
        """Mental preparation strategies"""
        
        prompt = f"""Create a mental preparation guide for a {competition_type} competition.

The dancer reports {anxiety_level} anxiety levels.

Provide:
1. **Mindset Strategies**: Specific mental techniques
2. **Visualization Exercises**: Step-by-step visualization routines
3. **Pre-Competition Rituals**: Calming routines for competition day
4. **Handling Pressure**: In-the-moment coping strategies
5. **Positive Self-Talk**: Example affirmations and mantras

Be empathetic and practical."""

        return self.generate_response(prompt)
    
    def costume_and_presentation(self, dance_style: str, level: str) -> str:
        """Advice on costume and presentation"""
        
        prompt = f"""Provide guidance on costume and presentation for {level} level {dance_style} competitions.

Cover:
1. **Costume Guidelines**: What's appropriate and expected
2. **Hair & Makeup**: Tips for polished appearance
3. **Posture & Presence**: How to carry yourself on the floor
4. **Common Mistakes**: What to avoid
5. **Confidence Tips**: Looking and feeling your best

Be specific and helpful."""

        return self.generate_response(prompt)
```

---

## Customizing Prompts

### Making Prompts More Specific

**Before (Generic):**
```python
prompt = "Analyze this dance progress"
```

**After (Specific):**
```python
prompt = """As a professional DanceSport coach with 20 years of experience, analyze this dancer's progress.

Consider:
1. **Technical Development**: Footwork, posture, frame
2. **Musical Interpretation**: Timing, rhythm, expression
3. **Performance Quality**: Confidence, presentation, artistry
4. **Learning Trajectory**: Rate of improvement, consistency
5. **Next Steps**: Specific recommendations for advancement

Provide actionable insights in a supportive, professional tone."""
```

### Adding Context to Improve Responses

**Example:**
```python
def analyze_with_history(self, current_data, historical_data):
    context = f"""Current Performance:
{json.dumps(current_data, indent=2)}

Historical Performance (Last 3 Months):
{json.dumps(historical_data, indent=2)}"""

    prompt = """Compare current performance to historical data.

Identify:
1. Improvements and positive trends
2. Areas showing regression or stagnation
3. Patterns in practice consistency
4. Recommendations for future focus

Highlight both progress and areas needing attention."""

    return self.generate_response(prompt, context)
```

### Temperature and Creativity Settings

```python
# For factual, consistent responses (e.g., technique analysis)
self.model = genai.GenerativeModel(
    "models/gemini-2.0-flash-exp",
    generation_config={
        'temperature': 0.3,  # Lower = more factual
        'top_p': 0.8,
        'max_output_tokens': 2048,
    }
)

# For creative responses (e.g., practice routine ideas)
self.model = genai.GenerativeModel(
    "models/gemini-2.0-flash-exp",
    generation_config={
        'temperature': 0.9,  # Higher = more creative
        'top_p': 0.95,
        'max_output_tokens': 2048,
    }
)
```

---

## Working with Notion API

### Reading Page Content

```python
def get_page_content(notion_client, page_id):
    """Get all content blocks from a page"""
    
    # Get the page
    page = notion_client.get_page(page_id)
    
    # Get blocks (content)
    blocks = notion_client.get_block_children(page_id)
    
    content = []
    for block in blocks['results']:
        block_type = block['type']
        
        if block_type == 'paragraph':
            text = block['paragraph']['rich_text']
            if text:
                content.append(text[0]['plain_text'])
        
        elif block_type == 'heading_1':
            text = block['heading_1']['rich_text']
            if text:
                content.append(f"# {text[0]['plain_text']}")
        
        # Add more block types as needed
    
    return '\n\n'.join(content)
```

### Querying Databases with Filters

```python
def get_recent_practices(notion_client, database_id, days=7):
    """Get practice entries from the last N days"""
    
    from datetime import datetime, timedelta
    
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    filter_obj = {
        "property": "Created time",
        "date": {
            "after": cutoff_date
        }
    }
    
    sorts = [
        {
            "property": "Created time",
            "direction": "descending"
        }
    ]
    
    results = notion_client.query_database(
        database_id,
        filter_obj=filter_obj,
        sorts=sorts
    )
    
    return results['results']
```

### Creating Rich Text Comments

```python
def add_formatted_comment(notion_client, page_id, comment_parts):
    """Add a comment with formatting
    
    comment_parts = [
        {"text": "Great job on ", "bold": False},
        {"text": "Cuban motion", "bold": True},
        {"text": "! Keep it up.", "bold": False}
    ]
    """
    
    rich_text = []
    for part in comment_parts:
        text_obj = {
            "type": "text",
            "text": {"content": part["text"]}
        }
        
        if part.get("bold"):
            text_obj["annotations"] = {"bold": True}
        
        rich_text.append(text_obj)
    
    notion_client.add_comment(page_id, rich_text)
```

---

## UI Customization

### Adding Custom Metrics Dashboard

```python
# In app.py, create a new function:

def show_metrics_dashboard(dance_data):
    """Display comprehensive metrics"""
    
    st.subheader("📊 Performance Metrics")
    
    # Calculate metrics
    total_figures = len(dance_data)
    avg_practice_time = calculate_avg_practice_time(dance_data)
    consistency_score = calculate_consistency(dance_data)
    improvement_rate = calculate_improvement(dance_data)
    
    # Display in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Figures",
            value=total_figures,
            delta="+3 this week"
        )
    
    with col2:
        st.metric(
            label="Avg Practice Time",
            value=f"{avg_practice_time} min",
            delta="+5 min"
        )
    
    with col3:
        st.metric(
            label="Consistency Score",
            value=f"{consistency_score}%",
            delta="+10%"
        )
    
    with col4:
        st.metric(
            label="Improvement Rate",
            value=f"{improvement_rate}%",
            delta="+2%"
        )
    
    # Add progress bars
    st.progress(consistency_score / 100)
    st.caption(f"Practice Consistency: {consistency_score}%")
```

### Creating Interactive Charts

```python
# Install plotly first: pip install plotly

import plotly.graph_objects as go
import plotly.express as px

def create_progress_chart(practice_history):
    """Create interactive progress chart"""
    
    # Prepare data
    dates = [entry['date'] for entry in practice_history]
    scores = [entry['score'] for entry in practice_history]
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        name='Progress',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Progress Over Time",
        xaxis_title="Date",
        yaxis_title="Skill Score",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
```

### Adding Sidebar Navigation

```python
def create_navigation():
    """Enhanced sidebar navigation"""
    
    st.sidebar.title("🎯 Navigation")
    
    pages = {
        "🏠 Home": "home",
        "📊 Progress": "progress",
        "🏃 Practice": "practice",
        "💬 Chat": "chat",
        "⚙️ Settings": "settings"
    }
    
    selection = st.sidebar.radio(
        "Go to",
        list(pages.keys())
    )
    
    return pages[selection]

# In main():
current_page = create_navigation()

if current_page == "home":
    show_home_page()
elif current_page == "progress":
    show_progress_page()
# ... etc
```

---

## Practice Exercises

### Exercise 1: Add a Motivational Quote Feature
Create a function that displays a random motivational quote for dancers.

### Exercise 2: Build a Practice Logger
Create a simple form where users can log their daily practice sessions.

### Exercise 3: Create a Progress Report Generator
Generate a weekly or monthly progress report in PDF format.

### Exercise 4: Add Email Notifications
Integrate email notifications for practice reminders.

### Exercise 5: Build a Goal Tracker
Create a system to set and track dance goals over time.

---

## Tips for Success

1. **Start Small**: Begin with simple modifications before building complex features
2. **Test Incrementally**: Test each change before moving to the next
3. **Read Error Messages**: They usually tell you exactly what's wrong
4. **Use Print Statements**: Debug by printing variable values
5. **Consult Documentation**: 
   - [Streamlit Docs](https://docs.streamlit.io)
   - [Notion API Docs](https://developers.notion.com)
   - [Google AI Studio](https://ai.google.dev)

---

## Additional Resources

- **Streamlit Gallery**: https://streamlit.io/gallery
- **Notion API Examples**: https://github.com/makenotion/notion-sdk-py
- **Gemini Cookbook**: https://github.com/google-gemini/cookbook

---

Happy Learning! 🎓💃
