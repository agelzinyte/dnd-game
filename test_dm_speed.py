"""Quick test to check DM API response time."""

import time
from dndgame.dungeon_master import DungeonMaster

dm = DungeonMaster(enabled=True)

print("Testing DM API response time...")
print("=" * 50)

start = time.time()
narration = dm.narrate_combat_start("TestPlayer", "Goblin")
elapsed = time.time() - start

if narration:
    print(f"\n🎲 {narration}\n")
    print("=" * 50)
    print(f"✅ API call successful!")
    print(f"⏱️  Response time: {elapsed:.2f} seconds")
else:
    print("❌ API call failed or DM is disabled")
    print(f"⏱️  Time taken: {elapsed:.2f} seconds")

print("\nNote: First API call is often slower due to connection setup.")
print("Subsequent calls should be faster (1-2 seconds).")
