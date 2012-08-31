RELEASEVER=$(shell date +%Y-%m-%d-%H-%M)
RELEASENAME=shogun-$(RELEASEVER)
RELEASEMEDIADIR=static
RELEASETOP=releases
RELEASEDIR:=$(RELEASETOP)/$(RELEASENAME)

WEBSITENAME=shogun
WEBSITEMEDIADIR:=/home/shogun/static/
WEBSITEDJANGODIR:=/home/shogun/django
WEBSITERELEASEDIR=$(WEBSITEDJANGODIR)/$(RELEASENAME)

run:
	python manage.py runserver

release: clean
	rm -rf $(RELEASEDIR)
	rsync -av . $(RELEASEDIR) --exclude '.git' --exclude 'releases' --exclude 'static'
	rsync -azv --progress --delete \
		$(RELEASEDIR) shogun@shogun-toolbox.org:$(WEBSITEDJANGODIR)
	rsync -azv --progress --delete \
		$(RELEASEMEDIADIR)/ shogun@shogun-toolbox.org:$(WEBSITEMEDIADIR)
	ssh shogun@shogun-toolbox.org \
		\( sed -i -e '"s/^PRODUCTION = False/PRODUCTION = True/g"' \
		$(WEBSITERELEASEDIR)/shogun/settings.py \; \
		cat django/settings_override.py '>>' $(WEBSITERELEASEDIR)/shogun/settings.py \; \
		python -mcompileall $(WEBSITERELEASEDIR)/ \; \
		find $(WEBSITERELEASEDIR) -type d -exec chmod 755 {} '\;' \; \
		find $(WEBSITERELEASEDIR) -type f -exec chmod 644 {} '\;' \; \
		chmod 640 $(WEBSITERELEASEDIR)/shogun/settings.py\* \; \
		cd $(WEBSITEDJANGODIR) \; rm -f $(WEBSITENAME) \; \
		ln -sf $(RELEASENAME) $(WEBSITENAME) \; \
		ln -sf $(WEBSITEMEDIADIR) $(WEBSITEMEDIADIR)/media \; \
		find $(WEBSITEMEDIADIR) -type d -exec chmod 755 {} '\;' \; \
		find $(WEBSITEMEDIADIR) -type f -exec chmod 644 {} '\;' \; \
		\)
	rm -rf $(RELEASEDIR)


clean:
	find ./ -name '*.pyc' -delete
	find ./ -name '*.swp' -delete

