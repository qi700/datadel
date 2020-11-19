import os
import json
text_file = 'passage_util_test'
files = os.listdir(text_file)
data_id = 0
res_json= []
f_out = open('passage_test_bert_point.json', 'w', encoding='utf-8')
for path in files:
    if(os.path.isfile(text_file + '/' + path)):
        print(path+'---start---')
        res_dict = {}
        file = open(text_file + '/' + path, 'r',encoding='utf8').read()
        data=file.split('\n')
        res_dict['news_id'] = int(data_id)
        res_dict['title'] = data[0].strip()
        res_dict['content'] = data[1].strip()
        data_id+=1
        f_out.write(json.dumps(res_dict))
        f_out.write('\n')
