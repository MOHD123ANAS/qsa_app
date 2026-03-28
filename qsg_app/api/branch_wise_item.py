import frappe

@frappe.whitelist(allow_guest=True)
def get_stock_by_branch(branch=None, length=None):
    conditions = ""
    values = {}

    
    if branch:
        conditions += " AND w.branch = %(branch)s"
        values["branch"] = branch

    
    limit_clause = ""
    if length:
        try:
            length = int(length)
            limit_clause = " LIMIT %(length)s"
            values["length"] = length
        except:
            pass  

    
    data = frappe.db.sql(f"""
        SELECT 
            b.item_code,
            i.item_name,
            i.item_group,
            w.branch,
            SUM(b.actual_qty) as qty
        FROM `tabBin` b
        JOIN `tabItem` i ON i.name = b.item_code
        JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE b.actual_qty > 0
        {conditions}
        GROUP BY b.item_code, w.branch
        ORDER BY qty DESC
        {limit_clause}
    """, values, as_dict=1)

    return {
        "status": "success",
        "count": len(data),
        "data": data
    }