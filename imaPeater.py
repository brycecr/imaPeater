#!/usr/bin/env python
import sys
import os
import email.parser
import email.utils

emailNameMap = {}

# infolosing -- 
# takes in an (email, name) tuple
# and returns true if emailNameMap contains the email as a key with an existing
#     name value is longer than that in addr
#
# In other words, this function is meant to provide a heuristic-based
# (longer names are more informative) test for whether a proposed
# new address tuple is information losing or not.
#
# Note that this is necessary because dict.update() overwrites
# values for shared keys with the new values.
#
# Also returns true if addr is a list, which is just identified
# by testing if it has @lists. in it, which is derived from @lists.stanford.edu
#
# Also returns true if doemail.org appears in the address...
#
def infolosing(addr):
    if addr[0] in emailNameMap:
        if len(emailNameMap[addr[0]]) > len(addr[1]):
            return True
    if '@lists.' in addr[0]:
        return True
    if 'doemail.org' in addr[0]:
        return True
    return False


# eatfiles --
# walks the directory subtree with dirname as the root
# and opens all files therein, making the assumption they are
# email files.
def eatfiles(dirname, outfile):
    for dirpath, dirs, files in os.walk(dirname):
        for filename in files: #this is bs needs to be any file except a directory, I think??
            with open(os.path.join(dirpath, filename)) as infile:
                try:
                    parser = email.parser.Parser()
                    msg = parser.parse(infile, True)

                    # skip things that were prior to 2006
                    year = email.utils.parsedate(msg.get('date'))[0]
                    if year < 2006:
                        continue

                    # include all address fields...maybe too many? Depends
                    # on how there are used in real life
                    addrFields = []
                    tos = msg.get_all('to',[])
                    fos = msg.get_all('from',[])
                    ccs = msg.get_all('cc',[])
                    bccs = msg.get_all('bcc',[])
                    resenttos = msg.get_all('resent-to',[])
                    resentfos = msg.get_all('resent-from',[])
                    resentccs = msg.get_all('resent-cc',[])
                    resentbccs = msg.get_all('resent-bcc',[])

                    # generate tuples from header fields
                    newaddrs = email.utils.getaddresses(tos+fos+ccs+bccs+resenttos+resentfos+resentccs+resentbccs)

                    #switch tuple order
                    newaddrs = [(t[1], t[0]) for t in newaddrs]

                    # filter out addresses that are lists, doemail, or already know longer names
                    newaddrs = [addr for addr in newaddrs if not infolosing(addr)]

                    # merge
                    emailNameMap.update(newaddrs)
                except:
                    # if there was a non-email file sitting there, try to ekip it and continue
                    print 'Problem parsing', dirpath + filename + '; Skipping file...'
                    continue
    of = open(outfile, 'w')
    for key, value in emailNameMap.iteritems():
        of.write(value + ' , ' + key + '\n')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "I require a directory or file name"
        sys.exit(1)
    print "Eating your email files in directory", sys.argv[1] + "..."
    eatfiles(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else 'emailList.txt')
    
