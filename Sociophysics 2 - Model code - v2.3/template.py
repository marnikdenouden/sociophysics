# Template for separate code files that have code that need to be run on start.
def setup():
    print("Always runs, when this code file is used")
    if __name__ == '__main__':
        print("Running only when this code file runs seperatly")
    else:
        print("Running only when this code is imported")
setup()