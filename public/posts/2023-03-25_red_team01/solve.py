flag_len = 21
enc_flag = [91, 241, 101, 166, 85, 192, 87, 188, 110, 164, 99, 152, 98, 252, 34, 152, 117, 164, 99, 162, 107]
key_len = 4
enc_flag = "5bf165a655c057bc6ea4639862fc229875a463a26b"
# Brute force the key by looping through all possible values
for i in range(10):
    for j in range(10):
        for k in range(10):
            for l in range(10):
                key = [i, j, k, l]
                decrypted_flag = ""
                for idx, c in enumerate(enc_flag):
                    decrypted_flag += (int(c) ^ key[idx % key_len])
                    print(decrypted_flag)
