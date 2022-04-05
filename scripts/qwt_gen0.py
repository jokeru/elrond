import base64
import requests

tiers = [
  'bronze',
  'argent',
  'or',
  'platine',
  'diamant',
]
seats = [
  66000,
  22000,
  7330,
  2440,
  820
]

# get balance of @qowattrewards.elrond wallet
qowattrewards_addr = 'erd1xf9jyvhjf00h0kp6hc8m8d2580m8guhysm5d7fnm9j5wq2jj9v6qremln6'
url = f"https://api.elrond.com/accounts/{qowattrewards_addr}/tokens"
response = requests.get(url)
data = response.json()
qowattrewards = int(data[0]['balance']) / pow(10, data[0]['decimals'])
print(f"@qowattrewards.elrond wallet = {qowattrewards:,.0f} qwt\n")

# pull pre-mint contract data
print(f"pulling down all pre-mint contract transactions, please be patient, this takes a bit of time ...")
contract_addr = 'erd1qqqqqqqqqqqqqpgq0jdfyzt2afk3dc35y9s8q0t0qk2tc56a83gq6ftr00'
minted = {}
level = 1
used = 0
i = 0
for tier in tiers:
  hex = f"mint_{tier}_nft".encode('utf-8').hex()
  b64 = base64.b64encode(hex.encode('utf-8')).decode('utf-8').replace("=", "")
  url = f"https://api.elrond.com/accounts/{contract_addr}/transactions/count"
  qs = {
    "status": "success",
    "search": b64
  }
  response = requests.get(url, params = qs)
  if response.status_code != 200:
    print(f"error on the '{tier}' tier")
  data = response.text
  minted[tier] = int(data)
  ratio = minted[tier] * 100 / seats[i]
  print(f"- {tier} tier: minted {minted[tier]} seats out of {seats[i]} ({ratio:.2f}%)")
  used += minted[tier] * (10000 * level)
  i += 1
  level *= 3
print(f"total qwt used = {used:,.0f}")

# validate run
rewards = used * 0.7 # 70% goes towards the rewards wallet
if qowattrewards != rewards :
  print(f"\nHouston, we have a problem:\n{qowattrewards} != {rewards}")
