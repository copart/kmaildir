# kmaildir

This is a small class that extends the standard library Maildir (mailbox) object to support the way Kmail supports Maildir.  It is a drop in replacement for Maildir.

## License
Apache License 2.0, see "COPYING" for details


## Sources
* [https://docs.python.org/2/library/mailbox.html](Python Mailbox)


## Usage

  #Basically use exactly as you would the standard maildir object

  import kmaildir

  mbox = kmaildir.Kmaildir('/home/me/vmail', factory=None, create=True)

  for folder in mbox.list_folders():
    print ( folder )
