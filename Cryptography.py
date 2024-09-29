from random import shuffle
import argparse
class Cryptography():
    class Playfair():
        def __init__(self):
            pass
  
        def _keyShuffle(self):
            '''Shuffles the alphabet in preparation for appending to key'''
            alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
            alphabet = list(alphabet)
            shuffle(alphabet)
            mixed = ''.join(alphabet)
            return mixed

        def _playfairSquare(self, key):
            '''Takes a key and creates a new 25 character key '''
            key = key.upper()
            keynospace = []

            #remove spaces and J's
            for ch in key:
                if ch != ' ' and ch != 'J':
                    keynospace.append(ch)
                    if ch == 'J':
                        keynospace.append('I')
            key = ''.join(keynospace)

            key += self._keyShuffle()
            key = list(key)
            output = []
            square = ''
            for i in key:
                if i not in output and i != 'j' and i != '':
                    output.append(i)
            for l in output:
                square += ''.join(l)
            #print(square)
            return square
        
        def _encode_playfair_digrams(self, message):
            '''Splits the message into digraphs, handling repeated characters and odd lengths'''
            digraphs = []
            msgnospace = []
            message = message.upper()
            for ch in message:
                if ch != ' ' and ch != 'J':
                    msgnospace.append(ch)
                    if ch == 'J':
                        msgnospace.append('I')
            message = ''.join(msgnospace)
            i = 0
            while i < len(message):
                ch1 = message[i]
                if i + 1 < len(message):
                    ch2 = message[i + 1]
                    if ch1 == ch2:
                        digraphs.append(ch1 + 'Q')
                        i += 1
                    else:
                        digraphs.append(ch1 + ch2)
                        i += 2
                else:
                    digraphs.append(ch1 + 'Q')
                    i += 1
            return ''.join(digraphs)
        
        def playfairEncrypt(self, message, key):
            '''Encrypts the plaintext using the Playfair cipher'''
            key = self._playfairSquare(key)
            print('Key:', '\n', key)
            print('Message:')
            
            message = message.upper()
            ciphertext = []

            message = self._encode_playfair_digrams(message)
            #print(f"Digraphs: {message}")

            for i in range(0, len(message), 2):
                ch1 = message[i]
                ch2 = message[i + 1]

                key1 = key.find(ch1)
                key2 = key.find(ch2)

                #are values present in the key?
                if key1 == -1 or key2 == -1:
                    raise ValueError(f"Character {ch1} or {ch2} not found in key square.")

                row1, col1 = divmod(key1, 5)
                row2, col2 = divmod(key2, 5)

                #print(f"Processing digraph: {ch1}{ch2}")
                #print(f"Positions - {ch1}: ({row1}, {col1}), {ch2}: ({row2}, {col2})")

                if row1 == row2:  #row
                    ciphertext.append(key[row1 * 5 + (col1 + 1) % 5])
                    ciphertext.append(key[row2 * 5 + (col2 + 1) % 5])
                    #print(f"Same row -> {ciphertext[-2]}{ciphertext[-1]}")
                elif col1 == col2:  #column
                    ciphertext.append(key[((row1 + 1) % 5) * 5 + col1])
                    ciphertext.append(key[((row2 + 1) % 5) * 5 + col2])
                    #print(f"Same column -> {ciphertext[-2]}{ciphertext[-1]}")
                else: #rectangle
                    ciphertext.append(key[row1 * 5 + col2])
                    ciphertext.append(key[row2 * 5 + col1])
                    #print(f"Rectangle swap -> {ciphertext[-2]}{ciphertext[-1]}")
            return ''.join(ciphertext)
        
        def playfairDecrypt(self, plaintext, key):
            '''Decrypts the ciphertext using the key'''
            key = self._playfairSquare(key)
            print('Message:')
            
            message = plaintext.upper()
            plaintext = []

            message = self._encode_playfair_digrams(message)
            #print(f"Digraphs: {message}")

            for i in range(0, len(message), 2):
                ch1 = message[i]
                ch2 = message[i + 1]

                key1 = key.find(ch1)
                key2 = key.find(ch2)

                #are values present in the key?
                if key1 == -1 or key2 == -1:
                    raise ValueError(f"Character {ch1} or {ch2} not found in key square.")

                row1, col1 = divmod(key1, 5)
                row2, col2 = divmod(key2, 5)

                #print(f"Processing digraph: {ch1}{ch2}")
                #print(f"Positions - {ch1}: ({row1}, {col1}), {ch2}: ({row2}, {col2})")

                if row1 == row2:  #row
                    plaintext.append(key[row1 * 5 + (col1 - 1) % 5])
                    plaintext.append(key[row2 * 5 + (col2 - 1) % 5])
                    #print(f"Same row -> {plaintext[-2]}{plaintext[-1]}")
                elif col1 == col2:  #column
                    plaintext.append(key[((row1 - 1) % 5) * 5 + col1])
                    plaintext.append(key[((row2 - 1) % 5) * 5 + col2])
                    #print(f"Same column -> {plaintext[-2]}{plaintext[-1]}")
                else: #rectangle
                    plaintext.append(key[row1 * 5 + col2])
                    plaintext.append(key[row2 * 5 + col1])
                    #print(f"Rectangle swap -> {plaintext[-2]}{plaintext[-1]}")
            return ''.join(plaintext)
        
    class CaesarShift():
        def __init__(self, key=13):
            self.key = key

        def caesarEncrypt(message, key=13):
            '''Encrypts a Caesar shift cipher'''
            alphabet = "abcdefghijklmnopqrstuvwxyz "
            ciphertext = []
            message = message.lower()

            for i in message:
                placeholder = alphabet.find(i)

                if placeholder != -1: #is it in the alphabet?
                    new_position = (placeholder + key) % len(alphabet)
                    ciphertext.append(alphabet[new_position])
                else:
                    ciphertext.append(i)

            ciphertext = ''.join(ciphertext)
            return ciphertext
        
        def caesarDecrypt(ciphertext, key=13):
            '''Decrypts a Caesar shifted cipher'''
            alphabet = "abcdefghijklmnopqrstuvwxyz "
            plaintext = []
            
            for char in ciphertext:
                placeholder = alphabet.find(char)
                if placeholder != -1:
                    new_position = (placeholder - key) % len(alphabet)
                    plaintext.append(alphabet[new_position])
                else:
                    plaintext.append(char)

            return ''.join(plaintext)
        
    class RailFence():
        def railEncrypt(message, railCount):
            '''Encryption using the rail fence cipher'''
            #grid formed by list of lists
            zigzag = [['\n' for column in range(len(message))] for rail in range(railCount)]
            direction = 1
            rail_index = 0 
            for character_index, character in enumerate(message):
                zigzag[rail_index][character_index] = character
                if rail_index == 0:
                    direction = 1
                elif rail_index == railCount - 1:
                    direction = -1
                
                rail_index += direction
            
            encrypted_message = ''.join([''.join(row) for row in zigzag])
            return encrypted_message.replace('\n', '')
    
        def railDecrypt(ciphertext, railCount):
            '''Decryption of a text enciphered with the Rail Fence cipher'''
            zigzag = [['\n' for column_index in range(len(ciphertext))] for rail in range(railCount)]
            direction = 1
            rail = 0        
            for char in range(len(ciphertext)):
                zigzag[rail][char] = 'x'
                if rail == 0:
                    direction = 1
                elif rail == railCount - 1:
                    direction = -1
                
                rail += direction

            secretChar = 0
            for rail in range(railCount):
                for column_index in range(len(ciphertext)):
                    if zigzag[rail][column_index] == 'x' and secretChar < len(ciphertext):
                        zigzag[rail][column_index] = ciphertext[secretChar]
                        secretChar += 1
            
            decrypted_message = []
            direction = 1
            rail = 0    
            for char in range(len(ciphertext)):
                decrypted_message.append(zigzag[rail][char])
                if rail == 0:
                    direction = 1
                elif rail == railCount - 1:
                    direction = -1     
                rail += direction
            
            return ''.join(decrypted_message) 

