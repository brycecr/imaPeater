#!/usr/bin/env python
import sys
import os
import email.parser
import email.utils

def eatFiles(dirname):
    emailNameMap = {}
    for dirpath, dirs, files in os.walk(dirname):
        for filename in files: #this is bs needs to be any file except a directory, I think??
            with open(os.path.join(dirpath, filename)) as infile:
                parser = email.parser.Parser()
                msg = parser.parse(infile) # handle error here
                print email.utils.parsedate(msg.get('date'))[0]
                addrFields = []
                addrFields.append(msg.get('to'))
                addrFields.append(msg.get('cc'))
                addrFields.append(msg.get('bcc'))
                for field in addrFields:
                    if field != None:
                        for addr in field.split(','):
                            print addr
                    #for i in msg.walk():
                        #print "NEW PART"
                        #print i
                    #print msg.get('to')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "I require a directory or file name as an argument"
        sys.exit(1)
    print "Eating your email files in directory", sys.argv[1] + "..."
    eatFiles(sys.argv[1])
    
