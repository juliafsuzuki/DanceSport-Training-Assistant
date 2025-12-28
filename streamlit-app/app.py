"""
DanceSport Assistant - Streamlit UI
A multi-agent system for DanceSport coaching and progress tracking
"""

import streamlit as st
import google.generativeai as genai
from notion_client import NotionClient, WorkspaceAnalyzer
from agents import DanceSportAssistant, ProgressTracker
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="DanceSport Assistant",
    page_icon="💃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4ECDC4;
        margin-bottom: 2rem;
    }
    .dance-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'notion_client' not in st.session_state:
        st.session_state.notion_client = None
    if 'assistant' not in st.session_state:
        st.session_state.assistant = None
    if 'workspace_data' not in st.session_state:
        st.session_state.workspace_data = None
    if 'dancesport_content' not in st.session_state:
        st.session_state.dancesport_content = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'api_keys_set' not in st.session_state:
        st.session_state.api_keys_set = False


def setup_api_keys():
    """Setup API keys from user input"""
    st.sidebar.header("🔑 API Configuration")
    
    notion_token = st.sidebar.text_input(
        "Notion Integration Token",
        type="password",
        help="Get this from https://www.notion.so/my-integrations"
    )
    
    google_api_key = st.sidebar.text_input(
        "Google API Key",
        type="password",
        help="Get this from Google AI Studio"
    )
    
    if st.sidebar.button("Connect", type="primary"):
        if notion_token and google_api_key:
            try:
                # Configure Gemini
                genai.configure(api_key=google_api_key)
                
                # Initialize Notion client
                st.session_state.notion_client = NotionClient(notion_token)
                
                # Test connection
                info = st.session_state.notion_client.get_integration_info()
                
                # Initialize assistant
                st.session_state.assistant = DanceSportAssistant(st.session_state.notion_client)
                
                st.session_state.api_keys_set = True
                st.sidebar.success(f"✅ Connected as: {info.get('name', 'Unknown')}")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"❌ Connection failed: {str(e)}")
        else:
            st.sidebar.warning("Please enter both API keys")
    
    return st.session_state.api_keys_set


def load_workspace_data():
    """Load and analyze workspace data"""
    if st.session_state.workspace_data is None:
        with st.spinner("Loading workspace data..."):
            try:
                # Get all workspace objects
                results = st.session_state.notion_client.search_all()
                all_objects = results.get('results', [])
                
                # Build hierarchy
                analyzer = WorkspaceAnalyzer(st.session_state.notion_client)
                st.session_state.workspace_data = analyzer.build_hierarchy(all_objects)
                
                # Find DanceSport content
                st.session_state.dancesport_content = analyzer.find_dancesport_content(
                    st.session_state.workspace_data
                )
                
                return True
            except Exception as e:
                st.error(f"Error loading workspace: {str(e)}")
                return False
    return True


