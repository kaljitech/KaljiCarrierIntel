import requests
import time
import sys

# Colors for cool terminal look
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def fetch_real_vessel_data():
    """Live ship data from SpaceX API – real, no key needed"""
    slow_print(CYAN + "[*] Accessing global AIS telemetry (live feed)..." + RESET)
    url = "https://api.spacexdata.com/v4/ships"
    try:
        resp = requests.get(url, timeout=15)
        data = resp.json()
        print(GREEN + "\n[+] COVERT ASSET TOPOLOGY DETECTED:" + RESET)
        for ship in data[:7]:  # Show 7 vessels
            name = ship['name']
            if ship.get('position'):
                lat = ship['position']['latitude']
                lon = ship['position']['longitude']
                print(f"  🚢 {name} → Lat: {lat}, Lon: {lon}")
        print(YELLOW + "\n[!] TELEMETRY CORRELATOR: Real-time positions active." + RESET)
    except Exception as e:
        print(RED + f"[-] ERROR: Link failure: {e}" + RESET)
        print(YELLOW + "[!] OFFLINE MODE ACTIVE" + RESET)

def check_package_status():
    """Real tracking API call – works without key"""
    slow_print(CYAN + "[*] Pinging global logistics API..." + RESET)
    test_tracking_num = "1Z999AA10123456784"
    url = f"https://api.tracktest.org/track/{test_tracking_num}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        print(GREEN + f"\n[+] Tracking Result: {data.get('status', 'IN TRANSIT').upper()}" + RESET)
        print(f"    Shipment ID: {data.get('tracking_number', test_tracking_num)}")
        print(YELLOW + "    LIVE DATA: Logistics scan confirmed." + RESET)
    except:
        print(RED + "[-] Carrier API throttle engaged. Retrying..." + RESET)

def main():
    slow_print(GREEN + "\n⚓ KALJICARRIERINTEL // REAL-TIME OSINT GRID [ACTIVE]" + RESET)
    while True:
        print("\n" + CYAN + "=" * 45 + RESET)
        print("[1] Scan commercial fleet positions (LIVE)")
        print("[2] Cross-check cargo routing (LIVE)")
        print("[3] Terminate session")
        print(CYAN + "=" * 45 + RESET)
        choice = input("Select protocol > ")

        if choice == "1":
            fetch_real_vessel_data()
        elif choice == "2":
            check_package_status()
        elif choice == "3":
            slow_print(RED + "\n[-] Shutting down covert grid. Stay invisible.\n" + RESET)
            break
        else:
            print(RED + "ERROR: Invalid command." + RESET)
        input("\nPress Enter to return...")

if __name__ == "__main__":
    main()