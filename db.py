import sqlite3


class Database:
    def __init__(self):
        self.con = sqlite3.connect("EmailLabels.db")
        self.cursor = self.con.cursor()
        self.create_tables()

    def create_tables(self):
        try:
            # Create Emails table
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS Emails ( id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL)"
            )

            # Create Labels table
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS Labels (id INTEGER PRIMARY KEY AUTOINCREMENT,label TEXT UNIQUE NOT NULL)"
            )

            # Create EmailLabelMapping table
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS EmailLabelMapping (email_id INTEGER,label_id INTEGER, FOREIGN KEY (email_id) REFERENCES Emails(id), FOREIGN KEY (label_id) REFERENCES Labels(id), UNIQUE(email_id, label_id))"
            )

            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def assign_label_to_email(self, email, label) -> bool:
        try:
            email_id = self.get_or_create_email_id(email)
            label_id = self.get_or_create_label_id(label)
            # Check if email-label mapping already exists
            self.cursor.execute(
                "INSERT OR IGNORE INTO EmailLabelMapping (email_id, label_id) VALUES (?, ?)",
                (email_id, label_id),
            )
            self.con.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error assigning label to email: {e}")
            return False

    def get_or_create_email_id(self, email) -> int | None:
        try:
            # Check if email exists and return the id
            self.cursor.execute("SELECT id FROM Emails WHERE email = ?", (email,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                # Insert email and return its ID
                self.cursor.execute("INSERT INTO Emails (email) VALUES (?)", (email,))
                self.con.commit()
                return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error getting or creating email ID: {e}")
            return None

    def get_or_create_label_id(self, label) -> int | None:
        try:
            # Check if label exists
            self.cursor.execute("SELECT id FROM Labels WHERE label = ?", (label,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                # Insert label and return its ID
                self.cursor.execute("INSERT INTO Labels (label) VALUES (?)", (label,))
                self.con.commit()
                return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error getting or creating label ID: {e}")
            return None

    def update_label_for_email(self, email, new_label) -> bool:
        try:
            email_id = self.get_or_create_email_id(email)
            label_id = self.get_or_create_label_id(new_label)

            # Update the label for the email
            self.cursor.execute(
                "INSERT OR REPLACE INTO EmailLabelMapping (email_id, label_id) VALUES (?, ?)",
                (email_id, label_id),
            )
            self.con.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating label for email: {e}")
            return False

    def close_connection(self):
        self.con.close()
