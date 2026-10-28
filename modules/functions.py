class GeneralFunctions:
    @staticmethod
    def print_error(error_message, optional_variable=""):
        print("\n***", error_message, optional_variable, "***\n")

    @staticmethod
    def calculate_percentages(current_connections, min_connections, max_connections):
        if max_connections == min_connections:
            return 0.0
        return (current_connections - min_connections) / (max_connections - min_connections) * 100

    @staticmethod
    def choose_color(current_connections, min_connections, max_connections):
        percentage = GeneralFunctions.calculate_percentages(
            current_connections, min_connections, max_connections
        )
        if percentage >= 90:
            return "69bc6e"
        if percentage >= 80:
            return "8cca8b"
        if percentage >= 70:
            return "9ed2a2"
        if percentage >= 60:
            return "cbe5c8"
        if percentage >= 50:
            return "e6f3e2"
        if percentage >= 40:
            return "e9f7ea"
        if percentage >= 30:
            return "f2f7f0"
        if percentage >= 20:
            return "f5fcf5"
        if percentage >= 10:
            return "f6fdf8"
        return "ffffff"
