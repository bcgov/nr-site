import load
import logging

import unittest

LOGGER = logging.getLogger()

class TestSum(unittest.TestCase):
    # def test_recordload(self):
    #     """
    #     Tests the loading of individual records from the data files after
    #     the column defs have been loaded
    #     """
    #     table_name = "srprofil"

    #     inputDataFile = f"/home/kjnether/proj/site/sampledata/{table_name}.lis"
    #     sqlDefFile = f"/home/kjnether/proj/site/runscript_local/bconline/{table_name}.sql"


    #     createdb = load.CreateDBTable(sqlDefFile)
    #     columnDefs = createdb.columnDefs
    #     dl = load.DataLoader(inputDataFile, columnDefs)
    #     allData = dl.next()
    #     #print(f'-{allData}-')
    #     LOGGER.debug(f"length: {len(allData)}")
    #     LOGGER.debug(f"endpos: {dl.endpos}")

    def test_readWholeFile(self):
        table_name = "srprofil"

        inputDataFile = f"/home/kjnether/proj/site/sampledata/{table_name}.lis"
        sqlDefFile = f"/home/kjnether/proj/site/runscript_local/bconline/{table_name}.sql"


        createdb = load.CreateDBTable(sqlDefFile)
        columnDefs = createdb.columnDefs
        dl = load.DataLoader(inputDataFile, columnDefs)
        #allData = dl.next()
        cnt = 0
        for rec in dl:
            #print(rec)
            rec = rec.replace("\n", '')
            print(f'{cnt} {len(rec)} {rec[0:100]}')
            if not cnt % 1000:
                print(f'cnt: {cnt}')
            if cnt > 3:
                import sys
                sys.exit()
            cnt += 1

if __name__ == '__main__':
    # logging setup
    LOGGER.setLevel(logging.INFO)
    hndlr = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s"
    )
    hndlr.setFormatter(formatter)
    LOGGER.addHandler(hndlr)
    LOGGER.debug("first test message")


    unittest.main()