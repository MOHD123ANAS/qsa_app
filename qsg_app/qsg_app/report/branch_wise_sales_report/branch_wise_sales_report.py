# Copyright (c) 2026, MD Anas and contributors
# For license information, please see license.txt

# import frappe

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "label": "POS Invoice",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "POS Invoice",
            "width": 180
        },
        {
            "label": "Date",
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": "Branch",
            "fieldname": "branch",
            "fieldtype": "Link",
            "options": "Branch",
            "width": 150
        },
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 180
        },
        {
            "label": "Cashier",
            "fieldname": "owner",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Warehouse",
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 150
        },
        {
            "label": "Total Amount",
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "width": 150
        }
    ]



def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND posting_date BETWEEN %(from_date)s AND %(to_date)s"
        values["from_date"] = filters.get("from_date")
        values["to_date"] = filters.get("to_date")

    
    if filters.get("branches"):
        conditions += " AND branches = %(branches)s"
        values["branches"] = filters.get("branches")

    data = frappe.db.sql(f"""
        SELECT 
            name,
            posting_date,
            branches as branch,
            customer,
            owner,
            set_warehouse as warehouse,
            grand_total
        FROM `tabPOS Invoice`
        WHERE docstatus = 1
        {conditions}
        ORDER BY posting_date DESC
    """, values, as_dict=1)

    return data