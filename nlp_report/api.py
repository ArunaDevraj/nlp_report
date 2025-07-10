import frappe
import json
import openai
import os
import re




@frappe.whitelist(allow_guest=True)
def smart_report(command):
    try:
        # Log incoming command
        frappe.log_error("Parsed Command Debug", command)

        parsed = parse_command_with_llm(command)
        parsed_data = json.loads(parsed)

        frappe.log_error("Parsed JSON", frappe.as_json(parsed_data))  # Log parsed output

        doctype = parsed_data["doctype"]
        filters = parsed_data.get("filters", {})
        fields = parsed_data.get("fields", ["*"])

        results = frappe.db.get_all(doctype, filters=filters, fields=fields, limit=100)
        return results

    except Exception as e:
        frappe.log_error(
            title="Smart Report Error",
            message=f"{str(e)[:1000]}"
        )
        return {"error": str(e)}



def parse_command_with_llm(command):
    command = command.lower().strip()

    def extract_name(text):
        match = re.search(r"(?:of|for)\s+([a-zA-Z\s\.]+)", text)
        return match.group(1).title().strip() if match else None

    def extract_status(text):
        match = re.search(r"status\s+(open|approved|rejected|cancelled|submitted)", text)
        return match.group(1).title() if match else None

    def get_employee_id_from_name(name):
        if not name:
            return None
        result = frappe.db.sql("""
            SELECT name FROM `tabEmployee`
            WHERE employee_name LIKE %s
            ORDER BY LOCATE(%s, employee_name)
            LIMIT 1
        """, (f"%{name}%", name), as_dict=True)
        return result[0]["name"] if result else None

    name = extract_name(command)
    status = extract_status(command)
    filters = {}

    # Leave Application logic
    if "leave application" in command:
        if status:
            filters["status"] = status
        elif "open" in command or "pending" in command:
            filters["status"] = "Open"
        elif "approved" in command:
            filters["status"] = "Approved"
        elif "rejected" in command:
            filters["status"] = "Rejected"
        elif "cancelled" in command:
            filters["status"] = "Cancelled"

        if name:
            emp_id = get_employee_id_from_name(name)
            if emp_id:
                filters["employee"] = emp_id

        return json.dumps({
            "doctype": "Leave Application",
            "filters": filters,
            "fields": ["employee", "employee_name", "status", "from_date", "to_date"]
        })

    # Expense Claim
    if "expense" in command:
        if name:
            emp_id = get_employee_id_from_name(name)
            if emp_id:
                filters["employee"] = emp_id

        return json.dumps({
            "doctype": "Expense Claim",
            "filters": filters,
            "fields": ["employee", "employee_name", "expense_type", "total_claimed_amount", "posting_date"]
        })

    # Attendance — handles all status cases
    if "attendance" in command:
        if name:
            emp_id = get_employee_id_from_name(name)
            if emp_id:
                filters["employee"] = emp_id

        # Important: more specific terms checked first
        if "work from home" in command or "wfh" in command:
            filters["status"] = "Work From Home"
        elif "on leave" in command:
            filters["status"] = "On Leave"
        elif "half day" in command or "halfday" in command:
            filters["status"] = "Half Day"
        elif "present" in command:
            filters["status"] = "Present"
        elif "absent" in command:
            filters["status"] = "Absent"

        return json.dumps({
            "doctype": "Attendance",
            "filters": filters,
            "fields": [
                "employee", "employee_name", "status",
                "attendance_date", "working_hours"
            ]
        })

    # Employee fallback
    if "employee" in command:
        return json.dumps({
            "doctype": "Employee",
            "filters": {},
            "fields": ["name", "employee_name", "department", "designation"]
        })

    # Fallback response
    return json.dumps({
        "doctype": "Employee",
        "filters": {},
        "fields": ["name", "employee_name"]
    })
