# --------------------------------------------------------------------------
# PyHiew PEiD - A PEiD signature matching addin for Hiew
# (c) Elias Bachaalany
import sys, re, os, zlib, pickle
import configparser
import traceback
import hiew

# --------------------------------------------------------------------------
# Add more PEiD signatures here to this list
PEID_DATABASES      = ['UserDB.TXT']
PEID_DATABASES      = [r"%s\%s" % (hiew.PYHIEW_PATH, x) for x in PEID_DATABASES]
PEID_DATABASE_CACHE = r'%s\peid-db.cache' % hiew.PYHIEW_PATH

# --------------------------------------------------------------------------
class TreeMatcher(object):
    def __init__(self):
        self.__tree = None
        self.version = 1
        self.ud = None
        self.src_fn = None


    def __set_tree(self, v):
        self.__tree = v


    Tree = property(lambda self: self.__tree, __set_tree)
    """Get / Set tree"""


    def pack(self, ud=None, version=None, src_fn=None):
        """
        Packs the tree into a data stream

        @return: packed tree or None
        """

        if ud is None:
            ud = self.ud
        if version is None:
            version = self.version
        if src_fn is None:
            src_fn = self.src_fn

        # Compose the header
        d = {
                'version'   : version,
                'ud'        : ud,
                'src_fn'    : src_fn,
                'tree'      : self.Tree
            }

        try:
            return zlib.compress(pickle.dumps(d))
        except Exception as e:
            print(("picke_error: %s" % str(e)))
            return None


    def unpack(self, stream, src_fn):
        """
        Unpacks the tree from a stream

        @return: Boolean
        """
        try:
            # Decompress
            d = zlib.decompress(stream)

            # Deserialize
            d = pickle.loads(d)

            # Load tree components
            self.__tree  = d['tree']
            self.version = d['version']
            self.ud      = d['ud']

            # Check if the cache comes from the same sources
            expected_src_fn = d['src_fn']
            if src_fn != expected_src_fn:
                return False

            self.src_fn = src_fn

            return True
        except Exception as e:
            #print("Exception: %s" % str(e))
            return False


    def match(self, bytes=None, fo=None):
        """
        Matches bytes in the tree and returns correponding leafs
        """
        if self.__tree is None or (bytes is None and fo is None):
            return []

        branch = self.__tree

        # No fixed pattern? Reading from stream?
        from_fo = bytes is None

        if from_fo:
            bytes = []
            # Count will always be greater than the counter
            c = 1
        else:
            c = len(bytes)

        i  = 0
        bt = []

        nomatch = False

        ret = []
        while True:
            # Leaf?
            if -2 in branch and not nomatch:
                # Append result
                ret.append((i, branch[-2]))

            # End?
            if i >= c or nomatch:
                # Check backtrack
                if bt:
                    branch, i = bt.pop()
                else:
                    # Done search
                    break

            # Get byte
            if from_fo:
                # Stream not finished, but reading backwards?
                if i < c - 1:
                    b = bytes[i]
                else:
                    # Read a new byte
                    b = fo.read(1)
                    # End of file?
                    if not b:
                        c = len(bytes)
                        from_fo = False
                        continue

                    # Save this byte
                    bytes.append(b[0])

                    # Update end of stream
                    c += 1
            # Read directly from the buffer
            else:
                b = bytes[i]

            # Exact match?
            exact = b in branch

            # Wild match?
            wild = -1 in branch

            # No match condition
            nomatch = not (wild or exact)

            if nomatch:
                continue

            # Wild and exact match?
            # We prefer exact match and backtrack if needed
            if wild and exact:
                # Save backtrack info: Wild card branch and the next byte
                bt.append((branch[-1], i+1))

            # Exact match?
            if exact:
                # Take the branch
                branch = branch[b]
            # Wild match?
            else:
                # Take wild branch
                branch = branch[-1]
            i += 1

        return ret


