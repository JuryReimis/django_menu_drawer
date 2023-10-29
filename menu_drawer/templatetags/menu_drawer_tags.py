from django import template

from menu_drawer.models import ParentalRelation

register = template.Library()


@register.inclusion_tag('menu_drawer/menu.html', takes_context=True)
def draw_menu(context, menu_name, *args, **kwargs):
    def get_tree(root_node: ParentalRelation, must_be_detailed=False):
        tree = {
            'node': root_node,
            'children': [],
            'active': False,
            'must_be_detailed': must_be_detailed
        }
        if root_node.menu_item.item_slug == selected_point:
            tree['active'] = True
            must_be_detailed = True
        else:
            must_be_detailed = False
        for child in menu:
            if child.parent == root_node.menu_item:
                child_tree = get_tree(child, must_be_detailed)
                if child_tree.get('active'):
                    tree['active'] = True
                tree['children'].append(child_tree)
        return tree

    def convert_tree_in_list(tree):
        children = tree.get('children')
        tree_node = tree.get('node')
        detailed = tree.get('active')
        if children and (detailed or tree.get('must_be_detailed')):
            tree_node.leaf = False
            yield tree_node
            yield 'open'
            for child in children:
                for element in convert_tree_in_list(child):
                    yield element
            yield 'close'
        else:
            tree_node.leaf = True
            yield tree_node

    menu = ParentalRelation.objects.filter(menu__menu_title=menu_name).select_related('menu', 'menu_item', 'parent')
    selected_point = context.request.GET.get('selected')
    url = context.request.path
    root_nodes = []
    for node in [node for node in menu if node.parent is None]:
        root_nodes.append(convert_tree_in_list(get_tree(node)))

    context = {
        'url': url,
        'root_nodes': root_nodes
    }
    return context
