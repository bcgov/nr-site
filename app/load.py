import csv
import datetime
import re
import os
import logging
import glob
import sys

import models.models as models
import app.database
import sqlalchemy

DB_ENGINE = app.database.engine
DB_METADATA = sqlalchemy.MetaData()

# creates the Table defs, eventually moving
# to declaritive base
models.metadata.create_all(DB_ENGINE)

#1998-02-09
DATEFORMAT = '%Y-%m-%d'

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
            self.curPos = -1
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
        LOGGER.debug(f'columnDefs: {len(self)}')
        for columnDef in self:
            startPosition = columnDef.columnPosition
            columnLength = columnDef.columnLength
            endPosition = startPosition + columnLength
            dataValue = line[startPosition:endPosition].strip()
            if columnDef.columnType == sqlalchemy.types.Integer:
                if dataValue == '0':
                    dataValue = 0
                elif not dataValue:
                    dataValue = None
                else:
                    dataValue = int(dataValue)
            if columnDef.columnType == sqlalchemy.types.Date:
                if not dataValue:
                    dataValue = None
                else:
                    try:
                        dataValue = datetime.datetime.strptime(dataValue, DATEFORMAT)
                    except ValueError:
                        LOGGER.warning(f'invalid date value: {dataValue}')
                        raise
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
        # stores the linesize defined in the spoolfile
        self.linesize = None

    # def getDataTableName(self):
    #     baseName = os.path.splitext(os.path.basename(self.inputSpoolFile))[0] + '.lis'
    #     dirName = os.path.dirname(self.inputSpoolFile)
    #     dataTable = os.path.join(dirName, baseName)


    def getColumnName(self, line):
        # re.split(pattern, string, maxsplit=0, flags=0)
        lineSplit = re.split('\s+', line)
        LOGGER.debug(f"split line: {lineSplit}")
        return lineSplit[1]

    def isSetDef(self, line, paramName=None):
        """parses the input line looking for a pattern starts with a
        'set' parameter

        if the added paramName is provided then looks for a set statement
        where the parameter that is being set, and returns true if the
        line is a 'set' line for that 'paramName'

        :param line: input line to be evaluated
        :type line: str
        :param paramName: [name of the input parameter], defaults to None
        :type paramName: [str], optional
        :return: [a boolean indicating if the line is a 'set' line and if a parameter
                  is provided whether its a set for that parameter]
        :rtype: [bool]
        """
        retVal = False
        line = line.replace(';', '')
        lineList = re.split("\s+", line)
        #LOGGER.debug(f'LineList: {lineList}, {paramName}')
        if lineList[0].lower() == 'set':
            if paramName is not None:
                if paramName.lower() == lineList[1].lower():
                    retVal = True
            else:
                retVal = True
        #LOGGER.debug(f'retVal: {retVal}')
        return retVal

    def getSetValue(self, line):
        """assumes that the input line is a 'set' line and if so will
        return the value that corresponds with the set

        :param line: [input line]
        :type line: [type]
        :return:
        """
        retVal = None
        if self.isSetDef(line):
            line = line.replace(';', '')
            lineList = re.split("\s+", line)
            retVal = lineList[-1]
        return retVal

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
                if self.isSetDef(line, "linesize"):
                    linesize = self.getSetValue(line)
                    LOGGER.debug(f"linesize: {linesize}")

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
        self.readSpool = ReadSqlSpoolFiles(self.sqlSpoolFile)
        self.columnDefs = self.readSpool.getDefs()

    def listTables(self):
        inspector = sqlalchemy.inspect(DB_ENGINE)
        for table_name in inspector.get_table_names():
            for column in inspector.get_columns(table_name):
                LOGGER.debug("Column: %s" % column['name'])

    # def getTableDeclarativeBase(self):

    #     app.models


    def createTable(self):
        saTable = getattr(models, f"t_{self.tableName}")
        colList = []
        for col in saTable.c:
            colName = str(col)
            colList.append(colName.split('.')[1].lower())
            #print(f"col: {col}")
        LOGGER.debug(f'column list: {colList}')
        #saTable = sqlalchemy.Table(self.tableName, DB_METADATA)
        # making sure all the columns are in the table
        for coldef in self.columnDefs:
            if coldef.columnName.lower() not in colList:
                column = sqlalchemy.Column(coldef.columnName, coldef.columnType)
                saTable.append_column(column, replace_existing=True)

        LOGGER.info(f"creating the table: {self.tableName}")
        #DB_METADATA.create_all(DB_ENGINE)
        models.metadata.create_all(DB_ENGINE)

    def dropTable(self):
        LOGGER.debug(f'tables: {DB_METADATA.tables}')
        #table = DB_METADATA.tables[f't_{self.tableName}]
        table = getattr(models, f't_{self.tableName}')

        LOGGER.info(f"dropping the table: {self.tableName}")
        table.drop(DB_ENGINE)
        #DB_METADATA.drop_all(bind=DB_ENGINE, tables=[table])

    def tableExists(self, tableName, connection):
        tableExist = True
        if not DB_ENGINE.dialect.has_table(connection, tableName):
            tableExist = False
        return tableExist

    #def getSourceDataRowCount(self):

    def getRowCount(self, tableName):
        Session = sqlalchemy.orm.sessionmaker(bind=DB_ENGINE)
        session = Session()
        table = getattr(models, f't_{self.tableName}')
        rows = session.query(table).count()
        session.close()
        rows = int(rows)
        LOGGER.info(f"table {self.tableName} row count: {rows} {type(rows)}")
        return rows

    def loadData(self, dataFile, dumpReplace=True):
        """[summary]

        :param dataFile: [description]
        :type dataFile: [type]
        :param dumpReplace: [description], defaults to True
        :type dumpReplace: bool, optional
        """
        # TODO: the sql def file has a parameter called linesize.  Need to ignore the carriage returns and treat input data as a stream.
        bufferSize = 1000
        bufferCnt = 0
        buffer = []
        if dumpReplace:
            self.dropTable()

        LOGGER.debug(f"column defs: {self.columnDefs}")
        with DB_ENGINE.connect() as conn:
            # get rows in datafile
            LOGGER.info(f"datafile to load: {dataFile}")
            rowsInDataFile = sum(1 for line in open(dataFile, "r", encoding='cp1252'))
            LOGGER.info(f"rows in data file {os.path.basename(dataFile)} : {rowsInDataFile}")
            with open(dataFile, "r", encoding='cp1252') as f:
                #table = DB_METADATA.tables[self.tableName]
                table = getattr(models, f't_{self.tableName}')
                if not self.tableExists(self.tableName, conn):
                    self.createTable()
                # get rows in table
                dbTableRowCount =  self.getRowCount(self.tableName)
                LOGGER.info(f"src row count: {rowsInDataFile} dest row count: {dbTableRowCount}")
                if dbTableRowCount != rowsInDataFile and dbTableRowCount != 0:
                    # rows in source and destination do not align, so recreate
                    self.dropTable()
                    self.createTable()
                    dbTableRowCount = 0
                if not dbTableRowCount and rowsInDataFile:
                    rowsInserted = 0
                    for line in f:
                        dataDict = self.columnDefs.getDataDict(line)
                        buffer.append(dataDict)
                        if bufferCnt >= bufferSize:
                            conn.execute(table.insert(), buffer)
                            bufferCnt = -1
                            buffer = []
                            LOGGER.info(f"rows inserted: {rowsInserted}")

                        #insStatement = sqlalchemy.insert(table).values(**dataDict)
                        #result = conn.execute(insStatement)
                        #if not rowsInserted % 200:
                        #    LOGGER.debug(f"inserted {rowsInserted}")
                        rowsInserted += 1
                        bufferCnt += 1
                    if buffer:
                        conn.execute(table.insert(), buffer)
                        bufferCnt = -1
                        buffer = []
                        LOGGER.info(f"rows {bufferCnt} inserted: {rowsInserted}")

