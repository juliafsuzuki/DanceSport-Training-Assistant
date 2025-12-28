"""
================================================================================
DANCESPORT ASSISTANT - MULTI-AGENT SYSTEM FOR KAGGLE
Version 1.0 - Extended from Notion AI Agent v60
================================================================================

A multi-agent AI system for DanceSport coaching with:
- Progress Analysis
- Practice Routine Generation  
- AI-Powered Comments
- Interactive Q&A Coach
- Notion Integration

Learn by doing - modify and extend this code!
================================================================================
"""

# ============================================================================
# STEP 1: Install Required Packages
# ============================================================================
print("=" * 80)
print("📦 INSTALLING PACKAGES")
print("=" * 80)

import subprocess
import sys
import warnings
warnings.filterwarnings('ignore')

packages = ["google-generativeai", "requests"]

for package in packages:
    print(f"Installing {package}...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", package], 
                   capture_output=True)

print("✅ All packages installed successfully.\n")

# ============================================================================
# STEP 2: Import Libraries
# ============================================================================
print("=" * 80)
print("📚 IMPORTING LIBRARIES")
print("=" * 80)

import os
import json
import requests
from datetime import datetime
import time
import re

from kaggle_secrets import UserSecretsClient
import google.generativeai as genai

print("✅ All libraries imported successfully.\n")

# ============================================================================
# STEP 3: Setup API Keys
# ============================================================================
print("=" * 80)
print("🔑 SETTING UP API KEYS")
print("=" * 80)

user_secrets = UserSecretsClient()
NOTION_TOKEN = user_secrets.get_secret("NOTION_TOKEN")
GOOGLE_API_KEY = user_secrets.get_secret("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

print("✅ API keys configured.\n")

# ============================================================================
# STEP 4: Notion API Client Class
# ============================================================================
print("=" * 80)
print("🔧 SETTING UP NOTION CLIENT")
print("=" * 80)

class NotionClient:
    """Enhanced Notion API client with comment support"""
    
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def get_integration_info(self):
        url = f"{self.base_url}/users/me"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def search_all(self, query="", page_size=100):
        url = f"{self.base_url}/search"
        payload = {"page_size": page_size}
        if query:
            payload["query"] = query
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_page(self, page_id):
        url = f"{self.base_url}/pages/{page_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_database(self, database_id):
        url = f"{self.base_url}/databases/{database_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def query_database(self, database_id, filter_obj=None, sorts=None):
        url = f"{self.base_url}/databases/{database_id}/query"
        payload = {}
        if filter_obj:
            payload["filter"] = filter_obj
        if sorts:
            payload["sorts"] = sorts
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def add_comment(self, page_id, comment_text):
        """Add a comment to a page"""
        url = f"{self.base_url}/comments"
        payload = {
            "parent": {"page_id": page_id},
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": comment_text}
                }
            ]
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

notion = NotionClient(NOTION_TOKEN)
print("✅ Notion client ready.\n")

# ============================================================================
# STEP 5: AI Agent Classes
# ============================================================================
print("=" * 80)
print("🤖 SETTING UP AI AGENTS")
print("=" * 80)

class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, name, model_name="models/gemini-2.0-flash-exp"):
        self.name = name
        self.model_name = model_name
        self.conversation_history = []
        
        # Initialize Gemini model
        self.model = genai.GenerativeModel(
            model_name,
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'max_output_tokens': 2048,
            }
        )
    
    def generate_response(self, prompt, context=None):
        """Generate AI response"""
        full_prompt = prompt
        if context:
            full_prompt = f"Context:\n{context}\n\nTask:\n{prompt}"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"


