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
    print("[1] Scan commercial fleet positions (LIVE REAL-WORLD DATA)")
    print("[2] Cross-check cargo routing (LIVE)")
    print("[3] Terminate session")
    print("==================================================")

def scan_fleet():
    print("\033[96m[*] Querying open-source AIS telemetry API (Baltic Sea Feed)...\033[0m")
    time.sleep(1.0)
    
    # This is a REAL, live public vessel tracking API endpoint
    url = "https://vessel.digitraffic.fi/api/v1/vessels"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # The API sends back data in GeoJSON format
        raw_data = response.json()
        vessels = raw_data.get("features", [])
        
        if not vessels:
            print("\033[91m[-] No vessels found in the live stream right now.\033[0m")
            return
            
        print("\033[92m[+] LIVE TELEMETRY STREAM ONLINE. PARSING REAL DATA...\033[0m\n")
        time.sleep(0.5)
        
        # Let's extract the top 4 actual live ships currently moving in the water
        real_ships = []
        for v in vessels[:4]:
            properties = v.get("properties", {})
            geometry = v.get("geometry", {})
            coordinates = geometry.get("coordinates", [0, 0])
            
            ship_info = {
                "vessel_mmsi": properties.get("mmsi"),
                "vessel_name": properties.get("name", "UNKNOWN CLASS"),
                "lat": coordinates[1],
                "lon": coordinates[0],
                "speed_knots": properties.get("sog"),  # Speed Over Ground
                "heading_deg": properties.get("cog"),  # Course Over Ground
                "timestamp_epoch": properties.get("timestamp")
            }
            real_ships.append(ship_info)
            
        # Output the actual, real live JSON feed
        output = {
            "status": "SUCCESS",
            "source": "Digitraffic Marine API",
            "total_active_tracked": len(vessels),
            "sample_fleet": real_ships
        }
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(f"\033[91m[-] API Error: Could not reach live server. Reason: {e}\033[0m")

def cross_check():
    print("\033[96m[*] Pinging open marine data nodes...\033[0m")
    time.sleep(1.0)
    print("\033[93m[!] Operational Notice: Cargo routing requires private carrier API keys.\033[0m")
    print("\033[91m[-] Service offline.\033[0m")

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
            
        input("\n\033[93mPress Enter to return...\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[91mKeyboardInterrupt\033[0m")
        sys.exit()