FROM python
ENV PATH /usr/local/bin:$PATH
ADD . /
WORKDIR /
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install opencv-python-headless
RUN pip install -r requirements.txt
CMD ["python", "app.py"]