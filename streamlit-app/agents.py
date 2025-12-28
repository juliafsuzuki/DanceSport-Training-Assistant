"""
AI Agent classes for DanceSport Assistant
"""

import google.generativeai as genai
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, name: str, model_name: str = "models/gemini-2.0-flash-exp"):
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
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate AI response with optional context"""
        full_prompt = prompt
        if context:
            full_prompt = f"Context:\n{context}\n\nTask:\n{prompt}"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"


class DanceSportAssistant(BaseAgent):
    """Specialized agent for DanceSport coaching and progress tracking"""
    
    def __init__(self, notion_client):
        super().__init__(name="DanceSport Coach", model_name="models/gemini-2.0-flash-exp")
        self.notion = notion_client
        self.dance_knowledge = self._load_dance_knowledge()
    
    def _load_dance_knowledge(self) -> Dict:
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
    
    def analyze_progress(self, dance_data: List[Dict]) -> str:
        """Analyze student's progress across dance figures"""
        
        if not dance_data:
            return "No dance data available for analysis."
        
        # Prepare context
        context = "Dance Progress Data:\n\n"
        for item in dance_data:
            context += f"- {item.get('title', 'Unknown')}\n"
            if item.get('properties'):
                context += f"  Properties: {json.dumps(item['properties'], indent=2)}\n"
        
        prompt = """As a DanceSport coach, analyze this student's progress data.

Provide a comprehensive analysis including:
1. **Overall Progress Assessment**: Current skill level and trajectory
2. **Strengths**: What the student is doing well
3. **Areas for Improvement**: Specific techniques or figures that need work
4. **Pattern Recognition**: Any trends in learning or practice habits
5. **Motivation & Engagement**: Signs of enthusiasm or potential challenges

Be encouraging, specific, and actionable in your feedback."""

        return self.generate_response(prompt, context)
    
    def suggest_practice_routine(self, dance_name: str, skill_level: str = "beginner", 
                                 focus_areas: Optional[List[str]] = None) -> str:
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
    
    def create_practice_comment(self, dance_name: str, observation: str) -> str:
        """Create a coach's comment for a practice session"""
        
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
    
    def answer_question(self, question: str, dance_context: Optional[str] = None) -> str:
        """Answer DanceSport-related questions"""
        
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
    
    def compare_dances(self, dance1: str, dance2: str) -> str:
        """Compare two dances"""
        
        info1 = self.dance_knowledge.get(dance1.lower())
        info2 = self.dance_knowledge.get(dance2.lower())
        
        if not info1 or not info2:
            return "I don't have information about one or both of these dances."
        
        context = f"""Dance 1: {dance1}
{json.dumps(info1, indent=2)}

Dance 2: {dance2}
{json.dumps(info2, indent=2)}"""

        prompt = """Compare these two dances in terms of:

1. **Timing & Rhythm**: How they differ musically
2. **Character & Style**: The emotional quality and expression
3. **Technical Elements**: Key movement differences
4. **Difficulty Level**: Which aspects are more challenging
5. **Common Mistakes**: What beginners often struggle with in each

Provide a clear, educational comparison that helps a student understand both dances better."""

        return self.generate_response(prompt, context)


class ProgressTracker:
    """Helper class to track and visualize progress"""
    
    def __init__(self, notion_client):
        self.notion = notion_client
    
    def get_practice_stats(self, database_id: str) -> Dict:
        """Get statistics from a practice database"""
        try:
            # Query the database
            results = self.notion.query_database(database_id)
            pages = results.get('results', [])
            
            stats = {
                'total_figures': len(pages),
                'figures_list': [],
                'last_updated': None
            }
            
            for page in pages:
                title = self._extract_title(page)
                created = page.get('created_time')
                
                stats['figures_list'].append({
                    'title': title,
                    'created': created,
                    'id': page.get('id')
                })
                
                # Track most recent update
                if created:
                    if not stats['last_updated'] or created > stats['last_updated']:
                        stats['last_updated'] = created
            
            return stats
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_title(self, page: Dict) -> str:
        """Extract title from page"""
        properties = page.get('properties', {})
        for prop_value in properties.values():
            if prop_value.get('type') == 'title':
                title_array = prop_value.get('title', [])
                if title_array:
                    return title_array[0].get('plain_text', 'Untitled')
        return 'Untitled'
