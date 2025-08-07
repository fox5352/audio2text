import subprocess

if __name__ == "__main__":
    cmd = ["pyinstaller", "--onefile", "main.py"]

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
