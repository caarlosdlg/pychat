def calcular_crc(data, polynomial):

    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
    return crc

def verify_crc(data, polynomial, expected_crc):

    crc = calcular_crc(data, polynomial)
    return crc == expected_crc