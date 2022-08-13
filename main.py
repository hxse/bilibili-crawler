#!/usr/bin/env python3
# coding: utf-8
import pdb

from playwright.sync_api import sync_playwright

import re
import json
import fire


def get_info(page):
    # page.screenshot(path=f"screenshot-{browser_type.name}.png")
    page.wait_for_selector(".cube-list li a.title", state="visible")
    elements = page.query_selector_all(".cube-list li a.title")
    data = []
    for element in elements:
        href = element.get_attribute("href")
        # print(element.get_attribute("title"))
        title = element.text_content()
        data.append({"url": "https:" + href, "title": title})
    return data


def wirte_json(fileName, data):
    with open(fileName, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def getBilibili(url):
    with sync_playwright() as p:
        for browser_type in [p.chromium]:
            browser = browser_type.launch(headless=False)
            page = browser.new_page()
            page.goto(url)

            data = []
            # page.wait_for_selector("span.be-pager-total", state="attached")
            # page.wait_for_selector("span.be-pager-total", state="visible")
            # state = page.is_visible(".be-pager-next")
            while 1:
                page.wait_for_timeout(3 * 1000)
                # page.wait_for_selector(".be-pager-next", state="attached")
                # page.wait_for_selector("span.be-pager-total", state="visible")

                state = page.query_selector(".be-pager-next").is_visible()

                pageData = get_info(page)
                data.extend(pageData)

                if not state:
                    break
                page.click(".be-pager-next")
            return json.dumps({"data": data})

            # page.wait_for_selector("span.be-pager-total", state="visible")
            # el = page.query_selector("span.be-pager-total")
            # # page.click("li.be-pager-next")
            # x = re.match("^共 (\d*) 页，$", el.text_content())
            # count = x.group(1)
            # print(count)

            # page.wait_for_selector(".be-pager-next")
            # nextState = page.query_selector(".be-pager-next").is_disabled()

            # data = []
            # for i in range(1, int(count) + 1):
            #     if i != 1:
            #         page.goto(url + f"?page={i}")

            #     pageData = get_info(page)
            #     data.extend(pageData)
            # print(data, len(data))

            # print(page.title())
            # browser.close()


if __name__ == "__main__":
    fire.Fire({"gb": getBilibili})
