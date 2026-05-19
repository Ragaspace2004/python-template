def calculate(x, y):
    """This function has several problems"""
    if x is None:
        return "error"

    result = x + y * 2
    print("Result is: " + str(result))

    # Unused variable
    # unused_var = 42

    # Old style dict creation
    # data = dict(name="John", age=30)

    # Redundant code
    # if len(data) > 0:
    #     pass

    return result


# Global variable used without declaration
counter = 0


# def increment():
#     counter += 1  # UnboundLocalError style issue
#     return counter


class User:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello {self.name}")


# Bad practices
user = User("Alice")
user.greet()

# Unused import

# Syntax / style issues
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
very_long_line = "This is a very long string that should probably be broken into multiple lines because it exceeds the maximum line length most teams use"
