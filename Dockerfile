FROM python:3.8-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD backend .
# 声明端口
EXPOSE 8000
# Run the application:
CMD ["uvicorn", "--app-dir", "/","main:app","--host", "0.0.0.0", "--port", "8000"]