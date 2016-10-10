import urllib2
import json
location = "Formby"
apiKey = "203f287ba8cf5c5f"
f = urllib2.urlopen('http://api.wunderground.com/api/'+apiKey+'/geolookup/conditions/q/IA/'+location+'.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_c = parsed_json['current_observation']['temp_c']
print "Current temperature in %s is: %s" % (location, temp_c)
f.close()