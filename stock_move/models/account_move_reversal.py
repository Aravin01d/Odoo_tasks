from odoo import  models

class AccountMoveReversal(models.TransientModel):
    """Inherits account.move.reversal to swap locations for reverse move."""
    _inherit = "account.move.reversal"

    def refund_moves(self):
        """Function to set source and destination locations."""
        res = super().refund_moves()
        sl = self.new_move_ids.source_loc_id
        self.new_move_ids.source_loc_id = self.new_move_ids.destination_loc_id.id
        self.new_move_ids.destination_loc_id = sl.id
        return res