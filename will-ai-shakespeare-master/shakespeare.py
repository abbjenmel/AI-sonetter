verbose = True
if verbose: print("Initializing...")
import curses
from curses.ascii import isdigit
import json
import nltk
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize
import random
from random import randint
import math
import approxSyls
import pronouncing
import multiprocessing
import time
import cPickle


d = cmudict.dict()
PUNCTS = [',','.','?',u"'",':',';','--','!',"''"]
bannedList = ["a",
              "'t", 
              "t",
              "au",
              "an",
              "niggard",
              u'ai',
              u'ais',
              "ais",
              u"ais",
              u'[',
              u']',
              u'c',
              u"c",
              "c",
              u'"',
              u'(paren',
              u'th',
              u"'",
              u'car',
              u'"quote',
              u"'i",
              "'i",
              u'videotex',
              u"'",
              u'.dot'
             ]
tagDict = {}
sonnets = "rekt"
"""
Load and parse sonnets from a file and return the structure
@param {string} file_name The file location (complete path)
@return {dictionary[]}
"""
def load_sonnets(file_name):
    sonnets = None
    with open(file_name, "r") as sonnetFile:
        sonnets = json.load(sonnetFile)

        def get_tags_from_sonnet(sonnet):
            return map(lambda line: nltk.pos_tag(word_tokenize(line)), sonnet)

        def add_tags_to_sonnet(sonnet_info):
            sonnet_info["tags"] = get_tags_from_sonnet(sonnet_info["sonnet"])
            return sonnet_info

        return map(add_tags_to_sonnet, sonnets)

if verbose: print("Analyzing Shakespeare's works...")
sonnets = load_sonnets("./sonnets.json")


"""
Builds the tag dictionary from multiple tag lists/lines given by load_sonnets
"""
def buildTagDict(sonnets):
    #gets a sonnet line
    for sonnet in sonnets:
        for taglist in sonnet["tags"]:
            addTagsToDict(taglist)


"""
Iterate through a single-line list of word/tag pairs and add them
to the tag dictionary
"""
def addTagsToDict(tagList):
    global tagDict
    for word,tag in tagList:
        word = word.lower()
        if word not in bannedList:
            if tagDict == {} or tagDict is None:
                tagDict[tag] = [word]
            elif tag in tagDict:
                if tag not in tagDict:
                    tagDict[tag] = [word]
                elif word not in tagDict[tag]:
                    tagDict[tag].append(word)
            else:
                tagDict[tag] = [word]
    return tagDict

if verbose: print ("building tagdict")
#buildTagDict(sonnets)
if verbose: print ("finished building")
if verbose: print (tagDict)

"""
Return the rank of a CMUdict word part.
Returns -1 if the word part does not have a rank
"""
def toRank(part):
    if part[-1].isdigit():
        return int(part[-1])
    return -1

"""
Convert a word into a list of syllable stress ranks
"""
def wordToSylRanks(word):
    try:
        return [toRank(part) for part in (d[word.lower()][0]) if toRank(part) != -1]
    except:
        return [1] * approxSyls.apSyls(word)

"""
Convert a list of words into a monolithic list of syllable stress ranks
"""
def stanzaToSylRanks(stanza):
    ranks = []
    for word in stanza:
        ranks = ranks + wordToSylRanks(word)
    return ranks

"""
Check to see if a list of words follows iambic pentameter and has a rhymable last word
"""
def isIP(stanza):
    ranks = stanzaToSylRanks(stanza)
    if len(ranks) != 10:
        return False
    for r in [ranks[i] for i in [1,3,5,7,9]]:
        if r <= 0:
            return False
    last = getLast(stanza)
    rhymes = [x for x in pronouncing.rhymes(last) if wordToSylRanks(x) == wordToSylRanks(last)]
    if len([rhyme for rhyme in rhymes if rhyme not in bannedList]) == 0:
        return False
    if stanza[0][0] == u"'":
        return False
    return True

"""
Takes a list of tags and searches the tag dictionary for appropriate replacements. Returns a new array of the same length containing the replaced sentence
"""
def replaceWordTags(tags):
    #Assuming each word in words is an nltk tag as a string. ie. ['UU','WC','CC']
    global tagDict
    newLine = []
    for tag in tags:
        if tag in tagDict:
            replacement = random.choice(tagDict[tag])
            newLine.append(replacement)
        else:
            newLine.append("NOTAG")
    return newLine

def chooseRhyme(word, rhyme):
    rhymes = []
    #Hacky fix for library bug. Wait, what am I saying? This whole project is hacky.
    while rhymes == []:
        rhymes = [r for r in pronouncing.rhymes(rhyme) if r not in bannedList]
    syls = wordToSylRanks(word)
    for r in rhymes:
        if wordToSylRanks(r) == syls:
            return r

    return rhymes[randint(0,len(rhymes) - 1)]

def makeRhyme(line, rhyme):
    if rhyme == "":
        return line
    else:
        chosenRhyme = chooseRhyme(getLast(line),rhyme)
        if line[-1] in PUNCTS:
            line[-2] = chosenRhyme
        else:
            line[-1] = chosenRhyme
        return line

"""
Generate a line in the meter
"""
def getIPLine(tags, rhyme):
    newLine = replaceWordTags(tags)
    noPunc = [x for x in newLine if x not in PUNCTS]
    while not isIP(noPunc):
        newLine = replaceWordTags(tags)
        noPunc = [x for x in newLine if x not in PUNCTS]
    newLine = makeRhyme(newLine, rhyme)
    return newLine

