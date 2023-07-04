from django import template

register = template.Library()


@register.filter()
def enumerate_items(items):
    return enumerate(items)


@register.filter()
def distribute_dishes(menu_list: list):
    menu_lenght = len(menu_list)
    final_res = []
    counter = 0
    if menu_lenght % 3 == 0:
        while counter != menu_lenght:
            final_res.append([
                menu_list.pop(0),
                menu_list.pop(0),
                menu_list.pop(0),
            ])
            counter += 3
            continue
    else:
        while counter != menu_lenght:
            if menu_lenght - counter < 3:
                the_rest = menu_lenght - counter
                last_diches = []
                for i in range(the_rest):
                    last_diches.append(menu_list.pop(0))
                else:

                    final_res.append(last_diches)
                    break

            final_res.append([
                menu_list.pop(0),
                menu_list.pop(0),
                menu_list.pop(0),
            ])
            counter += 3
            continue

    return final_res


@register.filter()
def get_index(value, arg):
    try:
        return value[arg]
    except (IndexError, KeyError, TypeError):
        return ''
