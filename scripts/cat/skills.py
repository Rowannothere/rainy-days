import random
from enum import Enum, Flag, auto
from typing import Union

import i18n

from scripts.config import get_config
from scripts.cat.enums import CatRank, CatAge, CatGroup


def scale_progress(current: float, ceiling: int, amount: float) -> float:
    """adjusts skill/experience gain for difficulty and distance to ceiling"""

    modifier = get_config("progress.difficulty_modifier")
    if not modifier or amount <= 0 or ceiling <= 0:
        return amount
    headroom = min(max(1 - current / ceiling, 1e-9), 1.0)
    gain_factor = headroom**modifier
    return amount * gain_factor


class SkillPath(Enum):
    EXPLORER = (
        "curious wanderer",
        "knowledgeable explorer",
        "brave pathfinder",
        "master of territories"
    )
    TRACKER = (
        "tracker instincts",
        "proficient tracker",
        "great tracker",
        "masterful tracker"
    )
    GUARDIAN = (
        "watchful",
        "good guard",
        "great guard",
        "guardian"
    )
    TUNNELER = (
        "enjoys digging",
        "good tunneler",
        "great tunneler",
        "fantastic tunneler"
    )
    NAVIGATOR = (
        "good with directions",
        "good navigator",
        "great navigator",
        "pathfinder"
    )
    SONG = (
        "likes to sing",
        "good singer",
        "great singer",
        "captivating singer"
    )
    GRACE = (
        "steps lightly",
        "graceful",
        "elegant",
        "radiates elegance"
    )
    CLEAN = (
        "tidy",
        "fur-care enthusiast",
        "meticulous cleaner",
        "master of aesthetics"
    )
    INNOVATOR = (
        "always curious",
        "problem solver",
        "creator of solutions",
        "visionary thinker"
    )
    COMFORTER = (
        "gentle voice",
        "comforting presence",
        "nightmare soother",
        "boogeyman-fighter"
    )
    MATCHMAKER = (
        "interested in relationship drama",
        "relationship advisor",
        "skilled heart-reader",
        "masterful matchmaker"
    )
    THINKER = (
        "oddly resourceful",
        "out-of-the-box thinker",
        "paradox enthusiast",
        "philosopher"
    )
    COOPERATIVE = (
        "lives in groups",
        "good sport",
        "team player",
        "insider"
    )
    SCHOLAR = (
        "always learning",
        "well-versed",
        "incredibly knowledgeable",
        "polymath"
    )
    TIME = (
        "oddly orderly",
        "always busy",
        "coordinated",
        "efficiency aficionado"
    )
    TREASURE = (
        "looks for trinkets",
        "item stasher",
        "trinket stower",
        "treasure keeper"
    )
    FISHER = (
        "bats at rivers", 
        "grazes fish", 
        "fish-catcher", 
        "gold star fishercat"
    )
    LANGUAGE = (
        "other-cat-ly whisperer",
        "dog-whisperer",
        "multilingual",
        "listener of all voices"
    ) 
    SLEEPER = (
        "dozes easily",
        "sunhigh log",
        "dormouse", 
        "leader of SnoozeClan"
    )
    GARDENER = (
            "loves to pick flowers",
            "grows herbs",
            "herb organizer",
            "caretaker of the greens"
        ) 

    # LG: outsider-unique skill paths feel free to change the descriptions

    # Kittypet-unique
    TWOLEGCARE = (
        "patient with housefolk",
        "housefolk friend",
        "trusted by Twolegs",
        "Twoleg whisperer"
    )
    CHARMER = (
        "easy to like",
        "magnetic",
        "irresistibly charming",
        "purrs hearts open"
    )
    SHOWCAT = (
        "preens for attention",
        "polished",
        "ribbon-winner",
        "show-perfect"
    )

    # Loner-unique
    WANDERER = (
        "restless paws",
        "well-traveled",
        "seasoned wanderer",
        "knower of lands"
    )
    SCAVENGER = (
        "picks at scraps",
        "resourceful scavenger",
        "keen scavenger",
        "finder of forgotten things"
    )
    SURVIVOR = (
        "tough soul",
        "survivor",
        "strong endurance",
        "unbreakable"
    )

    # Rogue-unique
    BRAWLER = (
        "scrappy",
        "street brawler",
        "ruthless brawler",
        "fights without rules"
    )
    INTIMIDATOR = (
        "unsettling glare",
        "intimidating",
        "fear-striker",
        "presence of nightmares"
    )
    AMBUSHER = (
        "hides well",
        "patient ambusher",
        "clever ambusher",
        "invisible ambusher"
    )
    TEACHER = ("quick to help", "good teacher", "great teacher", "excellent teacher")
    HUNTER = ("moss ball hunter", "good hunter", "great hunter", "renowned hunter")
    FIGHTER = (
        "avid play-fighter",
        "good fighter",
        "formidable fighter",
        "unusually strong fighter",
    )
    RUNNER = (
        "never sits still",
        "fast runner",
        "incredible runner",
        "fast as the wind",
    )
    CLIMBER = (
        "constantly climbing",
        "good climber",
        "great climber",
        "impressive climber",
    )
    SWIMMER = (
        "splashes in puddles",
        "good swimmer",
        "talented swimmer",
        "fish-like swimmer",
    )
    SPEAKER = (
        "confident with words",
        "good speaker",
        "great speaker",
        "eloquent speaker",
    )
    MEDIATOR = (
        "quick to make peace",
        "good mediator",
        "great mediator",
        "skilled mediator",
    )
    CLEVER = ("quick witted", "clever", "very clever", "incredibly clever")
    INSIGHTFUL = (
        "careful listener",
        "helpful insight",
        "valuable insight",
        "trusted advisor",
    )
    SENSE = ("oddly observant", "natural intuition", "keen eye", "unnatural senses")
    KIT = (
        "active imagination",
        "good kitsitter",
        "great kitsitter",
        "beloved kitsitter",
    )
    STORY = (
        "lover of stories",
        "good storyteller",
        "great storyteller",
        "masterful storyteller",
    )
    LORE = (
        "interested in Clan history",
        "learner of lore",
        "lore keeper",
        "lore master",
    )
    CAMP = ("picky nest builder", "steady paws", "den builder", "camp keeper")
    HEALER = ("interested in herbs", "good healer", "great healer", "fantastic healer")
    STAR = (
        "curious about StarClan",
        "connection to StarClan",
        "deep StarClan bond",
        "unshakable StarClan link",
    )
    DARK = (
        "interested in the Dark Forest",
        "Dark Forest affinity",
        "deep Dark Forest bond",
        "unshakable Dark Forest link",
    )
    OMEN = ("interested in oddities", "omen seeker", "omen sense", "omen sight")
    DREAM = ("restless sleeper", "strange dreamer", "dream walker", "dream shaper")
    CLAIRVOYANT = (
        "oddly insightful",
        "somewhat clairvoyant",
        "fairly clairvoyant",
        "incredibly clairvoyant"
    )
    PROPHET = (
        "fascinated by prophecies",
        "prophecy seeker",
        "prophecy interpreter",
        "prophet"
    )
    GHOST = (
        "morbid curiosity",
        "ghost sense",
        "ghost sight",
        "ghost speaker"
    ) 
    UNKNOWN = (
        "intrigued about the Unknown Residence",
        "Unknown Residence accord",
        "deep Unknown Residence bond",
        "unshakable Unknown Residence link"
    ) 
    WAKEFUL = (
        "never settles down",
        "light sleeper",
        "alert",
        "vigilant"
    ) 
    DELIVERER = (
        "queen helper",
        "helpful stork",
        "kit deliverer",
        "pregnancy expert"
    ) 
    DECORATOR = (
        "makes things pretty",
        "crafty paws",
        "creative",
        "decor master"
    ) 
    LEADERSHIP = (
        "deputy helper",
        "leads patrols",
        "leader's accomplice",
        "assiduous"
    ) 
    AGILE = (
        "parkours around camp",
        "light-footed",
        "lithe",
        "quick agilist"
    ) 
    STEALTHY = (
        "startles others",
        "underpawed",
        "furtive kitty",
        "clandestine"
    ) 
    MEMORY = (
        "remembers little details",
        "memorious",
        "retentive memory",
        "mnemonist"
    ) 
    MESSENGER = (
        "delivers messages",
        "message-bearer",
        "message-carrier",
        "harbinger to the clans"
    ) 
    ASSIST = (
        "little helper",
        "assist guard",
        "alert assistant",
        "camp's assister"
    ) 
    HISTORIAN = (
        "remembers stories",
        "bookkeeper",
        "archivist",
        "accountant of history"
    ) 
    BOOKMAKER = (
        "loves to tell stories",
        "journalist",
        "novelist",
        "author of many stories"
    ) 
    PATIENT = (
        "waits their turn",
        "serene",
        "even-tempered",
        "equanimous"
    ) 
    DETECTIVE = (
        "curious about mysteries",
        "elementary case-solver",
        "great sleuth",
        "masterful detective"
    ) 
    HERBALIST = (
        "curious about remedies",
        "herbal inventor",
        "poison maker",
        "creator of remedies"
    )
    CHEF = (
        "seasons their food",
        "cooks prey",
        "gourmet prey maker",
        "masterful chef"
    )
    PRODIGY = (
        "unusually gifted",
        "knows alot of facts",
        "smart role model",
        "seen as an omen"
    )
    DISGUISE = (
        "accessory hoarder",
        "creator of appearances",
        "skillful disguiser", 
        "shapeshifter"
    )
    PYRO = (
        "loves warmth",
        "messes with embers",
        "spark master", 
        "fire starter"
    )
    HYDRO = (
        "water lover",
        "great firefighter",
        "excellent extinguisher",
        "masterful extinguisher"
    )
    GIFTGIVER = (
        "loves to gift",
        "nice giftgiver",
        "excellent giftgiver", 
        "always gives gifts"
    )
    VIBES = (
        "senses vibes",
        "knows who to trust",
        "mood reader", 
        "vibe detector"
    )
    STARGAZER = (
        "gazes at the stars",
        "night vision",
        "star-filled eyes", 
        "celestial insight"
    )
    IMMUNE = (
        "rarely sick",
        "better immune system",
        "strong immune system", 
        "constant germ immunity"
    )

    MUSICVIBES = (
        "charming voice",
        "nice singing",
        "beautiful singing", 
        "lovely singing"
    )
    AURAVIBES = (
        "nice aura",
        "friendly aura",
        "calming aura", 
        "pleasant aura"
    )
    ANIMALTAKER = (
        "friendly with animals",
        "loves to care for animals",
        "wildlife friend", 
        "deep animal-lover"
    )
    VET = (
        "cares for injured creatures",
        "helps animals",
        "animal soother", 
        "woodland healer"
    )
    ANIMALMAGNET = (
        "small critters follow them",
        "attracts animals",
        "animals gather around them", 
        "animal magnet"
    )

    # bleu's expanded skillsets

    ACTING = (
    	"plays pretends",
    	"performs unique roles",
    	"skilled performer",
    	"great actor"
    	)

    ADVOCATE = (
        "suggests new ideas",
        "rallies for support",
        "supports causes",
        "speaks for others"
        )
    
    ANIMALOGIST = (
        "studies animal behavior",
        "gathers animal information",
        "trained zoologist",
        "expert zoologist"
        )
    
    ANTHROPOLOGIST = (
            "fascinated by Twolegs",
            "Twoleg enthusiast",
            "Kittypet sympathizer",
            "Kittypet affinity"
            )

    ARCHAEOLOGIST = (
            "plays with bones",
            "digs up graves",
            "analyzes skeletal remains",
            "skeletal collector"
            )

    ARCHIVER = (
            "remembers small details",
            "recounts past events",
            "trained fact checker",
            "expert archiver"
            )
    
    ARMORER = (
        "sharpens claws",
        "invents combative tools",
        "handles weapon accessories",
        "oversees weaponry"
        )

    ARRANGER = (
            "organizes flower petals",
            "crafts flower accessories",
            "trained florist",
            "flower arranger"
            )

    ASSASSIN = (
            "chases targets",
            "investigates codebreakers",
            "bloodhound",
            "bounty hunter"
            )

    ARTIFICER = (
            "decorates fur",
            "crafts pretty accessories",
            "designs accessories",
            "accessory crafter"
            )

    ARTISAN = (
            "drawn to pretty colors",
            "creative affinity",
            "artistically talented",
            "masterful artisan"
            )

    ASTRONOMER = (
            "enjoys stargazing",
            "guided by the stars",
            "star lore expert",
            "trained astronomer"
            )

    AURA = (
            "sensitive to environment", 
            "notices aura",
            "studies aura patterns",
            "aura reader" 
            )

    BALANCE = (
            "dexterous paws",
            "graceful moves",
            "balancer",
            "expert acrobatics"
            )
    
    BUILDER = (
            "interested in growing strong",
            "engages in muscle building",
            "strengthens muscles",
            "trained body builder"
            )
    
    CAMPER = (
            "makes up nests",
            "gathers nesting materials",
            "sets up camps",
            "camp builder"
            )

    CARPENTER = (
            "claws at wood",
            "forms wooden items",
            "whittles wood",
            "carpenter"
            )

    CHAMPION = (
            "aspiring defender",
            "powerful crusader",
            "mighty knight",
            "great champion"
            )

    COLLECTOR = (
            "picks up useful objects",
            "collects resources",
            "known hoarder",
            "skilled collector"
            )

    COMEDIAN = (
            "cracks silly jokes",
            "jokes around",
            "entertainer",
            "comedy genius"
            )
    
    COMMANDER = (
            "observes surroundings",
            "leads mock battles",
            "directs attacks",
            "commands allies"
            )
    
    COMPANION = (
            "offers comforting words",
            "close friend",
            "trusted ally",
            "personal favorite"
            )

    COMPULSION = (
            "charming presence",
            "weakens willpower",
            "compels others",
            "master manipulator"
            )
    
    CONSULTANT = (
            "observes relationships",
            "gives relationship advice",
            "specializes in personal matters",
            "relationship consultant"
            )

    CURSED = (
            "burdened by lineage",
            "suffers hardships",
            "encounters adversity",
            "cursed bloodline"
            )

    DANCER = (
            "rhythmic pawsteps",
            "prances around",
            "energetic mover",
            "lively motion"
            )
    
    DEATH = (
            "morbid senses",
            "smells death",
            "grim reaper",
            "angel of death"
            )

    DEBATER = (
            "quick to argue",
            "questions everything",
            "skilled debater",
            "serious debater"
            )

    DECEPTOR = (
            "tells white lies",
            "deceptive words",
            "smooth talker",
            "master swindler"
            )

    DISCIPLINE = (
            "follows rules",
            "judges misbehavior",
            "administers discipline",
            "atones for misconduct"
            )
    
    DIVER = (
            "holds in breath",
            "dives underwater",
            "swims with fishes",
            "plunges into deep waters"
            )

    ENFORCER = (
            "judges codebreakers",
            "pledges loyalty",
            "code follower",
            "code enforcer"
            )
    
    ENTERTAINER = (
            "center of attention",
            "fan favorite",
            "massive following",
            "beloved entertainer"
            )

    ETIQUETTE = (
            "conforms to society",
            "proper greeter",
            "respectfully cautious",
            "adequately behaves"
            )

    EXERCISE = (
            "always moving",
            "stretches legs",
            "body trainer",
            "muscle builder"
            )

    EXORCIST = (
            "scares away spirits",
            "evicts spirits",
            "commands spirits",
            "fearsome exorcist"
            )
    
    FAIRY = (
            "senses spirits",
            "dreams of the fae",
            "visited by fairies",
            "fairy kinship"
            )
    
    FOLLOWER = (
            "follows after others",
            "quick to take sides",
            "carefully chooses alliances",
            "loyal follower"
            )

    FORAGER = (
            "picks at berry bushes",
            "gathers fruits and seeds",
            "foraging dietician",
            "impressive forager"
            )
    
    FORTITUDE = (
            "rarely injured",
            "powerful fortitude",
            "high endurance",
            "strong constitution"
            )
    
    GAMBLER = (
            "takes big risks",
            "makes bold decision",
            "sacrifices safety",
            "daredevil"
            )
    
    GENEALOGIST = (
            "studies appearances",
            "guesses fur colors",
            "predicts pelt types",
            "foretells coat patterns"
            )

    GEOGRAPHER = (
            "nature spirit kindred",
            "observes land formations",
            "trained naturalist",
            "great geographer"
            )

    GRAVEKEEPER = (
            "ancestral curiosity",
            "tends to burial grounds",
            "burial caretaker",
            "ancestral groundskeeper"
            )

    GOSSIPER = (
            "socially engaged",
            "engages in idle gossip",
            "promotes internal strife",
            "politically active"
            )

    GUARDING = (
            "restless protector",
            "watches over others",
            "camp guard",
            "respected warden"
            )

    GUIDER = (
            "listens closely to others",
            "offers advice",
            "guides others",
            "skilled guider"
            )

    HERDER = (
            "groups together insects",
            "animal whisperer",
            "flock management",
            "herder"
            )

    HIDING = (
            "hide-and-seek winner",
            "blends into surroundings",
            "natural colors",
            "invisible hider"
            )
    
    HIKER = (
            "walks long distances",
            "takes extended walks",
            "skilled hiker",
            "expert hiker"
            )
    
    HYPNOTIST = (
            "offers persuasive arguments",
            "changes other's minds",
            "implants false memories",
            "powerful influence"
            )
    
    ILLUSION = (
            "magic affinity",
            "performs tricks",
            "skilled illusionist",
            "master of illusions"
            )

    INTIMIDATION = (
            "fluffs out chest",
            "fierce gaze",
            "threatening glare",
            "intimidating presence",
            )

    INVENTOR = (
            "innovative mind",
            "tinkers with random objects",
            "constructs creations",
            "inventor"
            )
    
    LEGACY = (
            "future heir",
            "prestigious lineage",
            "inherited status",
            "noble legacy"
            )
    
    LIFESAVER = (
            "quick reactor",
            "offers first aid",
            "rescues others from danger",
            "savior figure"
            )
    
    LUCKY = (
            "born lucky",
            "has good luck",
            "pushes luck",
            "lucky streak"
            )
    
    MANAGER = (
            "starts small tasks",
            "assigns roles",
            "dictates tasks",
            "oversees projects"
            )
    
    MECHANIC = (
            "gathers building materials",
            "plays with Twoleg objects",
            "learns mechanical structures",
            "makes helpful gadgets"
            )

    MEDITATION = (
            "ponders existence",
            "deep thinker",
            "reflects on life",
            "meditative"
            )

    MEDIUM = (
            "hears the dead's voices",
            "soul speaker",
            "spiritually intuitive",
            "spirit medium"
            )

    MENTALIST = (
            "knack for control",
            "offers suggestions",
            "diverts attention",
            "calculated guesser"
            )
    
    MINDER = (
            "looks after others",
            "deflects criticism",
            "controls public opinion",
            "experienced minder"
            )
    
    PARANORMAL = (
            "interested in the occult",
            "watches mystical spirits",
            "memorizes supernatural entities",
            "paranormal lorekeeper"
            )

    PILGRIM = (
            "interested in holy places",
            "takes care of shrines",
            "traveling pilgrim",
            "devoted worshipper"
            )

    POLITICIAN = (
            "asks small favors",
            "rallies for support",
            "persuasive charm",
            "drives personal agenda"
            )

    PSYCHOLOGIST = (
            "analyzes personal motives",
            "understands different perspectives",
            "studies cause and effect",
            "creates psychological profiles"
            )

    REPORTER = (
            "avid learner",
            "news bringer",
            "message giver",
            "grand herald"
            )
    
    GUARD = (
            "prevents accidents",
            "ensures collective safety",
            "navigates dangerous surroundings",
            "anticipates hazards"
            )

    SIGNALER = (
            "studies gestures",
            "makes up tail signs",
            "speaks in code",
            "commands with signals"
            )

    SOCIALITE = (
            "prominent background",
            "aristocratic power",
            "respected authority",
            "famous socialite"
            )

    SPORTER = (
            "imitates sporting activities",
            "trains with denmates",
            "skilled sporter",
            "master of a sport"
            )

    SUPPORTER = (
            "passive observer",
            "offers encouragement",
            "uplifts spirits",
            "strong moral support"
            )

    TRAINER = (
            "asks for advice",
            "studies techniques",
            "focuses on weakness",
            "personal trainer"
            )

    TRAVELER = (
            "curious about surroundings",
            "sight seer",
            "skilled tourist",
            "expert traveler"
            )

    TWOLEG = (
            "asks about twolegs",
            "part time kittypet",
            "studies twoleg interactions",
            "twoleg expert"
            )

    VOLUNTEER = (
            "cares for others",
            "eager helper",
            "charitable soul",
            "willing volunteer"
            )

    WRESTLER = (
            "starts play fights",
            "has a strong grasp",
            "wrestles opponents",
            "expert wrestler"
            )

    MIMICKER = (
            "repeats sounds",
            "copies vocal inflections",
            "repetitive chatterer",
            "perfect mimicry"
            )

    MINDFUL = (
            "sensitive of surroundings",
            "highly aware",
            "open mind",
            "enlightened"
            )

    MOURNER = (
            "grieves for the dead",
            "tells the departed's tales",
            "honored eulogist",
            "devoted mourner"
            )

    NEGOTIATOR = (
            "bargains for things",
            "offers solutions",
            "settles disputes",
           "negotiator"
            )
    
    NECROMANCER = (
            "resurrects insects",
            "defies death",
            "revives moribund",
            "necromancer"
            )
    
    NURSE = (
            "tends to denmates",
            "assists healers",
            "healer's assistant",
            "nurse"
            )
    
    ORATOR = (
            "speaks loudly",
            "makes speeches",
            "eloquent speaker",
            "known orator"
            )

    PAINTER = (
            "covered in mud",
            "enthusiastic dauber",
            "inspiring illustrator",
            "experienced painter"
            )

    PARENTING = (
            "offers praise and support",
            "cares for others",
            "respected nurturer",
            "beloved caregiver"
            )
    
    PLANNER = (
            "watches meetings",
            "offers praise",
            "hosts feasts",
            "plans parties"
            )

    PLAYING = (
            "plays around",
            "starts games with others",
            "invents games",
            "game maker"
            )

    PATROLLING = (
            "offers to join patrols",
            "joins the dawn patrol",
            "patrol enthusiast",
            "patrol leader"
            )

    PSYCHIC = (
            "senses strong feelings",
            "drawn to emotions",
            "emotionally perceptive",
            "reads minds"
            )

    POET = (
            "speaks from the heart",
            "rhymes words together",
            "eloquently speaks",
            "renowned poet"
            )
    
    POSSESSED = (
            "ghostly whispers",
            "acts oddly",
            "otherworldly gaze",
            "possessed"
            )
    PREACHER = (
            "curious about faith",
            "practices sermons",
            "spiritual leader",
            "respected preacher"
            )
    
    PROJECTION = (
            "shares emotions",
            "projects feelings",
            "manifests perception",
            "warps reality"
            )
    
    RANGER = (
            "throws pebbles",
            "attacks from a distance",
            "sharpened aim",
            "ranged attacks"
            )
    
    RECOVERER = (
            "heals quickly",
            "regenerates health",
            "hardy physique",
            "instant recovery"
            )
    
    REINCARNATED = (
            "dreams of a past life",
            "haunted by the past",
            "lives in the past",
            "reincarnated"
            )

    RESEARCHER = (
            "performs studies and tests",
            "discovers new concepts",
            "study evaluator",
            "detailed researcher"
            )
    
    RISEN = (
            "abnormal steps",
            "undead vessel",
            "risen walker",
            "ghastly figure"
            )
    
    RITE = (
            "tracks habits",
            "invents rituals",
            "honors traditions",
            "master of ceremonies"
            )

    SCHEMER = (
            "pulls pranks on others",
            "discord seeker",
            "chaos bringer",
            "trickster"
            )

    SCOUTER = (
            "seeks new things",
            "surveys environment",
            "reliable informant",
            "scout"
            )

    SCRIBE = (
            "makes stone carvings",
            "inscribes into stone",
            "stonemason",
            "scribe"
            )
    
    SIREN = (
            "comforting purrs",
            "enchanted lilt",
            "hypnotic voice",
            "warning call"
            )
    
    SPY = (
            "collects secrets",
            "gathers intelligence",
            "highly informed",
            "spymaster"
            )

    STARLESS = (
            "interested in outsiders",
            "studies culture",
            "questions authority",
            "welcomes outsiders"
            )

    STEALTH = (
            "pounces on others",
            "stays out of sight",
            "quiet pawsteps",
            "snake-like attacks"
            )

    STRATEGIST = (
            "makes plans",
            "thinks carefully",
            "detailed planner",
            "strategist"
            )

    STYLIST = (
            "cleans other's furs",
            "tidies loose fur strands",
            "dappers pelt appearances",
            "stylizes fur"
            )

    SUMMONER = (
            "watches over the dead",
            "talks with the supernatural",
            "controls spirits",
            "powerful spirit summoner"
            )

    TAMER = (
            "soft-spoken",
            "warm towards animals",
            "accompanies animals",
            "animal tamer"
            )

    THIEF = (
            "steals items",
            "sneaky paws",
            "cat burglar",
           "criminal mastermind"
            )
    
    TELEPATHIC = (
            "perceives unspoken actions", 
            "reads minds",
            "shares thoughts",
            "expert telepath"
            )
    
    TESTER = (
            "avid risk taker",
            "insatiable curiosity",
            "performs experiments",
            "conducts trials"
            )

    TRADER = (
            "swaps prey with others",
            "makes deals",
            "supplies resources",
            "traderer"
            )

    VISION = (
            "curious about visions",
            "vision interpreter",
            "predicts future",
            "masterful seer"
            )

    WEATHER = (
            "observes the weather",
            "studies the weather",
            "predicts weather patterns",
            "weather expert"
            )

    WEAVER = (
            "weaves nesting material",
            "careful claws",
            "mends items",
            "weaver"
            )
    
    MYTHOLOGICAL = (
            "distinct nature",
            "unique presence",
            "legendary ability",
            "mythological figure"
            )

    LEARNER = (
            "quick witted",
            "fast learner",
            "sharp memory",
            "expert memorizer"
            )

    COMPETITOR = (
            "watches competitions",
            "organizes competitions",
            "skilled competitor",
            "talented competitor"
            )

    CHALLENGER = (
            "observes sparring matches",
            "challenges others",
            "duel challenger",
            "sparring master"
            )

    BEHAVIORIST = (
            "sensitive to attitudes",
            "notices behavioral changes",
            "examines behavior",
            "interprets intentions"
            )

    HAUNTED = (
            "friends with spirits",
            "soul magnet",
            "phantom charmer",
            "haunted by specters"
            )

    RESURRECTED = (
            "summoned from the dead",
            "second chance",
            "borrowed time",
            "extended life"
            )

    PROJECTOR = (
        "glimpses into the afterlife",
        "projects consciousness",
        "walks with the dead",
        "afterlife visitor"
        )

    RETRIEVER = (
        "motivates others",
        "retrieves energy",
        "offers empowerment",
        "energizer"
        )

    EXTRACTOR = (
        "sensitive to altered energies",
        "focuses energy",
        "channels other's energy",
        "connected to life"
        )

    PURIFIER = (
        "deters negative emotions",
        "sends waves of joy",
        "light bringer",
        "pure soul"
        )

    TRANCER = (
        "dazed gaze",
        "goes into trances",
        "extended daydreams",
        "frequent musing"
        )

    DIVINER = (
        "obtains insightful suggestions",
        "deeply self-reflective",
        "gives life advice",
        "manifests futures"
        )

    @staticmethod
    def get_random(exclude: list = (), cat_group: "CatGroup" = None):
        """Get a random path, with more uncommon paths being less common."""

        all_unique = set()
        matching_unique = ()
        for grp, skills in GROUP_UNIQUE_SKILLS.items():
            all_unique.update(skills)
            if cat_group == grp:
                matching_unique = skills
        blocked = (all_unique - set(matching_unique)) | set(exclude)

        uncommon_paths = [
            i
            for i in (
                SkillPath.GHOST,
                SkillPath.PROPHET,
                SkillPath.CLAIRVOYANT,
                SkillPath.DREAM,
                SkillPath.OMEN,
                SkillPath.STAR,
                SkillPath.HEALER,
                SkillPath.DARK,
            )
            if i not in blocked
        ]

        if uncommon_paths and not int(random.random() * 15):
            return random.choice(uncommon_paths)

        common_paths = [
            i for i in list(SkillPath) if i not in blocked and i not in uncommon_paths
        ]
        # matching outsider-unique skills get extra weight
        weighted = list(common_paths)
        for skill in matching_unique:
            if skill in common_paths:
                weighted.extend([skill] * 3)
        return random.choice(weighted)


