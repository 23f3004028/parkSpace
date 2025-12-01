import csv
import smtplib
import os
from datetime import datetime, timedelta
from celery.schedules import crontab
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from .extensions import celery_app
from .controllers.__init__ import conn_database

def send_email(to_email, subject, body, attachment_path=None):
    print("\n" + "="*30)
    print(f"📧 SENDING EMAIL TO: {to_email}")
    print(f"Subject: {subject}")
    print(f"Body (Truncated): {body[:100]}...")
    if attachment_path:
        print(f"📎 Attachment: {attachment_path}")
    print("="*30 + "\n")
    return True

@celery_app.task
def export_user_history_csv(user_id, user_email):
    conn = None
    try:
        conn = conn_database()
        curr = conn.cursor()
        
        curr.execute('''
            SELECT PL.prime_location, BD.spot_number, BD.vehicle_number, 
                   datetime(BD.timestamp_booked, 'unixepoch') as booked_time, 
                   BD.price, BD.booking_status
            FROM BOOKING_DETAILS BD
            JOIN PARKING_SPOT PS ON PS.spot_number = BD.spot_number AND PS.lot_id = BD.lot_id
            JOIN PARKING_LOT PL ON PL.id = PS.lot_id
            WHERE BD.user_id = ?
        ''', (user_id,))
        rows = curr.fetchall()
        
        csv_data = [list(row) for row in rows]

        filename = f"export_{user_id}_{int(datetime.now().timestamp())}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Location", "Spot", "Vehicle", "Booked Time", "Price", "Status"])
            writer.writerows(csv_data)

        send_email(user_email, "Your Parking History Export", 
                   "Your detailed parking history is attached below.", filename)
        
        if os.path.exists(filename):
            os.remove(filename)
        
        return "Export Done"
    except Exception as e:
        print(f"CSV Export Error: {e}")
        return f"Export Failed: {str(e)}"
    finally:
        if conn: conn.close()

@celery_app.task
def daily_reminder():
    conn = None
    try:
        conn = conn_database()
        curr = conn.cursor()
        
        
        curr.execute("SELECT id, email, name FROM USERS WHERE is_admin=0")
        users = curr.fetchall()
        
        for user in users:
            user_id, email, name = user[0], user[1], user[2]
            
            curr.execute("SELECT COUNT(*) FROM BOOKING_DETAILS WHERE user_id=? AND booking_status='open'", (user_id,))
            active_count = curr.fetchone()[0]
            
            if active_count == 0:
                send_email(email, "Daily Reminder: Book a Spot!", 
                           f"Hi {name}, our parking lot is open! Do you need to book a spot for the evening?")
                
        return "Daily Reminders Sent"
    except Exception as e:
        print(f"Daily Reminder Error: {e}")
        return f"Reminder Failed: {str(e)}"
    finally:
        if conn: conn.close()


@celery_app.task
def monthly_activity_report():
    conn = None
    try:
        conn = conn_database()
        curr = conn.cursor()
        
        curr.execute("SELECT id, email, name FROM USERS WHERE is_admin=0")
        users = curr.fetchall()
        
        for user in users:
            user_id, email, name = user[0], user[1], user[2]
            
            curr.execute("SELECT SUM(price) FROM BOOKING_DETAILS WHERE user_id=? AND booking_status='closed'", (user_id,))
            spent = curr.fetchone()[0] or 0
            
            curr.execute('''
                SELECT PL.prime_location, COUNT(BD.id) as count
                FROM BOOKING_DETAILS BD
                JOIN PARKING_LOT PL ON BD.lot_id = PL.id
                WHERE BD.user_id = ?
                GROUP BY PL.prime_location
                ORDER BY count DESC LIMIT 1
            ''', (user_id,))
            most_used_lot = curr.fetchone()
            lot_name = most_used_lot[0] if most_used_lot else "N/A"
            
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #2a55e5;">Monthly Activity Report: {name}</h2>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d')}</p>
                    <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%;">
                        <tr><td><strong>Total Amount Spent (Closed Bookings)</strong></td><td>₹{spent:.2f}</td></tr>
                        <tr><td><strong>Most Used Parking Lot</strong></td><td>{lot_name}</td></tr>
                    </table>
                    <p style="margin-top: 20px;">Thank you for parking with us!</p>
                </body>
            </html>
            """
            
            send_email(email, "Monthly Activity Report", html_content)
            
        return "Monthly Reports Sent"
    except Exception as e:
        print(f"Monthly Report Error: {e}")
        return f"Monthly Report Failed: {str(e)}"
    finally:
        if conn: conn.close()

celery_app.conf.beat_schedule = {
    'daily-reminder-every-evening': {
        'task': 'backend.extensions.daily_reminder',
        'task': 'backend.extensions.monthly_activity_report',
        'schedule': crontab(hour=18, minute=0), 
    },
    'monthly-report-first-day': {
        'task': 'tasks.monthly_activity_report',
        'schedule': crontab(day_of_month=1, hour=9, minute=0), 
    }
}
