docker run -it --rm -d  --name wowza\
    -p 1935:1935 -p 8086:8086 -p 8087:8087 -p 8088:8088 \
    -p 5004-5008:5004-5008/udp \
    -e WSE_MGR_USER=wowza \
    -e WSE_MGR_PASS=clavesecreta \
    -v $(pwd)/applications:/usr/local/WowzaStreamingEngine/applications \
    -v $(pwd)/conf:/usr/local/WowzaStreamingEngine/conf \
    -v $(pwd)/content:/usr/local/WowzaStreamingEngine/content \
    --entrypoint /sbin/entrypoint.sh \
    wowzamedia/wowza-streaming-engine-linux:4.8.17
