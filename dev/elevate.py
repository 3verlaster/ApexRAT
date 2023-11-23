import pyuac

def main():
    print("Do stuff here that requires being run as an admin.")
    # The window will disappear as soon as the program exits!
    input("Press enter to close the window. >")

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:        
        main()  # Already an admin here.