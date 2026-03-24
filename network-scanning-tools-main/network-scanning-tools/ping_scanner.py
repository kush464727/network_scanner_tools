import subprocess
import platform
import re
import sys


def scan_host(host):
    os_type = platform.system().lower()
    param = '-n' if os_type == 'windows' else '-c'

    command = ['ping', param, '4', host]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        return parse_output(host, result.stdout, result.returncode)

    except subprocess.TimeoutExpired:
        return {"host": host, "status": "Timeout", "avg_time": "N/A"}
    except Exception as e:
        return {"host": host, "status": f"Error: {e}", "avg_time": "N/A"}


def parse_output(host, output, returncode):
    if returncode != 0:
        return {"host": host, "status": "Unreachable", "avg_time": "N/A"}

    # Extract average time
    match = re.search(r'Average = (\d+)ms', output) or re.search(r'avg = (\d+\.?\d*)', output)

    avg_time = match.group(1) + " ms" if match else "Unknown"

    return {"host": host, "status": "Reachable", "avg_time": avg_time}


def display_results(results):
    print("\n=== Ping Results ===")
    for r in results:
        print(f"{r['host']} --> {r['status']} | Avg Time: {r['avg_time']}")


def main():
    choice = input("Single host scan? (y/n): ").lower()
    results = []

    if choice == 'y':
        host = input("Enter host/IP: ")
        results.append(scan_host(host))
    else:
        base_ip = input("Enter base IP (e.g., 192.168.1): ")
        for i in range(1, 10):
            ip = f"{base_ip}.{i}"
            results.append(scan_host(ip))

    display_results(results)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit()