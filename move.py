# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.model import ModelView
from trytond.pyson import Eval
from trytond.transaction import Transaction
from trytond.i18n import gettext
from trytond.exceptions import UserError


class Move(metaclass=PoolMeta):
    __name__ = 'account.move'

    allow_draft = fields.Function(
        fields.Boolean("Allow Draft Move"), 'get_allow_draft')

    @classmethod
    def __setup__(cls):
        super(Move, cls).__setup__()
        if 'state' not in cls._check_modify_exclude:
            cls._check_modify_exclude.append('state')
        cls._buttons.update({
            'draft': {
                'invisible': ~Eval('allow_draft', False),
                'depends': ['allow_draft'],
                },
            })

    def get_allow_draft(self, name):
        if self.state == 'draft' or self.origin is not None:
            return False
        lines = [line for line in self.lines if line.origin is not None]
        if lines:
            return False
        return True

    @classmethod
    @ModelView.button
    def draft(cls, moves):
        Line = Pool().get('account.move.line')

        # Add the possiblity to allow draft a move event it has an origin.
        # In some special cases is needed.
        allow_draft = Transaction().context.get('move_allow_draft', False)
        if not allow_draft:
            for move in moves:
                if not move.allow_draft:
                    raise UserError(gettext(
                            'account_move_draft.msg_draft_not_allowed',
                            move=move.number,
                            ))

        cls.write(moves, {
            'state': 'draft',
            })
        Line.check_modify([l for m in moves for l in m.lines])