# --------------------------------------------------------------------------
class PEiDSigMatch(object):
    def __init__(self):
        self.__tree = None
        self.__tm = TreeMatcher()


    def save_cache(self, fn, src_fn):
        stream = self.__tm.pack(src_fn = src_fn)
        f = open(fn, 'wb')
        f.write(stream)
        f.close()


    def load_cache(self, fn, src_fn):
        try:
            f = open(fn, 'rb')
            stream = f.read()
            f.close()
            return self.__tm.unpack(stream, src_fn)
        except:
            return False


    def load(self, fn, cache_file=None):
        """
        @param fn: The file name(s) to load the signatures from
        @param cache_file: The name of the cache file
        """
        # Convert a file name into a one element list
        if isinstance(fn, str):
            fn = [fn]

        if cache_file and self.load_cache(cache_file, fn):
            return True

        # Initiate a parser and set default values
        c = configparser.RawConfigParser({'ep_only': 'True'}, strict=False)

        # The read method returns the same input list on success
        ret = len(fn) == len(c.read(fn))

        # Reset the tree
        tree = {}

        # Go over all sections
        for section in c.sections():
            packer    = section
            ep_only   = c.getboolean(section, 'ep_only')
            signature = c.get(section, 'signature').split(' ')

            branch = tree
            for b in signature:
                # Convert wildcard to -1 and number strings to numbers
                if b.startswith('?'):
                    b = -1
                else:
                    b = int(b, 16)

                branch = branch.setdefault(b, {})

            # A leaf has index -2
            leaf = branch.setdefault(-2, [])
            # Append packer info to the leaf
            leaf.append((packer, ep_only))

        # Store tree
        self.__tm.Tree = tree

        # Cache was required? Then cache the result
        if cache_file:
            self.save_cache(cache_file, fn)

        return ret

    def match(self, bytes=None, fo=None):
        return self.__tm.match(bytes=bytes, fo=fo)


# --------------------------------------------------------------------------
class HiewFo(object):
    """
    Create a Hiew file object class
    """
    def __init__(self):
        self.seek = hiew.Data.GetCurrentOffset()

    def read(self, sz):
        rc, buf = hiew.FileRead(self.seek, sz)
        if buf:
            self.seek += sz
        return buf


# --------------------------------------------------------------------------
class PEiDMainClass(object):
    def __init__(self):
        sys.setrecursionlimit(40000)

    def FixSigFiles(self):
        """
        PEiD signature file "UserDB.TXT" apparently uses the [ and ] characters in the packer name.
        Since we use the ConfigParser class, we replace those names with ( and )
        """
        re_fix = re.compile(r"^(\[.+)\[(.+)\](.+\])", re.M)
        try:
            for fn in PEID_DATABASES:
                f = open(fn, 'r')
                s = f.read()
                f.close()
                s2 = re_fix.sub(r'\1(\2)\3', s)
                if s != s2 and hiew.AskYesNo("File contains incorrect section names\n\nCorrect it now?"):
                    os.rename(fn, '%s.bak' % fn)
                    f = open(fn, 'w')
                    f.write(s2)
                    f.close()

            return True

        except Exception as e:
            traceback.print_exc()
            hiew.Window.FromString("Error", "Exception while reading or updating signature files:\n" + ''.join(traceback.format_exception(None, e, e.__traceback__)))
            return False


    def LoadSig(self):
        self.FixSigFiles()

        # Create a signature matcher
        self.sig = PEiDSigMatch()
        if not self.sig.load(PEID_DATABASES, PEID_DATABASE_CACHE):
            hiew.Message("Error", "Failed to load signature database!")
            return False

        return True


    def Show(self):
        # Try to match using a Hiew file object at the current offset
        result = self.sig.match(fo=HiewFo())
        if not result:
                hiew.Message("PEiD", "No signature was found at the current file offset")
                return False

        lines = []
        for match in reversed(result):
                depth, v = match
                lines.append("%s [Depth #%d]" % (v[0][0], depth))

        m = hiew.Menu()

        r = m.Create(
            title = " -* Hiew/PEiD - Signature match *- ",
            lines = lines,
            width = 80)

        while True:
            n, k = m.Show()
            if n == -1:
                break


# --------------------------------------------------------------------------
try:
    PEID_SCRIPT
    PEID_SCRIPT.Show()
except:
    # Create new instance
    t = PEiDMainClass()
    # Try to load the signatures
    if t.LoadSig():
        PEID_SCRIPT = t
        # Show match
        t.Show()
