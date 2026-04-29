import redis
import numpy as np
from typing import Optional, List, Dict
import logging

logger = logging.getLogger("TrustMark-Cache")

class EncodingCache:
    def __init__(
        self,
        redis_client: redis.Redis,
        ttl_hours: int = 24,
        namespace: str = "trustmark:v25"
    ):
        self.redis = redis_client
        self.ttl_seconds = ttl_hours * 3600
        self.ns = namespace
        self.registry_key = f"{self.ns}:registry:uids" # 📊 New: Global Tracking Set

    # ============================================================================
    # 🔑 KEY GENERATION
    # ============================================================================
    def _key(self, uid: str) -> str:
        return f"{self.ns}:enc:{uid.upper()}"

    # ============================================================================
    # ⚡ STORE ENCODING (Binary Fast + Registry Sync)
    # ============================================================================
    def cache_encoding(self, uid: str, encoding: List[float]) -> bool:
        try:
            uid = uid.upper()
            key = self._key(uid)

            # 🔥 Binary conversion (float32 is enough for 128-d face encodings)
            arr = np.array(encoding, dtype=np.float32)
            binary = arr.tobytes()

            # Using Pipeline for Atomic Operation
            pipe = self.redis.pipeline()
            pipe.setex(key, self.ttl_seconds, binary)
            pipe.sadd(self.registry_key, uid) # 📊 Track in registry
            pipe.execute()

            logger.info(f"✅ [CACHE_SET]: Identity {uid} pushed to Matrix RAM")
            return True

        except Exception as e:
            logger.error(f"⚠️ Cache push error: {e}")
            return False

    # ============================================================================
    # ⚡ GET ENCODING (Ultra Fast Buffer Fetch)
    # ============================================================================
    def get_encoding(self, uid: str) -> Optional[np.ndarray]:
        try:
            data = self.redis.get(self._key(uid))
            if not data:
                return None

            # 🏎️ Direct memory read
            return np.frombuffer(data, dtype=np.float32)
        except Exception as e:
            logger.error(f"❌ Fetch error: {e}")
            return None

    # ============================================================================
    # ⚡ BATCH SYNC (Mass Deployment 🔥)
    # ============================================================================
    def batch_sync(self, users_dict: Dict[str, List[float]]) -> int:
        if not users_dict: return 0
        try:
            pipe = self.redis.pipeline()
            for uid, enc in users_dict.items():
                uid = uid.upper()
                arr = np.array(enc, dtype=np.float32)
                pipe.setex(self._key(uid), self.ttl_seconds, arr.tobytes())
                pipe.sadd(self.registry_key, uid)

            results = pipe.execute()
            count = sum(1 for r in results if r)
            logger.info(f"📦 [MATRIX_SYNC]: {count} identities hot-swapped")
            return count
        except Exception as e:
            logger.error(f"❌ Batch sync fail: {e}")
            return 0

    # ============================================================================
    # 📊 HEALTH & ANALYTICS (Real-time Dashboard Power)
    # ============================================================================
    def get_health_stats(self) -> dict:
        try:
            info = self.redis.info("memory")
            # 🏎️ Use SCARD instead of SCAN for O(1) count
            count = self.redis.scard(self.registry_key)

            return {
                "active_identities": count,
                "ram_usage_mb": round(info["used_memory"] / (1024 * 1024), 2),
                "ram_peak_mb": round(info["used_memory_peak"] / (1024 * 1024), 2),
                "status": "SOVEREIGN_ONLINE",
                "latency": "SUB_MS"
            }
        except Exception:
            return {"status": "MATRIX_OFFLINE", "active_identities": 0}

    # ============================================================================
    # 🗑️ INVALIDATE (Safe Clean)
    # ============================================================================
    def invalidate_encoding(self, uid: str) -> bool:
        try:
            uid = uid.upper()
            pipe = self.redis.pipeline()
            pipe.delete(self._key(uid))
            pipe.srem(self.registry_key, uid) # Remove from registry
            pipe.execute()
            return True
        except Exception:
            return False