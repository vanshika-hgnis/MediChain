import hashlib
import json
import time
from typing import List, Dict, Any

from database import Database


class Block:
    def __init__(
        self, index: int, timestamp: float, data: Dict[str, Any], previous_hash: str
    ):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.pending_transactions: List[Dict[str, Any]] = []

    def create_genesis_block(self) -> Block:
        return Block(0, time.time(), {"message": "Genesis Block"}, "0")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: Dict[str, Any]) -> Block:
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), data, previous_block.hash)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True


# class HealthcareBlockchain(Blockchain):
#     def __init__(self, db_name="healthcare_blockchain.db"):
#         super().__init__()
#         self.users: Dict[str, Dict[str, Any]] = {}
#         self.access_permissions: Dict[str, List[str]] = {}
#         self.db = Database(db_name)

#     def add_user(self, username: str, user_type: str, password: str) -> bool:
#         if username in self.users:
#             return False
#         self.users[username] = {
#             "type": user_type,
#             "password": hashlib.sha256(password.encode()).hexdigest(),
#         }
#         if user_type == "patient":
#             self.access_permissions[username] = []
#         return True

#     def grant_access(self, patient_id: str, healthcare_provider_id: str) -> bool:
#         if (
#             patient_id in self.users
#             and healthcare_provider_id in self.users
#             and self.users[patient_id]["type"] == "patient"
#         ):
#             if patient_id in self.access_permissions:
#                 if healthcare_provider_id not in self.access_permissions[patient_id]:
#                     self.access_permissions[patient_id].append(healthcare_provider_id)
#                 return True
#         return False

#     def has_access(self, patient_id: str, healthcare_provider_id: str) -> bool:
#         return (
#             patient_id in self.access_permissions
#             and healthcare_provider_id in self.access_permissions[patient_id]
#         )

#     def add_medical_record(self, patient_id: str, record_data: Dict[str, Any]) -> bool:
#         try:
#             if not patient_id in self.users:
#                 raise ValueError("Patient not found in the system")

#             if self.users[patient_id]["type"] != "patient":
#                 raise ValueError("Specified ID is not a patient")

#             if not record_data.get("diagnosis") or not record_data.get("treatment"):
#                 raise ValueError("Diagnosis and treatment are required fields")

#             # Create the complete medical record
#             medical_record = {
#                 "patient_id": patient_id,
#                 "medical_data": record_data,
#                 "timestamp": record_data.get("date")
#                 or time.strftime("%Y-%m-%d %H:%M:%S"),
#                 "record_type": "medical_record",
#             }

#             # Add the record to the blockchain
#             self.add_block(medical_record)
#             return True

#         except Exception as e:
#             print(f"Error adding medical record: {str(e)}")
#             return False

#     def get_patient_records(
#         self, patient_id: str, requester_id: str
#     ) -> List[Dict[str, Any]]:
#         if patient_id == requester_id or self.has_access(patient_id, requester_id):
#             records = []
#             for block in self.chain[1:]:  # Skip genesis block
#                 if (
#                     block.data.get("patient_id") == patient_id
#                     and block.data.get("record_type") == "medical_record"
#                 ):
#                     records.append(block.data)
#             return records
#         return []

import hashlib
import json
import time
from typing import List, Dict, Any
from database import Database


