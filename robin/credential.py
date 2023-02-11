import robin_stocks.robinhood as rs

class rbCredential:
    def __init__(self):
        print("roCredential")

    def login(self):
        print("robinhod login ..")
        robin_user = ""
        robin_pass = ""
        res= rs.login(username=robin_user,
                password=robin_pass,
                expiresIn=31540000, # 365 days
                by_sms=True)
        print(res)
        return rs

if __name__ == "__main__":
    rbCredential().login()