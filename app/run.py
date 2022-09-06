from .application import Controller
import time

def main():
    
    __session = Controller()

    while (True):
        if not  __session.process():
            time.sleep(10)
       


if __name__ == "__main__":
    main()