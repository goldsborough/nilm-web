import psycopg2

class Database:

    def __init__(self, url):

        self.conn = None
        
        # First we try to connect to the database
        try:
            self.url = url

            # Access credentials via the passed on url. The url must
            # be parsed with the urlparse library. 
            self.conn = psycopg2.connect(database = self.url.path[1:],
                                         user = self.url.username,
                                         password = self.url.password,
                                         host = self.url.hostname,
                                         port = self.url.port)
            
            self.cursor = self.conn.cursor()

        except psycopg2.DatabaseError as e:
            print "Error connecting to database!"
        
    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()


    def get(self,items):
        """ 
        Queries the database for data 
        items: string of items to query for, must be
        comma-separated.
        """
        
        # the query is nothing else than an SQL statement,
        # where we concatenate the items we want to fetch
        query = "SELECT (" + items + ") FROM db;"

        # Execute the query
        self.cursor.execute(query)

        # Retrieve the data. It is returned in a very
        # weird state, where all rows are tuples, inside
        # of tuples where the data is the only element
        # (useless surrounding tuple) and all tuples are
        # strings instead of actual tuple objects
        rows = self.cursor.fetchall()
        
        # convert strings to tuples and return them
        return [eval(j) for i in rows for j in i]
                
    def write(self,items,data):
        """ 
        Writes items to the database.
        items: string of items to insert.
        data: list of strings of data to insert
        into the respective columns.
        """
        
        query = "INSERT INTO db (" + items + ") VALUES (" + ", ".join(data) + ");"

        self.cursor.execute(query)

    def summary(self,rows):
        """
        Processes data and returns only the maximum,
        minimum and average for each column.
        """
            
        # split the rows into columns
        cols = [ [r[c] for r in rows] for c in range(len(rows[0])) ]
        
        # the time in terms of fractions of hours of how long ago
        # the sample was. Assumes the sampling period is 10 minutes
        t = lambda col: "{:.1f}".format((len(rows) - col) / 6.0)

        # return a tuple, consisting of tuples of the maximum,
        # the minimum and the average for each column and their
        # respective time (how long ago, in fractions of hours)
        # average has no time, of course
        ret = []

        for c in cols:
            hi = max(c)
            hi_t = t(c.index(hi))

            lo = min(c)
            lo_t = t(c.index(lo))

            avg = sum(c)/len(rows)

            ret.append(((hi,hi_t),(lo,lo_t),avg))

        return ret
