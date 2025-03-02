#!/usr/bin/env python3
"""
SKYNET Invoice Generator Launcher
This script checks for required dependencies, installs them if needed, and runs the application.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time

class DependencyInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SKYNET Invoice Generator Setup")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title label
        title_label = ttk.Label(main_frame, text="SKYNET Invoice Generator", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Checking dependencies...", font=("Arial", 10))
        self.status_label.pack(pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=(0, 20))
        
        # Details text
        self.details_frame = ttk.Frame(main_frame)
        self.details_frame.pack(fill="both", expand=True)
        
        self.details_text = tk.Text(self.details_frame, height=8, width=50, wrap="word")
        self.details_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.details_frame, orient="vertical", command=self.details_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.details_text.configure(yscrollcommand=scrollbar.set)
        
        # Start the dependency check in a separate thread
        self.thread = threading.Thread(target=self.check_and_install_dependencies)
        self.thread.daemon = True
        self.thread.start()
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def update_status(self, message):
        """Update the status label."""
        self.status_label.config(text=message)
        self.log_message(message)
    
    def log_message(self, message):
        """Add a message to the details text."""
        self.details_text.insert(tk.END, message + "\n")
        self.details_text.see(tk.END)
    
    def update_progress(self, value):
        """Update the progress bar."""
        self.progress["value"] = value
        self.root.update_idletasks()
    
    def check_and_install_dependencies(self):
        """Check for required dependencies and install them if needed."""
        try:
            # Check if pip is installed
            self.update_status("Checking for pip...")
            self.update_progress(10)
            
            try:
                import pip
                self.log_message("Pip is installed.")
            except ImportError:
                self.update_status("Pip is not installed. Installing pip...")
                self.log_message("This may take a few minutes. Please wait...")
                
                # Install pip (this is system-dependent)
                if sys.platform == "win32":
                    # Windows
                    self.log_message("Windows detected. Installing pip...")
                    # Download get-pip.py
                    subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
                else:
                    # macOS/Linux
                    self.log_message("macOS/Linux detected. Installing pip...")
                    subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
                
                self.update_status("Pip installed successfully.")
            
            # Get the requirements file path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            requirements_path = os.path.join(script_dir, "requirements.txt")
            
            if not os.path.exists(requirements_path):
                self.update_status("Error: requirements.txt not found.")
                self.log_message(f"Looking for: {requirements_path}")
                messagebox.showerror("Error", "requirements.txt not found. Cannot install dependencies.")
                self.root.destroy()
                return
            
            # Read requirements
            with open(requirements_path, "r") as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            
            total_packages = len(requirements)
            installed_packages = 0
            
            self.update_status(f"Installing {total_packages} packages...")
            self.update_progress(20)
            
            # Install each package
            for package in requirements:
                package_name = package.split("==")[0].split(">=")[0].strip()
                self.update_status(f"Installing {package_name}...")
                
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])
                    self.log_message(f"Successfully installed {package}")
                except subprocess.CalledProcessError as e:
                    self.log_message(f"Error installing {package}: {str(e)}")
                    # Try without version constraint
                    try:
                        self.log_message(f"Trying to install {package_name} without version constraint...")
                        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--user"])
                        self.log_message(f"Successfully installed {package_name}")
                    except subprocess.CalledProcessError as e2:
                        self.log_message(f"Error installing {package_name}: {str(e2)}")
                
                installed_packages += 1
                progress_value = 20 + (installed_packages / total_packages * 60)
                self.update_progress(progress_value)
            
            self.update_status("All dependencies installed successfully.")
            self.update_progress(80)
            
            # Launch the application
            self.update_status("Launching SKYNET Invoice Generator...")
            self.log_message("Starting application...")
            
            # Find the app.py file
            app_path = os.path.join(script_dir, "app.py")
            if not os.path.exists(app_path):
                self.update_status("Error: app.py not found.")
                self.log_message(f"Looking for: {app_path}")
                messagebox.showerror("Error", "app.py not found. Cannot launch application.")
                self.root.destroy()
                return
            
            # Launch the application
            self.update_progress(90)
            time.sleep(1)  # Give user time to see the "Launching" message
            
            # Close the installer window
            self.root.after(0, self.launch_application, app_path)
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            self.log_message(f"An unexpected error occurred: {str(e)}")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def launch_application(self, app_path):
        """Launch the main application and close the installer."""
        self.update_progress(100)
        self.update_status("Setup complete. Starting application...")
        
        # Close this window
        self.root.destroy()
        
        # Start the main application
        subprocess.Popen([sys.executable, app_path])

if __name__ == "__main__":
    # Create the Tkinter application
    root = tk.Tk()
    app = DependencyInstallerApp(root)
    root.mainloop() 