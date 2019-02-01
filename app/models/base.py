from tortoise import fields
from tortoise.models import Model, ModelMeta as _ModelMeta

IGNORE_ATTRS = ['redis']


class PropertyHolder(type):  # 定义元类

    def __new__(cls, name, bases, attrs):  # 使用元类创建类时，会调用此方法
        '''
       :param name: 类名
       :param bases:  父类的元组
       :param attrs: dict类型，类的属性和函数
       :return:
       '''
        new_cls = type.__new__(cls, name, bases, attrs)
        new_cls.property_fields = []

        for attr in list(attrs) + sum([list(vars(base))
                                       for base in bases], []):
            if attr.startswith('_') or attr in IGNORE_ATTRS:
                continue
            if isinstance(getattr(new_cls, attr), property):
                new_cls.property_fields.append(attr)
        return new_cls


class ModelMeta(_ModelMeta, PropertyHolder):
    pass


class BaseModel(Model, metaclass=ModelMeta):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    _redis = None

    class Meta:
        abstract = True
