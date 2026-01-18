"""
ScreenSnap - Simple cross-platform screenshot tool for troubleshooting

Capture screenshots quickly and easily during troubleshooting sessions.
Supports full screen capture and window-specific capture (Windows).

Author: Atlas (Team Brain)
Created: 2026-01-18
Version: 1.0.0
License: MIT
Purpose: Save time during UI troubleshooting by enabling quick visual feedback
"""

import os
import sys
import platform
from pathlib import Path
from datetime import datetime
from typing import Optional
import json

VERSION = "1.0.0"
DEFAULT_CONFIG_PATH = Path.home() / ".screensnaprc"

# ============== CONFIGURATION ==============

class ScreenSnapConfig:
    """Configuration management for ScreenSnap"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from file"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._default_config()
        return self._default_config()
    
    def _default_config(self) -> dict:
        """Return default configuration"""
        return {
            "version": VERSION,
            "output_dir": ".",
            "format": "png",
            "include_timestamp": True
        }
    
    def save(self):
        """Save current configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)


# ============== MAIN CLASS ==============

class ScreenSnap:
    """Main screenshot capture class"""
    
    def __init__(self, output_dir: Optional[str] = None, 
                 format: str = "png",
                 config_path: Optional[Path] = None):
        """
        Initialize ScreenSnap
        
        Args:
            output_dir: Directory to save screenshots (default: current dir)
            format: Image format (default: png)
            config_path: Path to config file (default: ~/.screensnaprc)
        
        Raises:
            ValueError: If format is invalid
            ImportError: If Pillow is not installed
        """
        self.config_manager = ScreenSnapConfig(config_path)
        self.output_dir = Path(output_dir or self.config_manager.config['output_dir'])
        
        # Validate format
        valid_formats = ['png', 'jpg', 'jpeg']
        format_lower = format.lower()
        if format_lower not in valid_formats:
            raise ValueError(
                f"Invalid format '{format}'. Must be one of: {', '.join(valid_formats)}"
            )
        self.format = format_lower
        
        self.system = platform.system()
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Import PIL
        try:
            from PIL import ImageGrab
            self.ImageGrab = ImageGrab
        except ImportError:
            raise ImportError(
                "Pillow is required for ScreenSnap. Install it with: pip install pillow"
            )
    
    def _validate_filename(self, filename: str) -> str:
        """
        Validate and sanitize filename
        
        Args:
            filename: User-provided filename
        
        Returns:
            Sanitized filename (basename only, no path components)
        
        Raises:
            ValueError: If filename is invalid
        """
        if not filename:
            return filename
        
        # Get basename only (prevent path traversal)
        from os.path import basename
        clean_filename = basename(filename)
        
        # Check if path traversal was attempted
        if clean_filename != filename:
            raise ValueError(
                f"Invalid filename (path components not allowed): {filename}"
            )
        
        # Check length (most filesystems have 255 char limit)
        if len(clean_filename) > 255:
            raise ValueError(
                f"Filename too long ({len(clean_filename)} chars). Max: 255"
            )
        
        # Windows invalid characters: < > : " / \ | ? *
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            if char in clean_filename:
                raise ValueError(
                    f"Invalid character in filename: '{char}'"
                )
        
        return clean_filename
    
    def _generate_filename(self, custom_name: Optional[str] = None) -> Path:
        """
        Generate filename for screenshot
        
        Args:
            custom_name: Custom filename (optional)
        
        Returns:
            Full path to screenshot file
        
        Raises:
            ValueError: If custom_name is invalid
        """
        if custom_name:
            # Validate custom name
            filename = self._validate_filename(custom_name)
            if not filename.endswith(f'.{self.format}'):
                filename += f'.{self.format}'
        else:
            # Generate timestamp-based name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.{self.format}"
        
        return self.output_dir / filename
    
    def capture(self, filename: Optional[str] = None) -> Path:
        """
        Capture full screen screenshot
        
        Args:
            filename: Output filename (optional, auto-generates if not provided)
        
        Returns:
            Path to saved screenshot
        
        Raises:
            ValueError: If filename is invalid
            RuntimeError: If screenshot capture fails
        """
        try:
            # Generate filepath (validation happens here)
            filepath = self._generate_filename(filename)
            
            # Capture screenshot
            screenshot = self.ImageGrab.grab()
            
            # Save screenshot
            screenshot.save(filepath, self.format.upper())
            
            return filepath
        
        except ValueError:
            # Re-raise validation errors as-is
            raise
        
        except Exception as e:
            raise RuntimeError(f"Failed to capture screenshot: {e}")
    
    def capture_window(self, window_title: str, filename: Optional[str] = None) -> Path:
        """
        Capture specific window (Windows only for now)
        
        Args:
            window_title: Title of window to capture (substring match)
            filename: Output filename (optional)
        
        Returns:
            Path to saved screenshot
        
        Raises:
            NotImplementedError: If not on Windows
            ValueError: If window not found
        """
        if self.system != "Windows":
            # Fallback to full screen on non-Windows
            print(f"Warning: Window capture not supported on {self.system}, capturing full screen")
            return self.capture(filename)
        
        # Windows-specific window capture
        try:
            import win32gui
            import win32ui
            import win32con
            from ctypes import windll
            from PIL import Image
            
            # Find window by title
            hwnd = self._find_window(window_title)
            if not hwnd:
                print(f"Warning: Window '{window_title}' not found, capturing full screen")
                return self.capture(filename)
            
            # Get window dimensions
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top
            
            # Capture window
            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            saveDC.SelectObject(saveBitMap)
            
            # Copy window contents
            result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
            
            # Convert to PIL Image
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            screenshot = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )
            
            # Cleanup
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)
            
            # Save screenshot
            filepath = self._generate_filename(filename)
            screenshot.save(filepath, self.format.upper())
            
            return filepath
        
        except ImportError:
            # pywin32 not installed, fallback to full screen
            print("Warning: pywin32 not installed, capturing full screen instead")
            return self.capture(filename)
        
        except Exception as e:
            raise RuntimeError(f"Failed to capture window: {e}")
    
    def _find_window(self, title_substring: str) -> Optional[int]:
        """
        Find window handle by title substring (Windows only)
        
        Args:
            title_substring: Substring to search for in window titles
        
        Returns:
            Window handle (HWND) or None if not found
        """
        try:
            import win32gui
            
            def callback(hwnd, results):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if title_substring.lower() in window_title.lower():
                        results.append(hwnd)
            
            results = []
            win32gui.EnumWindows(callback, results)
            
            return results[0] if results else None
        
        except ImportError:
            return None


# ============== CLI INTERFACE ==============

def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ScreenSnap - Simple cross-platform screenshot tool",
        epilog="Examples:\n"
               "  screensnap                    # Capture full screen with timestamp\n"
               "  screensnap myscreen.png        # Capture to specific file\n"
               "  screensnap --window Chrome     # Capture Chrome window (Windows only)\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "filename",
        nargs="?",
        help="Output filename (optional, auto-generates if not provided)"
    )
    
    parser.add_argument(
        "--window", "-w",
        metavar="TITLE",
        help="Capture specific window by title substring (Windows only)"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        metavar="DIR",
        help="Output directory (default: current directory)"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["png", "jpg", "jpeg"],
        default="png",
        help="Image format (default: png)"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"ScreenSnap {VERSION}"
    )
    
    args = parser.parse_args()
    
    # Create ScreenSnap instance
    try:
        snap = ScreenSnap(
            output_dir=args.output_dir,
            format=args.format
        )
        
        # Capture screenshot
        if args.window:
            filepath = snap.capture_window(args.window, args.filename)
        else:
            filepath = snap.capture(args.filename)
        
        # Success message
        print(f"✅ Screenshot saved to: {filepath.absolute()}")
        return 0
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
