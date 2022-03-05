import os

from flask import Flask


class CONFIG:
    MINIMUM_NAME_LENGTH = 3
    MAXIMUM_NAME_LENGTH = 128
    SUBREDDITS = [
        "battlemaps",
        "dndmaps",
        "dungeondraft",
        "fantasymaps",
        "miskasmaps",
        "roll20",
        "FoundryVTT"
    ]
    IMAGE_EXTENSIONS = ["png", "jpg"]
    MINIMUM_IMAGE_SIZE_IN_BYTES = 5000
    MAXIMUM_IMAGE_SIZE_IN_BYTES = 20485760
    STATIC_DIRECTORY = "static"
    REST_DIRECTORY = "maps"
    UPLOAD_DIRECTORY = STATIC_DIRECTORY + "/images"
    MINIMUM_IMAGE_DIMENSION = 100
    THUMBNAIL_SIZE = 512
    THUMBNAIL_DIRECTORY = UPLOAD_DIRECTORY + "/thumbnails"
    MAPS_PER_PAGE = 100
    STOP_WORDS = ["able", "about", "above", "abroad", "according", "accordingly", "across", "actually", "adj", "after",
                  "afterwards", "again", "against", "ago", "ahead", "aint", "all", "allow", "allows", "almost", "alone",
                  "along", "alongside", "already", "also", "although", "always", "am", "amid", "amidst", "among",
                  "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway",
                  "anyways", "anywhere", "apart", "appear", "appreciate", "appropriate", "are", "arent", "around", "as",
                  "aside", "ask", "asking", "associated", "at", "available", "away", "awfully", "back", "backward",
                  "backwards", "be", "became", "because", "become", "becomes", "becoming", "been", "before",
                  "beforehand", "begin", "behind", "being", "believe", "below", "beside", "besides", "best", "better",
                  "between", "beyond", "both", "brief", "but", "by", "came", "can", "cannot", "cant", "cant", "caption",
                  "cause", "causes", "certain", "certainly", "changes", "clearly", "cmon", "co", "com", "come", "comes",
                  "concerning", "consequently", "consider", "considering", "contain", "containing", "contains",
                  "corresponding", "could", "couldnt", "course", "cs", "currently", "dare", "darent", "definitely",
                  "described", "despite", "did", "didnt", "different", "directly", "do", "does", "doesnt", "doing",
                  "done", "dont", "down", "downwards", "during", "each", "edu", "eg", "eight", "eighty", "either",
                  "else", "elsewhere", "end", "ending", "enough", "entirely", "especially", "et", "etc", "even", "ever",
                  "evermore", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example",
                  "except", "fairly", "far", "farther", "few", "fewer", "fifth", "first", "five", "followed",
                  "following", "follows", "for", "forever", "former", "formerly", "forth", "forward", "found", "four",
                  "from", "further", "furthermore", "get", "gets", "getting", "given", "gives", "go", "goes", "going",
                  "gone", "got", "gotten", "greetings", "had", "hadnt", "half", "happens", "hardly", "has", "hasnt",
                  "have", "havent", "having", "he", "hed", "hell", "hello", "help", "hence", "her", "here", "hereafter",
                  "hereby", "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "him", "himself", "his",
                  "hither", "hopefully", "how", "howbeit", "however", "hundred", "id", "ie", "if", "ignored", "ill",
                  "im", "immediate", "in", "inasmuch", "inc", "inc", "indeed", "indicate", "indicated", "indicates",
                  "inner", "inside", "insofar", "instead", "into", "inward", "is", "isnt", "it", "itd", "itll", "its",
                  "its", "itself", "ive", "just", "k", "keep", "keeps", "kept", "know", "known", "knows", "last",
                  "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked",
                  "likely", "likewise", "little", "look", "looking", "looks", "low", "lower", "ltd", "made", "mainly",
                  "make", "makes", "many", "may", "maybe", "maynt", "me", "mean", "meantime", "meanwhile", "merely",
                  "might", "mightnt", "mine", "minus", "miss", "more", "moreover", "most", "mostly", "mr", "mrs",
                  "much", "must", "mustnt", "my", "myself", "name", "namely", "nd", "near", "nearly", "necessary",
                  "need", "neednt", "needs", "neither", "never", "neverf", "neverless", "nevertheless", "new", "next",
                  "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "no-one", "nor", "normally",
                  "not", "nothing", "notwithstanding", "novel", "now", "nowhere", "obviously", "of", "off", "often",
                  "oh", "ok", "okay", "old", "on", "once", "one", "ones", "ones", "only", "onto", "opposite", "or",
                  "other", "others", "otherwise", "ought", "oughtnt", "our", "ours", "ourselves", "out", "outside",
                  "over", "overall", "own", "particular", "particularly", "past", "per", "perhaps", "placed", "please",
                  "plus", "possible", "presumably", "probably", "provided", "provides", "que", "quite", "qv", "rather",
                  "rd", "re", "really", "reasonably", "recent", "recently", "regarding", "regardless", "regards",
                  "relatively", "respectively", "right", "round", "said", "same", "saw", "say", "saying", "says",
                  "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves",
                  "sensible", "sent", "serious", "seriously", "seven", "several", "shall", "shant", "she", "shed",
                  "shell", "shes", "should", "shouldnt", "since", "six", "so", "some", "somebody", "someday", "somehow",
                  "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry",
                  "specified", "specify", "specifying", "still", "sub", "such", "sup", "sure", "take", "taken",
                  "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "thatll", "thats",
                  "thats", "thatve", "the", "their", "theirs", "them", "themselves", "then", "thence", "there",
                  "thereafter", "thereby", "thered", "therefore", "therein", "therell", "therere", "theres", "theres",
                  "thereupon", "thereve", "these", "they", "theyd", "theyll", "theyre", "theyve", "thing", "things",
                  "think", "third", "thirty", "this", "thorough", "thoroughly", "those", "though", "three", "through",
                  "throughout", "thru", "thus", "till", "to", "together", "too", "took", "toward", "towards", "tried",
                  "tries", "truly", "try", "trying", "ts", "twice", "two", "un", "under", "underneath", "undoing",
                  "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "upwards", "us",
                  "use", "used", "useful", "uses", "using", "usually", "v", "value", "various", "versus", "very", "via",
                  "viz", "vs", "want", "wants", "was", "wasnt", "way", "we", "wed", "welcome", "well", "well", "went",
                  "were", "were", "werent", "weve", "what", "whatever", "whatll", "whats", "whatve", "when", "whence",
                  "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever",
                  "whether", "which", "whichever", "while", "whilst", "whither", "who", "whod", "whoever", "whole",
                  "wholl", "whom", "whomever", "whos", "whose", "why", "will", "willing", "wish", "with", "within",
                  "without", "wonder", "wont", "would", "wouldnt", "yes", "yet", "you", "youd", "youll", "your",
                  "youre", "yours", "yourself", "yourselves", "youve", "zero", "a", "hows", "i", "whens", "whys", "b",
                  "c", "d", "e", "f", "g", "h", "j", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "uucp", "w", "x",
                  "y", "z", "I", "www", "amount", "bill", "bottom", "call", "computer", "con", "couldnt", "cry", "de",
                  "describe", "detail", "due", "eleven", "empty", "fifteen", "fifty", "fill", "find", "fire", "forty",
                  "front", "full", "give", "hasnt", "herse", "himse", "interest", "itse", "mill", "move", "myse",
                  "part", "put", "show", "side", "sincere", "sixty", "system", "ten", "thick", "thin", "top", "twelve",
                  "twenty", "abst", "accordance", "act", "added", "adopted", "affected", "affecting", "affects", "ah",
                  "announce", "anymore", "apparently", "approximately", "aren", "arent", "arise", "auth", "beginning",
                  "beginnings", "begins", "biol", "briefly", "ca", "date", "ed", "effect", "et-al", "ff", "fix", "gave",
                  "giving", "heres", "hes", "hid", "home", "id", "im", "immediately", "importance", "important",
                  "index", "information", "invention", "itd", "keys", "kg", "km", "largely", "lets", "line", "ll",
                  "means", "mg", "million", "ml", "mug", "na", "nay", "necessarily", "nos", "noted", "obtain",
                  "obtained", "omitted", "ord", "owing", "page", "pages", "poorly", "possibly", "potentially", "pp",
                  "predominantly", "present", "previously", "primarily", "promptly", "proud", "quickly", "ran",
                  "readily", "ref", "refs", "related", "research", "resulted", "resulting", "results", "run", "sec",
                  "section", "shed", "shes", "showed", "shown", "showns", "shows", "significant", "significantly",
                  "similar", "similarly", "slightly", "somethan", "specifically", "state", "states", "stop", "strongly",
                  "substantially", "successfully", "sufficiently", "suggest", "thered", "thereof", "therere", "thereto",
                  "theyd", "theyre", "thou", "thoughh", "thousand", "throug", "til", "tip", "ts", "ups", "usefully",
                  "usefulness", "ve", "vol", "vols", "wed", "whats", "wheres", "whim", "whod", "whos", "widely",
                  "words", "world", "youd", "youre", "map", "battlemap", "free", "battle", "art", "amp", "maps",
                  "small", "comments", "grid", "assets", "level", "version", "hand", "floor", "room", "pack", "rpg",
                  "drawn", "storey", "high", "inspired", "original", "battlemaps", "fight", "vtt", "set", "modular",
                  "adventure", "magic", "time", "grand", "sin", "divinity", "rest", "square", "tiles", "collaboration",
                  "joy", "encounter", "lost", "fall", "big", "hidden", "printable", "link", "making", "attempt",
                  "secret"]


app = Flask(__name__, static_url_path="/" + CONFIG.STATIC_DIRECTORY, static_folder=CONFIG.STATIC_DIRECTORY)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.getenv("USERNAME")}:{os.getenv("PASSWORD")}@{os.getenv("IP")}/flask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
