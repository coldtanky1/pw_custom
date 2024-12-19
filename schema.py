''' The SQLite schema/model for the bot. '''
from peewee import SqliteDatabase, Model, IntegerField, TextField

db = SqliteDatabase('player_info.db')

# The user_info table
class UserInfo(Model):
    user_id = IntegerField(primary_key=True)
    name = TextField()
    turns_accumulated = IntegerField()
    gov_type = TextField()
    tax_rate = IntegerField()
    conscription = TextField()
    freedom = TextField()
    police_policy = TextField()
    fire_policy = TextField()
    hospital_policy = TextField()
    war_status = TextField()
    happiness = IntegerField()
    corp_tax = IntegerField()

    class Meta:
        database = db

class UserStats(Model):
    name = TextField(primary_key=True)
    nation_score = IntegerField()
    gdp = IntegerField()
    adult = IntegerField()
    balance = IntegerField()

    class Meta:
        database = db

class UserMil(Model):
    name = TextField(primary_key=True)
    troops = IntegerField()
    planes = IntegerField()
    tanks = IntegerField()
    artillery = IntegerField()
    anti_air = IntegerField()
    barracks = IntegerField()
    # Mil production
    tank_factory = IntegerField()
    plane_factory = IntegerField()
    artillery_factory = IntegerField()
    anti_air_factory = IntegerField()

    class Meta:
        database = db

class Infra(Model):
    name = TextField(primary_key=True)
    basic_house = IntegerField()
    small_flat = IntegerField()
    apt_complex = IntegerField()
    skyscraper = IntegerField()
    lumber_mill = IntegerField()
    coal_mine = IntegerField()
    iron_mine = IntegerField()
    lead_mine = IntegerField()
    bauxite_mine = IntegerField()
    oil_derrick = IntegerField()
    uranium_mine = IntegerField()
    farm = IntegerField()
    aluminium_factory = IntegerField()
    steel_factory = IntegerField()
    oil_refinery = IntegerField()
    ammo_factory = IntegerField()
    concrete_factory = IntegerField()
    militaryfactory = IntegerField()
    corps = IntegerField()
    park = IntegerField()
    cinema = IntegerField()
    museum = IntegerField()
    concert_hall = IntegerField()

    class Meta:
        database = db

class Resources(Model):
    name = TextField(primary_key=True)
    wood = IntegerField()
    coal = IntegerField()
    iron = IntegerField()
    lead = IntegerField()
    bauxite = IntegerField()
    oil = IntegerField()
    uranium = IntegerField()
    food = IntegerField()
    steel = IntegerField()
    aluminium = IntegerField()
    gasoline = IntegerField()
    ammo = IntegerField()
    concrete = IntegerField()

    class Meta:
        database = db

class UserCustom(Model):
    name = TextField(primary_key=True)
    flag = TextField()

    class Meta:
        database = db


def init_db():
    db.connect()
    db.create_tables([UserInfo, UserStats, UserMil, Infra, Resources, UserCustom], safe=True)
    print("DB initialized")

def close_db():
    if not db.is_closed():
        db.close()
        print("DB closed")