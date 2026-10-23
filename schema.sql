
CREATE DATABASE IF NOT EXISTS bank_management;
USE bank_management;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS accounts (
    account_no INT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_type VARCHAR(20) NOT NULL,
    balance DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    CHECK (balance >= 0),
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_no INT NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    remarks VARCHAR(200),
    FOREIGN KEY (account_no)
        REFERENCES accounts(account_no)
);

INSERT IGNORE INTO customers
    (customer_id, customer_name, phone)
VALUES
    (1, 'Rahul Kumar', '9876543210'),
    (2, 'Amit Kumar', '9876543211');

INSERT IGNORE INTO accounts
    (account_no, customer_id, account_type, balance)
VALUES
    (1001, 1, 'Savings', 10000.00),
    (1002, 2, 'Savings', 5000.00);
