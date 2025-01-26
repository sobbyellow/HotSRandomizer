import os
import random
import xml.etree.ElementTree as ET
from textwrap import indent
from enum import Enum
import datetime

HERO_XML_DIR = "hero_xmls"
OUTPUT_FILE = "randomized.xml"
DEBUG = True
debug_messages = []
last_messages = []

class Debug(Enum):
    INFO = "\033[94m[Info]\033[0m"        # Blue
    WARNING = "\033[93m[Warning]\033[0m"  # Yellow
    ERROR = "\033[91m[Error]\033[0m"      # Red
    SUCCESS = "\033[32m[Success]\033[0m"  # Green
    NONE = ""

# Excluded abilities for randomization
EXCLUDED_ABILITIES = {
    "Attack", "attack", "Move", "move", "Stop", "stop", "HeroGenericSummonedUnitSpecialCaseInteraction", "SummonedUnitSpecialCaseInteraction", "MoveHoldPosition", "MovePatrol", "MoonwellDrink", "Cancel", "AcquireMove", "None", "BuildInProgress", "AbathurAssumingDirectControlCancel", "HearthstoneNoMana", "LockedHeroicAbility", "LootConsumableThrow", "SummonedMount", "AttackTowards", "Dance", "Dismount", "ZombieMorph", "SmartCommandUnitInteraction", "UnsummonMount", "CaptureMacGuffin", "AttackAlly", "AnubarakBurrowChargeCancel", "LockedHeroicAbilityChromie", "AnubarakBurrowChargeCancel", "SamuroImageTransmissionDummyShopAbility", "GallDoubleBackAbility", "RagnarosBigRagReturnMoltenCore", "FalstadHammerangBOOMerangActive", "GallOgreRageActivated", "MurkyCancelMarchoftheMurlocs", "ZagaraPassiveUIImproved", "ZagaraPassiveUI", "DeckardStayAWhileAndListenCancel", "MedicMedivacDropshipDepart", "BarbarianFuryShotOfFury", "LostVikingsLockedAbilityE", "AmazonCancelFend", "LeoricDrainEssence", "LucioCrossfadeActivateSpeedBoost", "LeoricGhastlySwing", "LeoricCancelWraithWalk", "MalGanisNightRushCancel", "MedicRedirectHealingBeam", "AzmodanAllShallBurnCancel", "KaelthasVerdantSpheresActive", "ButcherRuthlessOnslaughtCancel", "KelThuzadChainsLink", "BarbarianWhirlwindCancel", "JainaWaterElementalFrostbolt", "JainaWaterElementalConeOfCold", "JainaWaterElementalBlizzard", "RagnarosEmpowerSulfurasActive", "FenixPlanetCrackerCancel", "DeckardHoradricCubeCharging", "HoggerCancelHoggWild", "WizardArchonPurePowerDisintegrateCancel", "SgtHammerTankMode", "LostVikingsNordicAttackSquad", "TassadarForceWallCancel", "DeathwingMoltenFlameCancel", "KelThuzadChainsPull", "MonkBlankTrait", "LiLiCancelJugof1000Cups", "LostVikingsJump", "ZeratulVoidPrisonCancel", "SylvanasHauntingWaveActivate", "LockedHeroicAbilityVarian", "AnaAimDownSightsDeactivate", "LostVikingsLockedAbilityW", "ChoSurgingFistTriggerButton", "GarroshArmorUpDoubleUp", "SylvanasWailingArrowActivate", "EvolveMonstrosityActiveHotbar", "WhitemaneInquisitionCancel", "LostVikingsSpinToWin", "TychusOverkillRetarget", "SylvanasHauntingWaveActivateFree", "IllidanBetrayersThirstThrillOfBattle", "LucioCrossfadeActivateHealingBoost", "KaelthasPhoenixRetarget", "HoggerDestroyLootHoard", "ZeratulMightOfTheNerazimPassive", "RagnarosBigRagExplosiveRune", "LostVikingsVikingBribery", "ChromieDetonateTimeTrap", "MedivhPortalCancel", "LostVikingsLockedAbilityQ", "MalGanisFelClawsThird", "RagnarosBigRagMeteorShower", "RagnarosBigRagMoltenSwing", "RagnarosBigRagCancelReturnMoltenCore", "RagnarosBigRagSulfurasSmash", "DVaPilotTorpedoDashAbility", "NecromancerCursedStrikesPassive", "MeiOWCryoFreezeCancel", "LostVikingsMortar", "ArthasFrozenTempestDeactive", "DeckardLorenadoKnockback", "RagnarosLivingMeteorShiftingMeteorRedirect", "GenjiDragonbladeAttack", "WizardDisintegrateCancel", "LeoricEntombCancel", "DeathwingDestroyer", "DeathwingWorldbreaker", "DeathwingSkyfallActive", "ZuljinCancelBerserker", "WitchDoctorZombieWallCancel", "DiabloLightningBreathCancel", "LostVikingsNorseForce", "UtherFlashofLight", "YrelRighteousHammer", "YrelAvengingWrath", "KerriganUltraliskCharge", "DeckardFortitudeOfTheFaithfulAncientBlessings", "DVaPilotConcussivePulseAbility", "WizardArchonPurePowerDisintegrate", "DVaMechCancelBoosters", "GuldanDrainLifeCancel", "TychusCommandeerOdinRagnarokMissilesTargeted", "FirebatCombustionCancel", "BarbarianLeapArreatCraterCancel", "ZuljinRegenerationForestMedicine", "ArthasFrostmourneHungersPrimed", "TychusCommandeerOdinAnnihilate", "ArthasArmyOfTheDeadSacrifice", "DVaRetargetDefenseMatrix", "MedivhPortal2", "ChenEarth", "ChenFire", "ChenStorm", "SylvanasMindControlCancel", "AnaEyeOfHorusCancel", "BrightwingBlinkHealDoubleWyrmholeDash", "TychusRunAndGunOverkill", "MaievSpiritOfVengeanceBlink", "ZeratulWormhole", "JainaCommandWaterElemental", "MaievContainmentDiscContain", "MedicDetonateDisplacementGrenade", "DryadWispRedirect", "AlexstraszaPreservation", "MuradinSecondWindActivateable", "WitchDoctorRavenousSpiritCancel", "DvaCancelDefenseMatrix", "WitchDoctorGargantuanStomp", "TyraelElDruinsMightEldruinsFlash", "AbathurSymbioteCarapace", "JunkratRIPTireJump", "RuthlessOnslaughtCharge", "SamuroCancelBladestorm", "DVaPilotCallMech", "MeiOWIcingCancel", "SgtHammerNapalmStrikeSiege", "SgtHammerSpiderMinesSiegeMode", "KelThuzadDeathAndDecayShade", "MonkDeadlyReachActive", "TychusOdinThrusters", "LiLiCloudSerpentAttack", "TassadarResonanceBeamArcDischargeDummy", "ThrallFrostwolfsGrace", "AlexstraszaCleansingFlameDragonqueen", "AbathurSymbioteSpikeBurst", "AlarakUnleashDeadlyCharge", "AlarakDeadlyCharge2ndHeroicSadism", "AlarakCounterStrike2ndHeroicSadism", "GazloweDethLazorFirinMahLazorz", "FirebatBunkerDropFlamethrower", "AmazonSurgeOfLight", "NecromancerHasSpectralScytheActivePassiveUseDisallow", "TychusMinigun", "FalstadHammerang", "FenixRepeaterCannon", "ZeratulCleaveMightOfTheNerazim", "ChromiePastAndFutureMeSandBlast", "TassadarArchonActive", "AzmodanTideOfSinPassive", "ZeratulBlinkMightoftheNerazim", "ZeratulSingularitySpikeMightoftheNerazim", "MedivhLeyLineSealRedirect", "HanzoPOTGActivate", "ImperiusAngelicArmamentsLaunchMissiles", "SamuroIllusionMasterNoTarget", "AnaEyeOfHorusAttackDummy", "RaynorRaynorsRaidersIssueAttackOrder", "ZeratulShadowAssault", "AnaEyeOfHorusHighPoweredRound", "DVaBunnyHopOff", "GallShadowBoltVolleyMoltenBlockDummy", "GallTwistingNetherActivated", "GallShiftingNether", "AurielResurrectSelf", "DVaPilotBigShot", "YrelDivinePurposeActive", "AlexstraszaWingBuffet", "GreymaneRazorSwipe", "VarianHeroicStrikeActive", "YrelVindicationCast", "FirebatBunkerDropFortifiedBunkerOilSpill"
}
excluded_abilities = []
EXCLUDED_RELATED_ABILITIES = {
    "WitchDoctorGargantuanStomp"
}
# Temporary disabled until they're fixed maybe
TEMP_EXCLUDED_ABILITIES = {
}

