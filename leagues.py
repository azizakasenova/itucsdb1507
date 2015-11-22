import psycopg2 as dbapi2

class League:
    def __init__(self, name,abbreviation, countryID):
        self.name = name
        self.abbreviation = abbreviation
        self.countryID = countryID

class Leagues:
    def __init__(self, app):
        self.app = app

    def initialize_tables(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS LEAGUES(
                        LEAGUE_ID serial  NOT NULL,
                        NAME varchar(100)  NOT NULL,
                        ABBREVIATION varchar(10),
                        COUNTRY_ID int  NOT NULL,
                        CONSTRAINT LEAGUES_pk PRIMARY KEY (LEAGUE_ID),
                        CONSTRAINT LEAGUES_COUNTRIES
                            FOREIGN KEY (COUNTRY_ID)
                            REFERENCES COUNTRIES (COUNTRY_ID)
                    );
                    """)

                connection.commit()

    def add_league(self, league):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO LEAGUES (NAME, ABBREVIATION, COUNTRY_ID)
                    VALUES (%s, %s, %s) """,
                    (league.name, league.abbreviation, league.countryID))
                connection.commit()


    def get_leagues(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT * FROM LEAGUES"""
            cursor.execute(query)
            connection.commit()

            leagues = [(key, League(name, abbreviation, countryID))
                        for key, name, abbreviation, countryID in cursor]

            return leagues
