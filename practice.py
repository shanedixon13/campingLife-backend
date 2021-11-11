print ("Shane Dixon")

#print numbers from 30-70
for i in range(30,71):
    print(i, end=" ")

#work with files
#read notes.txt and count lines
file_read = open ("notes.txt","r")#r=read
all_lines=file_read.readlines()
print(f"There are {len(all_lines)} lines in the files")#string formatting
file_read.close()

#create a new file
test=open("demo.txt", "w") #w=write
test.write("Hello from Python\n")
test.write("This should be the second line\n")
test.write("Hello from Python\n")
test.close()

#write a line in the bottom of notes.txt
notes=open("notes.txt", "a")
notes.write("\n***THis text was added with Python code")

