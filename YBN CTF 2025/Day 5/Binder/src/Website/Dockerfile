# Use a lightweight Python image
FROM python:3.12-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create restricted directories inside /app
RUN mkdir -p /app/data /app/user_pages /app/default_pages

# Create non-root user
RUN useradd -m appuser

# --- Permission Hardening for /app ---

# Root owns everything except appuser-specific folders
RUN chown -R root:root /app && \
    chmod -R 755 /app && \
    chown -R appuser:appuser /app/data /app/user_pages && \
    chmod -R 770 /app/data /app/user_pages && \
    chown -R root:root /app/default_pages && \
    chmod -R 755 /app/default_pages

# --- System Hardening ---
# Block read access to sensitive system directories
RUN chmod o-rx /root /boot /srv /opt || true

# DO NOT restrict library directories — Python requires them.
# Instead, remove write permissions but keep read/execute.
RUN chmod -R o-w /usr /lib /lib64 || true

# Minimal /etc permissions:
# - /etc must be searchable (x)
# - ld.so.conf, hosts, resolv.conf must be readable
RUN chmod o-rwx /etc/* || true && \
    chmod o+rx /etc && \
    chmod o+r /etc/hosts /etc/resolv.conf /etc/ld.so.conf || true

# Environment variables
ENV BOT_URL="http://binder-admin-bot:420/visit"
ENV FLASK_SECRET_KEY="changed_in_production"
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Switch to restricted user
USER appuser

# Expose port
EXPOSE 5000

# Run Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
