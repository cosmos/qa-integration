import hashlib

# The hash we use is a 20-byte, uppercase truncated sha256.
# Ref: https://github.com/umee-network/umee/blob/959a1e4b93067db8b16fd1c241ab8f7c910931bc/x/oracle/types/hash.go#L23
def get_hash(exchange_rate, salt, valAddr):
    str = f'{exchange_rate}:{salt}:{valAddr}'
    encoded_string = str.encode()
    full_hash = hashlib.sha256(bytearray(encoded_string)).hexdigest()
    return full_hash[:40].upper()
