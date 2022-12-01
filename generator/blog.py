from datetime import datetime
from glob import glob
import pathlib
import re

from helper import create_jinja_env

env = create_jinja_env()
template = env.get_template("blog-post.html")

post_files = glob("./blog/**")

pathlib.Path("build/blog").mkdir(parents=True, exist_ok=True)

posts = []

for post_file in post_files:
    with open(post_file) as f:
        post_date_raw = re.search(r'([0-9]{8})', post_file).group()
        post_date = datetime.strptime(post_date_raw, '%Y%m%d')
        post_date_formatted = post_date.strftime("%d/%m/%Y")

        post_file_contents = f.read()
        post_title = re.search("<h1>(.*)</h1>", post_file_contents, re.DOTALL).group(1)
        post_summary = re.search("<summary>(.*)</summary>", post_file_contents, re.DOTALL).group(1)
        post_article = re.search("<article>(.*)</article>", post_file_contents, re.DOTALL).group(1)
        post_page = template.render(
            title=post_title,
            article=post_article,
            date=post_date_formatted,
        )

        out_file_name = post_file[2:]

        posts.append({
            "date": post_date_formatted,
            "date_raw": int(post_date_raw),
            "title": post_title,
            "summary": post_summary,
            "link": out_file_name,
        })

        with open("build/" + out_file_name, "w") as of:
            of.write(post_page)

index_template = env.get_template("blog-index.html")

ordered_posts = sorted(posts, key=lambda x: x["date_raw"], reverse=True)

with open("build/blog.html", "w") as of:
    rendered_index = index_template.render(posts=ordered_posts)
    of.write(rendered_index)
