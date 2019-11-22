""" Stupid simple Java and Org parsers. """
import re

def parse_lines(string):
    """ Splits document into terminations (;)"""
    # NOTE: splitting strings into substrings is stupid
    return [ x.strip() for x in string.split(";") ] # FIXME: this needs to check for comments.

def parse_comment_ml(string):
    """ Parses multi-line comment. `/** <comment> */` """
    multi = r"/\*[^*]*\*+(?:([^/*][^*]*)\*+)*/"
    r = re.match(multi, string)
    if r is not None:
        a, b = r.span()
        m = r.group(1).strip()
        return a, b, m
    else:
        return 0, 0, ""

def parse_comment_sl(string):
    """ Parses single-line comment. `// <comment>` """
    # NOTE: single line comments are often trailing comments
    pattern = r"//[^\n\r]+.*[\n\r]"
    r = re.search(pattern, string)
    if r is not None:
        a, b = r.span()
        return a, b
    else:
        return 0, 0

def parse_terminator(a: int, string):
    """ Returns the next termination including and after `a` """
    span = string[a:]
    return span.find(";")

def parse_definition(string):
    """ Parses definition without comment. """
    string = string.strip()
    a, b = parse_comment_sl(string)
    string = string[b:]
    
    a, b, r = parse_comment_ml(string)

    line = string[b:].strip().replace(";", "").split(" ")
    try:
        type_ = line[1]
        field = line[2]
        default = line[4:]
        # value = " ".join([type_] + default)
        return (field, type_, "".join(default))
    except IndexError:
        return None
    
def build_rows(string):
    lines = parse_lines(string)
    for line in lines:
        comment = parse_comment_ml(line)[2]
        f_v = parse_definition(line)
        if f_v is None :
            continue
        f, v, t = f_v
        yield (f, v, t, comment)
        
def build_definition_table(string):
    """ For typical definitions: `public Color color = new Color("ffffff"); ` with prefixed multiline comments. """
    colnames = "|field|type|default|notes|\n|-\n"
    return colnames + "| " + "|\n| ".join([ " | ".join(x) for x in build_rows(string) ])

def build_defaults_table(string):
    """ For typical overwrites: `itemCapacity = 30;` """
    colnames = "|field|default|\n|-\n"
    return colnames + "\n".join([ "| " + x.replace("=", "|").replace(";", " |")
                       for x in string.splitlines() ])

def build_content_tables(string):
    """ Reads an org file and makes a content table. """
    def format(x):
        if "*****" in x:
            raise ValueError("*****", f"unsupported header: {x}")

        # remove all code blocks
        x = x.replace("=", "")
        x = x.replace("~", "")

        # make headers into list
        x = ( x.replace("****", " " * 6 + "*")
               .replace("***", " " * 4 + "*")
               .replace("**", " " * 2 + "*") )

        # make github hyperlink
        l = ( x.replace("*", " ")
               .replace("TODO", " ")
               .replace("NEW", " ")
               .strip()
               .replace(" ", "-")
               .replace(".", "") )

        # splite bullet list and names
        h, n = x.split("*")
        n = n.strip()

        pre = "https://simonwoodburyforget.github.io/mindustry-modding/#"
        return f"\n  {h}* [[{pre}{l}][{n}]]"
        
    return "".join([ format(x) for x in string.splitlines() if ( x.startswith("* ") or 
                                                                 x.startswith("** ") ) ])

TEST = """
    public float splashDamage = 0f;
    /** Knockback in velocity. */
    public float knockback;
    /** Whether this bullet hits tiles. */
    public boolean hitTiles = true;
    /** Status effect applied on hit. */
    public StatusEffect status = StatusEffects.none;
    /** Intensity of applied status effect in terms of duration. */
    public float statusDuration = 60 * 10f;
    /** Whether this bullet type collides with tiles. */
    public boolean collidesTiles = true;
    /** Whether this bullet type collides with tiles that are of the same team. */
    public boolean collidesTeam = false;
    /** Whether this bullet type collides with air units. */
    public boolean collidesAir = true;
    /** Whether this bullet types collides with anything at all. */
    public boolean collides = true;
    /** Whether velocity is inherited from the shooter. */
    public boolean keepVelocity = true;

    //additional effects

    public int fragBullets = 9;
    public float fragVelocityMin = 0.2f, fragVelocityMax = 1f;
    public BulletType fragBullet = null;

    /** Use a negative value to disable splash damage. */
    public float splashDamageRadius = -1f;

    public int incendAmount = 0;
    public float incendSpread = 8f;
    public float incendChance = 1f;

    public float homingPower = 0f;
    public float homingRange = 50f;

    public int lightining;
    public int lightningLength = 5;

    public float hitShake = 0f;
"""

TEST2 = """
    public Color backColor = Pal.bulletYellowBack, frontColor = Pal.bulletYellow;
    public float bulletWidth = 5f, bulletHeight = 7f;
    public float bulletShrink = 0.5f;
    public String bulletSprite;
"""


TEST3 = """
    protected Color trailColor = Pal.missileYellowBack;

    protected float weaveScale = 0f;
    protected float weaveMag = -1f;

"""

if __name__ == "__main__":
    from pprint import pprint
    #pprint(java(TEST))
    #pprint(parse_rows("", ""))
    assert parse_comment_ml("thing") == (0, 0, "")
    assert parse_comment_ml("/** her */ thing")[2] == "her"
    assert parse_comment_sl("""// her 
                               thing""") == (0, 8)
    
    assert parse_definition("""
        /** her */ 
        public float thing = 34;
    """) == ("thing", "float 34")

    print(build_table(TEST3))
