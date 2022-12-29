from unittest import TestCase
import pymysql
import utils


class MockDB(TestCase):

    def setUpClass(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='2000825lxr', charset='utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute("use property")
        #
        # # drop database if it already exists
        # try:
        #     cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
        #     cursor.close()
        #     print("DB dropped")
        # except mysql.connector.Error as err:
        #     print("{}{}".format(MYSQL_DB, err))
        #
        # cursor = cnx.cursor(dictionary=True)
        # try:
        #     cursor.execute(
        #         "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_DB))
        # except mysql.connector.Error as err:
        #     print("Failed creating database: {}".format(err))
        #     exit(1)
        # cnx.database = MYSQL_DB
        #
        # query = """CREATE TABLE `test_table` (
        #           `id` varchar(30) NOT NULL PRIMARY KEY ,
        #           `text` text NOT NULL,
        #           `int` int NOT NULL
        #         )"""
        # try:
        #     cursor.execute(query)
        #     cnx.commit()
        # except mysql.connector.Error as err:
        #     if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        #         print("test_table already exists.")
        #     else:
        #         print(err.msg)
        # else:
        #     print("OK")
        #
        # insert_data_query = """INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
        #                     ('1', 'test_text', 1),
        #                     ('2', 'test_text_2',2)"""
        # try:
        #     cursor.execute(insert_data_query)
        #     cnx.commit()
        # except mysql.connector.Error as err:
        #     print("Data insertion to test_table failed \n" + err)
        # cursor.close()
        # cnx.close()
        #

    def test_db_write(self):
        self.assertEqual(utils.db_write("""INSERT INTO test_table (id, text, int) VALUES
                        ('3', 'test_text_3', 3);"""), True)
        self.assertEqual(utils.db_write("""INSERT INTO test_table (id, text, int) VALUES
                        ('1', 'test_text_3', 3);"""), False)
        self.assertEqual(utils.db_write("""DELETE FROM test_table WHERE id='1';"""), True)
        self.assertEqual(utils.db_write("""DELETE FROM test_table WHERE id='4';"""), True)

    def tearDownClass(self):
        self.cursor.close()
        self.conn.close()

        # # drop test database
        # try:
        #     cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
        #     cnx.commit()
        #     cursor.close()
        # except mysql.connector.Error as err:
        #     print("Database {} does not exists. Dropping db failed".format(MYSQL_DB))
