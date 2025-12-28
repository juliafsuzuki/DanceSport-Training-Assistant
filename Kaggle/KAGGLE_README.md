# 💃 DanceSport Assistant - Kaggle Version

**A multi-agent AI system for DanceSport coaching that runs in Kaggle notebooks!**

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Create a New Kaggle Notebook

1. Go to https://www.kaggle.com
2. Click **"New Notebook"**
3. You'll see an empty code cell

### Step 2: Add Your API Keys to Kaggle Secrets

**For Notion Token:**
1. In your notebook, click **"Add-ons"** → **"Secrets"**
2. Click **"+ Add a new secret"**
3. Label: `NOTION_TOKEN`
4. Value: Paste your Notion integration token
5. Click **"Add"**

**For Google API Key:**
1. Click **"+ Add a new secret"** again
2. Label: `GOOGLE_API_KEY`
3. Value: Paste your Google API key
4. Click **"Add"**

### Step 3: Copy the Code

1. Open `dancesport_assistant_kaggle.py`
2. **Copy ALL the code** (Ctrl+A, Ctrl+C)
3. **Paste into your Kaggle notebook** (Ctrl+V)

### Step 4: Run It!

1. Click **"Run All"** or press **Shift + Enter**
2. Wait 2-3 minutes for execution
3. Scroll through to see all the results!

---

## 📖 What This Code Does

### Automatic Demo Sequence

When you run the notebook, it automatically demonstrates all features:

**1. 📊 Progress Analysis**
- Analyzes your first available dance database
- Provides comprehensive coaching feedback
- Identifies strengths and areas for improvement

**2. 🏃 Practice Routine**
- Generates a 30-minute Cha Cha practice routine
- Includes warm-up, drills, practice, and cool-down
- Customized for beginner level

**3. ✍️ AI Comment Generator**
- Creates a professional coaching comment
- Based on a sample practice observation
- Can be posted directly to Notion pages

**4. 💬 Q&A Coach**
- Answers 2 sample DanceSport questions
- Uses the built-in dance knowledge base
- Provides educational, practical advice

**5. 📚 Dance Comparison**
- Compares Cha Cha vs Rumba
- Explains differences in timing, style, and technique

---

## 🎨 How to Customize

### Change the Dance Being Analyzed

Find this section in the code:
```python
# Use first available dance
selected_dance = dancesport_content['dance_categories'][0]
```

Change to:
```python
selected_dance = dancesport_content['dance_categories'][1]  # Try second dance
```

### Generate Different Practice Routines

Find this section:
```python
routine = assistant.suggest_practice_routine(
    dance_name="Cha Cha",
    skill_level="beginner",
    focus_areas=["Timing", "Cuban Motion"]
)
```

Try:
```python
routine = assistant.suggest_practice_routine(
    dance_name="Rumba",
    skill_level="intermediate",
    focus_areas=["Hip Action", "Body Leads"]
)
```

### Ask Your Own Questions

Find this section:
```python
questions = [
    "What's the difference between Cha Cha and Rumba timing?",
    # Add your own questions here!
]
```

Add your questions:
```python
questions = [
    "How do I improve my posture in Swing?",
    "What's the best way to practice Cuban motion at home?",
    "How can I make my Rumba more expressive?"
]
```

### Post Comments to Notion

Add this code at the end of the notebook:
```python
# Get a page ID from your workspace
page_id = "your-page-id-here"  # Replace with actual page ID

# Create a comment
my_comment = "Great practice session today! Keep focusing on timing."

# Post it
result = notion.add_comment(page_id, my_comment)
print("✅ Comment posted!")
```

---

## 🔧 Advanced Customization

### Add a New Dance to Knowledge Base

Find the `_load_dance_knowledge()` method and add:

```python
"samba": {
    "rhythm": "2/4 time, 50-52 bars per minute",
    "characteristics": "Energetic, bouncy, carnival spirit",
    "key_elements": ["Bounce action", "Rolling", "Samba walks"],
    "fundamental_figures": [
        "Basic Movement", "Whisks", "Samba Walks", "Volta"
    ]
}
```

### Create Your Own Agent

Add this code after the `DanceSportAssistant` class:

```python
class FitnessCoach(BaseAgent):
    """Agent for fitness and conditioning advice"""
    
    def __init__(self, notion_client):
        super().__init__(name="Fitness Coach")
        self.notion = notion_client
    
    def create_warmup(self, dance_name, duration=10):
        prompt = f"""Create a {duration}-minute warm-up routine 
        specifically for {dance_name} dancers.
        
        Include:
        1. Dynamic stretches
        2. Dance-specific movements
        3. Cardio activation
        """
        return self.generate_response(prompt)

# Use it
fitness_coach = FitnessCoach(notion)
warmup = fitness_coach.create_warmup("Cha Cha", 10)
print(warmup)
```

### Change AI Temperature (Creativity Level)

Find the `BaseAgent` class initialization:

