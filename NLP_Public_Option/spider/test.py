from curl_cffi import requests

headers = {
    'referer': 'https://weibo.com/newlogin?tabtype=weibo&gid=1028034288&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2Fhot%2Fweibo%2F102803',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'cookie': 'SCF=AtuyUqXBFVnetuJXSD1Uu4jkcksrMHsmqArTmcQ0Vvz7KwvLqcjDdLSr_SoW7IjiB6IjauIByLBK5k3s0GcaaaA.; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WF7OroSG-H_98HyIRMcopgF5JpVF02NS0-pShMpeK.p; SUB=_2AkMfnIjndcPxrARYnvERz2_nbYVH-jysSeERAn7uJhMyAxh87moQqSVutBF-XBUzOL4y3hqAzeDgkEa0wtsr4A6m; XSRF-TOKEN=3kupyyrVNskqyxHyW839xMVy; WBPSESS=Dt2hbAUaXfkVprjyrAZT_JZ417LJEQncKUMDm21mjP4lVD5WsQe-8tUmQ6sDlx_6Y9lzRQiE7cmVQrFnq_JcqhFwAv4avMbR-9-DzCEt9HH5-2U8mhZIH1kCN-6Yx1rFkgVB6bfqsHpyk5769Lfbyw=='
}

params = {
    'id': '5208599758374910',
    'is_show_bulletin': 2,
}

# 使用 impersonate 参数来模仿浏览器的TLS指纹
response = requests.get(
    "https://weibo.com/ajax/statuses/buildComments",
    headers=headers,
    params=params,
    impersonate="chrome110"
)

print(response.json())
