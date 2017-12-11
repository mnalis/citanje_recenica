USER=mnalis1

check: hrvatski.in
	@! grep '^[A-Z]' $< | sort | uniq -dc | grep .
	@./dictcheck.pl $<

publish: check
	git commit -a || true
	git push

update:
	chown -R $(USER) .git/ *.in *.cgi *.pl
	umask 022 && env -i setuidgid $(USER) git pull
	chmod a+r index.html

.PHONY: all check publish update
