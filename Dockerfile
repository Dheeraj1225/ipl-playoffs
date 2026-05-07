# Step 1: Use an official Python base image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the rest of your application code
COPY . .

# Step 5: Expose the port Streamlit runs on (default is 8501)
EXPOSE 8501

# Step 6: Command to run the app
ENTRYPOINT ["streamlit", "run", "predict.py", "--server.port=8501", "--server.address=0.0.0.0"]