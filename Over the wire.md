Over the wire -

**Level 0 -**

1\. open windows command prompt

2\. ssh bandit0@bandit.labs.overthewire.org -p 2220     

this command is used to connect to the server of bandit ; flag p 2220 means >> port number 2220



general command = ssh username@hostname

OR                ssh username@IP\_address



3\. password = bandit0





**Level 0-Level 1**



1\. use ls command to see what all files or other directories are there 

2\. use " cat readme " command to check content inside the readme file 

3\. password= ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If

4\. Now start a new session by first entering command " exit " and then again logging into the server with a username bandit1 from windows prompt





**Level 1- Level 2**

1\. use ls to see files .

2\. if a filename starts with a special character like "-", then use ./ prefixed so that the terminal reads it as path of a file and no syntax errors ocurr

3\. password=263JGJPfgU6LtdEvgfWU1XP5yac29mFx  



Level 2- Level 3

1.If there are spaces in a filename , then whitespaces  by default break the command line ; Hence three methods can be used

&#x09;A. put the filename in inverted commas 

&#x09;B. use \\ before every space 

&#x09;C. type the initial letters of the file name and then use tab for            	autocompletion 



2\. password=MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx





**Level 3- Level 4**

1.ls -a

2\. cat ./...Hiding-From-You

3.password = 2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ







**Level 4 -Level 5**

1. This level teaches how to see datatype of each file using "file" command. Human readable file is ASCII text
2. For checking all files 
file ./\*
3. password=4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw





Level 5- Level 6

1. cd inhere 

2\. find . -type f -size 1033c ! -executable

3\. password= HWasnPhtq9AVKe0dmk45nxy20cvUa6EG





Level 6 - Level 7

1. find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
2. find / → search the entire filesystem
3. \-user bandit7 → owner is bandit7
4. \-group bandit6 → group is bandit6
5. \-size 33c → exactly 33 bytes (c = bytes)
6. 2>/dev/null → hide permission denied errors
7. password= morbNTDkSW6jIlUc0ymOdMaLnOlFVAaj



Level 7 - Level 8

1.grep "millionth" data.txt

2.what does grep do ?

grep is used when you want to search for text patterns inside files or command output.

Think of it as:

grep = find lines that contain a specific word or pattern

3.password= dfwvzFQi4mU0wfNbFOe9RoWskMLg7eEc

&#x20;

Level 8- Level 9

1\. sort data.txt | uniq -u
Sorts all lines alphabetically so duplicates come together.

Then removes duplicates that come together and output line that is unique

2.password= 4CKMh1JI91bUIZZPXDqGanal4xvAg0JM



Level 9- Level 10

1.strings data.txt | grep "="

strings is used to see human readable text

2.password=  FGUW5ilLVJrxX9kMYMmlN4MgbpfMiqey





Level 10- Level 11

1.base64 -d data.txt

Base64 is an encoding that converts data into readable characters. To get the original text, you need to decode it.
I have to learn more about  different encodings

2.password= dtR173fZKb0RRsDFSGsg2RWnpNVj3qRr



