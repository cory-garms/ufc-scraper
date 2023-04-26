tables = {
    'Divisions': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'division': 'TEXT',
        'weight': 'INTEGER',
        'gender': 'CHARACTER(1)'
    },

    'Events': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'name': 'TEXT',
        'date': 'INTEGER',
        'location': 'TEXT',
        'promotion': 'INTEGER'
    },

    'Fighters': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'name': 'TEXT',
        'nickname': 'TEXT',
        'wins': 'INTEGER',
        'losses': 'INTEGER',
        'draws': 'INTEGER',
        'division': 'INTEGER',
        'age': 'INTEGER',
        'height': 'REAL',
        'weight': 'REAL',
        'reach': 'REAL',
        'legReach': 'REAL',
        'sigStrikesLanded': 'INTEGER',
        'sigStrikesAttempted': 'INTEGER',
        'sigStrikesHead': 'INTEGER',
        'sigStrikesBody': 'INTEGER',
        'sigStrikesLeg': 'INTEGER',
        'sigStrikesStanding': 'INTEGER',
        'sigStrikesClinch': 'INTEGER',
        'sigStrikesGround': 'INTEGER',
        'sigStrikesPerMin': 'REAL',
        'sigStrikesAbsorbedPerMin': 'REAL',
        'takedownsLanded': 'INTEGER',
        'takedownsAttempted': 'INTEGER',
        'takedownsPer15Min': 'INTEGER',
        'submissionAttemptPer15Min': 'INTEGER',
        'winKO': 'INTEGER',
        'winDEC': 'INTEGER',
        'winSUB': 'INTEGER',
        'avgFightTime': 'INTEGER',
        'firstRoundFinishes': 'INTEGER'
    },

    'FighterStatHistory': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'fighter': 'INTEGER',
        'event': 'INTEGER'
    },

    'Fights': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'event': 'INTEGER',
        'fighter1': 'INTEGER',
        'fighter2': 'INTEGER',
        'division': 'INTEGER'
    },

    'FightStats': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'fight': 'INTEGER',
        'fighter': 'INTEGER'
    },

    'Promotions': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'promotion': 'TEXT'
    },

    'Referees': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'name': 'TEXT'
    }
}

foreign_keys = {
    'Events': [('promotion', 'Promotions(id)')],

    'Fighters': [('division', 'Divisions(id)')],

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
