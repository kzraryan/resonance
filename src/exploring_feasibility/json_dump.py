import json

js = {"collections": {"AI-Embeddings": {"vectors": {"size": 768, "distance": "Cosine", "hnsw_config": "null", "quantization_config": "null", "on_disk": "null", "datatype": "null", "multivector_config": "null"}, "shard_number": "null", "sharding_method": "null", "replication_factor": "null", "write_consistency_factor": "null", "on_disk_payload": "null", "hnsw_config": "null", "wal_config": "null", "optimizers_config": "null", "init_from": "null", "quantization_config": "null", "sparse_vectors": "null", "strict_mode_config": "null"}}, "aliases": {}}

print(json.dumps(js, indent=4))