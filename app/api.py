from flask import Flask, request, jsonify
from src.accounts_registry import AccountsRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountsRegistry()

@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")

    if not data:
        return jsonify({"message": "Invalid body"}), 400

    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201


@app.route("/api/accounts", methods=["GET"])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.return_accounts()

    accounts_data = [
        {
            "name": acc.first_name,
            "surname": acc.last_name,
            "pesel": acc.pesel,
            "balance": acc.balance
        }
        for acc in accounts
    ]

    return jsonify(accounts_data), 200


@app.route("/api/accounts/count", methods=["GET"])
def get_account_count():
    print("Get account count request received")
    count = registry.get_accounts_count()
    return jsonify({"count": count}), 200


@app.route("/api/accounts/<pesel>", methods=["GET"])
def get_account_by_pesel(pesel):
    print("Get account by pesel request received")
    account = registry.find_by_pesel(pesel)

    if not account:
        return jsonify({"message": "Account not found"}), 404

    return jsonify({
        "name": account.first_name,
        "surname": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance
    }), 200


@app.route("/api/accounts/<pesel>", methods=["PATCH"])
def update_account(pesel):
    print("Update account request received")
    account = registry.find_by_pesel(pesel)

    if not account:
        return jsonify({"message": "Account not found"}), 404

    data = request.get_json()

    if "name" in data:
        account.first_name = data["name"]

    if "surname" in data:
        account.last_name = data["surname"]

    return jsonify({"message": "Account updated"}), 200


@app.route("/api/accounts/<pesel>", methods=["DELETE"])
def delete_account(pesel):
    print("Delete account request received")
    account = registry.find_by_pesel(pesel)

    if not account:
        return jsonify({"message": "Account not found"}), 404

    registry.accounts.remove(account)

    return jsonify({"message": "Account deleted"}), 200

