FROM  lsstsqre/lsst-texmf:latest

# Upgrade pip to latest version
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip --version

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt* ./

# Install Python dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Copy Python and LaTeX source files
COPY . .

# Make the build script executable
RUN chmod +x /app/build.sh

# Command to run make clean and make when container starts
#CMD ["sh", "-c", "make clean && make"]
CMD ["./build.sh"]
