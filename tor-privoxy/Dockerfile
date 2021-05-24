FROM alpine:3.7

EXPOSE 8118 9050 9051

RUN apk --update add privoxy tor runit tini

COPY service /etc/service/
ENV  C_FORCE_ROOT=true
ENTRYPOINT ["tini", "--"]
CMD ["runsvdir", "/etc/service"]
