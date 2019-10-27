""" Stupid simple Java parser. """
import re

def parse_lines(string):
    """ Splits document into terminations (;) and comments (*/) """
    return [ x.strip() for x in string.split(";") ]

def parse_comment(string):
    return re.search("/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/", string)

def parse_rows(comment, definition):
    return [ row_parser(x[0], x[1]) for x in lines ]

def java(string):
    return lines

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

if __name__ == "__main__":
    from pprint import pprint
    #pprint(java(TEST))
    #pprint(parse_rows("", ""))
    assert not parse_comment("thing")
    assert parse_comment("/** her */ thing")
    pprint(parse_comment("/** her */ thing"))
