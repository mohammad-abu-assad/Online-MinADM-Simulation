import os


class ExperimentCounter:
    """Manages the experiment counter for tracking the number of experiments, implemented as a Singleton."""

    def __init__(self, counter_file):
        self.counter_file = counter_file
        os.makedirs(os.path.dirname(self.counter_file), exist_ok=True)

    def get_counter(self):
        """Retrieves the current experiment counter."""
        try:
            if os.path.exists(self.counter_file):
                with open(self.counter_file, 'r') as file:
                    return int(file.read().strip())
            else:
                return 0
        except (IOError, ValueError) as e:
            print(f"Error reading counter file: {e}")
            return 0

    def set_counter(self, counter):
        """Updates the experiment counter."""
        try:
            with open(self.counter_file, 'w') as file:
                file.write(str(counter))
        except IOError as e:
            print(f"Error writing to counter file: {e}")
