#! /usr/bin/env python


fn_cfg = "./config.info"


def get_us_cfg():
	us_cfg = {}
	with open(fn_cfg, mode="r") as f:
		for line in f.readlines():
			str_pre, str, str_post = line.strip().partition(":")
			us_cfg[str_pre] = str_post
	return us_cfg
