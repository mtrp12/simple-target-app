FROM python:3-slim
RUN pip install flask==1.1.1
COPY app /simple_app/app/
COPY docs /simple_app/docs/
COPY tests /simple_app/tests/
COPY run_tests.sh run.py setup_db.py setup_db.sql start_app.sh /simple_app/
RUN mkdir /simple_app/data
RUN cd /simple_app && ./setup_db.py && ./run_tests.sh
CMD ["sh", "-c", "cd /simple_app && ./start_app.sh"]
