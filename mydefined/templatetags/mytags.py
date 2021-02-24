from django import template
register = template.Library()


class CDR_split(template.Node):
    def __init__(self, value):
        self.value = template.Variable(value)

    def render(self, context):
        str_n = self.value.resolve(context)
        # 分割6个CDR
        cdr_list = str_n.split(" ")
        # 增加换行符修改每一个CDR的显示颜色
        final_str_light = "<span class='cdr1'>%s&nbsp;</span><span class='cdr2'>%s&nbsp;</span><span class='cdr3'>%s&nbsp;</span>" % (
            cdr_list[0], cdr_list[1], cdr_list[2])
        final_str_heavy = "<span class='cdr4'>%s&nbsp;</span><span class='cdr5'>%s&nbsp;</span><span class='cdr6'>%s&nbsp;</span>" % (
            cdr_list[3], cdr_list[4], cdr_list[5])
        final_str = final_str_light + final_str_heavy
        return final_str


@register.tag(name="cdrsplit")
def do_split(parse, token):
    try:
        # tag_name表示标签名
        # value是由标签传递的数据
        print(dir(token))
        print("tttttttttt", token.position)
        tag_name, value = token.split_contents()
        print(tag_name, "nnnnnnnnnnnnnnnnnn")
    except BaseException:
        raise template.TemplateSyntaxError("syntax")
    else:
        print("vvvvvvvvvvvvvvvv", value)
    return CDR_split(value)
