path = '/home/fzeng/Desktop/'
old_file = path + '2601SID.csv'
new_file = path + '2601SID_LastName.csv'
with open(new_file, 'w') as new_f:
    with open(old_file, 'r') as old_f:
        for line in old_f:
            SID = line[0:line.find('"')-1]
            name = line[line.find('"'):]
            lastname = name[1:name.find(',')]
            new_line = SID + ', ' + lastname + '\n'
            print new_line
            new_f.write(new_line)
