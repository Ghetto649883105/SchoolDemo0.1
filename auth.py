import jwt
#  HTTP异常安全的编码和解密令牌
from fastapi import HTTPException, Security
#  fastapi的http授权凭证,和http承载
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
#  创建用于哈希和验证密码的上下文
from passlib.context import CryptContext
#  日期时间和时间增量
from datetime import datetime, timedelta, timezone


#  权限处理
class AuthHandler:
    security = HTTPBearer()  # 检验Authorization是否符合Bearer <token>/含credentials:Token字符串
    pwd_context = CryptContext(schemes=["bcrypt"],  # 哈希生成和验证(算法列表,标记被淘汰的算法)
                               deprecated="auto")
    secret = "SECRET112"

    # 加密密码及验证加密后密码的两个函数,暂时未用
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)  # hash:哈希生成

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)  # verify:验证

    def encode_token(self, user_id):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=0, minutes=5),  # exp:过期时间
            "iat": datetime.now(timezone.utc),  # iat:签发时间
            "sub": user_id  # sub:主题,一般为用户id
            # "nbf":  # nbf:生效时间
            # "jti":  # jti:令牌id
        }
        return jwt.encode(  # 生成Token
            payload,  # claims:payload载荷
            self.secret,  # key:签名密钥
            algorithm="HS256",  # algorithm:签名算法
            # headers=  # JWT头部信息
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:  # 过期异常
            return {
                "status": False,
                "detail": "token过期"
            }
            # raise HTTPException(status_code=401, detail="过期")  # 向客户端返回HTTP错误响应
        except jwt.InvalidTokenError:  # 格式异常
            return {
                "status": False,
                "detail": "token不正确"
            }
            # raise HTTPException(status_code=401, detail="假token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
