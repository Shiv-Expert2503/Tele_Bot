from gnewsclient import gnewsclient
client=gnewsclient.NewsClient()
# print(client.get_config())
client.language='hindi'
client.location='india'
client.topic='business'

print(client.locations)
print(client.languages)
    