import math
import web
import random
from web import form

render = web.template.render('templates/')

urls = (
    '/', 'index', 
    '/index', 'index',
    '/auto', 'auto',
    '/armor', 'armor',
    '/combat', 'combat',
    '/failure', 'failure'
)

app = web.application(urls, globals())
comments = ""
debug = ""

autoform = form.Form( 
    form.Textbox("autoSkill", description = "What is your Firearm skill?"),
    form.Textbox("autoShots", description = "How many shots do you want to fire?"),
    form.Textbox("autoRoll", description = "Roll your d100. What did you get?")
    )
    
armorform = form.Form( 
    form.Dropdown("armorAmmo", description = "What ammo are you using?", 
        args = ['Full Metal Jacket', 'Hollow Points', 'Armor Piercing'], value = 'Full Metal Jacket'),
    form.Dropdown("armorCartridge", description = "What cartridge are you using?", 
        args = ['Small Caliber Pistol', 'Low Velocity Pistol', 'High Velocity Pistol', 'Magnum Pistol', '12-Gauge Buckshot', 
        '12-Gauge Rifled Slug', 'Low Power Rifle', 'PDW/Carbine', 'Intermediate Rifle', 'Battle Rifle', 'Magnum Rifle'], value = 'Intermediate Rifle'),
    form.Dropdown("armorRating", description = "What armor is your victim wearing?", 
        args = ['None', 'Level I', 'Level IIA', 'Level II', 'Level IIIA', 'Level III', 'Level IV'], value = 'None'),
    form.Textbox("armorDamage", description = "Roll for damage. What did you get?")
    )
    
combatform = form.Form(
    form.Dropdown("combatWeapon", description = "Weapon Type", 
        args = ['Subcompact Pistol', 'Compact Pistol', 'Full-Size Pistol', 'Large Pistol', 'Black Powder Pistol', 'Black Powder Musket', 
        'Black Powder Rifle', 'Shotgun', 'Compact SMG', 'Full-Size SMG', 'Pistol-Caliber Carbine', 'PDW', 'Rifle-Caliber Carbine', 'Obrez', 'Small-Caliber Rifle', 
        'Battle Rifle', 'Small-Caliber DMR', 'Battle Rifle DMR', 'Magnum Sniper Rifle', 'Large-Caliber Sniper Rifle', 'Light Machine Gun', 'Medium Machine Gun', 'Heavy Machine Gun']),
    form.Checkbox("combatMagnification", description = "Using a magnification optic?"),
    form.Checkbox("combatStock", description = "Using a stock?"),
    form.Checkbox("combatGrip", description = "Using an offhand grip?"),
    form.Checkbox("combatAkimbo", description = "Akimbo?"),
    form.Dropdown("combatCartridge", description = "Cartridge Type", 
        args = ['.22 LR', '.22 WMR', '.22-250', '.220 Swift', '.222 Rem', '.223 Rem', '.243 Win', '.25 ACP', '.25-06', '.270 Winchester', '.30 Carbine', '.30-06', '.30-30', '.30-40', 
        '.300 AAC BLK', '.300 Win Mag', '.303 British', '.308 Win', '.32 ACP', '.32 S&W', '.338 Lapua', '.338 Win Mag', '.35 Remington', '.357 Magnum', '.357 SIG', '.375 H&H', 
        '.38 Special', '.38 Super', '.380 ACP', '.40 S&W', '.410 Shot', '.410 Slug', '.44 Magnum', '.44-40', '.45 ACP', '.45 Colt', '.45-70', '.450 Bushmaster', '.454 Casull', 
        '.458 SOCOM', '.460 S&W', '.50 AE', '.50 Beowulf', '.50 BMG',  '10mm Auto', '10 Gauge Shot', '10 Gauge Slug','12 Gauge Shot', '12 Gauge Slug', '16 Gauge Shot', '16 Gauge Slug', 
        '20 Gauge Shot', '20 Gauge Slug', '28 Gauge Shot', '28 Gauge Slug', '20x102mm', '4.6x30', '5.45x39', '5.56x45', '5.7x28', '500 S&W', '6.5mm Creedmoor', '6.5mm Grendel', 
        '6.5mm Japanese', '6.5mm Swedish', '6.8mm SPC', '7.5mm French', '7.5mm Swiss', '7.62x25 Tokarev', '7.62x39', '7.62x51', '7.62x54R', '7mm Mauser', '7mm Rem Mag', '7mm-08', 
        '8mm Mauser', '9mm Luger', '9x18 Makarov', '9x21mm', 'Lead Musket Ball', 'Lead Pistol Ball']),
    form.Dropdown("combatAmmo", description = "Ammunition Type", 
        args = ['Full Metal Jacket', 'Jacketed Hollow Point', 'Soft Point', 'Unjacketed', 'Overpressure', 'Armor Piercing', 'AP Incendiary', 'Depleted Uranium', 'High Explosive', 'Tracer']),
    form.Dropdown("combatStance", description = "Stance", args = ['Running', 'Walking', 'Standing', 'Kneeling', 'Sitting', 'Prone'], value = 'Standing'),
    form.Checkbox("combatBraced", description = "Bracing the weapon or using a bipod?"),
    form.Checkbox("combatAwkward", description = "Are you in an awkward firing position?"),
    form.Dropdown("combatShotType", description = "Shot Type",
        args = ['Aimed, Slow', 'Aimed, Rapid', 'Aimed, Auto', 'Point Shooting, Slow', 'Point Shooting, Rapid', 'Point Shooting, Auto', 'Blind Fire, Slow', 'Blind Fire, Rapid', 
        'Blind Fire, Auto', 'Suppression Fire']),
    form.Dropdown("combatDifficulty", description = "Target Difficulty", args = ['Full Visibility', 'Partial Visibility', 'Partial Concealment', 'Partial Cover', 'Full Concealment', 'Full Cover']),
    form.Dropdown("combatMotion", description = "Target Motion", args = ['Motionless', 'Moving Slowly', 'Moving Quickly', 'Moving Erratically']),
    form.Dropdown("combatArmor", description = "Defender Armor", args = ['None', 'Level I', 'Level IIA', 'Level II', 'Level IIIA', 'Level III', 'Level IV']),
    form.Textbox("combatMultiplier", description = "Narrative multiplier", value = 1),
    form.Textbox("combatDistance", description = "Distance in yards"),
    form.Textbox("combatShots", description = "Number of shots on target")
    )

failureform = form.Form(
    form.Dropdown("failureDropDown", description = "What did you DO?!", 
        args = ['Botched a firearm attack', 'Botched a melee combat roll', 'Failed any SAN roll', 'Lost 5 SAN at once or 1/5 or more SAN in a day (Realtime)', 'Lost 5 SAN at once or 1/5 or more SAN in a day (Summary)']),
    )


class index:
    def GET(self):
        return render.index()

class auto: 
    def GET(self): 
        form = autoform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.auto(form, comments)

    def POST(self): 
        form = autoform() 
        if not form.validates(): 
            return render.auto(form, comments)
        else:
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            #return "Grrreat success! boe: %s, bax: %s" % (form.d.boe, form['bax'].value)
            
            skill = int(form["autoSkill"].value)
            shots = int(form["autoShots"].value)
            roll = int(form["autoRoll"].value)
            prob = ((shots * 5) + skill) - 5
            maxShots = math.floor(skill / 5) + 1
            
            if shots <= maxShots:
                if roll <= prob:
                    raw = (math.floor(prob / 10) - (math.floor(roll / 10)))
                else:
                    raw = 0
                
                if raw > shots:
                    hits = shots
                else:
                    hits = raw
                
                if hits == 1:
                    comments = "You hit your target 1 time!"
                else:
                    comments = "You hit your target %s times!" % int(hits)
            else:
                comments = "Sorry, you cannot fire more than %s shots this round! Try again." % int(maxShots)
            
            return render.auto(form, comments)
            
