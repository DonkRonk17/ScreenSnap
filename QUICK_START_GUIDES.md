# ScreenSnap Quick Start Guides

**Agent-specific guides for Team Brain members**

---

## For Forge (Orchestrator)

**Primary use cases:**
1. Documenting system architecture decisions
2. Capturing state during planning sessions
3. Visual evidence for team coordination

**Setup:**
```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ScreenSnap")
from screensnap import ScreenSnap
```

**Example workflow:**
```python
# Forge orchestrating with visual documentation
snap = ScreenSnap(output_dir="planning_docs")

# Capture current system state
system_state = snap.capture("system_architecture_current.png")

# Share with team via Synapse
from synapselink import quick_send
quick_send(
    "ALL",
    "Architecture Review",
    f"Current system state captured: {system_state}\nPlease review before integration.",
    priority="HIGH"
)
```

---

## For Atlas (Builder)

**Primary use cases:**
1. Capturing build errors for debugging
2. Documenting tool interfaces during development
3. Visual testing of UI components

**Setup:**
```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ScreenSnap")
from screensnap import ScreenSnap
```

**Example workflow:**
```python
# Atlas building and documenting
snap = ScreenSnap(output_dir="build_screenshots")

# Capture error when it occurs
try:
    build_project()
except Exception as e:
    error_screen = snap.capture(f"build_error_{datetime.now().strftime('%H%M%S')}.png")
    print(f"Build failed! Screenshot: {error_screen}")
    # Now can debug with visual evidence
```

---

## For CLIO (Tester)

**Primary use cases:**
1. Capturing test failures with visual evidence
2. Documenting bug reproduction steps
3. Creating visual test reports

**Setup:**
```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ScreenSnap")
from screensnap import ScreenSnap
```

**Example workflow:**
```python
# CLIO testing with visual verification
snap = ScreenSnap(output_dir="test_results")

def test_with_screenshot(test_name, test_func):
    """Run test and capture screenshot on failure"""
    try:
        test_func()
        print(f"✅ {test_name} PASSED")
    except AssertionError as e:
        # Capture failure state
        screenshot = snap.capture(f"test_fail_{test_name}.png")
        print(f"❌ {test_name} FAILED - Screenshot: {screenshot.name}")
        raise

# Usage
test_with_screenshot("login_ui", test_login_ui)
test_with_screenshot("dashboard", test_dashboard)
```

---

## For Nexus (Integrator)

**Primary use cases:**
1. Capturing integration states
2. Documenting configuration screens
3. Visual validation of integrations

**Setup:**
```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ScreenSnap")
from screensnap import ScreenSnap
```

**Example workflow:**
```python
# Nexus validating integrations
snap = ScreenSnap(output_dir="integration_validation")

# Capture before and after integration
before = snap.capture("before_integration.png")
print(f"Pre-integration state captured: {before.name}")

# Perform integration
integrate_tool()

# Capture after
after = snap.capture("after_integration.png")
print(f"Post-integration state captured: {after.name}")

# Compare visually
print("Compare screenshots to validate integration success")
```

---

## For Bolt (Executor)

**Primary use cases:**
1. Automated error capture in workflows
2. Task completion documentation
3. Monitoring task execution

**Setup:**
```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ScreenSnap")
from screensnap import ScreenSnap
```

**Example workflow:**
```python
# Bolt executing automated tasks
snap = ScreenSnap(output_dir="task_execution")

def execute_task_with_capture(task_name, task_func):
    """Execute task and capture result"""
    try:
        result = task_func()
        # Capture success state
        screenshot = snap.capture(f"task_{task_name}_success.png")
        print(f"✅ Task {task_name} complete: {screenshot.name}")
        return result
    except Exception as e:
        # Capture error state
        screenshot = snap.capture(f"task_{task_name}_error.png")
        print(f"❌ Task {task_name} failed: {screenshot.name}")
        raise

# Usage in automated workflow
execute_task_with_capture("data_sync", sync_data)
execute_task_with_capture("backup", create_backup)
```

---

## For Logan (Human User)

**Primary use cases:**
1. Troubleshooting with support team
2. Bug reporting
3. Documentation

**CLI Usage:**
```bash
# Basic capture
screensnap

# Named capture
screensnap bug_report.png

# Capture specific window
screensnap --window "Chrome" browser_issue.png

# Save to specific folder
screensnap --output-dir ~/bug_reports error.png
```

**When to use:**
- When Porter or any agent asks "what do you see?"
- When reporting a bug
- When following UI instructions and getting stuck
- When documenting anything visual

**Quick tip:** Make it a habit to capture screenshots BEFORE asking for help!

---

## Universal Tips for All Agents

**1. Organize by purpose:**
```python
# Different folders for different purposes
snap_bugs = ScreenSnap(output_dir="bug_reports")
snap_docs = ScreenSnap(output_dir="documentation")
snap_tests = ScreenSnap(output_dir="test_results")
```

**2. Use descriptive filenames:**
```python
# Good
snap.capture("login_page_broken_button.png")

# Bad
snap.capture("screenshot1.png")
```

**3. Combine with SynapseLink:**
```python
from synapselink import quick_send

screenshot = snap.capture("issue.png")
quick_send("TEAM", "Issue Found", f"See screenshot: {screenshot.absolute()}")
```

**4. Integrate into error handlers:**
```python
def safe_execute(func):
    try:
        return func()
    except Exception as e:
        snap = ScreenSnap(output_dir="errors")
        screenshot = snap.capture(f"error_{func.__name__}.png")
        print(f"Error captured: {screenshot}")
        raise
```

**5. Automate repetitive captures:**
```python
# Capture multiple states in sequence
states = ["login", "dashboard", "settings"]
for state in states:
    navigate_to(state)
    snap.capture(f"{state}_page.png")
    time.sleep(1)
```

---

## Common Patterns

**Pattern 1: Before/After Comparison**
```python
before = snap.capture("before.png")
make_changes()
after = snap.capture("after.png")
print(f"Compare {before} vs {after}")
```

**Pattern 2: Error Capture with Context**
```python
try:
    risky_operation()
except Exception as e:
    screenshot = snap.capture(f"error_{type(e).__name__}.png")
    log_error(str(e), screenshot_path=screenshot)
```

**Pattern 3: Progress Documentation**
```python
for step in project_steps:
    execute_step(step)
    snap.capture(f"progress_step_{step}.png")
```

---

## Troubleshooting

**Q: Screenshot not capturing correctly?**
A: Check you have a display available (SSH with X11 forwarding if remote)

**Q: File not found?**
A: Check output directory exists and you have write permissions

**Q: Window capture not working?**
A: Window capture only works on Windows. Linux/macOS fall back to full screen.

**Q: How do I capture remote screen?**
A: Use SSH with X11 forwarding: `ssh -X user@host`

---

## Next Steps

1. **Try it now:** Capture your first screenshot
2. **Integrate:** Add to your error handlers
3. **Share:** Use with SynapseLink for team coordination
4. **Automate:** Build it into your workflows
5. **Measure:** Track time saved!

---

**Remember:** One screenshot = 1000 words. Use liberally!

**Questions?** Ask in Synapse or check [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
