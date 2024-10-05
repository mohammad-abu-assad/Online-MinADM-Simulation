import os


class FileManager:
    """Handles all file-related operations."""

    def __init__(self, data_directory, results_file):
        self.data_directory = data_directory
        self.results_file = results_file
        os.makedirs(self.data_directory, exist_ok=True)
        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)

    def save_experiment_data(self, file_name, content):
        """Saves experiment data to the specified file."""
        file_path = os.path.join(self.data_directory, file_name)
        try:
            with open(file_path, 'w') as file:
                file.write(content)
        except IOError as e:
            print(f"Error writing to file {file_path}: {e}")

    def append_to_results(self, result_line):
        """Appends the result data to the results file."""
        try:
            with open(self.results_file, 'a') as result_file:
                result_file.write(result_line)
        except IOError as e:
            print(f"Error writing to results file: {e}")

    def load_results(self):
        """Loads and returns the results from the results file."""
        results = []
        try:
            with open(self.results_file, 'r') as result_file:
                lines = result_file.readlines()
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines
                    parts = line.split(',')
                    if len(parts) != 3:
                        print(f"Skipping invalid line in results file: {line}")
                        continue
                    try:
                        number_of_nodes = int(parts[0])
                        number_of_paths = int(parts[1])
                        competitive_ratio = float(parts[2])
                        results.append({
                            'number_of_nodes': number_of_nodes,
                            'number_of_paths': number_of_paths,
                            'competitive_ratio': competitive_ratio
                        })
                    except ValueError as e:
                        print(f"Error parsing line in results file: {line} - {e}")
        except IOError as e:
            print(f"Error reading results file: {e}")
        return results
