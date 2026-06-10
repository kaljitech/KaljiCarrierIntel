import os
import time
import sys
import json

try:
    import requests
except ImportError:
    print("Installing required 'requests' library...")
    os.system("pip install requests")
    import requests

def clear_screen():
    os.system('clear')

def menu():
    print("\033[92m⚓ KALJICARRIERINTEL // REAL-TIME OSINT GRID [ACTIVE]\033[0m\n")
    print("==================================================")
    print("[1] Scan commercial fleet positions (LIVE)")
    print("[2] Cross-check cargo routing (LIVE)")
    print("[3] Terminate session")
    print("==================================================")

def scan_fleet():
    print("\033[96m[*] Accessing global AIS telemetry (live feed)...\033[0m")
    time.sleep(1.5)
    
    # CHANGE THIS URL BELOW TO YOUR ACTUAL LIVE API ENDPOINT LATER IF YOU HAVE ONE!
    url = "https://api.vesseltracker.com/v1/live" 
    
    try:
        # 1. Tries to connect to the web address with a 5-second limit
        response = requests.get(url, timeout=5)
        
        # 2. Checks if the website returned a broken error page (like a 404 or 500 error)
        response.raise_for_status()
        
        # 3. Tries to read the JSON safely
        data = response.json()
        print("\033[92m[+] Data successfully fetched!\033[0m")
        print(json.dumps(data, indent=2))
        
    except requests.exceptions.HTTPError as http_err:
        print(f"\033[91m[-] HTTP error occurred: {http_err}\033[0m")
        print("\033[93m[!] OFFLINE MODE ACTIVE\033[0m")
        
    except json.JSONDecodeError:
        print("\033[91m[-] ERROR: The server did not send back valid JSON data.\033[0m")
        print("\033[93m[!] OFFLINE MODE ACTIVE\033[0m")
        
    except Exception as e:
        print(f"\033[91m[-] Connection error: {e}\033[0m")
        print("\033[93m[!] OFFLINE MODE ACTIVE\033[0m")

def cross_check():
    print("\033[96m[*] Pinging global logistics API...\033[0m")
    time.sleep(1.5)
    print("\033[91m[-] API error - but service is still simulated.\033[0m")

def main():
    while True:
        clear_screen()
        menu()
        choice = input("Select protocol > ")
        
        if choice == '1':
            scan_fleet()
        elif choice == '2':
            cross_check()
        elif choice == '3':
            print("\033[91m[-] Terminating session...\033[0m")
            sys.exit()
        else:
            print("Invalid choice. Try again.")
            
        input("\nPress Enter to return...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[91mKeyboardInterrupt\033[0m")
        input("\nPress Enter to return...")