# Excluded face/abilCmd combinations
EXCLUSION_PATTERNS = {
    "RexxarMishaChargeRedirect": ["RexxarMishaCharge"],
    "JainaConeOfCold": ["WaterElemental"],
    "JainaFrostbolt": ["WaterElemental"],
}
# Excluded face/abilCmd combinations in specific slot (Slot, Face): [AbilCmd]
EXCLUSION_SLOTS = {
    ("Ability1", "AbathurLocustStrain"): ["AbathurSpawnLocusts"],
    ("Ability1", "SgtHammerBluntForceGun"): ["SgtHammerBluntForceGun"],
    ("Ability1", "WitchDoctorGargantuanStomp"): ["WitchDoctorGargantuanStomp"],
    ("Ability1", "AnaEyeOfHorusHighPoweredRound"): ["AnaEyeOfHorusAttackDummy"],
    ("Passive", "TassadarArchon"): [""]
}
# Excluded behaviors
EXCLUDED_BEHAVIORS = {
    "RavenousSoulsChannel", "SylvanasHauntingWaveWindrunnerCaster", "SylvanasHauntingWaveCaster", "MalGanisNightRushCaster", "DeathwingDragonflightBuff", "KaelthasPhoenixTimedLife", "AlarakDeadlyChargeChanneling", "ValeeraStealthCloak", "DeckardStayAWhileAndListenCasterBehavior", "StormEarthFireCasterBehavior", "L90ETCMoshPitChannel", "DiabloLightningBreathChanneledCoolup", "DiabloLightningBreathController", "FenixPlanetCrackerCasterBehavior", "MalGanisCarrionSwarmDelay", "AzmodanAllShallBurnChannel", "AzmodanAllShallBurnChannelMarchOfSin", "AzmodanAllShallBurnChanneledCoolup", "UsingVehicle", "BrightwingBlinkHealDoubleWyrmholeFreeCast", "MalGanisFelClawsTimer", "MalGanisFelClawsThirdCastTimer", "PassiveBuffWeaponSiegeModeRelic", "SiegeModeRelic", "MaelstromCannonSiegeMode", "SiegeMode", "PassiveBuffWeaponSiegeMode", "DehakaBurrowChannel", "WhitemaneInquisitionCasterChannelBehavior", "WhitemaneInquisitionClemencyCasterChannelBehavior", "SylvanasFreeHauntingWaveWindrunnerTalent", "LeoricWraithWalkCasterBehavior", "StukovLurkingArmCasterBehavior", "GuldanDrainLifeChannel", "YrelVindicationChannelBuff"
}

# Excluded talents
EXCLUDED_TALENTS = {
    "BrightwingPolyception", "CrusaderMasteryFlailSweep", "MaievVigorousVaulter", "ChromieSandBlastMountingSand", "RagnarosLivingMeteorPyrocasticFlow", "CrusaderMasteryIronSkinLightWithin", "ImperiusSolarionsFireBulwarkOfFlame", "LucioWallRideCantStopWontStop", "LostVikingsMasteryHunkaBurningOlaf", "ArthasMasteryFrostmourneFeedsFrostmourneHungers", "FenixGammaBurst", "MedicCaduceusReactor2dot0", "StukovBallistospores", "KelThuzadMasterOfTheColdDark", "RaynorPenetratingRoundDebilitatingRounds", "ZuljinYouWantAxe", "NexusHunterBloodRageDelayedDelivery", "BattleMomentumSylvanas", "AbathurMasteryRegenerativeMicrobes", "NovaNewRemoteDelivery", "SgtHammerSpiderMinesTargetingMines", "NexusHunterHuntersVengeancePureStrikes", "BattleMomentumNova", "GazloweSelfStealingStemBolts", "BrightwingArcaneBarrageArcaneFlare", "GallNotHereThere", "MedicProlongedSafeguard", "BrightwingSoothingPrecisionArcaneFlare", "AlarakDeadlyChargeSecondHeroic", "AlarakCounterStrikeItem", "IllidanMasteryShadowShieldEvasion", "MedivhArcaneRiftManaAdept", "ThrallMasteryStoneWolves", "AnaBioticGrenadeGrenadeCalibration", "StitchesHarpoon", "StitchesFishingHook", "MuradinMasteryDwarfTossLandingMomentum", "AnduinBoldStrategy", "NovaSnipeMaster", "ChromieDragonsBreathDragonsEye", "ChromieDragonsBreathEnvelopingAssault", "ProbiusParticleAcceleratorDisruptionPulse", "FalstadMasteryBarrelRollFreeRoll", "BrightwingSoothingMistRevitalizingMist", "MuradinStormBoltIt'sHammerTime", "MuradinStormboltPiercingBolt", "SylvanasTalentOverflowingQuiver", "SylvanasTalentWithTheWind", "SylvanasTalentDarkLadysAdvance", "ZaryaParticleGrenadePlasmaShock", "ChenRefreshingElixir", "SylvanasDreadfulWake", "SylvanasTalentBlackArrowsParalysis", "ThrallWindStalker", "KerriganUnbridledEnergy", "LeoricMasteryLingeringApparitionWraithWalk", "TracerSlipstreamRecall", "TyraelMasteryAngelicAbsorption", "TyraelMasteryZealotry", "AnduinChastiseHolyReach", "GazloweDethLazorArkReaktor", "DVaInForTheKill", "IllidanMasteryLungeDive", "DVaBoostersComingThrough", "TassadarHeroicAbilityForceWall", "AbathurMasteryEvolutionMasterUltimateEvolution", "HoggerAftershock", "StukovWithinMyReach", "StukovLingeringSpines", "ChenGroundingBrew", "GuldanDrainLifeDevourTheFrail", "GuldanDrainLifeGlyphOfDrainLife", "AmazonTrueSight", "GreymaneWorgenFormRelentlessPredator", "RexxarBearNecessitiesCharge", "SamuroHeroicAbilityIllusionMaster", "SamuroThreeBladeStyle", "TyrandeMasteryLunarFlareShootingStar", "AnaPiercingDarts", "LucioWallRideOnTheWall", "JunkratFragLauncherPutSomeEnglishOnIt", "RexxarMendPetBloodOfTheRhino", "LucioCrossfadeSpeedBoostWeMoveTogether", "DeathwingFireBombFlight", "RexxarCriticalCareMendPet"
}

# Custom linked talents that aren't linked to an ability
LINKED_TALENTS = {
    "DVaMechMechMode": ["DVaFullMetal"],
    "AnubarakScarabHostTrait": ["AnubarakBurningBeetles"],
    "ArtanisShieldOverloadTrait": ["ArtanisShieldOverloadShieldSurge"],
    "DiabloBlackSoulstone": ["DiabloMasteryDevilsDueBlackSoulstone", "DiabloLifeLeech"],
    "DiabloShadowCharge": ["DiabloShadowChargeOverpowerCruelty"],
    "DiabloOverpower": ["DiabloShadowChargeOverpowerCruelty"],
    "SamuroAdvancingStrikes": ["SamuroBlademastersPursuit", "SamuroAdvancingStrikesDeflection"],
    "ZaryaEnergy": ["ZaryaEnergyHitMe", "ZaryaPainIsTemporary", "ZaryaWeaponFeelTheHeat"],
    "AmazonAvoidance": ["AmazonPlateoftheWhale"],
    "AlarakSadism": ["AlarakPureMalice"],
    "MalfurionRegrowth": ["MalfurionWildGrowthTalent", "MalfurionRegrowthNaturesBalance"],
    "MalfurionMoonfire": ["MalfurionWildGrowthTalent", "MalfurionRegrowthNaturesBalance"],
    "GreymaneRazorSwipe": ["GreymaneToothAndClaw", "GreymaneRazorSwipeUnfetteredAssault"],
    "GreymaneDarkflight": ["GreymaneToothAndClaw", "GreymaneRazorSwipeUnfetteredAssault"],
    "OrpheaOverflowingChaos": ["OrpheaDeadMagic", "OrpheaAncestralStrength"],
    "JainaTraitFrostbite": ["JainaFrostbiteDeepChill", "JainaFrostbiteFrostArmor"],
    "WhitemaneTraitZeal": ["WhitemaneZealScarletWrath"],
    "ImperiusValorousBrand": ["ImperiusValorousBrandBrandOfSolarion", "ImperiusValorousBrandBurnTheImpure"],
    "SylvanasBlackArrows": ["SylvanasTalentOverwhelmingAffliction"],
    "NexusHunterFinalStrike": ["NexusHunterFinalStrikeUnleashedPotential"],
    "MedicCaduceusReactor": ["MedicCaduceusFeedback", "MedicCellularReactor"],
    "DeathwingDestroyer": ["DeathwingDestroyersRampage"],
    "RaynorGiveEmSomePepper": ["RaynorGiveEmSomePepperUnstableCompound", "RaynorGive'EmSomePepperSergeantPepper"],
    "DemonHunterHatred": ["DemonHunterSeethingHatred", "DemonHunterGloom"],
    "AlarakDeadlyChargeFirstHeroic": ["AlarakCounterStrikeItem"],
    "AlarakHeroicAbilityCounterStrike": ["AlarakDeadlyChargeSecondHeroic"],
    "VarianTwinBladesOfFury": ["VarianTwinBladesOfFuryFrenzy"],
    "DeckardHoradricCubeCharging": ["DeckardGemRuby", "DeckardKanaisCube"],
    "ValeeraEviscerate": ["ValeeraEviscerateSliceAndDice"],
    "ThrallFrostwolfResilience": ["ThrallAncestralWrath"],
    "MaievSpiritOfVengeance": ["MaievSpiritOfVengeanceShadowOrbVengeance"],
    "NecromancerRaiseSkeleton": ["NecromancerTalentKalansEdict"],
    "HanzoStormBow": ["HanzoPiercingArrows"],
    "HanzoScatterArrow": ["HanzoPiercingArrows"],
    "FenixShieldCapacitor": ["FenixRapidRecharge", "FenixDivertPowerWeaponsTalent"],
    "AnaTraitShrikeSniper": ["AnaMindNumbingAgent"],
    "AnaAimDownSightsActivate": ["AnaMindNumbingAgent"],
    "WitchDoctorVoodooRitualTrait": ["WitchDoctorVileInfection"],
    "VarianHeroicStrike": ["VarianMortalStrike"],
    "DeckardFortitudeOfTheFaithful": ["DeckardAncientBlessings"],
    "GallRunicBlast": ["GallDeafeningBlast"],
    "TassadarResonanceBeam": ["TassadarArcDischarge", "TassadarKhaydarinAmulet"],
    "MalthaelReapersMark": ["MalthaelInevitableEnd"],
    "LiLiFastFeet": ["LiLiEagerAdventurer", "LiLiShakeItOff"],
    "JunkratConcussionMine": ["JunkratConcussionMineBlowEmUp"],
    "JunkratSteelTrap": ["JunkratConcussionMineBlowEmUp"],
    "MurkyPufferfish": ["MurkyAFishyDeal"],
    "DVaPilotBigShot": ["DVaBigShotPewPewPew"],
    "ZeratulPermanentCloak": ["ZeratulMoveUnseen"],
    "KerriganAssimilation": ["KerriganAssimilationMastery"],
    "BarbarianFury": ["BarbarianNoEscape"],
    "TyraelRighteousness": ["TyraelMasteryLawAndOrder"],
    "TyraelSmite": ["TyraelMasteryLawAndOrder"],
    "FalstadHammerang": ["FalstadMasteryHammerangSecretWeapon"],
    "IllidanSweepingStrike": ["IllidanBladesOfAzzinoth"],
    "DeathwingAspectOfDeath": ["DeathwingDragonsIre"],
    "JainaBlizzard": ["JainaIcefuryWand"],
    "AbathurSymbioteSpikeBurst": ["AbathurMasteryPressurizedGlands"],
}

