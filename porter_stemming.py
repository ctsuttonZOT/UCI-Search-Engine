import sys

def porter_stem(word:str) -> str:
    #decide some rule real quick
    if len(word) < 3: #not big enough
        return word
    
    word = word.lower() # turn to lower 
    
    word = apply_plural_rules(word)
    #Keep applying rules until no change
    while True:
        new_word = apply_suffix_rules(word)
        if new_word is None:
            break
        word = new_word
        
    # take out'y' with 'i' if preceded by a vowel
    if word.endswith("y") and contains_vowel(word[:-1]):
        word = word[:-1] + "i"
        
    #remove the longer stuff
    word = remove_longer_suffix(word)
    
    #remove al, ible, etc.
    word = strip_context_suffix(word)

    # Final double consonant strip
    if ends_double_consonant(word) and not word.endswith(("l", "s", "z")):
        word = word[:-1]

    return word
    
    
def restore_e_if_needed(stem: str) -> str:
        if stem.endswith(("ng", "v", "p", "c", "t")) and len(stem) >= 3:
            return stem + "e"
        return stem

def apply_plural_rules(w: str) -> str:
        if w.endswith("sses"):
            return w[:-2]  #classes -> class
        elif w.endswith("ies"):
            return w[:-2]  # ponies -> poni
        elif w.endswith("ss") or w.endswith("us"):
            return w       # leave alone
        elif w.endswith("s"):
            return w[:-1]  #cats -> cat
        return w

#smaller suffixes, the simpleer ones to remove
def apply_suffix_rules(w: str) -> str:
    original = w

    if w.endswith("er"):
        temp = w[:-2]
        if measure_vc(temp) >= 1:
            if ends_double_consonant(temp): #check method description for info on this method
                temp = temp[:-1]
            temp = restore_e_if_needed(temp) #check method desscript
            w = temp

    elif w.endswith("ing"):
        temp = w[:-3]
        if measure_vc(temp) > 0:
            w = temp
            #check if stemming results in adding 'e' 
            if w.endswith(("at", "bl", "iz")): #cases needs e: such as hating, doubling
                w += "e"
            elif ends_double_consonant(w) and not w.endswith(("l", "s", "z")): #cases double letter: running, hopping, extra need to remove
                w = w[:-1]
            elif measure_vc(w) == 1 and ends_cvc(w): #cases: making, chasing, needs e
                w += "e"
            #else ends like missed, rizzed, belled, already valid after stemming

    elif w.endswith("ed"):
        temp = w[:-2]
        if measure_vc(temp) > 0:
            w = temp
            if w.endswith(("at", "bl", "iz")): #case: abled, cabled
                w += "e"
            elif ends_double_consonant(w) and not w.endswith(("l", "s", "z")):#cases: dropped, mopped, remove consonant
                w = w[:-1]
            elif measure_vc(w) == 1 and ends_cvc(w): #cases: maded, blamed, needs e aftet stemming
                w += "e"
            #else ends as blessed -> bless, killed -> kill

    return w if w != original else None
        
def measure_vc(word:str) -> int: #meant to count patterns of vowel-constant to check if over stemming
    #assume the word is passed in lower-cased already
    patterns = ''
    prev_type = '' #either V-vowel or C-consonant
    prev_char  = '' #for the prev char
    
    for curr_char in word:
        curr_type = "V" if is_vowel(curr_char, prev_char) else 'C'
        if curr_type != prev_type:
            patterns += curr_type #add the type to the pattern
            prev_type = curr_type
        prev_char = curr_char #go ahead 
    #print (patterns)
    return patterns.count("VC") #count the occurences

def ends_double_consonant(word:str): # soome special cases like chess etc
    if len(word) >= 2 and word[-1] == word[-2]:
        return word[-1] not in 'aeiou'
    return False

def contains_vowel(word:str)->bool:
    prev = ' '
    for c in word:
        if is_vowel(c,prev):
            return True
        prev = c
    return False

def is_vowel(char:str, prev:str) -> bool:
    vowels = "aeiou"
    if char in vowels:
        #print("TRUE")
        return True
    if char == "y":
        #print (prev and prev not in vowels)
        return prev and prev not in vowels
    #print("FALSE")
    return False

def ends_cvc(word: str) -> bool: #for specific rules - consonant-vowel-consonant 
    if len(word) < 3:
        return False
    
    c1, v, c2 = word[-3], word[-2], word[-1]
    
    if (not is_vowel(c1, word[-4] if len(word) > 3 else '')) and \
       is_vowel(v, c1) and \
       (not is_vowel(c2, v)) and \
       c2 not in "wxy":
        return True

    return False

def remove_longer_suffix(w: str) -> str:
    suffixes = {
        "icate": "ic", "ative": "", "alize": "al",
        "iciti": "ic", "ical": "ic", "ful": "", "ness": ""
    }
    for suf, rep in suffixes.items():
        if w.endswith(suf):
            stem = w[: -len(suf)]
            if measure_vc(stem) > 0:
                return stem + rep
    return w

def strip_context_suffix(w: str) ->str:
    suffixes = {"al", "ance", "ence", "er" "ic", "able", "ible", "ant", "ement", "ment", "ent",
                "ou", "ism", "ate", "iti", "ous", "ive", "ize", "ion"} #ion needs conditions
    
    for suf in suffixes: #check all poss endings
        if w.endswith(suf) :
            stem = w[:-len(suf)]
            
            if suf == "ion": #edge case
                if not stem.endswith(("s", "t")): #it does not apply, so no removing
                    continue  # skip this suffix

            if measure_vc(stem) > 1:
                return stem
    return w


def main():
    
    
    print(porter_stem(sys.argv[1]))

main()