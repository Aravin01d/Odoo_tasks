from odoo import Command,fields, models

class AccountMove(models.Model):
    """Inherits account move model."""
    _inherit = 'account.move'

    source_loc_id=fields.Many2one("stock.location", string="Source Location")
    destination_loc_id=fields.Many2one("stock.location", string="Destination Location")
    picking_type_id=fields.Many2one("stock.picking.type",string="Picking Type")
    picking_id=fields.Many2one("stock.picking",string="Picking")

    def action_post(self):
        """Function to create stock move when invoice is posted."""
        res=super().action_post()
        print("Picking type:",self.picking_type_id.name)


        for products in self.invoice_line_ids:


        picking=self.env['stock.picking'].create({
            'location_id': self.source_loc_id.id,
            'location_dest_id':self.destination_loc_id.id,
            'partner_id': self.partner_id.id,
            'picking_type_id':self.picking_type_id.id,
            'move_type': 'direct',
            'move_ids':[Command.create({
                'state':'draft',
                'location_id':self.source_loc_id.id,
                'location_dest_id':self.destination_loc_id.id,
                'product_id':self.invoice_line_ids.product_id.id,
                'product_uom_qty':self.invoice_line_ids.quantity,
            }) ]
            })
        self.picking_id=picking.id
        picking.action_confirm()
        # for move in picking.move_ids:
        #     self.env['stock.move.line'].create({
        #
        #         'move_id': move.id,
        #         'product_id': move.product_id.id,
        #         'product_uom_id': move.product_uom.id,
        #         'location_id': move.location_id.id,
        #         'location_dest_id': self.env.ref(
        #             'stock.stock_location_customers').id,
        #         'state': 'done',
        #         'picking_id': move.picking_id.id,
        #     })
        #
        #     picking.button_validate()

        return res

    def action_reverse(self):
        """Function to create stock move when invoice is reversed."""
        res=super().action_reverse()



        picking = self.env['stock.picking'].create({
            'location_id': self.destination_loc_id.id,
            'location_dest_id': self.source_loc_id.id,
            'partner_id': self.partner_id.id,
            'picking_type_id': self.picking_type_id.id,
            'move_type': 'direct',
            'move_ids': [Command.create({
                'state': 'draft',
                'location_id': self.destination_loc_id.id,
                'location_dest_id': self.source_loc_id.id,
                'product_id':self.invoice_line_ids.product_id.id,
            'product_uom_qty':self.invoice_line_ids.quantity,
            })]
        })

        picking.action_confirm()

        return res

    def action_get_stock_moves(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Moves',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id':self.picking_id.id,
        }