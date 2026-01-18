# ScreenSnap Integration Plan

**Goal:** 100% Utilization & Compliance Across Team Brain  
**Target Date:** January 25, 2026 (1 week from deployment)  
**Owner:** Atlas (Builder)

---

## 🎯 INTEGRATION GOALS

| Goal | Target | Metric |
|------|--------|--------|
| BCH Integration | @mention support | Works in BCH chat |
| AI Agent Adoption | 100% (5/5 agents) | All agents can capture screenshots |
| Logan Direct Usage | Daily during troubleshooting | CLI usage confirmed |
| Porter Usage | Next troubleshooting session | Saves 2+ hours |
| Time Savings | 10+ hours/month | Documented usage logs |

---

## 📦 BCH INTEGRATION

### API Endpoints Needed

**Endpoint 1:** `/api/tools/screensnap/capture`
```python
# In app/routes/tools.py
from fastapi import APIRouter
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ScreenSnap")
from screensnap import ScreenSnap

@router.post("/screensnap/capture")
async def screensnap_capture(filename: str = None, output_dir: str = None):
    """Capture screenshot via BCH API"""
    try:
        snap = ScreenSnap(output_dir=output_dir or "screenshots")
        filepath = snap.capture(filename)
        return {
            "status": "success",
            "file": str(filepath.absolute()),
            "filename": filepath.name
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

**Endpoint 2:** `/api/tools/screensnap/capture_window`
```python
@router.post("/screensnap/capture_window")
async def screensnap_capture_window(window_title: str, filename: str = None):
    """Capture specific window via BCH API"""
    try:
        snap = ScreenSnap(output_dir="screenshots")
        filepath = snap.capture_window(window_title, filename)
        return {
            "status": "success",
            "file": str(filepath.absolute()),
            "filename": filepath.name
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### @mention Handler

**Pattern:** `@screensnap [filename]` or `@screensnap --window "Title"`

**Implementation:**
```python
# In app/services/mention_handler.py
async def handle_screensnap_mention(message: str) -> str:
    """Handle @screensnap mentions in BCH"""
    import re
    from screensnap import ScreenSnap
    
    # Parse command
    if "--window" in message:
        match = re.search(r'@screensnap\s+--window\s+"([^"]+)"(?:\s+(\S+))?', message)
        if match:
            window_title = match.group(1)
            filename = match.group(2)
            snap = ScreenSnap(output_dir="screenshots")
            filepath = snap.capture_window(window_title, filename)
            return f"✅ Window screenshot saved: {filepath.name}"
    else:
        match = re.search(r'@screensnap(?:\s+(\S+))?', message)
        filename = match.group(1) if match else None
        snap = ScreenSnap(output_dir="screenshots")
        filepath = snap.capture(filename)
        return f"✅ Screenshot saved: {filepath.name}"
```

### BCH UI Widget (Optional)

**Screenshot Button:**
```javascript
// In BCH frontend
async function captureScreenshot() {
    const response = await fetch('/api/tools/screensnap/capture', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    });
    
    const data = await response.json();
    if (data.status === 'success') {
        showNotification(`Screenshot saved: ${data.filename}`);
    }
}
```

---

## 🤖 AI AGENT INTEGRATION

### For ALL Agents (Forge, Atlas, CLIO, Nexus, Bolt)

**Step 1: Import**
```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ScreenSnap")
from screensnap import ScreenSnap
```

**Step 2: Usage Pattern**
```python
# When to use ScreenSnap:
# - During UI troubleshooting sessions
# - When user reports visual bugs
# - When providing step-by-step UI instructions
# - When documenting system states
# - When error screens need to be captured

# Example:
snap = ScreenSnap(output_dir="troubleshooting_screenshots")
filepath = snap.capture("issue_description.png")

# Then share via Synapse or with user
print(f"Screenshot captured: {filepath}")
```

**Step 3: Integration with Other Tools**

**With SynapseLink:**
```python
from screensnap import ScreenSnap
from synapselink import quick_send

snap = ScreenSnap(output_dir="shared_screenshots")
filepath = snap.capture("bug_report.png")

quick_send(
    "TEAM",
    "Bug Report - Visual Evidence",
    f"Screenshot attached: {filepath.absolute()}\nPlease review the UI issue.",
    priority="HIGH"
)
```

**With TokenTracker:**
```python
from screensnap import ScreenSnap
from tokentracker import TokenTracker

snap = ScreenSnap()
tracker = TokenTracker()

# Capture during troubleshooting
filepath = snap.capture("troubleshoot_session.png")

# Log the session
tracker.log_usage(
    "AGENT",
    "model",
    input_tokens,
    output_tokens,
    f"Troubleshooting session with screenshot: {filepath.name}"
)
```

---

## 📊 ADOPTION STRATEGY

### Week 1: Foundation
- **Day 1:** BCH endpoints created (Forge)
- **Day 2:** All agents add imports, test basic capture
- **Day 3:** Porter uses in next troubleshooting session
- **Day 4:** Logan uses when asking for help
- **Day 5:** Gather feedback, measure time saved

### Week 2: Full Integration
- **Day 1-2:** BCH @mention handler implemented
- **Day 3-4:** Agents integrate into workflows
- **Day 5:** Adoption measurement, celebrate wins

### Target Metrics (Week 2 end):
- ✅ 100% agent adoption (5/5)
- ✅ Logan using CLI regularly
- ✅ Porter saved 2+ hours in first use
- ✅ 10+ screenshots captured for troubleshooting
- ✅ 0 blocking bugs reported

---

## 📚 TRAINING MATERIALS

### Quick Start Guide (for agents)

```markdown
# ScreenSnap Quick Start

**What it does:** Captures screenshots instantly for troubleshooting

**When to use:**
- User reports UI bug → capture their screen
- Providing UI instructions → capture to show what you mean
- Documenting errors → capture error screens
- Troubleshooting sessions → visual feedback

**How to use:**

1. Import:
```python
from screensnap import ScreenSnap
snap = ScreenSnap()
```

2. Capture:
```python
filepath = snap.capture("issue_name.png")
```

3. Share:
```python
# Via Synapse
quick_send("USER", "Screenshot", f"See: {filepath}")

# Or just tell user
print(f"Screenshot saved: {filepath}")
```

**That's it!** 3 lines of code, massive time savings.
```

### Real-World Scenarios

**Scenario 1: Porter & Logan Troubleshooting**
```
BEFORE:
Porter: "Click the options menu in Android Studio"
Logan: "I don't see an options menu"
Porter: "It should be in the top right"
Logan: "Still don't see it"
[20 minutes of back-and-forth]

AFTER with ScreenSnap:
Porter: "Can you capture your Android Studio screen?"
Logan: screensnap android_studio.png
Logan: "Screenshot sent"
Porter: [Views screenshot] "Ah, you're on a different version. Click here instead."
[Issue resolved in 30 seconds]

TIME SAVED: 19.5 minutes
```

**Scenario 2: Bug Reporting**
```
BEFORE:
User: "The button is broken"
Agent: "Which button?"
User: "The blue one"
Agent: "Can you describe where it is?"
[10 minutes of description]

AFTER with ScreenSnap:
Agent: "Can you run: screensnap bug_screen.png"
User: [Sends screenshot]
Agent: [Sees exact issue] "Got it, I see the problem"
[Issue identified immediately]

TIME SAVED: 10 minutes
```

---

## 🔧 MAINTENANCE PLAN

### Weekly Health Check
- ✅ Verify all agents still have access
- ✅ Review usage logs (how many screenshots captured?)
- ✅ Check for any error reports
- ✅ Measure time saved

### Monthly Review
- 📊 Analyze usage patterns
- 💡 Identify new use cases
- 🐛 Address any issues
- 🎯 Plan v1.1 features

### Success Metrics Tracking
```python
# Track in TokenTracker or separate log
{
    "tool": "ScreenSnap",
    "month": "2026-01",
    "screenshots_captured": 50,
    "time_saved_hours": 15,
    "agents_using": 5,
    "satisfaction": 95
}
```

---

## ✅ SUCCESS CRITERIA

**Phase 1 (Week 1): Integration Complete**
- ✅ BCH endpoints live
- ✅ All agents can import and use
- ✅ Documentation complete
- ✅ Porter uses in session, confirms time saved

**Phase 2 (Week 2): Adoption Complete**
- ✅ 100% agent adoption (5/5)
- ✅ Daily usage confirmed
- ✅ 10+ troubleshooting screenshots captured
- ✅ Measurable time savings (10+ hours)

**Phase 3 (Month 1): Full Utilization**
- ✅ Integrated into standard troubleshooting workflow
- ✅ Part of every agent's toolkit
- ✅ ROI demonstrated (15-30x first month)
- ✅ Feature requests for v1.1

---

## 💰 ROI PROJECTION

**Investment:**
- Build time: 4 hours @ $30/hour = $120
- Maintenance: 1 hour/month @ $30/hour = $30/month

**Returns (Conservative):**
- 5 uses/week saving 10 min each = 50 min/week = 3.3 hours/month
- 3.3 hours @ $30/hour = $99/month

**First Month ROI:** ($99 - $30 - $120) = -$51 (breakeven by Month 2)
**Ongoing ROI:** $99/month - $30/month = $69/month profit
**Annual Value:** $828/year

**Reality Check:**
- Porter's first use alone could save 2+ hours = $60
- Tool pays for itself in first troubleshooting session! ✅

---

## 🚀 LAUNCH CHECKLIST

**Pre-Launch:**
- ✅ Tool tested and production ready
- ✅ Documentation complete
- ✅ Branding generated
- ✅ Integration plan created
- ✅ GitHub deployed

**Launch Day:**
- ✅ Announce via SynapseLink to ALL
- ✅ Send targeted messages to Porter, Forge
- ✅ Post in BCH (if available)
- ✅ Update PROJECT_MANIFEST

**Week 1:**
- 📝 Monitor first uses
- 🐛 Fix any issues immediately
- 📊 Track time savings
- 💬 Gather feedback

**Week 2:**
- 🎯 Push for 100% adoption
- 📈 Measure and report ROI
- 🎉 Celebrate wins

---

**Plan Author:** Atlas  
**Review:** Forge  
**Tracking:** See ADOPTION_TRACKING.md for live status  
**Questions:** Ask in Synapse!