"""
Convert a list of words to a list of tags
"""
def toTags(line):
    return [x[1] for x in nltk.pos_tag(line)]

"""
Grab a random sonnet's tag set from the .json
"""
def getRandSonnetTags():
    return sonnets[randint(0, len(sonnets) - 1)]["tags"]

"""
Grab a random line from a sonnet
"""
def getRandSonnetLine(sonnet):
    return sonnet[randint(0, len(sonnet) - 1)]

"""
Generate a random sonnet structure of word tags
"""
def makeRandomSonnetStructure():
    sonnetStruct = []

    # For the first 13 lines, pick a correspondingly-indexed line from a random sonnet
    for i in range(0,14):
        randSonnet = getRandSonnetTags()
        line = []
        try:
            line = randSonnet[i]
        except:
            pass
        sonnetStruct.append([x[1] for x in line])

    return sonnetStruct

def getLast(line):
    last = line[-1]
    if last in PUNCTS:
        last = line[-2]
    return last

def createProtoSonnet():
    global tagDict
    if tagDict == {} or tagDict is None:
        buildTagDict(sonnets)
    lines = makeRandomSonnetStructure()
    protoSonnet = []

    line0  = getIPLine(lines[0],  "")             #a
    line1  = getIPLine(lines[1],  "")             #b
    line2  = getIPLine(lines[2],  getLast(line0)) #a
    line3  = getIPLine(lines[3],  getLast(line1)) #b
    line4  = getIPLine(lines[4],  "")             #c
    line5  = getIPLine(lines[5],  "")             #d
    line6  = getIPLine(lines[6],  getLast(line4)) #c
    line7  = getIPLine(lines[7],  getLast(line5)) #d
    line8  = getIPLine(lines[8],  "")             #e
    line9  = getIPLine(lines[9],  "")             #f
    line10 = getIPLine(lines[10], getLast(line8)) #e
    line11 = getIPLine(lines[11], getLast(line9)) #f
    line12 = getIPLine(lines[12], "")             #g
    line13 = getIPLine(lines[13], getLast(line12))#g

    protoSonnet.append(line0)
    protoSonnet.append(line1)
    protoSonnet.append(line2)
    protoSonnet.append(line3)
    protoSonnet.append(line4)
    protoSonnet.append(line5)
    protoSonnet.append(line6)
    protoSonnet.append(line7)
    protoSonnet.append(line8)
    protoSonnet.append(line9)
    protoSonnet.append(line10)
    protoSonnet.append(line11)
    protoSonnet.append(line12)
    protoSonnet.append(line13)

    return protoSonnet

"""
Takes a list of words and punctuation and returns a nicely formatted English sentence
"""
def wordListToSentence(wordList):
    sentence = ""
    for i in range(0,len(wordList) - 1):
        sentence = sentence + wordList[i]
        if wordList[i+1] not in PUNCTS:
            sentence = sentence + " "
    sentence = sentence + wordList[-1]
    return sentence

def protoSonnetToSonnet(protoSonnet):
    for outer in protoSonnet:
        outer[0] = outer[0].capitalize()
        for i in range(len(outer)):
            if outer[i] == u"i":
                outer[i] = u"I"

    for line in protoSonnet:
        for i in range(0, len(line)):

            if line[i] == u"''tis":
                line[i] = u"'tis"

            if line[i] == u"'i":
                line[i] = u'in'
            
            if line[i-1] in [u'.', u'!', u'?']:
                line[i] = line[i].title()


    sonneto = []
    for line in protoSonnet:
        sonneto.append(wordListToSentence(line))

    pretty = ""
    for line in sonneto:
        pretty += line + '\n'


    c = 0
    while c < len(pretty):

        if pretty[c-1:c+1] == u" '":
            try:
                test = pretty[c:c+4]
                if u" " in test:
                    pretty = pretty[:c-1]+pretty[c:]
            except:
                pass

        c += 1

    return pretty


def generateSonnet():
    sonnet = (protoSonnetToSonnet(createProtoSonnet()))
    print("hej")
    f= open("shakespearesonnets.txt","w+")
    print("hej2")
    print(sonnet)
    print("hej3")
    f.write(sonnet)
    print("hej4")
    f.close()


def createPickleTagDict():
    global tagDict, sonnets

    if verbose: print("Analyzing Shakespeare's works...")
    sonnets = load_sonnets("./sonnets.json")
    buildTagDict(sonnets)
    with open('pickleTagDict.pck','wb') as handle:
        cPickle.dump(tagDict,handle, protocol=cPickle.HIGHEST_PROTOCOL)

def readPickleTagDict():
    global tagDict
    with open('pickleTagDict.pck','rb') as handle:
        tagDict = cPickle.load(handle)

def worker():
    """thread worker function"""
    print("hej555")
    print 'Worker:'
    return

def runGenerator():
    generateSonnet()
    # p = multiprocessing.Process(target=generateSonnet)
    # print("hej3")
    # p.start()
    # print("hej4")
    # p.join(5)
    # print("hej6")
    # if p.is_alive():
    #     print("hej77")
    #     if verbose: print("Trying a different sonnet structure...\n")
        # p.terminate()
        # p.join()
    ##runGenerator()

    return
print("hej2")
if verbose: print("reading pickle dict")
readPickleTagDict()
#print tagDict
#print sonnets

if verbose: print("Generating sonnet...\n")
print("hej")
#while True:
runGenerator()
