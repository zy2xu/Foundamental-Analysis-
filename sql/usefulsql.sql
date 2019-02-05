-- select into csv 
SELECT *
FROM Indicators2017
INTO OUTFILE '/Users/zy2xu/Desktop/git/foundamentals/data/2017.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
