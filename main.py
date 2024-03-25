import http.server
from server import Server

server = http.server.HTTPServer(('localhost', 8080), Server)

if __name__ == '__main__':
    server.serve_forever()

# host = "localhost" '127.0.0.1'
# port = 8080
# server = http.server.HTTPServer((host, port), Server)
# server.serve_forever()
# from decimal import Decimal
# from urllib.parse import urlparse, parse_qs
#
# url = "http://localhost:8080/exchange?from=EUR&to=RUB&amount=10"
# result = urlparse(url)
# query_params = result.query
# # from_currency = query_params['from']
# # to_currency = query_params['to'][0]
# # amount = float(Decimal(query_params['amount'][0]))
# print(parse_qs(query_params))
# # print(from_currency)