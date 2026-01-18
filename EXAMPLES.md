# ScreenSnap Examples

This document provides 10 working examples demonstrating ScreenSnap's capabilities.

---

## Example 1: Basic Screenshot

**Use case:** Quickly capture your current screen

```bash
screensnap
```

**Output:**
```
✅ Screenshot saved to: screenshot_20260118_123456.png
```

**Result:** Screenshot saved in current directory with timestamp.

---

## Example 2: Named Screenshot

**Use case:** Capture with a specific filename for easy identification

```bash
screensnap bug_report.png
```

**Output:**
```
✅ Screenshot saved to: C:\Users\logan\Desktop\bug_report.png
```

**Result:** Screenshot saved as `bug_report.png` in current directory.

---

## Example 3: Capture to Specific Directory

**Use case:** Organize screenshots in a dedicated folder

```bash
screensnap --output-dir ~/screenshots error_screen.png
```

**Output:**
```
✅ Screenshot saved to: C:\Users\logan\screenshots\error_screen.png
```

**Result:** Screenshot saved in `~/screenshots/` (creates directory if needed).

---

## Example 4: Capture as JPEG

**Use case:** Smaller file size for sharing or storage

```bash
screensnap --format jpg screenshot.jpg
```

**Output:**
```
✅ Screenshot saved to: screenshot.jpg
```

**Result:** Screenshot saved as JPEG (typically 50-70% smaller than PNG).

---

## Example 5: Capture Specific Window (Windows)

**Use case:** Capture only a specific application window

```bash
screensnap --window "Chrome" browser_screenshot.png
```

**Output:**
```
✅ Screenshot saved to: browser_screenshot.png
```

**Result:** Captures only the Chrome window, not the entire screen.

**Note:** Falls back to full screen if window not found.

---

## Example 6: Python API - Basic Usage

**Use case:** Integrate screenshot capture into Python scripts

```python
from screensnap import ScreenSnap

# Create instance
snap = ScreenSnap()

# Capture screenshot
filepath = snap.capture("automated_screenshot.png")

print(f"Screenshot saved to: {filepath}")
```

**Output:**
```
Screenshot saved to: automated_screenshot.png
```

**Use in:** Automated testing, error logging, monitoring scripts.

---

## Example 7: Python API - Automated Error Capture

**Use case:** Automatically capture screenshots when errors occur

```python
from screensnap import ScreenSnap
import sys

def main():
    snap = ScreenSnap(output_dir="error_screenshots")
    
    try:
        # Your code that might fail
        risky_operation()
    
    except Exception as e:
        # Capture screenshot on error
        error_file = f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = snap.capture(error_file)
        
        print(f"Error occurred! Screenshot saved: {filepath}")
        print(f"Error message: {e}")
        
        # Log error with screenshot reference
        with open("error_log.txt", "a") as f:
            f.write(f"{datetime.now()}: {e} - Screenshot: {filepath}\n")

if __name__ == "__main__":
    main()
```

**Use in:** Production error logging, debugging, user support.

---

## Example 8: Python API - Multi-Window Capture

**Use case:** Capture multiple application windows in sequence

```python
from screensnap import ScreenSnap
import time

snap = ScreenSnap(output_dir="window_captures")

windows_to_capture = ["Chrome", "Visual Studio Code", "PowerShell"]

for window in windows_to_capture:
    try:
        filename = f"{window.lower().replace(' ', '_')}.png"
        filepath = snap.capture_window(window, filename)
        print(f"✓ Captured {window}: {filepath.name}")
        time.sleep(1)  # Brief pause between captures
    except Exception as e:
        print(f"✗ Failed to capture {window}: {e}")
```

**Output:**
```
✓ Captured Chrome: chrome.png
✓ Captured Visual Studio Code: visual_studio_code.png
✓ Captured PowerShell: powershell.png
```

**Use in:** System documentation, workflow recording, multi-app monitoring.

---

## Example 9: Integration with Team Brain Workflow

**Use case:** Capture screenshot and notify team via SynapseLink

