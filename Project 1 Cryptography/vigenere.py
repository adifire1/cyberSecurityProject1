#!/usr/bin/python3
#!/usr/bin/python3
import sys
from collections import Counter

#taken from Wikipedia
letter_freqs = {
    'A': 0.08167,
    'B': 0.01492,
    'C': 0.02782,
    'D': 0.04253,
    'E': 0.12702,
    'F': 0.02228,
    'G': 0.02015,
    'H': 0.06094,
    'I': 0.06966,
    'J': 0.00153,
    'K': 0.00772,
    'L': 0.04025,
    'M': 0.02406,
    'N': 0.06749,
    'O': 0.07507,
    'P': 0.01929,
    'Q': 0.00095,
    'R': 0.05987,
    'S': 0.06327,
    'T': 0.09056,
    'U': 0.02758,
    'V': 0.00978,
    'W': 0.02361,
    'X': 0.00150,
    'Y': 0.01974,
    'Z': 0.00074
}

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def pop_var(s):
    """Calculate the population variance of letter frequencies in given string."""
    freqs = Counter(s)
    mean = sum(float(v)/len(s) for v in freqs.values())/len(freqs)  
    return sum((float(freqs[c])/len(s)-mean)**2 for c in freqs)/len(freqs)

#https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC-Len.html
def getKeyLength(ciphertext):
    maxKeyLengthGuess = 10
    meanTable = []
    
    for guessLength in range(maxKeyLengthGuess):
        variance = 0.0
        mean = 0.0
        for i in range(guessLength):
            substring=""
            for j in range(0, len(ciphertext[i:]), guessLength):
                substring += ciphertext[i+j]
            variance += pop_var(substring)
        if(guessLength != 0):
            mean = variance/guessLength
        meanTable.append(mean)
        
    bestGuess = meanTable.index(sorted(meanTable, reverse = True)[0])
    
    return bestGuess

# refrence: https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-Recover.html
def frquencyAnalysis(sequence):
    allWeights = [0] * 26
    
    for i in range(26):
        weight = 0.0
        v = [0] * 26
        
        substringShift = [chr(((ord(sequence[j])-65-i)%26)+65) for j in range(len(sequence))]
        # count the number of letters
        for k in substringShift:
            v[ord(k) - ord('A')] += 1
        # get the frequency percentages
        for j in range(26):
            v[j] *= (1.0/float(len(sequence)))
        # compare to the english frequencies
        for key in letter_freqs:
           weight+=((v[ord(key) - ord('A')] - float(letter_freqs.get(key)))**2)/float(letter_freqs.get(key))
           
        allWeights[i] = weight
        
    shift = allWeights.index(min(allWeights))
        
    # return the letter
    return chr(shift+65)

def getKey(ciphertext, keyLength):
	key = ''

	# Calculate letter frequency table for each letter of the key
	for i in range(keyLength):
		substring=""
		# breaks the ciphertext into substrings
		for j in range(0,len(ciphertext[i:]), keyLength):
			substring+=ciphertext[i+j]
		key+=frquencyAnalysis(substring)

	return key


if __name__ == "__main__":
    # Read ciphertext from stdin
    # Ignore line breaks and spaces, convert to all upper case
    ccipher = sys.stdin.readline().rstrip()

    #################################################################
    # Your code to determine the key and decrypt the ciphertext here
    key = getKeyLength(ccipher)
    print(getKey(ccipher, key))