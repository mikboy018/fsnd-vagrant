from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from build_db import Users, Items, Categories

engine = create_engine('sqlite:///catelog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

session = DBSession()

# Create Admin User
user1 = Users(name = "Mike B.", email = "boyer.mike.e@gmail.com", admin = True)

session.add(user1)
session.commit()

# Create Category: Sports
category1 = Categories(name = "Sports")

session.add(category1)
session.commit()

# Create Items for Sports Category
item1 = Items(name = "Basketball", description = "A ball to play basketball.", category = category1)

session.add(item1)
session.commit()

# Create Category: Computers
category2 = Categories(name = "Computers")

session.add(category2)
session.commit()

# Create Items for Computers Category
item2 = Items(name = "Laptop", description = "Intel i7, 16 GB ram, 2 TB HDD, NVidia 1070", category = category2)

session.add(item2)
session.commit()

# Create Category: PetSupplies
category3 = Categories(name = "Pet Supplies")

session.add(category3)
session.commit()

# Create Items for PetSupplies Category
item3 = Items(name = "Dog Food", description = "Good for breakfast and dinner!", category = category3)

session.add(item3)
session.commit()


print "Added 3 categories, and 3 items"