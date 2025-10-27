#!/usr/bin/env python3
"""
Demo script for FA-2 Automation Testing Presentation
"""

import subprocess
import time
import os
import sys


def run_automation_demo():
    print("🚀 Starting Automation Testing Demo for FRUITABLES")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: Please run this script from the project root directory")
        return
    
    # Start Django server in background
    print("1. Starting Django development server...")
    server_process = subprocess.Popen(
        ["python", "manage.py", "runserver", "8001"],  # Use different port
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)  # Wait for server to start
    
    try:
        # Check if server is running
        import requests
        try:
            response = requests.get("http://localhost:8001/", timeout=5)
            if response.status_code == 200:
                print("✅ Django server is running successfully!")
            else:
                print("⚠️ Server started but may have issues")
        except:
            print("⚠️ Could not verify server status, but continuing...")
        
        # Run automation tests
        print("\n2. Running Selenium Automation Tests...")
        print("   👀 Browser will open automatically...")
        print("   📸 Screenshots will be saved to quality/ folder")
        
        # Create quality directory if it doesn't exist
        os.makedirs("quality", exist_ok=True)
        
        # Run specific automation tests
        test_commands = [
            ["pytest", "store/tests/automation/tests/test_login_ui.py", "-v", "-s", "-m", "automation"],
            ["pytest", "store/tests/automation/tests/test_add_to_cart_ui.py", "-v", "-s", "-m", "automation"],
            ["pytest", "store/tests/automation/tests/test_checkout_ui.py", "-v", "-s", "-m", "automation"]
        ]
        
        for i, cmd in enumerate(test_commands, 1):
            print(f"\n   Running Test Suite {i}/3: {' '.join(cmd[2:])}")
            print("   " + "-" * 50)
            
            result = subprocess.run(cmd, capture_output=False, text=True)
            
            if result.returncode == 0:
                print(f"✅ Test Suite {i} PASSED!")
            else:
                print(f"❌ Test Suite {i} had some failures, but demo continues...")
            
            time.sleep(2)  # Pause between test suites
        
        print("\n3. Running All Automation Tests Together...")
        print("   " + "-" * 50)
        
        result = subprocess.run([
            "pytest", 
            "store/tests/automation/tests/", 
            "-v", "-s", "-m", "automation"
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("✅ All Automation Tests PASSED!")
        else:
            print("❌ Some tests failed, but demo completed!")
            
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    finally:
        # Stop server
        print("\n4. Stopping Django server...")
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
            print("✅ Server stopped successfully")
        except:
            print("⚠️ Server may still be running")
    
    print("\n🎉 Demo completed! Ready for presentation.")
    print("\n📁 Check the 'quality/' folder for screenshots")
    print("📊 View test results above for detailed information")


def run_unit_tests():
    """Run unit tests for comparison"""
    print("\n🧪 Running Unit Tests for comparison...")
    print("=" * 40)
    
    result = subprocess.run([
        "pytest", 
        "store/tests/unit/", 
        "-v", "--tb=short"
    ], capture_output=False, text=True)
    
    if result.returncode == 0:
        print("✅ Unit Tests PASSED!")
    else:
        print("❌ Some unit tests failed")


def run_coverage_report():
    """Run coverage report"""
    print("\n📊 Generating Coverage Report...")
    print("=" * 40)
    
    result = subprocess.run([
        "pytest", 
        "--cov=store", 
        "--cov-report=html", 
        "--cov-report=term-missing",
        "-v"
    ], capture_output=False, text=True)
    
    print("📁 Coverage report saved to htmlcov/index.html")


if __name__ == "__main__":
    print("🎯 FRUITABLES FA-2 Testing Demo")
    print("Choose an option:")
    print("1. Run Automation Tests Demo (with visible browser)")
   
    
    try:
        choice = input("\nEnter your choice (1): ").strip()
        
        if choice == "1":
            run_automation_demo()
        elif choice == "2":
            run_unit_tests()
        elif choice == "3":
            run_coverage_report()
        elif choice == "4":
            run_unit_tests()
            run_automation_demo()
            run_coverage_report()
        else:
            print("Invalid choice. Running automation demo by default...")
            run_automation_demo()
            
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
