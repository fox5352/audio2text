import subprocess
import sys
import os
import platform

def get_platform_suffix():
    """Get platform-specific suffix for the executable name"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    else:
        return system

def build_executable(name_suffix=""):
    """Build the executable with optional name suffix"""
    base_name = "audio2text"
    
    # Add platform and optional suffix to name
    platform_suffix = get_platform_suffix()
    if name_suffix:
        exe_name = f"{base_name}-{platform_suffix}-{name_suffix}"
    else:
        exe_name = f"{base_name}-{platform_suffix}"
    
    # On Windows, PyInstaller automatically adds .exe
    cmd = ["pyinstaller", "--onefile", "main.py", "--name", exe_name]
    
    # Add platform-specific options
    if platform.system() == "Windows":
        # You can add Windows-specific options here
        pass
    elif platform.system() == "Linux":
        # You can add Linux-specific options here
        pass
    
    print(f"Building {exe_name} for {platform.system()}...")
    print(f"Command: {' '.join(cmd)}")
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # merge stderr into stdout
        text=True,
        bufsize=1
    )

    # Live print each line as it comes
    for line in process.stdout:
        print(line, end='')

    process.stdout.close()
    return_code = process.wait()

    print(f"\nReturn code: {return_code}")
    
    if return_code == 0:
        # List the built files
        dist_dir = "dist"
        if os.path.exists(dist_dir):
            print(f"\nBuilt files in {dist_dir}:")
            for file in os.listdir(dist_dir):
                file_path = os.path.join(dist_dir, file)
                size = os.path.getsize(file_path)
                print(f"  {file} ({size:,} bytes)")
    
    return return_code

if __name__ == "__main__":
    # Accept optional name suffix from command line
    name_suffix = sys.argv[1] if len(sys.argv) > 1 else ""
    
    exit_code = build_executable(name_suffix)
    sys.exit(exit_code)