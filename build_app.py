import sys
import subprocess
import platform
import shutil
import os

def run_pyinstaller(args: list):
    """Helper to run PyInstaller with specific arguments."""
    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--windowed"] + args + ["main.py"]
    print(f"Running PyInstaller: {' '.join(cmd)}")
    subprocess.check_call(cmd)

def main():
    """
    Cross-platform build script for PyInstaller.
    Handles specific flags required for macOS and Windows.
    """
    os_name = platform.system()
    print(f"Starting build process for {os_name}...")

    # Step 1: Install dependencies
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Step 2: Build Application
    app_name = "PDF Image Remover"

    if os_name == "Windows":
        # 1. Build Standard Directory Version
        print("\nBuilding Windows Directory version (Standard)...")
        run_pyinstaller(["--name", app_name])
        
        print("Zipping Directory version...")
        shutil.make_archive(f"dist/{app_name}-Windows-Standard", 'zip', "dist", app_name)
        
        # 2. Build Portable OneFile Version
        print("\nBuilding Windows OneFile version (Portable)...")
        run_pyinstaller(["--onefile", "--name", f"{app_name} Portable"])

    else:
        # Build for macOS / Linux
        args = ["--name", app_name]
        
        if os_name == "Darwin":
            print("\nApplying macOS specific flags...")
            args.extend([
                "--hidden-import=fitz",
                "--hidden-import=pymupdf",
                "--collect-all", "fitz",
                "--collect-all", "pymupdf",
            ])
            
        run_pyinstaller(args)
        
        if os_name == "Darwin":
            print("Zipping macOS .app bundle (using native ditto to preserve symlinks)...")
            zip_cmd = [
                "ditto", "-c", "-k", "--sequesterRsrc", "--keepParent",
                f"dist/{app_name}.app", f"dist/{app_name}-macOS.zip"
            ]
            subprocess.check_call(zip_cmd)

    print(f"\nBuild complete! You can find your application in the 'dist' folder.")

if __name__ == "__main__":
    main()
