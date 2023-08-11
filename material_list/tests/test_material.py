from odoo import exceptions
from odoo.tests import common


class MaterialListTest(common.TransactionCase):

    def setUp(self):
        
        super(MaterialListTest, self).setUp()
        self.material_list = self.env['material.list']
        self.supplier_list = self.env['supplier.list']

        self.supplier_data = {
            'name': 'Toko Maju Jaya',
        }
        self.supplier = self.supplier_list.create(self.supplier_data)

        self.material_data = {
            'name' : 'Material Celana Jeans',
            'material_code' : 'MCJ001',
            'material_type' : 'jeans',
            'material_price' : 150,
            'supplier_id' : self.supplier.id,
        }

        self.material = self.material_list.create(self.material_data)
        

    def test_create(self):
        self.assertEqual(self.material.name, 'Material Celana Jeans')
        self.assertEqual(self.material.material_code, 'MCJ001')
        self.assertEqual(self.material.material_type, 'jeans')
        self.assertEqual(self.material.material_price, 150)
        self.assertEqual(self.material.supplier_id.id, self.supplier.id)

    
    def test_invalid_price(self):

        with self.assertRaises(exceptions.ValidationError):
            self.material.write({
                'material_price': 50,
            })
    
    def test_update(self):
        self.material.write({'name': 'Celana Kain'})
        self.material.write({'material_code': 'MCK001'})
        self.material.write({'material_type': 'fabric'})
        self.material.write({'material_price': 300})

        self.assertEqual(self.material.name, 'Celana Kain')
        self.assertEqual(self.material.material_code, 'MCK001')
        self.assertEqual(self.material.material_type, 'fabric')
        self.assertEqual(self.material.material_price, 300)

    def test_filter(self):
        material_data_2 = {
            'name' : 'Material Celana Jeans 2',
            'material_code' : 'MCJ002',
            'material_type' : 'jeans',
            'material_price' : 250,
            'supplier_id' : self.supplier.id,
        }
        material_data_3 = {
            'name' : 'Material Celana Kain 3',
            'material_code' : 'MCK002',
            'material_type' : 'fabric',
            'material_price' : 300,
            'supplier_id' : self.supplier.id,
        }

        material_2 = self.material_list.create(material_data_2)
        material_3 = self.material_list.create(material_data_3)

        jeans_materials_item = self.material_list.search([('material_type', '=', 'jeans')])
        self.assertEqual(len(jeans_materials_item), 2)

        material_ids = jeans_materials_item.ids
        self.assertIn(material_2.id, material_ids)
        self.assertNotIn(material_3.id, material_ids)


    def test_delete(self): 
        self.material.unlink()
        jeans_materials_item = self.material_list.search([('material_type', '=', 'jeans')])
        self.assertEqual(len(jeans_materials_item), 0)
        

