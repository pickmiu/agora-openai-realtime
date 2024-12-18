import random
import logging
from ..logger import setup_logger

# Set up the logger with color and timestamp support
logger = setup_logger(name=__name__, log_level=logging.INFO)

topics = [
    {
        "number": "Topic 1: Small businesses",
        "questions": [
            "Do you know many small businesses where you live?",
            "Have you ever worked in small businesses?",
            "Do you prefer buying things from big companies or small businesses?",
            "Have you ever thought about starting your own business?"
        ]
    },
    {
        "number": "Topic 2: Sharing",
        "questions": [
            "Did your parents teach you to share when you were a child?",
            "What kind of things do you like to share with others?",
            "What kind of things are not suitable for sharing?",
            "Do you have anything to share with others recently?"
        ]
    },
    {
        "number": "Topic 3: Language",
        "questions": [
            "What languages can you speak?",
            "What languages would you like to learn in the future?",
            "How do you learn a foreign language?",
            "How are languages taught and learned in your school?",
            "What kinds of difficulties would you have if you want to learn a new language?"
        ]
    },
    {
        "number": "Topic 4: Pen & Pencil",
        "questions": [
            "Do you usually use a pen or a pencil?",
            "Which do you use more often? Pen or pencil?",
            "When was the last time you bought a pen or pencil?",
            "What do you think if someone gives you a pen or pencil as a present?"
        ]
    },
    {
        "number": "Topic 5: Chocolate",
        "questions": [
            "Do you like eating chocolate? Why or why not?",
            "How often do you eat chocolate?",
            "Did you often eat chocolate when you were a kid?",
            "Why do you think chocolate is popular around the world?",
            "What's your favourite flavour of chocolate?",
            "Do you think it is good to use chocolate as gifts to others?"
        ]
    },
    {
        "number": "Topic 6: Happy things",
        "questions": [
            "Is there anything that has made you feel happy lately?",
            "What made you happy when you were little?",
            "What do you think will make you feel happy in the future?",
            "When do you feel happy at work? Why?",
            "Do you feel happy when buying new things?",
            "Do you think people are happy when buying new things?"
        ]
    },
    {
        "number": "Topic 7: Staying up",
        "questions": [
            "Do you often stay up late?",
            "Did you stay up late when you were a kid?",
            "What do you do when you stay up late?",
            "What does it feel like the next morning if you stay up late?"
        ]
    },
    {
        "number": "Topic 8: T-shirt",
        "questions": [
            "Do you like wearing T-shirts?",
            "How often do you wear T-shirts?",
            "Do you like T-shirts with pictures or prints?",
            "Do you think older people who wear T-shirts are fashionable?",
            "Would you buy T-shirts as souvenirs on vacation?"
        ]
    },
    {
        "number": "Topic 9: Outer space and stars",
        "questions": [
            "Have you ever learnt about outer space and stars?",
            "Do you like science fiction movies? Why?",
            "Do you want to know more about outer space?",
            "Do you want to go into outer space in the future?"
        ]
    },
    {
        "number": "Topic 10: Art",
        "questions": [
            "Do you like art?",
            "Do you like visiting art galleries?",
            "Do you want to be an artist?",
            "Do you like modern art or traditional art?"
        ]
    },
    {
        "number": "Topic 11: Number",
        "questions": [
            "What's your favorite number?",
            "Are you good at remembering phone numbers?",
            "Do you usually use numbers?",
            "Are you good at math?"
        ]
    },
    {
        "number": "Topic 12: Weekends",
        "questions": [
            "Do you like weekends?",
            "What do you usually do on weekends? Do you study or work?",
            "What did you do last weekend?",
            "Do you make plans for your weekends?"
        ]
    },
    {
        "number": "Topic 13: Relax",
        "questions": [
            "What would you do to relax?",
            "Do you think doing sports is a good way to relax?",
            "Do you think vacation is a good time to relax?",
            "Do you think students need more relaxing time?"
        ]
    },
    {
        "number": "Topic 14: Life stages",
        "questions": [
            "What did you often do with your friends in your childhood?",
            "What do you think is the most important at the moment?",
            "Do you have any plans for the next five years?",
            "How do people remember each stage of their lives?"
        ]
    },
    {
        "number": "Topic 15: Breakfast",
        "questions": [
            "What do you usually eat for breakfast?",
            "Do you think breakfast is important?",
            "Are there any differences between the mornings of your childhood and now?",
            "Would you like to change your morning routine?"
        ]
    },
    {
        "number": "Topic 16: Jewelry",
        "questions": [
            "Do you often wear jewelry?",
            "What type of jewelry do you like?",
            "Do you usually buy jewelry?",
            "Why do you think some people wear a piece of jewelry for a long time?"
        ]
    },
    {
        "number": "Topic 17: Keys",
        "questions": [
            "Do you always bring a lot of keys with you?",
            "Have you ever lost your keys?",
            "Do you often forget the keys and lock yourself out?",
            "Do you think it's a good idea to leave your keys with a neighbour?"
        ]
    },
    {
        "number": "Topic 18: Library",
        "questions": [
            "Do you often go to the library?",
            "What do you usually do in the library?",
            "Did you go to the library when you were a kid?",
            "Do Chinese kids often go to the library?"
        ]
    },
    {
        "number": "Topic 19: Internet",
        "questions": [
            "When did you start using the internet?",
            "How often do you go online?",
            "How does the internet influence people?",
            "Do you think you spend too much time online?",
            "What would you do without the internet?"
        ]
    },
    {
        "number": "Topic 20: News",
        "questions": [
            "Are you interested in news?",
            "How do you usually find news?",
            "How do your friends get news?",
            "Have you read the news this morning?",
            "Do you often talk with your friends about the news?"
        ]
    },
    {
        "number": "Topic 21: Science",
        "questions": [
            "Do you like science?",
            "When did you start to learn about science?",
            "Which science subject is interesting to you?",
            "What kinds of interesting things have you done with science?",
            "Do you like watching science TV programs?",
            "Do Chinese people often visit science museums?"
        ]
    },
    {
        "number": "Topic 22: E-books and paper books",
        "questions": [
            "Which do you prefer, e-books or paper books?",
            "When do you usually read online?",
            "Will you read more online in the future?",
            "Do you think paper books will disappear in the future?"
        ]
    },
    {
        "number": "Topic 23: Daily routine",
        "questions": [
            "What is your daily study routine?",
            "Have you ever changed your routine?",
            "Do you think it is important to have a daily routine for your study?",
            "What part of your day do you like best?"
        ]
    },
    {
        "number": "Topic 24: Doing sports",
        "questions": [
            "What sports do you like?",
            "Where did you learn how to do it?",
            "Did you do some sports when you were young?",
            "Do you think students need more exercise?",
            "Do you know any schoolmates who are good at sports?",
            "Do you think it is important for people to exercise?",
            "Should schools encourage young students to take more physical exercise?"
        ]
    },
    {
        "number": "Topic 25: Exciting activities",
        "questions": [
            "Have you ever tried any exciting activities?",
            "What do you think were exciting activities when you were a child?",
            "Has anything exciting happened to you recently?",
            "Would you like to try scuba diving and bungee jumping?"
        ]
    },
    {
        "number": "Topic 26: Schools and workplaces",
        "questions": [
            "Where is your school?",
            "Do you like your school?",
            "Do you think your school is a good place to study?",
            "What is the environment like at your school?",
            "What do you think could be improved in your school?",
            "How important is interest in study?",
            "Which subject do you find challenging?",
            "Do you like your job?",
            "Do you currently have a good work environment?",
            "What do you think could be improved at your workplace?",
            "Have you ever thought about changing jobs?",
            "What do you think would be challenging when you start working in the future?",
            "Is there a place in your company that makes you feel relaxed?",
            "What are the advantages of a company having a relaxation room?",
            "How do you go to work?",
            "How do you go to school?"
        ]
    },
    {
        "number": "Topic 27: Holidays",
        "questions": [
            "Where did you go for your last holiday?",
            "Do you like holidays? Why?",
            "Which public holiday do you like best?",
            "What do you do on holidays?",
            "Do you like to spend your day at home?",
            "Do you prefer a leisurely or a busy holiday?"
        ]
    },
    {
        "number": "Topic 28: Childhood memory",
        "questions": [
            "What did you enjoy doing as a child?",
            "Did you enjoy your childhood?",
            "What are your best childhood memories?",
            "Do you think it is better for children to grow up in the city or in the countryside?"
        ]
    },
    {
        "number": "Topic 29: Asking for help",
        "questions": [
            "Do you ask for help when you have a problem?",
            "Why are teachers always willing to help students?",
            "What kinds of help do you often ask for?",
            "When was the last time you asked for help?"
        ]
    },
    {
        "number": "Topic 30: Morning routines",
        "questions": [
            "What do you do in the mornings?",
            "Is breakfast important?",
            "What is your morning routine?",
            "Do you like to get up early in the morning?"
        ]
    },
    {
        "number": "Topic 31: Staying at home",
        "questions": [
            "Are you a person who likes to stay at home?",
            "What do you do when you stay at home?",
            "What is your favourite place at home?",
            "What did you often do at home as a child?",
            "Would you like to stay at home a lot in the future?"
        ]
    },
    {
        "number": "Topic 32: Shopping",
        "questions": [
            "Do you like shopping?",
            "Do you compare prices when you shop? Why?",
            "Is it difficult for you to make choices when you shop?",
            "Do you think expensive products are always better than cheaper ones?"
        ]
    },
    {
        "number": "Topic 33: Weather",
        "questions": [
            "What’s the weather like where you live?",
            "Do you prefer cold or hot weather?",
            "Do you prefer dry or wet weather?",
            "Are you in the habit of checking the weather forecast? When/How often?",
            "What do you think are the effects of climate change in recent years?",
            "Would you like to visit other cities that have different climates from where you live?"
        ]
    },
    {
        "number": "Topic 34: Birthday",
        "questions": [
            "What do you usually do on your birthday?",
            "What did you do on your birthday when you were young?",
            "Do you think it is important for you to celebrate your birthday?",
            "Whose birthday do you think is the most important to celebrate in China?"
        ]
    },
    {
        "number": "Topic 35: Challenges",
        "questions": [
            "What subject do you think is the most challenging at school?",
            "Do you like to challenge yourself?",
            "Do you like to live a life that has a lot of challenges?",
            "How do you usually deal with challenges in daily life?"
        ]
    },
    {
        "number": "Topic 36: Plants",
        "questions": [
            "Do you keep plants at home?",
            "What plant did you grow when you were young?",
            "Do you know anything about growing a plant?",
            "Do Chinese people send plants as gifts?"
        ]
    },
    {
        "number": "Topic 37: Video games",
        "questions": [
            "Do you play video games?",
            "Would you watch others play video games?",
            "Do you think people spend too much time playing video games?",
            "Do you prefer playing video games alone or with others?"
        ]
    },
    {
        "number": "Topic 38: Social media",
        "questions": [
            "When did you start using social media?",
            "Do you think you spend too much time on social media?",
            "Do your friends use social media?",
            "What do people often do on social media?"
        ]
    },
    {
        "number": "Topic 39: Memory",
        "questions": [
            "Are you good at memorising things?",
            "Have you ever forgotten something important?",
            "What do you need to remember in your daily life?",
            "How do you remember important things?"
        ]
    },
    {
        "number": "Topic 40: Singing",
        "questions": [
            "Do you like singing? Why?",
            "Have you ever learned how to sing?",
            "Who do you want to sing for?",
            "Do you think singing can bring happiness to people?"
        ]
    },
    {
        "number": "Topic 41: Helping others",
        "questions": [
            "Do you usually help people around you?",
            "How do you help people around you, such as neighbours, family and friends?",
            "Do your parents teach you how to help others?",
            "Did your parents help you a lot when you were young?",
            "What have you done to help the elderly?"
        ]
    },
    {
        "number": "Topic 42: Films",
        "questions": [
            "What films do you like?",
            "Did you often watch films when you were a child?",
            "Did you ever go to the cinema alone as a child?",
            "Do you often go to the cinema with your friends?",
            "Do you think going to the cinema is a good way to spend time with friends?"
        ]
    },
    {
        "number": "Topic 43: Music/Musical instruments",
        "questions": [
            "Have you ever learned to play a musical instrument?",
            "What musical instruments do you enjoy listening to the most?",
            "Do you think children should learn to play an instrument at school?",
            "Do you think music education is important to children?",
            "Do a lot of people like music?",
            "Do schools in your country have music lessons?"
        ]
    },
    {
        "number": "Topic 44: Clothing",
        "questions": [
            "What kind of clothes do you like to wear?",
            "Do you prefer to wear comfortable and casual clothes or smart clothes?",
            "Do you like wearing T-shirts?",
            "Do you spend a lot of time choosing clothes?"
        ]
    },
    {
        "number": "Topic 45: The city you live in",
        "questions": [
            "What city do you live in?",
            "Do you like this city? Why?",
            "How long have you lived in this city?",
            "Are there big changes in this city?"
        ]
    },
    {
        "number": "Topic 46: Work or studies",
        "questions": [
            "What subjects are you studying?",
            "Do you like your subject?",
            "Why did you choose to study that subject?",
            "Do you think that your subject is popular in your country?",
            "Do you have any plans for your studies in the next five years?",
            "What are the benefits of being your age?",
            "Do you want to change your major?",
            "Do you prefer to study in the mornings or in the afternoons?",
            "How much time do you spend on your studies each week?",
            "Are you looking forward to working?",
            "What technology do you use when you study?",
            "What changes would you like to see in your school?",
            "What work do you do?",
            "Why did you choose to do that type of work (or that job)?",
            "Do you like your job?",
            "What requirements did you need to meet to get your current job?",
            "Do you have any plans for your work in the next five years?",
            "What do you think is the most important at the moment?",
            "Do you want to change to another job?",
            "Do you miss being a student?",
            "What technology do you use at work?",
            "Who helps you the most? And how?"
        ]
    },
    {
        "number": "Topic 47: Home/accommodation",
        "questions": [
            "What kind of house or apartment do you want to live in in the future?",
            "Are the transport facilities to your home very good?",
            "Do you prefer living in a house or an apartment?",
            "Please describe the room you live in.",
            "What part of your home do you like the most?",
            "How long have you lived there?",
            "Do you plan to live there for a long time?",
            "What’s the difference between where you are living now and where you have lived in the past?",
            "Can you describe the place where you live?",
            "What room does your family spend most of the time in?",
            "What's your favorite room in your apartment or house？",
            "What makes you feel pleasant in your home？",
            "Do you think it is important to live in a comfortable environment？",
            "Do you live in an apartment or a house?",
            "Who do you live with?",
            "What do you usually do in your apartment?",
            "What kinds of accommodation do you live in?"
        ]
    },
    {
        "number": "Topic 48: Hometown",
        "questions": [
            "Where is your hometown?",
            "Is that a big city or a small place?",
            "Please describe your hometown a little.",
            "How long have you been living there?",
            "Do you think you will continue living there for a long time?",
            "Do you like your hometown?",
            "Do you like living there?",
            "What do you like (most) about your hometown?",
            "Is there anything you dislike about it?",
            "What's your hometown famous for？",
            "Did you learn about the history of your hometown at school？",
            "Are there many young people in your hometown?",
            "Is your hometown a good place for young people to pursue their careers?"
        ]
    },
    {
        "number": "Topic 49: The area you live in",
        "questions": [
            "Do you like the area that you live in?",
            "Where do you like to go in that area?",
            "Do you know any famous people in your area?",
            "What are some changes in the area recently?",
            "Do you know any of your neighbors?",
            "Are the people in your neighborhood nice and friendly?"
        ]
    },
    {
        "number": "Topic 50",
        "questions": [
            "Part 2: Describe a website you often visit. You should say: - What it is about - How you found out about it - How often you visit it - And explain why you often visit it",
            "Part 3: What are the differences between old people and young people when they use the internet? What kinds of people would still go to the library to read and study? Is the library still necessary? Why? Why do some people like to read the news on the internet instead of getting it from TV? What's the difference between the internet and television? What are the most popular and least popular apps in China?"
        ]
    },
    {
        "number": "Topic 51",
        "questions": [
            "Part 2: Describe an advertisement you have seen but you did not like. You should say: - Where and when you saw it - What the advertisement was for - What you could see in the advertisement - And explain why you did not like the advertisement",
            "Part 3: What role does social media play in advertising? Does advertising encourage us to buy things we don't need? What do you think of celebrity endorsements in advertising? What are the benefits of advertising? Which one is more effective, newspaper advertising or online advertising? What are the most advertised products in your country?"
        ]
    },
    {
        "number": "Topic 52",
        "questions": [
            "Part 2: Describe a piece of technology you own that you feel is difficult to use. You should say: - When you got it - What you got it for - How often you use it - And explain how you feel about it",
            "Part 3: Does the development of technology affect the way we study? How? What changes has the development of technology brought about in our lives? Why do technology companies keep upgrading their products? Why are people so keen on buying iPhones even though they haven't changed much from one iPhone to the next? Why do big companies introduce new products frequently? What technology do people currently use?"
        ]
    },
    {
        "number": "Topic 53",
        "questions": [
            "Part 2: Describe another city you would like to stay for a short time. You should say: - Where the city is - Why you want to go there - Whom you will go there with - What you will do there - And explain why you will stay there just for a short time",
            "Part 3: Why is the noise pollution worse in tourism cities than in other cities? Do most people like planned travelling? Do you think tourists may come across bad things in other cities? Why do places with historical sites develop tourism industry more actively? Why are historical cities popular? Why do people sometimes go to other cities or other countries to travel?"
        ]
    },
    {
        "number": "Topic 54",
        "questions": [
            "Part 2: Describe a place (city/town) that is good for people to live in. You should say: - Where it is - How you knew this place - What it is like - And explain why it is better than other places to live in",
            "Part 3: What are the differences between cities and towns? What has happened to towns and villages in recent years in your country? What are the differences between big cities and small ones? What factors will contribute to whether a place is good to live in or not? What are the major changes that have happened in your city? How different is life in the countryside to life in the city?"
        ]
    },
    {
        "number": "Topic 55",
        "questions": [
            "Part 2: Describe a person who likes to buy goods with low prices. You should say: - Who this person is - What this person likes to buy - Where this person likes to buy things - And explain why this person likes cheap goods",
            "Part 3: What are the differences between shopping in a shopping mall and in a street market? Which is more commonly visited in China, shopping malls or street markets? Is advertising important? What are the disadvantages of shopping in a street market? How do you buy cheap products? Do you think things are more expensive in big shopping malls?"
        ]
    },
    {
        "number": "Topic 56",
        "questions": [
            "Part 2: Describe an important plant in your country. You should say: - What it is - Where you see it - What it looks like - And explain why it is important",
            "Part 3: What are the features of living in the countryside? Should schools teach children how to grow plants? Why do some people prefer to live in the countryside? Have new kinds of plants been grown in your city recently? Why do some people like to keep plants at home? Are there many trees in your city?"
        ]
    },
    {
        "number": "Topic 57",
        "questions": [
            "Part 2: Describe a daily routine that you enjoy. You should say: - What it is - When and why you started to follow this routine - Whether it is easy to follow this routine - And explain why you enjoy having this routine in your daily life",
            "Part 3: Should children have learning routines? What are the advantages of children having a routine at school? Does having a routine make kids feel more secure at school? How do people's routines differ on weekdays and weekends? What daily routines do people have at home? What are the differences between people's daily routines now and in the last 15 years?"
        ]
    },
    {
        "number": "Topic 58",
        "questions": [
            "Part 2: Describe a place you visited where the air was polluted. You should say: - Where the place is - When you visited it - Why the air was not good - And explain how you felt about the place",
            "Part 3: Is there more pollution now than in the past? Do you think the city is cleaner or dirtier than the countryside? Why? What can factories and power plants do to reduce pollutants? Do you think the wind has any effect on pollution? How? In what ways can air pollution be reduced effectively? Do you think many companies have been forced to reduce pollutants?"
        ]
    },
    {
        "number": "Topic 59",
        "questions": [
            "Part 2: Describe a historical building you have been to. You should say: - Where it is - What it looks like - What it is used for now - What you learned there - And how you felt about this historical building",
            "Part 3: Why do people visit historical buildings? Do Chinese people like to visit historical buildings? Do most people agree to the government’s funding to protect historical buildings? Is it necessary to protect historical buildings? What factors do people often consider when buying a house or an apartment? What are the differences between today’s houses and those in the past?"
        ]
    },
    {
        "number": "Topic 60",
        "questions": [
            "Part 2: Describe a time when you taught a friend/relative something. You should say: - Who you taught - What/how you taught - What the result was - And explain how you felt about the experience",
            "Part 3: What practical skills can young people teach old people? How can young people teach old people skills? How can we know what to do when we want to learn something new? Do you think 'showing' is a better way than 'telling' in education? Do people in your country like to watch videos to learn something? What skills can young people teach old people besides technology?"
        ]
    },
    {
        "number": "Topic 61",
        "questions": [
            "Part 2: Describe a person who thinks music is important and enjoys music. You should say: - Who this person is - How you knew him/her - What music he/she likes - Why he/she thinks music is important - And explain how you feel about him/her",
            "Part 3: What do you think about playing music for children in class? Why do many teachers incorporate music into the classroom? Do you think there are any advantages to a shop with music playing? Would people's shopping behaviour be affected in a shop with music? What do you think would be the effect of background music in a film? Why are musical movies so popular?"
        ]
    },
    {
        "number": "Topic 62",
        "questions": [
            "Part 2: Describe an occasion you wore the best clothes. You should say: - When it was - What you wore - Why you wore it - And how you felt about it",
            "Part 3: Do you think people need to wear formally in the workplace? Why do some people like to wear traditional clothes? Will traditional clothes disappear in the future? Do old people change their style of dressing? Why do some people like to wear expensive clothes? Who would wear formal clothes more often, young people or old people?"
        ]
    },
    {
        "number": "Topic 63",
        "questions": [
            "Part 2: Describe your first day at school that you remember. You should say: - Where the school was - How you went there - What happened that day - And how you felt on that day",
            "Part 3: What would parents prepare when their kids go to school on the first day? How do children socialize with each other? Is socialization important for children? What are the reasons for job change? Are big companies better than small companies? Why? What are the advantages and disadvantages coming along with changing jobs?"
        ]
    },
    {
        "number": "Topic 64",
        "questions": [
            "Part 2: Describe your favorite place in your house where you can relax. You should say: - Where it is - What it is like - What you enjoy doing there - And explain why you feel relaxed at this place",
            "Part 3: Why is it difficult for some people to relax? What are the benefits of doing exercise? Do people in your country exercise after work? What is the place where people spend most of their time at home? Do you think there should be classes for training young people and children how to relax? Which is more important, mental relaxation or physical relaxation?"
        ]
    },
    {
        "number": "Topic 65",
        "questions": [
            "Part 2: Describe an indoor or outdoor place where it is easy for you to study. You should say: - Where it is - What it is like - When you go there - What you study there - And explain why you would like to study in this place",
            "Part 3: Do you like to learn on your own or with others? What's the difference between learning face-to-face with teachers and learning by yourself? Do you prefer to study at home or study in other places? What are the benefits of gaining work experience while studying? Do most people like to study in a noisy place? What are the advantages and disadvantages of studying with other people?"
        ]
    },
    {
        "number": "Topic 66",
        "questions": [
            "Part 2: Describe a time when you missed or were late for an important meeting/event. You should say: - When it happened - What happened - Why you missed/were late for it - And explain how you felt about this experience",
            "Part 3: Are you a punctual person? Do you think it is important to be on time? Do you always avoid being late? Why are people often late for meetings or appointments? Are people in your country often late for meetings? Do you think people are born with time management skills or they can develop them?"
        ]
    },
    {
        "number": "Topic 67",
        "questions": [
            "Part 2: Describe a person you met at a party who you enjoyed talking with. You should say: - What party it was - Who this person is - What you talked about - And explain why you enjoyed talking with him/her",
            "Part 3: In what situations would people be willing to get to know new people? Where do people go to meet new people? How do people start a conversation? Is it difficult for Chinese people to communicate with people from other countries? Why are some people unwilling to have conversations with others? Is it difficult for adults to talk with children?"
        ]
    },
    {
        "number": "Topic 68",
        "questions": [
            "Part 2: Describe a place you have been to where things are expensive. You should say: - Where the place is - What the place is like - Why you went there - What you bought there - And explain why you think things are expensive there",
            "Part 3: Why do some people still use cash? Will the payment be paperless in the future? What do you think of the view that time is as important as money? Is it more important to choose a job with a high salary or with more time off? How important is it to have a variety of payment option? Why are things more expensive in some places than in others?"
        ]
    },
    {
        "number": "Topic 69",
        "questions": [
            "Part 2: Describe a special meal that someone made for you. You should say: - Who did it - When and how he/she cooked - What and why he/she cooked for you - And explain how you felt about the meal",
            "Part 3: Should students learn to cook at school? Do you think people's eating habits would change as they get older? Do people in your country like to learn to cook from TV programmes? What kinds of fast food are popular in China? Are there any people who wouldn't eat meat for their whole lives? What do you think about vegetarians?"
        ]
    },
    {
        "number": "Topic 70",
        "questions": [
            "Part 2: Describe something you own that you want to replace. You should say: - What it is - Where it is - How you got it - And explain why you want to replace it",
            "Part 3: Does consumption have any impact on the environment? Why do people always want to buy new things to replace old ones? Why do you think some people replace things more often than others? Why do young people change things more often than old people? Why do some people like to buy expensive things? Why do some people prefer to buy things in the supermarket rather than online?"
        ]
    },
    {
        "number": "Topic 71",
        "questions": [
            "Part 2: Describe a complaint that you made and you were satisfied with the result. You should say: - When it happened - Who you complained to - What you complained about - And explain why you were satisfied with the result",
            "Part 3: When are people more likely to make complaints? What do people often complain about? Which one is better when making a complaint, by talking or by writing? Who are more likely to make complaints, older people or younger people? How would you react if you received a poor service at a restaurant? How do people often respond to poor customer service?"
        ]
    },
    {
        "number": "Topic 72",
        "questions": [
            "Part 2: Describe a film character played by an actor or actress whom you admire. You should say: - Who this actor/actress is - When you saw the film - What the character was like in this film - And explain why you admire this actor/actress",
            "Part 3: Are actors or actresses very interested in their work? Why? Is being a professional actor or actress a good career? What can children learn from acting? Why do children like special costumes? What are the differences between actors or actresses who earn much and those who earn little? What are the differences between acting in a theatre and that in a film?"
        ]
    },
    {
        "number": "Topic 73",
        "questions": [
            "Part 2: Describe a new law you would like to introduce in your country. You should say: - What law it is - What changes this law brings - Whether this new law will be popular - How you came up with the new law - And explain how you feel about this new law",
            "Part 3: What rules should students follow at school? Do people in your country usually obey the law? What kinds of behavior are considered as good behavior? Do you think children can learn about the law outside of school? What are the benefits for people to obey rules? How can parents teach children to obey rules?"
        ]
    },
    {
        "number": "Topic 74",
        "questions": [
            "Part 2: Describe a piece of good news that you heard about someone you know well. You should say: - What it was - When you heard it - How you knew it - And explain how you felt about it",
            "Part 3: Is it good to share something on social media? Should the media only publish good news? How does social media help people access information? What kind of good news do people often share in the community? Do most people like to share good news with others? Do people like to hear good news from their friends?"
        ]
    },
    {
        "number": "Topic 75",
        "questions": [
            "Part 2: Describe a sport that you only have watched before but have not played yourself. You should say: - What it is - When you watched it - Where you watched it - Who you watched it with - And explain how you felt about it",
            "Part 3: What kinds of sports would you like to play in the future? Why are there many athletes in advertisements? What are the features of people who watch sports games online, such as gender or age? What's the most popular sport in your country? What kinds of sports are popular now but not popular 50 years ago? Do you think there are too many sorts of sports games on TV?"
        ]
    },
    {
        "number": "Topic 76",
        "questions": [
            "Part 2: Describe an enjoyable journey by public transport. You should say: - Where you went - Who you were with - What you did - And how you felt about it",
            "Part 3: Why do people choose to travel by public transport? Why do more and more people like to travel by plane? Do you think offering free public transport will solve traffic problems in the city? What are the disadvantages of traveling by public transport? What do you think are the cheapest and most expensive means of transport? What are the difficulties that commuters face during rush hours?"
        ]
    },
    {
        "number": "Topic 77",
        "questions": [
            "Part 2: Describe a time when someone gave you something that you really wanted. You should say: - What it was - When you received it - Who gave it to you - And explain why you wanted it so much",
            "Part 3: Should employees have their own goals? How should bosses reward employees? What kinds of gifts do young people like to receive as rewards? How should children spend their allowance money? Why do people like shopping more now than in the past? Do you think shopping is good for a country's economy?"
        ]
    },
    {
        "number": "Topic 78",
        "questions": [
            "Part 2: Describe a person who you are happy to know. You should say: - Who this person is - How you know this person - What he or she is like - And explain why you are happy to know him/her",
            "Part 3: How can children feel happy? What's the difference between adults' and children's happiness? Do you think everyone shares a similar definition of happiness? Some people say that living in a happy city is boring. What do you think? Which do you think is more important in the workplace, happiness or high salaries? How can companies improve employee happiness?"
        ]
    },
    {
        "number": "Topic 79",
        "questions": [
            "Part 2: Describe something you would like to learn in the future. You should say: - What it is - How you would like to learn it - Where you would like to learn it - Why you would like to learn it - And explain whether it’s difficult to learn it",
            "Part 3: What's the most popular thing to learn nowadays? At what age should children start making their own decisions? Why? Which influences young people more when choosing a course, income or interest? Do young people take their parents' advice when choosing a major? Besides parents, who else would people take advice from? Why do some people prefer to study alone?"
        ]
    },
    {
        "number": "Topic 80",
        "questions": [
            "Part 2: Describe an interesting place you have been to with a friend. You should say: - What and where the place is - Who you went with - When you went there - What you did there - And explain why you think it is interesting",
            "Part 3: Why do people need friends? How do you communicate with friends? Why don't some people like to socialise? Can talking with people improve social skills? Does technology help people communicate better with others? Do you prefer to go out with a group of friends or just with a few close friends?"
        ]
    },
    {
        "number": "Topic 81",
        "questions": [
            "Part 2: Describe an interesting old person you have met. You should say: - Who this person is - When/where you met this person - What you did with this person - And explain why you think this person is interesting",
            "Part 3: Do you think old people and young people can share interests? What can old people teach young people? Is it easy for young people and old people to make friends with each other? Are there benefits when one person is interested in another person? Why? Do you think people are more selfish or self-centered now than in the past? What benefits can people get if they are self-centered?"
        ]
    },
    {
        "number": "Topic 82",
        "questions": [
            "Part 2: Describe a person who encouraged you to achieve your goal. You should say: - Who the person is - How he/she encouraged you - What goal you achieved - And explain how you feel about this person",
            "Part 3: Do you think children are more likely to achieve their goals if they are encouraged? What should parents do if their children don't want to study? Who do you think should set goals for children? Who plays a more important role in children's education, parents or teachers? Is money the only motivation for people to work hard? Which is more important, competition or cooperation?"
        ]
    },
    {
        "number": "Topic 83",
        "questions": [
            "Part 2: Describe a tourist attraction that very few people visit but you think is interesting. You should say: - What the place is - What people can see there - Why only very few people visit there - And explain why you think it is interesting",
            "Part 3: Why do people visit tourist attractions? What makes a tourist attraction famous? Do local people like to visit local tourist attractions? Do you think tourism causes environmental damage? How can people prevent the environmental damage caused by tourism? Should all tourist attractions be free to the public?"
        ]
    },
    {
        "number": "Topic 84",
        "questions": [
            "Part 2: Describe a person you really enjoy studying/working with. You should say: - Who this person is - When you often study/work together - What you study/work together - And explain why you enjoy studying/working with him/her",
            "Part 3: Should children be encouraged to learn from their peers? What difficulties or problems would introverted people face in work or study? How can a person be a good co-worker? What makes a good employee? How can people improve their collaboration skills? Do you think it is more important for an employee to keep good relationships with colleagues than just focus on the work?"
        ]
    },
    {
        "number": "Topic 85",
        "questions": [
            "Part 2: Describe a place where you have taken photos more than once. You should say: - Where the place is - When you took the photos - What special features the photos taken there have - And explain why you have been there more than once to take photos",
            "Part 3: Do you like to take photos? Where do people often like to take photos? Who would like to take photos more often, young people or older people? Would you pay a lot of money to hire a photographer? Do you think being a photographer is a good job? On what occasions do people need formal photos?"
        ]
    },
    {
        "number": "Topic 86",
        "questions": [
            "Part 2: Describe a time you taught something new to a younger person. You should say: - When it happened - What you taught - Who you taught - Why you taught this person - And how you felt about the teaching",
            "Part 3: What skills do adults need to have? How can people be motivated to learn new things? What can children learn from teachers and parents? What are the skills that you wanted to learn? What skills should children learn before entering school? How does a good learner learn something new?"
        ]
    },
    {
        "number": "Topic 87",
        "questions": [
            "Part 2: Describe a noisy place you have been to. You should say: - Where it is - When you went there - What you did there - And explain why you feel it’s a noisy place",
            "Part 3: Do you think it is good for children to make noise? Should children not be allowed to make noise under any circumstances? What kinds of noises are there in our life? Which area is exposed to noise more, the city or the countryside? How would people usually respond to noises in your country? How can people consider others' feelings when chatting in public?"
        ]
    },
    {
        "number": "Topic 88",
        "questions": [
            "Part 2: Describe an activity you enjoyed in your free time when you were young. You should say: - What it was - Where you did it - Who you did it with - And explain why you enjoyed it",
            "Part 3: Is it important to have a break during work or study? What sports do young people like to do now? Are there more activities for young people now than 20 years ago? Can most people balance work and life in China? What activities do children and adults do nowadays? Do adults and children have enough time for leisure activities nowadays?"
        ]
    },
    {
        "number": "Topic 89",
        "questions": [
            "Part 2: Describe someone you know who made a good decision recently. You should say: - Who he/she is - When he/she made the decision - What decision he/she made - Why it was a good decision - And explain how you felt about the decision",
            "Part 3: Should parents make decisions for their children? Do you think parents are the best people to make decisions about their children's education? At what age do you think children can be allowed to make decisions by themselves? Why do most children find it difficult to make decisions? Should parents interfere in children's decision-making? How should parents help their children make decisions?"
        ]
    },
    {
        "number": "Topic 90",
        "questions": [
            "Part 2: Describe a risk you took that you thought would lead to a terrible result but ended up with a positive result. You should say: - When you took the risk - Why you took the risk - How it went - And explain how you felt about it",
            "Part 3: How should parents teach their children what a risk is? What risks should parents tell their children to avoid? Why do some people like to watch risk-taking movies? What kinds of sports are dangerous but exciting? Why do some people enjoy dangerous sports? Who is more interested in taking risks, the young or the old?"
        ]
    },
    {
        "number": "Topic 91",
        "questions": [
            "Part 2: Describe a natural place (e.g. parks, mountains). You should say: - Where this place is - How you knew this place - What it is like - And explain why you like to visit it",
            "Part 3: What kind of people like to visit natural places? What are the differences between a natural place and a city? Do you think that going to the park is the only way to get close to nature? What can people gain from going to natural places? Are there any wild animals in the city? Do you think it is a good idea to let animals stay in local parks for people to see?"
        ]
    },
    {
        "number": "Topic 92",
        "questions": [
            "Part 2: Describe a subject that you would like to learn in the future. You should say: - What it is - Where and how you want to learn it - Why you want to learn it - And explain if it will be difficult to learn it",
            "Part 3: What are the differences between online learning and offline learning? Do you prefer to study alone or with a group of people? What are the advantages and disadvantages of learning in a group? What subjects do most young people prefer to learn? Why? What is more important when choosing a job, high salary or interest? What do you think about face-to-face learning with teachers?"
        ]
    },
    {
        "number": "Topic 93",
        "questions": [
            "Part 2: Describe a time when you received money as a gift. You should say: - When it happened - Who gave you money - Why he/she gave you money - And explain how you used the money",
            "Part 3: Why do people rarely use cash now? When do children begin to comprehend the value of money? Is it good and necessary to teach children to save money? Should parents reward children with money? What are the advantages and disadvantages of using credit cards? Do you think it's a good thing that more people are using digital payment?"
        ]
    },
    {
        "number": "Topic 94",
        "questions": [
            "Part 2: Describe someone (a famous person) that is a role model for young people. You should say: - Who he/she is - How you knew him/her - What he/she has done - And explain why he/she can be a role model for young people",
            "Part 3: What kinds of people are likely to be the role models for teenagers? Is it important for children to have a role model? Are there any differences between today’s famous people and those of the past? What qualities do famous people have? What kinds of people are likely to become famous? Do people tend to choose the best people as their role model?"
        ]
    },
    {
        "number": "Topic 95",
        "questions": [
            "Part 2: Describe something that you did with someone/a group of people. You should say: - What it was - Who you did it with - How long it took you to do this - And explain why you did it together",
            "Part 3: How do you get along with your neighbors? How do neighbors help each other? Do you think neighbors help each other more often in the countryside than in the city? How do children learn to cooperate with each other? Do you think parents should teach children how to cooperate with others? How? Do you think it's important for children to learn about cooperation?"
        ]
    },
    {
        "number": "Topic 96",
        "questions": [
            "Part 2: Describe an unusual meal you had. You should say: - When you had it - Where you had it - Whom you had it with - And explain why it was unusual",
            "Part 3: What are the advantages and disadvantages of eating in restaurants? What fast food restaurants are there in your country? Do people eat fast food at home? Why do some people choose to eat out instead of ordering takeout? Do people in your country socialize in restaurants? Why? Do people in your country value food culture?"
        ]
    },
    {
        "number": "Topic 97",
        "questions": [
            "Part 2: Describe a picture/photograph of you that you like. You should say: - Where it was taken/drawn - When it was taken/drawn - Who took/drew it - And explain how you felt about it",
            "Part 3: Why do people take photos? What do people use to take photos these days, cameras or phones? Is it difficult for people to learn how to take good photos? How do people keep their photos? What photos do people often hang on the wall at home? Is it necessary for students to learn art?"
        ]
    },
    {
        "number": "Topic 98",
        "questions": [
            "Part 2: Describe a public event you have attended. You should say: - What the event was - When you went there - Whom you went there with - And explain why you enjoyed this event",
            "Part 3: What kinds of public events are popular in your country? Why do people like to attend these events? What are the benefits of attending public events? How do public events contribute to the local economy? What are some of the challenges in organizing public events? How can public events be made more inclusive?"
        ]
    },
    {
        "number": "Topic 99",
        "questions": [
            "Part 2: Describe a kind of car you would like to buy in the future. You should say: - What it is like - Where you can buy it - How you can buy it - And explain why you want to buy it",
            "Part 3: What are the advantages and disadvantages of riding a bicycle? Is the traffic planning reasonable in your hometown? What are the benefits of owning a car? How can public transportation be improved in cities? Why do some people prefer driving to using public transport? How does car ownership affect the environment?"
        ]
    },
    {
        "number": "Topic 100",
        "questions": [
            "Part 2: Describe something you did that made you feel proud. You should say: - What it was - How you did it - What difficulty you had - How you dealt with the difficulty - And explain why you felt proud of it",
            "Part 3: Which one is more important, personal goals or work goals? Have your life goals changed since your childhood? Does everyone set goals for themselves? What kinds of rewards are important at work? Do you think material rewards are more important than other rewards at work? What makes people feel proud of themselves?"
        ]
    },
    {
        "number": "Topic 101",
        "questions": [
            "Part 2: Describe a kind of foreign food you have had. You should say: - When you had it - Where you ate it - What it was - And explain how you felt about it",
            "Part 3: Is there a relationship between food and health? How do people's eating habits change over time? What are the benefits of trying foreign food? How does culture influence food preferences? Why do some people prefer to eat at home rather than in restaurants? What impact does globalization have on food choices?"
        ]
    },
    {
        "number": "Topic 102",
        "questions": [
            "Part 2: Describe a new development in the area where you live (e.g. shopping mall, park…). You should say: - What and where the development is - What it was like before - How long it took to complete it - How people feel about it - And explain how it has improved the area you live in",
            "Part 3: Is public transportation popular in China? What can be done to improve public transport services in your hometown? What leisure facilities can be used by people of all ages? Do you think young people in your country like going to the cinema? How is the subway system developing in your country? What transportation do you use the most?"
        ]
    },
    {
        "number": "Topic 103",
        "questions": [
            "Part 2: Describe a sport you watched and would like to try. You should say: - When and where you watched it - Why you watched it - Who you watched it with - Whether you will do it in the future - And explain how you felt about it",
            "Part 3: Why do many people like to buy expensive sportswear for playing ball games? What kinds of sports games do young and old people like to watch in your country? Why do so many people like to watch sports games? Do you think that international sports games are for money? Many advertisers like to use sports stars endorsements. What do you think are the reasons? Do you think sportsmen would use the sports gears promoted in the commercials?"
        ]
    },
    {
        "number": "Topic 104",
        "questions": [
            "Part 2: Describe a new skill that you learned. You should say: - What it was - How long you learned it - Why you learned it - And explain how long you will use the skill",
            "Part 3: What skills are important to learn for the future? How can people learn new skills effectively? What are the challenges of learning new skills? How does technology influence the way we learn new skills? Why is it important to keep learning new skills throughout life? What skills do employers look for in job candidates?"
        ]
    },
    {
        "number": "Topic 105",
        "questions": [
            "Part 2: Describe an occasion when you used a map (e.g. a paper map, an electronic map) that was useful. You should say: - When and where you used the map - What it was like - How useful it was - Why you used it - And explain how you felt about the experience",
            "Part 3: What do people usually do when they get lost? What are the differences between paper and digital maps? What do you think of in-car GPS navigation systems? What do people often do with a map? Why do some people prefer to use a paper map? How does learning to read a map help you learn more about your country?"
        ]
    },
    {
        "number": "Topic 106",
        "questions": [
            "Part 2: Describe a person who is good at making people feel welcome in his/her home. You should say: - Who this person is - How you knew him/her - How he/she makes you feel welcome - And explain why you think he/she is good at making people feel welcome",
            "Part 3: Do people in your country often invite others to their homes? Why? What do you think of serving food to visitors? What kind of people do you think are more likely to invite others to their homes? Who are more likely to invite others to their homes, people in the countryside or people in the city? Are tourist attractions in the countryside more popular than those in the cities? What facilities are there in the tourist attractions in your country?"
        ]
    },
    {
        "number": "Topic 107",
        "questions": [
            "Part 2: Describe a job that you would not like to do. You should say: - What it is - How you know about the job - Whether the job is difficult or not - And explain why you would not like to do it",
            "Part 3: What kind of jobs do young Chinese people like to do? Do young Chinese people prefer to choose an interesting job or a job with a high salary? Do you think it is easier to get a job now than in the past? Is it important to be successful in a job? Do you think AI will take over many jobs? Can AI improve people’s lives? If so, how?"
        ]
    },
    {
        "number": "Topic 108",
        "questions": [
            "Part 2: Describe a movie/film that you felt strongly about. You should say: - What it is about - When you watched it - Where you watched it - And explain why you felt strongly about it",
            "Part 3: Do most people prefer to watch movies at home or in a cinema? Why? What are the advantages of going to the cinema with friends? Is going to the cinema still popular? What kind of movies do you think need to be seen in the cinema to be fully appreciated? What can cinemas do to attract more audiences? Do you think people can learn new cultures through movies?"
        ]
    },
    {
        "number": "Topic 109",
        "questions": [
            "Part 2: Describe a time you had to finish something quickly. You should say: - What it was - When it happened - How you finished it - Why you had to finish it quickly - And explain how you felt about it",
            "Part 3: On what occasions do people have to do things in a hurry? Why do some people spend a long time on having a meal? Would people feel more satisfied if they finished doing something quickly? What kinds of jobs need to be done quickly? What are some examples of work that needs to be done quickly? What might make some people more productive than others in completing tasks?"
        ]
    },
    {
        "number": "Topic 110",
        "questions": [
            "Part 2: Describe a party that you enjoyed. You should say: - When and where the party was held - Who attended the party - What kind of party it was - What you did in the party - And explain why you enjoyed this party",
            "Part 3: Why do people like parties? Why do some people not like going to parties? Do you think those who tend to stay at home are less healthy than those who often attend parties? Do you think music and dancing are a must at a party? What would you do if you were disturbed by a neighbour’s party? What are the differences between holding a party at home and in a public place?"
        ]
    },
    {
        "number": "Topic 111",
        "questions": [
            "Part 2: Describe a place in your country that you think is interesting. You should say: - Where it is - How you knew it - What special features it has - And explain why you think it is interesting",
            "Part 3: How can people access travel information? Do people have different personalities in different regions of your country? What causes the differences between different regions of your country? Is it just youngsters who like to try new things, or do people of your parents' age also like to try new things? Is a great tourist destination also a good place to live? Why do people who go to live in small towns think these towns are more interesting than the big cities?"
        ]
    },
    {
        "number": "Topic 112",
        "questions": [
            "Part 2: Describe a historical period/moment you would like to learn more about. You should say: - What you are interested in - When it happened - What you know about it - And why you would like to learn more",
            "Part 3: Should everyone know history? In what ways can children learn history? What are the differences between learning history from books and from videos? Is it difficult to protect and preserve historic buildings? Who should be responsible for protecting historic buildings? Who should pay for the preservation of historic buildings?"
        ]
    }
]


