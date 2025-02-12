import random
import logging
from ..logger import setup_logger

# Set up the logger with color and timestamp support
logger = setup_logger(name=__name__, log_level=logging.INFO)

topics = [
    {
        "number": "Topic 1: Study",
        "questions": [
            "Do you work or are you a student?",
            "What subject are you studying?",
            "Why did you choose that subject?",
            "What would you like to do in the future?",
            "What are the most popular subjects in China?",
            "Do you think it's important to choose a subject you like?",
            "Are you looking forward to working?",
            "Do you like your subject? (Why? / Why not?)",
            "Do you prefer to study in the mornings or in the afternoons?",
            "Is your subject interesting to you?",
            "Is there any kind of technology you can use in study?"
        ]
    },
    {
        "number": "Topic 2: Work",
        "questions": [
            "What work do you do?",
            "Why did you choose to do that type of job?",
            "Do you like your job?",
            "Do you miss being a student?",
            "Is it very interesting?",
            "Is there any kind of technology you use at work?",
            "Can you manage your time well when you work?",
            "Who helps you most at work?"
        ]
    },
    {
        "number": "Topic 3: Hometown",
        "questions": [
            "Has your hometown changed much these years?",
            "Is that a big city or a small place?",
            "How long have you been living here?",
            "For you, what benefits are there living in a big city?",
            "Is there anything you dislike about it?",
            "What do you like most about your hometown?",
            "Where in your country do you live?"
        ]
    },
    {
        "number": "Topic 4: Accommodation",
        "questions": [
            "Are the transport facilities in your city very good?",
            "Which room does your family spend most of the time in?",
            "Do you live in a house or a flat?",
            "Do you plan to live here for a long time?",
            "Do you live alone or with your family?",
            "How long have you lived there?",
            "What do you usually do in your house/flat/room?",
            "Which is your favourite room in your home?",
            "What's the difference between where you are living now and where you lived in the past?",
            "What can you see when you look out the window of your room?",
            "Would you be willing to live in the countryside in the future?"
        ]
    },
    {
        "number": "Topic 5: The area you live in",
        "questions": [
            "Do you like the area that you live in now?",
            "Do you think the area you live in now is suitable for people of all ages?",
            "Are people in your area friendly?",
            "How has your area changed in recent years?",
            "Do you know any famous people in your area?",
            "Where do you like to go in your area?"
        ]
    },
    {
        "number": "Topic 6: Feeling bored",
        "questions": [
            "Do you often feel bored?",
            "What kinds of things would make you feel bored?",
            "What will you do if you feel bored?",
            "Do you think childhood is boring or adulthood is boring?"
        ]
    },
    {
        "number": "Topic 7: Old buildings",
        "questions": [
            "Have you ever seen some old buildings in your city?",
            "Do you think we should keep old buildings in cities?",
            "Would you prefer living in an old building or a modern house?"
        ]
    },
    {
        "number": "Topic 8: Lost and found",
        "questions": [
            "What will you do if you find something lost by others?",
            "Have you ever lost anything?",
            "Will you post on social media if you lose your items?"
        ]
    },
    {
        "number": "Topic 9: Mobile phones",
        "questions": [
            "Do you remember your first mobile phone?",
            "Do you often use your mobile phone for texting or making phone calls?",
            "How has your mobile phone changed your life?",
            "Will you buy a new one in the future?"
        ]
    },
    {
        "number": "Topic 10: Emails",
        "questions": [
            "Do you often send emails?",
            "Is sending emails popular in China?",
            "Do you think sending emails will be more or less popular in the future?"
        ]
    },
    {
        "number": "Topic 11: Evening time",
        "questions": [
            "Do you like morning or evening?",
            "What do you usually do in the evening?",
            "Are there any differences between what you do in the evening now and what you did in the past?"
        ]
    },
    {
        "number": "Topic 12: Computers",
        "questions": [
            "In what conditions would you use a computer?",
            "When was the first time you used a computer?",
            "What will your life be like without computers?",
            "In what conditions would it be difficult for you to use a computer?"
        ]
    },
    {
        "number": "Topic 13: Talents",
        "questions": [
            "Do you have a talent, or something you are good at?",
            "Do you think your talent can be useful for your future work?",
            "Do you think people in your family have the same talent?"
        ]
    },
    {
        "number": "Topic 14: Mirrors",
        "questions": [
            "Do you like looking at yourself in the mirror?",
            "Have you ever bought mirrors?",
            "Do you usually take a mirror with you?",
            "Would you use mirrors to decorate your room?"
        ]
    },
    {
        "number": "Topic 15: Daily routines",
        "questions": [
            "What is your daily routine?",
            "Have you ever changed your routine?",
            "Which part of your daily routine do you like best?"
        ]
    },
    {
        "number": "Topic 16: Art",
        "questions": [
            "Do you like art?",
            "Have you ever visited an art gallery?",
            "Is there any artwork on the wall in your room?",
            "Did you learn drawing when you were a kid?"
        ]
    },
    {
        "number": "Topic 17: Advertisements",
        "questions": [
            "What kinds of advertisements do you watch?",
            "Where can you see advertisements?",
            "Have you ever bought something because of its advertisement?",
            "Do you watch advertisements from the beginning to the end?"
        ]
    },
    {
        "number": "Topic 18: Dreams",
        "questions": [
            "Do you often remember your dreams?",
            "Are you interested in others’ dreams?",
            "Do you want to make your dreams come true?"
        ]
    },
    {
        "number": "Topic 19: Watches",
        "questions": [
            "Do you wear a watch?",
            "Have you ever got a watch as a gift?",
            "Why do some people wear expensive watches?"
        ]
    },
    {
        "number": "Topic 20: Swimming",
        "questions": [
            "Do you like swimming?",
            "Is it difficult to learn how to swim?",
            "Where do people usually go swimming in your country?",
            "What is the difference between swimming in the pool and swimming in the sea?"
        ]
    },
    {
        "number": "Topic 21: Car trip",
        "questions": [
            "Do you like to travel by car?",
            "Where is the farthest place you traveled to by car?",
            "Do you like to sit in the front or back when travelling by car?"
        ]
    },
    {
        "number": "Topic 22: Websites",
        "questions": [
            "What kinds of websites do you usually use?",
            "What is your favorite website?",
            "Are there any changes about the websites you usually use?",
            "What kinds of websites are popular in your country?"
        ]
    },
    {
        "number": "Topic 23: Street market",
        "questions": [
            "What do street markets sell?",
            "Do you prefer to go shopping in the shopping mall or the street market?",
            "When was the last time you went to a street market?",
            "Are there many street markets in China?"
        ]
    },
    {
        "number": "Topic 24: Reading",
        "questions": [
            "When do you read books?",
            "How often do you buy books?",
            "Have you ever read a novel that has been adapted into a film?",
            "Which one do you prefer, reading books or watching movies?"
        ]
    },
    {
        "number": "Topic 25: Collecting things",
        "questions": [
            "Do you collect anything?",
            "Are there any things you keep from childhood?",
            "Where do you usually keep things you collect?"
        ]
    },
    {
        "number": "Topic 26: Time management",
        "questions": [
            "Do you make plans every day?",
            "Is it easy to manage time?",
            "Do you think it’s useful to plan your time?",
            "Do you like being busy?"
        ]
    },
    {
        "number": "Topic 27: History",
        "questions": [
            "Have you ever been to a history museum?",
            "Do you like history?",
            "Have you ever watched historical films?",
            "Did you like history when you were young?",
            "When was the last time you read about history?"
        ]
    },
    {
        "number": "Topic 28: Sitting down",
        "questions": [
            "Where is your favorite place to sit?",
            "Do you always sit down for a long time?",
            "Do you feel sleepy after you sit down for a while?"
        ]
    },
    {
        "number": "Topic 29: Sports",
        "questions": [
            "What kind of sport did you do when you were young?",
            "Do you like watching athletic sports?",
            "Have you joined any sports team?",
            "Do you think there are too many athletic sports on TV now?",
            "Do you like watching sports programs on TV?",
            "Do you watch live sports games?",
            "Who do you like to watch sports games with?",
            "What kinds of games do you expect to watch in the future?"
        ]
    },
    {
        "number": "Topic 30: Cinema",
        "questions": [
            "Did you often go to the cinema when you were a child?",
            "Do you often go to the cinema with your friends?",
            "Do you still like the same kind of movie which you liked when you were a child?",
            "What genres of films do you like?",
            "Do you think going to the cinema is a good way to spend time with friends?"
        ]
    },
    {
        "number": "Topic 31: Riding Bikes",
        "questions": [
            "Did you have a bike when you were young?",
            "Did/Do you go to school by bike?",
            "Will you choose to ride a bike if you go out these days?",
            "Do you have a bike now?",
            "Do you often ride a bike now?",
            "Are bikes popular in China?"
        ]
    },
    {
        "number": "Topic 32: Roads",
        "questions": [
            "Are the roads in the area where you live busy?",
            "How do people cross the road in the city where you live?",
            "How is the condition of the roads in your city?",
            "Do you think the roads in your city need improvement?"
        ]
    },
    {
        "number": "Topic 33: Laughter",
        "questions": [
            "Do you like to watch movies or TV shows that make people laugh?",
            "Do you usually make your friends laugh?",
            "Have you laughed recently? Why?"
        ]
    },
    {
        "number": "Topic 34: Coins",
        "questions": [
            "Do you often take coins out with you?",
            "Have you ever collected coins?",
            "Is it convenient to use coins today?",
            "Do you use coins in your daily life?"
        ]
    },
    {
        "number": "Topic 35: Perfume",
        "questions": [
            "Do you like to use perfume?",
            "How often do you wear perfume?",
            "What kind of perfume do you like to wear?",
            "Have you ever given a perfume as a gift?"
        ]
    },
    {
        "number": "Topic 36: Fishing",
        "questions": [
            "Do you like eating fish?",
            "Is fishing popular in your country?",
            "Have you ever been to a place where there are lots of fish around you?",
            "Have you seen any movies featuring lots of fish?",
            "Why do some people like fishing?",
            "Where can you see fish?"
        ]
    },
    {
        "number": "Topic 37: Scenery",
        "questions": [
            "What kinds of beautiful scenery are there around your hometown?",
            "When you travel, do you like to stay in hotels with scenic views?",
            "Do people like to take photos of beautiful scenery?",
            "Why do people prefer to take photos of beautiful scenery with smartphones?"
        ]
    },
    {
        "number": "Topic 38: Teamwork",
        "questions": [
            "Do you like teamwork?",
            "Have you worked with a team or someone else?",
            "What do you think are the benefits of working together, in teams?",
            "What do you hate when working together with others?"
        ]
    },
    {
        "number": "Topic 39: Making friends",
        "questions": [
            "Do you like making friends?",
            "Did you make a lot of friends when you were a child?",
            "Have you made any new friends recently?",
            "What do you often talk about with your friends?",
            "Do you like meeting new people?",
            "Where can you meet new people?"
        ]
    },
    {
        "number": "Topic 40: Talking with others",
        "questions": [
            "What is your daily routine?",
            "Have you ever changed your routine?",
            "Which part of your daily routine do you like best?"
        ]
    },
    {
        "number": "Topic 41: Taking photos",
        "questions": [
            "Do you like to take photographs?",
            "Do you ever take photos of yourself?",
            "What is your favorite family photo?",
            "Do you want to improve your picture-taking skills?"
        ]
    },
    {
        "number": "Topic 42: Free time",
        "questions": [
            "What do you like to do in your spare time?",
            "How much time do you have each week for doing these things?",
            "Why do you like doing these activities?",
            "How did you start doing this activity at first?"
        ]
    },
    {
        "number": "Topic 43: Teachers",
        "questions": [
            "Did you want to be a teacher when you were younger?",
            "Do you remember your teachers from primary school?",
            "Do you have a favorite teacher?",
            "What kind of teacher do you prefer?"
        ]
    },
    {
        "number": "Topic 44: Science",
        "questions": [
            "Do you like science?",
            "When did you start to learn about science?",
            "What is your favourite subject of science?",
            "What kinds of interesting things have you done with science?",
            "Do you like watching science TV programs?",
            "Do Chinese people often visit science museums?"
        ]
    },
    {
        "number": "Topic 45",
        "questions": [
            "Part 2: Describe a person who is full of energy. You should say: - Who he or she is - What he or she does - Why he or she is full of energy - And explain how you feel about this person",
            "Part 3: What kind of jobs require a lot of energy? Do you think manual work will all be done by machines in the future? Do you think manual workers will earn more in the future?"
        ]
    },
    {
        "number": "Topic 46",
        "questions": [
            "Part 2: Describe someone you really like to spend time with. You should say: - Who he/she is - How you knew him/her - What you usually do together - And explain why you like to spend time with him/her",
            "Part 3: What qualities make someone a good friend? How important is friendship in life? Do you think friendships are easier to maintain now than in the past? What role do social media play in friendships?"
        ]
    },
    {
        "number": "Topic 47",
        "questions": [
            "Part 2: Describe a person who makes a contribution to society. You should say: - Who this person is - How you knew him/her - What type of work he/she does - And explain why you think he/she contributes to the society",
            "Part 3: What kinds of jobs are well-paid? What changes in working conditions have you noticed in your country in recent years? Do you think younger people should be less paid than older people?"
        ]
    },
    {
        "number": "Topic 48",
        "questions": [
            "Part 2: Describe an interesting neighbor. You should say: - Who this person is - How you know this person - What he or she does - And explain why you think this person is interesting",
            "Part 3: Do you have a good relationship with your neighbours? How can we improve our relationships with neighbours? Do you think neighbours are important? Do you think people's relationships with their neighbours today is the same as it was in the past?"
        ]
    },
    {
        "number": "Topic 49",
        "questions": [
            "Part 2: Describe a popular person. You should say: - Who he/she is - What he/she has done - Why he/she is popular - And explain how you feel about him/her",
            "Part 3: Why do some students want to become popular? What kinds of people are more popular at school? Do you think a good teacher should become popular? Why are some celebrities not popular?"
        ]
    },
    {
        "number": "Topic 50",
        "questions": [
            "Part 2: Describe a person you follow on social media. You should say: - Who he/she is - How you knew him/her - What he/she posts on social media - And explain why you follow him/her on social media",
            "Part 3: Do you think old people and young people use the same kind of social media app? Do old people spend much time on social media? What can people do on social media? Are television and newspapers still useful?"
        ]
    },
    {
        "number": "Topic 51",
        "questions": [
            "Part 2: Describe a family member you want to work with in the future. You should say: - Who he/she is - What he/she does - What kind of work you would like to do with him/her - And explain how you feel about him/her",
            "Part 3: What kinds of family businesses are common in China? Why do people want to do family business? What are the benefits of working with family members? Is it easier to get promotion in big companies?"
        ]
    },
    {
        "number": "Topic 52",
        "questions": [
            "Part 2: Describe a person who always has strong opinions. You should say: - Who this person is - How you knew him/her - Why you think he/her is an opinionated person - And explain how you feel about him/her",
            "Part 3: What aspects do young people have strong opinions about? What aspects do old people have strong opinions about? Are children’s opinions influenced by their parents?"
        ]
    },
    {
        "number": "Topic 53",
        "questions": [
            "Part 2: Describe a person who has chosen a career in the medical field (e.g. a doctor, a nurse). You should say: - Who her/she is - What he/she does - Why he/she chose this career - And explain how you feel about him/her",
            "Part 3: Do you think doctors and nurses are very important? Who is more important, doctors or nurses? Do you think that doctors and nurses are not paid enough? Do you think it is necessary to learn first aid skills?"
        ]
    },
    {
        "number": "Topic 54",
        "questions": [
            "Part 2: Describe a person who likes to read a lot. You should say: - Who this person is - How you knew him/her - What he/she likes to read - And explain why you think he/she likes to read a lot",
            "Part 3: Why are many people so keen on reading? Do you think parents should help their children develop the reading habit from an early age? Is reading for fun or for work?"
        ]
    },
    {
        "number": "Topic 55",
        "questions": [
            "Part 2: Describe a person who likes to make things by hand (e.g. toys, furniture). You should say: - Who this person is - What he/she makes - Why he/she likes to make things by hand - And explain how you feel about the person",
            "Part 3: Are traditional handicrafts important to tourism? What are the benefits for students to learn to make things by hand? Why do many children like to make things by hand? How important are traditional handicrafts to a country's industry? Is it reasonable to charge a high price for handmade things? How does modern technology change the handicraft industry?"
        ]
    },
    {
        "number": "Topic 56",
        "questions": [
            "Part 2: Describe a person from whom others like to ask for advice. You should say: - Who this person is - Why people like to ask for his/her advice - What kind of advice he/she often gives - And explain how you felt about the person",
            "Part 3: Do you follow the advice of your family members? Who should people ask for advice on big issues, family members or friends? Do people often ask for advice from professional people, like a lawyer? Why do some people like to ask others for advice on almost everything? Do you think the advice parents give their children is always good? Are professional consultancy services expensive in your country?"
        ]
    },
    {
        "number": "Topic 57",
        "questions": [
            "Part 2: Describe something you received for free. You should say: - What it was - Who you received it from - Why you received it for free - And explain how you felt about it",
            "Part 3: Do you think people should pay for higher education by themselves? What free gifts do companies usually give to their customers? Why do customers like to receive free gifts from companies?"
        ]
    },
    {
        "number": "Topic 58",
        "questions": [
            "Part 2: Describe a product you bought but you returned in the end. You should say: - What it is - When you bought it - Why you returned it - And explain how you felt about it",
            "Part 3: Is it common for people to return products they bought? What factors influence a customer's decision to return a product? How do stores handle returned products?"
        ]
    },
    {
        "number": "Topic 59",
        "questions": [
            "Part 2: Describe a traditional product in your country. You should say: - What it is - When you tried this product for the first time - What it is made of - And explain how important this product is",
            "Part 3: Do young people admire traditional products? Why is it important for children to learn about traditional products? Does the government have responsibility to protect traditional products? Do you think traditional products have better quality than modern products?"
        ]
    },
    {
        "number": "Topic 60",
        "questions": [
            "Part 2: Describe a kind of food people eat during a special event. You should say: - What the food is - What event people usually eat it - How it is cooked - And explain why it is for the special event.",
            "Part 3: Why do some people grow their own food these days? Is there any traditional food in your country? What can be the reasons that some young people prefer to have foreign food than having traditional food? Which food is generally popular in your country? Will there be more and more people planting food in the future?"
        ]
    },
    {
        "number": "Topic 61",
        "questions": [
            "Part 2: Describe a photo that is special to you. You should say: - When and where it was taken - Who are in the photo - Why it is special to you - And explain whether you will keep it for a long time",
            "Part 3: Who would take photos more often, young people or older people? What do young people and old people like to take photos of? Why do some people pay a ton of money to hire professional photographers to take photos at some special occasions, such as weddings?"
        ]
    },
    {
        "number": "Topic 62",
        "questions": [
            "Part 2: Describe the most expensive item you have ever bought. You should say: - When and where you bought it - What it was - What you used it for - And explain how you liked it",
            "Part 3: Do people spend too much time shopping these days? Why?"
        ]
    },
    {
        "number": "Topic 63",
        "questions": [
            "Part 2: Describe a piece of technology you own that you feel difficult to use. You should say: - What it is - When you got it - How often you use it - And explain how you feel about it",
            "Part 3: What technological products do people currently use? Why do big companies introduce new products frequently? Why are people so keen on buying iPhones even though they haven’t changed much? Does the development of technology affect the way we study?"
        ]
    },
    {
        "number": "Topic 64",
        "questions": [
            "Part 2: Describe a toy you got in your childhood. You should say: - What it was - When you got it - How you got it - And explain how you felt about it.",
            "Part 3: Why do some people think advertising aimed at children should be prohibited? Why do you think some parents buy lots of toys for their kids instead of spending more time with them? What are some of the differences between the toys kids play with nowadays and those they used to play with in the past?"
        ]
    },
    {
        "number": "Topic 65",
        "questions": [
            "Part 2: Describe a gift you would like to buy for your friend. You should say: - What gift you would like to buy - Who you would like to give it to - Why you want to buy this gift for him/her - And explain why you would like to choose that gift",
            "Part 3: When do people send gifts to others? Do people give gifts or red packets on traditional festivals? Is it hard to choose a gift? Will people feel happy when receiving an expensive gift?"
        ]
    },
    {
        "number": "Topic 66",
        "questions": [
            "Part 2: Describe a piece of clothing that someone gave you. You should say: - What it is - Who gave it to you - When you got it - And explain why this person gave you this piece of clothing",
            "Part 3: Why do people dress casually in daily life and dress formally at work? What are the advantages and disadvantages of wearing a uniform at work and school? Why do people from different countries wear different clothes?"
        ]
    },
    {
        "number": "Topic 67",
        "questions": [
            "Part 2: Describe something you cannot live without (not a computer/phone). You should say: - What it is - What you do with it - How it helps you in your life - And explain why you cannot live without it",
            "Part 3: Why are children attracted to electronic devices? Why do some adults hate to throw away old things, such as clothes? What do you think influences people to buy new things?"
        ]
    },
    {
        "number": "Topic 68",
        "questions": [
            "Part 2: Describe your grandfather/grandmother’s job. You should say: - What job he/she does - What you know about his/her job - Whether it is his/her only job - And explain how you feel about his/her job",
            "Part 3: How do people generally feel about their grandparents' jobs? What impact do grandparents' professions have on their grandchildren?"
        ]
    },
    {
        "number": "Topic 69",
        "questions": [
            "Part 2: Describe an online video where you learned something new. You should say: - When and where you watched it - What it was - Why you watched it - And explain what you learned from it",
            "Part 3: What kinds of videos are most popular in your country? Are there many people who watch online videos a lot? Do you think people spend too much time watching short videos? Why are so many young people obsessed with short videos?"
        ]
    },
    {
        "number": "Topic 70",
        "questions": [
            "Part 2: Describe a movie you watched recently. You should say: - When and where you watched it - Who you watched it with - What it was about - And explain why you chose to watch this movie",
            "Part 3: What kinds of movies do you think are successful in your country? What are the factors that make a successful movie? Do Chinese people prefer to watch domestic movies or foreign movies?"
        ]
    },
    {
        "number": "Topic 71",
        "questions": [
            "Part 2: Describe a good service you received. You should say: - What the service was - When you received it - Who you were with - And explain how you felt about it",
            "Part 3: What do you think of the relationship between companies and customers? As a customer, what kinds of services would you expect to receive from a company? Why should companies react quickly when customers have difficulties?"
        ]
    },
    {
        "number": "Topic 72",
        "questions": [
            "Part 2: Describe something that helps you to focus on study/work. You should say: - What it is - How often you do it - When you start doing it - And explain how it helps you concentrate",
            "Part 3: Do you think children need to have routines? Do you think routines are important for companies? What are the routine activities that old people and young people do in your country?"
        ]
    },
    {
        "number": "Topic 73",
        "questions": [
            "Part 2: Describe an ambition that you haven’t achieved. You should say: - What it is - Why you haven’t achieved it - What you have already done - And explain how you felt about it",
            "Part 3: What ambitions do children usually have? Why are some people very ambitious at work? Why do some people not have any dreams?"
        ]
    },
    {
        "number": "Topic 74",
        "questions": [
            "Part 2: Describe a song or piece of music you like. You should say: - What the song or music is - What kind of song or music it is - Where you first heard it - And explain why you like it",
            "Part 3: Do you think young people and old people enjoy the same kind of music? Why are many music competitions popular in China? What are the differences between live concerts and online concerts?"
        ]
    },
    {
        "number": "Topic 75",
        "questions": [
            "Part 2: Describe something that helped you learn a foreign language. You should say: - What it was - What language you learnt - Why you chose to learn that language - And explain how this thing helped you",
            "Part 3: What difficulties do people face when learning a language? Do you think language learning is important? Is studying abroad a good way to learn a foreign language?"
        ]
    },
    {
        "number": "Topic 76",
        "questions": [
            "Part 2: Describe a rule that you would like to change. You should say: - What it is - Why you want to change it - How others feel about the rule - And explain whether you have followed the rule",
            "Part 3: What kind of rules do schools in China have? What rules should children follow at home? Do people often violate the rules in China?"
        ]
    },
    {
        "number": "Topic 77",
        "questions": [
            "Part 2: Describe a story someone told you and you remember. You should say: - What the story was about - Who told you this story - Why you remember it - And explain how you feel about it",
            "Part 3: Do young children like the same stories as older children? How has technology changed the way of storytelling? Why do children like stories?"
        ]
    },
    {
        "number": "Topic 78",
        "questions": [
            "Part 2: Describe a foreign country you would like to go in the future. You should say: - Where it is - What it is famous for - What you can do there - And explain why you want to go there",
            "Part 3: What attracts tourists to your country? How important is it for people to travel abroad? What can people learn from traveling?"
        ]
    },
    {
        "number": "Topic 79",
        "questions": [
            "Part 2: Describe a place in the countryside that you visited. You should say: - Where it is - When you visited this place - What you did there - And explain how you feel about this place",
            "Part 3: Is there anything special about the countryside in China? What do people usually do when going to the countryside? Do you think more people will live in the countryside in the future?"
        ]
    },
    {
        "number": "Topic 80",
        "questions": [
            "Part 2: Describe an important river/lake in your country. You should say: - Where it is - How big/long it is - What it looks like - And explain why it is important",
            "Part 3: How can rivers/lakes benefit local people? How do rivers/lakes affect local tourism? Are rivers/lakes useful for transport?"
        ]
    },
    {
        "number": "Topic 81",
        "questions": [
            "Part 2: Describe a quiet place where you like to spend your time. You should say: - Where it is - How often you go there - What you do there - And explain how you feel about this place",
            "Part 3: Is it hard to find quiet places in cities? Why is it quieter in the countryside? Compared with young people, do old people prefer to live in quiet places?"
        ]
    },
    {
        "number": "Topic 82",
        "questions": [
            "Part 2: Describe a cultural place (e.g. library, museum, theatre). You should say: - Where it is - How you knew this place - What it is like - And explain how the place is related to culture",
            "Part 3: How does the internet affect culture? How is a culture formed? What kind of culture is popular among the young?"
        ]
    },
    {
        "number": "Topic 83",
        "questions": [
            "Part 2: Describe an ideal and perfect place where you would like to stay, e.g. a house or an apartment. You should say: - Where it would be - What it would look like - What special features it would have - And explain why it would be an ideal place for you",
            "Part 3: What are apartments like in your country? Why are apartments welcome in some places while not in other places? What would people normally consider when they rent or buy a house or an apartment?"
        ]
    },
    {
        "number": "Topic 84",
        "questions": [
            "Part 2: Describe a place in your hometown/city that is different from other places and you would like to visit with your parents/friends. You should say: - Where it is - Why you think it is different - Who you would like to go with - And explain whether you have been there",
            "Part 3: What are the differences between big cities and small cities? Where do people in your hometown like to go? What are the differences between the places young people like to go and the places old people like to go?"
        ]
    },
    {
        "number": "Topic 85",
        "questions": [
            "Part 2: Describe a positive change you made in your life. You should say: - What the change was - When it happened - How it happened - And explain why it was a positive change",
            "Part 3: Is it easier for young people to change? What are the disadvantages when people keep making changes in life? What are some of the major changes that occur to people throughout their lives?"
        ]
    },
    {
        "number": "Topic 86",
        "questions": [
            "Part 2: Describe a time that the vehicle broke down during your travel. You should say: - When and where it happened - Who you were with at that time - How you dealt with the broken vehicle - And explain what the impact this breakdown had.",
            "Part 3: What are the advantages and disadvantages of private transport? What do you think needs to be improved in public transport? Will there be fewer people using private cars because of the improved public transport?"
        ]
    },
    {
        "number": "Topic 87",
        "questions": [
            "Part 2: Describe a thing you once forgot to do. You should say: - What it is - When you forgot it - Why you forgot it - And explain how you felt about this experience",
            "Part 3: How can we strengthen our memory? What kind of people might easily forget things? What kind of things do people often forget?"
        ]
    },
    {
        "number": "Topic 88",
        "questions": [
            "Part 2: Describe a time you visited a new place. You should say: - Where it is - When you went there - Why you went there - And explain how you feel about the place",
            "Part 3: Which one do you prefer, living in a city or only visiting one as a tourist? How do children react when they go to a new school for the first time? How do young and old people react differently to new things?"
        ]
    },
    {
        "number": "Topic 89",
        "questions": [
            "Part 2: Describe an occasion you had a special cake. You should say: - When this happened - Where this happened - Who gave you the cake - And explain why it was a special cake",
            "Part 3: What’s the difference between special food in China and foreign countries? Do Chinese people usually cook special food in traditional festivals? Do Chinese families like to eat together during traditional holidays?"
        ]
    },
    {
        "number": "Topic 90",
        "questions": [
            "Part 2: Describe a time when you were caught in a traffic jam. You should say: - When it happened - Where it happened - How you passed the time while waiting - And explain how you felt when you were in that traffic jam",
            "Part 3: When do traffic jams usually happen? What are the causes of traffic jams? Do you think the problem of traffic congestion will be eased in the future or will it become worse?"
        ]
    }
]


def select_random_topics(part, num_topics):
    selected_topics = []

    last_part1_index = 49

    if part == 1:
        part_topics = topics[:last_part1_index]  # Part 1 的主题范围
        while len(selected_topics) < num_topics:
            random_index = random.randint(0, len(part_topics) - 1)
            selected_topics.append(part_topics.pop(random_index))
    elif part in (2, 3):
        part_topics = topics[last_part1_index+1:]  # Part 2 和 3 的主题范围
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
