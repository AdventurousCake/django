# DRF, django needs disable csrf

def test():
    while True:
        r = requests.post('http://127.0.0.1:8000/login/', data={"username":username,"password":password})
        print(r.json())

for i in range(50):
    threading.Thread(target=test).start()
