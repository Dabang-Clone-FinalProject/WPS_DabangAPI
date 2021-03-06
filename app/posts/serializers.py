from rest_framework import serializers
from rest_framework.fields import DictField, CharField, ListField, SerializerMethodField
from rest_framework.relations import StringRelatedField

from .models import PostRoom, PostImage, Broker, MaintenanceFee, RoomOption, PostAddress, RoomSecurity, SalesForm, \
    OptionItem, SecuritySafetyFacilities, ComplexInformation, ComplexImage, RecommendComplex, PostLike, UploadImage

from django.db.models import Max


class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = (
            'pk', 'companyName', 'address', 'managerName', 'tel', 'image', 'companyNumber', 'brokerage',
            'dabangCreated_at', 'successCount'
        )


class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceFee
        fields = (
            'postRoom', 'admin', 'totalFee',
        )


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionItem
        fields = (
            'name',
        )


class SecuritySafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySafetyFacilities
        fields = (
            'name',
        )


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAddress
        fields = (
            'loadAddress', 'detailAddress',
        )


class SalesFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesForm
        fields = (
            'type', 'depositChar', 'monthlyChar', 'depositInt', 'monthlyInt',
        )


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = (
            'image',
        )


class RecommendComplexSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendComplex
        fields = '__all__'


class ComplexImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexImage
        field = 'image'


class ComplexInformationSerializer(serializers.ModelSerializer):
    image = serializers.StringRelatedField(source='compleximage_set', many=True, )
    list = serializers.SerializerMethodField()
    countPost = serializers.SerializerMethodField(read_only=True)

    def get_countPost(self, obj):
        return obj.postroom_set.count()

    def get_list(self, obj):
        import random

        pk_list = []
        while True:
            max_id = ComplexInformation.objects.all()
            max_id = len(max_id)
            pk = random.randint(1, max_id)
            ins = ComplexInformation.objects.get(pk=pk)
            if ins.pk in pk_list:
                pass
            else:
                pk_list.append(ins.pk)
            if len(pk_list) >= 4:
                break
        return pk_list

    class Meta:
        model = ComplexInformation
        fields = (
            'pk',
            'complexName',
            'buildDate',
            'totalCitizen',
            'personalPark',
            'totalNumber',
            'heatingSystem',
            'minMaxFloor',
            'buildingType',
            'constructionCompany',
            'fuel',
            'complexType',
            'floorAreaRatio',
            'dryWasteRate',
            'complexSale',
            'complexPrice',
            'areaSale',
            'areaPrice',
            'image',
            'list',
            'countPost',
        )


class PostListSerializer(serializers.ModelSerializer):
    broker = BrokerSerializer(read_only=True)
    management_set = serializers.StringRelatedField(source='management', many=True, read_only=True)
    option_set = serializers.StringRelatedField(source='option', many=True, read_only=True)
    securitySafety_set = serializers.StringRelatedField(source='securitySafety', many=True, read_only=True)
    address = AddressSerializer(read_only=True, allow_null=True)
    salesForm = SalesFormSerializer(read_only=True)
    postimage = serializers.StringRelatedField(source='postimage_set', many=True)
    complex = ComplexInformationSerializer(read_only=True, )

    class Meta:
        model = PostRoom
        fields = [
            'pk',
            'broker',
            'type',
            'description',
            'address',
            'lng',
            'lat',
            'salesForm',
            'floor',
            'totalFloor',
            'areaChar',
            'supplyAreaInt',
            'supplyAreaChar',
            'shortRent',
            'management_set',
            'parkingDetail',
            'parkingTF',
            'living_expenses',
            'living_expenses_detail',
            'moveInChar',
            'moveInDate',
            'option_set',
            'heatingType',
            'pet',
            'elevator',
            'builtIn',
            'veranda',
            'depositLoan',
            'totalCitizen',
            'totalPark',
            'complete',
            'securitySafety_set',
            'postimage',
            'complex',
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    salesForm = SalesFormSerializer(read_only=True)
    management_set = ListField()
    option_set = ListField()
    securitySafety_set = ListField()
    postimage = serializers.ImageField(use_url=True)


    class Meta:
        model = PostRoom
        fields = [
            'pk',
            'broker',
            'type',
            'description',
            'salesForm',
            'floor',
            'totalFloor',
            'areaChar',
            'supplyAreaInt',
            'supplyAreaChar',
            'shortRent',
            'management_set',
            'parkingDetail',
            'parkingTF',
            'living_expenses',
            'living_expenses_detail',
            'moveInChar',
            'moveInDate',
            'option_set',
            'heatingType',
            'pet',
            'elevator',
            'builtIn',
            'veranda',
            'depositLoan',
            'totalCitizen',
            'totalPark',
            'complete',
            'securitySafety_set',
            'address',
            'postimage',
        ]


class PostLIkeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = [
            'post',
            'user',
        ]


class PostLikeUserSerializer(serializers.ModelSerializer):
    post = PostListSerializer()

    class Meta:
        model = PostLike
        fields = [
            'post',
        ]


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = (
            'image',
        )
