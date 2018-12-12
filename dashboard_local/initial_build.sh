sed -e "s|apiHOST|https://girder.local.wholetale.org|g" \
    -e "s|dashboardHOST|https://dashboard.local.wholetale.org|g" \
    -e "s|dataOneHOST|https://dev.nceas.ucsb.edu/knb/d1/mn/v2|g" \
    -e "s|authPROVIDER|Globus|g" -i config/environment.js && \
npm -g install bower && \
unset NODE_ENV && npm -s install && \
bower install --allow-root
./node_modules/.bin/ember build --environment=production