```python
from screensnap import ScreenSnap
from synapselink import quick_send
import sys

# Add paths
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ScreenSnap")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SynapseLink")

def report_issue_with_screenshot(issue_description):
    """Report an issue with visual evidence"""
    
    # Capture screenshot
    snap = ScreenSnap(output_dir="issue_reports")
    screenshot_file = f"issue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = snap.capture(screenshot_file)
    
    # Send to team
    message = f"""
    Issue Reported: {issue_description}
    
    Screenshot captured: {filepath.absolute()}
    
    Please review and advise.
    """
    
    quick_send(
        to="FORGE",
        subject="Issue Report with Screenshot",
        message_body=message,
        priority="HIGH",
        agent="ATLAS"
    )
    
    print(f"✅ Issue reported with screenshot: {filepath.name}")
    return filepath

# Usage
if __name__ == "__main__":
    report_issue_with_screenshot("UI rendering bug in BCH dashboard")
```

**Use in:** Bug reporting, team collaboration, issue tracking.

---

## Example 10: Batch Screenshot Capture

**Use case:** Capture multiple screenshots at intervals for monitoring

```python
from screensnap import ScreenSnap
import time
from datetime import datetime

def monitor_screen(duration_minutes=5, interval_seconds=30):
    """
    Capture screenshots at regular intervals
    
    Args:
        duration_minutes: How long to monitor (default: 5 minutes)
        interval_seconds: Time between captures (default: 30 seconds)
    """
    snap = ScreenSnap(output_dir="monitoring")
    
    end_time = time.time() + (duration_minutes * 60)
    capture_count = 0
    
    print(f"Starting screen monitoring for {duration_minutes} minutes...")
    print(f"Capturing every {interval_seconds} seconds")
    
    while time.time() < end_time:
        try:
            # Capture screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = snap.capture(f"monitor_{timestamp}.png")
            capture_count += 1
            
            print(f"[{capture_count}] Captured: {filepath.name}")
            
            # Wait for next interval
            time.sleep(interval_seconds)
        
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            break
        
        except Exception as e:
            print(f"Error during capture: {e}")
            time.sleep(interval_seconds)
    
    print(f"\nMonitoring complete! {capture_count} screenshots captured")
    print(f"Location: {snap.output_dir.absolute()}")

# Usage
if __name__ == "__main__":
    # Monitor for 5 minutes, capture every 30 seconds
    monitor_screen(duration_minutes=5, interval_seconds=30)
```

**Output:**
```
Starting screen monitoring for 5 minutes...
Capturing every 30 seconds
[1] Captured: monitor_20260118_120000.png
[2] Captured: monitor_20260118_120030.png
[3] Captured: monitor_20260118_120100.png
...
[10] Captured: monitor_20260118_120430.png

Monitoring complete! 10 screenshots captured
Location: C:\Users\logan\monitoring
```

**Use in:** System monitoring, performance testing, time-lapse documentation.

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `screensnap` | Basic capture with auto-name |
| `screensnap file.png` | Named capture |
| `screensnap --window "Title"` | Window capture (Windows) |
| `screensnap --output-dir ~/path` | Specify output directory |
| `screensnap --format jpg` | Change format |
| `screensnap --help` | Show help |
| `screensnap --version` | Show version |

---

## Tips & Tricks

1. **Organize screenshots:** Use `--output-dir` to keep screenshots organized by project or date
2. **Automate captures:** Integrate into error handlers, monitoring scripts, or test suites
3. **Share with team:** Combine with SynapseLink for instant team collaboration
4. **Batch processing:** Use Python API to capture multiple windows or screens
5. **File naming:** Use descriptive names like `bug_login_page.png` for easy identification
6. **Format choice:** Use PNG for quality (lossless), JPG for smaller files
7. **Timestamp naming:** Let auto-naming handle timestamps to avoid filename conflicts

---

## Need More Help?

- See [README.md](README.md) for installation and basic usage
- See [CHEAT_SHEET.txt](CHEAT_SHEET.txt) for quick command reference
- See [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) for BCH and agent integration
- Ask in Team Brain Synapse for support

---

**Happy Snapping! 📸**