# Custom linked heroic talents for heroics
LINKED_HEROICS = {
    "AurielResurrectSelf": "AurielHeroicResurrect",
    "VarianColossusSmash": "VarianColossusSmash",
    "VarianTaunt": "VarianTaunt",
    "VarianTwinBladesOfFury": "VarianTwinBladesOfFury",
    "AnaEyeOfHorusHighPoweredRound": "AnaHeroicAbilityEyeOfHorus",
    "DVaBunnyHop": "DvaMechBunnyHopHeroic",
    "DVaBunnyHopOn": "DvaMechBunnyHopHeroic",
    "LostVikingsLongboatRaid": "LostVikingsHeroicAbilityLongboatRaid",
    "NecromancerPoisonNova": "NecromancerHeroicAbilityPoisonNova",
    "Sundering": "ThrallHeroicAbilitySundering",
    "SamuroBladestorm": "SamuroHeroicAbilityBladestorm",
    "BrightwingEmeraldWind": "FaerieDragonHeroicAbilityEmeraldWind",
    "TyraelJudgment": "TyraelHeroicAbilityJudgement",
    "MurkyMarchOfTheMurlocs": "MurkyHeroicAbilityMarchoftheMurlocs",
    "UtherDivineShield": "UtherHeroicAbilityDivineShield",
    "TychusCommandeerOdin": "TychusHeroicAbilityCommandeerOdin",
    "AlarakDeadlyCharge": "AlarakDeadlyChargeFirstHeroic",
    "NexusHunterFinalStrike": "NexusHunterFinalStrike",
    "AbathurEvolveMonstrosityHotbar": "AbathurHeroicAbilityEvolveMonstrosity",
    "ZagaraNydusNetwork": "ZagaraHeroicAbilityNydusAssault",
    "DVaPilotBigShot": "DVaBigShotPewPewPew",
    "TinkerRoboGoblinPassive": "TinkerHeroicAbilityRoboGoblin",
    "IllidanMetamorphosis": "IllidanHeroicAbilityMetamorphosis",
    "BrightwingBlinkHealAllyDash": "FaerieDragonHeroicAbilityBlinkHeal"
}

# Custom linked behaviors for abilities
LINKED_BEHAVIORS = {
    "AzmodanSummonDemonWarrior": ["AzmodanSummonDemonWarriorUnitTracker"],
    "MurkySpawnEgg": ["AbnormalDeath", "OneQuarterValueHero"]
}

# Prerequisites for talents
PREREQ_TALENTS = {
}

# Talents not linked to an ability
GENERIC_TALENTS = []

# List of basic attacks
BASIC_ATTACKS = ["SylvanasHeroWeapon", "HeroKerrigan", "NecromancerHeroWeapon", "AzmodanHeroWeapon", "HeroBarbarian", "DryadHeroRangedWeapon", "KaelthasHeroWeapon", "HeroStitches", "MalthaelHeroWeapon", "HeroWizardWeapon", "HeroJaina", "MedivhHeroWeapon", "HeroMuradin", "ZuljinHeroWeapon", "AnduinHeroWeapon", "MephistoHeroWeapon", "AnaHeroWeapon", "WhitemaneHeroWeapon", "HeroValeera", "StukovHeroWeapon", "CrusaderHeroWeapon", "ImperiusHeroWeapon", "HeroMaievWeapon", "HeroArtanis", "HeroUther", "HeroWeaponAlarak", "ThrallHeroWeapon", "MonkHeroWeapon", "JunkratHeroWeaponRanged", "OrpheaWeapon", "AurielHeroWeapon", "HeroGarrosh", "ButcherHeroWeapon", "AnubarakHeroWeapon", "HeroGuldan", "TassadarResonanceBeam", "HeroFalstad", "TracerHeroWeapon", "YrelHeroWeapon", "HeroDiablo", "HeroRehgar", "HanzoHeroWeapon", "HoggerHeroWeapon", "TychusMiniGunRampingSpeedWeapon", "HeroTinker", "HeroMurky", "HeroLucioWeapon", "HeroZagara", "HeroIllidan", "ProbiusAttackWeapon", "ZaryaHeroWeapon", "HeroDehaka", "GenjiHeroWeapon", "VarianHeroWeaponBase", "RaynorWeapon", "HeroArthas", "AmazonHeroWeaponRanged", "DeathwingHeroWeapon", "ChromieHeroWeapon", "LeoricWeapon", "FenixHeroWeapon", "DeckardHeroWeapon", "TyrandeHeroWeapon", "HeroZeratul", "HeroAbathur", "HeroMalfurion", "AlexstraszaAttackWeapon", "RexxarRangedWeapon", "SamuroWeapon", "FirebatHeroWeapon", "MedicHeroWeapon", "HeroNova", "TyraelHeroWeapon", "ChenHeroWeapon", "DVaMechWeapon", "HeroGreymaneRangedWeapon", "HeroErikSlingshot", "HeroFaerieDragon", "HeroSgtHammer", "NexusHunterHeroWeapon", "RagnarosAttackWeapon", "HeroLiLi", "MeiOWHeroWeapon", "HeroWitchDoctor", "HeroL90ETC", "ChoHeroWeapon", "HeroKelThuzad", "HeroDemonHunter", "HeroMalGanisWeapon"]

def debug_print(message, prefix=Debug.INFO, end="\n"):
    if DEBUG:
        global last_messages
        if message not in last_messages:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            debug_message = f"[{timestamp}] {prefix.value} {message}"
            debug_messages.append(debug_message)
            print(debug_message, end=end)
            last_messages.append(message)
            if len(last_messages) > 6:
                last_messages.pop(0)

