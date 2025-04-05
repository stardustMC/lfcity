from django_redis import get_redis_connection
from django.db.models import Q
from user.models import User
from django.contrib.auth.backends import ModelBackend, UserModel


def jwt_response_payload_handler(token, user=None, request=None):
    redis = get_redis_connection('cart')
    cart_count = redis.hlen('cart_%s' % user.id)
    return {
        'token': token,
        'cart_count': cart_count,
    }

def get_user_by_multi_account(account: str):
    """
    用户既可以使用username登录，也可以使用手机号phone，所以这两种信息都可以查询到用户
    """
    user = User.objects.filter(Q(username=account) | Q(phone=account)).first()
    return user


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 客户端也可能把username放到额外参数了
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        if username is None or password is None:
            return

        user = get_user_by_multi_account(username)
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user