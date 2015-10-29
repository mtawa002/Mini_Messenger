COPY USR(userId, password, email, name, dateOfBirth) from '/tmp/mtawa002/data/USR.csv' WITH DELIMITER ',' CSV;

COPY WORK_EXPR(userId, company, role, location, startDate, endDate) from '/tmp/mtawa002/data/Work_Ex.csv' WITH DELIMITER ',' CSV;

COPY EDUCATIONAL_DETAILS(userId, institutionName, major, degree, startdate, enddate) from '/tmp/mtawa002/data/Edu_Det.csv' WITH DELIMITER ',' CSV;

COPY MESSAGE(msgId, senderId, receiverId, contents, sendTime, deleteStatus, status) from '/tmp/mtawa002/data/Message.csv' WITH DELIMITER ',' CSV;

COPY CONNECTION_USR(userId, connectionId, status) from '/tmp/mtawa002/data/Connection.csv' WITH DELIMITER ',' CSV;