# Extract abilities from file
def extract(hero_file):
    tree = ET.parse(hero_file)
    root = tree.getroot()
    abilities = { "Heroic": [], "Trait": [], "Ability": [] }
    seen_talents = []

    def extract_behaviors(ability_data, root):
        behaviors = set()
        face = ability_data.get("Face")
        if face and face in LINKED_BEHAVIORS:
            linked_behaviors = LINKED_BEHAVIORS[face]
            debug_print(f"Behaviors: {linked_behaviors} found for {face} in Linked Behaviors")
            behaviors.update(linked_behaviors)
        for abilEffect in root.findall(".//CAbilEffectTarget") + root.findall(".//CAbilEffectInstant"):
            abilID = abilEffect.get("id")
            if abilID == ability_data.get("AbilCmd", "").split(",")[0]:
                for cmdButton in abilEffect.findall(".//CmdButtonArray"):
                    for attribute_name in ["Requirements", "ShowValidator"]:
                        attribute = cmdButton.get(attribute_name, "")
                        if attribute:
                            resolved_behaviors = resolve_dependencies(attribute, tree, "Requirement" if attribute_name == "Requirements" else "Validator")
                            if resolved_behaviors:
                                debug_print(f"Behaviors: {attribute_name}={', '.join(resolved_behaviors)} found in {abilID}")
                                behaviors.update(resolved_behaviors)
                            else:
                                debug_print(f"Attribute {attribute_name} found in {abilID} but could not be resolved", Debug.WARNING)
        return list(behaviors)

    def extract_related_abilities(root):
        debug_print("Extracting related abilities")
        related_abilities = {}

        # Special cases of abilities without parents
        related_abilities["MeiOWCryoFreezeCancel"] = [{"Face": "MeiOWCryoFreezeCancel", "AbilCmd": "MeiOWCryoFreezeCancel,Execute", "Type": "AbilCmd", "Slot": "Trait", "Parent": "MeiOWCryoFreeze", "XML": "meiowdata.xml" }]
        related_abilities["MeiOWIcingCancel"] = [{ "Face": "MeiOWIcingCancel", "AbilCmd": "MeiOWIcingCancel,Execute", "Type": "AbilCmd", "Slot": "Ability3", "Parent": "MeiOWCryoFreeze", "XML": "meiowdata.xml" }]
        related_abilities["WitchDoctorGargantuanStomp"] = [{ "Face": "WitchDoctorGargantuanStomp", "Type": "Passive", "Slot": "Heroic", "Requirements": "WitchDoctorIsCastingGargantuanStomp", "Parent": "WitchDoctorGargantuan", "XML": "witchdoctordata.xml" }]
        related_abilities["FenixRepeaterCannon"] = [{ "Face": "FenixRepeaterCannon", "AbilCmd": "FenixRepeaterCannon,Execute", "Type": "AbilCmd", "Slot": "Ability2", "Parent": "FenixPhaseBomb", "XML": "fenixdata.xml", "Talents": extract_talents({"Face": "FenixRepeaterCannon"}, root, True)}]
        related_abilities["YrelVindicationCast"] = [{"Face": "YrelVindication", "Type": "AbilCmd", "AbilCmd": "YrelVindicationCast,Execute", "Slot": "Ability1", "Parent": "YrelVindication", "XML": "yreldata.xml"}]

        for abilEffect in root.findall(".//CAbilEffectTarget") + root.findall(".//CAbilEffectInstant"):
            ability_id = abilEffect.get("id")
            parent_abil = abilEffect.find("ParentAbil")

            if parent_abil != None:
                parent_abil_value = parent_abil.get("value")
                if parent_abil_value:
                    debug_print(f"Ability {ability_id} has a parent: {parent_abil_value}")
                    if ability_id not in related_abilities:
                        related_abilities[ability_id] = []

                    seen_entries = set()

                    for layout_button in root.findall(".//LayoutButtons"):
                        slot, face, abilCmd, abilType, requirements = layout_button.get('Slot'), layout_button.get('Face'), layout_button.get('AbilCmd'), layout_button.get('Type'), layout_button.get('Requirements')

                        r_ability_data = {key: value for key, value in {
                            "Face": face,
                            "AbilCmd": abilCmd,
                            "Type": abilType,
                            "Requirements": requirements,
                            "Slot": slot,
                            "Parent": parent_abil_value,
                            "XML": hero_file
                        }.items() if value is not None}

                        data_key = (face, abilCmd, abilType, requirements, slot)

                        if slot:
                            if face == ability_id or (abilCmd and abilCmd.replace(",Execute", "").replace(",255", "").replace(",On", "").replace(",Off", "") == ability_id):
                                if data_key not in seen_entries and face not in EXCLUDED_RELATED_ABILITIES:
                                    debug_print(f"Adding related ability {r_ability_data["Face"]} to {parent_abil_value}")
                                    r_ability_data["Behaviors"] = extract_behaviors(r_ability_data, root)
                                    r_ability_data["Talents"] = extract_talents(r_ability_data, root, True)
                                    if slot == "Heroic":
                                        r_ability_data["HeroicTalent"] = extract_heroic_talents(r_ability_data, root)
                                    seen_entries.add(data_key)
                                    related_abilities[ability_id].append(r_ability_data)
                                else:
                                    debug_print(f"Skipping related ability {r_ability_data["Face"]}, already added or excluded")
        return related_abilities

    def find_ability_from_talent(talent_id, root):
        ctalents = root.findall(f".//CTalent[@id='{talent_id}']")
        if ctalents:
            for ctalent in ctalents:
                ability = ctalent.find("Abil")
                if ability is not None:
                    ability_name = ability.get("value")
                    return ability_name
        return

    def extract_talents(ability_data, root, abil=False):
        talents = []
        skipped_talents = []
        generic_talents = []
        face = ability_data.get("Face")
        abilCmd = ability_data.get("AbilCmd")

        if abilCmd:
            abilCmd = abilCmd.replace(",Execute", "").replace(",255", "").replace(",On", "").replace(",Off", "")

        for talent in root.findall(".//CTalent"):
            talent_id = talent.get("id")
            talent_ability = talent.find("Abil")
            ability_name = None
            if talent_ability is not None:
                ability_name = talent_ability.get("value")

            if talent_id in EXCLUDED_TALENTS:
                seen_talents.append(talent_id)
                debug_print(f"Excluding talent {talent_id}: Found in Excluded Talents")
            else:
                if abil:
                    if ability_name:
                        if face == ability_name:
                            seen_talents.append(talent_id)
                            talents.append(talent_id)
                        elif abilCmd and abilCmd == ability_name:
                            seen_talents.append(talent_id)
                            talents.append(talent_id)
                    else:
                        if face in LINKED_TALENTS and talent_id in LINKED_TALENTS[face]:
                            seen_talents.append(talent_id)
                            talents.append(talent_id)
                        elif abilCmd and abilCmd in LINKED_TALENTS and talent_id in LINKED_TALENTS[abilCmd]:
                            seen_talents.append(talent_id)
                            talents.append(talent_id)
                else:
                    if talent_id not in GENERIC_TALENTS and talent_id not in seen_talents:
                        seen_talents.append(talent_id)
                        generic_talents.append(talent_id)
                        GENERIC_TALENTS.append(talent_id)
                    if talent_id not in seen_talents:
                        skipped_talents.append(talent_id)

        if len(talents) > 0:
            debug_print(f"Found talents: {', '.join(talents)}")
        if len(skipped_talents) > 0:
            debug_print(f"Skipped talents: {', '.join(skipped_talents)}")
        if len(generic_talents) > 0:
            debug_print(f"Generic talents: {', '.join(generic_talents)}")

        if abil:
            return talents
        else:
            return

    def extract_heroic_talents(ability_data, root):
        heroic = ability_data.get("Face")
        heroicCmd = ability_data.get("AbilCmd")
        for talentTreeArray in root.findall(".//TalentTreeArray"):
            tier = talentTreeArray.get("Tier")
            if tier == "4":
                talent = talentTreeArray.get("Talent")
                if talent is not None:
                    talent_ability = find_ability_from_talent(talent, root)
                    if talent_ability is not None:
                        if talent_ability in EXCLUDED_TALENTS:
                            debug_print(f"Tried to add {talent} to heroic {heroic} but excluded, skipping")
                            return
                        if (heroic and heroic == talent_ability) or (heroicCmd and heroicCmd == talent_ability):
                            debug_print(f"Found talent ability {talent} for heroic {heroic}")
                            return talent
                        else:
                            if heroic and heroic in LINKED_HEROICS:
                                debug_print(f"Found talent ability {LINKED_HEROICS[heroic]} for heroic {heroic}")
                                return LINKED_HEROICS[heroic]
                            elif heroicCmd and heroicCmd in LINKED_HEROICS:
                                debug_print(f"Found talent ability {LINKED_HEROICS[heroicCmd]} for heroic {heroicCmd}")
                                return LINKED_HEROICS[heroicCmd]
                            else:
                                debug_print(f"Couldn't find heroic talent for {heroic}", Debug.WARNING)
                    else:
                        debug_print(f"Couldn't find ability for talent {talent}", Debug.WARNING)
                else:
                    debug_print(f"Couldn't find talent in talent tree array for {heroic}", Debug.WARNING)
        return

    hero_name = format_hero_name(hero_file.replace("hero_xmls/", "").replace(".xml", ""))
    hero_units = []
    hero_units.append(root.find(f".//CUnit[@id='{hero_name}']"))
    if hero_name == "HeroLostVikings":
        hero_units.append(root.find(f".//CUnit[@id='HeroErik']"))
        hero_units.append(root.find(f".//CUnit[@id='HeroBaleog']"))
        hero_units.append(root.find(f".//CUnit[@id='HeroOlaf']"))
    elif hero_name == "HeroRexxar":
        hero_units.append(root.find(f".//CUnit[@id='RexxarMisha']"))
    elif hero_name == "HeroCho":
        hero_units.append(root.find(f".//CUnit[@id='HeroGall']"))
    elif hero_name == "HeroDVa":
        hero_units.append(root.find(f".//CUnit[@id='HeroDVaMech']"))
        hero_units.append(root.find(f".//CUnit[@id='HeroDVaPilot']"))

    global excluded_abilities
    excluded_abilities = []

    for hero_unit in hero_units:
        debug_print(f"Searching {hero_name}")
        related_abilities = extract_related_abilities(root)

        for layout_button in root.findall(".//LayoutButtons"):
            slot, face, abilCmd, abilType, requirements = layout_button.get('Slot'), layout_button.get('Face'), layout_button.get('AbilCmd'), layout_button.get('Type'), layout_button.get('Requirements')


            if slot:
                # Check if ability is excluded
                if should_exclude(face, abilCmd, slot, related_abilities):
                    continue
                debug_print(f"Extracting ability {face} in {slot} slot")
                ability_data = {key: value for key, value in {
                    "Face": face,
                    "AbilCmd": abilCmd,
                    "Type": abilType,
                    "Slot": slot,
                    "Requirements": requirements,
                    "XML": hero_file,
                }.items() if value is not None}

                ability_data["Behaviors"] = extract_behaviors(ability_data, root)
                ability_data["Talents"] = extract_talents(ability_data, root, True)
                if slot == "Heroic":
                    ability_data["HeroicTalent"] = extract_heroic_talents(ability_data, root)

                for related_ability_list in related_abilities.values():
                    for related_ability in related_ability_list:
                        if related_ability.get("Parent") == face or (abilCmd and related_ability.get("Parent") == abilCmd.replace(",Execute", "").replace(",255", "").replace(",On", "").replace(",Off", "")):
                            if "RelatedAbility" not in ability_data:
                                ability_data["RelatedAbility"] = []
                            ability_data["RelatedAbility"].extend(related_ability_list)

                if slot == "Heroic" and ability_data not in abilities["Heroic"]:
                    abilities["Heroic"].append(ability_data)
                elif slot == "Trait" and ability_data not in abilities["Trait"]:
                    abilities["Trait"].append(ability_data)
                elif slot.startswith("Ability") and ability_data not in abilities["Ability"]:
                    abilities["Ability"].append(ability_data)
    if len(excluded_abilities) > 0:
        debug_print(f"Excluded abilities: {', '.join(excluded_abilities)}")

    extract_talents({}, root, False)
    return abilities

