from user.models import UserProfiles


def updateVerifyEmail(data):

    print("verify email")
    # Use the data_dict dictionary as needed


def updateOmiseKey(topic,key,data):

    print(type(data), data["email"])
    
    if topic == "auth-service":
    
        if key == "create_token":
            user = UserProfiles.objects.filter(email=data["email"]).update(
            customer_omise_id=data["token"])

            if user:
                print("update omise success")
            else:
                print("update omise fail")

    # Use the data_dict dictionary as needed
