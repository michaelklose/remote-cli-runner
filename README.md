# remote-cli-runner

**remote-cli-runner (rcr)** is a lightweight, cross-platform SSH-based tool that lets you run common network and diagnostic commands (e.g., `ping`, `nslookup`, or arbitrary shell commands) **on a remote host**, while using a simple local CLI.

It works on:

- **Linux**
- **Windows** (PowerShell / CMD)
- **macOS** (optional)

`rcr` is a single CLI entrypoint:

```bash
rcr ping ...
rcr nslookup ...
rcr <any-command> ...
```

---

## 📁 Configuration (`~/.remote-cli-runner.ini`)

Before using `rcr`, create a configuration file in your home directory.

### Linux / macOS

```text
~/.remote-cli-runner.ini
```

### Windows

```text
C:\Users\<YourUser>\.remote-cli-runner.ini
```

### Configuration example (Linux/macOS)

```ini
[remote]
host = your.server.com
user = yourusername
key  = /home/yourusername/.ssh/id_ed25519
port = 22
```

### Configuration example (Windows)

```ini
[remote]
host = server.example.com
user = michael
key  = C:\Users\michael\.ssh\rcr
port = 22
```

`key` must point to a valid **SSH private key**.

---

## 🚀 Commands

### 🔹 Ping (executed on remote host)

#### Linux / macOS remote host

```bash
rcr ping 8.8.8.8 -c 4
```

#### Windows remote host

```powershell
rcr ping 8.8.8.8 -n 4
```

---

### 🔹 nslookup (remote)

```bash
rcr nslookup example.com
```

---

### 🔹 Generic remote commands

Any command that is **not** `ping` or `nslookup` is treated as a generic remote command.

```bash
rcr uname -a
rcr whoami
rcr ls -la /var/log
rcr systemctl status ssh
```

This allows you to use `rcr` as a simple SSH-based remote command runner.

---

## 🧩 Installation / Usage

Clone the repository:

```bash
git clone https://github.com/<yourname>/remote-cli-runner
cd remote-cli-runner
```

### Running directly with Python

#### Linux / macOS

```bash
python3 rcr.py ping 8.8.8.8 -c 4
```

#### Windows

```powershell
python rcr.py ping 1.1.1.1 -n 4
```

You can also make the script executable and put it in your PATH as `rcr`.

---

## 📦 Building native binaries (Linux & Windows)

`rcr` can be compiled into standalone executables using **PyInstaller**, so Python is not required on the target machine.

Install PyInstaller:

```bash
pip install pyinstaller
```

### Build a standalone binary on Linux

```bash
pyinstaller --onefile rcr.py
```

Output:

```text
dist/rcr
```

### Build a standalone binary on Windows

```powershell
pyinstaller --onefile rcr.py
```

Output:

```text
dist\rcr.exe
```

Copy the resulting binary to a directory in your `PATH` for global usage.

---

## 💡 Future improvements

- Support for multiple remote profiles (`--profile prod`)
- Automatic Windows remote host detection for ping options (`-c` vs `-n`)
- Verbose / debug mode
- Parallel execution on multiple hosts
- Additional built-in helpers (traceroute, dig, netstat, etc.)

---

## 📝 Summary

**remote-cli-runner** provides:

- A simple, unified CLI (`rcr`) for running commands on a remote machine  
- A clean `.ini` config file in the user home directory  
- Cross-platform support (Linux, Windows, macOS)  
- Optional standalone binaries via PyInstaller  

A minimal tool with maximal usefulness — ideal for network diagnostics, server access, and automation.
