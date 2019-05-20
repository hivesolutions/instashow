# [Instashow](http://instashow.hive.pt)

Web application designed to show instagram images on projector.

## Dockerfile

```bash
mkdir instashow && cd instashow
wget https://github.com/hivesolutions/instashow/raw/master/Dockerfile
docker build --no-cache -t self/instashow .
cd .. && rm -rf instashow
```

```bash
docker run --name instashow -p 0.0.0.0:8080:8080 -i -t self/instashow
```

## Configuration

| Name | Type | Description |
| ----- | ----- | ----- |
| **TITLE** | `str` | Top title for the slideshow presentation (eg: My photos). |
| **SUB_TITLE** | `str` | The lower text value that will be present in slideshow. |
| **BASE_URL** | `str` | The base URL/URI for the API callbacks (eg: http://instashow.bemisc.com/). |
| **INSTAGRAM_ID** | `str` | Identifier of the Instagram API client. |
| **INSTAGRAM_SECRET** | `str` | Secret key for the API Client (should not be shared). |
| **INSTAGRAM_REDIRECT_URL** | `str` | The full URI for the redirection after OAuth completed. |
