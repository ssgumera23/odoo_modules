# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CustomWarehouseStockRequest(models.Model):
    _name = 'custom.warehouse.stock.request'
    _description = "Warehouse Stock Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string="Name",
        readonly=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Contact",
        required=True,
        default=lambda self: self.env.user.partner_id,
        readonly=True,
        copy=False,
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)]}
    )
    request_date = fields.Datetime(
        string="Requested Date",
        default=lambda self: fields.Datetime.now(),
        required=True,
        readonly=True,
        copy=False,
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)]}
    )
    picking_type_id = fields.Many2one(
        'stock.picking.type',
        string="Operation Type",
        required=True,
        readonly=True,
        default=lambda self: self.get_default_picking(),
        # default=lambda self: self.env.user.property_warehouse_id.id,
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)]}
    )
    location_id = fields.Many2one(
        'stock.location',
        string="Source Location",
        domain=lambda self: self._set_domain_location_ids(),
        required=True,
        readonly=True,
        # default=lambda self: self.get_default_loc(),
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)]}
    )
    location_dest_id = fields.Many2one(
        'stock.location',
        string="Destination Location",
        domain=lambda self: self._set_domain_location_ids(),
        required=True,
        readonly=True,
        # default=lambda self: self.get_default_dest(),
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)]}
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        store=True,
        change_default=True,
        required=True,
        default=lambda self: self.env.company,
        readonly=True,
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)]}
    )
    created_user_id = fields.Many2one(
        'res.users',
        string="Created By",
        readonly=True,
        default=lambda self: self.env.user,
        copy=False
    )
    approve_user_id = fields.Many2one(
        'res.users',
        string="Approved By",
        readonly=True,
        copy=False
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('done', 'Received'),
        ('cancel', 'Cancelled')],
        default='draft',
        string="Status",
        copy=False
    )
    warehouse_stock_request_line_ids = fields.One2many(
        'custom.warehouse.stock.request.line',
        'stock_request_id',
        string="Request Lines",
        readonly=True,
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)]}
    )
    note = fields.Text(
        string="Notes",
        readonly=True,
        copy=True,
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)]}
    )

    def _set_domain_location_ids(self):
        location_ids = self.env.user.allowed_location_ids.ids
        return [('id', 'in', location_ids)]

    def get_default_picking(self):
        def_pick = self.env['stock.picking.type'].search(
            [('code', '=', 'internal'), ('warehouse_id', '=', self.env.user.property_warehouse_id.id),
             ('active', '=', True)])
        return def_pick

    def get_default_loc(self):
        # def_loc = self.env['stock.location'].search([('name', '=', 'Warehouse')])
        def_loc = self.env['stock.location'].search([('id', 'in', self.env.user.allowed_location_ids)])
        return def_loc

    def get_default_dest(self):
        def_dest = self.env['stock.location'].search([('name', '=', self.env.user.name)])
        return def_dest

    def action_warehouse_stock_request_send(self):
        self.ensure_one()
        template = self.env.ref('warehouse_stock_request.email_template_edi_warehouse_stock_request')
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='custom.warehouse.stock.request',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            custom_layout='mail.mail_notification_light',
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    # @api.onchange('picking_type_id')
    # def onchange_picking_type_id(self):
    #     for rec in self:
    #         rec.location_dest_id = rec.picking_type_id.default_location_dest_id.id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('custom.warehouse.stock.request')
        return super(CustomWarehouseStockRequest, self).create(vals_list)

    def show_transfers_picking(self):
        self.ensure_one()
        action = self.env.ref("stock.action_picking_tree_all")
        action = action.sudo().read()[0]
        action['domain'] = str([('stock_request_id', '=', self.id)])
        action['context'] = {'default_stock_request_id': self.id}
        return action

    def show_product_on_hand(self):
        self.ensure_one()
        action = self.env.ref("stock.dashboard_open_quants")
        action = action.sudo().read()[0]
        product_ids = []
        for line in self.warehouse_stock_request_line_ids:
            product_ids.append(line.product_id.id)
        action['domain'] = str([('product_id', 'in', product_ids)])
        action['context'] = {
            'search_default_on_hand': 1,
            'search_default_productgroup': 1,
        }
        return action

    def custom_action_confirmed(self):
        for rec in self:
            rec.state = 'confirmed'

    def custom_action_approved(self):
        action = self.env.ref("stock.action_picking_tree_all").sudo().read()[0]
        self.ensure_one()
        default_partner_id = self.env['res.partner'].search([('name', '=', self.created_user_id.name)])
        context = {
            'default_partner_id': default_partner_id.id,
            'default_picking_type_id': self.picking_type_id.id,
            'default_location_id': self.location_id.id,
            'default_location_dest_id': self.location_dest_id.id,
            'default_scheduled_date': self.request_date,
            'default_stock_request_id': self.id,
            'is_warehouse_stock_request': True,
        }
        line_vals = []
        for line in self.warehouse_stock_request_line_ids:
            line_vals.append((0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': line.demand_qty,
                'product_uom': line.product_uom.id,
                'description_picking': line.description,
                'name': line.description,
                'company_id': line.company_id.id,
                'picking_type_id': line.stock_request_id.picking_type_id.id,
                'location_id': line.stock_request_id.location_id.id,
                'location_dest_id': line.stock_request_id.location_dest_id.id,
            }))
        if line_vals:
            context.update({
                'default_move_ids_without_package': line_vals
            })
        self.state = 'approved'
        action['context'] = context
        action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
        return action

    def custom_action_done(self):
        for rec in self:
            picking_ids = self.env['stock.picking'].search([('stock_request_id', '=', rec.id)])
            if picking_ids:
                rec.approve_user_id = self.env.user.id

                if any(p.state not in ['done', 'cancel'] for p in picking_ids):
                    raise UserError(
                        _('Still picking transfer related to this request is not done yet so please validate it first.'))
            rec.state = 'done'

    def custom_action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def custom_action_draft(self):
        for rec in self:
            rec.state = 'draft'


class CustomWarehouseStockRequestLine(models.Model):
    _name = 'custom.warehouse.stock.request.line'
    _description = "Warehouse Stock Request Line"

    stock_request_id = fields.Many2one(
        'custom.warehouse.stock.request',
        string="Warehouse Stock Request",
        copy=False,
    )
    product_id = fields.Many2one(
        'product.product',
        string="Product",
        required=True
    )
    description = fields.Char(
        string='Description',
        required=True,
    )
    product_uom = fields.Many2one(
        'uom.uom',
        string="UOM",
        required=True
    )
    demand_qty = fields.Float(
        string="Demand Qty",
        required=True
    )
    company_id = fields.Many2one(
        string='Company',
        store=True,
        readonly=True,
        related='stock_request_id.company_id',
        change_default=True,
        default=lambda self: self.env.company
    )

    @api.onchange('product_id')
    def onchange_product(self):
        for rec in self:
            rec.description = rec.product_id.display_name
            rec.product_uom = rec.product_id.uom_id.id
