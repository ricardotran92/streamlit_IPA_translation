## Requirements
- Python >= 3.12

## Installation
1. Install uv
- Thay đổi Execution Policy để PowerShell không chặn chạy script
	* RemoteSigned: Cho phép chạy script từ máy tính cục bộ, nhưng chặn script tải từ Internet trừ khi có chữ ký đáng tin cậy.
	* Scope CurrentUser: Chỉ thay đổi chính sách cho user hiện tại (không ảnh hưởng đến toàn bộ hệ thống).
	* Force: Bỏ qua cảnh báo yêu cầu xác nhận.
```cmd
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```
Cài uv
```cmd
iwr -Uri https://astral.sh/uv/install.ps1 -UseBasicParsing | iex
hoặc
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -Command "& { iwr -Uri https://astral.sh/uv/install.ps1 -UseBasicParsing | iex }"
```
Install uv with python 3.12
```cmd
uv venv --python 3.12
```

2. Install the package in editable mode with all development dependencies
```cmd
uv pip install -e ".[dev]"
```
3. Set up environment. Copy the example environment file
```cmd
cp .env.example .env
```
4. Activate Virtual Machine
```cmd
source .venv/Scripts/activate
```
5. Check PIP (Preferred Installer Program). Directory should be belong to venv
```
which pip
```
5. Install PIP (Preferred Installer Program) for venv
```
python -m ensurepip --default-pip
python -m pip --version
```
- Check again
```cmd
Ricardo@RICARDO-MSI MINGW64 /d/repos/<repo_name> (main)
$ python --version
Python 3.12.9
Ricardo@RICARDO-MSI MINGW64 /d/repos/<repo_name> (main)
$ pip --version
pip 24.0 from D:\repos\<repo_name>\.venv\Lib\site-packages\pip (python 3.12)
Ricardo@RICARDO-MSI MINGW64 /d/repos/<repo_name> (main)
$ which python
/d/repos/<repo_name>/.venv/Scripts/python
Ricardo@RICARDO-MSI MINGW64 /d/repos/<repo_name> (main)
$ which pip
/d/repos/<repo_name>/.venv/Scripts/pip
```


