from abc import ABCMeta, abstractproperty
from hashlib import md5
import pickle


class RedisModel(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def id_(self):
        pass

    @classmethod
    def redis_key(cls, id_):
        return 'object: class={cls}, id={id_}'.format(cls=cls.__class__.__name__, id_=id_)

    @classmethod
    def from_redis(cls, redis_client, id_):
        user = redis_client.get(cls.redis_key(id_))
        if user:
            return pickle.loads(user)

    def to_redis(self, redis_client):
        redis_client.set(self.redis_key(self.id_), pickle.dumps(self))


class User(RedisModel):
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    @property
    def id_(self):
        return self.username

    def check_password(self, password_attempt):
        return self.hash_password(password_attempt) == self.password

    @staticmethod
    def hash_password(password):
        return md5(password).hexdigest()

    def __repr__(self):
       return "<User(name='%s', password='%s')>" % (self.username, self.password)
