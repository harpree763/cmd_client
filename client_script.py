#!/usr/bin/env python3
import os
import subprocess
import requests
import platform as pf

# --- COLORS ---
GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

# 🌐 SERVER URL
SERVER_URL = "https://cmd-server.onrender.com"

# 🧠 Detect OS (optional auto mode)
def detect_platform():
    if pf.system().lower() == "windows":
        return "cmd"
    return "kali"

def print_banner(selected_platform):
    print(f"""
{CYAN}{BOLD}┌──────────────────────────────────────────────────────────┐
│        {RESET}{RED}AI TERMINAL ({selected_platform.upper()}){RESET}{CYAN}{BOLD}                    │
│      {RESET}{BLUE}Cross-Platform Reasoning Engine v2.0{RESET}{CYAN}{BOLD}        │
└──────────────────────────────────────────────────────────┘{RESET}
""")

# 🔁 API CALL
def get_ai_response(prompt, platform):
    try:
        res = requests.post(
            SERVER_URL,
            json={
                "input": prompt,
                "platform": platform
            }
        )
        return res.json()
    except Exception as e:
        print(f"{RED}[!] Server Error: {e}{RESET}")
        return None

def execute_command(command):
    print(f"{YELLOW}[*] Running: {BOLD}{command}{RESET}\n")

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            print(line, end="")

        process.wait()

        if process.returncode == 0:
            print(f"\n{GREEN}[+] Success{RESET}")
        else:
            print(f"\n{RED}[!] Failed (Exit Code: {process.returncode}){RESET}")

    except Exception as e:
        print(f"{RED}[!] Execution error: {e}{RESET}")

# 🎯 Platform selector
def choose_platform():
    print(f"{CYAN}Select Platform:{RESET}")
    print("1. Kali Linux")
    print("2. Windows CMD")
    print("3. Auto Detect")

    choice = input(f"{BOLD}> {RESET}").strip()

    if choice == "2":
        return "cmd"
    elif choice == "3":
        return detect_platform()
    else:
        return "kali"

def clear_screen(platform):
    if platform == "cmd":
        os.system("cls")
    else:
        os.system("clear")

def main():
    selected_platform = choose_platform()
    clear_screen(selected_platform)
    print_banner(selected_platform)

    while True:
        try:
            # 🖥️ Prompt style
            if selected_platform == "cmd":
                user_input = input(f"{GREEN}C:\\AI-Terminal>{RESET} ").strip()
            else:
                print(f"{GREEN}┌──({BOLD}root㉿kali{RESET}{GREEN})-[{CYAN}~{GREEN}]")
                user_input = input(f"└─{BOLD}${RESET} ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "clear"]:
                if user_input.lower() == "clear":
                    clear_screen(selected_platform)
                    print_banner(selected_platform)
                    continue
                break

            print(f"{BLUE}[~] Thinking...{RESET}")

            result = get_ai_response(user_input, selected_platform)

            print("DEBUG:", result)

            if not result:
                print(f"{RED}[!] No response from server{RESET}")
                continue

            command = result.get("command")
            explanation = result.get("explanation")
            is_dangerous = result.get("is_dangerous", False)

            if explanation:
                print(f"{CYAN}[i] {explanation}{RESET}")

            if is_dangerous:
                confirm = input(f"{RED}[!] Dangerous command. Continue? (y/n): {RESET}")
                if confirm.lower() != "y":
                    print(f"{YELLOW}[!] Skipped{RESET}")
                    continue

            if not command:
                print(f"{RED}[!] No command received{RESET}")
                continue

            execute_command(command)
            print("")

        except KeyboardInterrupt:
            print(f"\n{YELLOW}[!] Use 'exit' to quit{RESET}")
        except Exception as e:
            print(f"{RED}[!] Error: {e}{RESET}")

    print(f"{CYAN}Session ended{RESET}")

if __name__ == "__main__":
    main()
