# nlp_report
🧠 Natural Language Report Generator for ERPNext

This Frappe app allows users to query ERPNext reports using natural language commands such as:

    “Show approved leave of Aruna D”

Using simple, intuitive phrases, users can generate Leave Applications, Attendance Logs, Expense Claims, and Employee details.
🚀 Features

    🔍 Query ERPNext data using plain English.

    📄 Auto-generates dynamic reports from Leave Application, Attendance, Expense Claim, and Employee doctype.

    🧠 Built-in natural language parser.

    🌐 User-friendly web interface.

    ⚙️ Extensible with OpenAI GPT API (future-ready).

📂 Project Structure

nlp_report/
├── nlp_report/
│   ├── api.py                       # Main logic to parse commands & return data
│   ├── www/
│   │   ├── natural-language-report.html  # Frontend UI
│   │   ├── natural_language_report.py    # Controller for the UI

🔧 Installation

    Clone the app into your frappe-bench/apps folder:

cd ~/frappe-bench/apps
git clone https://github.com/yourusername/nlp_report.git

    Install the app:

cd ~/frappe-bench
bench --site your-site-name install-app nlp_report

    Restart bench:

bench restart

🌐 Access the Interface

After installation, open the page:

http://<your-site>/natural-language-report

Enter a natural language command like:

Show all leave applications of Aruna D

🧠 Supported Commands

Examples of valid input:

    Show approved leave of Aruna D

    List all expense claims for John

    Show attendance status Work From Home for Meera

    Show employee details

⚙️ Backend Logic (api.py)

    Uses parse_command_with_llm() to convert input into structured ERPNext query.

    Supports basic NLP using Python regex.

    Fetches relevant data using frappe.db.get_all().

🔐 Security

This endpoint allows guest access (@frappe.whitelist(allow_guest=True)), so restrict public access if sensitive data is involved.



📄 License

MIT License

🙌 Contributors

Aruna D - Initial Developer
