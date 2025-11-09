import os

def update_screen(telemetry_data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
    _    _               ______       _   
    | |  | |              | ___ \     | |  
    | |  | | __ _ _ __ ___| |_/ / ___ | |_ 
    | |/\| |/ _` | '__/ _ \ ___ \/ _ \| __|
    \  /\  / (_| | | |  __/ |_/ / (_) | |_ 
    \/  \/ \__,_|_|  \___\____/ \___/ \__|                                       
        """)
    print("\n\n")
    print(f"INA219 Voltage: {telemetry_data['INA219_Voltage']} V\n")
    print(f"Compass Heading: {telemetry_data['Compass_Heading']}°")
