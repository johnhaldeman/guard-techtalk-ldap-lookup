FROM sdk_base
MAINTAINER IBM
EXPOSE 5000
WORKDIR /app
ADD . /app
RUN chmod +x /app/docker/install_guard_dependencies.sh
RUN /app/docker/install_guard_dependencies.sh
RUN mkdir /store
RUN	mkdir /store/log
RUN touch /store/log/app.log
RUN chmod a+rw /store/log/app.log
VOLUME ["/store"]
RUN rm -rf /app/store && ln -s /store /app/store
ENTRYPOINT ["python", "/app/run.py"]
