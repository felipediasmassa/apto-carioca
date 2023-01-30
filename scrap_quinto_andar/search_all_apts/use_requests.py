from requests_html import HTMLSession

url = "https://www.quintoandar.com.br/alugar/imovel/rio-de-janeiro-rj-brasil?survey=profiling_survey_rent_v2&survey_origin=home"

session = HTMLSession()
response = session.get(url)


def render_and_get_links(scrolldown):

    response.html.render(sleep=10, scrolldown=scrolldown)

    container_xpath = "/html/body/div[1]/main/section[2]/div[2]/div/div[1]"

    apts = response.html.xpath(container_xpath, first=True)

    print(apts.absolute_links)

    return


for value in range(10):
    render_and_get_links(scrolldown=value)


"""
all_links = response.html.absolute_links
print(all_links)

apts_links = [link for link in all_links if "imovel/" in link]

for apt_link in apts_links:
    print(apt_link)

print(len(apts_links))
"""
