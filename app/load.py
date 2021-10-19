import csv
import datetime
import re
import os
import logging

import app.models
import app.database
import sqlalchemy

DB_ENGINE = app.database.engine
DB_METADATA = sqlalchemy.MetaData()

#models.Base.metadata.create_all(bind=engine)



# eventually this will be replaced by the postgres connection
#sqlliteEngine = sqlite+pysqlite:///:memory


LOGGER = logging.getLogger()

class TypeMap:
    """used to map specific types defined by site data.

    """
    def __init__(self):
        self.defaultType = sqlalchemy.types.String
        self.typeMap = {
            "docid": sqlalchemy.types.Integer,
            "site_id": sqlalchemy.types.Integer,
            "siteid": sqlalchemy.types.Integer,
            "catid": sqlalchemy.types.Integer,
            "sequenceno": sqlalchemy.types.Integer,
            "pin": sqlalchemy.types.Integer,
            "pidno": sqlalchemy.types.Integer,
            "eventid": sqlalchemy.types.Integer,
            "associatedsiteid": sqlalchemy.types.Integer,
            "participant_id": sqlalchemy.types.Integer,
            "participantid": sqlalchemy.types.Integer,
            "questionid": sqlalchemy.types.Integer,
            "parentid": sqlalchemy.types.Integer,
            "ownerid": sqlalchemy.types.Integer,
            "contactid": sqlalchemy.types.Integer,
            "completorid": sqlalchemy.types.Integer,
            "aec_id": sqlalchemy.types.Integer,
            "lat": sqlalchemy.types.Integer,
            "latdeg": sqlalchemy.types.Integer,
            "latmin": sqlalchemy.types.Integer,
            "latsec": sqlalchemy.types.Integer,
            "lon": sqlalchemy.types.Integer,
            "londeg": sqlalchemy.types.Integer,
            "lonmin": sqlalchemy.types.Integer,
            "lonsec": sqlalchemy.types.Integer,
            "regdate": sqlalchemy.types.Date,
            "eventdate": sqlalchemy.types.Date,
            "approval_date": sqlalchemy.types.Date,
            "moddate": sqlalchemy.types.Date,
            "tombdate": sqlalchemy.types.Date,
            "effectivedate": sqlalchemy.types.Date,
            "enddate": sqlalchemy.types.Date,
            "parttype": sqlalchemy.types.Date,
            "datenoted": sqlalchemy.types.Date,
            "date_completed": sqlalchemy.types.Date,
            "expirydate": sqlalchemy.types.Date,
            "datecompleted": sqlalchemy.types.Date,
            "datereceived": sqlalchemy.types.Date,
            "datelocalauthority": sqlalchemy.types.Date,
            "dateregistrar": sqlalchemy.types.Date,
            "datedecision": sqlalchemy.types.Date,
            "dateentered": sqlalchemy.types.Date,
            "submissiondate": sqlalchemy.types.Date,
            "documentdate": sqlalchemy.types.Date
        }

    def getType(self, columnName):
        retType = self.defaultType
        if columnName.lower() in self.typeMap:
            retType = self.typeMap[columnName.lower()]
        return retType

class ColumnDef:
    def __init__(self, columnName, columnLength=None, columnPosition=None, columnType=None):
        self.columnName = columnName
        self._columnLength = columnLength
        self.columnType = columnType
        self._columnPosition = columnPosition

    @property
    def columnLength(self):
        return self._columnLength

    @columnLength.setter
    def columnLength(self, columnLength):
        if not isinstance(columnLength, int):
            _columnLength = int(columnLength)

    @property
    def columnPosition(self):
        return self._columnPosition

    @columnPosition.setter
    def columnPosition(self, columnPosition):
        if not isinstance(columnPosition, int):
            self._columnPosition = int(columnPosition)

    def __str__(self):
        outStr = f'{self.columnName} {self._columnLength} {self._columnPosition}'
        return outStr

class ColumnDefs:
    def __init__(self):
        self.columnDefs = []
        self.curPos = 0
        self.typeMap = TypeMap()

    def addColumnDef(self, columnDef):
        # update the type with the type map
        columnDef.columnType = self.typeMap.getType(columnDef.columnName)
        self.columnDefs.append(columnDef)

    def __iter__(self):
        return self

    def __next__(self):
        if self.curPos >= len(self.columnDefs):
            raise StopIteration
        retVal = self.columnDefs[self.curPos]
        self.curPos += 1
        return retVal

    def __len__(self):
        return len(self.columnDefs)

    def __str__(self):
        outStr = []
        for columnDef in self.columnDefs:
            outStr.append(str(columnDef))
        return str(outStr)

    def getDataDict(self, line):
        """Gets an input data line, uses the parameters in the column definition to
        restructure the line into a data dict that can be used to insert the data into
        the database.

        :param line: input data line that was generated using the spool file
                     defs that will be dumped into the database
        :type line: str
        """
        outDict = {}
        colCnt = 0
        for columnDef in self:
            startPosition = columnDef.columnPosition
            columnLength = columnDef.columnLength
            endPosition = startPosition + columnLength
            dataValue = line[startPosition:endPosition].strip()
            outDict[columnDef.columnName] = dataValue
            LOGGER.debug(f'{colCnt} : {columnDef.columnName} : -{dataValue}-')
            colCnt += 1
        return outDict

