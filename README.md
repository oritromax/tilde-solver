# Movie Folder Cleaner

## WHY? 

[Read the blog post](https://ioritro.com)

## Overview

The Movie Folder Cleaner script helps you clean up your movie folders by identifying and handling folders that contain a `~` in their name. It performs the following actions:

1. Lists all folders with a `~` in their name.
2. Finds corresponding folders without `~` based on a refined base name.
3. Deletes folders with `~` if the corresponding folder has a movie file larger than 600 MB.
4. Moves movie files from folders with `~` to corresponding folders if the latter does not have a movie file, then deletes the `~` folder.
5. Deletes folders with `~` if both the `~` folder and the corresponding folder have large movie files.
6. Prints remaining folders with `~` in their name.
7. Prints folders with multiple corresponding matches for manual handling.

## Features

- Automatically identifies and processes movie folders with `~` in their names.
- Safely moves or deletes folders based on predefined criteria.
- Handles cases with multiple matching folders by listing them for manual review.
- Outputs color-coded messages for easy reading in the terminal.

## Requirements

- Python 3.6+
- Appropriate permissions to read, move, and delete files in the specified directory.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/oritromax/tilde-solver.git
    cd movie-folder-cleaner
    ```

2. Ensure you have the necessary permissions to run the script on your directories.

## Usage

1. Open the script `main.py` in a text editor.

2. Modify the `root_dir` variable to point to your movie directory:

    ```python
    root_dir = "/path/to/your/root/directory"
    ```

3. Run the script:

    ```bash
    python main.py
    ```

4. Follow the prompts in the terminal. The script will:
    - List folders marked for deletion or file moving.
    - Ask for your confirmation before proceeding with each action.
    - Output the results, including any remaining folders and folders with multiple matches.


## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## Contact

If you have any questions or issues, please open an issue on GitHub. 
