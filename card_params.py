# Игрок
ME = "ME"
ENEMY = "ENEMY"

# Тип карточки
GOLDEN = "GOLDEN"
NORMAL = "NORMAL"
SPECIAL = "SPECIAL"

# Поле
MELEE = "MELEE"
RANGED = "RANGED"
SIEGE = "SIEGE"
MELEE_RANGED = "MELEE_RANGED"
SPECIAL_FIELD = "SPECIAL_FIELD"

# Скиллы
NON_SKILL = "-"
SPY = "SPY"
COMMAND_HORN = "COMMAND_HORN"
PLUS_ONE = "PLUS_ONE"
KILL_MELEE = "KILL_MELEE"
SKILL_RAISE = "SKILL_RAISE"
SUMMONING = "SUMMONING"
DOUBLING = "DOUBLING"
KILL_STRONGEST = "KILL_STRONGEST"
MARDREM = "MARDREM"
WAKE_UP_MARDREM = "WAKE_UP_MARDREM"
PHOENIX = "PHOENIX"

# Свойства карточек
CARD_PARAMS = {
    "avallach-2": [0, GOLDEN, MELEE, SPY],
    "cirilla-2": [15, GOLDEN, MELEE, NON_SKILL],
    "dandelion-2": [2, NORMAL, MELEE, COMMAND_HORN],
    "dandelion-2_copy": [2, NORMAL, MELEE, COMMAND_HORN],
    "draug": [10, GOLDEN, MELEE, NON_SKILL],
    "emiel-regis-2": [5, NORMAL, MELEE, NON_SKILL],
    "geralt-of-rivia-2": [15, GOLDEN, MELEE, NON_SKILL],
    "iorveth": [10, GOLDEN, RANGED, NON_SKILL],
    "isengrim-faoiltiarna": [10, GOLDEN, MELEE, PLUS_ONE],
    "leshen": [10, GOLDEN, RANGED, NON_SKILL],
    "letho-of-gulet": [10, GOLDEN, MELEE, NON_SKILL],
    "triss-merigold-2": [7, GOLDEN, MELEE, NON_SKILL],
    "villentretenmerth-2": [7, NORMAL, MELEE, KILL_MELEE],
    "yennefer-of-vengerberg-2": [7, GOLDEN, RANGED, SKILL_RAISE],
    "zoltan-chivay-2": [5, NORMAL, MELEE, NON_SKILL],
    "arachas-behemoth": [6, NORMAL, SIEGE, SUMMONING],
    "botcling": [4, NORMAL, MELEE, NON_SKILL],
    "crone-brewess": [6, NORMAL, MELEE, SUMMONING],
    "crone-weavess": [6, NORMAL, MELEE, SUMMONING],
    "crone-whispess": [6, NORMAL, MELEE, SUMMONING],
    "earth-elemental": [6, NORMAL, SIEGE, NON_SKILL],
    "fiend": [6, NORMAL, MELEE, NON_SKILL],
    "fire-elemental": [6, NORMAL, SIEGE, NON_SKILL],
    "frightener": [5, NORMAL, MELEE, NON_SKILL],
    "ice-giant": [5, NORMAL, SIEGE, NON_SKILL],
    "imlerith": [10, GOLDEN, MELEE, NON_SKILL],
    "keyran": [8, GOLDEN, MELEE_RANGED, PLUS_ONE],
    "plague-maiden": [5, NORMAL, MELEE, NON_SKILL],
    "vampire-bruxa": [4, NORMAL, MELEE, SUMMONING],
    "vampire-katakan": [5, NORMAL, MELEE, SUMMONING],
    "werewolf": [5, NORMAL, MELEE, NON_SKILL],
    "archer-support-1": [1, NORMAL, RANGED, SKILL_RAISE],
    "black-infantry-archer-1": [10, NORMAL, RANGED, NON_SKILL],
    "cahir-mawr-dyffryn-aep-ceallach": [6, NORMAL, MELEE, NON_SKILL],
    "cynthia": [4, NORMAL, RANGED, NON_SKILL],
    "fringilla-vigo": [6, NORMAL, RANGED, NON_SKILL],
    "heavy-zerrikanian-fire-scorpion": [10, NORMAL, SIEGE, NON_SKILL],
    "menno-coehoorn": [10, GOLDEN, MELEE, SKILL_RAISE],
    "morvran-voorhis": [10, GOLDEN, SIEGE, NON_SKILL],
    "puttkammer": [3, NORMAL, RANGED, NON_SKILL],
    "stefan-skellen": [9, NORMAL, MELEE, SPY],
    "tibor-eggebracht": [10, GOLDEN, RANGED, NON_SKILL],
    "vattier-de-rideaux": [4, NORMAL, MELEE, SPY],
    "young-emissary-1": [5, NORMAL, MELEE, DOUBLING],
    "blueboy-lugos": [6, NORMAL, MELEE, NON_SKILL],
    "cerys": [10, GOLDEN, MELEE, SUMMONING],
    "clan-an-craite-warrior": [6, NORMAL, MELEE, DOUBLING],
    "clan-dimun-pirate": [6, NORMAL, RANGED, KILL_STRONGEST],
    "clan-heymaey-skald": [4, NORMAL, MELEE, NON_SKILL],
    "ermion": [8, GOLDEN, RANGED, WAKE_UP_MARDREM],
    "hemdall": [11, GOLDEN, MELEE, NON_SKILL],
    "hjalmar": [10, GOLDEN, RANGED, NON_SKILL],
    "kambi": [0, NORMAL, MELEE, PHOENIX],
    "madman-lugos": [6, NORMAL, MELEE, NON_SKILL],
    "mardroeme": [0, SPECIAL, SPECIAL_FIELD, WAKE_UP_MARDREM],
    "olaf": [12, NORMAL, MELEE_RANGED, PLUS_ONE],
    "svanrige": [4, NORMAL, MELEE, NON_SKILL],
    "war-longship": [6, NORMAL, SIEGE, DOUBLING],
    "young-berserker": [2, NORMAL, RANGED, MARDREM],
    "young-vildkaarl": [8, NORMAL, RANGED, DOUBLING],
    "barclay-els": [6, NORMAL, MELEE_RANGED, NON_SKILL],
    "ciaran-aep-easnillien": [3, NORMAL, MELEE_RANGED, NON_SKILL],
    "dennis-cranmer": [6, NORMAL, MELEE, NON_SKILL],
    "dol-blathanna-scout-1": [6, NORMAL, MELEE_RANGED, NON_SKILL],
    "eithne": [10, GOLDEN, RANGED, NON_SKILL],
    "havcaaren-support-2": [5, NORMAL, MELEE, SUMMONING],
    "isengrim-faoiltiarna": [10, GOLDEN, MELEE, PLUS_ONE],
    "mahakaman-defenders-1": [5, NORMAL, MELEE, NON_SKILL],
    "milva": [10, NORMAL, RANGED, PLUS_ONE],
    "riordain": [1, NORMAL, RANGED, NON_SKILL],
    "saesenthessis": [10, GOLDEN, RANGED, NON_SKILL],
    "vrihedd-brigade-1": [5, NORMAL, MELEE_RANGED, NON_SKILL],
    "vrihedd-brigade-recruit": [4, NORMAL, RANGED, NON_SKILL],
}
