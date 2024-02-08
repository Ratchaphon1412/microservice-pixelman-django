from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *

from .models import *
# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from infrastructure.kafka.producer import ProducerKafka
from infrastructure.service import Facade


class RegisterAPIView(APIView):
    def post(self, request):
        """
        Create new user

        Return: Message
        Required: Username, Email, Password, Confirm Password


        """

        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            ShoppingCart.objects.create(user=serializer.instance, total=0)
            
            producer = ProducerKafka()
            service = Facade()
            print(serializer.data)
            # generate token verify email
            token = service.security.encrypt.verify_email_encryption(
                serializer.data['email'], serializer.data['id'])
            # send token to email service
            verify_email = {
                "to": serializer.data['email'],
                "link": settings.BASE_URL_FRONTEND +"verify/account/"+token,
            }
            producer.publish('email-service-topic', 'verify', verify_email)

            # serialized_data = {'user': serializer.data}
            producer.publish('payment-service-topic', 'create_user', serializer.data)

            return Response({"message": "Create User Success!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReverifyEmailAPIView(APIView):
    def post(self, request):
        """
        Reverify email

        Return: Message
        Required: Email


        """

        serializer = ReverifyEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            producer = ProducerKafka()
            service = Facade()
            user = UserProfiles.objects.filter(
                email=serializer.data['email']).first()

            # generate token verify email
            token = service.security.encrypt.verify_email_encryption(
                serializer.data['email'], user.id)
            # send token to email service
            verify_email = {
                "to": serializer.data['email'],
                "link": settings.BASE_URL_FRONTEND +"verify/account/"+token,
            }
            producer.publish('email-service-topic', 're-verify', verify_email)

            return Response({"message": "Reverify Email Success!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActiveUserAPIView(APIView):
    def post(self, request):
        """
        Active user

        Return: Message
        Required: Email


        """

        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            service = Facade()
            decryption = service.security.encrypt.verify_email_decryption(
                serializer.data.get("token"))
            _, uid = decryption.split(",")

            userUid = UserProfiles.objects.filter(
                id=uid).first()
            if userUid:
                userUid.is_email_verified = True
                userUid.save()
                return Response({"message": "Active User Success!"}, status=status.HTTP_200_OK)
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UserProfilesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Authorization 

        Return: User Profile
        Required: Authenticated
        """

        user = request.user
        serializer = UserProfilesSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Update user profile

        Return: Message
        Required: Authenticated

        """

        user = request.user
        serializer = UserProfilesUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            address = Address.objects.filter(
                address_id=serializer.validated_data.get("address_id")).first()
            if address:
                serializer.update(user, serializer.validated_data)

                return Response({"message": "Update User Success!"}, status=status.HTTP_200_OK)

        return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)


class AddressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get all address of user

        Return: List of address 
        Required: Authenticated

        """
        user = request.user
        address = Address.objects.filter(user=user)
        serializer = AddressSerializer(address, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create new address

        Return: Message
        Required: Authenticated

        """

        user = request.user
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response({"message": "Create Address Success!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Update address

        Return: Message
        Required: Authenticated

        """
        if not request.data.get("address_id"):
            return Response({"error": "address_id not found in request data"}, status=status.HTTP_400_BAD_REQUEST)

        address = request.user.address_set.filter(
            address_id=request.data.get("address_id")).first()

        serializer = AddressSerializer(address, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.update(address, serializer.validated_data)
            return Response({"message": "Update Address Success!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Delete address

        Return: Message
        Required: Authenticated

        """
        user = request.user

        address_id = request.data.get("address_id")

        if not address_id:
            return Response({"error": "address_id not found in request data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            address = Address.objects.get(address_id=address_id, user=user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

        address.delete()

        return Response({"message": "Delete Address Success!"}, status=status.HTTP_200_OK)


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get all cart of user

        Return: List of cart 
        Required: Authenticated

        """
        cart = Cart.objects.filter(user=request.user)
        shop = ShoppingCart.objects.get(user=request.user)

        serializers  = CartSerializer(cart, many=True)
        shopSerialize = ShoppingCartSerializer(shop)
        
        
        
        return Response({"cart":serializers.data, "shopping_cart":shopSerialize.data}
             , status=status.HTTP_200_OK)
    

    def post(self, request):
        """
        Create new cart

        Return: Message
        Required: Authenticated

        """
        product_serializer = ProductValidateSerializer(data=request.data)
        
        if product_serializer.is_valid(raise_exception=True):
            product,_ = Product.objects.get_or_create(
                product_id=product_serializer.validated_data.get("product_id"),
                name=product_serializer.validated_data.get("name"),
                price=product_serializer.validated_data.get("price"),
                image=product_serializer.validated_data.get("image"),
                category=product_serializer.validated_data.get("category")
                
                )
                
            if product:
                serializer = CartValidateSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    cart,create = Cart.objects.get_or_create(
                        user=request.user,
                        product=product,
                        quantity=serializer.validated_data.get("quantity"),
                        size=serializer.validated_data.get("size"),
                        color=serializer.validated_data.get("color")
                    )
                    
                    if create:
                        shopping,createShoppingCart= ShoppingCart.objects.get_or_create(
                            user=request.user,
                            
                        )
                        
                        if createShoppingCart:
                            shopping.total = product.price * serializer.validated_data.get("quantity")
                            shopping.save()
                            return Response({"message": "Create Cart Success!"}, status=status.HTTP_201_CREATED)
                        else:
                            shopping.total += product.price * serializer.validated_data.get("quantity")
                            shopping.save()
                        return Response({"message": "Create Cart Success!"}, status=status.HTTP_201_CREATED)
                
                        
                    
                    return Response({"error": "Create Cart Failed or IF Product exist Please Update!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        """
        Update cart

        Return: Message
        Required: Authenticated

        """
        serializer = CartUpdateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            product = Product.objects.filter(product_id=serializer.validated_data.get("product_id")).first()

            if product:
                cart = Cart.objects.filter(user=request.user,product_id=product.id, size=serializer.validated_data.get("size"), color=serializer.validated_data.get("color")).first()
                
                if cart:
                   
                    # Update the cart details here
                    
                    cart.quantity = serializer.validated_data.get("quantity")
                    cart.save()
                    
                    return Response({"message": "Update Cart Success!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Product does not have  size and color do not match."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Product does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        """
        Delete cart

        Return: Message
        Required: Authenticated

        """
        serializer = CartDeleteSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            product = Product.objects.filter(product_id=serializer.validated_data.get("product_id")).first()

            if product:
                cart = Cart.objects.filter(user=request.user,product_id=product.id, size=serializer.validated_data.get("size"), color=serializer.validated_data.get("color")).first()
                
                if cart:
                    product = cart.product
                    shopping = ShoppingCart.objects.filter(user=request.user).first()
                    
                    shopping.total -= product.price * cart.quantity
                    
                    if shopping.total <= 0:
                        shopping.total = 0
                        
                    shopping.save()
                    
                    
                    
                    cart.delete()
                    
                    return Response({"message": "Delete Cart Success!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Product does not have  size and color do not match."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Product does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
