import subprocess
import os

def main():
    print("Starting Job Copilot Dashboard...")
    # Change directory to the root of the project
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    # Run streamlit
    try:
        subprocess.run(["streamlit", "run", "ui/app.py"])
    except KeyboardInterrupt:
        print("\nStopping Job Copilot.")

if __name__ == "__main__":
    main()