class armor:
    def GET(self):
        form = armorform()
        return render.armor(form, comments)
    
    def POST(self):
        form = armorform()
        if not form.validates():
            return render.armor(form, comments)
        else:
            ammo = form["armorAmmo"].value
            cartridge = form["armorCartridge"].value
            armor = form["armorRating"].value
            roll = int(form["armorDamage"].value)
            multiplier = 0
            
            if ammo == "Full Metal Jacket":
                smallCaliberPistol = {'None': 1, 'Level I': .25, 'Level IIA': 0, 'Level II': 0, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                lowVelocityPistol = {'None': 1, 'Level I': .5, 'Level IIA': .25, 'Level II': 0, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                highVelocityPistol = {'None': 1, 'Level I': .75, 'Level IIA': .5, 'Level II': .25, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                magnumPistol = {'None': 1, 'Level I': 1, 'Level IIA': .75, 'Level II': .5, 'Level IIIA': .25, 'Level III': 0, 'Level IV': 0}
                twelvegaugeBuck = {'None': 1, 'Level I': .75, 'Level IIA': .5, 'Level II': .25, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                twelvegaugeSlug = {'None': 1, 'Level I': 1, 'Level IIA': 1, 'Level II': .75, 'Level IIIA': .5, 'Level III': .25, 'Level IV': 0}
                lowPowerRifle = {'None': 1, 'Level I': .5, 'Level IIA': .25, 'Level II': 0, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                pdwCarbine = {'None': 1, 'Level I': 1, 'Level IIA': 1, 'Level II': .75, 'Level IIIA': .5, 'Level III': .25, 'Level IV': 0}
                intermediateRifle = {'None': 1, 'Level I': 1, 'Level IIA': 1, 'Level II': .75, 'Level IIIA': .5, 'Level III': .25, 'Level IV': 0}
                battleRifle = {'None': 1, 'Level I': 1, 'Level IIA': 1, 'Level II': 1, 'Level IIIA': .75, 'Level III': .5, 'Level IV': 0}
                magnumRifle = {'None': 1, 'Level I': 1, 'Level IIA': 1, 'Level II': 1, 'Level IIIA': 1, 'Level III': .75, 'Level IV': .75}
                if cartridge == 'Small Caliber Pistol':
                    multiplier = smallCaliberPistol[armor]
                elif cartridge == 'Low Velocity Pistol':
                    multiplier = lowVelocityPistol[armor]
                elif cartridge == 'High Velocity Pistol':
                    multiplier = highVelocityPistol[armor]
                elif cartridge == 'Magnum Pistol':
                    multiplier = magnumPistol[armor]
                elif cartridge == '12-Gauge Buckshot':
                    multiplier = twelvegaugeBuck[armor]
                elif cartridge == '12-Gauge Rifled Slug':
                    multiplier = twelvegaugeSlug[armor]
                elif cartridge == 'Low Power Rifle':
                    multiplier = lowPowerRifle[armor]
                elif cartridge == 'PDW/Carbine':
                    multiplier = pdwCarbine[armor]
                elif cartridge == 'Intermediate Rifle':
                    multiplier = intermediateRifle[armor]
                elif cartridge == 'Battle Rifle':
                    multiplier = battleRifle[armor]
                else:
                    multiplier = magnumRifle[armor]
                
            elif ammo == "Hollow Points":
                smallCaliberPistol = {'None': 1.5, 'Level I': 0, 'Level IIA': 0, 'Level II': 0, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                lowVelocityPistol = {'None': 1.5, 'Level I': .25, 'Level IIA': 0, 'Level II': 0, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                highVelocityPistol = {'None': 1.5, 'Level I': .5, 'Level IIA': .25, 'Level II': 0, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                magnumPistol = {'None': 1.5, 'Level I': .75, 'Level IIA': .5, 'Level II': .25, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                twelvegaugeBuck = {'None': 1.5, 'Level I': .5, 'Level IIA': .25, 'Level II': 0, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                twelvegaugeSlug = {'None': 1.5, 'Level I': .75, 'Level IIA': .75, 'Level II': .5, 'Level IIIA': .25, 'Level III': 0, 'Level IV': 0}
                lowPowerRifle = {'None': 1.5, 'Level I': .25, 'Level IIA': 0, 'Level II': 0, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                pdwCarbine = {'None': 1.5, 'Level I': .75, 'Level IIA': .75, 'Level II': .5, 'Level IIIA': .25, 'Level III': 0, 'Level IV': 0}
                intermediateRifle = {'None': 1.5, 'Level I': .75, 'Level IIA': .75, 'Level II': .5, 'Level IIIA': .25, 'Level III': 0, 'Level IV': 0}
                battleRifle = {'None': 1.5, 'Level I': .75, 'Level IIA': .75, 'Level II': .75, 'Level IIIA': .5, 'Level III': .25, 'Level IV': 0}
                magnumRifle = {'None': 1.5, 'Level I': .75, 'Level IIA': .75, 'Level II': .75, 'Level IIIA': .75, 'Level III': .5, 'Level IV': .5}
                if cartridge == 'Small Caliber Pistol':
                    multiplier = smallCaliberPistol[armor]
                elif cartridge == 'Low Velocity Pistol':
                    multiplier = lowVelocityPistol[armor]
                elif cartridge == 'High Velocity Pistol':
                    multiplier = highVelocityPistol[armor]
                elif cartridge == 'Magnum Pistol':
                    multiplier = magnumPistol[armor]
                elif cartridge == '12-Gauge Buckshot':
                    multiplier = twelvegaugeBuck[armor]
                elif cartridge == '12-Gauge Rifled Slug':
                    multiplier = twelvegaugeSlug[armor]
                elif cartridge == 'Low Power Rifle':
                    multiplier = lowPowerRifle[armor]
                elif cartridge == 'PDW/Carbine':
                    multiplier = pdwCarbine[armor]
                elif cartridge == 'Intermediate Rifle':
                    multiplier = intermediateRifle[armor]
                elif cartridge == 'Battle Rifle':
                    multiplier = battleRifle[armor]
                else:
                    multiplier = magnumRifle[armor]
                
            else: #Armor Piercing Ammo
                smallCaliberPistol = {'None': .5, 'Level I': .25, 'Level IIA': 0, 'Level II': 0, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                lowVelocityPistol = {'None': .5, 'Level I': 1, 'Level IIA': .75, 'Level II': 0, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                highVelocityPistol = {'None': .5, 'Level I': 1, 'Level IIA': 1, 'Level II': .75, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                magnumPistol = {'None': .5, 'Level I': 1, 'Level IIA': 1, 'Level II': 1, 'Level IIIA': .75, 'Level III': 0, 'Level IV': 0}
                twelvegaugeBuck = {'None': .5, 'Level I': 1, 'Level IIA': 1, 'Level II': .75, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                twelvegaugeSlug = {'None': .5, 'Level I': 1, 'Level IIA': 1, 'Level II': 1, 'Level IIIA': 1, 'Level III': .75, 'Level IV': 0}
                lowPowerRifle = {'None': .5, 'Level I': 1, 'Level IIA': .75, 'Level II': 0, 'Level IIIA': 0, 'Level III': 0, 'Level IV': 0}
                pdwCarbine = {'None': .5, 'Level I': 1, 'Level IIA': 1, 'Level II': 1, 'Level IIIA': 1, 'Level III': .75, 'Level IV': 0}
                intermediateRifle = {'None': .5, 'Level I': 1, 'Level IIA': 1, 'Level II': 1, 'Level IIIA': 1, 'Level III': .75, 'Level IV': 0}
                battleRifle = {'None': .5, 'Level I': 1, 'Level IIA': 1, 'Level II': 1, 'Level IIIA': 1, 'Level III': 1, 'Level IV': 0}
                magnumRifle = {'None': .5, 'Level I': 1, 'Level IIA': 1, 'Level II': 1, 'Level IIIA': 1, 'Level III': 1, 'Level IV': 1}
                if cartridge == 'Small Caliber Pistol':
                    multiplier = smallCaliberPistol[armor]
                elif cartridge == 'Low Velocity Pistol':
                    multiplier = lowVelocityPistol[armor]
                elif cartridge == 'High Velocity Pistol':
                    multiplier = highVelocityPistol[armor]
                elif cartridge == 'Magnum Pistol':
                    multiplier = magnumPistol[armor]
                elif cartridge == '12-Gauge Buckshot':
                    multiplier = twelvegaugeBuck[armor]
                elif cartridge == '12-Gauge Rifled Slug':
                    multiplier = twelvegaugeSlug[armor]
                elif cartridge == 'Low Power Rifle':
                    multiplier = lowPowerRifle[armor]
                elif cartridge == 'PDW/Carbine':
                    multiplier = pdwCarbine[armor]
                elif cartridge == 'Intermediate Rifle':
                    multiplier = intermediateRifle[armor]
                elif cartridge == 'Battle Rifle':
                    multiplier = battleRifle[armor]
                else:
                    multiplier = magnumRifle[armor]
            
            #comments = "You shot %s rounds with your %s, against %s armor. You rolled %s damage." % (ammo, cartridge, armor, roll)
            calculatedDamage = int(math.floor(roll * multiplier))
            if calculatedDamage != 0:
                comments = "You did %s total damage!" % calculatedDamage
            else:
                comments = "BOO! You did ZERO total damage. But remember, if you rolled a Hard Success or better, you can still tell the GM you wanna shoot the baddie in the face!"
            
            return render.armor(form, comments)

class Cartridge ():
    strength = 0
    penetrates = "none"
    damage = 0
    
    def __init__(self, strength, penetrates, damage):
        self.strength = strength
        self.penetrates = penetrates
        self.damage = damage

class combat:
    def GET(self):
        form = combatform()
        return render.combat(form, comments, debug)
    
    def POST(self):
        form = combatform()
        if not form.validates():
            return render.combat(form, comments, debug)
        else:
            weapon = form["combatWeapon"].value
            magnification = form["combatMagnification"].value
            stock = form["combatStock"].value
            grip = form["combatGrip"].value
            akimbo = form["combatAkimbo"].value
            cartridge = form["combatCartridge"].value
            ammo = form["combatAmmo"].value
            stance = form["combatStance"].value
            braced = form["combatBraced"].value
            awkward = form["combatAwkward"].value
            shotType = form["combatShots"].value
            difficulty = form["combatDifficulty"].value
            motion = form["combatMotion"].value
            armor = form["combatArmor"].value
            multiplier = int(form["combatMultiplier"].value)
            distance = int(form["combatDistance"].value)
            shots = int(form["combatShots"].value)
            
            penetrationCalculator = 0 #G10
            armorRating = 0 #G12
            calledShotCalculator = 0 #20
            longerRangePenalty = 0 #E22
            rawHits = 0 #E23
            totalHits = 0 #B27
            rawDamage = 0 #G13
            damageMultiplier = 0 #G15
            unarmoredDamageModifier = 0 #G17
            totalDamage = 0 #B30
            
            isBuckshot = 0 #G8
            isSlug = 0 #G9
            longRangeBuckPenalty = 1 #G7
            addSMGPenetration = 0 #G3
            projectilesPerShot = 1 #G22
            highCaliberCoverPenetration = 0 #G19
            calculatedRange = "" #C23
            calledShotString = ". You can use a CALLED SHOT"
            
            randStock = 1 #E5
            randGrip = 1 #E6
            randAkimbo = 1 #E7
            randStance = 1 #E12
            randBraced = 1 #E13
            randAwkward = 1 #E14
            randLongRange = 1 #ShotType!E1
            randShotType = 1 #E16
            randDifficulty= 1 #E17
            randMotion = 1 #E18
            
            
            #E3
            weaponCategory = {'Subcompact Pistol': 1, 'Compact Pistol': 1, 'Full-Size Pistol': 1, 'Large Pistol': 1, 'Black Powder Pistol': 1, 'Black Powder Musket': 3, 
                'Black Powder Rifle': 4, 'Shotgun': 2, 'Compact SMG': 3, 'Full-Size SMG': 3, 'Pistol-Caliber Carbine': 3, 'PDW': 3, 'Rifle-Caliber Carbine': 4, 'Obrez': 1, 'Small-Caliber Rifle': 4, 
                'Battle Rifle': 5, 'Small-Caliber DMR': 4, 'Battle Rifle DMR': 5, 'Magnum Sniper Rifle': 6, 'Large-Caliber Sniper Rifle': 6, 'Light Machine Gun': 4, 'Medium Machine Gun': 5, 'Heavy Machine Gun': 6}
            
            #Give SMG more penetration (G3)
            if weapon == "Compact SMG" or weapon == "Full-Size SMG" or weapon == "Pistol-Caliber Carbine":
                addSMGPenetration = 1
            else:
                addSMGPenetration = 0
                
            #Is buckshot? (G8)
            if cartridge == ".410 Shot" or cartridge == "10 Gauge Shot" or cartridge == "12 Gauge Shot" or cartridge == "16 Gauge Shot" or cartridge == "20 Gauge Shot" or cartridge == "28 Gauge Shot":
                isBuckshot = 1
            else:
                isBuckshot = 0
            
            #Is slug? (G9)
            if cartridge == ".410 Slug" or cartridge == "10 Gauge Slug" or cartridge == "12 Gauge Slug" or cartridge == "16 Gauge Slug" or cartridge == "20 Gauge Slug" or cartridge == "28 Gauge Slug":
                isSlug = 1
            else:
                isSlug = 0
                
            #Pellets per shotshell (G22)
            if cartridge == ".410 Shot":
                projectilesPerShot = 3
            elif cartridge == "10 Gauge Shot":
                projectilesPerShot = 18
            elif cartridge == "12 Gauge Shot":
                projectilesPerShot= 9
            elif cartridge == "16 Gauge Shot":
                projectilesPerShot = 6
            elif cartridge == "20 Gauge Shot":
                projectilesPerShot = 5
            elif cartridge == "28 Gauge Shot":
                projectilesPerShot = 4
            else:
                projectilesPerShot = 1
                
            #Bonus for using a stock (E5)
            #if stock:
            if 'combatStock' in web.input():
                randStock = (random.randint(114, 116) * .01)
            else:
                randStock = 1
            
            #Penalty for no grip (E6)
            if 'combatGrip' in web.input():
                randGrip = 1
            else:
                randGrip = (random.randint(85, 95) * .01)
                
            #Penalty for akimbo (E7)
            if 'combatAkimbo' in web.input():
                randAkimbo = (random.randint(55, 65) * .01)
            else:
                randAkimbo = 1

            #Create cartridge object E9
            if cartridge == ".22 LR":
                mycartridge = Cartridge(0, "None", random.randint(1, 6))
            elif cartridge == '.22 WMR':
                mycartridge = Cartridge(0, "None", (random.randint(1, 6) + 1))
            elif cartridge == '.22-250':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6)))
            elif cartridge == '.220 Swift':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6)))
            elif cartridge == '.222 Rem':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6)))
            elif cartridge == '.223 Rem':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6)))
            elif cartridge == '.243 Win':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6)))
            elif cartridge == '.25 ACP':
                mycartridge = Cartridge(0, "None", random.randint(1, 6))
            elif cartridge == '.25-06':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6)))
            elif cartridge == '.270 Winchester':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6)))
            elif cartridge  == '.30 Carbine':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 8)+random.randint(1, 4)))
            elif cartridge == '.30-06':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '.30-30':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 3))
            elif cartridge == '.30-40':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 3))
            elif cartridge == '.300 AAC BLK':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 12) + 1))
            elif cartridge == '.300 Win Mag':
                mycartridge = Cartridge(5, "III", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '.303 British':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '.308 Win':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '.32 ACP':
                mycartridge = Cartridge(1, "I", random.randint(1, 8))
            elif cartridge == '.32 S&W':
                mycartridge = Cartridge(1, "I", random.randint(1, 8))
            elif cartridge == '.338 Lapua':
                mycartridge = Cartridge(5, "III", (random.randint(1, 8)+random.randint(1, 8) + 4))
            elif cartridge == '.338 Win Mag':
                mycartridge = Cartridge(5, "III", (random.randint(1, 8)+random.randint(1, 8) + 4))
            elif cartridge == '.35 Remington':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 3))
            elif cartridge == '.357 Magnum':
                mycartridge = Cartridge(3, "II", (random.randint(1, 8)+random.randint(1, 4)))
            elif cartridge == '.357 SIG':
                mycartridge = Cartridge(2, "IIA", random.randint(1, 10))
            elif cartridge == '.375 H&H':
                mycartridge = Cartridge(5, "III", (random.randint(1, 8)+random.randint(1, 8) + 4))
            elif cartridge == '.38 Special':
                mycartridge = Cartridge(2, "IIA", random.randint(1, 10))
            elif cartridge == '.38 Super':
                mycartridge = Cartridge(2, "IIA", random.randint(1, 10))
            elif cartridge == '.380 ACP':
                mycartridge = Cartridge(1, "I", (random.randint(1, 8) + 1))
            elif cartridge == '.40 S&W':
                mycartridge = Cartridge(2, "IIA", random.randint(1, 10))
            elif cartridge == '.410 Shot':
                mycartridge = Cartridge(1, "I", random.randint(1, 2))
            elif cartridge == '.410 Slug':
                mycartridge = Cartridge(2, "IIA", (random.randint(1, 10) + 2))
            elif cartridge == '.44 Magnum':
                mycartridge = Cartridge(3, "II", (random.randint(1, 10)+random.randint(1, 4) + 2))
            elif cartridge == '.44-40':
                mycartridge = Cartridge(2, "IIA", (random.randint(1, 10) + 2))
            elif cartridge == '.45 ACP':
                mycartridge = Cartridge(1, "I", (random.randint(1, 10) + 2)) 
            elif cartridge == '.45 Colt':
                mycartridge = Cartridge(2, "IIA", (random.randint(1, 10) + 2))   
            elif cartridge == '.45-70':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 8)+random.randint(1, 8) + 4))
            elif cartridge == '.450 Bushmaster':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 8)+random.randint(1, 8) + 4))
            elif cartridge == '.454 Casull':
                mycartridge = Cartridge(3, "II", (random.randint(1, 8)+random.randint(1, 8) + 4))
            elif cartridge == '.458 SOCOM':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 8)+random.randint(1, 8) + 4))
            elif cartridge == '.460 S&W':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 10)+random.randint(1, 4) + 3))
            elif cartridge == '.50 AE':
                mycartridge = Cartridge(3, "II", (random.randint(1, 10)+random.randint(1, 6) + 3))
            elif cartridge == '.50 Beowulf':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 8)+random.randint(1, 8) + 4))
            elif cartridge == '.50 BMG':
                mycartridge = Cartridge(6, "IV", (random.randint(1, 10)+random.randint(1, 10)+random.randint(1, 8) + 6))
            elif cartridge == '10mm Auto':
                mycartridge = Cartridge(2, "IIA", (random.randint(1, 10) + 2))
            elif cartridge == '10 Gauge Shot':
                mycartridge = Cartridge(3, "II", random.randint(1, 8))
            elif cartridge == '10 Gauge Slug':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 10) + 4))
            elif cartridge == '12 Gauge Shot':
                mycartridge = Cartridge(3, "II", random.randint(1, 6))
            elif cartridge == '12 Gauge Slug':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 10) + 6))
            elif cartridge == '16 Gauge Shot':
                mycartridge = Cartridge(3, "II", random.randint(1, 4))
            elif cartridge == '16 Gauge Slug':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 10) + 5))
            elif cartridge == '20 Gauge Shot':
                mycartridge = Cartridge(3, "II", random.randint(1, 3))
            elif cartridge == '20 Gauge Slug':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 10) + 4))
            elif cartridge == '28 Gauge Shot':
                mycartridge = Cartridge(3, "II", random.randint(1, 3))
            elif cartridge == '28 Gauge Slug':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 10) + 3))
            elif cartridge == '20x102mm':
                mycartridge = Cartridge(6, "IV", (random.randint(1, 12)+random.randint(1, 12)+random.randint(1, 12) + 10))
            elif cartridge == '4.6x30':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 10) + 1))
            elif cartridge == '5.45x39':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6)))
            elif cartridge == '5.56x45':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6)))
            elif cartridge == '5.7x28':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 10) + 1))
            elif cartridge == '500 S&W':
                mycartridge = Cartridge(3, "II", (random.randint(1, 10)+random.randint(1, 6) + 3))
            elif cartridge == '6.5mm Creedmoor':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '6.5mm Grendel':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 1))
            elif cartridge == '6.5mm Japanese':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '6.5mm Swedish':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '6.8mm SPC':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6)))
            elif cartridge == '7.5mm French':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '7.5mm Swiss':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '7.62x25 Tokarev':
                mycartridge = Cartridge(3, "II", random.randint(1, 10))
            elif cartridge == '7.62x39':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 1))
            elif cartridge == '7.62x51':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '7.62x54R':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '7mm Mauser':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '7mm Rem Mag':
                mycartridge = Cartridge(5, "III", (random.randint(1, 8)+random.randint(1, 8) + 4))
            elif cartridge == '7mm-08':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '8mm Mauser':
                mycartridge = Cartridge(4, "IIIA", (random.randint(1, 6)+random.randint(1, 6) + 4))
            elif cartridge == '9mm Luger':
                mycartridge = Cartridge(2, "IIA", random.randint(1, 10))
            elif cartridge == '9x18 Makarov':
                mycartridge = Cartridge(1, "I", (random.randint(1, 8) + 1))
            elif cartridge == '9x21mm':
                mycartridge = Cartridge(2, "IIA", random.randint(1, 10))
            elif cartridge == 'Lead Musket Ball':
                mycartridge = Cartridge(0, "None", (random.randint(1, 10) + 4))
            elif cartridge == 'Lead Pistol Ball':
                mycartridge = Cartridge(0, "None", random.randint(1, 8))
            
            #E10
            ammoCategory = {'Full Metal Jacket': 0, 'Jacketed Hollow Point': -1, 'Soft Point': -1, 'Unjacketed': -1, 'Overpressure': 1, 'Armor Piercing': 1, 
                'AP Incendiary': 1, 'Depleted Uranium': 1, 'High Explosive': 1, 'Tracer':0}
                        
            #Penalty or Bonus for stance (E12)
            if stance == 'Running':
                randStance = (random.randint(25, 35) * .01)
            elif stance == 'Walking':
                randStance = (random.randint(4, 6) * .1)
            elif stance == 'Standing':
                randStance = (random.randint(9, 10) * .1)
            elif stance == 'Kneeling':
                randStance = (random.randint(13, 14) * .1)
            elif stance == 'Sitting':
                randStance = (random.randint(135, 140) * .01)
            elif stance == 'Prone':
                randStance = (random.randint(145, 160) * .01)
            
            #Bonus for using bracing the firearm (E13)
            if 'combatBraced' in web.input():
                randBraced = (random.randint(110, 120) * .01)
            else:
                randBraced = 1
            
            #Penalty for awkward position (E14)
            if 'combatAwkward' in web.input():
                randAwkward = (random.randint(75, 85) * .01)
            else:
                randAwkward = 1
              
            
            #Calculate weapon ranges (C23)
            #Pistol first
            if weaponCategory[weapon] == 1 and distance == 0 or distance == 1:
                calculatedRange = "Point Blank"
            elif weaponCategory[weapon] == 1 and 2 <= distance <= 7:
                calculatedRange = "Close"
            elif weaponCategory[weapon] == 1 and 8 <= distance <= 25:
                calculatedRange = "Medium"
            elif weaponCategory[weapon] == 1 and 26 <= distance <= 75:
                calculatedRange = "Long"
            elif weaponCategory[weapon] == 1 and distance > 75:
                calculatedRange = "Extreme"
            #Buckshot next
            elif isBuckshot == 1 and distance == 0 or distance == 1:
                calculatedRange = "Point Blank"
            elif isBuckshot == 1 and 2 <= distance <= 7:
                calculatedRange = "Close"
            elif isBuckshot == 1 and 8 <= distance <= 25:
                calculatedRange = "Medium"
            elif isBuckshot == 1 and 26 <= distance <= 40:
                calculatedRange = "Long"
            elif isBuckshot == 1 and distance > 40:
                calculatedRange = "Extreme"
            #Shotgun slug now
            elif isSlug == 1 and distance == 0 or distance == 1:
                calculatedRange = "Point Blank"
            elif isSlug == 1 and 2 <= distance <= 10:
                calculatedRange = "Close"
            elif isSlug == 1 and 11 <= distance <= 50:
                calculatedRange = "Medium"
            elif isSlug == 1 and 51 <= distance <= 100:
                calculatedRange = "Long"
            elif isSlug == 1 and distance > 100:
                calculatedRange = "Extreme"
            #SMG next
            if weaponCategory[weapon] == 3 and distance == 0 or distance == 1:
                calculatedRange = "Point Blank"
            elif weaponCategory[weapon] == 3 and 2 <= distance <= 10:
                calculatedRange = "Close"
            elif weaponCategory[weapon] == 3 and 11 <= distance <= 50:
                calculatedRange = "Medium"
            elif weaponCategory[weapon] == 3 and 51 <= distance <= 100:
                calculatedRange = "Long"
            elif weaponCategory[weapon] == 3 and distance > 100:
                calculatedRange = "Extreme"
            #Light Rifle ranges
            if weaponCategory[weapon] == 4 and distance == 0 or distance == 1:
                calculatedRange = "Point Blank"
            elif weaponCategory[weapon] == 4 and 2 <= distance <= 50:
                calculatedRange = "Close"
            elif weaponCategory[weapon] == 4 and 51 <= distance <= 150:
                calculatedRange = "Medium"
            elif weaponCategory[weapon] == 4 and 'combatMagnification' in web.input() and 151 <= distance <= 350:
                calculatedRange = "Medium"
            elif weaponCategory[weapon] == 4 and 'combatMagnification' not in web.input() and 151 <= distance <= 350:
                calculatedRange = "Long"
            elif weaponCategory[weapon] == 4 and distance > 350:
                calculatedRange = "Extreme"
            #Medium Rifle now
            if weaponCategory[weapon] == 5 and distance == 0 or distance == 1:
                calculatedRange = "Point Blank"
            elif weaponCategory[weapon] == 5 and 2 <= distance <= 50:
                calculatedRange = "Close"
            elif weaponCategory[weapon] == 5 and 51 <= distance <= 250:
                calculatedRange = "Medium"
            elif weaponCategory[weapon] == 5  and 'combatMagnification' in web.input() and 251 <= distance <= 450:
                calculatedRange = "Medium"
            elif weaponCategory[weapon] == 5  and 'combatMagnification' not in web.input() and 251 <= distance <= 450:
                calculatedRange = "Long"
            elif weaponCategory[weapon] == 5 and distance > 450:
                calculatedRange = "Extreme"
            #Heavy Rifle is last
            if weaponCategory[weapon] == 6 and distance == 0 or distance == 1:
                calculatedRange = "Point Blank"
            elif weaponCategory[weapon] == 6 and 2 <= distance <= 400:
                calculatedRange = "Close"
            elif weaponCategory[weapon] == 6 and 401 <= distance <= 650:
                calculatedRange = "Medium"
            elif weaponCategory[weapon] == 6 and 651 <= distance <= 1500:
                calculatedRange = "Long"
            elif weaponCategory[weapon] == 6 and distance > 1500:
                calculatedRange = "Extreme"
                
            #Penalty for longer range shots (E22)
            if calculatedRange == "Point Blank":
                longerRangePenalty = 1.9
            elif calculatedRange == "Close":
                longerRangePenalty = .9
            elif calculatedRange == "Medium":
                longerRangePenalty = .75
            elif calculatedRange == "Long":
                longerRangePenalty = .5
            elif calculatedRange == "Extreme":
                longerRangePenalty = .25
            
            #Decrease accuracy for full auto at long range (ShotType!E1)
            if calculatedRange == "Point Blank":
                randLongRange = 1
            elif calculatedRange == "Close":
                randLongRange = 1
            elif calculatedRange == "Medium":
                randLongRange = .8
            elif calculatedRange == "Long":
                randLongRange = .6
            elif calculatedRange == "Extreme":
                randLongRange = .4
            
            #Penalty for fast or bad aim (E16)
            if shotType == 'Aimed, Slow':
                randShotType = (random.randint(9, 11) * .1)
            elif shotType == 'Aimed, Rapid':
                randShotType = (random.randint(8, 10) * .1)
            elif shotType ==  'Aimed, Auto':
                randShotType = ((random.randint(7, 9) * .1) * randLongRange)
            elif shotType == 'Point Shooting, Slow':
                randShotType = (random.randint(7, 9) * .1)
            elif shotType == 'Point Shooting, Rapid':
                randShotType = (random.randint(65, 85) * .01)
            elif shotType == 'Point Shooting, Auto':
                randShotType = ((random.randint(4, 6) * .1) * randLongRange)
            elif shotType == 'Blind Fire, Slow':
                randShotType = (random.randint(5, 20) * .01)
            elif shotType == 'Blind Fire, Rapid':
                randShotType = (random.randint(5, 20) * .01)
            elif shotType == 'Blind Fire, Auto':
                randShotType = ((random.randint(5, 20) * .01) * randLongRange)
            else: #'Suppression Fire' 
                ((random.randint(6, 12) * .01) * randLongRange)
                
            #Penalty for hard-to-see targets (E17)
            if weaponCategory[weapon] == 6:
                highCaliberCoverPenetration = .15
            else:
                highCaliberCoverPenetration = 0
                
            if difficulty == 'Full Visibility':
                randDifficulty = (random.randint(9, 11) * .1)
            elif difficulty == 'Partial Visibility':
                randDifficulty = (random.randint(65, 70) * .01)
            elif difficulty == 'Partial Concealment':
                randDifficulty = (random.randint(55, 75) * .01)
            elif difficulty == 'Partial Cover':
                randDifficulty = (random.randint(55, 75) * .01)
            elif difficulty == "Full Concealment":
                randDifficulty = (random.randint(10, 20) * .1)
            elif difficulty == "Full Cover":
                randDifficulty = 0 + highCaliberCoverPenetration
                
            #Penalty for moving targets (E18)
            if motion == 'Motionless':
                randMotion = (random.randint(9, 11) * .1)
            elif motion == 'Moving Slowly':
                randMotion = (random.randint(8, 9) * .1)
            elif motion == 'Moving Quickly':
                randMotion = (random.randint(65, 75) * .01)
            elif motion == 'Moving Erratically':
                (random.randint(55, 70) * .01)
                
            #Long range buckshot penalty (G7)
            if calculatedRange == "Point Blank" or "Close":
                longRangeBuckPenalty = 1
            elif calculatedRange == "Medium":
                longRangeBuckPenalty = (random.randint(65, 85) * .01)
            elif calculatedRange == "Long":
                longRangeBuckPenalty = (random.randint(4, 6) * .1)
            elif calculatedRange == "Extreme":
                (random.randint(15, 35) * .01)
            
            #Penetration calculator (G10)
            penetrationCalculator = (mycartridge.strength + ammoCategory[ammo] + addSMGPenetration)
            
            #Armor rating (G12)
            if armor == "Level IV":
                armorRating = 6
            elif armor == "Level III":
                armorRating = 5
            elif armor == "Level IIIA":
                armorRating = 4
            elif armor == "Level II":
                armorRating = 3
            elif armor == "Level IIA":
                armorRating = 2
            elif armor == "Level I":
                armorRating = 1
            else: #unarmored
                armorRating = 0

            #Raw hits calculator (E24)
            #rawHits = math.floor(int(shots) * int(longerRangePenalty) * int(randStock) * int(randGrip) * int(randAkimbo) * int(randStance) * int(randBraced) * int(randAwkward) * int(randShotType) * int(randDifficulty) * int(randMotion) * int(multiplier))
            preHits = math.floor(shots * longerRangePenalty * randStock * randGrip * randAkimbo * randStance * randBraced * randAwkward * randShotType * randDifficulty * randMotion * multiplier)
            rawHits = int(preHits)

            #Total hits calcultor (B27)
            if isBuckshot == 0:
                if rawHits > shots:
                    subtotalHits = math.floor(shots * projectilesPerShot)
                else:
                    subtotalHits = math.floor(rawHits * projectilesPerShot)
            else:
                if rawHits > shots:
                    subtotalHits = math.floor(shots * projectilesPerShot * longRangeBuckPenalty)
                else:
                    subtotalHits = math.floor(rawHits * projectilesPerShot * longRangeBuckPenalty)
            totalHits = int(subtotalHits)
                    
            #Called shot calculator (E20 & B28)
            calledShot = 0
            if isBuckshot == 0:
                if (int(totalHits) / int(shots)) > .94:
                    calledShot = random.randint(1,2)
                else:
                    calledShot = 0
            elif calculatedRange == "Point Blank" or calculatedRange == "Close":
                calledShot = random.randint(1,2)
            else:
                calledShot = 0
            
            if calledShot == 1:
                calledShotCalculator = 1
            else:
                calledShotCalculator = 0
            
            #Called shot string generator
                if calledShotCalculator == 1:
                    calledShotString = ". You can use a CALLED SHOT"
                else:
                    calledShotString = ""
            
            #Raw damage calculator (G13)
            rawDamage = (totalHits * mycartridge.damage)
            
            #Damage multiplier (G15)
            armorEffectiveness = (armorRating - penetrationCalculator) #(G14)
            if armorRating == 0:
                damageMultiplier = 1
            elif armorEffectiveness == 1:
                damageMultiplier = .25
            elif armorEffectiveness == 0:
                damageMultiplier = .5
            elif armorEffectiveness == -1:
                damageMultiplier = .75
            elif armorEffectiveness < -1:
                damageMultiplier = 1
            else:
                damageMultiplier = 0
            
            #Unarmored damage modifier (G17)
            if armorRating == 0:
                if ammoCategory[ammo] == -1:
                    unarmoredDamageModifier = 1.5
                elif ammoCategory[ammo] == 0:
                    unarmoredDamageModifier = 1
                else:
                    unarmoredDamageModifier = .5
            else:
                unarmoredDamageModifier= 1
                    
            #Total damage calculator (B30)
            totalDamage = int(math.floor((rawDamage * damageMultiplier) * unarmoredDamageModifier))
            
            comments = "At %s Range, you manage hit your target %s times, doing %s damage%s!" % (calculatedRange, totalHits, totalDamage, calledShotString)
            #debug = "penetrationCalculator=%s, calledShotCalculator=%s, longerRangePenalty=%s, rawHits=%s, totalHits=%s, totalDamage=%s, isBuckshot=%s, isSlug=%s, longRangeBuckPenalty=%s, addSMGPenetration=%s, projectilesPerShots=%s, highCaliberCoverPenetration=%s, calculatedRange=%s" % (penetrationCalculator, calledShotCalculator, longerRangePenalty, rawHits, totalHits, totalDamage, isBuckshot, isSlug, longRangeBuckPenalty, addSMGPenetration, projectilesPerShot, highCaliberCoverPenetration, calculatedRange)
            #debug = "shots=%s, longerRangePenalty=%s, randStock=%s, randGrip=%s, randAkimbo=%s, randStance=%s, randBraced=%s, randAwkward=%s, randShotType=%s, randDifficulty=%s, randMotion=%s, multiplier=%s" % (shots, longerRangePenalty, randStock, randGrip, randAkimbo, randStance, randBraced, randAwkward, randShotType, randDifficulty, randMotion, multiplier)
            #debug = "magnification=%s, stock=%s, grip=%s, akimbo=%s, braced=%s, awkward=%s" % (form["combatMagnification"].value, form["combatStock"].value, form["combatGrip"].value, form["combatAkimbo"].value, form["combatBraced"].value, form["combatAwkward"].value)
            #debug = web.input()
            #debug = "weapondamage=%s, armorRating=%s, penetrationCalc=%s, armorEfctvnss=%s, rawdamage=%s, damageMult=%s, unarmoredDamMod=%s" % (mycartridge.damage, armorRating, penetrationCalculator, armorEffectiveness, rawDamage, damageMultiplier, unarmoredDamageModifier)
            
            return render.combat(form, comments, debug)
            
            
