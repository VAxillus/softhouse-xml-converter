#!/usr/bin/env python3
import sys

tags = {'P': [['<firstname>', '</firstname>'], ['<lastname>', '</lastname>']],
        'T': [['<mobile>', '</mobile>'], ['<home>', '</home>']],
        'A': [['<street>', '</street>'], ['<town>', '</town>'], ['<zipcode>', '</zipcode>']],
        'F': [['<name>', '</name>'], ['<born>', '</born>']]}

scopedTags = {'P': ['<person>', '</person>'],
             'T': ['<phone>', '</phone>'],
             'A': ['<address>', '</address>'],
             'F': ['<family>', '</family>']}

scopeLevel = {'P': ['P'],
              'T': None,
              'A': None,
              'F': ['P', 'F']}

scopeStack = []

def encapsulateFieldWithXMLTags(field, xml):
    return xml[0] + field + xml[1]

def encapsulateArrayWithXMLTags(arr, xml):
    return [xml[0]] + arr + [xml[1]]

def openXMLTag(arr, xml):
    return [xml[0]] + arr

def closeXMLTag(arr, xml):
    return [xml[1]] + arr

def closePreviousScope(xml, key, xmlToPrepend=None):
    if xmlToPrepend == None:
        xmlToPrepend = []

    for previousScope in scopeLevel[scopeStack[-1]]:
        if previousScope == key and scopeStack:
            xmlToPrepend.append(scopedTags[scopeStack[-1]][1])
            scopeStack.pop()
            if scopeStack and previousScope in scopeLevel[scopeStack[-1]]:
                closePreviousScope(xml, key, xmlToPrepend)

    return xmlToPrepend + xml

def createXMLTags(line):
    key = line[0]
    xml = list(map(encapsulateFieldWithXMLTags, line[1:], tags[key]))

    if scopeLevel[key] == None:
        xml = encapsulateArrayWithXMLTags(xml, scopedTags[key])
    else:
        xml = openXMLTag(xml, scopedTags[key])
        if scopeStack:
            xml = closePreviousScope(xml, key)
        scopeStack.append(key)

    return xml

def main(argv):
    data = [line.rstrip('\n').split('|') for line in open(argv[0])]
    xml = list(map(createXMLTags, data))
    while scopeStack:
        xml[-1].append(scopedTags[scopeStack.pop()][1])

    indentation = 4
    spaces = ' ' * indentation

    with open(argv[1], 'w') as file:
        file.write('<people>\n')
        for lines in xml:
            for tag in lines:
                if tag[1] == '/':
                    spaces = spaces[indentation:]
                file.writelines(spaces + '%s\n' % tag)
                if tag.find('/') == -1:
                    spaces += ' ' * indentation
        file.write('</people>\n')
    file.close()

if __name__ == "__main__":
    main(sys.argv[1:])
