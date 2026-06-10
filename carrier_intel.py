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
    print("[1] Scan commercial fleet positions (LIVE REAL DATA)")
    print("[2] Cross-check cargo routing (LIVE)")
    print("[3] Terminate session")
    print("==================================================")

def scan_fleet():
    print("\033[96m[*] Querying open-source AIS telemetry API (Baltic Sea Feed)...\033[0m")
    time.sleep(1.0)
    
    # FIXED: The correct live server endpoint
    url = "https://meri.digitraffic.fi/api/ais/v1/locations"
    headers = {
        "User-Agent": "KaljiCarrierIntel/1.0 (Open-Source OSINT Tool)"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        raw_data = response.json()
        real_ships = []
        
        # Parse the live GeoJSON data structure safely
        if isinstance(raw_data, dict) and "features" in raw_data:
            vessels = raw_data.get("features", [])
            for v in vessels[:4]:  # Extract the top 4 live ships moving right now
                props = v.get("properties", {})
                geom = v.get("geometry", {})
                coords = geom.get("coordinates", [0, 0])
                
                real_ships.append({
                    "vessel_mmsi": props.get("mmsi"),
                    "lat": coords[1] if len(coords) > 1 else 0,
                    "lon": coords[0] if len(coords) > 0 else 0,
                    "speed_knots": props.get("sog"),
                    "heading_deg": props.get("cog"),
                    "nav_status": props.get("navStatus")
                })
        elif isinstance(raw_data, list):
            for v in raw_data[:4]:
                real_ships.append({
                    "vessel_mmsi": v.get("mmsi"),
                    "lat": v.get("latitude"),
                    "lon": v.get("longitude"),
                    "speed_knots": v.get("speedOverGround"),
                    "heading_deg": v.get("courseOverGround")
                })
                
        if not real_ships:
            print("\033[91m[-] No active vessel telemetry streams found at this timestamp.\033[0m")
            return
            
        print("\033[92m[+] LIVE TELEMETRY STREAM ONLINE. PARSING REAL DATA...\033[0m\n")
        time.sleep(0.5)
        
        output = {
            "status": "SUCCESS",
            "source": "Fintraffic Marine Open Data Grid",
            "live_tracking_nodes": real_ships
        }
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(f"\033[91m[-] API Error: Could not fetch grid coordinates. Reason: {e}\033[0m")

def cross_check():
    print("\033[96m[*] Pinging open marine data nodes...\033[0m")
    time.sleep(1.0)
    print("\033[93m[!] Operational Notice: Cargo manifests require private commercial tokens.\033[0m")
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