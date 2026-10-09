import sqlite3

DB_NAME = "crm_database.db"

def get_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Create the tickets table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            customer_name TEXT,
            company TEXT,
            contact_info TEXT,
            product_service TEXT,
            problem_details TEXT,
            priority TEXT,
            status TEXT,
            next_action TEXT,
            assigned_dept TEXT,
            suggested_dept TEXT,
            saved_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_ticket(ticket):
    """Save a new ticket to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tickets (ticket_id, customer_name, company, contact_info, product_service, problem_details, priority, status, next_action, assigned_dept, suggested_dept, saved_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        ticket.get("ticket_id"),
        ticket.get("customer_name"),
        ticket.get("company"),
        ticket.get("contact_info"),
        ticket.get("product_service"),
        ticket.get("problem_details"),
        ticket.get("priority"),
        ticket.get("status"),
        ticket.get("next_action"),
        ticket.get("assigned_dept"),
        ticket.get("suggested_dept"),
        ticket.get("saved_at")
    ))
    conn.commit()
    conn.close()

def get_all_tickets():
    """Get all tickets from the database, newest first."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY saved_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def check_duplicate_customer(customer_name, product_service):
    """Check if a customer has already reported the same problem."""
    if not customer_name:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tickets WHERE customer_name = ? AND product_service = ?", 
        (customer_name, product_service)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None

def clear_database():
    """Delete all tickets (for demo purposes)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets")
    conn.commit()
    conn.close()