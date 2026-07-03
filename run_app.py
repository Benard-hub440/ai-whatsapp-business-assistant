import os
import sys
import subprocess

def check_env():
    if not os.path.exists(".env"):
        print("Error: .env file not found!")
        print("Please create a .env file with your twilio ")
        return False
    return True

def check_dependencies():
    try:
        import flask
        import ollama
        import dotenv
        return True
    except ImportError as e:
        print(f"Missing dependency: {e.name}")
        print("Attempting to install dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            return True
        except Exception as install_err:
            print(f"Failed to install dependencies: {install_err}")
            return False

def main():
    print("Starting the service")
    
    if not check_env():
        return

    if not check_dependencies():
        print("Please run: pip install -r requirements.txt")
        return

    # Run the app
    print("Environment check passed. Starting Flask server...")
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n Shutting down...")

if __name__ == "__main__":
    main()
