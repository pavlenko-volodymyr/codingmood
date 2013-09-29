from django.contrib.auth.models import User
import factory as factory_boy


TEST_USER_PASSWORD = 1


class UserFactory(factory_boy.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory_boy.Sequence(lambda n: 'person{0}'.format(n))
    first_name = factory_boy.Sequence(lambda n: 'John{0}'.format(n))
    last_name = factory_boy.Sequence(lambda n: 'Doe{0}'.format(n))
    email = factory_boy.Sequence(lambda n: 'person{0}@example.com'.format(n))
    is_active = True
    is_superuser = False
    is_staff = False
    password = TEST_USER_PASSWORD

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
