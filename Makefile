clean:
	rm -f strongs.sqlite

create_database:
	./manage.py syncdb --noinput
	./manage.py migrate --noinput
	./manage.py createsuperuser --username=root --email=root@strongs.de --noinput

make_fixtures:
	./manage.py create_users
	./manage.py create_posts
	./manage.py create_photos

all: clean create_database make_fixtures