```python
self.model = genai.GenerativeModel(
    model_name,
    generation_config={
        'temperature': 0.7,  # Change this: 0.0-1.0
        # 0.0-0.3 = More factual
        # 0.4-0.7 = Balanced (default)
        # 0.8-1.0 = More creative
    }
)
```

---

## 📚 Understanding the Code Structure

### Main Components

```
📦 DanceSport Assistant
├── 🔧 NotionClient
│   ├── Connect to Notion API
│   ├── Search pages/databases
│   ├── Query databases
│   └── Add comments
│
├── 🤖 BaseAgent
│   ├── AI model initialization
│   ├── Prompt generation
│   └── Response handling
│
├── 💃 DanceSportAssistant (extends BaseAgent)
│   ├── Dance knowledge base
│   ├── Progress analysis
│   ├── Practice routines
│   ├── Comment generation
│   ├── Q&A system
│   └── Dance comparison
│
└── 🛠️ Helper Functions
    ├── extract_title()
    ├── build_workspace_hierarchy()
    └── find_dancesport_content()
```

### Code Flow

```
1. Install packages
2. Import libraries
3. Setup API keys
4. Initialize Notion client
5. Create AI agents
6. Load workspace data
7. Run demos:
   ├── Progress analysis
   ├── Practice routine
   ├── Comment generation
   ├── Q&A coach
   └── Dance comparison
8. Display summary
```

---

## 🎓 Learning Exercises

### Exercise 1: Analyze a Different Dance
**Task**: Modify the code to analyze your Rumba progress instead of Cha Cha

**Hint**: Look for `selected_dance = dancesport_content['dance_categories'][0]`

### Exercise 2: Create Custom Questions
**Task**: Ask 3 questions about Swing dance

**Hint**: Modify the `questions` list in Feature 4

### Exercise 3: Post a Real Comment
**Task**: Generate a comment and post it to one of your Notion pages

**Hint**: 
```python
# Find a page ID from your workspace printout
# Use notion.add_comment(page_id, comment_text)
```

### Exercise 4: Add a New Agent
**Task**: Create a "CompetitionCoach" agent that gives pre-competition advice

**Template**:
```python
class CompetitionCoach(BaseAgent):
    def prepare_for_competition(self, days_until, dance_list):
        prompt = f"Create a {days_until}-day prep plan for: {dance_list}"
        return self.generate_response(prompt)
```

### Exercise 5: Customize Practice Routines
**Task**: Generate a 45-minute intermediate Rumba routine focusing on "Expression" and "Musicality"

---

## 🐛 Troubleshooting

### Error: "Secret not found"
**Solution**: Make sure you added both secrets in Kaggle:
- `NOTION_TOKEN`
- `GOOGLE_API_KEY`

### Error: "Page not found" or "Database not found"
**Solution**: 
1. Make sure your Notion pages are shared with your integration
2. Check that you have a page titled "DanceSport"

### Error: "Rate limit exceeded"
**Solution**: 
- Add `time.sleep(2)` between API calls
- The code already has delays built in

### No DanceSport content found
**Solution**: 
1. Create a page in Notion called "DanceSport"
2. Add databases for dances (e.g., "Fundamental Cha Cha")
3. Share the page with your integration
4. Re-run the notebook

---

## 📊 Expected Output

When you run the notebook, you should see:

```
================================================================================
📦 INSTALLING PACKAGES
================================================================================
✅ All packages installed successfully.

================================================================================
📚 IMPORTING LIBRARIES
================================================================================
✅ All libraries imported successfully.

... (setup continues) ...

================================================================================
💃 DANCESPORT ASSISTANT - INTERACTIVE DEMO
================================================================================

... (5 feature demos) ...

================================================================================
✅ DANCESPORT ASSISTANT - READY TO USE!
================================================================================
```

---

## 🎯 Next Steps

Once you're comfortable with the basic usage:

1. **Explore**: Try all the customization examples
2. **Experiment**: Change prompts and see how responses change
3. **Extend**: Add new agents or features
4. **Share**: Share your notebook with other dancers!

---

## 💡 Pro Tips

1. **Save Your Work**: Click "Save Version" in Kaggle to save your customizations
2. **Make It Private**: Click "Share" → "Make Private" if it contains sensitive data
3. **Duplicate Before Experimenting**: "File" → "Save & Run Version" to create a backup
4. **Use Comments**: Add `# Your notes here` to remember what you changed

---

## 🔗 Resources

- **Kaggle Notebooks**: https://www.kaggle.com/docs/notebooks
- **Notion API**: https://developers.notion.com
- **Google Gemini**: https://ai.google.dev

---

## 🆘 Need Help?

If you get stuck:
1. Check the error message carefully
2. Look for the line number in the error
3. Check the Troubleshooting section above
4. Try running individual sections of code

---

**Happy Dancing! 💃🕺**

*This is a learning project - experiment, break things, and learn!*
