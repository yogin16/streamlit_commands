FROM python:3.6.5
RUN mkdir -p /streamlit_commands
WORKDIR /streamlit_commands

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./ ./

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONPATH=/streamlit_commands

# otherwise it doesn't start the app in contaier
RUN mkdir -p /root/.streamlit
RUN cp credentials.toml /root/.streamlit/credentials.toml
RUN cp config.toml /root/.streamlit/config.toml

CMD ["/bin/bash"]