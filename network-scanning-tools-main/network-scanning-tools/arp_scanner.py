import subprocess
import platform
import re
import sys


def scan_arp():
    os_type = platform.system().lower()
    command = ['arp', '-a'] if os_type == 'windows' else ['arp', '-n']

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        return parse_output(result.stdout)

    except subprocess.TimeoutExpired:
        print("[!] Timeout occurred")
        return []
    except Exception as e:
        print(f"[!] Error: {e}")
        return []


def parse_output(output):
    pattern = r'(\d+\.\d+\.\d+\.\d+)[^\n]*([a-fA-F0-9:-]{17})'
    matches = re.findall(pattern, output)

    results = []
    for ip, mac in matches:
        results.append({"ip": ip, "mac": mac})

    return results


def save_to_file(results):
    with open("arp_results.txt", "w") as f:
        for r in results:
            f.write(f"{r['ip']} - {r['mac']}\n")


def display_results(results):
    print("\n=== ARP Table ===")
    print("IP Address\t\tMAC Address")
    print("-" * 40)

    for r in results:
        print(f"{r['ip']}\t\t{r['mac']}")

    print(f"\nTotal Entries: {len(results)}")


def main():
    results = scan_arp()
    display_results(results)

    save = input("Save results to file? (y/n): ").lower()
    if save == 'y':
        save_to_file(results)
        print("Saved to arp_results.txt")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit()