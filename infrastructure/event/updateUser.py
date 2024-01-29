from user.models import UserProfiles


def updateVerifyEmail(data):

    print("verify email")
    # Use the data_dict dictionary as needed


def updateOmiseKey(data):

    print(type(data), data["email"])

    user = UserProfiles.objects.filter(email=data["email"]).update(
        customer_omise_id=data["token"])

    if user:
        print("update omise success")
    else:
        print("update omise fail")

    # Use the data_dict dictionary as needed
