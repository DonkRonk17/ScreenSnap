# ScreenSnap Integration Examples

**Code examples for integrating ScreenSnap with Team Brain tools and workflows**

---

## Integration 1: TokenTracker

**Purpose:** Track token usage AND time saved by using screenshots

```python
from screensnap import ScreenSnap
from tokentracker import TokenTracker
import time

def troubleshoot_with_tracking(issue_description):
    """Troubleshoot with visual feedback and track efficiency"""
    
    tracker = TokenTracker()
    snap = ScreenSnap(output_dir="troubleshooting")
    
    start_time = time.time()
    
    # Capture screenshot for troubleshooting
    screenshot = snap.capture(f"issue_{issue_description}.png")
    
    # Estimate time saved (vs 20-minute verbal description)
    time_saved_minutes = 19.5  # Conservative estimate
    
    # Log the session with time savings
    tracker.log_usage(
        agent="ATLAS",
        model="sonnet-4.5",
        input_tokens=100,
        output_tokens=50,
        task=f"Troubleshooting with ScreenSnap: {screenshot.name} (saved {time_saved_minutes} min)"
    )
    
    print(f"✅ Screenshot captured: {screenshot}")
    print(f"⏱️ Estimated time saved: {time_saved_minutes} minutes")
    
    return screenshot

# Usage
troubleshoot_with_tracking("ui_button_not_responding")
```

---

## Integration 2: SynapseLink

**Purpose:** Share screenshots instantly with team via Synapse

```python
from screensnap import ScreenSnap
from synapselink import quick_send
import sys

sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ScreenSnap")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SynapseLink")

def report_visual_issue(issue_title, issue_description, recipients="TEAM"):
    """Report an issue with visual evidence"""
    
    # Capture screenshot
    snap = ScreenSnap(output_dir="issue_reports")
    screenshot = snap.capture(f"issue_{issue_title.replace(' ', '_')}.png")
    
    # Compose message
    message = f"""
Visual Issue Report: {issue_title}

Description: {issue_description}

Screenshot: {screenshot.absolute()}

Please review and advise on next steps.
    """
    
    # Send via Synapse
    quick_send(
        to=recipients,
        subject=f"Visual Issue: {issue_title}",
        message_body=message,
        priority="HIGH",
        agent="ATLAS"
    )
    
    print(f"✅ Issue reported with screenshot to {recipients}")
    return screenshot

# Usage
report_visual_issue(
    "Login Button Broken",
    "The login button appears grayed out and unclickable",
    recipients="FORGE,CLIO"
)
```

---

## Integration 3: ContextCompressor

**Purpose:** Compress screenshot analysis context to save tokens

```python
from screensnap import ScreenSnap
from contextcompressor import ContextCompressor

def analyze_screenshot_efficiently(screenshot_path, analysis_query):
    """Analyze screenshot with compressed context"""
    
    # This is a conceptual example - ContextCompressor works with text
    # For actual screenshot analysis, you'd extract text/OCR first
    
    compressor = ContextCompressor()
    
    # Example: If you have text description of the screenshot
    screenshot_description = f"""
    Screenshot analysis for: {screenshot_path}
    
    [Long description of what's in the screenshot...]
    [UI elements, colors, layout, etc...]
    [Hundreds of lines of detailed description...]
    """
    
    # Compress the description before sending to AI for analysis
    compressed = compressor.compress_text(
        screenshot_description,
        query=analysis_query,
        method="relevant"
    )
    
    print(f"Token savings: {compressed.estimated_token_savings}")
    print(f"Compressed content ready for AI analysis")
    
    return compressed

# Usage
analyze_screenshot_efficiently(
    "bug_report.png",
    "What UI elements are causing the error?"
)
```

---

## Integration 4: BCH Backend

**Purpose:** Make ScreenSnap available via BCH API

