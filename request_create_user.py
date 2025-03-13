import configuration
import requests
import data

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)

def post_products_kits(body):
    return requests.post(configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH,
                         json=body)

response = post_new_user(data.user_body)
print(response.status_code)
print(response.json())

print(configuration.DIVIDER)

response = post_products_kits(data.product_ids)
print(response.status_code)
print(response.json())

print(configuration.DIVIDER)