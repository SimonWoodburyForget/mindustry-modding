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

## UnlockableContent and MappableContent 

Pretty much all types can have a name and description.

| field       | type   | notes                    |
|-------------|--------|--------------------------|
| name        | String | name visible to the user |
| description | String |                          |

## Item

*extends `UnlockableContent`* Objects that ride conveyors/sorters and can be used in crafters.

| field          | value         | notes                                                                 |
|----------------|---------------|-----------------------------------------------------------------------|
| color          | Color         | hex string of color                                                   |
| type           | ItemType      | resource or material; used for tabs and core acceptance               |
| explosiveness  | float 0       | how explosive this item is.                                           |
| flammability   | float 0       | flammability above 0.3 makes this eleigible for item burners.         |
| radioactivity  | float         | how radioactive this item is. 0=none, 1=chernobyl ground zero         |
| hardness       | int 0         | drill hardness of the item                                            |
| cost           | float 1       | used for calculating place times; 1 cost = 1 tick added to build time |
| alwaysUnlocked | boolean false | If true, item is always unlocked.                                     |
    
## BlockStorage

*extends `UnlockableContent`* 

| field          | type          | notes |
|----------------|---------------|-------|
| hasItems       | boolean       |       |
| hasLiquids     | boolean       |       |
| hasPower       | boolean       |       |
| outputsLiquid  | boolean false |       |
| consumesPower  | boolean true  |       |
| outputsPower   | boolean false |       |
| itemCapacity   | int 10        |       |
| liquidCapacity | float 10      |       |

## BuildVisibility

Possible options for build visibility include:
- hidden,
- shown, 
- debugOnly,
- sandboxOnly,
- campaignOnly.

## Block

*extends `BlockStorage`* -- Attributes for all objects that are blocks.

| field               | value                  | notes                                                                              |
|---------------------|------------------------|------------------------------------------------------------------------------------|
| update              | boolean                | whether this block has a tile entity that updates                                  |
| destructible        | boolean                | whether this block has health and can be destroyed                                 |
| unloadable          | boolean true           | whether unloaders work on this block                                               |
| solid               | boolean                | whether this is solid                                                              |
| solidifes           | boolean                | whether this block CAN be solid.                                                   |
| rotate              | boolean                | whether this is rotateable                                                         |
| breakable           | boolean                | whether you can break this with rightclick                                         |
| placeableOn         | boolean true           | whether this floor can be placed on.                                               |
| health              | int -1                 | tile entity health                                                                 |
| baseExplosiveness   | float 0                | base block explosiveness                                                           |
| floating            | boolean false          | whether this block can be placed on edges of liquids.                              |
| size                | int 1                  | multiblock size                                                                    |
| expanded            | boolean false          | Whether to draw this block in the expanded draw range.                             |
| timers              | int 0                  | Max of timers used.                                                                |
| fillesTile          | true                   | Special flag; if false, floor will be drawn under this block even if it is cached. |
| alwaysReplace       | boolean false          | whether this block can be replaced in all cases                                    |
| group               | BlockGroup none        | Unless `canReplace` is overriden, blocks in the same group can replace each other. |
| priority            | TargetPriority base    | Targeting priority of this block, as seen by enemies.                              |
| configurable        | boolean                | Whether the block can be tapped and selected to configure.                         |
| consumesTap         | boolean                | Whether this block consumes touchDown events when tapped.                          |
| posConfig           | boolean                | Whether the config is positional and needs to be shifted.                          |
| targetable          | boolean true           | Whether units target this block.                                                   |
| canOverdrive        | boolean true           | Whether the overdrive core has any effect on this block.                           |
| outlineColor        | Color "404049"         | Outlined icon color.                                                               |
| outlineIcon         | boolean false          | Whether the icon region has an outline added.                                      |
| hasShadow           | boolean true           | Whether this block has a shadow under it.                                          |
| breakSound          | Sound boom             | Sounds made when this block breaks.                                                |
| activeSound         | Sound none             | The sound that this block makes while active. One sound loop. Do not overuse.      |
| activeSoundVolume   | float 0.5              | Active sound base volume.                                                          |
| idleSound           | Sound none             | The sound that this block makes while idle. Uses one sound loop for all blocks.    |
| idleSoundVolume     | float 0.5              | Idle sound base volume.                                                            |
| requirements        | ItemStack []           | Cost of constructing this block.                                                   |
| category            | Category distribution  | Category in place menu.                                                            |
| buildCost           | float                  | Cost of building this block; do not modify directly!                               |
| buildVisibility     | BuildVisibility hidden | Whether this block is visible and can currently be built.                          |
| buildCostMultiplier | float 1f               | Multiplier for speed of building this block.                                       |
| instantTransfer     | boolean false          | Whether this block has instant transfer.                                           |
| alwaysUnlocked      | boolean false          |                                                                                    |

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

