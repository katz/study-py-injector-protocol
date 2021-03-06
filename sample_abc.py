from abc import abstractmethod, ABCMeta
from typing import NewType, Optional, List
from injector import Injector, Module, singleton
from dataclasses import dataclass

# int型に別名を付けておく
UserId = NewType("UserId", int)


# Entityのつもり
@dataclass
class User:
    user_id: UserId
    name: str

    def __eq__(self, other: object):
        # user_idのみで比較する
        return isinstance(other, User) and (self.user_id == other.user_id)


class UserRepository(metaclass=ABCMeta):
    """ABCを使い、Userクラス用のレポジトリが備えるべきメソッドを定義しておく"""

    @abstractmethod
    def find_user_by_id(self, user_id: UserId) -> Optional[User]:
        ...

    @abstractmethod
    def get_all_users(self) -> List[User]:
        ...


class InMemoryUserRepository(UserRepository):
    """インメモリーなUserレポジトリのつもり"""

    def __init__(self):
        user_id = UserId(12345)
        self.users = {
            user_id: User(user_id=user_id, name="test name"),
        }

    def find_user_by_id(self, user_id: UserId) -> Optional[User]:
        return self.users.get(user_id)


def configure(binder):
    """UserRepositoryを実装したクラスとして、InMemoryUserRepositoryを返すようにInjectorを設定する"""
    binder.bind(UserRepository, to=InMemoryUserRepository, scope=singleton)


class DatabaseModule(Module):
    pass


if __name__ == "__main__":
    # Injectorの初期化
    injector = Injector([configure, DatabaseModule()])

    # InjectorはUserRepositoryを実装したInMemoryUserRepositoryクラスのインスタンスを作り取り出そうとするが、
    # InMemoryUserRepositoryクラスはget_all_users()を実装していないので、実行時にエラーになる。
    # mypyがinjector.get(UserRepository)でエラーを出すので、# type: ignoreを付与してる
    repo: UserRepository = injector.get(UserRepository)

    # 上の文でエラーになるので、ここまでたどり着かない。
    user = repo.find_user_by_id(UserId(12345))

    if user:
        print("user_id:{0}, name:{1}".format(user.user_id, user.name))

    # ここもたどり着かない
    repo.get_all_users()
