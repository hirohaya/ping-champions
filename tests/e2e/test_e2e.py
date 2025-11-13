#!/usr/bin/env python
"""E2E Tests for Ping Champions"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8001"
TIMEOUT = 5

class E2ETests:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
        
    def wait_for_server(self, max_retries=10):
        """Wait for server to be ready"""
        for i in range(max_retries):
            try:
                response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
                if response.status_code == 200:
                    print("✅ Backend server is running")
                    return True
            except:
                print(f"⏳ Waiting for backend... ({i+1}/{max_retries})")
                time.sleep(1)
        return False
    
    def test(self, name, method, endpoint, data=None, expected_status=200):
        """Run a single test"""
        try:
            url = f"{BASE_URL}{endpoint}"
            print(f"\n🧪 Testing: {name}")
            print(f"   {method} {endpoint}")
            
            if method == "GET":
                response = requests.get(url, timeout=TIMEOUT)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=TIMEOUT)
            elif method == "PUT":
                response = requests.put(url, json=data, timeout=TIMEOUT)
            elif method == "DELETE":
                response = requests.delete(url, timeout=TIMEOUT)
            
            if response.status_code == expected_status:
                print(f"   ✅ Status {response.status_code} (expected {expected_status})")
                try:
                    content = response.json()
                    print(f"   📦 Response: {json.dumps(content, indent=2)}")
                except:
                    print(f"   📦 Response: {response.text}")
                self.passed += 1
                self.results.append((name, "PASSED", response.status_code))
                return response
            else:
                print(f"   ❌ Status {response.status_code} (expected {expected_status})")
                print(f"   Error: {response.text}")
                self.failed += 1
                self.results.append((name, "FAILED", response.status_code))
                return None
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
            self.failed += 1
            self.results.append((name, "ERROR", str(e)))
            return None
    
    def run_all(self):
        """Run all E2E tests"""
        print("=" * 60)
        print("🚀 Starting E2E Tests for Ping Champions")
        print("=" * 60)
        
        # Wait for backend
        if not self.wait_for_server():
            print("❌ Backend server is not running")
            sys.exit(1)
        
        # Test 1: Root endpoint
        self.test("Root Endpoint", "GET", "/", expected_status=200)
        
        # Test 2: Create event
        event_data = {
            "name": "Ping Match #1",
            "date": "2024-12-15",
            "time": "19:00"
        }
        event_response = self.test("Create Event", "POST", "/create", data=event_data, expected_status=200)
        
        event_id = None
        if event_response:
            try:
                event_id = event_response.json().get("id")
                print(f"   Event ID: {event_id}")
            except:
                pass
        
        # Test 3: List events
        self.test("List Events", "GET", "/events", expected_status=200)
        
        # Test 4: Register player
        if event_id:
            player_data = {
                "name": "João Silva",
                "event_id": event_id
            }
            player_response = self.test("Register Player", "POST", "/", data=player_data, expected_status=200)
            
            player_id = None
            if player_response:
                try:
                    player_id = player_response.json().get("id")
                    print(f"   Player ID: {player_id}")
                except:
                    pass
            
            # Test 5: List players
            self.test("List Players", "GET", f"/players?event_id={event_id}", expected_status=200)
            
            # Test 6: Get all players (system stats)
            self.test("List All Players", "GET", "/players/all", expected_status=200)
        
        # Test 7: API Health - check multiple endpoints
        self.test("Matches Endpoint", "GET", "/matches?event_id=1", expected_status=200)
        
        # Test 8: Ranking endpoint
        self.test("Ranking Endpoint", "GET", "/ranking?event_id=1", expected_status=200)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 E2E Test Summary")
        print("=" * 60)
        
        for test_name, status, result in self.results:
            symbol = "✅" if status == "PASSED" else "❌"
            print(f"{symbol} {test_name}: {status} ({result})")
        
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Total: {self.passed + self.failed}")
        print(f"📊 Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        print("=" * 60)

if __name__ == "__main__":
    tester = E2ETests()
    tester.run_all()