def main():
    cipher_program = Cryptography()

    #instantiate playfair to pass in self parameter
    Playfair = cipher_program.Playfair()

    parser = argparse.ArgumentParser(description="Encrypt or decrypt using Playfair, Caesar, or Rail ciphers")
    parser.add_argument('--playfairEncrypt', nargs=2, metavar=('TEXT', 'KEY'), 
                        type=str, help="Encrypt using playfair cipher with text and key. USAGE: 'text' 'key'")
    parser.add_argument('--playfairDecrypt', nargs=2, metavar=('TEXT', 'KEY'),
                        type=str, help="Decrypt using playfair cipher with text and key. USAGE: 'text' 'key'")
    
    parser.add_argument('--railEncrypt', nargs=2, metavar=('TEXT', 'RAILS'),
                        type=str, help="Encrypt using rail cipher with text and number of rails. USAGE: 'text' 3")
    parser.add_argument('--railDecrypt', nargs=2, metavar=('TEXT', 'RAILS'),
                        type=str, help="Decrypt using rail cipher with text and number of rails. USAGE: 'text' 3")
    
    parser.add_argument('--caesarEncrypt', nargs=2, metavar=('TEXT', 'KEY'),
                        type=str, help="Encrypt using substitution cipher with text and key. USAGE: 'text' 13")
    parser.add_argument('--caesarDecrypt', nargs=2, metavar=('TEXT', 'KEY'),
                        type=str, help="Decrypt using substitution cipher with text and key. USAGE: 'text' 13")   
    args = parser.parse_args()

    if args.playfairEncrypt:
        text, key = args.playfairEncrypt
        print(Playfair.playfairEncrypt(text, key)) 
    if args.playfairDecrypt:
        text, key = args.playfairDecrypt
        print(Playfair.playfairDecrypt(text, key))
    
    if args.caesarEncrypt:
        text, key = args.caesarEncrypt
        print(cipher_program.CaesarShift.caesarEncrypt(text, int(key)))
    if args.caesarDecrypt:
        text, key = args.caesarDecrypt
        print(cipher_program.CaesarShift.caesarDecrypt(text, int(key)))
    
    if args.railEncrypt:
        text, rails = args.railEncrypt
        print(cipher_program.RailFence.railEncrypt(text, int(rails)))
    if args.railDecrypt:
        text, rails = args.railDecrypt
        print(cipher_program.RailFence.railDecrypt(text, int(rails)))

if __name__ == "__main__":
    main()

        