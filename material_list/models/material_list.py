from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaterialList(models.Model):
    _name = 'material.list'
    _description = 'Material List'
    
    name = fields.Char('Material Name', required=True)
    material_code = fields.Char('Material Code', required=True)

    material_type = fields.Selection([('fabric', 'Fabric'), ('jeans', 'Jeans'), ('cotton', 'Cotton')], string="Material Type",  required=True, default='fabric')
    material_price = fields.Float('Material Buy Price')
    supplier_id = fields.Many2one(
        'supplier.list', string='Related Supplier', required=True)

    
    @api.constrains('material_price')
    def limit_value(self):
        for record in self:
            if record.material_price < 100.0:
                raise ValidationError("Harga harus diatas 100")
            
    


    

class Supplier(models.Model):
    _name = 'supplier.list'
    _description = 'Supplier'
    
    name = fields.Char(string='Name', required=True)


    _sql_constraints = [
    ('name_unique', 'unique(name)', 'name already exists!')
]
