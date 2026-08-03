import sys
import subprocess
import platform

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

    # Step 2: Prepare PyInstaller command
    app_name = "PDF Image Remover"
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", # Overwrite output directory without asking
        "--windowed",
        "--name", app_name,
    ]

    if os_name == "Windows":
        print("Applying Windows specific flags (--onefile)...")
        cmd.append("--onefile")

    # macOS specific requirements for PyMuPDF
    if os_name == "Darwin":
        print("Applying macOS specific flags...")
        # macOS users expect a .app bundle, which is created by --windowed.
        # --onefile is deprecated and breaks .app bundles on Mac.
        cmd.extend([
            "--hidden-import=fitz",
            "--hidden-import=pymupdf",
            "--collect-all", "fitz",
            "--collect-all", "pymupdf",
        ])
    
    cmd.append("main.py")

    # Step 3: Run Build
    print(f"Running PyInstaller: {' '.join(cmd)}")
    subprocess.check_call(cmd)

    print(f"\nBuild complete! You can find your application in the 'dist' folder.")

if __name__ == "__main__":
    main()
