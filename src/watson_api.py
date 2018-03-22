import json
from os.path import join, dirname
from watson_developer_cloud import PersonalityInsightsV2

#{
#  "url": "https://gateway.watsonplatform.net/personality-insights/api",
#  "username": "b3265b11-c769-49c1-9761-8a9ca1881e19",
#  "password": "HNEUVEKNUFF7"
#}

personality_insights = PersonalityInsightsV2(username='b3265b11-c769-49c1-9761-8a9ca1881e19',password='HNEUVEKNUFF7')

with open(join(dirname(__file__), '../resources/personality.txt')) as \
         personality_text:
		     personality_insights_json = {"contentItems": [
		         {"id": "245160944223793152", "userid": "bob", "sourceid": "twitter",
		          "created": 1427720427, "updated": 1427720427,
		          "contenttype": "text/plain", "charset": "UTF-8",
		          "language": "en-us", "content": personality_text.read(),
		          "parentid": "", "reply": "false", "forward": "false"}]}

print(json.dumps(personality_insights.profile(text=personality_insights_json), indent=2))