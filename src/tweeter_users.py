import json
import logging
import sys
import json
import rethinkdb as r
import io

#Neccesary log
root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s : %(asctime)s :%(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


out_data ={"content_items":[]}
elements=[]

#Make it work for python 2 and 3
try:
    to_unicode = unicode
except NameError:
    to_unicode = str


#write json data
def write_json(data):
	#print data
	with io.open('data.json','w',encoding='utf8') as outfile:
		str_ = json.dumps(data,indent=4,sort_keys=True,separators=(',', ': '), ensure_ascii=False)
		outfile.write(to_unicode(str_))
		root.info('Finished write JSON Data .....')
		
#Structure for send to Watson
#{
#         "content": "\"What my faith gives me no one can match\"#Belief",
#         "contenttype": "text/plain",
#         "created": 1445472961000,
#         "id": "656987336266223616",
#         "language": "en"
#      }

##Bring all Fields necesary to send to Watson
def get_users():
	root.info('Trying to connect to local DataBase...')
	r.connect('localhost',28015).repl()
	root.info('Connected to Rethink DB ...Displaying search..')
	root.info('Querying tweets this may take several minutes....')
	tweets = r.db('test').table('tweets').pluck("id_str","text","lang","created_at").run()
	#print tweets
	#fields = tweets.filter("id","full_text","lang","coordinates").run()
	#print tweets
	root.info('Finished query ...trying to rename data fields..')
	for chunk in tweets:
		elements.append(chunk)
		chunk["language"] = chunk.pop("lang")
		chunk["contenttype"]="text/plain"
		chunk["id"] = chunk.pop("id_str")
		chunk["content"] = chunk.pop("text")
		chunk["created"] = chunk.pop("created_at")
	#Add to the dictionary	
	out_data["content_items"]=elements

	#Write data
	write_json(out_data)

#Rename the keys in order to send to watson


get_users()