def should_exclude(face, abilCmd, slot, related_abilities):
    # Exclude abilities with parents
    if (face and face in related_abilities) or (abilCmd and abilCmd.split(",")[0] in related_abilities):
        excluded_abilities.append(face)
        return True

    # Excluded abilities
    if face in EXCLUDED_ABILITIES or (abilCmd and abilCmd.split(",")[0] in EXCLUDED_ABILITIES):
        excluded_abilities.append(face)
        return True

    # Temp excluded abilities
    if face in TEMP_EXCLUDED_ABILITIES or (abilCmd and abilCmd.split(",")[0] in TEMP_EXCLUDED_ABILITIES):
        excluded_abilities.append(face)
        return True

    # Excluded face/abilCmd combinations
    if face in EXCLUSION_PATTERNS and abilCmd:
        for pattern in EXCLUSION_PATTERNS[face]:
            if pattern in abilCmd:
                excluded_abilities.append(face)
                return True

    # Excluded face/abilCmd combinations in specific slot
    if slot and (slot, face) in EXCLUSION_SLOTS and abilCmd:
        for pattern in EXCLUSION_SLOTS[(slot, face)]:
            if pattern in abilCmd:
                excluded_abilities.append(face)
                return True
    elif slot and (slot, face) in EXCLUSION_SLOTS and abilCmd == "":
        excluded_abilities.append(face)
        return True
    if face is None and abilCmd is None:
        return True

    return False

def resolve_dependencies(entity_id, xml, entity_type="Requirement"):
    resolved_behaviors = []
    visited_entities = set()

    def resolve_recursive(entity_id):
        if entity_id in visited_entities:
            return  # Avoid infinite loops
        visited_entities.add(entity_id)

        if entity_type == "Requirement":
            entity = xml.find(f".//CRequirement[@id='{entity_id}']")
            if entity is None:
                entity = xml.find(f".//CRequirementEq[@id='{entity_id}']")
        elif entity_type == "Validator":
            entity = xml.find(f".//CValidatorUnitHasBehavior[@id='{entity_id}']")
            if entity is None:
                entity = xml.find(f".//CValidatorCombine[@id='{entity_id}']")
        else:
            debug_print(f"Unknown entity type: {entity_type} for {entity_id}", Debug.WARNING)
            return

        if entity is None:
            debug_print(f"Couldn't resolve {entity_type} for {entity_id}", Debug.WARNING)
            return

        if entity_type == "Requirement":
            if entity.tag == "CRequirementEq":
                for operand in entity.findall("OperandArray"):
                    operand_id = operand.get("value")
                    if "CountBehavior" in operand_id:
                        behavior = xml.find(f".//CRequirementCountBehavior[@id='{operand_id}']")
                        if behavior:
                            count = behavior.find("Count")
                            if count is not None:
                                resolved_behaviors.append(count.get("Link"))
                            else:
                                debug_print(f"Couldn't find behavior for {behavior}", Debug.WARNING)
            else:
                for node in entity.findall("NodeArray"):
                    link = node.get("Link")
                    if link.startswith("EqCountBehavior"):
                        cReqEq = xml.find(f".//CRequirementEq[@id='{link}']")
                        if cReqEq:
                            for operand in cReqEq.findall("OperandArray"):
                                operand_id = operand.get("value")
                                if "CountBehavior" in operand_id:
                                    behavior = xml.find(f".//CRequirementCountBehavior[@id='{operand_id}']")
                                    if behavior:
                                        count = behavior.find("Count")
                                        if count is not None:
                                            resolved_behaviors.append(count.get("Link"))
                                        else:
                                            debug_print(f"Couldn't find behavior for {behavior}", Debug.WARNING)

                    elif link.startswith("And") or link.startswith("Or"):
                        composite_requirement = xml.find(f".//CRequirementAnd[@id='{link}']") or \
                                                xml.find(f".//CRequirementOr[@id='{link}']")
                        if composite_requirement:
                            for operand in composite_requirement.findall("OperandArray"):
                                operand_id = operand.get("value")
                                resolve_recursive(operand_id)
        elif entity_type == "Validator":
            if entity.tag == "CValidatorCombine":
                for combine_array in entity.findall("CombineArray"):
                    combine_id = combine_array.get("value")
                    resolved_behaviors.extend(resolve_dependencies(combine_id, xml, "Validator"))
            else:
                behavior = entity.find(".//Behavior")
                if behavior is not None:
                    behavior_value = behavior.get("value")
                    if behavior_value:
                        resolved_behaviors.append(behavior_value)
                    else:
                        debug_print(f"Couldn't find behavior for {behavior}", Debug.WARNING)
    resolve_recursive(entity_id)

    return resolved_behaviors

def format_hero_name(hero_name):

    special_cases = {
        "Brightwing": "HeroFaerieDragon",
        "Lili": "HeroLiLi",
        "Sgthammer": "HeroSgtHammer",
        "Nexushunter": "HeroNexusHunter",
        "Kelthuzad": "HeroKelThuzad",
        "L90etc": "HeroL90ETC",
        "Witchdoctor": "HeroWitchDoctor",
        "Demonhunter": "HeroDemonHunter",
        "Thefirelords": "HeroRagnaros",
        "Dva": "HeroDVa",
        "Malganis": "HeroMalGanis",
        "Genn": "HeroGreymane",
        "Meiow": "HeroMeiOW",
        "Lostvikings": "HeroLostVikings"
    }

    # Remove 'data' and capitalize hero name
    hero_name = hero_name.replace('data', '').capitalize()

    return special_cases.get(hero_name, "Hero" + hero_name)

def unformat_hero_name(hero_name):

    special_cases = {
        "faeriedragon": "brightwing",
        "lili": "lili",
        "sgthammer": "sgthammer",
        "nexushunter": "nexushunter",
        "kelthuzad": "kelthuzad",
        "l90etc": "l90etc",
        "witchdoctor": "witchdoctor",
        "demonhunter": "demonhunter",
        "ragnaros": "thefirelords",
        "dva": "dva",
        "malganis": "malganis",
        "greymane": "genn",
        "meiow": "meiow",
        "cho": "chogall",
        "gall": "chogall"
    }
    hero_name = hero_name.replace("Hero", "").lower()

    return special_cases.get(hero_name, hero_name)

def random_scaling():
    rand = random.random()
    if rand < 0.9:
        return 0.04 # 90% chance for 4% scaling
    elif rand < 0.96:
        return random.choice([0.035, 0.045]) # 6% chance for 3.5% or 4.5% scaling
    elif rand < 0.98:
        return random.choice([0.03, 0.05]) # 2% chance for 3% or 5% scaling
    elif rand < 0.99:
        return random.choice([0.025, 0.055]) # 1% chance for 2.5% or 5.5% scaling
    return random.choice([0.02, 0.06]) # 1% chance for 2% or 6% scaling

