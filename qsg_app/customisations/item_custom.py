import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields():
    custom_fields = {
        "Item": [
        {
            "fieldname": "item_brand",
            "fieldtype": "Data",
            "label": "Supplier Brand",
            "insert_after": "stock_uom",
            "reqd": 0,
            "in_list_view": 1,
            "in_standard_filter": 1,
            
        }

        ]
    }

    for doctype, fields in custom_fields.items(): 
        for field in fields: 
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                create_custom_field(doctype, field) 
                frappe.db.commit() 
                frappe.clear_cache(doctype=doctype)

def delete_custom_fields():
    custom_fields_to_delete = { "Item": ["item_brand"]}  

    for doctype, fields in custom_fields_to_delete.items(): 
        for field_name in fields: 
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}): 
                frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_missing=True) 
                frappe.db.commit() 
                frappe.clear_cache(doctype=doctype)      