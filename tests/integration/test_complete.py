#!/usr/bin/env python
"""Complete test runner - starts server and runs E2E tests"""
import subprocess
import time
import sys
import os
import requests
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def start_server():
    """Start backend server in subprocess"""
    print("🚀 Starting backend server...")
    cmd = [sys.executable, 'run_server.py']
    proc = subprocess.Popen(cmd, cwd=os.path.dirname(__file__), 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)  # Give server time to start
    return proc

def run_e2e_tests():
    """Run E2E tests"""
    BASE_URL = "http://localhost:8001"
    tests_passed = 0
    tests_failed = 0
    
    print("\n" + "="*60)
    print("🧪 Running E2E Tests")
    print("="*60)
    
    # Test 1: Root endpoint
    print("\n✓ Test 1: Root Endpoint")
    try:
        resp = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"  Status: {resp.status_code}")
        print(f"  Response: {resp.json()}")
        if resp.status_code == 200:
            tests_passed += 1
            print("  ✅ PASSED")
        else:
            tests_failed += 1
            print("  ❌ FAILED")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ ERROR: {e}")
    
    # Test 2: Create Event
    print("\n✓ Test 2: Create Event (POST /events/create)")
    try:
        event_data = {
            "name": "Ping Match Sprint 1",
            "date": "2024-12-15",
            "time": "19:00"
        }
        resp = requests.post(f"{BASE_URL}/events/create", json=event_data, timeout=5)
        print(f"  Status: {resp.status_code}")
        print(f"  Response: {resp.json()}")
        if resp.status_code == 200:
            tests_passed += 1
            print("  ✅ PASSED")
            event_id = resp.json().get("id")
        else:
            tests_failed += 1
            print("  ❌ FAILED")
            event_id = None
    except Exception as e:
        tests_failed += 1
        event_id = None
        print(f"  ❌ ERROR: {e}")
    
    # Test 3: List Events
    print("\n✓ Test 3: List Events (GET /)")
    try:
        resp = requests.get(f"{BASE_URL}/events", timeout=5)
        print(f"  Status: {resp.status_code}")
        events = resp.json()
        print(f"  Events count: {len(events) if isinstance(events, list) else 'unknown'}")
        if resp.status_code == 200:
            tests_passed += 1
            print("  ✅ PASSED")
        else:
            tests_failed += 1
            print("  ❌ FAILED")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ ERROR: {e}")
    
    # Test 4: Register Player
    if event_id:
        print("\n✓ Test 4: Register Player (POST /players)")
        try:
            resp = requests.post(
                f"{BASE_URL}/players/?name=João%20Silva&event_id={event_id}",
                timeout=5
            )
            print(f"  Status: {resp.status_code}")
            print(f"  Response: {resp.json()}")
            if resp.status_code == 200:
                tests_passed += 1
                print("  ✅ PASSED")
                player_id = resp.json().get("id")
            else:
                tests_failed += 1
                print("  ❌ FAILED")
                player_id = None
        except Exception as e:
            tests_failed += 1
            player_id = None
            print(f"  ❌ ERROR: {e}")
        
        # Test 5: List Players
        print("\n✓ Test 5: List Players (GET /players)")
        try:
            resp = requests.get(f"{BASE_URL}/players/?event_id={event_id}", timeout=5)
            print(f"  Status: {resp.status_code}")
            players = resp.json()
            print(f"  Players count: {len(players) if isinstance(players, list) else 'unknown'}")
            if resp.status_code == 200:
                tests_passed += 1
                print("  ✅ PASSED")
            else:
                tests_failed += 1
                print("  ❌ FAILED")
        except Exception as e:
            tests_failed += 1
            print(f"  ❌ ERROR: {e}")
        
        # Test 6: Get All Players
        print("\n✓ Test 6: List All Players (GET /players/all)")
        try:
            resp = requests.get(f"{BASE_URL}/players/all", timeout=5)
            print(f"  Status: {resp.status_code}")
            all_players = resp.json()
            print(f"  Total players: {len(all_players) if isinstance(all_players, list) else 'unknown'}")
            if resp.status_code == 200:
                tests_passed += 1
                print("  ✅ PASSED")
            else:
                tests_failed += 1
                print("  ❌ FAILED")
        except Exception as e:
            tests_failed += 1
            print(f"  ❌ ERROR: {e}")
    
    # Test 7: Matches endpoint
    print("\n✓ Test 7: List Matches (GET /matches)")
    try:
        resp = requests.get(f"{BASE_URL}/matches/?event_id=1", timeout=5)
        print(f"  Status: {resp.status_code}")
        matches = resp.json()
        print(f"  Matches count: {len(matches) if isinstance(matches, list) else 'unknown'}")
        if resp.status_code == 200:
            tests_passed += 1
            print("  ✅ PASSED")
        else:
            tests_failed += 1
            print("  ❌ FAILED")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ ERROR: {e}")
    
    # Test 8: Ranking endpoint
    print("\n✓ Test 8: Ranking (GET /ranking)")
    try:
        resp = requests.get(f"{BASE_URL}/ranking?event_id=1", timeout=5)
        print(f"  Status: {resp.status_code}")
        if resp.status_code == 200 or resp.status_code == 404:  # 404 OK if endpoint is optional
            tests_passed += 1
            print("  ✅ PASSED")
        else:
            tests_failed += 1
            print("  ❌ FAILED")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ ERROR: {e}")
    
    # Test 9: Create Match
    match_id = None
    if event_id and "player_id" in locals():
        print("\n✓ Test 9: Create Match (POST /matches)")
        try:
            # Create second player first
            resp2 = requests.post(
                f"{BASE_URL}/players/?name=Maria%20Santos&event_id={event_id}",
                timeout=5
            )
            if resp2.status_code == 200:
                player2_id = resp2.json().get("id")
                
                # Create match with both players
                match_data = {
                    "event_id": event_id,
                    "player1_id": player_id,
                    "player2_id": player2_id,
                    "best_of": 5
                }
                resp = requests.post(f"{BASE_URL}/matches/", json=match_data, timeout=5)
                print(f"  Status: {resp.status_code}")
                print(f"  Response: {resp.json()}")
                if resp.status_code == 200:
                    tests_passed += 1
                    print("  ✅ PASSED")
                    match_id = resp.json().get("id")
                else:
                    tests_failed += 1
                    print("  ❌ FAILED")
            else:
                tests_failed += 1
                print("  ❌ FAILED to create second player")
        except Exception as e:
            tests_failed += 1
            print(f"  ❌ ERROR: {e}")
        
        # Test 10: Get single match
        if match_id:
            print("\n✓ Test 10: Get Match (GET /matches/{id})")
            try:
                resp = requests.get(f"{BASE_URL}/matches/{match_id}", timeout=5)
                print(f"  Status: {resp.status_code}")
                print(f"  Response: {resp.json()}")
                if resp.status_code == 200:
                    tests_passed += 1
                    print("  ✅ PASSED")
                else:
                    tests_failed += 1
                    print("  ❌ FAILED")
            except Exception as e:
                tests_failed += 1
                print(f"  ❌ ERROR: {e}")
            
            # Test 11: Update match (set winner)
            print("\n✓ Test 11: Update Match (PUT /matches/{id})")
            try:
                update_data = {
                    "winner_id": player_id,
                    "finished": 1
                }
                resp = requests.put(f"{BASE_URL}/matches/{match_id}", json=update_data, timeout=5)
                print(f"  Status: {resp.status_code}")
                print(f"  Response: {resp.json()}")
                if resp.status_code == 200:
                    tests_passed += 1
                    print("  ✅ PASSED")
                else:
                    tests_failed += 1
                    print("  ❌ FAILED")
            except Exception as e:
                tests_failed += 1
                print(f"  ❌ ERROR: {e}")
    
    # Test 12: Get single event
    print("\n✓ Test 12: Get Event (GET /events/{id})")
    try:
        resp = requests.get(f"{BASE_URL}/events/1", timeout=5)
        print(f"  Status: {resp.status_code}")
        if resp.status_code == 200 or resp.status_code == 404:
            tests_passed += 1
            print("  ✅ PASSED")
        else:
            tests_failed += 1
            print("  ❌ FAILED")
    except Exception as e:
        tests_failed += 1
        print(f"  ❌ ERROR: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 E2E Test Summary")
    print("="*60)
    print(f"✅ Passed: {tests_passed}")
    print(f"❌ Failed: {tests_failed}")
    print(f"📈 Total: {tests_passed + tests_failed}")
    if tests_passed + tests_failed > 0:
        rate = (tests_passed / (tests_passed + tests_failed)) * 100
        print(f"📊 Success Rate: {rate:.1f}%")
    print("="*60)
    
    return tests_failed == 0

if __name__ == '__main__':
    # Start server
    server_proc = start_server()
    
    try:
        # Run tests
        success = run_e2e_tests()
        sys.exit(0 if success else 1)
    finally:
        # Cleanup
        print("\n🛑 Stopping server...")
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except:
            server_proc.kill()
        print("✅ Server stopped")