class ReadSqlSpoolFiles:
    """used to read the .lis files and extract:
        * column names
        * column lengths
        * column column types

    gets this information by parsing out the column definitions from the sql
    file.  Format for SQL plus formatting:
    https://docs.oracle.com/cd/B19306_01/server.102/b14357/ch12013.htm#BACHCABF

    """
    def __init__(self, inputSpoolFile):
        self.inputSpoolFile = inputSpoolFile
        # used to identify a line that includes a column def
        columnDefRegexString = '^\s*column\s+\w+\s+format\s+\w+.*;$'
        self.coldefRegex = re.compile(columnDefRegexString)

        # used to extract the length from the column def
        replaceRegextString = '^\s*column\s+\w+\s+format\s+\w{1}'
        self.replaceRegex = re.compile(replaceRegextString)

    def getColumnName(self, line):
        # re.split(pattern, string, maxsplit=0, flags=0)
        lineSplit = re.split('\s+', line)
        LOGGER.debug(f"split line: {lineSplit}")
        return lineSplit[1]

    def getDefs(self):
        """reads the input sql file used to generate the dump file
        and extracts the column name definitions.

        :return: a list of numbers that identify the column positions where one column
                 starts and another ends
        :rtype: list
        """
        # columnLengths will be a list defining the locations in list of characters
        #   where one column starts and another ends
        columnLengths = ColumnDefs()
        prevValue = 0
        with open(self.inputSpoolFile) as fh:
            for line in fh:
                line = line.strip()
                if self.isColumnDef(line):
                    LOGGER.debug(f'input line: {line}')
                    colName = self.getColumnName(line)
                    colLength = self.getColumnLength(line)
                    columnPosition = prevValue
                    colDef = ColumnDef(colName, colLength, columnPosition)
                    columnLengths.addColumnDef(colDef)
                    prevValue = prevValue + 1 + colLength
        return columnLengths

    def getColumnLength(self, line):
        strippedString = self.replaceRegex.sub('', line).replace(';', '').strip()
        LOGGER.debug(strippedString)
        return int(strippedString)

    def isColumnDef(self, line):
        match = False
        if self.coldefRegex.match(line):
            match = True
            LOGGER.debug(f'line: {line}')
        return match

class CreateDBTable:
    """using the sql spool file that was used to create the dump files will
    create a database table with the same prefix as the name of the spool
    file.

    Name of the table can be overriden by providing that arg
    """

    def __init__(self, sqlSpoolFile, tableName=None):
        if tableName is None:
            tableName = os.path.splitext(os.path.basename(sqlSpoolFile))[0]
        self.tableName = tableName
        self.sqlSpoolFile = sqlSpoolFile
        readSpool = ReadSqlSpoolFiles(self.sqlSpoolFile)
        self.columnDefs = readSpool.getDefs()

    def listTables(self):
        inspector = sqlalchemy.inspect(DB_ENGINE)

        for table_name in inspector.get_table_names():
            for column in inspector.get_columns(table_name):
                LOGGER.info("Column: %s" % column['name'])

    def createTable(self):

        saTable = sqlalchemy.Table(self.tableName, DB_METADATA)
        for coldef in self.columnDefs:
            column = sqlalchemy.Column(coldef.columnName, coldef.columnType)
            saTable.append_column(column)

        LOGGER.debug(f"creating the table: {self.tableName}")
        DB_METADATA.create_all(DB_ENGINE)

    def loadData(self, dataFile):

        LOGGER.debug(f"column defs: {self.columnDefs}")
        with DB_ENGINE.connect() as conn:
            with open(dataFile, "r") as f:
                table = DB_METADATA.tables[self.tableName]
                rowsInserted = 0
                for line in f:
                    dataDict = self.columnDefs.getDataDict(line)

                    insStatement = sqlalchemy.insert(table).values(**dataDict)
                    result = conn.execute(insStatement)
                    if not rowsInserted % 200:
                        LOGGER.debug(f"inserted {rowsInserted}")
                    rowsInserted += 1

#         user = Table('user', metadata_obj,
#     Column('user_id', Integer, primary_key=True),
#     Column('user_name', String(16), nullable=False),
#     Column('email_address', String(60)),
#     Column('nickname', String(50), nullable=False)
# )









if __name__ == '__main__':

    # logging setup
    LOGGER.setLevel(logging.DEBUG)
    hndlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
    hndlr.setFormatter(formatter)
    LOGGER.addHandler(hndlr)
    LOGGER.debug("first test message")


    inputDataFile = '/home/kjnether/proj/site/sampledata/srsites.lis'
    sqlDefFile = '/home/kjnether/proj/site/runscript_local/bconline/srsites.sql'

    createDb = CreateDBTable(sqlDefFile)
    createDb.createTable()
    createDb.listTables()
    createDb.loadData(inputDataFile)


    def tmp():
        # reading the sql file used to generate the lis (column delimited) dump
        # files
        readSpool = ReadSqlSpoolFiles(sqlDefFile)
        columnDefs = readSpool.getDefs()

        # create the datamodel in SQL Alchemy


        colCnt = 1
        startValue = 1
        LOGGER.debug(f"column defs: {columnDefs}")
        with open(inputDataFile, "r") as f:
            for line in f:
                #print('----------------------------------------------')
                #print(line)
                colCnt = 1
                for columnDef in columnDefs:
                    startPosition = columnDef.columnPosition
                    columnLength = columnDef.columnLength
                    endPosition = startPosition + columnLength
                    dataValue = line[startPosition:endPosition].strip()

                    LOGGER.debug(f'{colCnt} : {columnDef.columnName} : -{dataValue}-')

                    colCnt += 1




    #     csv_reader = csv.DictReader(f)

    #     for row in csv_reader:
    #         db_record = models.Record(
    #             date=datetime.datetime.strptime(row["date"], "%Y-%m-%d"),
    #             country=row["country"],
    #             cases=row["cases"],
    #             deaths=row["deaths"],
    #             recoveries=row["recoveries"],
    #         )
    #         db.add(db_record)

    #     db.commit()

    # db.close()