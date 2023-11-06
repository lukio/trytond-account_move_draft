# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._check_modify_exclude.add('validated_by')
        cls._check_modify_exclude.add('posted_by')
