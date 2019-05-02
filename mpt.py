#!/usr/bin/env python3

import sha3
import rlp
import pprint

HASH_LEN = 32    # 32-byte, 256-bit
HEXADEC  = 16

DEBUG_MODE = True
DEBUG_MODE2 = True
DEBUG_MODE3 = True


def remove(dict_, segment):
        """
        Removes initial key segments from the keys of dictionaries.
        """

        for key in dict_.keys():
                print('\n( Branch Index:', key[0], ')') if DEBUG_MODE == True else 1
                break

        return {k[len(segment):] : v for k, v in dict_.items()}


def select(dict_, segment):
        """
        Selects dictionary elements with given initial key segments.
        """

        return {k : v for k, v in dict_.items() if k.startswith(segment)}

def find_common_segment(dict_):
        """
        Finds common initial segments in the keys of dictionaries.
        """

        segment = ""
        for i in range(min([len(e) for e in dict_.keys()])):
                if len({e[i] for e in dict_.keys()}) > 1:
                        break
                segment += list(dict_.keys())[0][i]

        return segment


def patricia_subtree(dict_):
        """
        Creates Patricia tries that begin with regular nodes.
        """

        pt = (HEXADEC + 1) * [None]

        if "" in dict_:
                pt[-1] = dict_[""]
                del(dict_[""])

        for e in {e[0] for e in dict_.keys()}:
                #print('Select =', select(dict_, e)) if DEBUG_MODE == True else 1

                pt[int(e, HEXADEC)] = patricia(remove(select(dict_, e), e))

        return pt


def patricia(dict_):
        """
        Creates Patricia tries from dictionaries.
        """

        print('# Dict =', dict_) if DEBUG_MODE == True else 1

        segment = find_common_segment(dict_)
        #print('# Common segment =', segment) if DEBUG_MODE == True else 1

        if   len(dict_) == 1:
                # Leaf Node, i.e. last patricia tree...
                print('\n## Leaf Node ##') if DEBUG_MODE == True else 1

                pt = list(dict_.items())[0]


                if len(pt[0]) % 2 == 0:
                        print('#### prefix = 20 ####') if DEBUG_MODE == True else 1
                        pt = (bytes.fromhex("20" + pt[0]), pt[1])
                else:
                        print('#### prefix = 3 ####') if DEBUG_MODE == True else 1
                        pt = (bytes.fromhex("3"  + pt[0]), pt[1])

                for e in pt:
                        pass
                        #pt_hex = [binascii.hexlify(bytearray(e))]

                print('#### key-end =', segment, ' -> leaf =', dict_, ' ####') if DEBUG_MODE == True else 1
                print('#### pt =', pt, ' ####') if DEBUG_MODE == True else 1
                print('') if DEBUG_MODE == True else 1


        elif segment:
                # Subtree
                print('\n## (Shared) Extension + Branch Node ##') if DEBUG_MODE == True else 1

                dict_ = remove(dict_, segment)

                if len(segment) % 2 == 0:
                        print('#### prefix = 00 ####') if DEBUG_MODE == True else 1
                        pt = [bytes.fromhex("00" + segment), patricia_subtree(dict_)]
                else:
                        print('#### prefix = 1 ####') if DEBUG_MODE == True else 1
                        pt = [bytes.fromhex("1"  + segment), patricia_subtree(dict_)]

                for e in pt:
                        pass
                        #pt_hex = [binascii.hexlify(bytearray(e))]

                print('#### shared nibble = ', segment, ' -> branch =', dict_, ' ####') if DEBUG_MODE == True else 1
                print('#### pt =', pt, ' ####') if DEBUG_MODE == True else 1
                print('') if DEBUG_MODE == True else 1

        else:
                # Subtree
                print('\n## (Unshared) Branch Node ##\n') if DEBUG_MODE == True else 1

                pt = patricia_subtree(dict_)

        return pt



def merkle(element):
        """
        Encodes Patricia trie elements using Keccak 256 hashes and RLP.
        """

        if not element:    # None
                merkle_ = b""
                print('## ("") merkle =', merkle_, '') if DEBUG_MODE2 == True else 1

        elif isinstance(element, str):
                merkle_ = bytes.fromhex(element)
                print('## (str) merkle =', merkle_, '') if DEBUG_MODE2 == True else 1

        elif isinstance(element, bytes):
                merkle_ = element
                print('## (bytes) merkle =', merkle_, '') if DEBUG_MODE2 == True else 1

        else: # if element = list
                merkle_ = [merkle(e) for e in element]
                print('\n## (List) merkle =', merkle_, '') if DEBUG_MODE2 == True else 1

                rlp_ = rlp.encode(merkle_)
                print('merkle =', merkle_, '') if DEBUG_MODE3 == True else 1
                print('rlp(merkle) =', rlp_, '') if DEBUG_MODE3 == True else 1
                print('len(rlp) =', len(rlp_), '') if DEBUG_MODE3 == True else 1
                if len(rlp_) >= HASH_LEN:
                        print('####Over-length####') if DEBUG_MODE3 == True else 1
                        merkle_ = sha3.keccak_256(rlp_).digest()
                        print('####Hashed merkle =', merkle_, '####') if DEBUG_MODE3 == True else 1

                # Q: Store merkle_ or store rlp_?

        return merkle_

def merkle_patricia(dict_):
        """
        Creates Merkle Patricia tries from dictionaries.
        """

        return [merkle(e) for e in patricia(dict_)]

def info(dict_):
        """
        Prints info about the Merkle Patricia tries created from dictionaries.
        """

        print("\n(1) Patricia trie:\n")
        trie_ = patricia(dict_)

        print('\nPatricia trie = ', end='')
        print(trie_)
        #pprint.pprint(trie_)
        print("------------------------------------------------------------------------")

        print("\n(2) Merkle Patricia trie:\n")
        merkle_ = merkle_patricia(dict_)

        print('\nMerkle Patricia trie = ', end='')
        print(merkle_)
        #pprint.pprint(merkle_)
        print("------------------------------------------------------------------------")

        print("\n(3) Hash of the RLP encoding of the Merkle Patricia trie:\n")

        print('\n## (Root) merkle =', merkle_, '') if DEBUG_MODE2 == True else 1
        rlp_ = rlp.encode(merkle_)
        print('rlp(merkle) =', rlp_, '') if DEBUG_MODE3 == True else 1

        print('\nRoot Hash =', sha3.keccak_256(rlp_).hexdigest())
        print("------------------------------------------------------------------------")
