safeFilenameChars = lambda: 'abcdefghijklmnopqrstuvwxyz1234567890-_ ,'
safeFilename = lambda title: ''.join(c for c in title.casefold() if c in safeFilenameChars())