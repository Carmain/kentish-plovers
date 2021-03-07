def get_or_none(class_model, **kwargs):
    try:
        return class_model.objects.get(**kwargs)
    except class_model.DoesNotExist:
        return None


def flush_session(request, keys):
    for key in keys:
        if key in request.session:
            del request.session[key]
