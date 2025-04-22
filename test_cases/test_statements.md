# 🧪 Test Cases for `/generate-statement` API

This document contains **15 test cases** for the Flask-based API that generates multilingual credit card statements in PDF format.

---

### 🔹 Test Case 1: Valid request with English

- **Input**: `customer_id=1001`, `language=en`
- **Expected Output**: JSON with `success: True` and a valid `pdf_url`
- **Status**: ✅ Pass

---

### 🔹 Test Case 2: Valid request with Tamil

- **Input**: `customer_id=1001`, `language=ta`
- **Expected Output**: JSON with `success: True` and Tamil-translated content in the PDF
- **Status**: ✅ Pass

---

### 🔹 Test Case 3: Invalid Customer ID

- **Input**: `customer_id=9999`, `language=en`
- **Expected Output**: `success: False`, error message `Customer not found`
- **Status**: ✅ Pass

---

### 🔹 Test Case 4: Missing Customer ID

- **Input**: `language=en`
- **Expected Output**: `success: False`, error: `Customer ID is required`
- **Status**: ✅ Pass

---

### 🔹 Test Case 5: Missing Language (default to English)

- **Input**: `customer_id=1001`
- **Expected Output**: `success: True`, PDF content in English
- **Status**: ✅ Pass

---

### 🔹 Test Case 6: Invalid Language Code

- **Input**: `customer_id=1001`, `language=xx`
- **Expected Output**: Fallback to English, `success: True`
- **Status**: ✅ Pass

---

### 🔹 Test Case 7: PDF File Is Created

- **Input**: Valid request
- **Expected Output**: File saved in `/media` directory
- **Status**: ✅ Pass

---

### 🔹 Test Case 8: Empty Transaction History

- **Input**: `customer_id` with no transactions
- **Expected Output**: PDF with empty transaction table and message like "No transactions available"
- **Status**: ✅ Pass

---

### 🔹 Test Case 9: Multi-page PDF (100+ transactions)

- **Input**: `customer_id=1001` (pre-seeded with 100+ transactions)
- **Expected Output**: PDF spans multiple pages, headers repeated
- **Status**: ✅ Pass

---

### 🔹 Test Case 10: Reward Points Included

- **Input**: Customer with reward points
- **Expected Output**: "Reward Points" section shown with correct value
- **Status**: ✅ Pass

---

### 🔹 Test Case 11: RTL Language Rendering (Arabic)

- **Input**: `customer_id=1001`, `language=ar`
- **Expected Output**: Arabic layout and translations rendered correctly (Right-to-left)
- **Status**: ✅ Pass

---

### 🔹 Test Case 12: Invalid HTTP Method

- **Input**: POST request to `/generate-statement`
- **Expected Output**: 405 Method Not Allowed
- **Status**: ✅ Pass

---

### 🔹 Test Case 13: Response Type Check

- **Input**: Valid GET request
- **Expected Output**: Response content-type = `application/json`
- **Status**: ✅ Pass

---

### 🔹 Test Case 14: PDF Filename Pattern Validation

- **Input**: Valid GET request
- **Expected Output**: `statement_<cardnumber>_<date>.pdf` format
- **Status**: ✅ Pass

---

### 🔹 Test Case 15: Internal Error Fallback

- **Input**: Malformed or missing customer ID
- **Expected Output**: `success: False` with meaningful error
- **Status**: ✅ Pass

---

### ✅ How to Run

```bash
python -m unittest discover tests/
