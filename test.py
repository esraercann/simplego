 def transform_from_html_file(self, template_html_file: Literal["tabular_template.html", "card_template.html"], content: Optional[Content] = None):
            from jinja2 import Environment, FileSystemLoader
            from jinja2.exceptions import UndefinedError

            env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True)
            template = env.get_template(template_html_file)

            rendered_html_text = ""
            if template_html_file == "tabular_template.html":
                result_html = self.df.to_html(index=False).replace('class="dataframe"', 'class="table table-dark"') \
                    .replace('<th>', '<th scope="col" style="font-size:20px;">') \
                    .replace('<td>', '<td style="color: orange; font-size:20px;">') \
                    .replace('text-align: right;', 'text-align: left;')

                rendered_html_text = template.render(content=result_html, metadata=self._preserved_expr())

                return rendered_html_text
            elif template_html_file == "card_template.html":
                for card in content.message:
                    card.title = self._convert_emojis_to_unicode(card.title)
                    for item in card.items:
                        try:
                            item.value = self._format_value(self.df[item.value].values[0], item.value_format)
                        except KeyError as e:
                            raise PidgeyPlatformException(status_code=404, message=f"{e} column not found")
                try:
                    rendered_html_text = template.render(cards=content.message, format=content.card_format)
                except UndefinedError as e:
                    raise PidgeyPlatformException(status_code=400, message=e.message)

            return rendered_html_text
