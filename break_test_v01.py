"""
Breaking test script for ScreenSnap v0.1
Purpose: Find ALL the ways this can fail
"""

import sys
sys.path.insert(0, '.')

def test_invalid_output_dir():
    """Test with invalid output directory"""
    try:
        from screensnap import ScreenSnap
        
        # Test 1: Path with invalid characters
        try:
            snap = ScreenSnap(output_dir="/invalid/path/that/cannot/exist")
            filepath = snap.capture("test.png")
            print("[WARN] Accepted invalid output dir - no validation?")
        except Exception as e:
            print(f"[OK] Rejected invalid output dir: {type(e).__name__}")
        
        # Test 2: Path traversal attempt
        try:
            snap = ScreenSnap(output_dir="../../../../../../../windows/system32")
            filepath = snap.capture("test.png")
            print("[CRITICAL] Path traversal possible!")
        except PermissionError:
            print("[OK] Path traversal blocked by OS permissions")
        except Exception as e:
            print(f"[OK] Path traversal blocked: {type(e).__name__}")
    
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")

def test_invalid_filenames():
    """Test with invalid or dangerous filenames"""
    try:
        from screensnap import ScreenSnap
        snap = ScreenSnap(output_dir="test_screenshots")
        
        # Test 1: Filename with path traversal
        try:
            filepath = snap.capture("../../../test.png")
            print("[WARN] Filename path traversal not validated")
            import os
            if filepath.exists():
                os.remove(filepath)
        except Exception as e:
            print(f"[OK] Path traversal in filename blocked: {type(e).__name__}")
        
        # Test 2: Filename with special characters
        try:
            filepath = snap.capture("test:file*.png")  # Invalid Windows filename
            print("[INFO] Special chars handled: {filepath}")
        except Exception as e:
            print(f"[OK] Special chars rejected: {type(e).__name__}")
        
        # Test 3: Empty filename
        try:
            filepath = snap.capture("")
            print(f"[OK] Empty filename handled (auto-generated): {filepath.name}")
            import os
            if filepath.exists():
                os.remove(filepath)
        except Exception as e:
            print(f"[INFO] Empty filename error: {e}")
        
        # Test 4: Very long filename (1000 chars)
        try:
            filepath = snap.capture("A" * 1000 + ".png")
            print("[WARN] Accepted 1000-char filename")
            import os
            if filepath.exists():
                os.remove(filepath)
        except Exception as e:
            print(f"[OK] Long filename rejected: {type(e).__name__}")
        
        # Cleanup
        import os
        try:
            os.rmdir("test_screenshots")
        except:
            pass
    
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")

def test_format_validation():
    """Test format parameter validation"""
    try:
        from screensnap import ScreenSnap
        
        # Test 1: Invalid format
        try:
            snap = ScreenSnap(format="invalid_format")
            filepath = snap.capture("test.png")
            print("[WARN] Accepted invalid format - no validation?")
            import os
            if filepath.exists():
                os.remove(filepath)
        except Exception as e:
            print(f"[OK] Invalid format rejected: {type(e).__name__}")
        
        # Test 2: Case sensitivity
        try:
            snap = ScreenSnap(format="PNG")
            filepath = snap.capture("test_caps.png")
            print("[OK] Uppercase format handled")
            import os
            if filepath.exists():
                os.remove(filepath)
        except Exception as e:
            print(f"[INFO] Case handling: {e}")
    
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")

def test_window_capture_edge_cases():
    """Test window capture with edge cases"""
    try:
        from screensnap import ScreenSnap
        snap = ScreenSnap(output_dir="test_screenshots")
        
        # Test 1: Non-existent window
        try:
            filepath = snap.capture_window("WindowThatDoesNotExist123456")
            print(f"[OK] Non-existent window handled (fallback): {filepath.name}")
            import os
            if filepath.exists():
                os.remove(filepath)
        except Exception as e:
            print(f"[INFO] Non-existent window error: {e}")
        
        # Test 2: Empty window title
        try:
            filepath = snap.capture_window("")
            print(f"[OK] Empty window title handled: {filepath.name}")
            import os
            if filepath.exists():
                os.remove(filepath)
        except Exception as e:
            print(f"[INFO] Empty window title error: {e}")
        
        # Cleanup
        import os
        try:
            os.rmdir("test_screenshots")
        except:
            pass
    
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")

def test_rapid_captures():
    """Test resource handling with rapid captures"""
    try:
        from screensnap import ScreenSnap
        import os
        
        snap = ScreenSnap(output_dir="test_screenshots")
        
        # Capture 10 screenshots rapidly
        files = []
        for i in range(10):
            try:
                filepath = snap.capture(f"rapid_{i}.png")
                files.append(filepath)
            except Exception as e:
                print(f"[FAIL] Rapid capture {i} failed: {e}")
                break
        
        if len(files) == 10:
            print(f"[OK] Handled 10 rapid captures successfully")
        else:
            print(f"[WARN] Only {len(files)}/10 rapid captures succeeded")
        
        # Cleanup
        for f in files:
            if f.exists():
                os.remove(f)
        try:
            os.rmdir("test_screenshots")
        except:
            pass
    
    except Exception as e:
        print(f"[FAIL] Rapid capture test failed: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("ScreenSnap v0.1 - BREAKING TESTS")
    print("=" * 60)
    print()
    
    print("TEST 1: Invalid Output Directories")
    print("-" * 60)
    test_invalid_output_dir()
    print()
    
    print("TEST 2: Invalid Filenames")
    print("-" * 60)
    test_invalid_filenames()
    print()
    
    print("TEST 3: Format Validation")
    print("-" * 60)
    test_format_validation()
    print()
    
    print("TEST 4: Window Capture Edge Cases")
    print("-" * 60)
    test_window_capture_edge_cases()
    print()
    
    print("TEST 5: Rapid Captures")
    print("-" * 60)
    test_rapid_captures()
    print()
    
    print("=" * 60)
    print("Review warnings and failures above!")
    print("=" * 60)
