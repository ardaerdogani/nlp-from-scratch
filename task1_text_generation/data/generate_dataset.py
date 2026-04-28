import random
import os

TOPICS = {
    "nature": {
        "subjects": [
            "the ancient forest", "the flowing river", "the tall mountain",
            "the deep ocean", "the green valley", "the wide desert",
            "the frozen tundra", "the tropical jungle", "the quiet lake",
            "the rolling hills", "the coral reef", "the dark cave",
            "the open meadow", "the rocky cliff", "the sandy beach"
        ],
        "verbs": [
            "stretches", "flows", "rises", "spreads", "grows",
            "blooms", "changes", "remains", "appears", "thrives"
        ],
        "adjectives": [
            "beautiful", "vast", "ancient", "mysterious", "peaceful",
            "wild", "colorful", "dense", "remote", "pristine",
            "majestic", "serene", "lush", "rugged", "tranquil"
        ],
        "objects": [
            "trees", "flowers", "animals", "birds", "rivers",
            "mountains", "clouds", "stones", "leaves", "roots",
            "branches", "streams", "paths", "meadows", "shadows"
        ],
        "adverbs": [
            "silently", "gracefully", "slowly", "endlessly", "gently",
            "naturally", "freely", "quietly", "steadily", "beautifully"
        ]
    },
    "science": {
        "subjects": [
            "the researcher", "the experiment", "the theory",
            "the discovery", "the laboratory", "the scientist",
            "the observation", "the hypothesis", "the evidence",
            "the analysis", "the method", "the formula",
            "the equation", "the measurement", "the result"
        ],
        "verbs": [
            "reveals", "demonstrates", "confirms", "suggests", "proves",
            "explains", "predicts", "measures", "analyzes", "discovers"
        ],
        "adjectives": [
            "complex", "fundamental", "critical", "innovative", "precise",
            "theoretical", "empirical", "systematic", "rigorous", "novel",
            "remarkable", "significant", "groundbreaking", "logical", "measurable"
        ],
        "objects": [
            "particles", "molecules", "cells", "atoms", "elements",
            "compounds", "forces", "waves", "fields", "reactions",
            "structures", "patterns", "systems", "processes", "phenomena"
        ],
        "adverbs": [
            "carefully", "precisely", "systematically", "thoroughly", "accurately",
            "consistently", "repeatedly", "reliably", "experimentally", "theoretically"
        ]
    },
    "technology": {
        "subjects": [
            "the computer", "the network", "the software", "the algorithm",
            "the database", "the processor", "the system", "the platform",
            "the application", "the interface", "the server", "the device",
            "the program", "the framework", "the protocol"
        ],
        "verbs": [
            "processes", "transmits", "stores", "analyzes", "connects",
            "optimizes", "executes", "manages", "transforms", "enables"
        ],
        "adjectives": [
            "advanced", "digital", "efficient", "powerful", "modern",
            "automated", "intelligent", "scalable", "robust", "secure",
            "innovative", "reliable", "fast", "flexible", "distributed"
        ],
        "objects": [
            "data", "signals", "packets", "files", "records",
            "operations", "commands", "queries", "requests", "responses",
            "connections", "resources", "modules", "components", "services"
        ],
        "adverbs": [
            "efficiently", "rapidly", "automatically", "seamlessly", "securely",
            "reliably", "continuously", "instantly", "dynamically", "intelligently"
        ]
    },
    "history": {
        "subjects": [
            "the civilization", "the empire", "the kingdom", "the nation",
            "the leader", "the explorer", "the army", "the people",
            "the culture", "the dynasty", "the colony", "the republic",
            "the revolution", "the movement", "the alliance"
        ],
        "verbs": [
            "conquered", "established", "transformed", "united", "expanded",
            "influenced", "protected", "governed", "developed", "preserved"
        ],
        "adjectives": [
            "ancient", "powerful", "influential", "legendary", "historic",
            "notable", "remarkable", "prosperous", "vast", "celebrated",
            "enduring", "formidable", "distinguished", "renowned", "significant"
        ],
        "objects": [
            "territories", "traditions", "monuments", "writings", "artifacts",
            "laws", "customs", "achievements", "battles", "treaties",
            "institutions", "structures", "records", "legacies", "discoveries"
        ],
        "adverbs": [
            "gradually", "dramatically", "eventually", "significantly", "profoundly",
            "historically", "strategically", "politically", "culturally", "decisively"
        ]
    },
    "food": {
        "subjects": [
            "the chef", "the recipe", "the ingredient", "the dish",
            "the cuisine", "the flavor", "the meal", "the kitchen",
            "the restaurant", "the tradition", "the technique", "the spice",
            "the sauce", "the bread", "the harvest"
        ],
        "verbs": [
            "combines", "creates", "enhances", "transforms", "blends",
            "prepares", "serves", "tastes", "seasons", "presents"
        ],
        "adjectives": [
            "delicious", "fresh", "savory", "aromatic", "traditional",
            "exotic", "rich", "sweet", "spicy", "tender",
            "crispy", "healthy", "organic", "flavorful", "hearty"
        ],
        "objects": [
            "vegetables", "herbs", "meats", "fruits", "grains",
            "spices", "oils", "sauces", "breads", "desserts",
            "soups", "salads", "pastas", "cheeses", "wines"
        ],
        "adverbs": [
            "carefully", "skillfully", "perfectly", "delicately", "lovingly",
            "expertly", "traditionally", "creatively", "freshly", "generously"
        ]
    },
    "travel": {
        "subjects": [
            "the traveler", "the journey", "the destination", "the road",
            "the landscape", "the adventure", "the explorer", "the path",
            "the voyage", "the expedition", "the wanderer", "the guide",
            "the tourist", "the pilgrim", "the route"
        ],
        "verbs": [
            "discovers", "explores", "reaches", "crosses", "follows",
            "navigates", "visits", "wanders", "arrives", "ventures"
        ],
        "adjectives": [
            "breathtaking", "remote", "exotic", "scenic", "unforgettable",
            "charming", "vibrant", "hidden", "spectacular", "diverse",
            "ancient", "bustling", "peaceful", "picturesque", "magnificent"
        ],
        "objects": [
            "landscapes", "cities", "villages", "temples", "markets",
            "beaches", "mountains", "ruins", "gardens", "bridges",
            "harbors", "castles", "monuments", "trails", "islands"
        ],
        "adverbs": [
            "eagerly", "slowly", "boldly", "curiously", "joyfully",
            "adventurously", "peacefully", "carefully", "excitedly", "patiently"
        ]
    },
    "education": {
        "subjects": [
            "the student", "the teacher", "the school", "the university",
            "the curriculum", "the classroom", "the lecture", "the professor",
            "the learner", "the mentor", "the course", "the program",
            "the institution", "the scholar", "the study"
        ],
        "verbs": [
            "teaches", "learns", "inspires", "develops", "guides",
            "encourages", "prepares", "challenges", "supports", "advances"
        ],
        "adjectives": [
            "comprehensive", "engaging", "interactive", "foundational", "advanced",
            "practical", "theoretical", "inspiring", "structured", "progressive",
            "inclusive", "rigorous", "creative", "effective", "meaningful"
        ],
        "objects": [
            "skills", "knowledge", "concepts", "ideas", "methods",
            "principles", "subjects", "topics", "strategies", "techniques",
            "perspectives", "theories", "disciplines", "frameworks", "approaches"
        ],
        "adverbs": [
            "effectively", "actively", "collaboratively", "critically", "creatively",
            "thoughtfully", "diligently", "enthusiastically", "independently", "systematically"
        ]
    },
    "health": {
        "subjects": [
            "the doctor", "the patient", "the treatment", "the hospital",
            "the medicine", "the therapy", "the practice", "the research",
            "the body", "the mind", "the diet", "the exercise",
            "the prevention", "the recovery", "the wellness"
        ],
        "verbs": [
            "improves", "strengthens", "heals", "supports", "promotes",
            "protects", "restores", "maintains", "enhances", "prevents"
        ],
        "adjectives": [
            "healthy", "vital", "essential", "beneficial", "natural",
            "effective", "preventive", "therapeutic", "holistic", "active",
            "balanced", "nutritious", "restorative", "sustainable", "mindful"
        ],
        "objects": [
            "habits", "nutrients", "vitamins", "muscles", "organs",
            "systems", "functions", "cells", "tissues", "conditions",
            "routines", "practices", "foods", "activities", "exercises"
        ],
        "adverbs": [
            "regularly", "naturally", "consistently", "gradually", "actively",
            "mindfully", "properly", "effectively", "safely", "holistically"
        ]
    },
    "art": {
        "subjects": [
            "the artist", "the painting", "the sculpture", "the gallery",
            "the musician", "the composer", "the performance", "the exhibition",
            "the creation", "the masterpiece", "the technique", "the movement",
            "the canvas", "the melody", "the design"
        ],
        "verbs": [
            "creates", "inspires", "captures", "expresses", "reveals",
            "transforms", "celebrates", "reflects", "evokes", "portrays"
        ],
        "adjectives": [
            "creative", "expressive", "vibrant", "abstract", "classical",
            "modern", "elegant", "bold", "subtle", "profound",
            "dynamic", "harmonious", "striking", "delicate", "unique"
        ],
        "objects": [
            "colors", "shapes", "textures", "patterns", "forms",
            "sounds", "rhythms", "compositions", "perspectives", "emotions",
            "themes", "styles", "visions", "impressions", "movements"
        ],
        "adverbs": [
            "beautifully", "expressively", "boldly", "delicately", "vividly",
            "skillfully", "passionately", "gracefully", "dramatically", "subtly"
        ]
    },
    "sports": {
        "subjects": [
            "the athlete", "the team", "the coach", "the competition",
            "the champion", "the player", "the match", "the tournament",
            "the stadium", "the training", "the season", "the record",
            "the league", "the game", "the strategy"
        ],
        "verbs": [
            "competes", "trains", "wins", "performs", "achieves",
            "overcomes", "inspires", "dominates", "excels", "advances"
        ],
        "adjectives": [
            "athletic", "competitive", "skilled", "determined", "powerful",
            "swift", "dedicated", "talented", "relentless", "impressive",
            "disciplined", "strategic", "dynamic", "exceptional", "fierce"
        ],
        "objects": [
            "goals", "records", "victories", "challenges", "opponents",
            "skills", "techniques", "strategies", "achievements", "performances",
            "medals", "titles", "seasons", "events", "matches"
        ],
        "adverbs": [
            "fiercely", "skillfully", "tirelessly", "brilliantly", "powerfully",
            "strategically", "consistently", "passionately", "determinedly", "impressively"
        ]
    }
}

TEMPLATES = [
    "{subject} {verb} {adverb} among the {adjective} {object}.",
    "The {adjective} {object} and {adjective} {object} define {subject} in many ways.",
    "When {subject} {verb} the {object}, the {adjective} world takes notice.",
    "{subject} {verb} with great purpose, shaping the {adjective} {object} of our time.",
    "In the realm of {adjective} {object}, {subject} {verb} {adverb}.",
    "Every day, {subject} {verb} the {object} that make life {adjective}.",
    "Through {adjective} effort, {subject} {verb} {adverb} toward new {object}.",
    "The connection between {subject} and the {adjective} {object} {verb} {adverb}.",
    "Many believe that {subject} {verb} the very {object} we depend upon.",
    "As {subject} {verb} {adverb}, the {adjective} {object} continue to evolve.",
    "Understanding how {subject} {verb} is key to appreciating {adjective} {object}.",
    "The role of {subject} in shaping {adjective} {object} cannot be overstated.",
    "It is well known that {subject} {verb} {adverb} across all {object}.",
    "{subject} has long been associated with {adjective} {object} and lasting impact.",
    "The importance of {subject} grows as {adjective} {object} become more central.",
    "In recent years, {subject} {verb} the boundaries of {adjective} {object}.",
    "Both {subject} and the {adjective} {object} play a vital role in progress.",
    "Experts agree that {subject} {verb} {adverb}, transforming our view of {object}.",
    "The study of how {subject} {verb} reveals deep truths about {adjective} {object}.",
    "One cannot discuss {adjective} {object} without mentioning how {subject} {verb}.",
]

CONNECTORS = [
    "Furthermore, ", "In addition, ", "Moreover, ", "Similarly, ",
    "As a result, ", "Consequently, ", "Meanwhile, ", "Nevertheless, ",
    "On the other hand, ", "In contrast, ", "For example, ", "Indeed, ",
    "Significantly, ", "Notably, ", "Importantly, ", "Interestingly, ",
    "In fact, ", "Therefore, ", "However, ", "Additionally, "
]

INTRO_TEMPLATES = [
    "The world of {topic} is full of wonder and complexity.",
    "Throughout history, {topic} has played a central role in human life.",
    "Few subjects capture human imagination like {topic} does.",
    "The study of {topic} reveals fascinating patterns and insights.",
    "People have always been drawn to the mysteries of {topic}.",
    "In modern times, {topic} continues to shape our understanding of the world.",
    "The significance of {topic} extends far beyond its obvious boundaries.",
    "To truly understand our world, one must appreciate the role of {topic}.",
    "From ancient times to the present day, {topic} has evolved remarkably.",
    "The field of {topic} offers endless opportunities for learning and growth."
]

CONCLUSION_TEMPLATES = [
    "In summary, {topic} remains an essential part of human experience.",
    "The future of {topic} holds great promise and exciting possibilities.",
    "As we continue to explore {topic}, new discoveries await us at every turn.",
    "The importance of {topic} will only grow in the years to come.",
    "Understanding {topic} helps us build a better and more connected world."
]

def fill_template(template, topic_data, topic_name):
    result = template
    result = result.replace("{topic}", topic_name)
    result = result.replace("{subject}", random.choice(topic_data["subjects"]))
    result = result.replace("{verb}", random.choice(topic_data["verbs"]))
    result = result.replace("{adjective}", random.choice(topic_data["adjectives"]))
    result = result.replace("{object}", random.choice(topic_data["objects"]))
    result = result.replace("{adverb}", random.choice(topic_data["adverbs"]))
    return result

def generate_paragraph(topic_name, topic_data, num_sentences=5):
    sentences = []
    for i in range(num_sentences):
        template = random.choice(TEMPLATES)
        sentence = fill_template(template, topic_data, topic_name)
        if i > 0 and random.random() < 0.3:
            sentence = random.choice(CONNECTORS) + sentence[0].lower() + sentence[1:]
        sentences.append(sentence)
    return " ".join(sentences)

def generate_section(topic_name, topic_data, num_paragraphs=4):
    paragraphs = []
    intro = fill_template(random.choice(INTRO_TEMPLATES), topic_data, topic_name)
    paragraphs.append(intro)

    for _ in range(num_paragraphs):
        num_sentences = random.randint(4, 7)
        paragraph = generate_paragraph(topic_name, topic_data, num_sentences)
        paragraphs.append(paragraph)

    conclusion = fill_template(random.choice(CONCLUSION_TEMPLATES), topic_data, topic_name)
    paragraphs.append(conclusion)

    return "\n\n".join(paragraphs)

def generate_corpus(target_words=12000, seed=42):
    random.seed(seed)
    sections = []
    word_count = 0
    topic_names = list(TOPICS.keys())

    while word_count < target_words:
        topic_name = random.choice(topic_names)
        topic_data = TOPICS[topic_name]
        num_paragraphs = random.randint(3, 6)
        section = generate_section(topic_name, topic_data, num_paragraphs)
        sections.append(section)
        word_count += len(section.split())

    corpus = "\n\n---\n\n".join(sections)
    return corpus

def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "corpus.txt")

    corpus = generate_corpus(target_words=12000)
    word_count = len(corpus.split())

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(corpus)

    print(f"Generated corpus with {word_count} words")
    print(f"Character count: {len(corpus)}")
    print(f"Saved to: {output_path}")
    return corpus

if __name__ == "__main__":
    main()