def main_interface():
    """Main application interface"""
    
    # Header
    st.markdown('<div class="main-header">💃 DanceSport Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your AI-Powered Dance Coach</div>', unsafe_allow_html=True)
    
    # Load workspace data
    if not load_workspace_data():
        st.warning("Unable to load workspace data. Please check your connection.")
        return
    
    # Sidebar - Dance Selection
    st.sidebar.header("🎵 Select Dance")
    
    dancesport_data = st.session_state.dancesport_content
    
    if not dancesport_data or not dancesport_data.get('dance_categories'):
        st.sidebar.warning("No DanceSport content found in your workspace")
        st.info("""
        **Setup Instructions:**
        1. Create a page in Notion titled "DanceSport"
        2. Add databases for different dance categories (e.g., "Fundamental Cha Cha", "Open Rumba")
        3. Add pages within those databases for individual figures
        4. Refresh this app to see your content
        """)
        return
    
    # Create dance selector
    dance_categories = dancesport_data['dance_categories']
    dance_options = [f"{cat['category']} - {cat['dance']}" for cat in dance_categories]
    
    selected_dance_idx = st.sidebar.selectbox(
        "Choose a dance category:",
        range(len(dance_options)),
        format_func=lambda i: dance_options[i]
    )
    
    selected_dance_data = dance_categories[selected_dance_idx]
    
    # Display selected dance info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Category:** {selected_dance_data['category']}")
    st.sidebar.markdown(f"**Dance:** {selected_dance_data['dance']}")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Progress Analysis",
        "🏃 Practice Routine",
        "💬 Chat with Coach",
        "✍️ Add Comment"
    ])
    
    # Tab 1: Progress Analysis
    with tab1:
        st.header("📊 Progress Analysis")
        
        if st.button("Analyze My Progress", type="primary"):
            with st.spinner("Analyzing your progress..."):
                try:
                    # Get database entries
                    tracker = ProgressTracker(st.session_state.notion_client)
                    database_id = selected_dance_data['database_id']
                    
                    results = st.session_state.notion_client.query_database(database_id)
                    pages = results.get('results', [])
                    
                    # Display stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Figures", len(pages))
                    with col2:
                        st.metric("Dance Type", selected_dance_data['dance'])
                    with col3:
                        st.metric("Category", selected_dance_data['category'])
                    
                    # Get AI analysis
                    analysis = st.session_state.assistant.analyze_progress(pages)
                    
                    st.markdown("### Coach's Analysis")
                    st.markdown(analysis)
                    
                    # Show figure list
                    if pages:
                        with st.expander("📋 View All Figures"):
                            for page in pages:
                                title = tracker._extract_title(page)
                                url = page.get('url', '#')
                                st.markdown(f"- [{title}]({url})")
                
                except Exception as e:
                    st.error(f"Error analyzing progress: {str(e)}")
    
    # Tab 2: Practice Routine
    with tab2:
        st.header("🏃 Practice Routine Generator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            skill_level = st.selectbox(
                "Skill Level",
                ["Beginner", "Intermediate", "Advanced"]
            )
        
        with col2:
            duration = st.selectbox(
                "Practice Duration",
                ["30 minutes", "45 minutes", "60 minutes"]
            )
        
        focus_areas = st.multiselect(
            "Focus Areas (optional)",
            ["Footwork", "Timing", "Hip Action", "Frame", "Connection", "Musicality"]
        )
        
        if st.button("Generate Practice Routine", type="primary"):
            with st.spinner("Creating your personalized routine..."):
                try:
                    routine = st.session_state.assistant.suggest_practice_routine(
                        dance_name=selected_dance_data['dance'],
                        skill_level=skill_level.lower(),
                        focus_areas=focus_areas if focus_areas else None
                    )
                    
                    st.markdown("### Your Practice Routine")
                    st.markdown(routine)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Routine",
                        data=routine,
                        file_name=f"{selected_dance_data['dance']}_routine_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                
                except Exception as e:
                    st.error(f"Error generating routine: {str(e)}")
    
    # Tab 3: Chat with Coach
    with tab3:
        st.header("💬 Chat with Your Coach")
        
        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask your coach anything about DanceSport..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("Coach is thinking..."):
                    try:
                        response = st.session_state.assistant.answer_question(
                            question=prompt,
                            dance_context=f"Current focus: {selected_dance_data['dance']}"
                        )
                        st.markdown(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"Sorry, I encountered an error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Tab 4: Add Comment
    with tab4:
        st.header("✍️ Add Practice Comment")
        
        st.markdown("""
        Add a comment to a specific figure in your Notion workspace. 
        The AI coach will help you create constructive feedback.
        """)
        
        # Get list of pages in current database
        try:
            database_id = selected_dance_data['database_id']
            results = st.session_state.notion_client.query_database(database_id)
            pages = results.get('results', [])
            
            tracker = ProgressTracker(st.session_state.notion_client)
            page_titles = {tracker._extract_title(page): page.get('id') for page in pages}
            
            selected_figure = st.selectbox(
                "Select Figure",
                list(page_titles.keys())
            )
            
            observation = st.text_area(
                "Your Practice Observation",
                placeholder="Example: Today I practiced the basic movement and noticed my timing was off on the 2nd and 4th beats...",
                height=100
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🤖 Generate Coach Comment", type="secondary"):
                    if observation:
                        with st.spinner("Generating comment..."):
                            try:
                                comment = st.session_state.assistant.create_practice_comment(
                                    dance_name=selected_dance_data['dance'],
                                    observation=observation
                                )
                                st.session_state.generated_comment = comment
                                st.markdown("**Generated Comment:**")
                                st.info(comment)
                            except Exception as e:
                                st.error(f"Error generating comment: {str(e)}")
                    else:
                        st.warning("Please enter your observation first")
            
            with col2:
                if st.button("💾 Post to Notion", type="primary"):
                    comment_text = st.session_state.get('generated_comment', observation)
                    if comment_text:
                        with st.spinner("Posting comment to Notion..."):
                            try:
                                page_id = page_titles[selected_figure]
                                result = st.session_state.notion_client.add_comment(
                                    page_id=page_id,
                                    comment_text=comment_text
                                )
                                st.success("✅ Comment posted successfully!")
                                st.balloons()
                            except Exception as e:
                                st.error(f"Error posting comment: {str(e)}")
                    else:
                        st.warning("Please generate or enter a comment first")
        
        except Exception as e:
            st.error(f"Error loading figures: {str(e)}")


def main():
    """Main application entry point"""
    init_session_state()
    
    # Check if API keys are set
    if not setup_api_keys():
        st.info("👈 Please enter your API keys in the sidebar to get started")
        
        # Show setup instructions
        with st.expander("📖 Setup Instructions"):
            st.markdown("""
            ### Getting Started
            
            **1. Notion Integration Token**
            - Go to https://www.notion.so/my-integrations
            - Click "New integration"
            - Give it a name (e.g., "DanceSport Assistant")
            - Copy the "Internal Integration Token"
            
            **2. Google API Key**
            - Go to https://aistudio.google.com/app/apikey
            - Create a new API key
            - Copy the key
            
            **3. Share Notion Pages**
            - Open your DanceSport page in Notion
            - Click "Share" → "Invite"
            - Select your integration
            
            **4. Enter Keys**
            - Paste both keys in the sidebar
            - Click "Connect"
            """)
        return
    
    # Show main interface
    main_interface()


if __name__ == "__main__":
    main()
