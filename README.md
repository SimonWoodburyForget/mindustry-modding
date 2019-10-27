*Disclaimier: This is an overview of the possible fields and types, some of them may or may not work as expected.*

# Overview
## Directory Structure

At the root of your project you should have a `content/`directory, this is where all the JSON data goes, and in that directory you have other directories for various types of units, these are the current common ones:

- `content/items/` for things like copper and surge-alloy,
- `content/blocks/`for things like turrets and floors,
- `content/mechs/` for player controlled mechs tau and dagger,
- `content/liquids/`for liquids like water and slag,
- `content/units/` for flying or ground units like reaper and dagger,
- `content/zones/` for configuration of campaign maps.

Feilds have noumerous attributes, but the important one is `type` as it's what tells the parser which class of object to select. A lot of objects are actually very simple, and follow the common OOP patterns, all that means is they inherit attributes and various behaviors. *(sometimes predictably, othertimes not as much)*


# Referance
## Effect

Value type should be `string`. This type will animate a pre-programmed effects. List of built-in effects:

- none, placeBlock, breakBlock, smoke, spawn, tapBlock, select;
- vtolHover, unitDrop, unitPickup, unitLand, pickup, healWave, heal, 
    landShock, reactorsmoke, nuclearsmoke, nuclearcloud;
- redgeneratespark, generatespark, fuelburn, plasticburn, pulverize, 
    pulverizeRed, pulverizeRedder, pulverizeSmall;- pulverizeMedium;
- producesmoke, smeltsmoke, formsmoke, blastsmoke, lava, doorclose, 
    dooropen, dooropenlarge, doorcloselarge, purify;- purifyoil, purifystone, generate;
- mine, mineBig, mineHuge, smelt, teleportActivate, teleport, teleportOut, ripple, bubble, launch;
- healBlock, healBlockFull, healWaveMend, overdriveWave, overdriveBlockFull, shieldBreak, hitBulletSmall, hitFuse;
- hitBulletBig, hitFlameSmall, hitLiquid, hitLaser, hitLancer, hitMeltdown, despawn, flakExplosion, blastExplosion;
- plasticExplosion, artilleryTrail, incendTrail, missileTrail, absorb, flakExplosionBig, plasticExplosionFlak, burning, fire;
- fireSmoke, steam, fireballsmoke, ballfire, freezing, melting, wet, oily, overdriven, dropItem, shockwave;
- bigShockwave, nuclearShockwave, explosion, blockExplosion, 
    blockExplosionSmoke, shootSmall, shootHeal, shootSmallSmoke;- shootBig, shootBig2, shootBigSmoke;
- shootBigSmoke2, shootSmallFlame, shootPyraFlame, shootLiquid, shellEjectSmall, shellEjectMedium;
- shellEjectBig, lancerLaserShoot, lancerLaserShootSmoke, lancerLaserCharge,
    lancerLaserChargeBegin, lightningCharge;- lightningShoot;
- unitSpawn, spawnShockwave, magmasmoke, impactShockwave, 
    impactcloud, impactsmoke, dynamicExplosion, padlaunch, commandSend, coreLand.

You can't currently create custom effects.

## BulletType

This type is typically used within the field of another type, like turret ammo, or weapon bullet, or fragment bullet.

| field            | value    |                                                |
|------------------|----------|------------------------------------------------|
| lifetime         | float    | amount of ticks it lasts                       |
| speed            | float    | inital speed of bullet                         |
| damage           | float    | collision damage                               |
| hitSize          | float 4  | collision radius                               |
| drawSize         | float 40 |                                                |
| drag             | float 0  | decelleration per tick                         |
| pierce           | boolean  | whether it can collide                         |
| hitEffect        | Effect   | created when bullet hits something             |
| despawnEffect    | Effect   | created when bullet despawns                   |
| shootEffect      | Effect   | created when shooting                          |
| smokeEffect      | Effect   | created when shooting                          |
| hitSound         | Sound    | made when hitting something or getting removed |
| inaccuracy       | float 0  | extra inaccuracy                               |
| ammoMultiplier   | float 2  | how many bullets get created per item/liquid   |
| reloadMultiplier | float 1  | multiplied by turret reload speed              |
| recoil           | float    | recoil from shooter entities                   |


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


## UnlockableContent and MappableContent 

Base interface for an unlockable content type.

| field       | type          |                          |
|-------------|---------------|--------------------------|
| name        | public String | name visible to the user |
| description | public String |                          |

## Item extends UnlockableContent

Objects that ride conveyors/sorters and can be used in crafters.

| field          | value             |                                                                       |
|----------------|-------------------|-----------------------------------------------------------------------|
| color          | string            | hex string of color                                                   |
| type           | string "resource" | resource or material; used for tabs and core acceptance               |
| explosiveness  | float 0           | how explosive this item is.                                           |
| flammability   | float 0           | flammability above 0.3 makes this eleigible for item burners.         |
| radioactivity  | float             | how radioactive this item is. 0=none, 1=chernobyl ground zero         |
| hardness       | int 0             | drill hardness of the item                                            |
| cost           | float 1           | used for calculating place times; 1 cost = 1 tick added to build time |
| alwaysUnlocked | boolean false     | If true, item is always unlocked.                                     |