if __name__ == '__main__':

    # logging setup
    LOGGER.setLevel(logging.INFO)
    hndlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
    hndlr.setFormatter(formatter)
    LOGGER.addHandler(hndlr)
    LOGGER.debug("first test message")


    # TODO:
    # should build a proper load script,
    # alternative is to define an order which tables are loaded or some kind of feedback
    # process that allows the process to continue to try based on certain foreign key
    # errors

    # load a single table
    # ----------------------------------
    # srparrol
    # srsitpar
    #
    LOGGER.setLevel(logging.INFO)
    table_name = 'srprfuse' # srevents  srevpart srsitpar srparrol srsitdoc srdocpar srprfuse srparrol
    inputDataFile = f'/home/kjnether/proj/site/sampledata/{table_name}.lis'
    sqlDefFile = f'/home/kjnether/proj/site/runscript_local/bconline/{table_name}.sql'
    createDb = CreateDBTable(sqlDefFile)
    #createDb.dropTable()
    createDb.createTable()
    createDb.listTables()
    createDb.loadData(inputDataFile, dumpReplace=False)

    sys.exit()

    # loading all tables
    tableDir = r'/home/kjnether/proj/site/sampledata/*.lis'
    sqlDir = r'/home/kjnether/proj/site/runscript_local/bconline'
    #files = os.listdir(tableDir)
    datafiles = glob.glob(tableDir)
    LOGGER.debug(f"datafiles: {datafiles}")
    exceptionList = []
    for curFile in datafiles:
        if os.path.basename(curFile) == 'srprofil.lis':
            exceptionList.append(curFile)
    for exceptionFile in exceptionList:
        datafiles.remove(exceptionFile)

    LOGGER.debug(f'list of data files: {datafiles}')
    for datafile in datafiles:
        sqlFile = os.path.splitext(os.path.basename(datafile))[0] + '.sql'
        sqlFileFullPath = os.path.join(sqlDir, sqlFile)
        if not os.path.exists(sqlFileFullPath):
            msg = f'the sql file {sqlFileFullPath} does not exist'
            raise ValueError(msg)
        createDb = CreateDBTable(sqlFileFullPath)
        createDb.createTable()
        createDb.listTables()
        createDb.loadData(datafile, False)
