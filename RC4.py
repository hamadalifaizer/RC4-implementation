import codecs

MOD = 256


def KSA(key):
    key_length = len(key)
    S = list(range(MOD)) 
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]

    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % MOD]
        yield K


def get_keystream(key):
    #  Gets encryption key to get the keystream using PRGA

    S = KSA(key)
    return PRGA(S)


def encrypt_text(key, text):
    key = [ord(c) for c in key]
    keystream = get_keystream(key)

    res = []
    for c in text:
        val = ("%02X" % (c ^ next(keystream)))  
        res.append(val)
    return ''.join(res)


def encrypt(key, plaintext):
    ''' key - key used to encrtpt plaintext a hex string
        plaintext - plaintext string to encrpyt
    '''
    plaintext = [ord(c) for c in plaintext]
    return encrypt_text(key, plaintext)


def decrypt(key, ciphertext):
    ''' key - key used to encrtpt plaintext a hex string
        ciphertext - plaintext encoded into a hex
    '''
    ciphertext = codecs.decode(ciphertext, 'hex_codec', errors='strict')
    res = encrypt_text(key, ciphertext)
    return codecs.decode(res, 'hex_codec').decode('utf-8')



def main():
    Choice = input('Would you like to encrypt[E] or decrypt[D]: ')

    if (Choice == 'E'):
        key = input('enter key here: ')  
        plaintext = input('enter plaintext to encrypt here: ') 
        ciphertext = encrypt(key, plaintext)
        print('ciphertext:', ciphertext)

    elif (Choice == 'D'):
        ciphertext = input('enter ciphertext to decrypt here: ')
        key = input('enter key here: ')
        decrypted = decrypt(key, ciphertext)
        print('decrypted:', decrypted)

    else:
        print('invaid input')

if __name__ == '__main__':
    main()