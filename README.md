Setup:
1. Create and use this virtual environment for load_test.py script:
python3 -m venv venv
source venv/bin/activate
pip install requests
source venv/bin/activate

2. Run the system:
docker-compose up --build 

3. Simulate crash:
docker-compose stop account_service_1
docker-compose rm -f account_service_1
docker-compose up account_service_1
