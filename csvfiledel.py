import csv
import os
fh = open(r'passage_test_csv\passage_test.csv',"w+",newline='',encoding='utf8')
writer = csv.writer(fh,delimiter = '\t')
text_file = 'passage_util_test'
files = os.listdir(text_file)
for path in files:
    if(os.path.isfile(text_file + '/' + path)):
        print(path+'---start---')
        res = []
        file = open(text_file + '/' + path, 'r',encoding='utf8').read()
        data=file.split('\n')
        res.append(data[1].strip())
        res.append(data[0].strip())
        res.append(data[0])
        if res:
            writer.writerow(res)