def find_ctalent(talent, xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    ctalent = root.find(f".//CTalent[@id='{talent}']")

    return ctalent

def update_requirements(ability, index):
    if ability:
        tree = ET.parse(ability.get("XML"))
        root = tree.getroot()
    else:
        debug_print(f"Could not update requirements of ability {ability}", Debug.WARNING)
        return

    if ability.get("AbilCmd"):
        ability_id = ability.get("AbilCmd").replace(",Execute", "").replace(",255", "").replace(",On", "").replace(",Off", "")
    elif ability.get("Face"):
        ability_id = ability.get("Face")

    if ability_id == "VarianTwinBladesOfFury":
        ability_id = "VarianTwinBladesofFury"

    original_ability = root.find(f".//CAbilEffectTarget[@id='{ability_id}']")
    if original_ability is None:
        original_ability = root.find(f".//CAbilEffectInstant[@id='{ability_id}']")
    if original_ability is None:
        original_ability = root.find(f".//CAbilBehavior[@id='{ability_id}']")
    if original_ability is None:
        debug_print(f"Ability '{ability_id}' not found in either CAbilEffectTarget or CAbilEffectInstant", Debug.WARNING)
        return

    new_ability = ET.fromstring(ET.tostring(original_ability))
    extra = ""

    for cmd_button in new_ability.findall(".//CmdButtonArray"):
        reqs = cmd_button.get("Requirements")
        if reqs:
            updated_reqs = reqs.replace("Ultimate1Unlocked", f"Ultimate{index}Unlocked").replace("Ultimate2Unlocked", f"Ultimate{index}Unlocked")
            if updated_reqs != reqs:
                cmd_button.set("Requirements", updated_reqs)
            elif reqs == "ValeeraCloakofShadowsRequirements":
                extra = f'''\n<CRequirement id="ValeeraCloakofShadowsRequirements">
    <NodeArray index="Show" Link="EqCountBehaviorUltimate{index}UnlockedCompleteOnlyAtUnit1" />
</CRequirement>'''

        if cmd_button.get("ShowValidator") and (cmd_button.get("ShowValidator") == "CasterHasUltimate1Unlocked" or cmd_button.get("ShowValidator") == "CasterHasUltimate2Unlocked"):
            cmd_button.set("ShowValidator", f"CasterHasUltimate{index}Unlocked")

        if cmd_button.get("UseValidator") and (cmd_button.get("UseValidator") == "UtherHasUltimate1UnlockedAndDoesNotHaveSpiritFormGhost" or cmd_button.get("UseValidator") == "UtherHasUltimate2UnlockedAndDoesNotHaveSpiritFormGhost"):
            cmd_button.set("UseValidator", f"UtherHasUltimate{index}UnlockedAndDoesNotHaveSpiritFormGhost")

    return ET.tostring(new_ability, encoding="unicode") + extra

def write_to_xml(hero, abilities):
    debug_print(f"RANDOMIZING {hero.upper()}")

    # Health stats
    life_max = random.choice([685, 730, 804, 1130, 1140, 1260, 1270, 1300, 1330, 1340, 1365, 1365, 1375, 1390, 1400, 1425, 1425, 1430, 1442, 1450, 1470, 1482, 1490, 1500, 1502, 1511, 1520, 1525, 1525, 1550, 1560, 1595, 1598, 1622, 1650, 1650, 1660, 1665, 1675, 1698, 1700, 1700, 1720, 1725, 1725, 1764, 1780, 1810, 1835, 1875, 1896, 1900, 1925, 1950, 1962, 1968, 1975, 2000, 2021, 2027, 2047, 2060, 2075, 2080, 2100, 2150, 2154, 2220, 2260, 2275, 2280, 2292, 2357, 2375, 2450, 2464, 2473, 2490, 2517, 2550, 2600, 2625, 2625, 2678, 2750, 2765, 2825, 2860, 2900, 2950, 2950, 3020])
    if random.random() < (1 / 90):
        life_regen = life_max * 0.04 # 1.11% chance to get Murky's health regen
    else:
        life_regen = life_max * 0.002083333

    # Collision and inner radius
    radius = random.uniform(0.5, 1.25) // 0.0625 * 0.0625
    inner_radius = radius

    basic_attack = ""
    extra_attack = ""
    # Basic attack
    if hero != "HeroGall":
        if len(BASIC_ATTACKS) > 0:
            basic_attack = random.choice(BASIC_ATTACKS)
            BASIC_ATTACKS.remove(basic_attack)
            if basic_attack == "DVaMechWeapon":
                basic_attack = random.choice(["DVaMechWeapon", "DVaPilotWeapon"])
            elif basic_attack == "DryadHeroRangedWeapon":
                extra_attack += '\n    <WeaponArray Link="DryadHeroMeleeWeapon" />'
                extra_attack += '\n    <WeaponArray Link="DryadHeroRangedWeaponStarwoodSpearMastery" />'
            elif basic_attack == "HeroGreymaneRangedWeapon":
                extra_attack += '\n    <WeaponArray Link="HeroGreymaneMeleeWeapon" />'
                extra_attack += '\n    <WeaponArray Link="HeroGreymaneWorgenWeapon" />'
            elif basic_attack == "AlexstraszaAttackWeapon":
                basic_attack = random.choice(["AlexstraszaAttackWeapon", "AlexstraszaDragonConeWeapon"])
            elif basic_attack == "CrusaderHeroWeapon":
                extra_attack += '\n    <WeaponArray Link="CrusaderFlailSweepWeapon" />'
            elif basic_attack == "RaynorWeapon":
                extra_attack += '\n    <WeaponArray Link="RaynorWeaponMelee" />'
            elif basic_attack == "AmazonHeroWeaponRanged":
                extra_attack += '\n    <WeaponArray Link="AmazonHeroWeaponMelee" />'
            elif basic_attack == "RexxarRangedWeapon":
                extra_attack += '\n    <WeaponArray Link="RexxarMeleeWeapon" />'
            elif basic_attack == "HeroErikSlingshot":
                basic_attack = random.choice(["HeroErikSlingshot", "HeroBaleogBow", "HeroOlaf"])
        else:
            debug_print("Ran out of Basic Attacks to assign, defaulting to Raynor", Debug.ERROR)
            basic_attack = "RaynorWeapon"
            extra_attack += '\n    <WeaponArray Link="RaynorWeaponMelee" />'

    # CUnit parent
    parent = "StormHeroMounted"
    if hero in ["HeroAbathur", "HeroAmazon", "HeroFaerieDragon", "HeroGall", "HeroDeathwing", "HeroDehaka", "HeroDryad", "HeroDVa", "HeroFalstad", "HeroLucio", "HeroMedivh", "HeroProbius", "HeroRehgar", "HeroSgtHammer", "HeroYrel"]:
        parent = "StormHeroMountedCustom"

    # Unit height
    height = ""
    if hero == "HeroFaerieDragon":
        height = '\n    <Height value="1" />'
    elif hero == "HeroFalstad":
        height = '\n    <Height value="2" />'

    def generate_layout_buttons():
        layout_buttons_content = ""
        def add_layout_button(ability, slot):
            face = ability.get("Face", "")
            abil_cmd = ability.get("AbilCmd", "")
            button_type = ability.get("Type", "")
            reqs = ability.get("Requirements", "")
            related_ability = ability.get("RelatedAbility", "")
            layout_button = ""

            if related_ability:
                for r_abil in related_ability:
                    layout_button += f'<LayoutButtons Face="{r_abil.get("Face")}"' if r_abil.get("Face") else "<LayoutButtons"
                    layout_button += f' AbilCmd="{r_abil.get("AbilCmd")}"' if r_abil.get("AbilCmd") else ""
                    layout_button += f' Type="{r_abil.get("Type")}"' if r_abil.get("Type") else ""
                    layout_button += f' Requirements="{r_abil.get("Requirements", "")}"' if r_abil.get("Requirements", "") else ""
                    layout_button += f' Slot="{slot}" />\n'
                    # Lazy fix
                    if r_abil.get("Face") == "WitchDoctorGargantuanStomp" and r_abil.get("Type") == "Passive":
                        layout_button += f'<LayoutButtons Face="WitchDoctorGargantuanStomp" Type="AbilCmd" AbilCmd="WitchDoctorGargantuanStompCommand,Execute" Slot="Heroic" />\n'


            layout_button += f'<LayoutButtons Face="{face}"' if face else "<LayoutButtons"
            layout_button += f' AbilCmd="{abil_cmd}"' if abil_cmd else ""
            layout_button += f' Type="{button_type}"' if button_type else ""
            layout_button += f' Requirements="{reqs}"' if reqs else ""
            layout_button += f' Slot="{slot}" />\n'

            return layout_button

        heroics = ""

        for i, heroic in enumerate(abilities["Heroic"]):
            layout_buttons_content += add_layout_button(heroic, "Heroic")
            heroics += str(update_requirements(heroic, i+1)) + "\n"


        if abilities["Trait"]:
            layout_buttons_content += add_layout_button(abilities["Trait"][0], "Trait")

        for i, ability in enumerate(abilities["Ability"]):
            slot = f'Ability{i + 1}'
            layout_buttons_content += add_layout_button(ability, slot)

        return indent(layout_buttons_content, "         "), heroics

    def generate_behaviors():
        behavior_content = ""

        for ability_type in ["Heroic", "Trait", "Ability"]:
            for ability in abilities.get(ability_type, []):
                related_ability = ability.get("RelatedAbility", "")
                if "Behaviors" in ability:  # Check if ability has Behaviors
                    behaviors = ability["Behaviors"]
                    if isinstance(behaviors, list):
                        for behavior in behaviors:
                            if behavior not in EXCLUDED_BEHAVIORS:
                                behavior_content += f'\n<BehaviorArray Link="{behavior}" />'
                    elif isinstance(behaviors, str):
                        if behaviors not in EXCLUDED_BEHAVIORS:
                            behavior_content += f'\n<BehaviorArray Link="{behaviors}" />'
                if related_ability:
                    for r_abil in related_ability:
                        if "Behaviors" in r_abil:
                            rBehaviors = r_abil["Behaviors"]
                            if isinstance(rBehaviors, list):
                                for behavior in rBehaviors:
                                    if behavior not in EXCLUDED_BEHAVIORS:
                                        behavior_content += f'\n<BehaviorArray Link="{behavior}" />'
                            elif isinstance(rBehaviors, str):
                                if rBehaviors not in EXCLUDED_BEHAVIORS:
                                    behavior_content += f'\n<BehaviorArray Link="{rBehaviors}" />'

        return indent(behavior_content, "    ")

    def generate_abil_arrays():
        abil_arrays_content = ""
        added_arrays = []

        for ability_group in ["Heroic", "Trait", "Ability"]:
            for ability in abilities[ability_group]:
                face = ability.get("Face", "")
                abil_cmd = ability.get("AbilCmd", "").replace(",Execute", "").replace(",255", "").replace(",On", "").replace(",Off", "")
                related_ability = ability.get("RelatedAbility", "")

                if face and face not in added_arrays:
                    abil_arrays_content += f'    <AbilArray Link="{face}" />\n'
                    added_arrays.extend(face)
                if abil_cmd and abil_cmd != face and abil_cmd.replace(",Execute", "").replace(",255", "").replace(",On", "").replace(",Off", "") not in added_arrays:
                    abil_arrays_content += f'    <AbilArray Link="{abil_cmd}" />\n'
                    added_arrays.extend(abil_cmd.replace(",Execute", "").replace(",255", "").replace(",On", "").replace(",Off", ""))
                if related_ability:
                    for r_abil in related_ability:
                        r_face = r_abil.get("Face")
                        r_abil_cmd = r_abil.get("AbilCmd")
                        r_abil_cmd = r_abil_cmd.replace(",Execute", "").replace(",255", "").replace(",On", "").replace(",Off", "") if r_abil_cmd else r_abil_cmd
                        if r_face and r_face not in added_arrays:
                            abil_arrays_content += f'    <AbilArray Link="{r_face}" />\n'
                            added_arrays.extend(r_face)
                        if r_abil_cmd and r_abil_cmd != r_face and r_abil_cmd not in added_arrays:
                            abil_arrays_content += f'    <AbilArray Link="{r_abil_cmd}" />\n'
                            added_arrays.extend(r_abil_cmd)

        return abil_arrays_content.strip()

    def generate_chero(hero):
        path = os.path.join(HERO_XML_DIR, unformat_hero_name(hero) + "data.xml")
        tree = ET.parse(path)
        root = tree.getroot()
        cHero = root.find(f".//CHero[@id='{hero.replace("Hero","")}']")
        if cHero is None:
            debug_print(f"Couldn't find CHero for {hero}", Debug.WARNING)
            return ""

        cHero_content = ET.fromstring(ET.tostring(cHero))
        ctalent = []

        talent_tiers = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        tier_limits = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}

        # Count amount of talents per tier and then remove them
        for talent_tree in cHero_content.findall(".//TalentTreeArray"):
            tier = int(talent_tree.get("Tier"))
            tier_limits[tier] += 1
            cHero_content.remove(talent_tree)
        for talent_ai_builds in cHero_content.findall(".//TalentAIBuildsArray"):
            cHero_content.remove(talent_ai_builds)

        # Remove everything else
        for child in list(cHero_content):
            cHero_content.remove(child)

        i = 0
        _talents = []
        for ability_group in ["Heroic", "Trait", "Ability"]:
            for i, ability in enumerate(abilities[ability_group]):
                face = ability.get("Face", "")
                slot = ability.get("Slot", "")
                related_ability = ability.get("RelatedAbility", "")
                talents = ability.get("Talents", "")
                if related_ability is not None:
                    for rAbil in related_ability:
                        related_talents = rAbil.get("Talents", "")
                        if related_talents is not None:
                            talents.extend(related_talents)

                if slot == "Heroic":
                    heroicTalent = ability.get("HeroicTalent", "")
                    if heroicTalent is not None and heroicTalent not in talent_tiers[4]:
                        talent_tiers[4].append(heroicTalent)
                        _ctalent = find_ctalent(heroicTalent, ability.get("XML"))
                        # Bunny Hop fix
                        if _ctalent is None and heroicTalent == "DvaMechBunnyHopHeroic":
                            _ctalent = find_ctalent("DVaBunnyHop", ability.get("XML"))
                        if _ctalent is not None:
                            ctalent.append(_ctalent)
                            ctalent_behaviors = _ctalent.findall(".//BehaviorArray")
                            if ctalent_behaviors:
                                for b in ctalent_behaviors:
                                    bTag = b.get("value")
                                    if bTag:
                                        if bTag == "Ultimate1Unlocked" or bTag == "Ultimate2Unlocked":
                                            b.set("value", f"Ultimate{i+1}Unlocked")
                        else:
                            debug_print(f"Couldn't find CTalent for {heroicTalent}", Debug.WARNING)
                    else:
                        debug_print(f"Couldn't find heroic talent for {ability.get("Face")}", Debug.WARNING)
                    if talents:
                        for talent in talents:
                            if talent != heroicTalent and talent not in talent_tiers[7]:
                                talent_tiers[7].append(talent)
                                if len(talent_tiers[4]) > i and talent_tiers[4][i]:
                                    PREREQ_TALENTS[talent] = talent_tiers[4][i]
                                    i += 1
                    elif face in LINKED_TALENTS:
                        for linked in LINKED_TALENTS[face]:
                            talent_tiers[7].append(linked)
                            if len(talent_tiers[4]) > i and talent_tiers[4][i]:
                                PREREQ_TALENTS[talent] = talent_tiers[4][i]
                                i += 1
                    else:
                        debug_print(f"No heroic upgrades found for {face}")
                else:
                    if face in LINKED_TALENTS:
                        for linked in LINKED_TALENTS[face]:
                            if linked not in _talents:
                                _talents.append(linked)
                    if talents:
                        for talent in talents:
                            if talent not in _talents:
                                _talents.append(talent)


        random.shuffle(_talents)
        for talent in _talents:
            valid_tiers = [tier for tier in talent_tiers if tier != 4 and len(talent_tiers[tier]) < tier_limits[tier]]
            if valid_tiers:
                tier = random.choice(valid_tiers)
                if talent not in talent_tiers[tier]:
                    talent_tiers[tier].append(talent)

        for tier in talent_tiers:
            while len(talent_tiers[tier]) < tier_limits[tier] and len(GENERIC_TALENTS) > 0:
                generic_talent = random.choice(GENERIC_TALENTS) # Add a random generic talent
                GENERIC_TALENTS.remove(generic_talent)
                talent_tiers[tier].append(generic_talent)

        if len(GENERIC_TALENTS) == 0:
            debug_print("Ran out of talents to assign", Debug.WARNING)

        for tier, talents in talent_tiers.items():
            column = 1
            for talent in talents:
                talent_elem = ET.SubElement(cHero_content, "TalentTreeArray")
                talent_elem.set("Talent", talent)
                talent_elem.set("Tier", str(tier))
                talent_elem.set("Column", str(column))
                column += 1
                if talent in PREREQ_TALENTS:
                    prereqtalent_elem = ET.SubElement(talent_elem, "PrerequisiteTalentArray")
                    prereqtalent_elem.set("value", PREREQ_TALENTS[talent])

        ai_talent_choices = []
        for tier, talents in talent_tiers.items():
            ai_talent_choices.extend(talents)

        for _ in range(6):  # Create 6 AI builds
            ai_build = ET.SubElement(cHero_content, "TalentAIBuildsArray")
            ai_build.set("ChanceToPick", str(random.randint(1, 16)))
            sample_size = min(len(ai_talent_choices), random.randint(1, 3))
            for talent in random.sample(ai_talent_choices, sample_size):
                talent_elem = ET.SubElement(ai_build, "TalentsArray")
                talent_elem.set("value", talent)

        xml_str = ET.tostring(cHero_content, encoding="unicode", method="xml")
        xml_str = xml_str.replace('<TalentTreeArray', '\n    <TalentTreeArray')
        xml_str = xml_str.replace('<TalentAIBuildsArray', '\n    <TalentAIBuildsArray')
        xml_str = xml_str.replace('</TalentAIBuildsArray', '\n    </TalentAIBuildsArray')
        xml_str = xml_str.replace('<TalentsArray', '\n        <TalentsArray')
        xml_str = xml_str.replace('</CHero>', '\n</CHero>\n')
        if ctalent:
            for c in ctalent:
                xml_str += ET.tostring(c, encoding="unicode", method="xml")

        return xml_str

    layout_buttons_content, heroics = generate_layout_buttons()
    behavior_content = generate_behaviors()
    abil_arrays_content = generate_abil_arrays()
    chero_content = generate_chero(hero)

    hero_cunit = f'''<CUnit id="{hero}" parent="{parent}">
    <LifeStart value="{life_max}" />
    <LifeMax value="{life_max}" />
    <LifeRegenRate value="{life_regen}" />
    <Radius value="{radius}" />
    <InnerRadius value="{inner_radius}" />{height}
    <WeaponArray Link="{basic_attack}" />{extra_attack}
    <AIThinkTree value="ai/{hero}Custom.aitree" />
    <HeroPlaystyleFlags index="BodyBlocker" value="1" />
    <HeroPlaystyleFlags index="EnergyImportant" value="1" />
    <HeroPlaystyleFlags index="Ganker" value="1" />
    <HeroPlaystyleFlags index="Overconfident" value="1" />
    <HeroPlaystyleFlags index="RoleTank" value="1" />
    <HeroPlaystyleFlags index="AllyHealer" value="1" />
    <HeroPlaystyleFlags index="ChanneledAutoAttacker" value="1" />
    <HeroPlaystyleFlags index="Helper" value="1" />
    <HeroPlaystyleFlags index="Roamer" value="1" />
    <HeroPlaystyleFlags index="RoleSupport" value="1" />
    <CardLayouts index="0">
{layout_buttons_content}    </CardLayouts>{f'{behavior_content}' if behavior_content != "" else ""}
    {abil_arrays_content}
</CUnit>\n{heroics}\n
{chero_content}'''

    return hero_cunit


