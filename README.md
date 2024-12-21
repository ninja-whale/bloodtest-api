## Blood Test Management API

This is a Django-based REST API for managing blood test results with features like test creation, fetching, batch uploads, and statistics aggregation.

### Features
1. **Endpoints**:
   - `POST /api/tests/`: Create a new blood test record.
   - `GET /api/tests/?patient_id=<id>`: Retrieve all tests for a specific patient.
   - `GET /api/tests/stats/`: Retrieve aggregated test statistics.
   - `POST /api/tests/batch-upload/`: Batch upload test results using a CSV file.

2. **Key Functionalities**:
   - Caching with Redis for statistics endpoint.
   - Validation for test values and data consistency.
   - Supports batch uploads via CSV.

3. **Unit Tests**:
   - Tests included for creating, retrieving, and fetching statistics for test records.

### Prerequisites
- Python 3.8+
- Redis server (for caching functionality)
- Postman or any REST API testing tool (optional, for testing endpoints)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ninja-whale/bloodtest-api.git
   cd bloodtest-api
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Redis server:
   ```bash
   redis-server
   ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Testing
Run the included unit tests:
```bash
python manage.py test
```

### Usage
Use Postman or curl to interact with the endpoints:
- Example for creating a test record:
  ```bash
  curl -X POST http://127.0.0.1:8000/api/tests/ \
       -H "Content-Type: application/json" \
       -d '{
           "patient_id": 123,
           "test_name": "Hemoglobin",
           "value": 13.5,
           "unit": "g/dL",
           "test_date": "2024-12-16T12:00:00Z",
           "is_abnormal": false
       }'
  ```

### Contributing
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to the branch:
   ```bash
   git push origin feature-name
   ```
4. Open a Pull Request.

### License
This project is licensed under the MIT License.
