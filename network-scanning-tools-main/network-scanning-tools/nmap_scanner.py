import subprocess
import platform
import re
import sys


def check_nmap():
    try:
        subprocess.run(['nmap', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def run_scan(target, option):
    if option == '1':
        command = ['nmap', '-sn', target]
    elif option == '2':
        command = ['nmap', target]
    elif option == '3':
        ports = input("Enter port range (e.g., 20-100): ")
        command = ['nmap', '-p', ports, target]
    elif option == '4':
        command = ['nmap', '-sV', target]
    elif option == '5':
        command = ['nmap', '-O', target]
    else:
        print("Invalid option")
        return ""

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )

        return result.stdout

    except subprocess.TimeoutExpired:
        return "[!] Scan Timeout"
    except Exception as e:
        return f"[!] Error: {e}"


def parse_output(output):
    pattern = r'(\d+/tcp)\s+open\s+(\S+)'
    return re.findall(pattern, output)


def display_results(parsed, raw):
    print("\n=== Nmap Results ===")

    if not parsed:
        print("Raw Output:\n", raw)
        return

    print("PORT\tSERVICE")
    print("-" * 25)

    for port, service in parsed:
        print(f"{port}\t{service}")


def save_results(data):
    with open("nmap_results.txt", "w") as f:
        f.write(data)


def main():
    print("=== Nmap Scanner ===")

    if not check_nmap():
        print("[!] Nmap not installed")
        return

    target = input("Enter target IP/network: ")

    print("""
1. Host Discovery (-sn)
2. Default Port Scan
3. Custom Port Scan
4. Service Version Detection (-sV)
5. OS Detection (-O)
""")

    choice = input("Select option: ")

    output = run_scan(target, choice)
    parsed = parse_output(output)

    display_results(parsed, output)

    save = input("Save results? (y/n): ")
    if save.lower() == 'y':
        save_results(output)
        print("Saved to nmap_results.txt")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit()