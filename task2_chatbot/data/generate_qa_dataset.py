import json
import random
import os

GEOGRAPHY_QA = [
    ("What is the capital of France?", "The capital of France is Paris."),
    ("What is the capital of Germany?", "The capital of Germany is Berlin."),
    ("What is the capital of Japan?", "The capital of Japan is Tokyo."),
    ("What is the capital of Italy?", "The capital of Italy is Rome."),
    ("What is the capital of Spain?", "The capital of Spain is Madrid."),
    ("What is the capital of Brazil?", "The capital of Brazil is Brasilia."),
    ("What is the capital of Australia?", "The capital of Australia is Canberra."),
    ("What is the capital of Canada?", "The capital of Canada is Ottawa."),
    ("What is the capital of Egypt?", "The capital of Egypt is Cairo."),
    ("What is the capital of India?", "The capital of India is New Delhi."),
    ("What is the capital of China?", "The capital of China is Beijing."),
    ("What is the capital of Russia?", "The capital of Russia is Moscow."),
    ("What is the capital of Mexico?", "The capital of Mexico is Mexico City."),
    ("What is the capital of Turkey?", "The capital of Turkey is Ankara."),
    ("What is the capital of Argentina?", "The capital of Argentina is Buenos Aires."),
    ("What is the largest continent?", "Asia is the largest continent by both area and population."),
    ("What is the smallest continent?", "Australia is the smallest continent."),
    ("What is the longest river in the world?", "The Nile is the longest river in the world."),
    ("What is the largest ocean?", "The Pacific Ocean is the largest ocean on Earth."),
    ("What is the tallest mountain?", "Mount Everest is the tallest mountain in the world."),
    ("What is the largest desert?", "The Sahara is the largest hot desert in the world."),
    ("What is the deepest ocean?", "The Pacific Ocean is the deepest ocean."),
    ("Where is the Amazon rainforest?", "The Amazon rainforest is located in South America."),
    ("Where is the Great Wall?", "The Great Wall is located in China."),
    ("Where are the pyramids?", "The most famous pyramids are located in Egypt."),
    ("How many continents are there?", "There are seven continents on Earth."),
    ("How many oceans are there?", "There are five oceans on Earth."),
    ("What separates Europe and Asia?", "The Ural Mountains separate Europe and Asia."),
    ("What is the largest country by area?", "Russia is the largest country by area."),
    ("What is the smallest country?", "Vatican City is the smallest country in the world."),
]

SCIENCE_QA = [
    ("What is the speed of light?", "The speed of light is approximately 300,000 kilometers per second."),
    ("What is gravity?", "Gravity is a force that attracts objects with mass toward each other."),
    ("What is photosynthesis?", "Photosynthesis is the process by which plants convert sunlight into energy."),
    ("What is DNA?", "DNA is a molecule that carries genetic instructions for living organisms."),
    ("What is an atom?", "An atom is the smallest unit of ordinary matter that forms a chemical element."),
    ("What is the periodic table?", "The periodic table organizes chemical elements by atomic number and properties."),
    ("What is evolution?", "Evolution is the process of change in living organisms over generations."),
    ("What causes earthquakes?", "Earthquakes are caused by the movement of tectonic plates beneath the Earth."),
    ("What is the water cycle?", "The water cycle describes the continuous movement of water through evaporation, condensation, and precipitation."),
    ("How does the heart work?", "The heart pumps blood through the body by contracting and relaxing its chambers."),
    ("What is a cell?", "A cell is the basic structural and functional unit of all living organisms."),
    ("What is temperature?", "Temperature is a measure of the average kinetic energy of particles in a substance."),
    ("What is energy?", "Energy is the capacity to do work or cause change in a physical system."),
    ("What is a molecule?", "A molecule is a group of two or more atoms bonded together chemically."),
    ("What is electricity?", "Electricity is the flow of electric charge through a conductor."),
    ("What is magnetism?", "Magnetism is a physical force produced by moving electric charges."),
    ("What is sound?", "Sound is a vibration that travels through a medium as a wave."),
    ("What is light?", "Light is electromagnetic radiation that is visible to the human eye."),
    ("What causes rain?", "Rain is caused by water vapor condensing in clouds and falling as droplets."),
    ("What is the atmosphere?", "The atmosphere is the layer of gases surrounding Earth."),
    ("What is a black hole?", "A black hole is a region in space where gravity is so strong that nothing can escape."),
    ("What is a star?", "A star is a luminous sphere of plasma held together by its own gravity."),
    ("What is the solar system?", "The solar system consists of the Sun and all objects that orbit around it."),
    ("How many planets are in the solar system?", "There are eight planets in our solar system."),
    ("What is oxygen?", "Oxygen is a chemical element essential for respiration in most living organisms."),
    ("What is carbon dioxide?", "Carbon dioxide is a gas produced by respiration and combustion."),
    ("What is a volcano?", "A volcano is an opening in the Earth where molten rock and gases escape."),
    ("What is a tsunami?", "A tsunami is a series of large ocean waves caused by underwater disturbances."),
    ("What is a fossil?", "A fossil is the preserved remains or traces of ancient organisms."),
    ("What is the moon?", "The Moon is Earth's only natural satellite."),
]

MATH_QA = [
    ("What is addition?", "Addition is the mathematical operation of combining two or more numbers to get a sum."),
    ("What is subtraction?", "Subtraction is the operation of finding the difference between two numbers."),
    ("What is multiplication?", "Multiplication is repeated addition of a number a specified number of times."),
    ("What is division?", "Division is the operation of splitting a number into equal parts."),
    ("What is a fraction?", "A fraction represents a part of a whole, written as one number over another."),
    ("What is a percentage?", "A percentage is a number expressed as a fraction of one hundred."),
    ("What is an equation?", "An equation is a mathematical statement that two expressions are equal."),
    ("What is geometry?", "Geometry is the branch of mathematics dealing with shapes and spatial relationships."),
    ("What is algebra?", "Algebra is a branch of mathematics that uses symbols to represent numbers and quantities."),
    ("What is a prime number?", "A prime number is a number greater than one that has no divisors other than one and itself."),
    ("What is pi?", "Pi is a mathematical constant approximately equal to 3.14159."),
    ("What is the Pythagorean theorem?", "The Pythagorean theorem states that in a right triangle, the square of the hypotenuse equals the sum of the squares of the other two sides."),
    ("What is a square root?", "A square root of a number is a value that, when multiplied by itself, gives the original number."),
    ("What is an angle?", "An angle is the figure formed by two rays sharing a common endpoint."),
    ("What is a triangle?", "A triangle is a polygon with three sides and three angles."),
    ("What is a circle?", "A circle is a shape where all points are equidistant from a center point."),
    ("What is area?", "Area is the measure of the surface enclosed within a boundary."),
    ("What is volume?", "Volume is the measure of space occupied by a three-dimensional object."),
    ("What is probability?", "Probability is the measure of how likely an event is to occur."),
    ("What is statistics?", "Statistics is the science of collecting, analyzing, and interpreting numerical data."),
    ("What is a function?", "A function is a relation that assigns exactly one output to each input."),
    ("What is infinity?", "Infinity is a concept describing something without any limit or end."),
    ("What is zero?", "Zero is the integer between negative one and positive one, representing nothing."),
    ("What is a decimal?", "A decimal is a way of writing fractions using the base ten number system."),
    ("What is calculus?", "Calculus is a branch of mathematics that studies continuous change."),
]

TECHNOLOGY_QA = [
    ("What is a computer?", "A computer is an electronic device that processes data according to instructions."),
    ("What is the internet?", "The internet is a global network of interconnected computers and servers."),
    ("What is software?", "Software is a set of instructions that tells a computer what to do."),
    ("What is hardware?", "Hardware refers to the physical components of a computer system."),
    ("What is an algorithm?", "An algorithm is a step-by-step procedure for solving a problem."),
    ("What is a database?", "A database is an organized collection of structured data stored electronically."),
    ("What is programming?", "Programming is the process of writing instructions for computers to follow."),
    ("What is artificial intelligence?", "Artificial intelligence is the simulation of human intelligence by computer systems."),
    ("What is machine learning?", "Machine learning is a subset of AI where systems learn from data without explicit programming."),
    ("What is a network?", "A network is a group of interconnected computers that can share resources."),
    ("What is cybersecurity?", "Cybersecurity is the practice of protecting systems and data from digital attacks."),
    ("What is cloud computing?", "Cloud computing delivers computing services over the internet on demand."),
    ("What is a server?", "A server is a computer that provides data and services to other computers."),
    ("What is an operating system?", "An operating system is software that manages computer hardware and other software."),
    ("What is a browser?", "A web browser is software used to access and view websites on the internet."),
    ("What is encryption?", "Encryption is the process of converting data into a coded form for security."),
    ("What is bandwidth?", "Bandwidth is the maximum rate of data transfer across a network."),
    ("What is a pixel?", "A pixel is the smallest unit of a digital image or display."),
    ("What is RAM?", "RAM is temporary memory that a computer uses to store data it is currently processing."),
    ("What is a CPU?", "A CPU is the central processing unit that executes instructions in a computer."),
    ("What is binary code?", "Binary code uses only zeros and ones to represent data in computers."),
    ("What is a firewall?", "A firewall is a security system that monitors and controls network traffic."),
    ("What is a virus in computing?", "A computer virus is malicious software that replicates itself and spreads to other systems."),
    ("What is virtual reality?", "Virtual reality is a simulated experience created by computer technology."),
    ("What is robotics?", "Robotics is the field of designing, building, and operating robots."),
]

HISTORY_QA = [
    ("When did World War II end?", "World War II ended in 1945."),
    ("Who was the first president of the United States?", "George Washington was the first president of the United States."),
    ("What was the Renaissance?", "The Renaissance was a cultural movement in Europe from the 14th to the 17th century."),
    ("When was the printing press invented?", "The printing press was invented by Johannes Gutenberg around 1440."),
    ("What was the Industrial Revolution?", "The Industrial Revolution was a period of major industrialization from the 18th to 19th century."),
    ("When did humans first land on the moon?", "Humans first landed on the moon on July 20, 1969."),
    ("What was the Roman Empire?", "The Roman Empire was a powerful civilization centered in Rome that lasted for centuries."),
    ("Who discovered America?", "Christopher Columbus reached the Americas in 1492, though indigenous peoples lived there long before."),
    ("What was the French Revolution?", "The French Revolution was a period of radical change in France beginning in 1789."),
    ("When was the telephone invented?", "Alexander Graham Bell invented the telephone in 1876."),
    ("What was ancient Egypt known for?", "Ancient Egypt was known for its pyramids, pharaohs, and advanced civilization."),
    ("When did World War I begin?", "World War I began in 1914."),
    ("What was the Cold War?", "The Cold War was a period of geopolitical tension between the United States and the Soviet Union."),
    ("Who built the Great Wall of China?", "The Great Wall of China was built over centuries by multiple Chinese dynasties."),
    ("What was the Age of Exploration?", "The Age of Exploration was a period when European nations explored the world by sea."),
    ("When was electricity discovered?", "The understanding of electricity developed over centuries, with key experiments in the 18th century."),
    ("What was the Silk Road?", "The Silk Road was an ancient network of trade routes connecting East Asia to the Mediterranean."),
    ("Who was Leonardo da Vinci?", "Leonardo da Vinci was an Italian polymath known for art, science, and invention."),
    ("What was the ancient Greek civilization?", "Ancient Greece was a civilization known for its philosophy, democracy, and cultural achievements."),
    ("When was the internet created?", "The internet originated from ARPANET in the late 1960s and became publicly accessible in the 1990s."),
]

GENERAL_QA = [
    ("What is language?", "Language is a system of communication using words, sounds, or symbols."),
    ("What is music?", "Music is the art of organizing sounds in time to create melody, harmony, and rhythm."),
    ("What is art?", "Art is the expression of human creativity and imagination through various forms."),
    ("What is democracy?", "Democracy is a system of government where citizens participate in decision-making."),
    ("What is philosophy?", "Philosophy is the study of fundamental questions about existence, knowledge, and ethics."),
    ("What is culture?", "Culture refers to the shared beliefs, customs, and practices of a group of people."),
    ("What is education?", "Education is the process of acquiring knowledge and skills through learning."),
    ("What is economics?", "Economics is the study of how societies allocate scarce resources."),
    ("What is psychology?", "Psychology is the scientific study of the mind and behavior."),
    ("What is literature?", "Literature refers to written works regarded as having artistic merit."),
    ("What is a ecosystem?", "An ecosystem is a community of living organisms interacting with their environment."),
    ("What is climate change?", "Climate change refers to long-term shifts in global temperatures and weather patterns."),
    ("What is renewable energy?", "Renewable energy comes from sources that naturally replenish, like solar and wind power."),
    ("What is biodiversity?", "Biodiversity is the variety of life forms in a particular habitat or on Earth as a whole."),
    ("What is recycling?", "Recycling is the process of converting waste materials into reusable materials."),
    ("What is communication?", "Communication is the exchange of information between individuals or groups."),
    ("What is a vaccine?", "A vaccine is a biological preparation that provides immunity against a specific disease."),
    ("What is nutrition?", "Nutrition is the process of obtaining food necessary for health and growth."),
    ("What is exercise?", "Exercise is physical activity performed to improve health and fitness."),
    ("What is sleep?", "Sleep is a natural state of rest where the body and mind recover and recharge."),
]

TEMPLATE_QUESTIONS = {
    "what_is": [
        ("What is {concept}?", "{concept} is {definition}."),
    ],
    "how_does": [
        ("How does {concept} work?", "{concept} works by {explanation}."),
    ],
    "why_is": [
        ("Why is {concept} important?", "{concept} is important because {reason}."),
    ],
    "difference": [
        ("What is the difference between {a} and {b}?", "{a} is {def_a}, while {b} is {def_b}."),
    ],
    "can_you": [
        ("Can you explain {concept}?", "Certainly. {concept} refers to {definition}."),
    ],
    "tell_me": [
        ("Tell me about {concept}.", "{concept} is {definition}. It plays an important role in many areas."),
    ],
}

CONCEPTS = {
    "photosynthesis": {
        "definition": "the process by which plants use sunlight to produce food",
        "explanation": "converting sunlight, water, and carbon dioxide into glucose and oxygen",
        "reason": "it produces oxygen and food for plants and other organisms"
    },
    "gravity": {
        "definition": "a fundamental force that attracts objects with mass toward each other",
        "explanation": "creating an attractive force proportional to the masses involved",
        "reason": "it keeps planets in orbit and holds us on the surface of Earth"
    },
    "evolution": {
        "definition": "the gradual change in species over generations through natural selection",
        "explanation": "selecting traits that improve survival and reproduction over time",
        "reason": "it explains the diversity of life on Earth"
    },
    "democracy": {
        "definition": "a form of government where power rests with the people",
        "explanation": "allowing citizens to vote and participate in decision-making",
        "reason": "it gives people a voice in how they are governed"
    },
    "electricity": {
        "definition": "the flow of electric charge through conductors",
        "explanation": "moving electrons through a circuit to transfer energy",
        "reason": "it powers most modern technology and infrastructure"
    },
    "the water cycle": {
        "definition": "the continuous movement of water through the environment",
        "explanation": "cycling water through evaporation, condensation, and precipitation",
        "reason": "it distributes fresh water across the planet"
    },
    "metabolism": {
        "definition": "the set of chemical reactions that sustain life in organisms",
        "explanation": "breaking down nutrients to produce energy and building materials",
        "reason": "it provides the energy needed for all bodily functions"
    },
    "ecosystems": {
        "definition": "communities of living organisms interacting with their physical environment",
        "explanation": "maintaining a balance of energy flow and nutrient cycling among species",
        "reason": "they sustain biodiversity and provide essential services to life on Earth"
    },
    "magnetism": {
        "definition": "a physical force created by moving electric charges",
        "explanation": "generating fields that attract or repel certain materials",
        "reason": "it is used in motors, generators, and many electronic devices"
    },
    "climate": {
        "definition": "the long-term pattern of weather conditions in a region",
        "explanation": "averaging temperature, precipitation, and wind over many years",
        "reason": "it determines what ecosystems and agriculture can exist in an area"
    },
    "the immune system": {
        "definition": "the body's defense mechanism against infections and diseases",
        "explanation": "detecting and destroying harmful pathogens using specialized cells",
        "reason": "it protects the body from illness and helps recovery"
    },
    "plate tectonics": {
        "definition": "the theory that Earth's outer shell is divided into moving plates",
        "explanation": "slowly moving large sections of the crust and upper mantle",
        "reason": "it explains earthquakes, volcanic eruptions, and mountain formation"
    },
    "respiration": {
        "definition": "the process of breathing and cellular energy production",
        "explanation": "taking in oxygen and releasing carbon dioxide while producing energy",
        "reason": "it provides the energy cells need to function"
    },
    "the nervous system": {
        "definition": "a network of nerves and cells that transmit signals throughout the body",
        "explanation": "sending electrical impulses between the brain, spinal cord, and body",
        "reason": "it coordinates all voluntary and involuntary actions"
    },
    "erosion": {
        "definition": "the wearing away of land surfaces by natural forces",
        "explanation": "gradually removing rock and soil through wind, water, and ice",
        "reason": "it shapes landscapes and affects land use over time"
    },
    "condensation": {
        "definition": "the process of water vapor turning into liquid water",
        "explanation": "cooling water vapor until it forms droplets on surfaces or in the air",
        "reason": "it is a key step in cloud formation and the water cycle"
    },
    "friction": {
        "definition": "a force that opposes the sliding motion of two surfaces in contact",
        "explanation": "creating resistance between surfaces as they move against each other",
        "reason": "it allows us to walk, drive, and hold objects without slipping"
    },
    "combustion": {
        "definition": "a chemical reaction that produces heat and light from fuel and oxygen",
        "explanation": "rapidly combining a substance with oxygen to release energy",
        "reason": "it powers engines, heats homes, and provides energy"
    },
    "diffusion": {
        "definition": "the movement of particles from high concentration to low concentration",
        "explanation": "allowing particles to spread out evenly through random motion",
        "reason": "it is essential for gas exchange in lungs and nutrient transport in cells"
    },
    "symbiosis": {
        "definition": "a close biological relationship between two different species",
        "explanation": "allowing two organisms to live together in a mutually beneficial way",
        "reason": "it demonstrates how species cooperate and depend on each other"
    },
}

COMPARISONS = [
    {"a": "a plant cell", "b": "an animal cell", "def_a": "has a cell wall and chloroplasts", "def_b": "lacks a cell wall but has centrioles"},
    {"a": "weather", "b": "climate", "def_a": "the short-term atmospheric conditions in an area", "def_b": "the long-term average of weather patterns"},
    {"a": "speed", "b": "velocity", "def_a": "how fast something moves regardless of direction", "def_b": "speed with a specified direction"},
    {"a": "mass", "b": "weight", "def_a": "the amount of matter in an object", "def_b": "the force of gravity acting on that mass"},
    {"a": "an element", "b": "a compound", "def_a": "a pure substance made of one type of atom", "def_b": "a substance made of two or more elements chemically bonded"},
    {"a": "a conductor", "b": "an insulator", "def_a": "a material that allows electricity to flow easily", "def_b": "a material that resists the flow of electricity"},
    {"a": "a solid", "b": "a liquid", "def_a": "matter with a fixed shape and volume", "def_b": "matter with a fixed volume but variable shape"},
    {"a": "mitosis", "b": "meiosis", "def_a": "cell division producing two identical cells", "def_b": "cell division producing four genetically different cells"},
    {"a": "an acid", "b": "a base", "def_a": "a substance with a pH below 7 that donates protons", "def_b": "a substance with a pH above 7 that accepts protons"},
    {"a": "renewable energy", "b": "nonrenewable energy", "def_a": "energy from sources that replenish naturally like solar and wind", "def_b": "energy from finite sources like fossil fuels"},
    {"a": "a hypothesis", "b": "a theory", "def_a": "a testable prediction about how something works", "def_b": "a well-supported explanation based on extensive evidence"},
    {"a": "hardware", "b": "software", "def_a": "the physical components of a computer", "def_b": "the programs and instructions that run on hardware"},
    {"a": "the ocean", "b": "a lake", "def_a": "a vast body of saltwater covering much of Earth", "def_b": "a smaller body of freshwater surrounded by land"},
    {"a": "a planet", "b": "a star", "def_a": "a celestial body that orbits a star", "def_b": "a luminous sphere of plasma that produces energy through fusion"},
    {"a": "a river", "b": "a stream", "def_a": "a large natural flow of water to the sea", "def_b": "a smaller natural flow of water"},
]

def generate_templated_qa(concepts, comparisons):
    pairs = []

    for concept_name, concept_data in concepts.items():
        for template_type, templates in TEMPLATE_QUESTIONS.items():
            for q_template, a_template in templates:
                if template_type == "difference":
                    continue
                q = q_template.replace("{concept}", concept_name)
                if template_type == "what_is" or template_type == "can_you" or template_type == "tell_me":
                    a = a_template.replace("{concept}", concept_name).replace("{definition}", concept_data["definition"])
                elif template_type == "how_does":
                    a = a_template.replace("{concept}", concept_name).replace("{explanation}", concept_data["explanation"])
                elif template_type == "why_is":
                    a = a_template.replace("{concept}", concept_name).replace("{reason}", concept_data["reason"])
                else:
                    continue
                pairs.append((q, a))

    for comp in comparisons:
        for q_template, a_template in TEMPLATE_QUESTIONS["difference"]:
            q = q_template.replace("{a}", comp["a"]).replace("{b}", comp["b"])
            a = a_template.replace("{a}", comp["a"]).replace("{b}", comp["b"])
            a = a.replace("{def_a}", comp["def_a"]).replace("{def_b}", comp["def_b"])
            pairs.append((q, a))

    return pairs

CONVERSATIONAL_QA = [
    ("Hello!", "Hello! How can I help you today?"),
    ("Hi there.", "Hi! What would you like to know?"),
    ("Good morning.", "Good morning! What can I help you with?"),
    ("How are you?", "I am doing well, thank you for asking. How can I assist you?"),
    ("What can you do?", "I can answer questions about science, math, history, technology, and more."),
    ("Thank you.", "You are welcome! Let me know if you have more questions."),
    ("Goodbye.", "Goodbye! Have a great day!"),
    ("Can you help me?", "Of course! Please tell me what you need help with."),
    ("What are you?", "I am a chatbot designed to answer your questions."),
    ("Who made you?", "I was created as part of a natural language processing project."),
    ("What is your name?", "I am a question-answering chatbot. You can call me Bot."),
    ("Are you smart?", "I try my best to provide helpful and accurate answers."),
    ("Do you learn?", "I learn from the data I was trained on to answer your questions."),
    ("What topics do you know?", "I know about science, math, history, geography, technology, and general knowledge."),
    ("Can you tell me a fact?", "Sure! The speed of light is approximately 300,000 kilometers per second."),
    ("What is your purpose?", "My purpose is to answer questions and provide helpful information."),
    ("How do you work?", "I process your questions and generate answers based on patterns I learned during training."),
    ("Are you a human?", "No, I am a computer program designed to answer questions."),
    ("Do you have feelings?", "I do not have feelings, but I am designed to be helpful and friendly."),
    ("What language do you speak?", "I communicate in English."),
    ("Can you do math?", "I can explain mathematical concepts and answer math-related questions."),
    ("What time is it?", "I do not have access to a clock, but I can help with other questions."),
    ("Tell me something interesting.", "Did you know that honey never spoils? Archaeologists have found edible honey in ancient tombs."),
    ("What is the meaning of life?", "That is a deep philosophical question. Many believe it is about finding purpose and happiness."),
    ("Do you sleep?", "I do not sleep. I am always ready to answer your questions."),
    ("What is your favorite color?", "I do not have preferences, but many people enjoy the color blue."),
    ("Can you sing?", "I cannot sing, but I can share information about music if you are interested."),
    ("Do you like music?", "I do not have personal preferences, but music is a wonderful form of human expression."),
    ("How old are you?", "I was recently created as part of a programming project."),
    ("Where are you from?", "I exist as software on a computer. I do not have a physical location."),
    ("What is happiness?", "Happiness is a positive emotional state characterized by feelings of joy and satisfaction."),
    ("What is love?", "Love is a complex emotion involving deep affection and care for another person or thing."),
    ("What is friendship?", "Friendship is a close relationship between people based on mutual trust and support."),
    ("What is success?", "Success is the achievement of a desired goal or outcome through effort and dedication."),
    ("What is knowledge?", "Knowledge is the understanding of facts and information gained through experience or education."),
    ("What is wisdom?", "Wisdom is the ability to apply knowledge and experience to make good decisions."),
    ("What is creativity?", "Creativity is the ability to generate new and original ideas or solutions."),
    ("What is courage?", "Courage is the ability to face fear and difficulties with bravery."),
    ("What is patience?", "Patience is the ability to wait calmly and endure difficulties without frustration."),
    ("What is respect?", "Respect is showing consideration and appreciation for others and their feelings."),
]

PREFIXES_Q = [
    "Can you tell me, ", "I want to know, ", "Please explain, ",
    "Could you answer: ", "I am curious, ", "Help me understand, ",
    "Do you know ", "Please tell me, ", "I would like to know, ",
    "Quick question: ", "I have a question: ", "Explain to me, ",
    "I need to understand, ", "Would you explain ", "May I ask, ",
    "I was wondering, ", "Can you explain ", "Could you tell me, ",
    "I'd like to ask: ", "Can you answer: ",
]

PREFIXES_A = [
    "Sure! ", "Of course. ", "Great question! ", "Certainly. ",
    "That is a good question. ", "Here is the answer: ",
    "I can help with that. ", "Let me explain. ",
    "Absolutely. ", "Good question. ", "Happy to help! ",
    "Yes, ", "Right, so ", "Well, ", "To answer that, ",
]

REPHRASING_PATTERNS = [
    ("What is", "Define"),
    ("What is", "Describe"),
    ("What is", "Explain what"),
    ("What is", "What do you mean by"),
    ("What is", "What does the term"),
    ("How does", "In what way does"),
    ("How does", "Can you explain how"),
    ("Why is", "What is the reason"),
    ("Why is", "For what reason is"),
    ("When did", "In what year did"),
    ("When was", "What year was"),
    ("Who was", "Tell me about"),
    ("Where is", "In what location is"),
    ("Where is", "Where can you find"),
    ("How many", "What is the number of"),
]

def generate_variation_qa(base_pairs, seed=42):
    random.seed(seed)
    variations = []
    for q, a in base_pairs:
        pq = random.choice(PREFIXES_Q)
        pa = random.choice(PREFIXES_A)
        new_q = pq + q[0].lower() + q[1:]
        new_a = pa + a
        variations.append((new_q, new_a))
    return variations

def generate_rephrase_qa(base_pairs, seed=42):
    random.seed(seed)
    variations = []
    for q, a in base_pairs:
        for old, new in REPHRASING_PATTERNS:
            if q.startswith(old):
                new_q = q.replace(old, new, 1)
                if new_q != q:
                    pa = random.choice(PREFIXES_A)
                    variations.append((new_q, pa + a))
                break
    return variations

def generate_follow_up_qa(base_pairs, seed=42):
    random.seed(seed)
    follow_ups = []
    templates = [
        ("Can you elaborate on {topic}?", "To elaborate, {answer}"),
        ("What else should I know about {topic}?", "Additionally, {answer}"),
        ("Is there more to know about {topic}?", "Yes, {answer}"),
        ("Give me more details about {topic}.", "In more detail, {answer}"),
        ("Summarize {topic} for me.", "In summary, {answer}"),
    ]
    for q, a in base_pairs:
        if random.random() < 0.4:
            # Extract a rough topic from the question
            topic = q.rstrip("?").rstrip(".").lower()
            for words in ["what is ", "what are ", "how does ", "why is ",
                          "define ", "explain ", "describe "]:
                if topic.startswith(words):
                    topic = topic[len(words):]
                    break
            ft_q, ft_a = random.choice(templates)
            follow_ups.append((
                ft_q.replace("{topic}", topic),
                ft_a.replace("{answer}", a[0].lower() + a[1:])
            ))
    return follow_ups

def generate_all_qa_pairs(seed=42):
    random.seed(seed)
    all_pairs = []

    # Base pairs
    all_pairs.extend(GEOGRAPHY_QA)
    all_pairs.extend(SCIENCE_QA)
    all_pairs.extend(MATH_QA)
    all_pairs.extend(TECHNOLOGY_QA)
    all_pairs.extend(HISTORY_QA)
    all_pairs.extend(GENERAL_QA)
    all_pairs.extend(CONVERSATIONAL_QA)

    # Templated pairs from concepts
    templated = generate_templated_qa(CONCEPTS, COMPARISONS)
    all_pairs.extend(templated)

    base_factual = GEOGRAPHY_QA + SCIENCE_QA + MATH_QA + TECHNOLOGY_QA + HISTORY_QA + GENERAL_QA

    # Prefix variations (multiple rounds with different seeds)
    for i in range(8):
        all_pairs.extend(generate_variation_qa(base_factual, seed=seed + i))
    for i in range(5):
        all_pairs.extend(generate_variation_qa(templated, seed=seed + 100 + i))
    for i in range(3):
        all_pairs.extend(generate_variation_qa(CONVERSATIONAL_QA, seed=seed + 200 + i))

    # Rephrased questions
    all_pairs.extend(generate_rephrase_qa(base_factual, seed=seed))
    all_pairs.extend(generate_rephrase_qa(templated, seed=seed + 1))

    # Follow-up questions
    all_pairs.extend(generate_follow_up_qa(base_factual, seed=seed))
    all_pairs.extend(generate_follow_up_qa(templated, seed=seed + 1))

    # Deduplicate by question text
    seen = set()
    unique_pairs = []
    for q, a in all_pairs:
        key = q.strip().lower()
        if key not in seen:
            seen.add(key)
            unique_pairs.append({"question": q, "answer": a})

    random.shuffle(unique_pairs)
    return unique_pairs

def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "qa_pairs.json")

    pairs = generate_all_qa_pairs()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pairs, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(pairs)} QA pairs")
    print(f"Saved to: {output_path}")
    return pairs

if __name__ == "__main__":
    main()
