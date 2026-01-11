#!/usr/bin/env python3
"""
Dashboard Testing Suite

Tests all Streamlit dashboards to ensure they compile and are accessible.
Run before claiming dashboards are ready.

Usage:
    python test/test_dashboards.py
    
Returns:
    0 if all tests pass
    1 if any test fails
"""

import subprocess
import time
import requests
import sys
from pathlib import Path


class DashboardTester:
    """Test Streamlit dashboards for compilation and accessibility"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.processes = []
        self.test_results = []
        
    def cleanup(self):
        """Kill all test processes"""
        for proc in self.processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except:
                try:
                    proc.kill()
                except:
                    pass
    
    def test_dashboard(self, name: str, file_path: str, port: int, wait_time: int = 15) -> bool:
        """
        Test a single dashboard
        
        Args:
            name: Dashboard name for reporting
            file_path: Path to the Streamlit file
            port: Port to run on
            wait_time: Seconds to wait for startup
            
        Returns:
            True if test passes, False otherwise
        """
        print(f"\n{'='*70}")
        print(f"Testing: {name}")
        print(f"File: {file_path}")
        print(f"Port: {port}")
        print(f"{'='*70}")
        
        full_path = self.project_root / file_path
        
        # Check file exists
        if not full_path.exists():
            print(f"❌ FAIL: File does not exist: {full_path}")
            self.test_results.append((name, False, "File not found"))
            return False
        
        print(f"✓ File exists")
        
        # Try to compile (syntax check)
        print(f"→ Checking Python syntax...")
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(full_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ FAIL: Python syntax error")
            print(result.stderr)
            self.test_results.append((name, False, "Syntax error"))
            return False
        
        print(f"✓ Python syntax valid")
        
        # Start Streamlit server
        print(f"→ Starting Streamlit on port {port}...")
        try:
            proc = subprocess.Popen(
                [
                    sys.executable, "-m", "streamlit", "run",
                    str(full_path),
                    "--server.port", str(port),
                    "--server.headless", "true",
                    "--server.address", "localhost"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.project_root)
            )
            self.processes.append(proc)
            
        except Exception as e:
            print(f"❌ FAIL: Could not start Streamlit: {e}")
            self.test_results.append((name, False, f"Start failed: {e}"))
            return False
        
        print(f"✓ Streamlit process started (PID: {proc.pid})")
        
        # Wait for server to be ready
        print(f"→ Waiting {wait_time}s for server to be ready...")
        time.sleep(wait_time)
        
        # Check if process is still running
        if proc.poll() is not None:
            stdout, stderr = proc.communicate()
            print(f"❌ FAIL: Process died during startup")
            print(f"Exit code: {proc.returncode}")
            print(f"STDERR:\n{stderr.decode()}")
            self.test_results.append((name, False, "Process died"))
            return False
        
        print(f"✓ Process still running")
        
        # Try to connect to the server
        print(f"→ Testing HTTP connection to http://localhost:{port}...")
        url = f"http://localhost:{port}"
        
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"✓ Server responded with status 200")
                    print(f"✓ Content length: {len(response.content)} bytes")
                    
                    # Check for basic Streamlit markers
                    if b"streamlit" in response.content.lower() or b"<!DOCTYPE html>" in response.content:
                        print(f"✓ Valid HTML/Streamlit content detected")
                        print(f"\n✅ PASS: {name} is working correctly!")
                        self.test_results.append((name, True, "All checks passed"))
                        
                        # Keep server running for a moment
                        time.sleep(2)
                        
                        # Stop the server
                        print(f"→ Stopping server...")
                        proc.terminate()
                        proc.wait(timeout=5)
                        print(f"✓ Server stopped cleanly")
                        
                        return True
                    else:
                        print(f"⚠️  Server responded but content looks wrong")
                        
                else:
                    print(f"⚠️  Attempt {attempt+1}/{max_attempts}: Status {response.status_code}")
                    if attempt < max_attempts - 1:
                        time.sleep(3)
                        
            except requests.exceptions.ConnectionError:
                print(f"⚠️  Attempt {attempt+1}/{max_attempts}: Connection refused")
                if attempt < max_attempts - 1:
                    time.sleep(3)
            except Exception as e:
                print(f"⚠️  Attempt {attempt+1}/{max_attempts}: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(3)
        
        print(f"❌ FAIL: Could not connect to server after {max_attempts} attempts")
            
        self.test_results.append((name, False, "Connection failed"))
        return False
    
    def run_all_tests(self):
        """Run all dashboard tests"""
        print("\n" + "="*70)
        print("STREAMLIT DASHBOARD TEST SUITE")
        print("="*70)
        
        # Define all dashboards to test
        dashboards = [
            ("Main Dashboard Hub", "src/reports/main_dashboard.py", 8501),
            ("Draft Preparation", "src/reports/draft_dashboard.py", 8502),
            ("Day-to-Day Season", "src/reports/day_to_day_season.py", 8503),
            ("Postseason Roster Lock", "src/reports/postseason_report.py", 8504),
        ]
        
        passed = 0
        failed = 0
        
        try:
            for name, path, port in dashboards:
                if self.test_dashboard(name, path, port):
                    passed += 1
                else:
                    failed += 1
                    
                # Clean up between tests
                self.cleanup()
                time.sleep(2)
                
        finally:
            # Ensure all processes are killed
            self.cleanup()
        
        # Print summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        for name, success, message in self.test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status}: {name}")
            if not success:
                print(f"         Reason: {message}")
        
        print(f"\nTotal: {passed} passed, {failed} failed")
        
        if failed > 0:
            print("\n❌ SOME TESTS FAILED - Dashboards are NOT ready")
            return 1
        else:
            print("\n✅ ALL TESTS PASSED - Dashboards are ready!")
            return 0


def main():
    """Main test execution"""
    tester = DashboardTester()
    
    try:
        exit_code = tester.run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        tester.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()
        tester.cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()
