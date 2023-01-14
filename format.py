
import os
import json
import shutil


title, section = '', ''


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)



files = ["index", "next", "prev"]

templates = {}

# load in the templates
for file in files :
    with open(f"templates/{file}.html") as f:
        templates[file] = f.read()


# file structure: sike.pona.la/jan/kala-pona/embed.html


if os.path.exists("jan"):
    shutil.rmtree("jan")
os.makedirs("jan")


# load in the jans
with open('jan.json') as json_file:
    jan_data = json.load(json_file)

    # load in our main page

    content = ""

    with open("index_template.html") as f:
        content = f.read()

    with open("index.html", 'w') as f:
        jan_list = ""
        for jan in jan_data:
            jan_list += f'<a href="{jan["url"]}">{jan["name"]}</a>'

        content = content.replace("{{ jan }}", jan_list)
        f.write(content)

    # sike.pona.la/jan
    with cd("jan"):

        for nanpa in range(0, len(jan_data)):
            # make their folder
            if os.path.exists(jan_data[nanpa]["name"]):
                shutil.rmtree(jan_data[nanpa]["name"])
            os.makedirs(jan_data[nanpa]["name"])

            # sike.pona.la/jan/name
            with cd(jan_data[nanpa]["name"]):

                # index of previous person and next person
                nanpa_next = nanpa + 1 if nanpa < len(jan_data) - 1 else 0
                nanpa_prev = nanpa - 1 if nanpa > 0 else len(jan_data) - 1

                # links to go to the previous and next person's profiles
                nextlink = jan_data[nanpa_next]["url"]
                prevlink = jan_data[nanpa_prev]["url"]

                # create the files
                for file in files:

                    # embed.html, prev.html, next.html
                    destination = f"{file}.html"

                    # write the html and save
                    with open(destination, 'w') as f:
                        output = templates[file]

                        output = output.replace("{{ prevlink }}", prevlink)
                        output = output.replace("{{ nextlink }}", nextlink)
                        f.write(output)

                # # update data json dict
                #
                # if title not in article_data.keys():
                #     article_data[title] = {}
                # article_data[title]["title"] = title
                # article_data[title]["index"] = int(os.path.splitext(file_name)[0].split('_')[0])
                # article_data[title]["tags"] = tags
                #
                #
                #
                #
                # json_string = json.dumps(article_data)
                #
                # with open('scripts/articles.json', 'w') as outfile:
                #     outfile.write(json_string)



# rebuild the article pages
# rebuild tag pages
# rebuild user pages
