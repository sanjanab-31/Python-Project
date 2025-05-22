import subprocess
import sys
import os
import time

def run_command(command, cwd=None):
    """Run a command and return its output"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    print("=== Setting up Smart Rainwater Harvester ===\n")
    
    # 1. Install requirements
    print("1. Installing Python requirements...")
    success, output = run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    if not success:
        print("Error installing requirements:", output)
        return
    print("Requirements installed successfully!\n")

    # 2. Test MongoDB connection
    print("2. Testing MongoDB connection...")
    success, output = run_command([sys.executable, "test_mongodb.py"])
    if not success:
        print("Error testing MongoDB connection:", output)
        return
    print(output)

    # 3. Run Django migrations
    print("\n3. Running Django migrations...")
    success, output = run_command([sys.executable, "manage.py", "makemigrations"])
    if not success:
        print("Error making migrations:", output)
        return
    print(output)

    success, output = run_command([sys.executable, "manage.py", "migrate"])
    if not success:
        print("Error applying migrations:", output)
        return
    print(output)

    # 4. Test MongoDB operations
    print("\n4. Testing MongoDB operations...")
    success, output = run_command([sys.executable, "test_mongodb_operations.py"])
    if not success:
        print("Error testing MongoDB operations:", output)
        return
    print(output)

    # 5. Start the development server
    print("\n5. Starting development server...")
    server_process = subprocess.Popen(
        [sys.executable, "manage.py", "runserver"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait a bit for the server to start
    time.sleep(2)
    
    if server_process.poll() is None:
        print("Development server is running!")
        print("You can access the API at: http://localhost:8000/")
        print("\nPress Ctrl+C to stop the server...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server_process.terminate()
            print("\nServer stopped.")
    else:
        stdout, stderr = server_process.communicate()
        print("Error starting development server:")
        print(stderr)

if __name__ == "__main__":
    main()
