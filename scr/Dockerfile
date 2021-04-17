# docker build -t image_gfp_orcamento -f . .
# docker run -d -p 5001:5001 --rm --name container_gfp_orcamento image_gfp_orcamento
#
FROM python:3
COPY . /gfp_orcamento
WORKDIR /gfp_orcamento
RUN pip install --no-cache-dir -r static/requirements.txt
CMD python -m flask run --host=0.0.0.0 --port=5001