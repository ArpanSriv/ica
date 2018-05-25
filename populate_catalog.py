import datetime

import time
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker
from flask import url_for

from database_setup import Base, Item, Category, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

session.query(Item).delete()
session.query(Category).delete()
session.query(User).delete()

categories = {
    'Soccer': {
        'Ball': {
            'description': "A football, soccer ball, or association football ball is the ball used in the sport of "
                           "association football. The name of the ball varies according to whether the sport is "
                           "called 'football', 'soccer', or 'association football'. The ball's spherical shape, "
                           "as well as its size, weight, and material composition, are specified by Law 2 of the Laws "
                           "of the Game maintained by the International Football Association Board. Additional, "
                           "more stringent, standards are specified by FIFA and subordinate governing bodies for the "
                           "balls used in the competitions they sanction.",
            'creation_time': time.time(),
            'category_id': 1,
            'user_id': 1,
            'picture': "https://images.pexels.com/photos/47730/the-ball-stadion-football-the-pitch-47730.jpeg?cs=srgb&dl=ball-field-football-47730.jpg&fm=jpg"
        },

        'Football Shoes': {
            'description': 'Football boots, called cleats or soccer shoes in North America, are an item of '
                           'footwear worn when playing football. Those designed for grass pitches have studs on the '
                           'outsole to aid grip. From simple and humble beginnings football boots have come a long '
                           'way and today find themselves subject to much research, development, sponsorship and '
                           'marketing at the heart of a multi-national global industry. Modern "boots" are not truly '
                           'boots in that they do not cover the ankle - like most other types of specialist sports '
                           'footwear, their basic design and appearance has converged with that of sneakers since the '
                           '1960s.',
            'creation_time': time.time(),
            'category_id': 1,
            'user_id': 1,
            'picture': "https://images.pexels.com/photos/274385/pexels-photo-274385.jpeg?cs=srgb&dl=boots-brand-championship-274385.jpg&fm=jpg"
        },

        'picture': "https://images.pexels.com/photos/47730/the-ball-stadion-football-the-pitch-47730.jpeg?cs=srgb&dl=ball-field-football-47730.jpg&fm=jpg"
    },
    'Basketball': {
        'Backboard': {
            'description': "A backboard is a piece of basketball equipment. It is a raised vertical board with an "
                           "attached basket consisting of a net suspended from a hoop. It is made of a flat, "
                           "rigid piece of, often Plexiglas or tempered glass which also has the properties of safety "
                           "glass when accidentally shattered. It is usually rectangular as used in NBA, "
                           "NCAA and international basketball. In recreational environments, a backboard may be oval "
                           "or a fan-shape, particularly in non-professional games. The top of the hoop is 10 feet ("
                           "305 cm) above the ground. Regulation backboards are 72 inches (183 cm) wide by 42 inches "
                           "(110 cm) tall. All basketball rims (hoops) are 18 inches (46 cm) in diameter. The inner "
                           "rectangle on the backboard is 24 inches (61 cm) wide by 18 inches (46 cm) tall. In "
                           "professional and most higher college settings, the backboard is part of a portable "
                           "stanchion that can be moved out of the way in other sports, though in most high schools "
                           "and examples such as Stanford University's Maples Pavilion, backboards are mounted as "
                           "part of a suspended system using ceiling joists to support the goal and allow them to be "
                           "put out of the way in the ceiling when not in use.",
            'creation_time': time.time(),
            'category_id': 2,
            'user_id': 1,
            'picture': "https://images.pexels.com/photos/264258/pexels-photo-264258.jpeg?cs=srgb&dl=action-active-activity-264258.jpg&fm=jpg"
        },

        'Ball': {
            'description': "A basketball (basketball ball) is a spherical ball used in basketball games. Basketballs "
                           "typically range in size from very small promotional items only a few inches in diameter "
                           "to extra large balls nearly a foot in diameter used in training exercises. For example, "
                           "a youth basketball could be 27 inches (69 cm) in circumference, while an NCAA men's ball "
                           "would be a maximum of 30 inches (76 cm) and an NCAA women's ball would be a maximum of 29 "
                           "inches (74 cm). The standard for a basketball in the NBA is 29.5 inches (75 cm) in "
                           "circumference and for the WNBA, a maximum circumference of 29 inches (74 cm). High school "
                           "and junior leagues normally use NCAA, NBA or WNBA sized balls.",
            'creation_time': time.time(),
            'category_id': 2,
            'user_id': 1,
            'picture': "https://images.pexels.com/photos/945471/pexels-photo-945471.jpeg?cs=srgb&dl=athletes-ball-basketball-945471.jpg&fm=jpg"
        },

        'Breakaway Rim': {
            'description': "A breakaway rim is a basketball rim that contains a hinge and a spring at the point "
                           "where it attaches to the backboard so that it can bend downward when a player dunks a "
                           "basketball, and then quickly snaps back into a horizontal position when the player "
                           "releases it. It allows players to dunk the ball without shattering the backboard, "
                           "and it reduces the possibility of wrist injuries. Breakaway rims were invented in the "
                           "mid-1970s and are now an essential element of high-level basketball. ",
            'creation_time': time.time(),
            'category_id': 2,
            'user_id': 1,
            'picture': "https://images.pexels.com/photos/976837/pexels-photo-976837.jpeg?cs=srgb&dl=ball-basket-basketball-976837.jpg&fm=jpg"
        },

        'picture': "https://images.pexels.com/photos/264258/pexels-photo-264258.jpeg?cs=srgb&dl=action-active-activity-264258.jpg&fm=jpg"
    },
    'Baseball': {
        'Bat': {
            'description': "A baseball bat is a smooth wooden or metal club used in the sport of baseball to hit the "
                           "ball after it is thrown by the pitcher. By regulation it may be no more than 2.75 inches "
                           "(70 mm) in diameter at the thickest part and no more than 42 inches (1,100 mm) long. "
                           "Although historically bats approaching 3 pounds (1.4 kg) were swung, today bats of 33 "
                           "ounces (0.94 kg) are common, topping out at 34 ounces (0.96 kg) to 36 ounces (1.0 kg).",
            'creation_time': time.time(),
            'category_id': 3,
            'user_id': 1,
            'picture': "https://images.pexels.com/photos/843341/pexels-photo-843341.jpeg?cs=srgb&dl=balls-baseball-baseball-bat-843341.jpg&fm=jpg "
        },

        'Batting Helmet': {
            'description': "A batting helmet is worn by batters in the game of baseball or softball. It is meant to "
                           "protect the batter's head from errant pitches thrown by the pitcher. A batter who is 'hit "
                           "by pitch,' due to an inadvertent wild pitch or a pitcher's purposeful attempt to hit him, "
                           "may be seriously, even fatally, injured.",
            'creation_time': time.time(),
            'category_id': 3,
            'user_id': 1,
            'picture': "https://images.pexels.com/photos/209804/pexels-photo-209804.jpeg?cs=srgb&dl=active-athlete-baseball-209804.jpg&fm=jpg"
        },

        'Ball': {
            'description': "A baseball is a ball used in the sport of the same name, baseball. The ball features a "
                           "rubber or cork center, wrapped in yarn, and covered, in the words of the Official "
                           "Baseball Rules 'with two strips of white horsehide or cowhide, tightly stitched "
                           "together.' It is 9.00–9.25 inches (228.60–234.95 mm) in circumference, (2.86–2.94 in or "
                           "72.64–74.68 mm in diameter), and masses from 5.00 to 5.25 ounces (141.75 to 148.83 g). "
                           "The yarn or string used to wrap the baseball can be up to one mile (1.6 km) in length. "
                           "Some are wrapped in a plastic-like covering.",
            'creation_time': time.time(),
            'category_id': 3,
            'user_id': 1,
            'picture': "https://images.pexels.com/photos/46859/pexels-photo-46859.jpeg?dl&fit=crop&crop=entropy&w=1920&h=1440"
        },

        'picture': "https://images.pexels.com/photos/209804/pexels-photo-209804.jpeg?cs=srgb&dl=active-athlete-baseball-209804.jpg&fm=jpg"
    },
    'Snowboarding': {
        'Snowboard': {
            'description': "Snowboards are the basic equipment for snowboarding and are used for sliding over the "
                           "snow filled surface. Usually the snowboard is made of hard wood core that is sandwiched "
                           "between multiple layers of fibre glass. Other elements like carbon fibre, Kevlar, "
                           "aluminium are also used in the making of a modern snowboard.",
            'creation_time': time.time(),
            'category_id': 5,
            'user_id': 1,
            'picture': "https://images.pexels.com/photos/848599/pexels-photo-848599.jpeg?cs=srgb&dl=action-clouds-cold-848599.jpg&fm=jpg"
        },

        'Snowboard Binding': {
            'description': 'These are specially designed equipment and are attached to the snowboard. The major '
                           'functionality of these bindings is to hold the boot of the rider in proper place in order '
                           'to efficiently transfer the rider’s force into the motion of the board. Based on their '
                           'characteristics, there are three types of bindings which are strap-in, step-in, '
                           'and hybrid bindings.',
            'creation_time': time.time(),
            'category_id': 5,
            'user_id': 1,
            'picture': "https://images.pexels.com/photos/376697/pexels-photo-376697.jpeg?cs=srgb&dl=equipment-ice-ski-376697.jpg&fm=jpg"
        },

        'picture': "https://images.pexels.com/photos/848599/pexels-photo-848599.jpeg?cs=srgb&dl=action-clouds-cold-848599.jpg&fm=jpg"
    }
}

user1 = User(
    id=1,
    name="Dummy User",
    email="dummyisthis@gmail.com",
    picture="https://image.flaticon.com/icons/svg/236/236934.svg"
)

session.add(user1)
session.commit()

for category_name in categories:
    print(category_name)

    category = Category(
        name=category_name,
        user=user1,
        picture=categories.get(category_name).get('picture')
    )

    session.add(category)
    session.commit()

    for item in categories.get(category_name):
        if item != 'picture':
            print("-- {}".format(item))

            items_dict = categories.get(category_name).get(item)

            desc = items_dict.get('description')
            cat_id = items_dict.get('category_id')
            uid = items_dict.get('user_id')
            picture = items_dict.get('picture')

            print("   {} {} {} {}".format(desc, time, cat_id, uid))
            item = Item(name=item,
                        description=desc,
                        creationtime=datetime.datetime.now(),
                        category=category,
                        user=user1,
                        picture=picture)
            session.add(item)
            session.commit()
