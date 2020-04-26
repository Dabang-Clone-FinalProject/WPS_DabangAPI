from django.db import models

from config import settings


def post_image_path(instance, filename):
    a = f'{instance.id}/{filename}'
    return a


def security_image_path(instance, filename):
    a = f'{instance.id}/{filename}'
    return a


def broker_image_path(instance, filename):
    a = f'{instance.id}/{filename}'
    return a


class PostRoom(models.Model):
    broker = models.ForeignKey(
        'posts.Broker',
        on_delete=models.SET_NULL,
        null=True,
    )
    HEATING_ZONE = (
        ('Center', '중앙'),
        ('Division', '개별'),
        ('Area', '지역'),
    )
    type = models.CharField('매물 종류', max_length=10, null=True, )
    description = models.TextField(max_length=500, verbose_name='설명', )
    address = models.ForeignKey(
        'posts.PostAddress',
        on_delete=models.CASCADE, null=True,
    )
    salesForm = models.OneToOneField(
        'posts.SalesForm',
        on_delete=models.CASCADE, null=True,
    )
    # 위도 경도
    lat = models.FloatField('x축', null=True, )
    lng = models.FloatField('y축', null=True, )

    floor = models.CharField(null=True, verbose_name='층 수', max_length=5)
    totalFloor = models.CharField(null=True, verbose_name='건물 층 수', max_length=5)
    areaChar = models.CharField(verbose_name='문자형 전용 면적', max_length=20, null=True, )
    supplyAreaInt = models.IntegerField(verbose_name='정수형 공급 면적', )
    supplyAreaChar = models.CharField(verbose_name='문자형 공급 면적', max_length=10, null=True, )
    shortRent = models.NullBooleanField('단기임대', default=None, )
    management = models.ManyToManyField(
        'posts.AdministrativeDetail',
        through='MaintenanceFee',
    )

    parkingDetail = models.CharField(verbose_name='주차 비용', null=True, max_length=10)
    parkingTF = models.NullBooleanField('주차 가능 유무', default=None)
    parkingPay = models.FloatField('주차 비용', null=True, )

    living_expenses = models.CharField('생활비', null=True, max_length=15, )
    living_expenses_detail = models.CharField('생활비 항목', null=True, max_length=20, )

    moveInChar = models.CharField('크롤링용 입주날짜', null=True, max_length=10)
    moveInDate = models.DateTimeField(verbose_name='입주 가능 날짜', null=True, )
    #
    option = models.ManyToManyField('OptionItem', through='RoomOption', verbose_name='옵션 항목')
    heatingType = models.CharField('난방 종류', max_length=10)

    pet = models.NullBooleanField('반려동물', default=None)
    elevator = models.NullBooleanField('엘레베이터', default=None)
    builtIn = models.NullBooleanField('빌트인', default=None)
    veranda = models.NullBooleanField('베란다/ 발코니', default=None)
    depositLoan = models.NullBooleanField('전세 자금 대출', default=None)
    totalCitizen = models.CharField('총 세대 수', max_length=10, null=True, )
    totalPark = models.CharField('세대당 주차 대수', max_length=10, null=True, )
    complete = models.CharField('준공 년 월', max_length=10, null=True, )
    #
    securitySafety = models.ManyToManyField(
        'posts.SecuritySafetyFacilities',
        through='RoomSecurity',
    )

    @staticmethod
    def project_crawling_start():
        from posts.crawling.postFind import postFind
        postFind()


class PostAddress(models.Model):
    # address = models.ForeignKey('posts.PostRoom', on_delete=models.CASCADE, null=True)
    loadAddress = models.CharField(max_length=50, null=True,)
    detailAddress = models.CharField(max_length=30, null=True, )


class SalesForm(models.Model):
    type = models.CharField(max_length=10, verbose_name='매물 종류', )
    depositChar = models.CharField(null=True, verbose_name='문자형 매매-보증금', max_length=10)  # 보증금
    monthlyChar = models.CharField(null=True, verbose_name='문자형 월세', max_length=10)  # 월세
    depositInt = models.IntegerField('정수형 매매-보증금', null=True, )
    monthlyInt = models.IntegerField('정수형 월세', null=True, )

    @staticmethod
    def start():
        type_list = ['매매', '전세', '월세']
        for i in type_list:
            SalesForm.objects.create(
                type=i,
            )


class MaintenanceFee(models.Model):
    postRoom = models.ForeignKey('posts.PostRoom', verbose_name='해당 매물', on_delete=models.CASCADE,
                                 related_name='management_set')
    admin = models.ForeignKey('posts.AdministrativeDetail', verbose_name='포함 항목', on_delete=models.CASCADE, )
    totalFee = models.FloatField(verbose_name='관리비 합계')


# 관리비 포함 항목
class AdministrativeDetail(models.Model):
    name = models.CharField(max_length=10, verbose_name='포함 항목 물품')

    def __str__(self):
        return '{}'.format(self.name)


class OptionItem(models.Model):
    name = models.CharField('옵션 항목 아이템', max_length=10, )
    image = models.ImageField('옵션 이미지', null=True, )

    def __str__(self):
        return '{}'.format(self.name)


class SecuritySafetyFacilities(models.Model):
    name = models.CharField('보안/안전 시설 아이템', max_length=10, null=True)
    image = models.ImageField('시설 이미지', null=True, upload_to=security_image_path, )

    def __str__(self):
        return '{}'.format(self.name)


class PostLike(models.Model):
    post = models.ForeignKey('posts.PostRoom', on_delete=models.CASCADE, )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True, )


class RoomOption(models.Model):
    postRoom = models.ForeignKey('posts.PostRoom', verbose_name='해당 매물', on_delete=models.CASCADE,
                                 related_name='option_set')
    option = models.ForeignKey('OptionItem', verbose_name='해당 옵션', on_delete=models.CASCADE,
                               related_name='optionname_set')
    created_at = models.DateTimeField(auto_now_add=True, )


class RoomSecurity(models.Model):
    postRoom = models.ForeignKey('posts.PostRoom', verbose_name='해당 매물', on_delete=models.CASCADE,
                                 related_name='securitySafety_set')
    security = models.ForeignKey('posts.SecuritySafetyFacilities', verbose_name='보안 안전 시설', on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True, )


class Broker(models.Model):
    companyName = models.CharField('회사 명', max_length=30, null=True, )
    address = models.CharField('주소', max_length=50, null=True, )
    managerName = models.CharField('중개인', max_length=30, null=True, )
    tel = models.CharField('전화번호', max_length=13, null=True, )
    image = models.ImageField('이미지', upload_to=broker_image_path, null=True, )
    companyNumber = models.CharField('사업자 번호', max_length=20, null=True, )
    brokerage = models.CharField('중개등록번호', max_length=30, null=True, )
    dabangCreated_at = models.CharField('다방 가입일', max_length=20, null=True, )
    successCount = models.CharField('거래 성공 횟수', max_length=20, null=True, )


class PostImage(models.Model):
    image = models.ImageField(upload_to=post_image_path, verbose_name='방 이미지', null=True, )
    post = models.ForeignKey(
        'posts.postRoom',
        verbose_name='해당 게시글',
        on_delete=models.CASCADE, related_name='postimage_set'
    )

    def __str__(self):
        return '{}'.format(self.image)