```python
# File: app/routes/tools.py (in BCH backend)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ScreenSnap")
from screensnap import ScreenSnap

router = APIRouter(prefix="/api/tools", tags=["tools"])

class ScreenshotRequest(BaseModel):
    filename: str = None
    output_dir: str = "screenshots"
    window_title: str = None

@router.post("/screensnap/capture")
async def capture_screenshot(request: ScreenshotRequest):
    """Capture screenshot via BCH API"""
    try:
        snap = ScreenSnap(output_dir=request.output_dir)
        
        if request.window_title:
            filepath = snap.capture_window(request.window_title, request.filename)
        else:
            filepath = snap.capture(request.filename)
        
        return {
            "status": "success",
            "filepath": str(filepath.absolute()),
            "filename": filepath.name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/screensnap/status")
async def screensnap_status():
    """Check if ScreenSnap is available"""
    try:
        from screensnap import ScreenSnap, VERSION
        return {
            "available": True,
            "version": VERSION
        }
    except ImportError:
        return {
            "available": False,
            "error": "ScreenSnap not installed"
        }
```

**Frontend Usage:**
```javascript
// In BCH frontend
async function captureScreenshot(filename = null) {
    const response = await fetch('/api/tools/screensnap/capture', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename })
    });
    
    const data = await response.json();
    if (data.status === 'success') {
        alert(`Screenshot saved: ${data.filename}`);
    }
}
```

---

## Integration 5: Automated Workflow

**Purpose:** Use ScreenSnap in automated agent workflows

```python
from screensnap import ScreenSnap
from synapselink import quick_send
from tokentracker import TokenTracker
import time

class AutomatedTroubleshooter:
    """Automated troubleshooting with visual feedback"""
    
    def __init__(self, agent_name="BOLT"):
        self.snap = ScreenSnap(output_dir="automated_troubleshooting")
        self.tracker = TokenTracker()
        self.agent_name = agent_name
    
    def troubleshoot_task(self, task_name, task_func):
        """Execute task and capture visual state on error"""
        
        start_time = time.time()
        
        try:
            # Execute task
            result = task_func()
            
            # Capture success state
            screenshot = self.snap.capture(f"{task_name}_success.png")
            
            # Log success
            self.tracker.log_usage(
                self.agent_name,
                "model",
                50,
                25,
                f"Task {task_name} succeeded - screenshot: {screenshot.name}"
            )
            
            return result
        
        except Exception as e:
            # Capture error state
            screenshot = self.snap.capture(f"{task_name}_error.png")
            
            # Report error with visual evidence
            quick_send(
                "FORGE",
                f"Task Failed: {task_name}",
                f"Task {task_name} failed with error: {e}\n\n"
                f"Screenshot captured: {screenshot.absolute()}\n\n"
                f"Please review.",
                priority="HIGH",
                agent=self.agent_name
            )
            
            # Log error
            self.tracker.log_usage(
                self.agent_name,
                "model",
                50,
                25,
                f"Task {task_name} failed - screenshot: {screenshot.name}"
            )
            
            raise

# Usage
troubleshooter = AutomatedTroubleshooter("BOLT")

def risky_task():
    # Some task that might fail
    import random
    if random.random() < 0.3:
        raise Exception("Random failure for demonstration")
    return "Success!"

# Run with automated visual feedback
troubleshooter.troubleshoot_task("data_processing", risky_task)
```

---

## Integration 6: Test Automation

**Purpose:** Visual verification in automated testing

```python
from screensnap import ScreenSnap
import unittest

class VisualTestCase(unittest.TestCase):
    """Test case with visual evidence capture"""
    
    def setUp(self):
        self.snap = ScreenSnap(output_dir="test_screenshots")
    
    def test_with_screenshot(self, test_name):
        """Decorator to capture screenshot on test failure"""
        def decorator(test_func):
            def wrapper(*args, **kwargs):
                try:
                    return test_func(*args, **kwargs)
                except AssertionError as e:
                    # Capture failure state
                    screenshot = self.snap.capture(f"test_fail_{test_name}.png")
                    print(f"\n❌ Test {test_name} failed - Screenshot: {screenshot}")
                    raise
            return wrapper
        return decorator
    
    @test_with_screenshot("login_ui")
    def test_login_ui(self):
        """Test login UI"""
        # Navigate to login page
        # Check UI elements
        self.assertTrue(check_login_button_visible())
        # If assertion fails, screenshot is captured automatically

# Usage
suite = unittest.TestLoader().loadTestsFromTestCase(VisualTestCase)
unittest.TextTestRunner().run(suite)
```

---

