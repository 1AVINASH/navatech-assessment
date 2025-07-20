from bloom_filter2 import BloomFilter
import redis
import pickle

class BloomFilterService:
    def __init__(self):
        ...

    # Load or create Bloom filter
    def get(self, data):
        if not data:
            bloom = BloomFilter(max_elements=1_000_000, error_rate=0.01)
            return bloom
        return data
    
    def add(self, bloom_filter: BloomFilter, data: str):
        bloom_filter.add(data)
        return bloom_filter

    # Usage in your signup function
    def check_value(self, bloom_filter, email):
        if email in bloom_filter:
            # Might be a duplicate → you need to check DB to confirm
            return True, "Email already exists"
        else:
            return False, "Email accepted"

    def check_false_positive(self, stored_email, recvd_email):
        if recvd_email == stored_email:
            # Might be a duplicate → you need to check DB to confirm
            return False, "Email already exists"
        else:
            return True, "Email accepted"

        
