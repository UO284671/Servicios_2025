docker run --rm -d --name prosody --network pruebas \
  -p 5222:5222 \
  -v $(pwd)/etc/prosody:/etc/prosody \
  -v $(pwd)/data:/var/lib/prosody \
  unclev/prosody-docker-extended:0.10