## Integration 7: Error Logging System

**Purpose:** Automatic screenshot capture in error logging

```python
from screensnap import ScreenSnap
import logging
import traceback
from datetime import datetime

class VisualErrorLogger:
    """Error logger with automatic screenshot capture"""
    
    def __init__(self, log_file="error_log.txt"):
        self.snap = ScreenSnap(output_dir="error_screenshots")
        self.log_file = log_file
        
        # Setup logging
        logging.basicConfig(
            filename=log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def log_error_with_screenshot(self, error, context=""):
        """Log error and capture screenshot"""
        
        # Capture screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot = self.snap.capture(f"error_{timestamp}.png")
        
        # Log error with screenshot reference
        error_msg = f"""
Error: {str(error)}
Context: {context}
Screenshot: {screenshot.absolute()}
Traceback:
{traceback.format_exc()}
        """
        
        logging.error(error_msg)
        
        return screenshot

# Usage as context manager
logger = VisualErrorLogger()

try:
    # Risky operation
    complex_operation()
except Exception as e:
    screenshot = logger.log_error_with_screenshot(e, "During complex_operation")
    print(f"Error logged with screenshot: {screenshot}")
```

---

## Integration 8: Documentation Generator

**Purpose:** Auto-generate visual documentation

```python
from screensnap import ScreenSnap
import time

class VisualDocGenerator:
    """Generate visual documentation automatically"""
    
    def __init__(self, output_dir="docs/screenshots"):
        self.snap = ScreenSnap(output_dir=output_dir)
        self.documentation = []
    
    def document_step(self, step_name, description, window=None):
        """Document a step with screenshot"""
        
        # Capture screenshot
        if window:
            screenshot = self.snap.capture_window(window, f"step_{step_name}.png")
        else:
            screenshot = self.snap.capture(f"step_{step_name}.png")
        
        # Add to documentation
        self.documentation.append({
            "step": step_name,
            "description": description,
            "screenshot": screenshot.name
        })
        
        print(f"📸 Documented: {step_name}")
        time.sleep(0.5)  # Brief pause for UI to stabilize
    
    def generate_markdown(self, title="Visual Guide"):
        """Generate markdown documentation"""
        
        md = f"# {title}\n\n"
        
        for i, doc in enumerate(self.documentation, 1):
            md += f"## Step {i}: {doc['step']}\n\n"
            md += f"{doc['description']}\n\n"
            md += f"![{doc['step']}]({doc['screenshot']})\n\n"
            md += "---\n\n"
        
        return md

# Usage
doc_gen = VisualDocGenerator()

# Document a process
doc_gen.document_step(
    "open_settings",
    "Open the Settings window by clicking the gear icon",
    window="Settings"
)

doc_gen.document_step(
    "navigate_security",
    "Navigate to the Security tab",
    window="Settings"
)

# Generate documentation
markdown = doc_gen.generate_markdown("Security Configuration Guide")
with open("security_guide.md", "w") as f:
    f.write(markdown)
```

---

## Quick Integration Checklist

**For any agent integrating ScreenSnap:**

1. ✅ Add import path
2. ✅ Create ScreenSnap instance
3. ✅ Use in error handlers
4. ✅ Integrate with SynapseLink (optional)
5. ✅ Track usage with TokenTracker (optional)
6. ✅ Document visual workflows

**Minimal integration (3 lines):**
```python
from screensnap import ScreenSnap
snap = ScreenSnap()
screenshot = snap.capture("issue.png")
```

**Full integration (with team coordination):**
```python
from screensnap import ScreenSnap
from synapselink import quick_send
from tokentracker import TokenTracker

snap = ScreenSnap()
tracker = TokenTracker()

screenshot = snap.capture("issue.png")
tracker.log_usage("AGENT", "model", 100, 50, f"Screenshot: {screenshot.name}")
quick_send("TEAM", "Issue Found", f"Screenshot: {screenshot.absolute()}")
```

---

## Need Help?

- See [CHEAT_SHEET.txt](CHEAT_SHEET.txt) for quick reference
- See [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md) for agent-specific guides
- See [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) for full integration strategy
- Ask in Synapse for support

---

**Remember:** The best integration is the one you actually use! Start simple, expand as needed.
