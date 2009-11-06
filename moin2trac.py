#!/usr/bin/python
usage = '''Convert a moinmoin wiki to a trac wiki or multiple trac wikis
usage:

    moin2trac.py <moindir> <tracprojectdir> [<wikimapfile>]

    <moindir> is the original moinmoin directory.
    <tracprojectdir> is the target trac project directory
    <wikimapfile>  A mapping of page name to trac wikis
    
   Optionally you may also include <wikimapfile> which
   is useful if you would like to split your wiki into
   a trac multi-project or if you would prefer to map
   only some of you pages into your wiki.

   The syntax is as follow 
   MoinPageName   <tracprojectdir>

   If a <wikimapfile> is specified then only
   those pages in the map file will be transfered
'''

import sys,os
import re
from trac.attachment import Attachment
# Work for 0.10.3 and 0.11
try:
    from  trac.scripts.admin import TracAdmin
except:
    from trac.admin.console import TracAdmin


def recodeName (filename):
    return re.sub (r'\(([\dabcdefABCDEF]+)\)',
                   lambda m: m.group(1).decode('hex'),
                   filename)

def convert(moindir, tracdir = None, mapfile = None):
    pagemap = None
    if mapfile:
        pagemap = {}
        for line in open(mapfile):
            if line[0] == '#': continue
            (page, wikidir) = line.split()
            pagemap[page] = wikidir

    pages = os.listdir(moindir)
    for page in pages:
        wikidir = tracdir
        if pagemap:
            if not pagemap.has_key(page): continue
            wikidir = pagemap[page]

        admin  = TracAdmin()
        admin.env_set (wikidir)
        revdir = moindir + '/' + page + '/revisions'
        if os.access(revdir, os.F_OK):
            revisions = os.listdir(revdir)
            for rev in revisions:
                cmd='wiki import %s %s' % ( recodeName(page),  revdir +'/'+rev)
                print cmd, "->", wikidir
                admin.onecmd('wiki remove %s' % recodeName(page))
                admin.onecmd(cmd)
        # Process attachments
        attdir = moindir + '/' + page + '/attachments'
        if os.access(attdir, os.F_OK):
            attachments = os.listdir(attdir)
            for att in attachments:
                attachment = Attachment(admin.env_open(), 'wiki', page)
                size = os.stat(attdir + '/'+ att)[6]
                print "attaching " + att + ' = ' + str(size)
                attfile = open (attdir + '/'+ att)
                attachment.insert (att, attfile, size)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print usage
        sys.exit()
    args = sys.argv[1:]
    convert(*args)