def write_ai(hero, abilities):
    HERO_AI_MAP = {
    "Abathur": {"includes_modified": ["abathurRemoveNoGoals"]},
    "Alarak": {"includes": ["alarak"]},
    "Alexstrasza": {"includes_modified": ["alexstraszaNoFlameEscape"]},
    "Amazon": {"includes": ["amazon"]},
    "Ana": {"includes": ["ana"]},
    "Anubarak": {"includes": ["anubarak"]},
    "Artanis": {"includes": ["artanis"]},
    "Arthas": {"includes": ["arthas"]},
    "Auriel": {"includes": ["auriel"]},
    "Azmodan": {"includes_modified": ["azmodanNoCancelBeam"]},
    "Barbarian": {"includes": ["barbarian"]},
    "Blaze": {"includes": ["blaze"]},
    "Brightwing": {"includes": ["brightwing"]},
    "Butcher": {"includes": ["butcher"]},
    "Chen": {"includes": ["chen"]},
    "Cho": {"includes": ["cho"]},
    "Chromie": {"includes": ["chromie"]},
    "Crusader": {"includes": ["crusader"]},
    "Deckard": {"includes": ["deckard"]},
    "Dehaka": {"includes": ["dehaka"]},
    "Diablo": {"includes_modified": ["diabloNoHellgate"]},
    "Dryad": {"includes": ["dryad"]},
    "DVa": {
        "includes": ["dvamech", "dvapilot"],
        "includes_modified": ["dvaNoPanicBoost"]
    },
    "Falstad": {"includes": ["falstad"]},
    "Fenix": {"includes": ["fenix"]},
    "Gall": {"includes_modified": ["gallMovement"]},
    "Garrosh": {"includes": ["garrosh"]},
    "Gazlowe": {"includes_modified": ["gazloweNoGoblinEscape"]},
    "Genji": {"includes": ["genji"]},
    "Greymane": {"includes": ["greymane"]},
    "Guldan": {"includes": ["guldan"]},
    "Hanzo": {"includes_modified": ["hanzoNoVaultEscape"]},
    "Hogger": {"includes_modified": ["hoggerNoHoardapultEscape"]},
    "Illidan": {"includes": ["illidan"]},
    "Imperius": {"includes": ["imperius"]},
    "Jaina": {"includes": ["jaina"]},
    "Junkrat": {"includes_modified": ["junkratNoRideEscape"]},
    "Kaelthas": {"includes": ["kaelthas"]},
    "KelThuzad": {"includes": ["kelthuzad"]},
    "Kerrigan": {"includes_modified": ["kerriganNoChrysalis"]},
    "L90": {"includes": ["l90etc"]},
    "Leoric": {"includes": ["leoric"]},
    "LiLi": {"includes": ["lili"]},
    "Lucio": {"includes": ["lucio"]},
    "Maiev": {"includes": ["maiev"]},
    "Malfurion": {"includes": ["malfurion"]},
    "MalGanis": {"includes": ["malganis"]},
    "Malthael": {"includes_modified": ["malthaelNoPanicRites"]},
    "Medic": {"includes": ["medic"]},
    "Medivh": {"includes_modified": ["medivhNoRaven"]},
    "MeiOW": {"includes": ["meiow"]},
    "Mephisto": {"includes": ["mephisto"]},
    "Monk": {"includes_modified": ["monkNoPanic7orAir"]},
    "Muradin": {"includes": ["muradin"]},
    "Murky": {"includes": ["murky"]},
    "Nazeebo": {"includes": ["nazeebo"]},
    "Necromancer": {"includes": ["necromancer"]},
    "Nova": {"includes_modified": ["novaNoGhostProtocol"]},
    "Orphea": {"includes": ["orphea"]},
    "Probius": {"includes": ["probius"]},
    "Ragnaros": {"includes": ["ragnaros"]},
    "Raynor": {"includes": ["raynor"]},
    "Rehgar": {"includes": ["rehgar"]},
    "Rexxar": {"includes": ["rexxar"]},
    "Samuro": {"includes": ["samuro"]},
    "SgtHammer": {"includes": ["sgthammer"]},
    "Stitches": {"includes": ["stitches"]},
    "Stukov": {"includes": ["stukov"]},
    "Sylvanas": {"includes": ["sylvanas"]},
    "Tassadar": {"includes_modified": ["tassadarNoShadowWalk"]},
    "Thrall": {"includes": ["thrall"]},
    "Tracer": {"includes": ["tracer"]},
    "Tychus": {"includes": ["tychus"]},
    "Tyrael": {"includes": ["tyrael"]},
    "Tyrande": {"includes": ["tyrande"]},
    "Uther": {"includes": ["uther"]},
    "Valla": {"includes": ["valla"]},
    "Valeera": {"includes_modified": ["valeeraNoPanicStealth"]},
    "Varian": {"includes": ["varian"]},
    "Whitemane": {"includes": ["whitemane"]},
    "Wizard": {"includes": ["wizard"]},
    "Yrel": {"includes_modified": ["yrelNoPanicArdentOrBubble"]},
    "Zagara": {"includes": ["zagara"]},
    "Zarya": {"includes": ["zarya"]},
    "Zeratul": {"includes": ["zeratul"]},
    "Zuljin": {"includes_modified": ["zuljinNoPanicUltOrRegen"]},
    "Deathwing": {"includes_modified": ["deathwingNoFlight"]},
    "NexusHunter": {"includes_modified": ["nexushunterNoPanicRage"]}
    }
    includes = []
    includes_modified = []

    def add_ai(ability_hero):
        if ability_hero in HERO_AI_MAP:
            hero_data = HERO_AI_MAP[ability_hero]
            if "includes" in hero_data:
                includes.extend(hero_data["includes"])
            if "includes_modified" in hero_data:
                includes_modified.extend(hero_data["includes_modified"])

    def add_to_aitree():
        input_path = os.path.join("ai_templates", hero.replace("Hero","").lower() + ".aitree")
        output_path = os.path.join("ai", hero + "Custom.aitree")
        os.makedirs("ai", exist_ok=True)

        with open(input_path, 'r', encoding='us-ascii') as f:
            lines = f.readlines()

        modified_content = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line == "</tree>":
                for i in includes:
                    if i != hero:
                        modified_content.append(f'<include file="AI/{i}.aitree" />')
                for i in includes_modified:
                    if not i.startswith(hero):
                        modified_content.append(f'<include file="modifiedAI/{i}.aitree" />')
            modified_content.append(stripped_line)

        with open(output_path, 'w', encoding='us-ascii') as f:
            f.write('\n'.join(modified_content))
            debug_print(f"Writing AI to {output_path}")

    for category, abilities_list in abilities.items():
        for ability in abilities_list:
            if ability.get("Face"):
                for ability_hero in HERO_AI_MAP:
                    if ability.get("Face").startswith(ability_hero) and hero != "Hero" + ability_hero:
                        add_ai(ability_hero)

    # Removes duplicates
    includes = list(set(includes))
    includes_modified = list(set(includes_modified))

    add_to_aitree()

