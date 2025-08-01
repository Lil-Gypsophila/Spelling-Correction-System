"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
Date Created: 24/12/2024
Date Modified: 30/12/2024

Main module to run the application

"""

from GUI import SpellCheckerGUI


if __name__ == "__main__":
    
    try:

        app = SpellCheckerGUI()
        app.mainloop()
    
    except Exception as e:

        print(f"Error starting the application: {e}")