"""
Security test script for ScreenSnap v0.2
Purpose: Verify all v0.1 vulnerabilities are fixed
"""

import sys
sys.path.insert(0, '.')

def test_filename_validation():
    """Test that filename validation is working"""
    from screensnap import ScreenSnap
    import os
    
    snap = ScreenSnap(output_dir="test_screenshots")
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Path traversal in filename
    tests_total += 1
    try:
        filepath = snap.capture("../../../test.png")
        print("[FAIL] Path traversal still possible in filename")
    except ValueError as e:
        if "path components" in str(e).lower():
            print("[PASS] Path traversal blocked in filename")
            tests_passed += 1
        else:
            print(f"[FAIL] Wrong error for path traversal: {e}")
    
    # Test 2: Invalid characters in filename
    tests_total += 1
    try:
        filepath = snap.capture("test:file.png")
        print("[FAIL] Invalid characters accepted")
    except ValueError as e:
        if "invalid character" in str(e).lower():
            print("[PASS] Invalid characters rejected")
            tests_passed += 1
        else:
            print(f"[FAIL] Wrong error for invalid chars: {e}")
    
    # Test 3: Extremely long filename
    tests_total += 1
    try:
        filepath = snap.capture("A" * 300 + ".png")
        print("[FAIL] Long filename accepted")
    except ValueError as e:
        if "too long" in str(e).lower():
            print("[PASS] Long filename rejected")
            tests_passed += 1
        else:
            print(f"[FAIL] Wrong error for long filename: {e}")
    
    # Test 4: Valid filename works
    tests_total += 1
    try:
        filepath = snap.capture("valid_test.png")
        if filepath.exists():
            print("[PASS] Valid filename works")
            tests_passed += 1
            os.remove(filepath)
        else:
            print("[FAIL] Valid filename didn't create file")
    except Exception as e:
        print(f"[FAIL] Valid filename failed: {e}")
    
    # Cleanup
    try:
        os.rmdir("test_screenshots")
    except:
        pass
    
    return tests_passed, tests_total

def test_format_validation():
    """Test that format validation is working"""
    from screensnap import ScreenSnap
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Invalid format rejected
    tests_total += 1
    try:
        snap = ScreenSnap(format="invalid")
        print("[FAIL] Invalid format accepted")
    except ValueError as e:
        if "invalid format" in str(e).lower():
            print("[PASS] Invalid format rejected")
            tests_passed += 1
        else:
            print(f"[FAIL] Wrong error for invalid format: {e}")
    
    # Test 2: Valid formats accepted
    tests_total += 1
    try:
        snap1 = ScreenSnap(format="png")
        snap2 = ScreenSnap(format="jpg")
        snap3 = ScreenSnap(format="PNG")  # Case insensitive
        print("[PASS] Valid formats accepted")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] Valid formats failed: {e}")
    
    return tests_passed, tests_total

def test_empty_filename():
    """Test that empty filename generates auto-name"""
    from screensnap import ScreenSnap
    import os
    
    tests_passed = 0
    tests_total = 0
    
    tests_total += 1
    try:
        snap = ScreenSnap(output_dir="test_screenshots")
        filepath = snap.capture("")  # Empty string
        if filepath.exists() and "screenshot_" in filepath.name:
            print("[PASS] Empty filename handled (auto-generated)")
            tests_passed += 1
            os.remove(filepath)
        else:
            print("[FAIL] Empty filename didn't auto-generate")
    except Exception as e:
        print(f"[INFO] Empty filename behavior: {e}")
    
    # Cleanup
    try:
        os.rmdir("test_screenshots")
    except:
        pass
    
    return tests_passed, tests_total

def test_basic_functionality():
    """Test that basic functionality still works"""
    from screensnap import ScreenSnap
    import os
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Basic capture
    tests_total += 1
    try:
        snap = ScreenSnap(output_dir="test_screenshots")
        filepath = snap.capture("basic_v02.png")
        if filepath.exists() and filepath.stat().st_size > 0:
            print("[PASS] Basic capture still works")
            tests_passed += 1
            os.remove(filepath)
        else:
            print("[FAIL] Basic capture broken")
    except Exception as e:
        print(f"[FAIL] Basic capture error: {e}")
    
    # Test 2: Auto-naming
    tests_total += 1
    try:
        snap = ScreenSnap(output_dir="test_screenshots")
        filepath = snap.capture()
        if filepath.exists() and "screenshot_" in filepath.name:
            print("[PASS] Auto-naming still works")
            tests_passed += 1
            os.remove(filepath)
        else:
            print("[FAIL] Auto-naming broken")
    except Exception as e:
        print(f"[FAIL] Auto-naming error: {e}")
    
    # Cleanup
    try:
        os.rmdir("test_screenshots")
    except:
        pass
    
    return tests_passed, tests_total

if __name__ == "__main__":
    print("=" * 70)
    print("ScreenSnap v0.2 - Security & Validation Tests")
    print("=" * 70)
    print()
    
    all_passed = 0
    all_total = 0
    
    print("TEST GROUP 1: Filename Validation")
    print("-" * 70)
    passed, total = test_filename_validation()
    all_passed += passed
    all_total += total
    print(f"Results: {passed}/{total} passed")
    print()
    
    print("TEST GROUP 2: Format Validation")
    print("-" * 70)
    passed, total = test_format_validation()
    all_passed += passed
    all_total += total
    print(f"Results: {passed}/{total} passed")
    print()
    
    print("TEST GROUP 3: Empty Filename Handling")
    print("-" * 70)
    passed, total = test_empty_filename()
    all_passed += passed
    all_total += total
    print(f"Results: {passed}/{total} passed")
    print()
    
    print("TEST GROUP 4: Basic Functionality (Regression)")
    print("-" * 70)
    passed, total = test_basic_functionality()
    all_passed += passed
    all_total += total
    print(f"Results: {passed}/{total} passed")
    print()
    
    print("=" * 70)
    print(f"OVERALL: {all_passed}/{all_total} tests passed")
    print("=" * 70)
    
    if all_passed == all_total:
        print("SUCCESS! All vulnerabilities fixed, functionality preserved!")
    else:
        print("FAILURE: Some tests failed - review above")
    
    sys.exit(0 if all_passed == all_total else 1)