def select_and_remove_abilities(all_abilities):
    return {
        "Heroic": all_abilities["Heroic"][:2],
        "Trait": all_abilities["Trait"][:1],
        "Ability": all_abilities["Ability"][:3]
    }, {
        "Heroic": all_abilities["Heroic"][2:],
        "Trait": all_abilities["Trait"][1:],
        "Ability": all_abilities["Ability"][3:]
    }

all_abilities = { "Heroic": [], "Trait": [], "Ability": [] }

for hero_file in os.listdir(HERO_XML_DIR):
    if hero_file.endswith(".xml"):
        hero_path = os.path.join(HERO_XML_DIR, hero_file)
        abilities = extract(hero_path)
        for key in abilities:
            all_abilities[key].extend(abilities[key])

debug_print(f"Number of abilities found:\n Heroics: {len(all_abilities["Heroic"])}\n Traits: {len(all_abilities["Trait"])}\n Abilities: {len(all_abilities["Ability"])}")

for key in all_abilities:
    debug_print("Shuffling all abilities")
    random.shuffle(all_abilities[key])

with open(OUTPUT_FILE, 'w') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n<Catalog>\n')

    for hero_file in os.listdir(HERO_XML_DIR):
        if hero_file.endswith(".xml"):
            hero = format_hero_name(os.path.splitext(hero_file)[0])

            if len(all_abilities["Heroic"]) >= 2 and len(all_abilities["Trait"]) >= 1 and len(all_abilities["Ability"]) >= 3:
                if hero == "HeroChogall":
                    # Cho
                    selected_abilities, all_abilities = select_and_remove_abilities(all_abilities)
                    hero_xml = write_to_xml("HeroCho", selected_abilities)
                    output.write(hero_xml)
                    write_ai("cho", selected_abilities)
                    # Gall
                    selected_abilities, all_abilities = select_and_remove_abilities(all_abilities)
                    hero_xml = write_to_xml("HeroGall", selected_abilities)
                    output.write(hero_xml)
                    write_ai("gall", selected_abilities)
                else:
                    selected_abilities, all_abilities = select_and_remove_abilities(all_abilities)
                    hero_xml = write_to_xml(hero, selected_abilities)
                    output.write(hero_xml)
                    write_ai(hero, selected_abilities)
            else:
                debug_print(f"Not enough abilities found to generate {hero} (Number of abilities left: Heroics={len(all_abilities["Heroic"])}, Traits={len(all_abilities["Trait"])}, Abilities={len(all_abilities["Ability"])})", Debug.WARNING)

    output.write('</Catalog>\n')

debug_print(f"Generated XML file with randomized Heroes: {OUTPUT_FILE}", Debug.SUCCESS)

with open("debug_log.txt", "w") as log_file:
    log_file.write("\n".join(debug_messages))
