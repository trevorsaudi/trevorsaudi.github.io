flag_len = 21
enc_flag = [91, 241, 101, 166, 85, 192, 87, 188, 110, 164, 99, 152, 98, 252, 34, 152, 117, 164, 99, 162, 107]
hex_flag = ''
for i in enc_flag:
    hex_flag += hex(i)[2:]
key_len = 4

# Brute force the key by looping through all possible values
for i in range(10):
    for j in range(10):
        for k in range(10):
            for l in range(10):
                key = [i, j, k, l]
                decrypted_flag = ""
                for idx, c in enumerate(hex_flag):
                    decrypted_flag += chr(int(c, 16) ^ key[idx % key_len])
                if len(decrypted_flag) == flag_len:
                    print("Decrypted flag:", decrypted_flag)
