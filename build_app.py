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
        
        # Add Instructions.txt for Windows
        with open(f"dist/{app_name}/HOW_TO_RUN_Instructions.txt", "w", encoding="utf-8") as f:
            f.write("=== HOW TO RUN THE APP ===\n\n")
            f.write("Because this is a free open-source app, Windows Defender SmartScreen might block it.\n")
            f.write("To run it:\n")
            f.write("1. Double-click the app.\n")
            f.write("2. If a blue screen appears saying 'Windows protected your PC', click 'More info'.\n")
            f.write("3. Click 'Run anyway'.\n")
        
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
            print("Zipping macOS .app bundle and instructions...")
            # Create a folder to hold the app and instructions
            release_dir = f"dist/{app_name}_macOS_Release"
            os.makedirs(release_dir, exist_ok=True)
            
            # Move the .app into the release folder
            shutil.move(f"dist/{app_name}.app", f"{release_dir}/{app_name}.app")
            
            # Add Instructions.txt for macOS
            with open(f"{release_dir}/HOW_TO_RUN_Instructions.txt", "w", encoding="utf-8") as f:
                f.write("=== HOW TO RUN THE APP ===\n\n")
                f.write("Because this is a free open-source app, macOS Gatekeeper might block it.\n")
                f.write("To run it:\n")
                f.write("1. DO NOT double-click the app immediately.\n")
                f.write("2. RIGHT-CLICK (or Control-click) the app icon and select 'Open'.\n")
                f.write("3. You will see a warning. Click the new 'Open' button that appears.\n\n")
                f.write("Alternatively, open Terminal and run:\n")
                f.write(f"xattr -cr /path/to/PDF\\ Image\\ Remover.app\n")
                f.write("(Tip: You can type 'xattr -cr ' and just drag and drop the app into the terminal!)\n")
            
            # Zip the folder using ditto
            zip_cmd = [
                "ditto", "-c", "-k", "--keepParent",
                release_dir, f"dist/{app_name}-macOS.zip"
            ]
            subprocess.check_call(zip_cmd)

    print(f"\nBuild complete! You can find your application in the 'dist' folder.")

if __name__ == "__main__":
    main()