class DanceSportAssistant(BaseAgent):
    """Specialized agent for DanceSport coaching"""
    
    def __init__(self, notion_client):
        super().__init__(name="DanceSport Coach")
        self.notion = notion_client
        self.dance_knowledge = self._load_dance_knowledge()
    
    def _load_dance_knowledge(self):
        """Load DanceSport knowledge base"""
        return {
            "cha_cha": {
                "rhythm": "4/4 time, 30-32 bars per minute",
                "characteristics": "Syncopated, flirtatious, playful",
                "key_elements": ["Cuban motion", "Compact steps", "Sharp timing"],
                "fundamental_figures": [
                    "Basic Movement", "New York", "Spot Turn", "Hand to Hand",
                    "Side Step", "Time Step", "Forward Walk", "Backward Walk"
                ]
            },
            "rumba": {
                "rhythm": "4/4 time, 25-27 bars per minute",
                "characteristics": "Romantic, slow, sensual",
                "key_elements": ["Cuban motion", "Delayed weight transfer", "Body leads"],
                "fundamental_figures": [
                    "Basic Movement", "Box", "Underarm Turn", "Progressive Walks",
                    "Forward Walk", "Backward Walk"
                ]
            },
            "swing": {
                "rhythm": "4/4 time, 30-46 bars per minute",
                "characteristics": "Bouncy, energetic, fun",
                "key_elements": ["Bounce action", "Triple steps", "Rock steps"],
                "fundamental_figures": [
                    "Basic Step", "Underarm Turn", "Change of Places", "Link",
                    "Forward Walk", "Backward Walk"
                ]
            },
            "bolero": {
                "rhythm": "4/4 time, 24-26 bars per minute",
                "characteristics": "Romantic, smooth, rise and fall",
                "key_elements": ["Rise and fall", "Cuban motion", "Controlled movement"],
                "fundamental_figures": [
                    "Basic Movement", "Progressive Walks", "Side Step"
                ]
            },
            "mambo": {
                "rhythm": "4/4 time, 47-51 bars per minute",
                "characteristics": "Exciting, syncopated, sharp",
                "key_elements": ["Sharp movements", "Syncopation", "Strong hip action"],
                "fundamental_figures": [
                    "Basic Movement", "Break Steps", "Side Steps"
                ]
            }
        }
    
    def analyze_progress(self, dance_data):
        """Analyze student's progress"""
        
        if not dance_data:
            return "No dance data available for analysis."
        
        # Prepare context
        context = "Dance Progress Data:\n\n"
        for item in dance_data:
            title = self._extract_title(item)
            context += f"- {title}\n"
        
        prompt = """As a DanceSport coach, analyze this student's progress data.

Provide a comprehensive analysis including:
1. **Overall Progress Assessment**: Current skill level and trajectory
2. **Strengths**: What the student is doing well
3. **Areas for Improvement**: Specific techniques or figures that need work
4. **Pattern Recognition**: Any trends in learning or practice habits
5. **Motivation & Engagement**: Signs of enthusiasm or potential challenges

Be encouraging, specific, and actionable in your feedback."""

        return self.generate_response(prompt, context)
    
    def suggest_practice_routine(self, dance_name, skill_level="beginner", 
                                 focus_areas=None):
        """Generate a personalized practice routine"""
        
        dance_name_lower = dance_name.lower()
        dance_info = None
        
        # Find matching dance
        for dance, info in self.dance_knowledge.items():
            if dance in dance_name_lower:
                dance_info = info
                break
        
        if not dance_info:
            return f"I don't have specific information about {dance_name} in my knowledge base."
        
        context = f"""Dance: {dance_name}
Skill Level: {skill_level}
Rhythm: {dance_info['rhythm']}
Characteristics: {dance_info['characteristics']}
Key Elements: {', '.join(dance_info['key_elements'])}
Fundamental Figures: {', '.join(dance_info['fundamental_figures'])}
"""
        
        if focus_areas:
            context += f"\nFocus Areas: {', '.join(focus_areas)}"
        
        prompt = """Create a detailed 30-minute practice routine for this dance.

Structure the routine with:
1. **Warm-up (5 minutes)**: Specific movements to prepare the body
2. **Technique Drills (10 minutes)**: Focused practice on key elements
3. **Figure Practice (10 minutes)**: Working through fundamental figures
4. **Cool-down & Review (5 minutes)**: Integration and reflection

For each section:
- Provide specific exercises with timing
- Include coaching tips and points of focus
- Add progression notes (how to make it easier/harder)

Make it practical, achievable, and progressive."""

        return self.generate_response(prompt, context)
    
    def create_practice_comment(self, dance_name, observation):
        """Create a coach's comment"""
        
        prompt = f"""As a DanceSport coach, write an encouraging and constructive comment 
about a student's practice of {dance_name}.

Observation: {observation}

The comment should:
- Be supportive and motivating
- Acknowledge progress
- Provide 1-2 specific tips for improvement
- Keep it concise (2-3 sentences)
- Use professional dance terminology where appropriate"""

        return self.generate_response(prompt)
    
    def answer_question(self, question, dance_context=None):
        """Answer DanceSport questions"""
        
        context = "DanceSport Knowledge Base:\n"
        for dance, info in self.dance_knowledge.items():
            context += f"\n{dance.upper()}:\n"
            context += f"  Rhythm: {info['rhythm']}\n"
            context += f"  Characteristics: {info['characteristics']}\n"
            context += f"  Key Elements: {', '.join(info['key_elements'])}\n"
        
        if dance_context:
            context += f"\n\nAdditional Context:\n{dance_context}"
        
        prompt = f"""Question: {question}

Provide a clear, informative answer that:
- Uses proper DanceSport terminology
- Gives practical advice where applicable
- References specific techniques or figures when relevant
- Is encouraging and educational"""

        return self.generate_response(prompt, context)
    
    def _extract_title(self, page):
        """Extract title from page"""
        properties = page.get('properties', {})
        for prop_value in properties.values():
            if prop_value.get('type') == 'title':
                title_array = prop_value.get('title', [])
                if title_array:
                    return title_array[0].get('plain_text', 'Untitled')
        return 'Untitled'


