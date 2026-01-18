def get_controller_command():
    print("\nController options:")
    print("1 - START mission")
    print("2 - PAUSE")
    print("3 - ABORT")
    print("4 - EXIT")

    choice = input("Enter command number: ").strip()

    if choice == "1":
        return "START"
    elif choice == "2":
        return "PAUSE"
    elif choice == "3":
        return "ABORT"
    elif choice == "4":
        return "EXIT"
    else:
        print("Invalid command")
        return None
