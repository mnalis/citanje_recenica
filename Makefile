check: hrvatski.in
	@! grep '^[A-Z]' $< | sort | uniq -dc | grep .
	@./dictcheck.pl $<

publish: check
	git commit -a
	git push

.PHONY: all check publish
