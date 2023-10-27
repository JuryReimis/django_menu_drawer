from django import template

from menu_drawer.models import ParentalRelation

register = template.Library()


@register.inclusion_tag('menu_drawer/menu.html', takes_context=True)
def draw_menu(context, menu_name, *args, **kwargs):
    def get_tree(root_node: ParentalRelation):
        tree = {
            'node': root_node,
            'children': []
        }
        root_node.active = True
        for child in menu:
            if child.parent == root_node.menu_item:
                tree['children'].append(get_tree(child))
        return tree

    def convert_tree_in_list(tree):
        children = tree.get('children')
        tree_node = tree.get('node')
        if children:
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
    selected_point = context.request.resolver_match.kwargs.get('slug')
    root_nodes = []
    for node in [node for node in menu if node.parent is None]:
        root_nodes.append(convert_tree_in_list(get_tree(node)))

    context = {
        'slug': selected_point,
        'root_nodes': root_nodes
    }
    return context
