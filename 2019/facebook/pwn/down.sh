mkdir $2 && wget $1 -O $2.tar.gz && tar -xvzf $2.tar.gz -C $2 && mv $2/dist/* $2 && rm -r $2/dist && rm $2.tar.gz
