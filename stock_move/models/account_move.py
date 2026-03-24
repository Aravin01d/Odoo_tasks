from odoo import Command,fields, models, api
from odoo.exceptions import ValidationError
class AccountMove(models.Model):
    """Inherits account move model."""
    _inherit = 'account.move'

    source_loc_id = fields.Many2one("stock.location", string="Source Location")
    destination_loc_id = fields.Many2one("stock.location", string="Destination Location")
    picking_type_id = fields.Many2one("stock.picking.type",string="Picking Type")
    picking_id = fields.Many2one("stock.picking",string="Picking")
    rev_picking_id = fields.Many2one("stock.picking",string="Reverse Picking")

    def action_post(self):
        """Function to create stock move when invoice is posted."""
        res = super().action_post()
        if self.move_type == 'out_invoice':
            l = []
            for item in self.invoice_line_ids:
                if item.product_id.is_storable == True:
                    l+=[(fields.Command.create({
                        'state': 'draft',
                        'location_id': self.source_loc_id.id,
                        'location_dest_id': self.destination_loc_id.id,
                        'product_id': item.product_id.id,
                        'product_uom_qty': item.quantity
                    }))]

                    if l:
                        picking = self.env['stock.picking'].create({
                            'location_id': self.source_loc_id.id,
                            'location_dest_id':self.destination_loc_id.id,
                            'partner_id': self.partner_id.id,
                            'picking_type_id':self.picking_type_id.id,
                            'move_type': 'direct',
                            'move_ids':[product for product in l]
                            })
                        self.picking_id = picking.id
                        picking.action_confirm()

        if self.move_type == 'out_refund':
            for product in self.invoice_line_ids:
                for items in self.picking_id.move_line_ids:
                    if product.quantity > items.quantity:
                        raise ValidationError("Quantity more than invoiced.")
            l = []
            for item in self.invoice_line_ids:
                if item.product_id.is_storable == True:
                    l += [(fields.Command.create({
                        'state': 'draft',
                        'location_id': self.source_loc_id.id,
                        'location_dest_id': self.destination_loc_id.id,
                        'product_id': item.product_id.id,
                        'product_uom_qty': item.quantity
                    }))]
                    if l:
                        rev_picking = self.env['stock.picking'].create({
                            'location_id': self.source_loc_id.id,
                            'location_dest_id': self.destination_loc_id.id,
                            'partner_id': self.partner_id.id,
                            'picking_type_id': self.picking_type_id.id,
                            'move_type': 'direct',
                            'move_ids': [product for product in l]
                        })
                        self.rev_picking_id = rev_picking.id
                        rev_picking.action_confirm()

        return res

    def action_reverse(self):
        """Function to raise error if picking not performed before reversing move."""
        res=super().action_reverse()
        if self.source_loc_id and self.destination_loc_id and self.picking_id.state != 'done' :
            raise ValidationError("Picking not performed")

        return res

    def action_get_stock_moves(self):
        """Function to display moves smart button."""
        for products in self.invoice_line_ids:
            if products.product_id.is_storable == True:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Moves',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'stock.picking',
                    'res_id':self.picking_id.id,
                }

    def action_get_reverse_stock_moves(self):
        """Function to display reverse move smart button."""
        for products in self.picking_id.move_line_ids:
            if products.product_id.is_storable == True:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Reverse Moves',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'stock.picking',
                    'res_id':self.rev_picking_id.id
                }
