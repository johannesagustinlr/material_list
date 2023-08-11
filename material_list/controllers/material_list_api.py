
import json


from odoo import http, _, exceptions
from odoo.http import request

import werkzeug.wrappers


class MaterialList(http.Controller):

    @http.route(['/material_list','/material_list/<string:material_type>'],csrf=False, auth="user", methods=['get'])
    def get_material_list(self,material_type=None, **kwargs):
        res = []
        if material_type is None:
            materials = request.env['material.list'].sudo().search([])
            for material in materials:
                value = {
                    'name' : material.name,
                    'material_code': material.material_code,
                    'material_type': material.material_type,
                    'supplier_id':material.supplier_id.name,
                    'material_price':material.material_price,
                }
                res.append(value)
            data = {
                'status':200,
                'message':'success',
                'response': res
            }
            return werkzeug.wrappers.Response(
                status=200,
                content_type='application/json; charset=utf-8',
                response=json.dumps(data)
            )  
        else:
            if material_type not in ['jeans','cotton','fabric']:
                return werkzeug.wrappers.Response(
                    status=400,
                    content_type='application/json; charset=utf-8',
                    response=json.dumps({
                        'error':'Error',
                        'error_desc':'Material Type not in option'
                    })
                )
            else:
                materials = request.env['material.list'].sudo().search([('material_type','=',material_type)])
                for material in materials:
                    value = {
                        'name' : material.name,
                        'material_code': material.material_code,
                        'material_type': material.material_type,
                        'supplier_id':material.supplier_id.name,
                        'material_price':material.material_price,
                    }
                    res.append(value)
                data = {
                    'status':200,
                    'message':'success',
                    'response': res
                }
                return werkzeug.wrappers.Response(
                    status=200,
                    content_type='application/json; charset=utf-8',
                    response=json.dumps(data)
                )

    @http.route(['/create/material'],csrf=False, auth="user", type='json', methods=['POST'])
    def create_material(self, name, material_code, material_type, material_price, supplier_name, **kwargs):  
        materials = request.env['material.list']
        supplier_id = request.env['supplier.list'].sudo().search([('name','=',supplier_name)])
        if len(supplier_id) == 0 :
            return {
               "Error Description" : "Supplier name not in our database"
            }            
        if material_type not in ['jeans','cotton','fabric']:
            return {
               "Error Description" : "Material type not in our database"
            } 
        material_data = {
            'name' : name,
            'material_code' : material_code,
            'material_type' : material_type,
            'material_price' : material_price,
            'supplier_id' : supplier_id[0].id,
        }
        material_id = materials.sudo().create(material_data)
        data = {
                    'message':'success',
                    'id':material_id.id,
                    'name' : name,
                    'material_code' : material_code,
                    'material_type' : material_type,
                    'material_price' : material_price,
                    'supplier_name' : supplier_name,
                }
        return data
    

    @http.route('/delete/material/<int:material_id>/', auth='user', methods=['POST'], csrf=False)
    def delete_material(self, material_id):
        try:
            material = request.env['material.list'].sudo().browse(material_id)
            result  = {
                'message':'success',
                'id':material_id,
            }
            material.unlink()
            return json.dumps(result)
        except Exception as e:
            result = str(e)
            return json.dumps(result)
        
    @http.route('/update/material/<int:material_id>/', auth='user',type='http', methods=['POST'], csrf=False)
    def update_material(self, material_id, **params):
        field_list = ['material_name','material_type', 'material_code', 'material_price', 'supplier_name']
        params_dict = {}
        if not params:
            return json.dumps({
                'message':"Failed, Don't have any field to update",
            })
        
        for params_key in params.keys():
            if params_key not in field_list:
                return json.dumps({
                'message':"Failed, Material list dont have field '{name}' ".format(name = params_key)
            })

            else:
                value = request.params.get(params_key)
                if params_key == 'material_price' and value < 100.0:
                    return json.dumps({
                        'message':"Failed, material price should higher than 100 "})
                
                if params_key == 'supplier_name':
                    supplier_id = request.env['supplier.list'].sudo().search([('name','=',value)])
                    if len(supplier_id) == 0 :
                        return {
                        "Error Description" : "Supplier name not in our database"
                        }            
                    else:
                        value = supplier_id[0].id
                params_dict[params_key] = value

        
        try:
            material = request.env['material.list'].sudo().browse(material_id)
            result  = {
                'message':'success updating new value',
                'id':material_id,
            }
            material.sudo().write(params_dict)

            return json.dumps(result)
        except Exception as e:
            result = str(e)
            return json.dumps(result)

        
                    




    
