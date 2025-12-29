# 💃 DanceSport Training Assistant: From Single Agent to Multi-Agent AI System
Building an Intelligent Personal Assistant for DanceSport Training Management
This project demonstrates the evolution from a single AI agent to a sophisticated multi-agent AI system that manages and analyzes a comprehensive DanceSport training program in Notion.

## 🎯 Phase 1: Single Agent Foundation
Starting with a single AI agent powered by Google's Gemini 2.5 Flash (the latest AI model), the system connects to Notion via API to retrieve, organize, and analyze training data across multiple dance styles (Cha Cha, Rumba, Swing, Bolero, and Mambo). The agent provides intelligent insights into training structure, progress patterns, and learning approaches.


## 🎯 Phase 2: Multi-Agent Architecture
The single agent is being extended into a multi-agent AI system with two key architectural patterns:

💬 1. Personal Assistant Agent

Acts as the orchestrator and user interface
Coordinates between specialized sub-agents
Provides conversational interaction
Manages context and workflow

💬 2. Parallel Agent Executor

Executes concurrent tasks simultaneously
Specialized agents working in parallel:

📊 Progress Tracker Agent: Monitors learning progress across all dance groups
🏃 Deep Dive Agent: Analyzes started items and their status
✍️ Comment Assistant Agent: Interactively manages training notes and feedback
📚 Completion Reporter Agent: Tracks and celebrates completed training milestones

This multi-agent approach enables efficient parallel processing, specialized expertise, and scalable task management.


## 🔮 Phase 3: Production Deployment (Future Plan)
The final phase transforms the notebook prototype into a production-ready personal assistant with:
User Interface Development

Web-based dashboard for real-time progress visualization
Interactive chat interface for natural language commands
Mobile-responsive design for on-the-go training management
Visual analytics and progress tracking charts

Production Infrastructure

Cloud deployment (AWS/GCP/Azure) for 24/7 availability
Secure API authentication and data encryption
Automated background tasks for progress monitoring
Real-time notifications for training milestones and reminders

Personal Assistant Capabilities

Voice-activated training updates and queries
Scheduled progress reports and insights
Intelligent recommendations based on training patterns
Integration with calendar for practice scheduling

The goal is to create a fully functional, always-accessible personal assistant that actively supports and enhances competitive DanceSport training through intelligent automation and insights.
Tech Stack: Python, Notion API, Google Gemini 2.5 Flash API, Kaggle Notebooks (Development) → Web Framework (React/Streamlit), Cloud Services, CI/CD Pipeline (Production)




# DanceSport-Training-Assistant
Multi-agent AI system for my personal DanceSport training assistant

# 💃 DanceSport AI Assistant

Multi-agent AI system for DanceSport coaching and progress tracking.

## 🎯 Current Version: Kaggle Notebook

The code in Kaggle notebook will demonstrate 5 features:
📊 Progress Analysis - AI analyzes your dance practice data
🏃 Practice Routine - Generates a 30-minute Cha Cha routine
✍️ AI Comments - Creates professional coaching feedback
💬 Q&A Coach - Answers DanceSport questions
📚 Dance Comparison - Compares Cha Cha vs Rumba

## 🚀 Quick Start

1. Open [Kaggle](https://www.kaggle.com) and create a new notebook
2. Follow the setup in `GETTING_STARTED_CHECKLIST.md`
3. Copy code from `dancesport_assistant_kaggle.py`
4. Run and enjoy!

## 📚 Documentation

- **Setup Guide**: [GETTING_STARTED_CHECKLIST.md](GETTING_STARTED_CHECKLIST.md)
- **Detailed Docs**: [KAGGLE_README.md](KAGGLE_README.md)
- **Comparison with v60**: [VERSION_COMPARISON.md](VERSION_COMPARISON.md)

## 🎓 Learning Project

This project teaches:
- Multi-agent AI architecture
- Notion API integration
- Google Gemini AI
- Object-oriented programming

## 🔮 Future Plans

- [ ] Web interface with Streamlit
- [ ] Additional coaching agents
- [ ] Video analysis integration
- [ ] Mobile app

## 📄 License

For educational purposes.

---

**Built with ❤️ for dancers who code**
```

---

## ⚠️ Important: What NOT to Upload

**Never upload** these to GitHub:
- ❌ Your API keys
- ❌ Your Notion token  
- ❌ Any secret credentials
- ❌ Personal practice data

**Instead**: Create a `.gitignore` file, and list what to ignore such:
.env
secrets.txt
*_secret*
config.py
```
