# ✅ Getting Started Checklist - Kaggle Version

Follow these steps to get your DanceSport Assistant running in 5 minutes!

---

## 🎯 Pre-Requirements

### ☐ Step 1: Get Your API Keys

**Notion Integration Token:**
1. [ ] Go to https://www.notion.so/my-integrations
2. [ ] Click "New integration"
3. [ ] Name it "DanceSport Assistant"
4. [ ] Copy the token (starts with "secret_")
5. [ ] Save it somewhere safe

**Google API Key:**
1. [ ] Go to https://aistudio.google.com/app/apikey
2. [ ] Click "Create API Key"
3. [ ] Copy the key
4. [ ] Save it somewhere safe

---

## 🚀 Kaggle Setup

### ☐ Step 2: Create Kaggle Notebook

1. [ ] Go to https://www.kaggle.com
2. [ ] Click "Code" → "New Notebook"
3. [ ] You should see an empty code cell

### ☐ Step 3: Add API Keys to Kaggle Secrets

**Add Notion Token:**
1. [ ] Click "Add-ons" (right sidebar)
2. [ ] Click "Secrets"
3. [ ] Click "+ Add a new secret"
4. [ ] Label: `NOTION_TOKEN`
5. [ ] Value: Paste your Notion token
6. [ ] Click "Add"

**Add Google API Key:**
1. [ ] Click "+ Add a new secret"
2. [ ] Label: `GOOGLE_API_KEY`
3. [ ] Value: Paste your Google key
4. [ ] Click "Add"

### ☐ Step 4: Copy the Code

1. [ ] Open the file `dancesport_assistant_kaggle.py`
2. [ ] Select ALL the code (Ctrl+A / Cmd+A)
3. [ ] Copy it (Ctrl+C / Cmd+C)
4. [ ] Go back to your Kaggle notebook
5. [ ] Click in the code cell
6. [ ] Paste the code (Ctrl+V / Cmd+V)

### ☐ Step 5: Run It!

1. [ ] Click "Run All" (or press Shift+Enter)
2. [ ] Wait 2-3 minutes for execution
3. [ ] Scroll through the output to see results!

---

## 📊 Notion Setup

### ☐ Step 6: Prepare Your Notion Workspace

**Create DanceSport Page:**
1. [ ] Open Notion
2. [ ] Create a new page
3. [ ] Title it "DanceSport"

**Add Dance Databases:**
1. [ ] In the DanceSport page, add a database
2. [ ] Name it "Fundamental Cha Cha" (or your dance)
3. [ ] Add a few pages (dance figures) inside

**Share with Integration:**
1. [ ] Click "Share" on the DanceSport page
2. [ ] Click "Invite"
3. [ ] Find "DanceSport Assistant" (your integration)
4. [ ] Click "Invite"

### ☐ Step 7: Re-run Notebook

1. [ ] Go back to Kaggle
2. [ ] Click "Run All" again
3. [ ] You should now see your DanceSport data!

---

## ✅ Verification Checklist

After running, you should see:

1. [ ] ✅ Packages installed successfully
2. [ ] ✅ Libraries imported successfully  
3. [ ] ✅ API keys configured
4. [ ] ✅ Notion client ready
5. [ ] ✅ Successfully connected to Notion
6. [ ] ✅ Found your DanceSport page
7. [ ] ✅ Progress analysis completed
8. [ ] ✅ Practice routine generated
9. [ ] ✅ AI comment created
10. [ ] ✅ Questions answered
11. [ ] ✅ Dance comparison completed

---

## 🐛 Troubleshooting

### Problem: "Secret not found"
- [ ] Check you named secrets exactly: `NOTION_TOKEN` and `GOOGLE_API_KEY`
- [ ] Make sure you clicked "Add" after entering each secret

### Problem: "No DanceSport content found"
- [ ] Verify you created a page titled "DanceSport" in Notion
- [ ] Check you shared the page with your integration
- [ ] Try searching for "dancesport" in the Notion app to find the page

### Problem: Code won't run
- [ ] Make sure you copied ALL the code
- [ ] Check for any error messages in red
- [ ] Try "Run All" again

### Problem: Integration not found when sharing
- [ ] Go back to https://www.notion.so/my-integrations
- [ ] Check if your integration was created
- [ ] Make sure it's in the same workspace

---

## 🎓 What to Do After Setup

### ☐ Learning Exercises (Choose One)

**Beginner:**
1. [ ] Change the dance being analyzed (line ~550)
2. [ ] Ask a different question (line ~650)
3. [ ] Generate a Rumba routine instead of Cha Cha (line ~600)

**Intermediate:**
1. [ ] Add a new dance to the knowledge base
2. [ ] Modify the AI prompts
3. [ ] Create a comment and post it to Notion

**Advanced:**
1. [ ] Create a new agent class
2. [ ] Add a completely new feature
3. [ ] Integrate with another API

---

## 📁 Files Reference

| File | Purpose | When to Read |
|------|---------|--------------|
| `dancesport_assistant_kaggle.py` | Main code | Copy this into Kaggle |
| `KAGGLE_README.md` | Detailed setup guide | If you get stuck |
| `VERSION_COMPARISON.md` | Comparison with v60 | To understand improvements |
| `QUICKSTART.md` | Quick reference | For fast lookup |
| `EXAMPLES.md` | Code examples | When customizing |

---

## 🎯 Success Criteria

You've successfully set up the system when:

✅ Notebook runs without errors
✅ You see your Notion workspace data
✅ AI analysis is generated
✅ All 5 demo features complete
✅ Summary shows your workspace stats

---

## 🆘 Still Stuck?

If you've checked all the boxes but something isn't working:

1. **Check the error message** - It usually tells you what's wrong
2. **Read KAGGLE_README.md** - More detailed troubleshooting
3. **Verify API keys** - Most common issue
4. **Check Notion sharing** - Second most common issue

---

## 🎉 You're Done!

Once everything works:
- [ ] Save your notebook ("Save Version")
- [ ] Try the learning exercises
- [ ] Start customizing!

**Congratulations!** 🎊 You now have a working multi-agent AI system!

---

**Next:** Open `KAGGLE_README.md` for customization ideas and learning exercises.

---

## 📝 Notes Section

Use this space to track what you've done:

```
Date: ___________
What I tried: 




What worked: 




What I learned: 




Next steps: 



```

---

**Happy Dancing & Coding! 💃🕺**
