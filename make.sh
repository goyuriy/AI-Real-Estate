#!/usr/bin/env sh
set -e

SERVICE_NAME=admin-web
COMPANY_NAME=webdevelop-pro

CMD=$1

case ${CMD} in
install)
  echo "Creating virtual envoiroment into venv folder"
  virtualenv --python=python3 venv
  source venv/bin/activate
  echo "Installing requirements"
  pip install -r requirements.txt
  pip install -r requirements-dev.txt
  echo "Copy pre commit hook"
  echo './make.sh lint' >> .git/hooks/pre-commit
  chmod +x .git/hooks/pre-commit
  ;;

lint)
  pylint admin/ tests/
  ;;

bandit)
  bandit --exclude ./venv -ll -r ./
  if [ $? -ne 0 ]; then
    exit 1
  fi
  ;;

container-scan)
  snyk container test cr.webdevelop.us/$COMPANY_NAME/$SERVICE_NAME:latest
  ;;

deploy-dev)
  BRANCH_NAME=`git rev-parse --abbrev-ref HEAD`
  SHORT_SHA=`git rev-parse --short HEAD`
  echo $BRANCH_NAME, $SHORT_SHA
  docker build -t cr.webdevelop.us/$COMPANY_NAME/$SERVICE_NAME:$SHORT_SHA -t cr.webdevelop.us/$COMPANY_NAME/$SERVICE_NAME:latest-dev --platform=linux/amd64 .
  # snyk container test cr.webdevelop.us/$COMPANY_NAME/$SERVICE_NAME:$SHORT_SHA
  if [ $? -ne 0 ]; then
    echo "===================="
    echo "snyk has found a vulnerabilities, please consider choosing alternative image from snyk"
    echo "===================="
  fi
  docker push cr.webdevelop.us/$COMPANY_NAME/$SERVICE_NAME:$SHORT_SHA
  docker push cr.webdevelop.us/$COMPANY_NAME/$SERVICE_NAME:latest-dev
  kubectl -n webdevelop-dev set image deployment/$SERVICE_NAME $SERVICE_NAME=cr.webdevelop.us/$COMPANY_NAME/$SERVICE_NAME:$SHORT_SHA
  ;;

unit)
  python -m pytest -vv -s tests/unit/*.py
  ;;

test)
  python -m pytest tests/unit_test.py &&
  python tests/integration_test.py
  ;;

help)
  @echo "Run cloud-config | install | lint | help"
  ;;

run-dev)
  yes 'yes' | python admin/manage.py collectstatic
  ./admin/manage.py runserver
  ;;

run)
  cd ./admin/
  ./manage.py collectstatic --no-input && ./manage.py migrate easy_thumbnails && gunicorn admin.wsgi --bind $HOST:$PORT --workers 5
  ;;
*)
  echo 'not found, use help to get a list of valid commands'
  exit 1
esac
