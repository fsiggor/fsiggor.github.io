FROM hugomods/hugo:0.159.1

COPY . /src

RUN hugo mod get

EXPOSE 1313

CMD ["hugo", "server", "-D", "--bind", "0.0.0.0"]