# Outsider-group-locked skills. Cats from these groups can roll them; cats
# from other groups can only get them from a parent.
GROUP_UNIQUE_SKILLS = {
    CatGroup.HOUSEHOLD: (
        SkillPath.TWOLEGCARE,
        SkillPath.CHARMER,
        SkillPath.SHOWCAT,
    ),
    CatGroup.LONER_GROUP: (
        SkillPath.WANDERER,
        SkillPath.SCAVENGER,
        SkillPath.SURVIVOR,
    ),
    CatGroup.ROGUE_GROUP: (
        SkillPath.BRAWLER,
        SkillPath.INTIMIDATOR,
        SkillPath.AMBUSHER,
    ),
}


class HiddenSkillEnum(Enum):
    ROGUE = "rogue's knowledge"
    LONER = "loner's knowledge"
    KITTYPET = "kittypet's knowledge"


class SkillTypeFlag(Flag):
    SUPERNATURAL = auto()
    STRONG = auto()
    AGILE = auto()
    SMART = auto()
    OBSERVANT = auto()
    SOCIAL = auto()


class Skill:
    """Skills handling functions mostly"""

    tier_ranges = ((0, 9), (10, 19), (20, 29))
    point_range = (0, 29)

    short_strings = {
        SkillPath.TEACHER: "teaching",
        SkillPath.HUNTER: "hunting",
        SkillPath.FIGHTER: "fighting",
        SkillPath.RUNNER: "running",
        SkillPath.CLIMBER: "climbing",
        SkillPath.SWIMMER: "swimming",
        SkillPath.SPEAKER: "speaking",
        SkillPath.MEDIATOR: "mediating",
        SkillPath.CLEVER: "clever",
        SkillPath.INSIGHTFUL: "advising",
        SkillPath.SENSE: "observing",
        SkillPath.KIT: "caretaking",
        SkillPath.STORY: "storytelling",
        SkillPath.LORE: "lorekeeping",
        SkillPath.CAMP: "campkeeping",
        SkillPath.HEALER: "healing",
        SkillPath.STAR: "StarClan",
        SkillPath.OMEN: "omen",
        SkillPath.DREAM: "dreaming",
        SkillPath.CLAIRVOYANT: "predicting",
        SkillPath.PROPHET: "prophesying",
        SkillPath.GHOST: "ghosts",
        SkillPath.DARK: "dark forest",
        SkillPath.GARDENER: "gardening",
        SkillPath.TWOLEGCARE: "twoleg care",
        SkillPath.CHARMER: "charming",
        SkillPath.SHOWCAT: "showcat",
        SkillPath.WANDERER: "wandering",
        SkillPath.SCAVENGER: "scavenging",
        SkillPath.SURVIVOR: "surviving",
        SkillPath.BRAWLER: "brawling",
        SkillPath.INTIMIDATOR: "intimidating",
        SkillPath.AMBUSHER: "ambushing",
        SkillPath.UNKNOWN: "unknown residence",
        SkillPath.WAKEFUL: "awake",
        SkillPath.DELIVERER: "delivery",
        SkillPath.DECORATOR: "decorator",
        SkillPath.LEADERSHIP: "great leader",
        SkillPath.AGILE: "agile",
        SkillPath.STEALTHY: "stealthy",
        SkillPath.MEMORY: "memorizing",
        SkillPath.MESSENGER: "messenger",
        SkillPath.ASSIST: "assisting",
        SkillPath.HISTORIAN: "history keeper",
        SkillPath.BOOKMAKER: "storymaker",
        SkillPath.TUNNELER: "tunneling",
        SkillPath.PATIENT: "patience",
        SkillPath.DETECTIVE: "solves mysteries",
        SkillPath.HERBALIST: "herbalist",
        SkillPath.CHEF: "chef",
        SkillPath.PRODIGY: "prodigy",
        SkillPath.EXPLORER: "exploring",
        SkillPath.TRACKER: "tracking",
        SkillPath.GUARDIAN: "guarding",
        SkillPath.NAVIGATOR: "navigating",
        SkillPath.SONG: "singing",
        SkillPath.GRACE: "grace",
        SkillPath.CLEAN: "cleaning",
        SkillPath.INNOVATOR: "innovating",
        SkillPath.COMFORTER: "comforting",
        SkillPath.MATCHMAKER: "matchmaking",
        SkillPath.THINKER: "thinking",
        SkillPath.COOPERATIVE: "cooperating",
        SkillPath.SCHOLAR: "learning",
        SkillPath.TIME: "efficient",
        SkillPath.TREASURE: "finding",
        SkillPath.FISHER: "fishing",
        SkillPath.LANGUAGE: "language",
        SkillPath.SLEEPER: "sleeping",
        SkillPath.DISGUISE: "disguiser",
        SkillPath.PYRO: "flame controller",
        SkillPath.HYDRO: "water hoarder",
        SkillPath.GIFTGIVER: "gives gifts",
        SkillPath.VIBES: "vibe detector",
        SkillPath.STARGAZER: "looks at the stars",
        SkillPath.IMMUNE: "immunity to sickness",
        SkillPath.MUSICVIBES: "musical aura",
        SkillPath.AURAVIBES: "pleasant aura",
        SkillPath.ANIMALTAKER: "loves animals",
        SkillPath.VET: "animal helper",
        SkillPath.ANIMALMAGNET: "animal attractor",

        SkillPath.ACTING: "acting",
        SkillPath.ANTHROPOLOGIST: "anthropology",
        SkillPath.ARCHAEOLOGIST: "archaeology",
        SkillPath.ARCHIVER: "archiving",
        SkillPath.ARRANGER: "arranging",
        SkillPath.ARTIFICER: "artificer",
        SkillPath.ARTISAN: "artistry",
        SkillPath.ASTRONOMER: "astronomy",
        SkillPath.BALANCE: "balancing",
        SkillPath.CARPENTER: "carpentry",
        SkillPath.COLLECTOR: "collecting",
        SkillPath.COMEDIAN: "comedy",
        SkillPath.DANCER: "dancing",
        SkillPath.DEBATER: "debating",
        SkillPath.DECEPTOR: "deception",
        SkillPath.DISCIPLINE: "disciplinary",
        SkillPath.ENFORCER: "enforcing",
        SkillPath.ETIQUETTE: "etiquette",
        SkillPath.EXERCISE: "exercising",
        SkillPath.EXORCIST: "exorcizing",
        SkillPath.FORAGER: "foraging",
        SkillPath.FORTITUDE: "fortitude",
        SkillPath.GEOGRAPHER: "geography",
        SkillPath.GRAVEKEEPER: "gravekeeping",
        SkillPath.GOSSIPER: "gossiping",
        SkillPath.GUARDING: "guarding",
        SkillPath.GUIDER: "guiding",
        SkillPath.HERDER: "herding",
        SkillPath.HIDING: "hiding",
        SkillPath.INTIMIDATION: "intimidation",
        SkillPath.INVENTOR: "inventing",
        SkillPath.MEDIUM: "mediumship",
        SkillPath.MENTALIST: "mentalist",
        SkillPath.REPORTER: "reporting",
        SkillPath.MIMICKER: "mimicry",
        SkillPath.MINDFUL: "mindfulness",
        SkillPath.MOURNER: "mourning",
        SkillPath.NEGOTIATOR: "negotiating",
        SkillPath.PAINTER: "painting",
        SkillPath.PARENTING: "parenting",
        SkillPath.PLAYING: "playing",
        SkillPath.PATROLLING: "patrolling",
        SkillPath.PSYCHIC: "psychic",
        SkillPath.POET: "poetry",
        SkillPath.RESEARCHER: "researching",
        SkillPath.SCHEMER: "scheming",
        SkillPath.SCOUTER: "scouting",
        SkillPath.SCRIBE: "scribing",
        SkillPath.STARLESS: "starless cats",
        SkillPath.STEALTH: "stealthing",
        SkillPath.STRATEGIST: "strategizing",
        SkillPath.STYLIST: "stylizing",
        SkillPath.SUMMONER: "summoning",
        SkillPath.TAMER: "taming",
        SkillPath.THIEF: "thievery",
        SkillPath.TRADER: "trading",
        SkillPath.VISION: "visions",
        SkillPath.WEATHER: "weather reporting",
        SkillPath.WEAVER: "weaving",

        SkillPath.AURA: "aura reading",
        SkillPath.ADVOCATE: "advocation",
        SkillPath.ASSASSIN: "assassinating",
        SkillPath.CHAMPION: "championship",
        SkillPath.COMMANDER: "commanding",
        SkillPath.COMPULSION: "compelling",
        SkillPath.CURSED: "cursed",
        SkillPath.DEATH: "death",
        SkillPath.ENTERTAINER: "entertaining",
        SkillPath.FAIRY: "fairy",
        SkillPath.ILLUSION: "illusions",
        SkillPath.LEGACY: "legacy",
        SkillPath.MEDITATION: "meditating",
        SkillPath.MINDER: "minding",
        SkillPath.NECROMANCER: "resurrecting",
        SkillPath.NURSE: "nursing",
        SkillPath.ORATOR: "oration",
        SkillPath.PLANNER: "planning",
        SkillPath.POSSESSED: "possessed",
        SkillPath.PREACHER: "preaching",
        SkillPath.PROJECTION: "projection",
        SkillPath.RANGER: "ranging",
        SkillPath.RECOVERER: "recovery",
        SkillPath.REINCARNATED: "reincarnated",
        SkillPath.RISEN: "undead",
        SkillPath.RITE: "ritualistic",
        SkillPath.SIREN: "siren",
        SkillPath.SPY: "spying",
        SkillPath.TELEPATHIC: "telepathy",
        SkillPath.TESTER: "testing",

        SkillPath.ANIMALOGIST: "animal studies",
        SkillPath.ARMORER: "weapon crafting",
        SkillPath.BUILDER: "body building",
        SkillPath.CAMPER: "camping",
        SkillPath.COMPANION: "companionship",
        SkillPath.CONSULTANT: "consulting",
        SkillPath.DIVER: "deep diving",
        SkillPath.FOLLOWER: "following commands",
        SkillPath.GAMBLER: "risk taking",
        SkillPath.GENEALOGIST: "pelt studies",
        SkillPath.GUARD: "safety guard",
        SkillPath.HIKER: "hiking",
        SkillPath.HYPNOTIST: "hypnotizing",
        SkillPath.LIFESAVER: "saving lives",
        SkillPath.LUCKY: "lucky",
        SkillPath.MANAGER: "project management",
        SkillPath.MECHANIC: "mechanics",
        SkillPath.PARANORMAL: "paranormal",
        SkillPath.PILGRIM: "pilgrimage",
        SkillPath.POLITICIAN: "politics",
        SkillPath.PSYCHOLOGIST: "psychoanalyzing",
        SkillPath.SIGNALER: "signaling",
        SkillPath.SOCIALITE: "social influence",
        SkillPath.SPORTER: "sporting",
        SkillPath.SUPPORTER: "supporting",
        SkillPath.TRAINER: "training",
        SkillPath.TRAVELER: "traveling",
        SkillPath.TWOLEG: "twoleg lore",
        SkillPath.VOLUNTEER: "volunteering",
        SkillPath.WRESTLER: "wrestling",

        SkillPath.MYTHOLOGICAL: "mythological",
        SkillPath.LEARNER: "learning",
        SkillPath.COMPETITOR: "competing",
        SkillPath.CHALLENGER: "challenging",
        SkillPath.BEHAVIORIST: "behaviorist",
        SkillPath.HAUNTED: "haunted",
        SkillPath.RESURRECTED: "resurrected",

        SkillPath.PROJECTOR: "projecting",
        SkillPath.RETRIEVER: "energy retrieval",
        SkillPath.EXTRACTOR: "energy refocusing",
        SkillPath.PURIFIER: "cleansing emotions",
        SkillPath.TRANCER: "trancing",
        SkillPath.DIVINER: "divining",
    }

    def __init__(self, path: SkillPath, points: int = 0, interest_only: bool = False):
        self.path = path
        self.interest_only = interest_only
        if points > self.point_range[1]:
            self._p = self.point_range[1]
        elif points < self.point_range[0]:
            self._p = self.point_range[0]
        else:
            self._p = points

    def __repr__(self) -> str:
        return f"<Skill: {self.path}, {self.points}, {self.tier}, {self.interest_only}>"

    def get_short_skill_string(self):
        """
        Returns a localized short string descriptor of the skill
        :return: string representing the skill
        """
        return i18n.t(f"cat.skills.{Skill.short_strings.get(self.path, 'unknown')}")

    @staticmethod
    def generate_from_save_string(save_string: str):
        """Generates the skill from the save string in the cat data"""
        if not save_string:
            return None

        split_values = save_string.split(",")
        if split_values[2].lower() == "true":
            interest = True
        else:
            interest = False

        return Skill(SkillPath[split_values[0]], int(split_values[1]), interest)

    @staticmethod
    def get_random_skill(
        points: int = None,
        point_tier: int = None,
        exclude=(),
        interest_only=False,
        cat_group: "CatGroup" = None,
        rng=random.Random(),
    ):
        """Generates a random skill. If wanted, you can specify a tier for the points
        value to be randomized within."""

        if isinstance(points, int):
            points = points
        elif isinstance(point_tier, int) and 1 <= point_tier <= 3:
            points = rng.randint(
                Skill.tier_ranges[point_tier - 1][0],
                Skill.tier_ranges[point_tier - 1][1],
            )
        else:
            points = rng.randint(Skill.point_range[0], Skill.point_range[1])

        if isinstance(exclude, SkillPath):
            exclude = [exclude]

        return Skill(
            SkillPath.get_random(exclude, cat_group=cat_group), points, interest_only
        )

    @property
    def points(self):
        return self._p

    @points.setter
    def points(self, val):
        if val > self.point_range[1]:
            self._p = self.point_range[1]
        elif val < self.point_range[0]:
            self._p = self.point_range[0]
        else:
            self._p = val

    @property
    def skill(self):
        """Skill property"""
        return self.path.value[self.tier]

    @skill.setter
    def skill(self):
        """Can't set the skill directly with this setter"""
        print("Can't set skill directly")

    @property
    def tier(self):
        """Returns the tier level of the skill"""
        if self.interest_only:
            return 0
        for _ran, i in zip(Skill.tier_ranges, range(1, 4)):
            if _ran[0] <= self.points <= _ran[1]:
                return i

        return 1

    @tier.setter
    def tier(self):
        print("Can't set tier directly")

    def get_points_to_tier(self, tier: int):
        """This is separate from the tier setter, since it will booonly allow you
        to set points to tier 1, 2, or 3, and never 0. Tier 0 is retricted to interest_only
        skills"""

        # Make sure it in the right range. If not, return.
        if not (1 <= tier <= 3):
            return

        # Adjust to 0-indexed ranges list
        return Skill.tier_ranges[tier - 1][0]

    def set_points_to_tier(self, tier: int):
        """This is separate from the tier setter, since it will only allow you
        to set points to tier 1, 2, or 3, and never 0. Tier 0 is restricted to interest_only
        skills"""

        # Make sure it in the right range. If not, return.
        if not (1 <= tier <= 3):
            return

        # Adjust to 0-indexed ranges list
        self.points = Skill.tier_ranges[tier - 1][0]

    def get_save_string(self):
        """Gets the string that is saved in the cat data"""
        return f"{self.path.name},{self.points},{self.interest_only}"

    def get_skill_from_string(self, string, interest=False, skill_object_only=False):
        """Returns a SkillPath given a string skill"""

        # LG
        if interest:
            interest_string = "True"
        else:
            interest_string = "False"
        for skill in SkillPath:
            if string in skill.value:
                index = skill.value.index(string)
                if skill_object_only:
                    return skill
                return self.generate_from_save_string(
                    f"{skill.name},{Skill.get_points_to_tier(self, tier=max(1,index))},{interest_string}"
                )

        return "String not found in any Enum"


