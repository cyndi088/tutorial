from django.db import models
from pygments import highlight
from pygments.lexers import get_all_lexers
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    title = models.CharField(max_length=100, blank=True, default='', verbose_name='标题')
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE, verbose_name='创建者')
    code = models.TextField(verbose_name='代码')
    highlighted = models.TextField(verbose_name='代码HTML格式')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100, verbose_name='语言')
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100, verbose_name='风格')

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created']
        verbose_name_plural = 'Snippets'  # 首页列表的显示名称（模型类重命名复数）
        verbose_name = 'Snippet'  # 列表页和详情页的显示名称（模型类实例对象）
