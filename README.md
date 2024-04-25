# Hand-gesture-mouse-control
This program enables desktop control using hand gestures captured through a webcam.

## Supported Gestures:
* LMB
* RMB
* Holding LMB
* opening on-screen keyboard

## Requirements
For the program to run you need the following Python packages:
* cv2
* mediapipe
* pyautogui

### How to Run

 If you're not using Anaconda, follow these steps to set up the environment and run the script:

 1. **Ensure Python is Installed**: Make sure you have Python installed on your system. If not, download and install it from [Python's official website](https://www.python.org/).

 2. **Install Required Packages**: Navigate to the directory containing the project files and use pip to install the required packages listed in `requirementspip.txt`. Please note that `requirementspip.txt` may include additional packages that are not necessary for running `hand_control.py`. These additional packages might have been included as the `requirementspip.txt` file was generated from a Conda environment.

     ```bash
     pip install -r requirementspip.txt
     ```

 3. **Run the Script**: After installing the necessary packages, execute the following command in your terminal or command prompt:

     ```bash
     python hand_control.py
     ```

 Following these steps should install the required dependencies and run the Python script successfully.
 ### How to Run (Anaconda)

 If you're using Anaconda, follow these steps to set up the environment and run the script:

 1. **Open Anaconda Prompt**: Launch Anaconda Prompt from your system's applications.

 2. **Create a New Conda Environment**: Use the following command to create a new Conda environment. Replace `your_env_name` with a name of your choice. Please note that `requirementsconda.txt` may include additional packages that are not necessary for running `hand_control.py`. These additional packages might have been included as the `requirementsconda.txt` file was generated from a Conda environment.

     ```bash
     conda create --name your_env_name --file requirementsconda.txt
     ```

 3. **Activate Your Environment**: After the environment is created, activate it using the command below. Remember to replace `your_env_name` with the chosen environment name.

     ```bash
     conda activate your_env_name
     ```

 4. **Run the Script**: Navigate to the directory containing `hand_control.py` and execute the following command:

     ```bash
     python hand_control.py
     ```

 Following these steps should prepare your environment and execute the Python script successfully.