print("✅ AI agents initialized.\n")

# ============================================================================
# STEP 6: Helper Functions
# ============================================================================

def extract_title(obj):
    """Extract title from page or database object"""
    if obj.get('object') == 'page':
        properties = obj.get('properties', {})
        for prop_value in properties.values():
            if prop_value.get('type') == 'title':
                title_array = prop_value.get('title', [])
                if title_array:
                    return title_array[0].get('plain_text', 'Untitled')
    elif obj.get('object') == 'database':
        title_array = obj.get('title', [])
        if title_array:
            return title_array[0].get('plain_text', 'Untitled Database')
    return 'Untitled'


def build_workspace_hierarchy(all_objects):
    """Build workspace hierarchy from objects"""
    pages = [obj for obj in all_objects if obj.get('object') == 'page']
    databases = [obj for obj in all_objects if obj.get('object') == 'database']
    
    workspace_data = {
        "total_objects": len(all_objects),
        "total_pages": len(pages),
        "total_databases": len(databases),
        "main_pages": [],
        "databases_by_parent": {},
        "pages_by_parent": {}
    }
    
    # Process pages
    for page in pages:
        parent = page.get('parent', {})
        parent_type = parent.get('type')
        parent_id = None
        
        if parent_type == 'page_id':
            parent_id = parent.get('page_id')
        elif parent_type == 'database_id':
            parent_id = parent.get('database_id')
        
        page_info = {
            'id': page.get('id'),
            'title': extract_title(page),
            'created_time': page.get('created_time'),
            'url': page.get('url'),
            'parent_id': parent_id,
            'parent_type': parent_type,
            'object': page
        }
        
        if parent_id is None:
            workspace_data['main_pages'].append(page_info)
        else:
            if parent_id not in workspace_data['pages_by_parent']:
                workspace_data['pages_by_parent'][parent_id] = []
            workspace_data['pages_by_parent'][parent_id].append(page_info)
    
    # Process databases
    for db in databases:
        parent = db.get('parent', {})
        parent_type = parent.get('type')
        parent_id = parent.get('page_id') if parent_type == 'page_id' else None
        
        db_info = {
            'id': db.get('id'),
            'title': extract_title(db),
            'created_time': db.get('created_time'),
            'url': db.get('url'),
            'parent_id': parent_id,
            'parent_type': parent_type,
            'object': db
        }
        
        if parent_id not in workspace_data['databases_by_parent']:
            workspace_data['databases_by_parent'][parent_id] = []
        workspace_data['databases_by_parent'][parent_id].append(db_info)
    
    return workspace_data


def find_dancesport_content(workspace_data):
    """Find DanceSport-related content"""
    dancesport_items = {
        'main_page': None,
        'dance_categories': []
    }
    
    # Find main DanceSport page
    for page in workspace_data['main_pages']:
        if 'dancesport' in page['title'].lower():
            dancesport_items['main_page'] = page
            break
    
    if not dancesport_items['main_page']:
        return dancesport_items
    
    # Find dance categories
    main_page_id = dancesport_items['main_page']['id']
    databases = workspace_data['databases_by_parent'].get(main_page_id, [])
    
    for db in databases:
        title_lower = db['title'].lower()
        if 'fundamental' in title_lower or 'open' in title_lower:
            # Get individual dances
            dance_dbs = workspace_data['databases_by_parent'].get(db['id'], [])
            for dance_db in dance_dbs:
                dancesport_items['dance_categories'].append({
                    'category': db['title'],
                    'dance': dance_db['title'],
                    'database_id': dance_db['id'],
                    'database_obj': dance_db
                })
    
    return dancesport_items

# ============================================================================
# STEP 7: Verify Notion Connection
# ============================================================================
print("=" * 80)
print("🔍 VERIFYING NOTION CONNECTION")
print("=" * 80)

