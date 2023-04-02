enc_flag = [91,241,101,166,85,192,87,188,110,164,99,152,98,252,34,152,117,164,99,162,107]
flag_len = len(enc_flag)
key_len = 4
found = False

for k1 in range(256):
    for k2 in range(256):
        for k3 in range(256):
            for k4 in range(256):
                key = [k1, k2, k3, k4]
                flag = ""
                for i in range(flag_len):
                    c = chr(enc_flag[i] ^ key[i % key_len])
                    flag += c
                print(flag)
                if flag.startswith("RS{") and flag.endswith("}"):
                    found = True
                    print("Found key:", key)
                    print("Flag:", flag)
                    break
            if found:
                break
        if found:
            break
    if found:
        break