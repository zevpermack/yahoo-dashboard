FROM public.ecr.aws/lambda/python:3.12

ENV LAMBDA_TASK_ROOT=/var/task

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY constants.py ${LAMBDA_TASK_ROOT}

# Avoid cache purge by adding requirements first
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install --no-cache-dir -r requirements.txt

ARG DB_HOST
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DEVELOPMENT
ARG SUPABASE_URL
ARG SUPABASE_KEY

ENV DB_HOST $DB_HOST
ENV DB_NAME $DB_NAME
ENV DB_USER $DB_USER
ENV DB_PASSWORD $DB_PASSWORD
ENV DEVELOPMENT $DEVELOPMENT
ENV SUPABASE_URL $SUPABASE_URL
ENV SUPABASE_KEY $SUPABASE_KEY

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