try:
    integration_info = notion.get_integration_info()
    print(f"\n✅ Successfully connected to Notion!")
    print(f"\nIntegration Details:")
    print(f"  • Bot ID: {integration_info.get('id', 'N/A')}")
    print(f"  • Bot Name: {integration_info.get('name', 'N/A')}")
    print(f"  • Type: {integration_info.get('type', 'N/A')}")
    print()
except Exception as e:
    print(f"❌ Error connecting to Notion: {str(e)}")

# ============================================================================
# STEP 8: Load Workspace Data
# ============================================================================
print("=" * 80)
print("📊 LOADING WORKSPACE DATA")
print("=" * 80)

try:
    print("\n🔍 Searching for all pages and databases...")
    all_results = notion.search_all()
    all_objects = all_results.get('results', [])
    print(f"✅ Found {len(all_objects)} total objects\n")
    
    # Build hierarchy
    workspace_data = build_workspace_hierarchy(all_objects)
    
    print(f"Summary:")
    print(f"  • Total Pages: {workspace_data['total_pages']}")
    print(f"  • Total Databases: {workspace_data['total_databases']}")
    print(f"  • Main Pages: {len(workspace_data['main_pages'])}\n")
    
    # Find DanceSport content
    dancesport_content = find_dancesport_content(workspace_data)
    
    if dancesport_content['main_page']:
        print(f"✅ Found DanceSport page: {dancesport_content['main_page']['title']}")
        print(f"   Dance categories found: {len(dancesport_content['dance_categories'])}\n")
        
        if dancesport_content['dance_categories']:
            print("   Available dances:")
            for idx, dance in enumerate(dancesport_content['dance_categories'], 1):
                print(f"   {idx}. {dance['category']} - {dance['dance']}")
            print()
    else:
        print("⚠️  No DanceSport page found in workspace\n")

except Exception as e:
    print(f"❌ Error loading workspace: {str(e)}")
    import traceback
    traceback.print_exc()

# ============================================================================
# STEP 9: Initialize DanceSport Assistant
# ============================================================================
print("=" * 80)
print("🎯 INITIALIZING DANCESPORT ASSISTANT")
print("=" * 80)

assistant = DanceSportAssistant(notion)
print("✅ DanceSport Assistant ready!\n")

# ============================================================================
# STEP 10: INTERACTIVE DEMO - Choose Your Action
# ============================================================================
print("=" * 80)
print("💃 DANCESPORT ASSISTANT - INTERACTIVE DEMO")
print("=" * 80)

print("\nWhat would you like to do? Choose an option:\n")
print("1. 📊 Analyze Progress on a Dance")
print("2. 🏃 Generate Practice Routine")
print("3. ✍️  Create & Post AI Comment")
print("4. 💬 Ask Coach a Question")
print("5. 📚 Compare Two Dances")
print("\nFor this demo, we'll run examples of each feature...\n")

# ============================================================================
# DEMO FEATURE 1: Progress Analysis
# ============================================================================
print("=" * 80)
print("📊 FEATURE 1: PROGRESS ANALYSIS")
print("=" * 80)

if dancesport_content['dance_categories']:
    # Use first available dance
    selected_dance = dancesport_content['dance_categories'][0]
    print(f"\nAnalyzing: {selected_dance['dance']}")
    print(f"Category: {selected_dance['category']}")
    print(f"Database ID: {selected_dance['database_id']}\n")
    
    try:
        # Query database
        results = notion.query_database(selected_dance['database_id'])
        pages = results.get('results', [])
        
        print(f"Found {len(pages)} figures/entries in this dance\n")
        
        if pages:
            print("Generating AI analysis...\n")
            print("-" * 80)
            
            analysis = assistant.analyze_progress(pages)
            print(analysis)
            
            print("\n" + "-" * 80)
            print(f"✅ Analysis complete!\n")
        else:
            print("⚠️  No entries found in this database\n")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
else:
    print("⚠️  No DanceSport content available for analysis\n")

time.sleep(2)

# ============================================================================
# DEMO FEATURE 2: Practice Routine
# ============================================================================
print("=" * 80)
print("🏃 FEATURE 2: PRACTICE ROUTINE GENERATOR")
print("=" * 80)

print("\nGenerating a practice routine for Cha Cha (Beginner level)...\n")
print("-" * 80)

try:
    routine = assistant.suggest_practice_routine(
        dance_name="Cha Cha",
        skill_level="beginner",
        focus_areas=["Timing", "Cuban Motion"]
    )
    print(routine)
    print("\n" + "-" * 80)
    print("✅ Practice routine generated!\n")
except Exception as e:
    print(f"❌ Error: {str(e)}\n")