class HealthcareBlockchain(Blockchain):
    def __init__(self, db_name="healthcare_blockchain.db"):
        super().__init__()
        self.db = Database(db_name)
        self.users: Dict[str, Dict[str, Any]] = {}
        self.access_permissions: Dict[str, List[str]] = {}
        self._load_users_from_db()

    def _load_users_from_db(self):
        """Load existing users from database into memory"""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT username, password, user_type FROM users")
        for username, password, user_type in cursor.fetchall():
            self.users[username] = {
                "type": user_type,
                "password": password,
            }
            if user_type == "patient":
                self.access_permissions[username] = []

        # Load access permissions
        cursor.execute("SELECT patient_id, provider_id FROM access_permissions")
        for patient_id, provider_id in cursor.fetchall():
            if patient_id in self.access_permissions:
                self.access_permissions[patient_id].append(provider_id)

    def add_user(self, username: str, user_type: str, password: str) -> bool:
        if username in self.users:
            return False

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Add to database first
        if not self.db.add_user(username, hashed_password, user_type):
            return False

        # If database insertion successful, add to memory
        self.users[username] = {
            "type": user_type,
            "password": hashed_password,
        }

        if user_type == "patient":
            self.access_permissions[username] = []

        return True

    def grant_access(self, patient_id: str, healthcare_provider_id: str) -> bool:
        if (
            patient_id in self.users
            and healthcare_provider_id in self.users
            and self.users[patient_id]["type"] == "patient"
        ):
            if patient_id in self.access_permissions:
                if healthcare_provider_id not in self.access_permissions[patient_id]:
                    # Add to database first
                    if self.db.add_access_permission(
                        patient_id, healthcare_provider_id
                    ):
                        self.access_permissions[patient_id].append(
                            healthcare_provider_id
                        )
                        return True
        return False

    def has_access(self, patient_id: str, healthcare_provider_id: str) -> bool:
        # Check both memory and database
        return (
            patient_id in self.access_permissions
            and healthcare_provider_id in self.access_permissions[patient_id]
        ) or self.db.check_access_permission(patient_id, healthcare_provider_id)

    def add_medical_record(self, username: str, record_data: Dict[str, Any]) -> bool:
        try:
            if not username in self.users:
                raise ValueError("Patient not found in the system")

            if self.users[username]["type"] != "patient":
                raise ValueError("Specified ID is not a patient")

            if not record_data.get("diagnosis") or not record_data.get("treatment"):
                raise ValueError("Diagnosis and treatment are required fields")

            # Create the complete medical record
            medical_record = {
                "username": username,
                "medical_data": record_data,
                "timestamp": record_data.get("date")
                or time.strftime("%Y-%m-%d %H:%M:%S"),
                "record_type": "medical_record",
            }

            # Add the record to the blockchain
            new_block = self.add_block(medical_record)

            # Save the block to the database
            if not self.db.add_block(new_block):
                raise ValueError("Failed to save block to database")

            # Save the medical record to the database
            if not self.db.add_medical_record(
                username=username,
                record_data=record_data,
                block_index=new_block.index,
            ):
                raise ValueError("Failed to save medical record to database")

            return True

        except Exception as e:
            print(f"Error adding medical record: {str(e)}")
            return False

    def get_patient_records(
        self, patient_id: str, requester_id: str
    ) -> List[Dict[str, Any]]:
        if patient_id == requester_id or self.has_access(patient_id, requester_id):
            # Get records from both blockchain and database
            blockchain_records = []
            for block in self.chain[1:]:  # Skip genesis block
                if (
                    block.data.get("patient_id") == patient_id
                    and block.data.get("record_type") == "medical_record"
                ):
                    blockchain_records.append(block.data)

            # Get detailed records from database
            db_records = self.db.get_patient_records(patient_id)

            # Merge and return records (prioritizing database records as they contain more detail)
            return db_records or blockchain_records
        return []

    def verify_blockchain_integrity(self) -> bool:
        """Verify the integrity of both in-memory and database stored blocks"""
        # First check in-memory chain
        if not super().is_chain_valid():
            return False

        # Then verify against database
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM blocks ORDER BY index")
        db_blocks = cursor.fetchall()

        if len(db_blocks) != len(self.chain):
            return False

        for i, block in enumerate(db_blocks):
            if block[0] != self.chain[i].index:  # Compare indices
                return False
            if block[4] != self.chain[i].hash:  # Compare hashes
                return False

        return True

    def __del__(self):
        """Ensure database connection is closed when object is destroyed"""
        try:
            self.db.close()
        except:
            pass
