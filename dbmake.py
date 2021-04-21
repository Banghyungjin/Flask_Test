import pymysql

db = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = '1234',
    db = 'busan'
)

sql = '''
    CREATE TABLE `topic` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`title` varchar(100) NOT NULL,
	`body` text NOT NULL,
	`author` varchar(30) NOT NULL,
    `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id)
	) ENGINE=innoDB DEFAULT CHARSET=utf8;
'''

sql_insert = "INSERT INTO `busan`.`users` (`title`, `body`, `author`) VALUES ('방형진', 'banghyungjin@gmail.com', 'Bang','12345');"

title = input('제목을 적으세요 = ')
body = input('내용을 적으세요 = ')
author = input('저자를 적으세요 = ')

sql_insert_2 = "INSERT INTO `busan`.`topic` (`title`, `body`, `author`) VALUES (%s, %s, %s);" 
val = [title, body, author]

cursor = db.cursor()
cursor.execute(sql)
print(cursor.rowcount, "개의 줄이 추가되었습니다.")
db.commit()
db.close()
#cursor.execute('SELECT * FROM topic;')
#users = cursor.fetchall()
#print(users)