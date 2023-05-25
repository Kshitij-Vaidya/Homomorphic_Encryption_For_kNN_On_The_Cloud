For RSA.py, written below is a sample of the object creation and passing of messages to the RSA class fo encryption and decryption.

test1 = RSA(k=1024)
message = b"Hello"
test1.get_public_key()
encrypted_message = test1.encrypt(message)
print(f"Message: {message}")
print(f"Encrypted Message: {encrypted_message}")
decrypted_message = test1.decrypt(encrypted_message)
print(f"Decrypted Message: {decrypted_message}")


For ElGamal.py, written below is a sample of the object and examples of arguments to be passed to the class. The primes passed and arguments are only as examples, any suitable values can be passed provided they satisfy the conditions necessary for proper encryption and decryption

test1 = ElGamal(6059056325654647085094673182820944702832808469246997590718614195302008976987677315330071892238115498233312708495024254444096787664043222683347160040706719286459263151857138107380333342113325579387780454681519176118730887918867537162514761997437249443, 7987903360290893870380841504510894449635092976012306005418780150883535078584661327124984048104946827664497045936791187482354329085853313906411064846262914819364089011651321400398782595157593889738511521280352222376627915193982566811045451019495202587)
m = b"5"
print(f"Message: {m}")
e_m = test1.encrypt(m)
print(f"Encrypted message: {e_m}")
d_m = test1.decrypt(e_m)
print(f"Decrypted message: {d_m}")


For Paillier.py, written below is an example of the object to be passed along with sample arguments. The value of k should be compatible with the length of the message

test = Paillier(k=32)
n, g = test.get_public_key()
message = b"Hello"
print(message)
encrypted = test.encrypt(message)
print(encrypted)
decrypted = test.decrypt(encrypted)
print(decrypted)
