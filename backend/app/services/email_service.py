"""
📧 EMAIL ALERTS SERVICE
Handles notifications for attendance, alerts, and system events
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import os
from datetime import datetime

class EmailService:
    """Email notification service for alerts and notifications"""
    
    def __init__(self):
        self.sender_email = os.getenv("EMAIL_SENDER", "noreply@trustmark.edu")
        self.sender_password = os.getenv("EMAIL_PASSWORD", "test-password")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    def send_attendance_alert(self, admin_email: str, student_name: str, uid: str, subject: str) -> bool:
        """Send attendance recorded alert to admin"""
        try:
            subject_line = f"✅ Attendance Recorded - {student_name}"
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="background-color: #f0f8ff; padding: 20px; border-radius: 5px;">
                        <h2>✅ Attendance Verified</h2>
                        <p><strong>Student:</strong> {student_name}</p>
                        <p><strong>UID:</strong> {uid}</p>
                        <p><strong>Subject:</strong> {subject}</p>
                        <p><strong>Timestamp:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                        <p><em>This is an automated notification from TrustMark Sovereign</em></p>
                    </div>
                </body>
            </html>
            """
            
            return self._send_email(admin_email, subject_line, html_body)
        except Exception as e:
            print(f"❌ Error sending attendance alert: {str(e)}")
            return False
    
    def send_duplicate_warning(self, admin_email: str, uid: str, student_name: str, subject: str) -> bool:
        """Alert admin about duplicate attendance attempt"""
        try:
            subject_line = f"⚠️ DUPLICATE ATTENDANCE ATTEMPT - {student_name}"
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="background-color: #fff3cd; padding: 20px; border-radius: 5px; border-left: 4px solid #ff9800;">
                        <h2>⚠️ Duplicate Attendance Detected</h2>
                        <p style="color: #856404;"><strong>Possible cheating attempt detected!</strong></p>
                        <p><strong>Student:</strong> {student_name}</p>
                        <p><strong>UID:</strong> {uid}</p>
                        <p><strong>Subject:</strong> {subject}</p>
                        <p><strong>Attempt Time:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                        <p style="color: red;"><strong>Action Required:</strong> Please verify this attendance manually</p>
                    </div>
                </body>
            </html>
            """
            
            return self._send_email(admin_email, subject_line, html_body)
        except Exception as e:
            print(f"❌ Error sending duplicate warning: {str(e)}")
            return False
    
    def send_system_alert(self, admin_email: str, alert_type: str, message: str) -> bool:
        """Send system alert to admin"""
        try:
            subject_line = f"🔴 System Alert - {alert_type}"
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="background-color: #ffebee; padding: 20px; border-radius: 5px; border-left: 4px solid #f44336;">
                        <h2>🔴 System Alert</h2>
                        <p><strong>Alert Type:</strong> {alert_type}</p>
                        <p><strong>Message:</strong> {message}</p>
                        <p><strong>Timestamp:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                        <p style="color: #f44336;"><strong>Status:</strong> Requires immediate attention</p>
                    </div>
                </body>
            </html>
            """
            
            return self._send_email(admin_email, subject_line, html_body)
        except Exception as e:
            print(f"❌ Error sending system alert: {str(e)}")
            return False
    
    def _send_email(self, recipient_email: str, subject: str, html_body: str) -> bool:
        """Internal method to send email"""
        try:
            # For development: just log instead of actually sending
            if self.sender_password == "test-password":
                print(f"📧 [DEV MODE] Email would be sent to {recipient_email}")
                print(f"   Subject: {subject}")
                return True
            
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            
            msg.attach(MIMEText(html_body, "html"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())
            
            print(f"✅ Email sent to {recipient_email}")
            return True
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False

# Singleton instance
email_service = EmailService()
