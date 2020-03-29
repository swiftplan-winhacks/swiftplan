import sqlite3
from event import *

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        conn = self.connect()
        c = conn.cursor()

        init_query = """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL,
            passwd_hash TEXT NOT NULL
        );
        """
        c.execute(init_query)
        conn.commit()
        conn.close()
    
    def connect(self):
        return sqlite3.connect(self.db_name + '.db')

    def addUser(self, username, passwd_hash):
        conn = self.connect()
        c = conn.cursor()

        query_1 = """
        INSERT INTO users VALUES("{username}", "{passwd_hash}");
        """

        try:
            c.execute(query_1)
        except Exception as e:
            print("Could not add this user because of an error: ", e)

        query_2 = f"""
        CREATE TABLE IF NOT EXISTS {username} (
            id INTEGER PRIMARY KEY,
            event_name TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_desc TEXT,
            event_location_lat REAL NOT NULL,
            event_location_lng REAL NOT NULL,
            is_fixed INTEGER NOT NULL,
            start_date TEXT,
            start_time TEXT,
            duration TEXT,
            end_date TEXT,
            end_time TEXT,
            scheduled_date TEXT,
            scheduled_time TEXT,
            scheduled_duration TEXT,
            location_name TEXT
        );
        """

        try:
            c.execute(query_2)
            conn.commit()
            print(f"User {username} added successfully")
        except Exception as e:
            print("Could not add this user because of an error: ", e)
        

        conn.close()
    
    def removeUser(self, username):
        conn = self.connect()
        c = conn.cursor()

        query_1 = f"""
        DELETE FROM users
        WHERE username = "{username}";
        """

        try:
            c.execute(query_1)
        except Exception as e:
            print("Could not delete this user because of an error: ", e)

        query_2 = f"""
        DROP TABLE IF EXISTS {username};
        """

        try:
            c.execute(query_2)
            conn.commit()
            print(f"User {username} removed successfully")
        except Exception as e:
            print("Could not delete this user because of an error: ", e)

        conn.close()
    
    def addEvent(self, username, event):
        if(type(event) != Event):
            raise Exception("event should be an object of type Event __init__(self, name, type, desc, location, is_fixed, timeframe, scheduled_datetime=None):")

        conn = self.connect()
        c = conn.cursor()

        query = f"""
        INSERT INTO {username}
        VALUES(
            NULL,
            "{event.name}",
            "{event.type}",
            "{event.desc}",
            {event.location.lat},
            {event.location.lng},
            {event.isFixed()},
            "{event.timeframe.start_date}",
            "{event.timeframe.start_time}",
            "{event.timeframe.duration}",
            "{event.timeframe.end_date}",
            "{event.timeframe.end_time}",
            "{event.scheduled_datetime.start_date}",
            "{event.scheduled_datetime.start_time}",
            "{event.scheduled_datetime.duration}",
            "{event.location_name}"
        );
        """
        
        try:
            c.execute(query)
            conn.commit()
            event.setId(c.lastrowid)
            print(f"Event added succesfully")
        except Exception as e:
            print("Could not add this event because of an error: ", e)

        conn.close()

        return event

        
    def updateEvent(self, username, event):
        if(type(event) != Event):
            raise Exception("event should be an object of type Event __init__(self, name, type, desc, location, is_fixed, timeframe, scheduled_datetime=None):")

        conn = self.connect()
        c = conn.cursor()

        query = f"""
        UPDATE {username} SET
        scheduled_date = "{event.scheduled_datetime.start_date}",
        scheduled_time = "{event.scheduled_datetime.start_time}"
        WHERE id = {event.id};
        """

        try:
            c.execute(query)
            conn.commit()
            print(f"Event updated successfully")
        except Exception as e:
            print("Could not update this event because of an error: ", e)

        conn.close()

    def removeEvent(self, username, event_id):
        conn = self.connect()
        c = conn.cursor()

        query = f"""
        DELETE FROM {username}
        WHERE id = {event_id};
        """

        try:
            c.execute(query)
            conn.commit()
            print(f"Event deleted successfully")
        except Exception as e:
            print("Could not delete this event because of an error: ", e)

        conn.close()

    def fetchEvents(self, username):
        conn = self.connect()
        c = conn.cursor()

        query = f"""
        SELECT * FROM {username}
        """
        data = []
        try:
            for row in c.execute(query):
                print(row)
                e = Event(
                    name = row[1],
                    type = row[2],
                    desc = row[3],
                    location = Location(
                        lat = row[4],
                        lng = row[5]
                    ),
                    is_fixed = int(row[6]),
                    timeframe = Timeframe(
                        start_date = row[7],
                        start_time = row[8],
                        end_date = row[10],
                        end_time = row[11],
                        duration = row[9]
                    ),
                    location_name = row[15]
                )

                e.reschedule(Timeframe(row[12], row[13], row[12], row[13], row[14]))

                e.setId(row[0])

                data.append(e)

        except Exception as e:
            print("Could not fetch data because of an error: ", e)

        conn.close()
        return data

    def fetchEventsByDay(self,login):
        data = self.fetchEvents(login)

        dictionary = {}
        for e in data:
            if(e.scheduled_datetime.start_date not in dictionary):
                dictionary[e.scheduled_datetime.start_date] = []
            dictionary[e.scheduled_datetime.start_date].append(e)
        return dictionary


# #test
# db = Database("b")
# db.addUser("test", "test")
# for i in range(10):
#     t = Timeframe("01.01.1234", "13:00","02.01.1234", "13:21", "3:00")
#     e = Event(f"a{i}", "nothing", "lol", Location(00.123,00.123), True, t)
#     db.addEvent("test", e)
# print(db.fetchEventsByDay("test"))