class CatSkills:
    """
    Holds the cats skills, and handled changes in the skills.
    """

    # Mentor Inflence groups.
    # pylint: disable=unsupported-binary-operation
    influence_flags = {
        SkillPath.TEACHER: SkillTypeFlag.STRONG
        | SkillTypeFlag.AGILE
        | SkillTypeFlag.SMART
        | SkillTypeFlag.OBSERVANT
        | SkillTypeFlag.SOCIAL,
        SkillPath.HUNTER: SkillTypeFlag.STRONG
        | SkillTypeFlag.AGILE
        | SkillTypeFlag.OBSERVANT,
        SkillPath.FIGHTER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE,
        SkillPath.RUNNER: SkillTypeFlag.AGILE,
        SkillPath.CLIMBER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE,
        SkillPath.SWIMMER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE,
        SkillPath.SPEAKER: SkillTypeFlag.SOCIAL | SkillTypeFlag.SMART,
        SkillPath.MEDIATOR: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL,
        SkillPath.CLEVER: SkillTypeFlag.SMART,
        SkillPath.INSIGHTFUL: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.SENSE: SkillTypeFlag.OBSERVANT,
        SkillPath.KIT: SkillTypeFlag.SOCIAL,
        SkillPath.STORY: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL,
        SkillPath.LORE: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL,
        SkillPath.CAMP: SkillTypeFlag.OBSERVANT | SkillTypeFlag.SOCIAL,
        SkillPath.HEALER: SkillTypeFlag.SMART
        | SkillTypeFlag.OBSERVANT
        | SkillTypeFlag.SOCIAL,
        SkillPath.STAR: SkillTypeFlag.SUPERNATURAL,
        SkillPath.OMEN: SkillTypeFlag.SUPERNATURAL | SkillTypeFlag.OBSERVANT,
        SkillPath.DREAM: SkillTypeFlag.SUPERNATURAL,
        SkillPath.CLAIRVOYANT: SkillTypeFlag.SUPERNATURAL | SkillTypeFlag.OBSERVANT,
        SkillPath.PROPHET: SkillTypeFlag.SUPERNATURAL,
        SkillPath.GHOST: SkillTypeFlag.SUPERNATURAL,
        SkillPath.DARK: SkillTypeFlag.SUPERNATURAL,
        SkillPath.GARDENER: SkillTypeFlag.SMART,
        SkillPath.UNKNOWN: SkillTypeFlag.SUPERNATURAL,
        SkillPath.WAKEFUL: SkillTypeFlag.STRONG | SkillTypeFlag.OBSERVANT,
        SkillPath.DELIVERER: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL,
        SkillPath.DECORATOR: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.LEADERSHIP: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL,
        SkillPath.AGILE: SkillTypeFlag.AGILE | SkillTypeFlag.OBSERVANT,
        SkillPath.STEALTHY: SkillTypeFlag.SMART | SkillTypeFlag.AGILE | SkillTypeFlag.OBSERVANT,
        SkillPath.MEMORY: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.MESSENGER: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.ASSIST: SkillTypeFlag.STRONG | SkillTypeFlag.SOCIAL,
        SkillPath.HISTORIAN: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.BOOKMAKER: SkillTypeFlag.SOCIAL,
        SkillPath.TUNNELER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE,
        SkillPath.PATIENT: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.DETECTIVE: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.HERBALIST: SkillTypeFlag.SMART | SkillTypeFlag.SUPERNATURAL,
        SkillPath.CHEF: SkillTypeFlag.AGILE | SkillTypeFlag.SOCIAL,
        SkillPath.PRODIGY: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.EXPLORER: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.TRACKER: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.GUARDIAN: SkillTypeFlag.STRONG | SkillTypeFlag.OBSERVANT,
        SkillPath.NAVIGATOR: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.SONG: SkillTypeFlag.SOCIAL,
        SkillPath.GRACE: SkillTypeFlag.AGILE,
        SkillPath.CLEAN: SkillTypeFlag.OBSERVANT | SkillTypeFlag.SOCIAL,
        SkillPath.INNOVATOR: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.COMFORTER: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.MATCHMAKER: SkillTypeFlag.SOCIAL | SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.THINKER: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.COOPERATIVE: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.SCHOLAR: SkillTypeFlag.SMART,
        SkillPath.TIME: SkillTypeFlag.AGILE | SkillTypeFlag.SMART,
        SkillPath.TREASURE: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.FISHER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE | SkillTypeFlag.OBSERVANT,
        SkillPath.LANGUAGE: SkillTypeFlag.SOCIAL,
        SkillPath.SLEEPER: SkillTypeFlag.STRONG,
        SkillPath.DISGUISE: SkillTypeFlag.AGILE | SkillTypeFlag.OBSERVANT | SkillTypeFlag.SMART,
        SkillPath.PYRO: SkillTypeFlag.SMART,
        SkillPath.HYDRO: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.GIFTGIVER: SkillTypeFlag.SOCIAL,
        SkillPath.VIBES: SkillTypeFlag.OBSERVANT | SkillTypeFlag.SOCIAL | SkillTypeFlag.SMART,
        SkillPath.STARGAZER: SkillTypeFlag.OBSERVANT | SkillTypeFlag.SOCIAL,
        SkillPath.MUSICVIBES: SkillTypeFlag.SOCIAL,
        SkillPath.AURAVIBES: SkillTypeFlag.SOCIAL,
        SkillPath.ANIMALTAKER: SkillTypeFlag.SOCIAL,
        SkillPath.VET: SkillTypeFlag.OBSERVANT | SkillTypeFlag.SOCIAL,
        SkillPath.ANIMALMAGNET: SkillTypeFlag.SOCIAL,
        SkillPath.IMMUNE: SkillTypeFlag.OBSERVANT,

        SkillPath.ACTING: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.ANTHROPOLOGIST: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.ARCHAEOLOGIST: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.ARCHIVER: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.ARRANGER: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.ARTIFICER: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.ARTISAN: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.ASTRONOMER: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.BALANCE: SkillTypeFlag.AGILE,
        SkillPath.CARPENTER: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.COLLECTOR: SkillTypeFlag.AGILE,
        SkillPath.COMEDIAN: SkillTypeFlag.SOCIAL,
        SkillPath.DANCER: SkillTypeFlag.AGILE,
        SkillPath.DEBATER: SkillTypeFlag.SOCIAL,
        SkillPath.DECEPTOR: SkillTypeFlag.SOCIAL,
        SkillPath.DISCIPLINE: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.ENFORCER: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.ETIQUETTE: SkillTypeFlag.SOCIAL,
        SkillPath.EXERCISE: SkillTypeFlag.AGILE,
        SkillPath.EXORCIST: SkillTypeFlag.SUPERNATURAL,
        SkillPath.FORAGER: SkillTypeFlag.AGILE,
        SkillPath.GEOGRAPHER: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.GRAVEKEEPER: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.GOSSIPER: SkillTypeFlag.SOCIAL,
        SkillPath.GUARDING: SkillTypeFlag.AGILE,
        SkillPath.GUIDER: SkillTypeFlag.SOCIAL,
        SkillPath.HERDER: SkillTypeFlag.AGILE,
        SkillPath.HIDING: SkillTypeFlag.AGILE,
        SkillPath.FORTITUDE: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.INTIMIDATION: SkillTypeFlag.STRONG,
        SkillPath.INVENTOR: SkillTypeFlag.AGILE | SkillTypeFlag.SMART,
        SkillPath.MEDIUM: SkillTypeFlag.SUPERNATURAL,
        SkillPath.MENTALIST: SkillTypeFlag.SMART,
        SkillPath.REPORTER: SkillTypeFlag.SOCIAL | SkillTypeFlag.SMART | SkillTypeFlag.AGILE,
        SkillPath.MIMICKER: SkillTypeFlag.SOCIAL | SkillTypeFlag.SMART,
        SkillPath.MINDFUL: SkillTypeFlag.OBSERVANT,
        SkillPath.MOURNER: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.NEGOTIATOR: SkillTypeFlag.SOCIAL | SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.PAINTER: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.PARENTING: SkillTypeFlag.SOCIAL,
        SkillPath.PLAYING: SkillTypeFlag.SOCIAL,
        SkillPath.PATROLLING: SkillTypeFlag.SOCIAL,
        SkillPath.PSYCHIC: SkillTypeFlag.OBSERVANT,
        SkillPath.POET: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL,
        SkillPath.RESEARCHER: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.SCAVENGER: SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE,
        SkillPath.SCHEMER: SkillTypeFlag.SOCIAL | SkillTypeFlag.SMART,
        SkillPath.SCOUTER: SkillTypeFlag.AGILE | SkillTypeFlag.OBSERVANT | SkillTypeFlag.SMART,
        SkillPath.SCRIBE: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.STARLESS: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.STEALTH: SkillTypeFlag.AGILE | SkillTypeFlag.SMART,
        SkillPath.STRATEGIST: SkillTypeFlag.OBSERVANT | SkillTypeFlag.SMART,
        SkillPath.STYLIST: SkillTypeFlag.SOCIAL | SkillTypeFlag.SMART,
        SkillPath.SUMMONER: SkillTypeFlag.SUPERNATURAL,
        SkillPath.TAMER: SkillTypeFlag.STRONG | SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.THIEF: SkillTypeFlag.AGILE | SkillTypeFlag.SMART,
        SkillPath.TRADER: SkillTypeFlag.SOCIAL | SkillTypeFlag.SMART,
        SkillPath.VISION: SkillTypeFlag.SUPERNATURAL,
        SkillPath.WEATHER: SkillTypeFlag.OBSERVANT | SkillTypeFlag.SMART,
        SkillPath.WEAVER: SkillTypeFlag.AGILE,

        SkillPath.AURA: SkillTypeFlag.SUPERNATURAL,
        SkillPath.ADVOCATE: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.ASSASSIN: SkillTypeFlag.STRONG | SkillTypeFlag.OBSERVANT,
        SkillPath.CHAMPION: SkillTypeFlag.STRONG,
        SkillPath.COMMANDER: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL,
        SkillPath.COMPULSION: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.CURSED: SkillTypeFlag.SUPERNATURAL,
        SkillPath.DEATH: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.SUPERNATURAL,
        SkillPath.ENTERTAINER: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.FAIRY: SkillTypeFlag.SUPERNATURAL,
        SkillPath.ILLUSION: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.LEGACY: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL,
        SkillPath.MEDITATION: SkillTypeFlag.SMART,
        SkillPath.MINDER: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL,
        SkillPath.NECROMANCER: SkillTypeFlag.SUPERNATURAL,
        SkillPath.NURSE: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.ORATOR: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.PLANNER: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.POSSESSED: SkillTypeFlag.SUPERNATURAL,
        SkillPath.PREACHER: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.PROJECTION: SkillTypeFlag.SUPERNATURAL,
        SkillPath.RANGER: SkillTypeFlag.STRONG,
        SkillPath.RECOVERER: SkillTypeFlag.STRONG,
        SkillPath.REINCARNATED: SkillTypeFlag.SUPERNATURAL,
        SkillPath.RISEN: SkillTypeFlag.SUPERNATURAL,
        SkillPath.RITE: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.SIREN: SkillTypeFlag.SUPERNATURAL,
        SkillPath.SPY: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.TELEPATHIC: SkillTypeFlag.SUPERNATURAL,
        SkillPath.TESTER: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,

        SkillPath.ANIMALOGIST: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.ARMORER: SkillTypeFlag.OBSERVANT,
        SkillPath.BUILDER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE,
        SkillPath.CAMPER: SkillTypeFlag.OBSERVANT,
        SkillPath.COMPANION: SkillTypeFlag.SOCIAL,
        SkillPath.CONSULTANT: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL,
        SkillPath.DIVER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE,
        SkillPath.FOLLOWER: SkillTypeFlag.SOCIAL,
        SkillPath.GAMBLER: SkillTypeFlag.AGILE,
        SkillPath.GENEALOGIST: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.GUARD: SkillTypeFlag.SOCIAL | SkillTypeFlag.AGILE,
        SkillPath.HIKER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE,
        SkillPath.HYPNOTIST: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.SUPERNATURAL,
        SkillPath.LIFESAVER: SkillTypeFlag.AGILE,
        SkillPath.LUCKY: SkillTypeFlag.AGILE | SkillTypeFlag.SUPERNATURAL,
        SkillPath.MANAGER: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.MECHANIC: SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.PARANORMAL: SkillTypeFlag.SUPERNATURAL,
        SkillPath.PILGRIM: SkillTypeFlag.SUPERNATURAL,
        SkillPath.POLITICIAN: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.PSYCHOLOGIST: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.SIGNALER: SkillTypeFlag.SMART | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE,
        SkillPath.SOCIALITE: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.SPORTER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE,
        SkillPath.SUPPORTER: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.TRAINER: SkillTypeFlag.STRONG | SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE,
        SkillPath.TRAVELER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE,
        SkillPath.TWOLEG: SkillTypeFlag.SMART,
        SkillPath.VOLUNTEER: SkillTypeFlag.SOCIAL,
        SkillPath.WRESTLER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE,

        SkillPath.MYTHOLOGICAL: SkillTypeFlag.SOCIAL,
        SkillPath.LEARNER: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.AGILE | SkillTypeFlag.SMART,
        SkillPath.COMPETITOR: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.STRONG,
        SkillPath.CHALLENGER: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.STRONG, 
        SkillPath.BEHAVIORIST: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.SMART, 
        SkillPath.HAUNTED: SkillTypeFlag.OBSERVANT | SkillTypeFlag.SUPERNATURAL,
        SkillPath.RESURRECTED: SkillTypeFlag.SUPERNATURAL,

        SkillPath.PROJECTOR: SkillTypeFlag.SUPERNATURAL,
        SkillPath.RETRIEVER: SkillTypeFlag.SUPERNATURAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.SOCIAL,
        SkillPath.EXTRACTOR: SkillTypeFlag.SUPERNATURAL,
        SkillPath.PURIFIER: SkillTypeFlag.SUPERNATURAL | SkillTypeFlag.OBSERVANT,
        SkillPath.TRANCER: SkillTypeFlag.SUPERNATURAL | SkillTypeFlag.OBSERVANT,
        SkillPath.DIVINER: SkillTypeFlag.SUPERNATURAL | SkillTypeFlag.OBSERVANT | SkillTypeFlag.SOCIAL,

        SkillPath.TWOLEGCARE: SkillTypeFlag.SOCIAL | SkillTypeFlag.OBSERVANT,
        SkillPath.CHARMER: SkillTypeFlag.SOCIAL,
        SkillPath.SHOWCAT: SkillTypeFlag.SOCIAL | SkillTypeFlag.AGILE,
        SkillPath.WANDERER: SkillTypeFlag.AGILE | SkillTypeFlag.SMART | SkillTypeFlag.OBSERVANT,
        SkillPath.SURVIVOR: SkillTypeFlag.STRONG | SkillTypeFlag.SMART,
        SkillPath.BRAWLER: SkillTypeFlag.STRONG | SkillTypeFlag.AGILE,
        SkillPath.INTIMIDATOR: SkillTypeFlag.STRONG | SkillTypeFlag.SOCIAL,
        SkillPath.AMBUSHER: SkillTypeFlag.AGILE | SkillTypeFlag.OBSERVANT,
    }

    # pylint: enable=unsupported-binary-operation

    def __init__(
        self,
        skill_dict=None,
        primary_path: SkillPath = None,
        primary_points: int = 0,
        secondary_path: SkillPath = None,
        secondary_points: int = 0,
        hidden_skill: HiddenSkillEnum = None,
        interest_only=False,
    ):
        if skill_dict:
            self.primary = Skill.generate_from_save_string(skill_dict["primary"])
            self.secondary = Skill.generate_from_save_string(skill_dict["secondary"])
            self.hidden = (
                HiddenSkillEnum[skill_dict["hidden"]] if skill_dict["hidden"] else None
            )
        else:
            if primary_path:
                self.primary = Skill(primary_path, primary_points, interest_only)
            else:
                self.primary = None
            if secondary_path:
                self.secondary = Skill(secondary_path, secondary_points, interest_only)
            else:
                self.secondary = None

            self.hidden = hidden_skill

    def __repr__(self) -> str:
        return f"<CatSkills: Primary: |{self.primary}|, Secondary: |{self.secondary}|, Hidden: |{self.hidden}|>"

    def get_all(self) -> dict:
        skill_dict = {}
        if self.primary:
            skill_dict[self.primary.path] = self.primary.tier
        if self.secondary:
            skill_dict[self.secondary.path] = self.secondary.tier

        return skill_dict

    @staticmethod
    def generate_new_catskills(
        rank: CatRank,
        age: CatAge,
        hidden_skill: HiddenSkillEnum = None,
        cat_group: "CatGroup" = None,
        rng=random.Random(),
    ):
        """Generates a new skill"""
        new_skill = CatSkills()

        new_skill.hidden = hidden_skill

        if rank == CatRank.NEWBORN or age == CatAge.NEWBORN:
            pass
        elif rank == CatRank.KITTEN or age == CatAge.KITTEN:
            new_skill.primary = Skill.get_random_skill(
                points=0, interest_only=True, cat_group=cat_group, rng=rng
            )
        elif rank.is_any_apprentice_rank() or age == CatAge.ADOLESCENT:
            new_skill.primary = Skill.get_random_skill(
                point_tier=1, interest_only=True, cat_group=cat_group, rng=rng
            )
            if rng.randint(1, 3) == 1:
                new_skill.secondary = Skill.get_random_skill(
                    point_tier=1,
                    interest_only=True,
                    exclude=new_skill.primary.path,
                    cat_group=cat_group,
                    rng=rng,
                )
        else:
            primary_tier = 1
            secondary_tier = 1
            if age == CatAge.YOUNG_ADULT:
                primary_tier += rng.randint(0, 1)
                secondary_tier += rng.randint(0, 1)
            elif age == CatAge.ADULT:
                primary_tier += rng.randint(0, 2)
                secondary_tier += rng.randint(0, 1)
            elif age == CatAge.SENIOR_ADULT:
                primary_tier += rng.randint(1, 2)
                secondary_tier += rng.randint(0, 1)
            elif age == CatAge.SENIOR:
                primary_tier -= rng.randint(0, 1)

            new_skill.primary = Skill.get_random_skill(
                point_tier=primary_tier, cat_group=cat_group, rng=rng
            )
            if rng.randint(1, 2) == 1:
                new_skill.secondary = Skill.get_random_skill(
                    point_tier=secondary_tier,
                    exclude=new_skill.primary.path,
                    cat_group=cat_group,
                    rng=rng,
                )

        return new_skill

    def get_skill_dict(self):
        return {
            "primary": self.primary.get_save_string() if self.primary else None,
            "secondary": self.secondary.get_save_string() if self.secondary else None,
            "hidden": self.hidden.name if self.hidden else None,
        }

    def skill_string(self, short=False, is_adolescent=False):
        output = []

        if short:
            if self.primary:
                output.append(self.primary.get_short_skill_string())
            if self.secondary:
                output.append(self.secondary.get_short_skill_string())
        else:
            if self.primary:
                if is_adolescent and self.primary.tier == 0:
                    output.append(i18n.t(f"cat.skills.{self.primary.skill}.5"))
                else:
                    output.append(i18n.t(f"cat.skills.{self.primary.skill}"))
            if self.secondary:
                if is_adolescent and self.secondary.tier == 0:
                    output.append(i18n.t(f"cat.skills.{self.secondary.skill}.5"))
                else:
                    output.append(i18n.t(f"cat.skills.{self.secondary.skill}"))

        if not output:
            return "???"

        out = " & ".join(output)
        return out

    def mentor_influence(self, mentor):
        """Handles mentor influence on the cat's skill
        :param mentor: the mentor's cat object
        """

        if not mentor:
            return

        # Determine if any skills can be effected
        mentor_tags = (
            CatSkills.influence_flags[mentor.skills.primary.path]
            if mentor.skills.primary
            else None
        )

        can_primary = (
            bool(CatSkills.influence_flags[self.primary.path] & mentor_tags)
            if self.primary and mentor_tags
            else False
        )
        can_secondary = (
            bool(CatSkills.influence_flags[self.secondary.path] & mentor_tags)
            if self.secondary and mentor_tags
            else False
        )

        # If nothing can be effected, just return as well.
        if not (can_primary or can_secondary):
            return

        amount_effect = random.randint(1, 4)

        if can_primary and can_secondary:
            if random.randint(1, 2) == 1:
                self._add_skill(self.primary, amount_effect)
                path = self.primary.path
            else:
                self._add_skill(self.secondary, amount_effect)
                path = self.secondary.path
        elif can_primary:
            self._add_skill(self.primary, amount_effect)
            path = self.primary.path
        else:
            self._add_skill(self.secondary, amount_effect)
            path = self.secondary.path

        return mentor.ID, path, amount_effect

    @staticmethod
    def _add_skill(skill: Skill, amount: int):
        """adds skill points, scaled by progress.difficulty_modifier"""

        scaled = scale_progress(skill.points, Skill.point_range[1], amount)
        # stochastic rounding so points still increase on average
        gain = int(scaled)
        if random.random() < scaled - gain:
            gain += 1
        skill.points += gain

    def progress_skill(self, the_cat):
        """
        this function should be run every moon for every cat to progress their skills accordingly
        :param the_cat: the cat object for affected cat
        """
        if the_cat.status.rank == CatRank.NEWBORN or the_cat.moons <= 0:
            return

        # Give a primary is there isn't one already, and the cat is older than one moon.
        if not self.primary:
            parents = [
                the_cat.fetch_cat(i)
                for i in [the_cat.parent1, the_cat.parent2] + the_cat.adoptive_parents
                if type(the_cat) == type(the_cat.fetch_cat(i))
            ]
            parental_paths = [
                i.skills.primary.path for i in parents if i.skills.primary
            ] + [i.skills.secondary.path for i in parents if i.skills.secondary]

            # If there are parental paths, flip a coin to determine if they will get a parents path
            if parental_paths and random.randint(0, 1):
                self.primary = Skill(
                    random.choice(parental_paths),
                    points=0,
                    interest_only=the_cat.status.rank.is_any_apprentice_rank()
                    or the_cat.status.rank == CatRank.KITTEN,
                )
            else:
                self.primary = Skill.get_random_skill(
                    points=0,
                    interest_only=the_cat.status.rank.is_any_apprentice_rank()
                    or the_cat.status.rank == CatRank.KITTEN,
                    cat_group=the_cat.status.group,
                )

        if the_cat.status.is_clancat:
            if the_cat.status.rank == CatRank.KITTEN:
                # Check to see if the cat gains a secondary
                if not self.secondary and not int(random.random() * 22):
                    # if there's no secondary skill, try to give one!
                    self.secondary = Skill.get_random_skill(
                        points=0,
                        interest_only=True,
                        exclude=self.primary.path,
                        cat_group=the_cat.status.group,
                    )

                # if the the_cat has skills, check if they get any points this moon
                if not int(random.random() * 4):
                    amount_effect = random.randint(1, 4)
                    if self.primary and self.secondary:
                        if random.randint(1, 2) == 1:
                            self._add_skill(self.primary, amount_effect)
                        else:
                            self._add_skill(self.secondary, amount_effect)
                    elif self.primary:
                        self._add_skill(self.primary, amount_effect)

            elif the_cat.status.rank.is_any_apprentice_rank():
                # Check to see if the cat gains a secondary
                if not self.secondary and not int(random.random() * 22):
                    # if there's no secondary skill, try to give one!
                    self.secondary = Skill.get_random_skill(
                        points=0,
                        interest_only=True,
                        exclude=self.primary.path,
                        cat_group=the_cat.status.group,
                    )

                # Check if they get any points this moon
                if not int(random.random() * 4):
                    amount_effect = random.randint(2, 5)
                    if self.primary and self.secondary:
                        if random.randint(1, 2) == 1:
                            self._add_skill(self.primary, amount_effect)
                        else:
                            self._add_skill(self.secondary, amount_effect)
                    elif self.primary:
                        self._add_skill(self.primary, amount_effect)

            elif the_cat.moons > 120:
                # for old cats, we want to check if the skills start to degrade at all, age is the great equalizer

                self.primary.interest_only = False
                if self.secondary:
                    self.secondary.interest_only = False

                chance = max(1, 160 - the_cat.moons)
                if not int(
                    random.random() * chance
                ):  # chance increases as the_cat ages
                    self.primary.points -= 1
                    if self.secondary:
                        self.secondary.points -= 1
            else:
                # If they are still in "interest" stage, there is a change to swap primary and secondary
                # If they are still in "interest" but reached this part, they just graduated.
                if self.primary.interest_only and self.secondary:
                    flip = random.choices(
                        [False, True],
                        [self.primary.points + 1, self.secondary.points + 1],
                    )[0]
                    if flip:
                        _temp = self.primary
                        self.primary = self.secondary
                        self.secondary = _temp

                self.primary.interest_only = False
                if self.secondary:
                    self.secondary.interest_only = False

                # If a cat doesn't can a secondary, have a small change for them to get one.
                # but, only a first-tier skill.
                if not self.secondary and not int(random.random() * 300):
                    self.secondary = Skill.get_random_skill(
                        exclude=self.primary.path,
                        point_tier=1,
                        cat_group=the_cat.status.group,
                    )

                # There is a change for primary to continue to improve throughout life
                # That chance decreases as the cat gets older.
                # This is to simulate them reaching their "peak"
                if not int(random.random() * int(the_cat.moons / 4)):
                    self._add_skill(self.primary, 1)
        else:
            # For outside cats, just check interest and flip it if needed.
            # Going on age, rather than status here.
            if the_cat.age not in (CatAge.KITTEN, CatAge.ADOLESCENT):
                self.primary.interest_only = False
                if self.secondary:
                    self.secondary.interest_only = False

    def meets_skill_requirement(
        self, path: Union[str, SkillPath, HiddenSkillEnum], min_tier: int = 0
    ) -> bool:
        """Check if a cat meets a given skill requirement.

        :param Union[str, SkillPath, HiddenSkillEnum] path: todo: someone describe this amalgam
        :param int min_tier: the lowest tier of skill that will pass this test
        :return bool: True if cat meets skill requirement
        """

        if isinstance(path, str):
            try:
                path = SkillPath[path]
            except KeyError:
                raise KeyError(f"{path} is not a real skill path")

        if isinstance(path, SkillPath):
            if self.primary:
                # LG
                if min_tier == -1:
                    if path != self.primary.path and (
                        (
                            not self.secondary
                            or (self.secondary and path != self.secondary.path)
                        )
                    ):
                        return True
                else:
                    # --
                    if path == self.primary.path and self.primary.tier >= min_tier:
                        return True

            if self.secondary:
                # LG
                if min_tier == -1:
                    if path != self.secondary.path and (
                        (
                            not self.primary
                            or (self.primary and path != self.primary.path)
                        )
                    ):
                        return True
                else:
                    # --
                    if path == self.secondary.path and self.secondary.tier >= min_tier:
                        return True

        return False

    def check_skill_requirement_list(self, skill_list: list) -> int:
        """Takes a whole list of skill requirements in the form
        [ "SKILL_PATH,MIN_TIER" ... ] and determines how many skill
        requirements are met. The list format is used in all patrol and event skill
        restrictions. Returns an integer value of how many skills requirements are met.
        """
        skills_meet = 0
        for _skill in skill_list:
            info = _skill.split(",")

            if "-" in info[0]:
                is_exclusionary = True
                info[0] = info[0].replace("-", "")
            else:
                is_exclusionary = False

            if len(info) != 2:
                print("Incorrectly formatted skill restriction", _skill)
                continue
            try:
                min_tier = int(info[1])
            except ValueError:
                print("Min Skill Tier cannot be converted to int", _skill)
                continue

            if self.meets_skill_requirement(info[0], min_tier):
                if info[0] == self.primary.path:
                    skills_meet += self.primary.tier
                elif self.secondary:
                    skills_meet += self.secondary.tier
                break

            elif is_exclusionary:
                skills_meet += self.primary.tier
                break

        return skills_meet

    @staticmethod
    def get_skills_from_old(old_skill, rank: CatRank, age: CatAge):
        """Generates a CatSkill object"""
        new_skill = CatSkills()
        conversion = {
            "strong connection to StarClan": (SkillPath.STAR, 2),
            "good healer": (SkillPath.HEALER, 1),
            "great healer": (SkillPath.HEALER, 2),
            "fantastic healer": (SkillPath.HEALER, 3),
            "good teacher": (SkillPath.TEACHER, 1),
            "great teacher": (SkillPath.TEACHER, 2),
            "fantastic teacher": (SkillPath.TEACHER, 3),
            "good mediator": (SkillPath.MEDIATOR, 1),
            "great mediator": (SkillPath.MEDIATOR, 2),
            "excellent mediator": (SkillPath.MEDIATOR, 3),
            "smart": (SkillPath.CLEVER, 1),
            "very smart": (SkillPath.CLEVER, 2),
            "extremely smart": (SkillPath.CLEVER, 3),
            "good hunter": (SkillPath.HUNTER, 1),
            "great hunter": (SkillPath.HUNTER, 2),
            "fantastic hunter": (SkillPath.HUNTER, 3),
            "good fighter": (SkillPath.FIGHTER, 1),
            "great fighter": (SkillPath.FIGHTER, 2),
            "excellent fighter": (SkillPath.FIGHTER, 3),
            "good speaker": (SkillPath.SPEAKER, 1),
            "great speaker": (SkillPath.SPEAKER, 2),
            "excellent speaker": (SkillPath.SPEAKER, 3),
            "good storyteller": (SkillPath.STORY, 1),
            "great storyteller": (SkillPath.STORY, 2),
            "fantastic storyteller": (SkillPath.STORY, 3),
            "smart tactician": (SkillPath.INSIGHTFUL, 1),
            "valuable tactician": (SkillPath.INSIGHTFUL, 2),
            "valuable insight": (SkillPath.INSIGHTFUL, 3),
            "good kitsitter": (SkillPath.KIT, 1),
            "great kitsitter": (SkillPath.KIT, 2),
            "beloved kitsitter": (SkillPath.KIT, 3),
            "camp keeper": (SkillPath.CAMP, 3),
            "den builder": (SkillPath.CAMP, 2),
            "omen sight": (SkillPath.OMEN, 3),
            "dream walker": (SkillPath.DREAM, 2),
            "clairvoyant": (SkillPath.CLAIRVOYANT, 2),
            "prophet": (SkillPath.PROPHET, 3),
            "lore keeper": (SkillPath.LORE, 2),
            "keen eye": (SkillPath.SENSE, 2),
        }

        old_skill = old_skill.strip()
        if old_skill in conversion:
            new_skill.primary = Skill(conversion[old_skill][0])
            new_skill.primary.set_points_to_tier(conversion[old_skill][1])
        else:
            new_skill = CatSkills.generate_new_catskills(rank, age)

        return new_skill
