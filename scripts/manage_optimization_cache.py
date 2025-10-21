#!/usr/bin/env python3
"""
Manage workflow optimization cache.

Usage:
    # View cache stats
    python scripts/manage_optimization_cache.py --stats

    # Clear entire cache
    python scripts/manage_optimization_cache.py --clear

    # Invalidate specific workflow
    python scripts/manage_optimization_cache.py --invalidate implement.md

    # List all cached workflows
    python scripts/manage_optimization_cache.py --list

    # Export cache for inspection
    python scripts/manage_optimization_cache.py --export cache-backup.json
"""

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


class OptimizationCache:
    """Thread-safe optimization cache with file persistence."""

    def __init__(self, cache_path: str = ".windsurf/.optimization-cache.json"):
        self.cache_path = Path(cache_path)
        self.data = self._load()

    def _load(self) -> dict:
        """Load cache from disk."""
        if not self.cache_path.exists():
            return {
                "version": "1.0.0",
                "created": datetime.utcnow().isoformat() + "Z",
                "cache": {},
                "stats": {
                    "total_entries": 0,
                    "cache_hits": 0,
                    "cache_misses": 0,
                    "last_updated": datetime.utcnow().isoformat() + "Z",
                },
            }

        with open(self.cache_path) as f:
            return json.load(f)

    def _save(self):
        """Save cache to disk."""
        self.data["stats"]["last_updated"] = datetime.utcnow().isoformat() + "Z"

        # Ensure directory exists
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.cache_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def get(self, cache_key: str) -> str | None:
        """
        Get cached result.

        Returns:
            Optimized content if cache hit, None if cache miss
        """
        if cache_key in self.data["cache"]:
            self.data["stats"]["cache_hits"] += 1
            self._save()
            return self.data["cache"][cache_key]["optimized_content"]

        self.data["stats"]["cache_misses"] += 1
        self._save()
        return None

    def put(
        self,
        cache_key: str,
        file_path: str,
        original_content: str,
        optimized_content: str,
        metadata: dict,
    ):
        """Store optimization result in cache."""
        original_hash = hashlib.sha256(original_content.encode()).hexdigest()

        self.data["cache"][cache_key] = {
            "file_path": file_path,
            "original_content_hash": original_hash,
            "optimized_content": optimized_content,
            "metadata": {**metadata, "timestamp": datetime.utcnow().isoformat() + "Z"},
        }

        self.data["stats"]["total_entries"] = len(self.data["cache"])
        self._save()

    def invalidate(self, cache_key: str) -> bool:
        """Remove entry from cache. Returns True if found and removed."""
        if cache_key in self.data["cache"]:
            del self.data["cache"][cache_key]
            self.data["stats"]["total_entries"] = len(self.data["cache"])
            self._save()
            return True
        return False

    def clear(self):
        """Clear entire cache."""
        self.data["cache"] = {}
        self.data["stats"]["total_entries"] = 0
        self._save()

    def stats(self) -> dict:
        """Get cache statistics."""
        return self.data["stats"]

    def find_by_path(self, file_path: str) -> tuple[str, dict] | None:
        """Find cache entry by file path. Returns (cache_key, entry) or None."""
        for key, entry in self.data["cache"].items():
            if entry["file_path"] == file_path:
                return (key, entry)
        return None


def main():
    parser = argparse.ArgumentParser(description="Manage optimization cache")
    parser.add_argument("--stats", action="store_true", help="Show cache statistics")
    parser.add_argument("--clear", action="store_true", help="Clear entire cache")
    parser.add_argument("--invalidate", metavar="WORKFLOW", help="Invalidate specific workflow")
    parser.add_argument("--export", metavar="FILE", help="Export cache to file")
    parser.add_argument("--list", action="store_true", help="List all cached workflows")

    args = parser.parse_args()

    cache = OptimizationCache()

    if args.stats:
        stats = cache.stats()
        print("\nCache Statistics:")
        print(f"  Total entries: {stats['total_entries']}")
        print(f"  Cache hits: {stats['cache_hits']}")
        print(f"  Cache misses: {stats['cache_misses']}")
        print(f"  Last updated: {stats['last_updated']}")

        if stats["total_entries"] > 0:
            total_requests = stats["cache_hits"] + stats["cache_misses"]
            if total_requests > 0:
                hit_rate = stats["cache_hits"] / total_requests * 100
                print(f"  Hit rate: {hit_rate:.1f}%")

    elif args.clear:
        confirm = input("Clear entire cache? This cannot be undone. (y/N): ")
        if confirm.lower() == "y":
            cache.clear()
            print("✅ Cache cleared")
        else:
            print("❌ Cancelled")

    elif args.invalidate:
        workflow_path = f".windsurf/workflows/{args.invalidate}"
        result = cache.find_by_path(workflow_path)

        if result:
            cache_key, entry = result
            cache.invalidate(cache_key)
            print(f"✅ Invalidated cache for {workflow_path}")
        else:
            print(f"❌ No cache entry found for {workflow_path}")

    elif args.export:
        with open(args.export, "w") as f:
            json.dump(cache.data, f, indent=2)
        print(f"✅ Cache exported to {args.export}")

    elif args.list:
        if not cache.data["cache"]:
            print("\n📭 Cache is empty")
        else:
            print(f"\n📦 Cached workflows ({len(cache.data['cache'])} entries):\n")
            for key, entry in cache.data["cache"].items():
                print(f"  {entry['file_path']}")
                print(f"    Hash: {key[:16]}...")
                print(f"    Cached: {entry['metadata']['timestamp']}")
                original_tokens = entry["metadata"].get("original_tokens", "?")
                optimized_tokens = entry["metadata"].get("optimized_tokens", "?")
                print(f"    Tokens: {original_tokens} → {optimized_tokens}")
                print()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
