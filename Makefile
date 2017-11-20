USER=mnalis1

check: hrvatski.in
	@! grep '^[A-Z]' $< | sort | uniq -dc | grep .
	@./dictcheck.pl $<

publish: check
	git commit -a
	git push

update:
	umask 022 && env -i setuidgid $(USER) git pull

.PHONY: all check publish update
