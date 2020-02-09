from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('src/templates')
env = Environment(loader=file_loader)
template = env.get_template('publicity.html')
result = template.render(
    year='2020',
    other_year='2019',
    other_year_link='2019'
)
with open('build/publicity.html', 'a') as f:
    f.write(result)