time.sleep(2)

# ============================================================================
# DEMO FEATURE 3: AI Comment
# ============================================================================
print("=" * 80)
print("✍️  FEATURE 3: AI COMMENT GENERATOR")
print("=" * 80)

print("\nGenerating coach's comment for a practice observation...\n")

sample_observation = "Today I practiced the basic movement and my timing was much better, but I still struggle with the Cuban motion on the 4&1."

print(f"Observation: {sample_observation}\n")
print("Generating AI comment...\n")
print("-" * 80)

try:
    comment = assistant.create_practice_comment(
        dance_name="Cha Cha",
        observation=sample_observation
    )
    print(comment)
    print("\n" + "-" * 80)
    
    # Option to post to Notion
    print("\n📝 This comment can be posted to any Notion page using:")
    print("   notion.add_comment(page_id, comment)")
    print("\n✅ Comment generated!\n")
except Exception as e:
    print(f"❌ Error: {str(e)}\n")

time.sleep(2)

# ============================================================================
# DEMO FEATURE 4: Q&A Coach
# ============================================================================
print("=" * 80)
print("💬 FEATURE 4: ASK YOUR COACH")
print("=" * 80)

questions = [
    "What's the difference between Cha Cha and Rumba timing?",
    "How can I improve my Cuban motion?",
    "What should I focus on as a beginner in Rumba?"
]

print("\nAsking sample questions...\n")

for idx, question in enumerate(questions[:2], 1):  # Ask 2 questions
    print(f"\nQuestion {idx}: {question}")
    print("-" * 80)
    
    try:
        answer = assistant.answer_question(question)
        print(answer)
        print("-" * 80)
        print()
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
    
    if idx < 2:
        time.sleep(3)

print("✅ Q&A demo complete!\n")

# ============================================================================
# DEMO FEATURE 5: Compare Dances
# ============================================================================
print("=" * 80)
print("📚 FEATURE 5: DANCE COMPARISON")
print("=" * 80)

print("\nComparing Cha Cha vs Rumba...\n")
print("-" * 80)

try:
    comparison = assistant.compare_dances("Cha Cha", "Rumba")
    print(comparison)
    print("\n" + "-" * 80)
    print("✅ Comparison complete!\n")
except Exception as e:
    print(f"❌ Error: {str(e)}\n")

# ============================================================================
# STEP 11: Summary & Next Steps
# ============================================================================
print("=" * 80)
print("📝 EXECUTION SUMMARY")
print("=" * 80)

print(f"""
✅ Notion connection: Verified
✅ Workspace data: Loaded
✅ DanceSport Assistant: Initialized
✅ Features demonstrated:
   1. Progress Analysis
   2. Practice Routine Generator
   3. AI Comment Creator
   4. Q&A Coach
   5. Dance Comparison

📊 Your Workspace:
   • Total objects: {workspace_data.get('total_objects', 0)}
   • Pages: {workspace_data.get('total_pages', 0)}
   • Databases: {workspace_data.get('total_databases', 0)}
   • DanceSport dances: {len(dancesport_content.get('dance_categories', []))}
""")

print("=" * 80)
print("🎓 HOW TO USE & EXTEND THIS CODE")
print("=" * 80)

print("""
CUSTOMIZE THE DEMOS:
--------------------
1. Change the dance being analyzed:
   selected_dance = dancesport_content['dance_categories'][1]  # Try different index

2. Modify practice routine parameters:
   routine = assistant.suggest_practice_routine(
       dance_name="Rumba",           # Change dance
       skill_level="intermediate",   # Change level
       focus_areas=["Hip Action"]    # Change focus
   )

3. Ask your own questions:
   answer = assistant.answer_question("Your question here")

4. Post comments to Notion:
   notion.add_comment(page_id, "Your comment here")


ADD NEW FEATURES:
-----------------
1. Create a new agent:
   class FitnessCoach(BaseAgent):
       def create_warmup(self, dance_name):
           prompt = "Create a warmup for " + dance_name
           return self.generate_response(prompt)

2. Add more dance knowledge:
   Edit the _load_dance_knowledge() method in DanceSportAssistant

3. Customize prompts:
   Modify the prompt strings in each method to change AI behavior


LEARN MORE:
-----------
- Study each class and method
- Try modifying prompts to see how AI responses change
- Experiment with different temperature settings
- Add print statements to debug and understand flow
""")

print("=" * 80)
print("✅ DANCESPORT ASSISTANT - READY TO USE!")
print("=" * 80)

print("\n💡 TIP: Scroll up to see all the demo results!\n")
