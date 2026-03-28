import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields():
    custom_fields = {
        "POS Invoice": [
        {
            "fieldname": "customer_type",
            "fieldtype": "Data",
            "label": "Customer Type",
            "insert_after": "customer",
            "fetch_from":"custom.customer_type",
            "in_list_view": 1,
            "in_standard_filter": 1,
            "read_only": 1,
            "reqd":0
        },
        {
            "fieldname": "branches",
            "fieldtype": "Data",
            "label": "Branch",
            "insert_after": "set_warehouse",
            "fetch_from":"set_warehouse.branch",
            "in_list_view": 1,
            "in_standard_filter": 1,
            "read_only": 1,
            "reqd":0
        },

        ]
    }

    for doctype, fields in custom_fields.items(): 
        for field in fields: 
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                create_custom_field(doctype, field) 
                frappe.db.commit() 
                frappe.clear_cache(doctype=doctype)

def delete_custom_fields(): 
    custom_fields_to_delete = { "POS Invoice": ["customer_type","branches"]}  

    for doctype, fields in custom_fields_to_delete.items(): 
        for field_name in fields: 
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}): 
                frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_missing=True) 
                frappe.db.commit() 
                frappe.clear_cache(doctype=doctype)      