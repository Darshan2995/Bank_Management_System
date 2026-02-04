import streamlit as st
import json
import random
import string
from pathlib import Path

# ------------------ BANK CLASS ------------------ #
class Bank:
    database = "data.json"

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database, "r") as f:
                return json.load(f)
        return []

    @classmethod
    def save_data(cls, data):
        with open(cls.database, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def generate_account():
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        sp = random.choices("!@#$%^&*", k=1)
        acc = alpha + num + sp
        random.shuffle(acc)
        return "".join(acc)

# ------------------ STREAMLIT UI ------------------ #
st.set_page_config(page_title="Bank Management System", layout="centered")
st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "View Details",
        "Update Details",
        "Delete Account"
    ]
)

data = Bank.load_data()

# ------------------ CREATE ACCOUNT ------------------ #
if menu == "Create Account":
    st.header("Create New Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    email = st.text_input("Email")
    pin = st.text_input("4 Digit PIN", type="password")

    if st.button("Create Account"):
        if age < 18 or len(pin) != 4:
            st.error("Age must be 18+ and PIN must be 4 digits")
        else:
            acc_no = Bank.generate_account()
            user = {
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "acc_No": acc_no,
                "balance": 0
            }
            data.append(user)
            Bank.save_data(data)

            st.success("Account Created Successfully 🎉")
            st.write("### Account Number:")
            st.code(acc_no)

# ------------------ DEPOSIT MONEY ------------------ #
elif menu == "Deposit Money":
    st.header("Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        user = next((u for u in data if u["acc_No"] == acc and u["pin"] == int(pin)), None)
        if not user:
            st.error("Invalid Account or PIN")
        elif amount > 10000:
            st.warning("Max deposit limit is 10,000")
        else:
            user["balance"] += amount
            Bank.save_data(data)
            st.success(f"₹{amount} deposited successfully")

# ------------------ WITHDRAW MONEY ------------------ #
elif menu == "Withdraw Money":
    st.header("Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        user = next((u for u in data if u["acc_No"] == acc and u["pin"] == int(pin)), None)
        if not user:
            st.error("Invalid Account or PIN")
        elif amount > user["balance"]:
            st.warning("Insufficient Balance")
        elif amount > 10000:
            st.warning("Max withdrawal limit is 10,000")
        else:
            user["balance"] -= amount
            Bank.save_data(data)
            st.success(f"₹{amount} withdrawn successfully")

# ------------------ VIEW DETAILS ------------------ #
elif menu == "View Details":
    st.header("Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):
        user = next((u for u in data if u["acc_No"] == acc and u["pin"] == int(pin)), None)
        if not user:
            st.error("Invalid Account or PIN")
        else:
            st.json(user)

# ------------------ UPDATE DETAILS ------------------ #
elif menu == "Update Details":
    st.header("Update Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Fetch Details"):
        user = next((u for u in data if u["acc_No"] == acc and u["pin"] == int(pin)), None)

        if not user:
            st.error("Invalid Account or PIN")
        else:
            name = st.text_input("New Name", user["name"])
            email = st.text_input("New Email", user["email"])
            new_pin = st.text_input("New PIN", value=str(user["pin"]))

            if st.button("Update"):
                user["name"] = name
                user["email"] = email
                user["pin"] = int(new_pin)
                Bank.save_data(data)
                st.success("Details Updated Successfully")

# ------------------ DELETE ACCOUNT ------------------ #
elif menu == "Delete Account":
    st.header("Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        user = next((u for u in data if u["acc_No"] == acc and u["pin"] == int(pin)), None)

        if not user:
            st.error("Invalid Account or PIN")
        else:
            data.remove(user)
            Bank.save_data(data)
            st.success("Account Deleted Successfully 🗑️")
