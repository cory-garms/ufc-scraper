tables = {
    'Divisions': {
        'id': {'type': 'INTEGER', 'constraint': 'PRIMARY KEY ASC'},
        'division': {'type': 'TEXT'},
        'weight': {'type': 'INTEGER'},
        'gender': {'type': 'CHARACTER(1)'}
    },

    'Events': {
        'id': {'type': 'INTEGER', 'constraint':  'PRIMARY KEY ASC'},
        'name': {'type': 'TEXT'},
        'date': {'type': 'INTEGER'},
        'location': {'type': 'TEXT'},
        'promotion': {'type': 'INTEGER'}
    },

    'Fighters': {
        'id': {'type': 'INTEGER', 'constraint':  'PRIMARY KEY ASC'},
        'name': {'type': 'TEXT'},
        'nickname': {'type': 'TEXT'},
        'wins': {'type': 'INTEGER'},
        'losses': {'type': 'INTEGER'},
        'draws': {'type': 'INTEGER'},
        'division': {'type': 'INTEGER'},
        'age': {'type': 'INTEGER'},
        'height': {'type': 'REAL'},
        'weight': {'type': 'REAL'},
        'reach': {'type': 'REAL'},
        'legReach': {'type': 'REAL'},
        'sigStrikesLanded': {'type': 'INTEGER'},
        'sigStrikesAttempted': {'type': 'INTEGER'},
        'sigStrikesHead': {'type': 'INTEGER'},
        'sigStrikesBody': {'type': 'INTEGER'},
        'sigStrikesLeg': {'type': 'INTEGER'},
        'sigStrikesStanding': {'type': 'INTEGER'},
        'sigStrikesClinch': {'type': 'INTEGER'},
        'sigStrikesGround': {'type': 'INTEGER'},
        'sigStrikesPerMin': {'type': 'REAL'},
        'sigStrikesAbsorbedPerMin': {'type': 'REAL'},
        'takedownsLanded': {'type': 'INTEGER'},
        'takedownsAttempted': {'type': 'INTEGER'},
        'takedownsPer15Min': {'type': 'INTEGER'},
        'submissionAttemptPer15Min': {'type': 'INTEGER'},
        'winKO': {'type': 'INTEGER'},
        'winDEC': {'type': 'INTEGER'},
        'winSUB': {'type': 'INTEGER'},
        'avgFightTime': {'type': 'INTEGER'},
        'firstRoundFinishes': {'type': 'INTEGER'},
        'trainsAt': {'type': 'INTEGER'}
    },

    'FighterStatHistory': {
        'id': {'type': 'INTEGER', 'constraint': 'PRIMARY KEY ASC'},
        'fighter': {'type': 'INTEGER'},
        'event': {'type': 'INTEGER'}
    },

    'Fights': {
        'id': {'type': 'INTEGER', 'constraint': 'PRIMARY KEY ASC'},
        'event': {'type': 'INTEGER'},
        'fighter1': {'type': 'INTEGER'},
        'fighter2': {'type': 'INTEGER'},
        'division': {'type': 'INTEGER'},
        'rounds': {'type': 'INTEGER'},
        'title': {'type': 'INTEGER', 'constraint': 'CHECK(title in (0, 1))'}
    },

    'FightStats': {
        'id': {'type': 'INTEGER', 'constraint': 'PRIMARY KEY ASC'},
        'fight': {'type': 'INTEGER'},
        'fighter': {'type': 'INTEGER'}
    },

    'Promotions': {
        'id': {'type': 'INTEGER', 'constraint': 'PRIMARY KEY ASC'},
        'promotion': {'type': 'TEXT'}
    },

    'Gyms': {
        'id': {'type': 'INTEGER', 'constraint': 'PRIMARY KEY ASC'},
        'name': {'type': 'TEXT'}
    },

    'Referees': {
        'id': {'type': 'INTEGER', 'constraint': 'PRIMARY KEY ASC'},
        'name': {'type': 'TEXT'}
    }
}

foreign_keys = {
    'Events': [('promotion', 'Promotions(id)')],

    'Fighters': [('division', 'Divisions(id)'),
                 ('trainsAt', 'Gyms(id)')],

    'FighterStatHistory': [('fighter', 'Fighters(id)'),
                           ('event', 'Events(id)')],

    'Fights': [('event', 'Events(id)'),
               ('fighter1', 'Fighters(id)'),
               ('fighter2', 'Fighters(id)'),
               ('division', 'Divisions(id)')
              ],

    'FightStats': [('fight', 'Fights(id)'),
                   ('fighter', 'Fighters(id)')]
}

