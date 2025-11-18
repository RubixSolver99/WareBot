import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def update_screen(telemetry_data):
    clear_screen()
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
    print(f"Compass Heading: {telemetry_data['Compass_Heading']}°\n")
    print(f"Wheel Left Angular Velocity: {telemetry_data['Wheel_Left_Ang_Vel']} rad/s\n")
    print(f"Wheel Right Angular Velocity: {telemetry_data['Wheel_Right_Ang_Vel']} rad/s\n")
    print(f"Chassis Linear Velocity: {telemetry_data['Chassis_Lin_Vel']} m/s\n")
    print(f"Chassis Angular Velocity: {telemetry_data['Chassis_Ang_Vel']} rad/s\n")