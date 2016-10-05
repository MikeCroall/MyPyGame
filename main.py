def main():
    try:
        import pygame
    except ImportError as ex:
        print("Please install pygame - it is a required module!")
        return
    print("Excellent - pygame is installed and imported!")


main()
print("See you again soon!")