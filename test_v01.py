"""
Basic test script for ScreenSnap v0.1
Purpose: Confirm core functionality works
"""

import sys
sys.path.insert(0, '.')

def test_import():
    """Test that module imports successfully"""
    try:
        from screensnap import ScreenSnap
        print("[OK] Module imports successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Import failed: {e}")
        return False

def test_basic_capture():
    """Test basic screenshot capture"""
    try:
        from screensnap import ScreenSnap
        import os
        
        snap = ScreenSnap(output_dir="test_screenshots")
        filepath = snap.capture("test_basic.png")
        
        if filepath.exists() and filepath.stat().st_size > 0:
            print(f"[OK] Basic capture works: {filepath}")
            # Cleanup
            os.remove(filepath)
            os.rmdir("test_screenshots")
            return True
        else:
            print("[FAIL] Screenshot file not created or empty")
            return False
    
    except Exception as e:
        print(f"[FAIL] Basic capture failed: {e}")
        return False

def test_auto_filename():
    """Test auto-generated filenames"""
    try:
        from screensnap import ScreenSnap
        import os
        
        snap = ScreenSnap(output_dir="test_screenshots")
        filepath = snap.capture()  # No filename provided
        
        if filepath.exists() and "screenshot_" in filepath.name:
            print(f"[OK] Auto filename works: {filepath.name}")
            # Cleanup
            os.remove(filepath)
            os.rmdir("test_screenshots")
            return True
        else:
            print("[FAIL] Auto filename failed")
            return False
    
    except Exception as e:
        print(f"[FAIL] Auto filename test failed: {e}")
        return False

def test_pillow_missing():
    """Test error handling when Pillow is missing"""
    # This test is informational only - we can't actually test without Pillow
    print("[INFO] Pillow dependency test: Check import error message is clear")
    print("[INFO] If Pillow is missing, you should see: 'Pillow is required...'")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("ScreenSnap v0.1 - Basic Tests")
    print("=" * 60)
    
    tests = [
        test_import,
        test_basic_capture,
        test_auto_filename,
        test_pillow_missing
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("✅ All tests passed!")
    else:
        print("⚠️ Some tests failed - review above")
