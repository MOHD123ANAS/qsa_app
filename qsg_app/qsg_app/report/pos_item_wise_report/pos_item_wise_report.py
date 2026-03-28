# Copyright (c) 2026, MD Anas and contributors
# For license information, please see license.txt

# import frappe


import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart


def get_columns():
    return [
        {
            "label": "Item Code",
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "label": "Item Name",
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Item Group",
            "fieldname": "item_group",
            "fieldtype": "Link",
            "options": "Item Group",
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
            "label": "Branch",
            "fieldname": "branch",
            "fieldtype": "Link",
            "options": "Branch",
            "width": 150
        },
        {
            "label": "Qty Sold",
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": "Avg Rate",
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "Total Sales",
            "fieldname": "total_sales",
            "fieldtype": "Currency",
            "width": 150
        }
    ]


def get_data(filters):
    conditions = ""
    values = {}

    
    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s"
        values["from_date"] = filters.get("from_date")
        values["to_date"] = filters.get("to_date")

    
    if filters.get("branch"):
        conditions += " AND w.branch = %(branch)s"
        values["branch"] = filters.get("branch")

    data = frappe.db.sql(f"""
        SELECT 
            pii.item_code,
            pii.item_name,
            i.item_group,
            pi.customer,
            w.branch,
            SUM(pii.qty) as qty,
            SUM(pii.amount) / SUM(pii.qty) as rate,
            SUM(pii.amount) as total_sales
        FROM `tabPOS Invoice` pi
        JOIN `tabPOS Invoice Item` pii ON pii.parent = pi.name
        LEFT JOIN `tabItem` i ON i.name = pii.item_code
        LEFT JOIN `tabWarehouse` w ON pii.warehouse = w.name
        WHERE pi.docstatus = 1
        {conditions}
        GROUP BY pii.item_code, pi.customer, w.branch
        ORDER BY qty DESC
        LIMIT 20
    """, values, as_dict=1)

    return data

def get_chart(data):
    
    item_map = {}

    for row in data:
        item = row["item_code"]
        item_map[item] = item_map.get(item, 0) + row["qty"]

    labels = list(item_map.keys())
    values = list(item_map.values())

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Qty Sold",
                    "values": values
                }
            ]
        },
        "type": "bar"
    }