class failure:
    def GET(self): 
        form = failureform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.failure(form, comments)

    def POST(self): 
        # if you lose any SAN, you get FAILEDSAN happen to you.
        # if you lose 5 SAN or 1/5 SAN: amend description, bout of madness.
        form = failureform() 
        if not form.validates(): 
            return render.failure(form, comments)
        else:
            dropdown = form["failureDropDown"].value
            coinFlip = random.randint(1,2)
            firearm = {1: 'Double feed!', 2: 'Failure to extract!', 3: 'Failure to feed!', 4: 'Stovepipe!', 5: 'Out of battery!', 6: 'Slamfire!', 7:'Hangfire!', 8:'Dud round!'}
            catastrophicFirearm = {1: 'Squib!', 2: 'Explosion!'}
            melee = {1: 'Your foot slips!', 2: 'Your weapon gets stuck!', 3: 'You drop your weapon!', 4: 'Your enemy parries and disarms you!', 5: 'You fall on your ass!'}
            catastrophicMelee = {1: 'Your weapon breaks!', 2: 'Like a balloon! When something bad happens!'}
            
            failedSAN = {1: 'You jump in fright and drop something (spectacles, flashlight, gun, book, etc.)!', 2: 'You cry out in terror (drawing attention or saying something inappropriate)!',
                3: 'You move involuntarily (swerving the wheel, throwing your hands up in horror, cringing)!', 4: 'Involuntary combat action (lashing out with a fist, squeezing a trigger, taking shelter behind someone else.)!',
                5: 'You freeze in place, staring disbelievingly for a moment but take no action!'}
            amendDesc = {1: 'Personal Description: Suitable entries might include "Wild-eyed," "Thousand-yard stare," "World-weary," or "No longer cares for their own appearance".', 
                2: 'Ideology/Beliefs: A balanced entry such as "religious" might be changed to something more extreme or deranged, such as "Unbelievers must be converted or made to suffer". Alternatively, a new entry that is appropriate to the situation might be made, such as "Obsessed with defeating the Cthulhu cult"',
                3: 'Significant People: A new name might be added together with a reason for its inclusion. For example, "Can\'t rest until Delbert Smith is in his grave," or "Robin Poole is the incarnation of Ganesh."',
                4: 'Meaningful Locations: The present location might take on great significance, or the investigator might become fixated on reaching another location for either rational or irrational reasons. The former might be the cult temple in the jungle; the latter might be an overpowering desire to visit Graceland.',
                5: 'Treasured Possessions: It is easy to lose possessions while one\'s mind is disrupted by insanity. Any possessions might be erased or noted as lost. A new possession might be acquired and given great significance.',
                6: 'Traits: A trait might be erased or altered to something more suitable; for example: "bully," "drug addict," "easily distracted," "talks too loud," "lack of inhibitions.',
                7: 'Arcane Tomes, Spells and Artifacts: Such items might be lost or destroyed in a fit of pique. The investigator might involuntarily cast any spells that they know, activate artifacts, or study a tome that they had previously shunned.'}
            phobias = {1: 'Ablutophobia: Fear of washing or bathing', 2: 'Acrophobia: Fear of heights', 3: 'Aerophobia: Fear of flying', 4: 'Agoraphobia: Fear of open, public (crowded) places', 5: 'Alektorophobia: Fear of chickens', 6: 'Alliumphobia: Fear of garlic', 7: 'Amaxophobia: Fear of being in or riding in vehicles',
                8: 'Ancraophobia: Fear of wind', 9: 'Androphobia: Fear of men', 10: 'Anglophobia: Fear of England or English culture, etc.', 11: 'Anthrophobia: Fear of flowers', 12: 'Apotemnophobia: Fear of people with amputations', 13: 'Arachnophobia: Fear of spiders', 14: 'Astraphobia: Fear of lightning', 
                15: 'Atephobia: Fear of ruin or ruins', 16: 'Aulophobia: Fear of flutes', 17: 'Bacteriophobia: Fear of bacteria', 18: 'Ballistophobia: Fear of missiles or bullets', 19: 'Basophobia: Fear of falling', 20: 'Bibliophobia: Fear of books', 21: 'Botanophobia: Fear of plants', 
                22: 'Caligynephobia: Fear of beautiful women', 23: 'Cheimaphobia: Fear of cold', 24: 'Chronomentrophobia: Fear of clocks', 25: 'Claustrophobia: Fear of confined spaces', 26: 'Coulrophobia: Fear of clowns', 27: 'Cynophobia: Fear of dogs',  28: 'Demonophobia: Fear of spirits or demons', 
                29: 'Demophobia: Fear of crowds', 30: 'Dentophobia: Fear of dentists', 31: 'Disposophobia: Fear of throwing stuff out (hoarding)', 32: 'Doraphobia: Fear of fur', 33: 'Dromophobia: Fear of crossing streets', 34: 'Ecclesiophobia: Fear of church', 35: 'Eisoptrophobia: Fear of mirrors', 
                36: 'Enetophobia: Fear of needles or pins', 37: 'Entomophobia: Fear of insects', 38: 'Felinophobia: Fear of cats', 39: 'Gephyrophobia: Fear of crossing bridges', 40: 'Gerontophobia: Fear of old people or of growing old', 41: 'Gynophobia: Fear of women', 42: 'Haemaphobia: Fear of blood', 
                43: 'Hamartophobia: Fear of sinning', 44: 'Haphophobia: Fear of touch', 45: 'Herpetophobia: Fear of reptiles', 46: 'Homichlophobia: Fear of fog', 47: 'Hoplophobia: Fear of firearms', 48: 'Hydrophobia: Fear of water', 49: 'Hypnophobia: Fear of sleep or of being hypnotized', 
                50: 'Iatrophobia: Fear of doctors', 51: 'Ichthyophobia: Fear of fish', 52: 'Katsaridaphobia: Fear of cockroaches', 53: 'Keraunophobia: Fear of thunder', 54: 'Lachanophobia: Fear of vegetables', 55: 'Ligyrophobia: Fear of loud noises', 56: 'Limnophobia: Fear of lakes', 57: 'Mechanophobia: Fear of machines or machinery', 
                58: 'Megalophobia: Fear of large things', 59: 'Merinthophobia: Fear of being bound or tied up', 60: 'Meteorophobia: Fear of meteors or meteorites', 61: 'Monophobia: Fear of being alone', 62: 'Mysophobia: Fear of dirt or contamination', 63: 'Myxophobia: Fear of slime', 64: 'Necrophobia: Fear of dead things', 
                65: 'Octophobia: Fear of the figure 8', 66: 'Odontophobia: Fear of teeth', 67: 'Oneirophobia: Fear of dreams', 68: 'Onomatophobia: Fear of hearing a certain word or words', 69: 'Ophidiophobia: Fear of snakes', 70: 'Ornithophobia: Fear of birds', 71: 'Parasitophobia: Fear of parasites', 
                72: 'Pediophobia: Fear of dolls', 73: 'Phagophobia: Fear of swallowing, of eating or of being eaten', 74: 'Pharmacophobia: Fear of drugs', 75: 'Phasmophobia: Fear of ghosts', 76: 'Phenogophobia: Fear of daylight', 77: 'Pogonophobia: Fear of beards', 78: 'Potamophobia: Fear of rivers', 
                79: 'Potophobia: Fear of alcohol or alcoholic beverages', 80: 'Pyrophobia: Fear of fire', 81: 'Rhabdophobia: Fear of magic', 82: 'Scotophobia: Fear of darkness or of the night', 83: 'Selenophobia: Fear of the moon', 84: 'Siderodromophobia: Fear of train travel', 85: 'Siderophobia: Fear of stars', 
                86: 'Stenophobia: Fear of narrow things or places', 87: 'Symmetrophobia: Fear of symmetry', 88: 'Taphephobia: Fear of being buried alive or of cemeteries', 89: 'Taurophobia: Fear of bulls', 90: 'Telephonophobia: Fear of telephones', 91: 'Teratophobia: Fear of monsters', 92: 'Thalassophobia: Fear of the sea', 
                93: 'Tomophobia: Fear of surgi- cal operations', 94: 'Triskadekaphobia: Fear of the number 13', 95: 'Vestiphobia: Fear of clothing', 96: 'Wiccaphobia: Fear of witches and witchcraft', 97: 'Xanthophobia: Fear of the color yellow or the word "yellow"', 98: 'Xenoglossophobia: Fear of foreign languages', 
                99: 'Xenophobia: Fear of strangers or foreigners', 100: 'Zoophobia: Fear of animals'}
            manias = {1: 'Ablutomania: compulsion for washing oneself', 2: 'Aboulomania: pathological indecisiveness', 3: 'Achluomania: an excessive liking for darkness', 4: 'Acromaniaheights: compulsion for high places', 5: 'Agathomania: pathological kindness', 6: 'Agromania: intense desire to be in open spaces', 
                7: 'Aichmomania: obsession with sharp or pointed objects', 8: 'Ailuromania: abnormal fondness for cats', 9: 'Algomania: obsession with pain', 10: 'Alliomania: obsession with garlic', 11: 'Amaxomania: obsession with being in vehicles', 12: 'Amenomania: irrational cheerfulness', 
                13: 'Anthomania: obsession with flowers', 14: 'Arithmomania: obsessive preoccupation with numbers', 15: 'Asoticamania: impulsive or reckless spending', 16: 'Automania: an excessive liking for solitude', 17: 'Balletomania: abnormal fondness for ballet', 18: 'Bibliokleptomania: compulsion for stealing books', 
                19: 'Bibliomania: obsession with books and/or reading', 20: 'Bruxomania: compulsion for grinding teeth', 21: 'Cacodemomania: pathological belief that one is inhabited by an evil spirit', 22: 'Callomania: obsession with one\'s own beauty', 23: 'Cartacoethes: uncontrollable compulsion to see maps everywhere', 
                24: 'Catapedamania: Obsession with jumping from high places', 25: 'Cheimatomania: abnormal desire for cold and/or cold things', 26: 'Choreomania: dancing mania or uncontrollable frenzy', 27: 'Clinomania: excessive desire to stay in bed', 28: 'Coimetromania: obsession with cemeteries', 
                29: 'Coloromania: obsession with a specific color', 30: 'Coulromania: obsession with clowns', 31: 'Countermania: compulsion to experience fearful situations', 32: 'Dacnomania: obsession with killing', 33: 'Demonomania: pathological belief  that one is possessed by demons', 34: 'Dermatillomania: compulsion for picking at one\'s skin', 
                35: 'Dikemania: obsession to see justice done', 36: 'Dipsomania: abnormal craving for alcohol', 37: 'Doramania: obsession with owning furs', 38: 'Doromania: obsession with giving gifts', 39: 'Drapetomania: compulsion for running away', 40: 'Ecdemiomania: compulsion for wandering', 
                41: 'Egomania: irrational self-centered attitude or self-worship', 42: 'Empleomania: Insatiable urge to hold office', 43: 'Enosimania: pathological belief that one has sinned', 44: 'Epistemomania: obsession for acquiring knowledge', 45: 'Eremiomania: compulsion for stillness', 46: 'Etheromania: craving for ether', 
                47: 'Gamomania: obsession with issuing odd marriage proposals', 48: 'Geliomania: uncontrollable compulsion to laugh', 49: 'Goetomania: obsession with witches and witchcraft', 50: 'Graphomania: obsession with writing everything down', 51: 'Gymnomania: compulsion with nudity', 52: 'Habromania: abnormal tendency to create pleasant delusions (in spite of reality)', 
                53: 'Helminthomania: an excessive liking for worms', 54: 'Hoplomania: obsession with firearms', 55: 'Hydromania: irrational craving for water', 56: 'Ichthyomania: obsession with fish', 57: 'Iconomania: obsession with icons or portraits', 58: 'Idolomania: obsession or devotion to an idol', 
                59: 'Infomania: excessive devotion to accumulating facts', 60: 'Klazomania: irrational compulsion to shout', 61: 'Kleptomania: irrational compulsion for stealing', 62: 'Ligyromania: uncontrollable compulsion to make loud or shrill noises', 63: 'Linonomania: obsession with string', 64: 'Lotterymania: an extreme desire to take part in lotteries', 
                65: 'Lypemania: an abnormal tendency toward deep melancholy', 66: 'Megalithomania: abnormal tendency to compose bizarre ideas when in the presence of stone circles/standing stones', 67: 'Melomania: obsession with music or a specific tune', 68: 'Metromania: insatiable desire for writing verse', 
                69: 'Misomania: hatred of everything, obsession of hating some subject or group', 70: 'Monomania: abnormal obsession with a single thought or idea', 71: 'Mythomania: lying or exaggerating to an abnormal extent', 72: 'Nosomania: delusion of suffering from an imagined disease', 73: 'Notomania: compulsion to record everything (e.g. photograph)', 
                74: 'Onomamania: obsession with names (people, places, things)', 75: 'Onomatomania: irresistible desire to repeat certain words', 76: 'Onychotillomania: compulsive picking at the fingernails', 77: 'Opsomania: abnormal love for one kind of food', 78: 'Paramania: an abnormal pleasure in complaining', 
                79: 'Personamania: compulsion to wear masks', 80: 'Phasmomania: obsession with ghosts', 81: 'Phonomania: pathological tendency to murder', 82: 'Photomania: pathological desire for light', 83: 'Planomania: abnormal desire to disobey social norms', 84: 'Plutomania: obsessive desire for wealth', 
                85: 'Pseudomania: irrational compulsion for lying', 86: 'Pyromania: compulsion for starting fires', 87: 'Question-Asking Mania: compulsive urge to ask questions', 88: 'Rhinotillexomania: compulsive nose picking', 89: 'Scribbleomania: obsession with scribbling/doodling', 90: 'Siderodromomania: intense fascination with trains and railroad travel', 
                91: 'Sophomania: the delusion that one is incredibly intelligent', 92: 'Technomania: obsession with new technology', 93: 'Thanatomania: belief that one is cursed by death magic', 94: 'Theomania: belief that he or she is a god', 95: 'Titillomaniac: compulsion for scratching oneself', 96: 'Tomomania: irrational predilection for performing surgery', 
                97: 'Trichotillomania: craving for pulling out own hair', 98: 'Typhlomania: pathological blindness', 99: 'Xenomania: obsession with foreign things', 100: 'Zoomania: insane fondness for animals'}
            boutOfMadnessRealTime = {1: 'Amnesia: The investigator has no memory of events that have taken place since they were last in a place of safety. For example, it seems to them that one moment they were eating breakfast and the next they are facing a monster.', 
                2: 'Psychosomatic disability: The investigator suffers psychosomatic blindness, deafness, or loss of the use of a limb or limbs.', 
                3: 'Violence: A red mist descends on the investigator and they explode in a spree of uncontrolled violence and destruction directed at their surroundings, allies or foes alike.', 
                4: 'Paranoia: The investigator suffers severe paranoia; everyone is out to get them; no one can be trusted; they are being spied on; someone has betrayed them; what they are seeing is a trick.', 
                5: 'Significant Person: Review the investigator\'s backstory entry for Significant People. The investigator mistakes another person in the scene for their Significant Person. Consider the nature of the relationship; the investigator acts upon it.', 
                6: 'Faint: The investigator faints.', 
                7: 'Flee in panic: The investigator is compelled to get as far away as possible by whatever means are available, even if it means taking the only vehicle and leaving everyone else behind.', 
                8: 'Physical hysterics or emotional outburst: The investigator is incapacitated from laughing, crying, screaming, etc.',
                9: 'Phobia: Investigator gains a new phobia. Even if the source of the phobia is not present, the investigator imagines it is there: ' + phobias[random.randint(1,len(phobias))],
                10: 'Mania: The investigator gains a new mania. The investigator seeks to indulge in their new mania: ' + manias[random.randint(1,len(manias))]}
            boutofMadnessSummary = {1: 'Amnesia: The investigator comes to their senses in some unfamiliar place with no memory of who they are. Their memories will slowly return to them over time.', 
                2: 'Robbed: The investigator comes to their senses 1D10 hours later, having been robbed. They are unharmed. If they were carrying a Treasured Possession (see investigator backstory), make a Luck roll to see if it was stolen. Everything else of value is automatically missing.', 
                3: 'Battered: The investigator comes to their senses 1D10 hours later to find themselves battered and bruised. Hit points are reduced to half of what they were before going insane, though this does not cause a Major wound. They have not been robbed. How the damage was sustained is up to the Keeper', 
                4: 'Violence: The investigator explodes in a spree of violence and destruction. When the investigator comes to their senses, their actions may or may not be apparent or remembered. Who or what the investigator has inflicted violence upon and whether they have killed or simply inflicted harm is up to the Keeper.', 
                5: 'Ideology/Beliefs: Review the investigator\'s backstory entry for Ideology and Beliefs. The investigator manifests one of these in an extreme, crazed and demonstrative manner. For example, a religious person might be found later, preaching the gospel loudly on the subway.', 
                6: 'Significant People: Consult the investigator\'s backstory entry for Significant People and why the relationship is so important. In the time that passes (1D10 hours or more) the investigator has done their best to get close to that person and act upon their relationship in some way', 
                7: 'Institutionalized: The investigator comes to their senses in a psychiatric ward or police cell. They may slowly recall the events that led them there.', 
                8: 'Flee in panic: When the investigator comes to their senses they are far away, perhaps lost in the wilderness or on a train or long-distance bus.',
                9: 'Phobia: The investigator gains a new phobia. The investigator comes to their senses 1D10 hours later, having taken every precaution to avoid their new phobia: ' + phobias[random.randint(1,len(phobias))],
                10: 'Mania: The investigator gains a new mania. The investigator comes to their senses 1D10 hours later. During this bout of madness, the investigator will have been fully indulging in their new mania. Whether this is apparent to other people is up to the Keeper and player: ' + manias[random.randint(1,len(manias))]}
            
            
            if dropdown == 'Botched a firearm attack' and coinFlip == 1:
                comments = "Lasts for 1 combat round: " + firearm[random.randint(1,len(firearm))]
            elif dropdown == 'Botched a firearm attack' and coinFlip == 2:
                comments = "Takes firearm out of commission until it can be repaired: " + catastrophicFirearm[random.randint(1,len(catastrophicFirearm))]
            elif dropdown == 'Botched a melee combat roll' and coinFlip == 1:
                comments = "Lasts for 1 combat round: " + melee[random.randint(1,len(melee))]
            elif dropdown == 'Botched a melee combat roll' and coinFlip == 2:
                comments = "Takes weapon out of commission until it can be repaired: " + catastrophicMelee[random.randint(1,len(catastrophicMelee))]
            elif dropdown == 'Failed any SAN roll':
                comments = "Lasts for 1 combat round: " + failedSAN[random.randint(1,len(failedSAN))]
            elif dropdown == 'Lost 5 SAN at once or 1/5 or more SAN in a day (Realtime)':
                comments = "Amend backstory: " + amendDesc[random.randint(1,len(amendDesc))] + " DM controls player for 1D10 combat rounds (about a minute). Then the underlying insanity lasts 1D10 hours for Temporary Insanity; longer for Indefinite Insanity: " + boutOfMadnessRealTime[random.randint(1,len(boutOfMadnessRealTime))]
            elif dropdown == 'Lost 5 SAN at once or 1/5 or more SAN in a day (Summary)':
                comments = "Amend backstory: " + amendDesc[random.randint(1,len(amendDesc))] + " Basically a fast-forward for 1D10 hours. If Temporary Insanity, it\'s done now. If Indefinite Insanity, it\'s still happening: " + boutofMadnessSummary[random.randint(1,len(boutofMadnessSummary))]
            
            return render.failure(form, comments)
                    
if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()