| field              | value             | notes                                                                   |
|--------------------|-------------------|-------------------------------------------------------------------------|
| lifetime           | float             | amount of ticks it lasts                                                |
| speed              | float             | inital speed of bullet                                                  |
| damage             | float             | collision damage                                                        |
| hitSize            | float 4           | collision radius                                                        |
| drawSize           | float 40          |                                                                         |
| drag               | float 0           | decelleration per tick                                                  |
| pierce             | boolean           | whether it can collide                                                  |
| hitEffect          | Effect            | created when bullet hits something                                      |
| despawnEffect      | Effect            | created when bullet despawns                                            |
| shootEffect        | Effect            | created when shooting                                                   |
| smokeEffect        | Effect            | created when shooting                                                   |
| hitSound           | Sound             | made when hitting something or getting removed                          |
| inaccuracy         | float 0           | extra inaccuracy                                                        |
| ammoMultiplier     | float 2           | how many bullets get created per item/liquid                            |
| reloadMultiplier   | float 1           | multiplied by turret reload speed                                       |
| recoil             | float             | recoil from shooter entities                                            |
| splashDamage       | float 0f          |                                                                         |
| knockback          | float             | Knockback in velocity.                                                  |
| hitTiles           | boolean true      | Whether this bullet hits tiles.                                         |
| status             | StatusEffect none | Status effect applied on hit.                                           |
| statusDuration     | float 600         | Intensity of applied status effect in terms of duration.                |
| collidesTiles      | boolean true      | Whether this bullet type collides with tiles.                           |
| collidesTeam       | boolean false     | Whether this bullet type collides with tiles that are of the same team. |
| collidesAir        | boolean true      | Whether this bullet type collides with air units.                       |
| collides           | boolean true      | Whether this bullet types collides with anything at all.                |
| keepVelocity       | boolean true      | Whether velocity is inherited from the shooter.                         |
| fragBullets        | int 9             |                                                                         |
| fragVelocityMin    | float 0.2         |                                                                         |
| fragVelocityMax    | float 1           |                                                                         |
| fragBullet         | BulletType null   |                                                                         |
| splashDamageRadius | float -1f         | Use a negative value to disable splash damage.                          |
| incendAmount       | int 0             |                                                                         |
| incendSpread       | float 8f          |                                                                         |
| incendChance       | float 1f          |                                                                         |
| homingPower        | float 0f          |                                                                         |
| homingRange        | float 50f         |                                                                         |
| lightining         | int               |                                                                         |
| lightningLength    | int 5             |                                                                         |
| hitShake           | float 0f          |                                                                         |
    
### BasicBulletType

The actual bullet type.

| field        | value                  | notes |
|--------------|------------------------|-------|
| backColor    | Color bulletYellowBack |       |
| frontColor   | Color bulletYellow     |       |
| bulletWidth  | float 5                |       |
| bulletHeight | float 7                |       |
| bulletShrink | float 0.5              |       |
| bulletSprite | String                 |       |

#### ArtilleryBulletType

| field       | value                 | notes |
|-------------|-----------------------|-------|
| trailEffect | Effect artilleryTrail |       |


Defaults:

| field         | value     |
|---------------|-----------|
| collidesTiles | false     |
| collides      | false     |
| hitShake      | 1         |
| hitSound      | explosion |

#### BombBulletType

Defaults:

| field              | value     |
|--------------------|-----------|
| collidesTiles      | false     |
| collides           | false     |
| bulletShrink       | 0.7       |
| lifetime           | 30        |
| drag               | 0.05      |
| keepVelocity       | false     |
| collidesAir        | false     |
| hitSound           | explosion |

    
#### FlakBulletType

Bullets that explode near enemies.

| field        | value    | notes |
|--------------|----------|-------|
| explodeRange | float 30 |       |

Defaults:

| field              | value            |
|--------------------|------------------|
| splashDamage       | 15               |
| splashDamageRadius | 34               |
| hitEffect          | flakExplosionBig |
| bulletWidth        | 8                |
| bulletHeight       | 10               |


#### HealBulletType

Bullets that can heal blocks of the same team as the shooter.

| field       | value   | notes |
|-------------|---------|-------|
| healPercent | float 3 |       |

Defaults:

| field         | value     |
|---------------|-----------|
| shootEffect   | shootHeal |
| smokeEffect   | hitLaser  |
| hitEffect     | hitLaser  |
| despawnEffect | hitLaser  |
| collidesTeam  | true      |


#### LiquidBulletType

| field  | value       |                |
|--------|-------------|----------------|
| liquid | Liquid null | required field |

Defaults:

| field          | value     |
|----------------|-----------|
| lifetime       | 74        |
| statusDuration | 90        |
| despawnEffect  | none      |
| hitEffect      | hitLiquid |
| smokeEffect    | none      |
| shootEffect    | none      |
| drag           | 0.009     |
| knockback      | 0.55      |


#### MassDriverBolt

Defaults:

| field         | value        |
|---------------|--------------|
| collidesTiles | false        |
| lifetime      | 200          |
| despawnEffect | smeltsmoke   |
| hitEffect     | hitBulletBig |
| drag          | 0.005        |

#### MissileBulletType

| field      | value                   |   |
|------------|-------------------------|---|
| trailColor | Color missileYellowBack |   |
| weaveScale | float 0                 |   |
| weaveMag   | float -1                |   |
    