def select_random_topics(part, num_topics):
    selected_topics = []

    if part == 1:
        part_topics = topics[:49]  # Part 1 的主题范围
        while len(selected_topics) < num_topics:
            random_index = random.randint(0, len(part_topics) - 1)
            selected_topics.append(part_topics.pop(random_index))
    elif part in (2, 3):
        part_topics = topics[50:]  # Part 2 和 3 的主题范围
        random_index = random.randint(0, len(part_topics) - 1)
        selected_topics.append(part_topics[random_index])

    return [{"number": topic["number"], "questions": topic["questions"]} for topic in selected_topics]


async def get_topics_and_questions() -> str:
    part = 0
    num = 3

    data = ""

    if part in (1, 0):
        num_topics_part1 = int(num) if part == 1 and num else 3  # 默认Part 1选择3个主题
        topics_part1 = select_random_topics(1, num_topics_part1)
        for topic in topics_part1:
            questions = "\n".join(topic['questions'])
            data += f"Part 1 Topics: {topic['number']}\nQuestions:\n{questions}\n\n"

    if part in (2, 3, 0):
        num_topics_part2and3 = 1  # Part 2 和 3 总是选择1个主题
        topic_part2and3 = select_random_topics(2, num_topics_part2and3)
        for topic in topic_part2and3:
            questions = "\n".join(topic['questions'])
            data += f"Part 2&3 Topic: {topic['number']}\nQuestions:\n{questions}\n\n"

    logger.info(f"function call <get_topics_and_questions> data={data}")
    return data
