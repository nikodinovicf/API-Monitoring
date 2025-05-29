# ✅ Use Python 3.10 as the base image
FROM python:3.10

# ✅ Set the working directory inside the container
WORKDIR /app

# ✅ Copy all application files into the container
COPY . /app

# ✅ Install dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Expose the port on which the Flask API runs
EXPOSE 5050

# ✅ Start the application using an absolute path
CMD ["python", "/app/main.py"]
