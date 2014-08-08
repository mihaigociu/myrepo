import re

f = open('/home/mihai/work/luceafarul.txt')

def get_words(line):
    return [w for w in re.split(r'[,;.!?\'\ ]+', line.strip()) if w]

def get_sorted_anagram(word):
    l = list(word)
    l.sort()
    return ''.join(l)

def get_anagrams(f):
    anagrams = {}

    for line in f.readlines():
        line = line.lower()
        #replace weird chars
        line = line.replace('\xc5\x9f', 's')
        line = line.replace('\xc5\x9e', 's')
        line = line.replace('\xc3\xae', 'i')
        line = line.replace('\xc4\x83', 'a')
        line = line.replace('\xc3\xa2', 'a')
        line = line.replace('\xc5\xa3', 't')
        line = line.replace('\xc3\x8e', 'i')
        
        words = get_words(line)

        for word in words:
            sorted_anagram = get_sorted_anagram(word)
            
            if sorted_anagram not in anagrams:
                anagrams[sorted_anagram] = {
                    'counts': 1,
                    'words': set((word,))
                }
            else:
                anagrams[sorted_anagram]['counts'] += 1
                anagrams[sorted_anagram]['words'].add(word)

    return anagrams

anagrams = get_anagrams(f)
counted = [(anagram, anagrams[anagram]['counts']) for anagram in anagrams]
counted.sort(key=lambda x: x[1])
